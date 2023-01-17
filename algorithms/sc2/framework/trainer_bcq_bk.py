"""
Simple training loop; Boilerplate that could apply to any arbitrary neural network,
so nothing in this file really has anything to do with GPT specifically.
"""

import math
import logging
import torch
import copy
import numpy as np
from tqdm import tqdm
from torch.utils.data.dataloader import DataLoader
from torch.nn import functional as F
from tensorboardX.writer import SummaryWriter
from framework.utils import load_data

from framework.buffer import SequentialDataset

logger = logging.getLogger(__name__)


class TrainerConfig:
    """ base BCQ config"""
    betas = (0.9, 0.95)
    gamma = 0.99
    optimizer = "Adam"
    tau = 0.005
    grad_norm_clip = 1.0,

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Trainer:

    def __init__(self, model, config):
        self.model = model
        self.config = config
        self.writter = SummaryWriter(config.log_dir)

        # take over whatever gpus are on the system
        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            self.model = torch.nn.DataParallel(self.model).to(self.device)

        self.raw_model = self.model.module if hasattr(self.model, "module") else self.model
        self.optimizer = self.raw_model.configure_optimizers(config)

        self.target_model = copy.deepcopy(self.raw_model)
        self.target_model.train(False)
        self.global_step = 0

    def update_target(self):
        for param, target_param in zip(self.raw_model.parameters(), self.target_model.parameters()):
            target_param.data.copy_(self.config.tau * param.data + (1 - self.config.tau) * target_param.data)


    def train(self, episodes, data_dir, num_agents):
        raw_model, config = self.raw_model, self.config
        raw_model.train(True)

        def run_epoch(dataset):
            loader = DataLoader(dataset, shuffle=True, pin_memory=True,
                                batch_size=config.batch_size, drop_last=True,
                                num_workers=self.config.num_workers)
            pbar = tqdm(enumerate(loader), total=len(loader))
            logger.info("***** Trainging Begin ******")
            for it, (s, o, pre_a, r, t, s_next, o_next, cur_a, next_ava) in pbar:
                # [step_size, context_length, num_agents, data_dim]
                s = s.to(self.device)
                o = o.to(self.device)
                r = r.to(self.device)
                s_next = s_next.to(self.device)
                o_next = o_next.to(self.device)
                cur_a = cur_a.to(self.device)
                next_ava = next_ava.to(self.device)
                done = s.eq(s_next.data)
                done = done.min(-1)[0].unsqueeze(-1).detach().long()

                with torch.no_grad():
                    next_q = torch.stack([raw_model(o_next[:, :, j, :])[0]
                                                                 for j in range(config.num_agents)], dim=2)
                    next_actor_q = torch.stack([raw_model(o_next[:, :, j, :])[1]
                                                                 for j in range(config.num_agents)], dim=2)
                    if next_ava is not None:
                        next_q[next_ava == 0] = -1e8
                        next_actor_q[next_ava == 0] = -1e8

                    next_softmax_actor_q = F.softmax(next_actor_q, dim=3)
                    candidate_a = (next_softmax_actor_q / next_softmax_actor_q.max(dim=3, keepdim=True).values
                                   > raw_model.threshold).float()

                    next_action = (candidate_a * next_softmax_actor_q +
                                   (torch.ones(1, 1, 1, 1).to(self.device) - candidate_a) * -1e8).argmax(3, keepdim=True)

                    next_q = torch.stack([self.target_model(o_next[:, :, j, :])[0]
                                             for j in range(config.num_agents)], dim=2)
                    next_q = next_q.gather(-1, next_action)

                with torch.set_grad_enabled(True):
                    # Get current Q estimate
                    current_q = torch.stack([raw_model(o[:, :, j, :])[0]
                                                        for j in range(config.num_agents)], dim=2)
                    current_actor_q = torch.stack([raw_model(o[:, :, j, :])[1]
                                                        for j in range(config.num_agents)], dim=2)
                    current_q = current_q.gather(3, cur_a)

                    # Compute Q loss
                    q_total_eval = raw_model.mix_model(current_q, s)
                    q_total_next = self.target_model.mix_model(next_q, s_next)
                    expected_q_total = r[:, :, 0, :] + config.gamma * (1 - done.min(2)[0]) * q_total_next

                    q_loss = F.smooth_l1_loss(q_total_eval, expected_q_total)

                    i_loss = F.nll_loss(F.log_softmax(current_actor_q, dim=-1).reshape(-1, raw_model.num_actions),
                                        cur_a.reshape(-1))

                    loss = q_loss + i_loss + 1e-2 * current_actor_q.pow(2).mean()

                logger.info(" Training loss %f", loss.item())
                # self.writter.add_scalar('loss', loss.item(), self.global_step)
                self.global_step += 1

                # Optimize the Q
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                # report progress
                pbar.set_description(f"epoch {epoch + 1} iter {it}: train loss {loss.item():.5f}.")


        for epoch in range(config.max_epochs):
            bias = 0
            num_step = 20
            for i in range(num_step):
                global_states, local_obss, actions, done_idxs, rewards, time_steps, next_global_states, next_local_obss, \
                next_available_actions = load_data(int(episodes/num_step), bias,
                                                   data_dir, n_agents=num_agents)
                offline_dataset = SequentialDataset(1, global_states, local_obss, actions, done_idxs, rewards,
                                                    time_steps,
                                                    next_global_states, next_local_obss, next_available_actions)
                run_epoch(offline_dataset)
                bias += int(episodes/num_step)
            self.global_step += 1
        self.raw_model = raw_model

