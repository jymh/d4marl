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
import itertools
from framework.utils import load_data
from framework.buffer import SequentialDataset

logger = logging.getLogger(__name__)


class TrainerConfig:
    """ base BCQ config"""
    # learning_rate = 0.0002
    betas = (0.9, 0.95)
    gamma = 0.99
    optimizer = "Adam"
    tau = 0.005
    grad_norm_clip = 1.0,
    alpha = 0.1
    actor_learning_rate = 1e-4

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Trainer:

    def __init__(self, model, config):
        self.model = model
        self.config = config
        # self.writter = SummaryWriter(config.log_dir)
        self.writter = config.writer
        # take over whatever gpus are on the system
        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            self.model = torch.nn.DataParallel(self.model).to(self.device)

        self.raw_model = self.model.module if hasattr(self.model, "module") else self.model
        self.optimizer, self.actor_optimizer = self.raw_model.configure_optimizers(config)

        self.target_model = copy.deepcopy(self.raw_model)
        self.target_model.q1.train(False)
        self.target_model.q2.train(False)
        self.global_step = 0
        self.alpha = config.alpha
        self.lamda = config.lamda
        self.mix_model = self.raw_model.mix_model

        # List of parameters for both Q-networks (save this for convenience)
        self.q_params = itertools.chain(self.raw_model.q1.parameters(),
                                        self.raw_model.q2.parameters(),
                                        self.mix_model.parameters())

    def update_target(self):
        for param, target_param in zip(self.raw_model.parameters(), self.target_model.parameters()):
            target_param.data.copy_(self.config.tau * param.data + (1 - self.config.tau) * target_param.data)

    def train(self, episodes, data_dir, num_agents):
        raw_model, config = self.raw_model, self.config
        raw_model.train(True)

        def run_epoch(dataset):
            loader = DataLoader(dataset, shuffle=False, pin_memory=True,
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

                # calculate mix parameter:
                with torch.set_grad_enabled(True):
                    w, b = self.mix_model(s)

                # calculate Q loss:
                with torch.no_grad():
                    target_q1 = torch.stack([self.target_model.q1(o_next[:, :, j, :])
                                             for j in range(config.num_agents)], dim=2)
                    target_q2 = torch.stack([self.target_model.q2(o_next[:, :, j, :])
                                             for j in range(config.num_agents)], dim=2)
                    target_q = torch.min(target_q1, target_q2)

                    if next_ava is not None:
                        target_q[next_ava == 0] = -100
                    next_actor = torch.stack([self.target_model.pi(o_next[:, :, j, :])
                                              for j in range(config.num_agents)], dim=2)
                    next_action = next_actor.argmax(dim=-1, keepdim=True)
                    beta = 10
                    target_q = target_q.gather(-1, next_action)
                    q_total_next = (w * target_q + b).sum(dim=2, keepdim=False).reshape(-1, 1)
                    backup = r[:, :, 0, :] + config.gamma * (1 - done.min(2)[0]) * q_total_next * F.softmax(
                        q_total_next / beta, dim=0).reshape(-1, 1)  # KL

                with torch.set_grad_enabled(True):
                    # Get current Q estimate
                    eval_q1 = torch.stack([raw_model.q1(o[:, :, j, :])
                                           for j in range(config.num_agents)], dim=2)
                    eval_q2 = torch.stack([raw_model.q2(o[:, :, j, :])
                                           for j in range(config.num_agents)], dim=2)

                    current_q1 = eval_q1.gather(-1, cur_a)
                    current_q2 = eval_q2.gather(-1, cur_a)

                    q1_total_eval = (w * current_q1 + b).sum(dim=2, keepdim=False).reshape(-1, 1)
                    q2_total_eval = (w * current_q2 + b).sum(dim=2, keepdim=False).reshape(-1, 1)

                    index = torch.zeros_like(q1_total_eval).to(self.device)

                    for i in range(1, index.shape[0]):
                        if done.min(2)[0].reshape(-1)[i] == 1:
                            index[i][0] = 0
                        else:
                            index[i][0] = index[i - 1][0] + 1

                    decay = torch.ones_like(q1_total_eval) * config.lamda * config.gamma
                    decay = torch.pow(decay, index)

                    loss_q1 = ((decay * (q1_total_eval - backup)) ** 2).mean()
                    loss_q2 = ((decay * (q2_total_eval - backup)) ** 2).mean()
                    loss_q = loss_q1 + loss_q2

                for p in self.q_params:
                    p.requires_grad = True
                self.optimizer.zero_grad()
                loss_q.backward()
                grad_norm_clip = config.grad_norm_clip[0]
                torch.nn.utils.clip_grad_norm_(raw_model.parameters(), grad_norm_clip)
                self.optimizer.step()

                # calculate the actor loss
                for p in self.q_params:
                    p.requires_grad = False
                w, b = self.mix_model(s)

                eval_q1 = torch.stack([raw_model.q1(o[:, :, j, :])
                                       for j in range(config.num_agents)], dim=2)

                eval_q2 = torch.stack([raw_model.q2(o[:, :, j, :])
                                       for j in range(config.num_agents)], dim=2)

                actor = torch.stack([self.raw_model.pi(o[:, :, j, :])
                                     for j in range(config.num_agents)], dim=2)
                pi_a = actor.argmax(dim=-1, keepdim=True)

                q1_pi = (w * eval_q1).gather(-1, pi_a)
                q2_pi = (w * eval_q2).gather(-1, pi_a)
                v_pi = torch.min(q1_pi, q2_pi)

                beta = 0.5
                q1_old_actions = (w * eval_q1).gather(-1, cur_a)
                q2_old_actions = (w * eval_q2).gather(-1, cur_a)
                q_old_actions = torch.min(q1_old_actions, q2_old_actions)
                adv_pi = q_old_actions - v_pi

                weights = F.softmax(adv_pi / beta, dim=0)  # KL

                loss_pi = (-F.log_softmax(actor, dim=-1).gather(-1, cur_a) * weights.shape[0] * weights.detach()).mean()

                for p in self.q_params:
                    p.requires_grad = True

                self.actor_optimizer.zero_grad()
                loss_pi.backward()
                grad_norm_clip = config.grad_norm_clip[0]
                torch.nn.utils.clip_grad_norm_(raw_model.parameters(), grad_norm_clip)
                self.actor_optimizer.step()
                # report progress
                pbar.set_description(
                    f"epoch {epoch + 1} iter {it}: q loss {loss_q.item():.5f} .pi loss {loss_pi.item():.5f} ")

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
