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

from framework.buffer import  SequentialDataset

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
        #self.writer = SummaryWriter(config.log_dir)
        self.writer = config.writer

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
        self.alpha = config.alpha

        self.n_correct = 0
        self.n_total = 0

    def update_target(self):
        for param, target_param in zip(self.raw_model.parameters(), self.target_model.parameters()):
            target_param.data.copy_(self.config.tau * param.data + (1 - self.config.tau) * target_param.data)

    def train(self, train_episodes, test_episodes, data_dir, num_agents, offline_iter):
        raw_model, config = self.raw_model, self.config
        raw_model.train(True)

        def run_epoch(split, dataset):
            is_train = split == 'train'
            loader = DataLoader(dataset, shuffle=True, pin_memory=True,
                                batch_size=config.batch_size, drop_last=True,
                                num_workers=self.config.num_workers)
            pbar = tqdm(enumerate(loader), total=len(loader))
            logger.info("***** Training Begin ******")
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

                with torch.set_grad_enabled(True):
                    w, b = self.raw_model.mix_model(s)

                with torch.no_grad():
                    target_q = torch.stack([self.target_model(o_next[:, :, j, :])[0]
                                          for j in range(config.num_agents)], dim=2)

                    if next_ava is not None:
                        target_q[next_ava == 0] = -1e8
                    actor = torch.stack([self.target_model(o_next[:, :, j, :])[1]
                                          for j in range(config.num_agents)], dim=2)
                    # next_action = actor.argmax(dim=-1, keepdim=True)
                    next_action = target_q.argmax(dim=-1, keepdim=True)

                    correct_actions = next_action.eq(cur_a).int()
                    self.n_correct += torch.sum(correct_actions)
                    self.n_total += torch.sum(torch.ones_like(next_action))

                    target_q = target_q.gather(-1, next_action)
                    q_total_next = w * target_q + b

                    expected_q_total = r[:, :, 0, :] + config.gamma * (1 - done.min(2)[0]) * q_total_next.squeeze(dim=-1)

                if is_train:
                    with torch.set_grad_enabled(True):
                        # Get current Q estimate
                        eval_q = torch.stack([raw_model(o[:, :, j, :])[0]
                                                            for j in range(config.num_agents)], dim=2)

                        current_q = eval_q.gather(-1, cur_a)

                        q_total_eval = w * current_q + b

                        bellman_error = F.smooth_l1_loss(q_total_eval.squeeze(dim=-1), expected_q_total.squeeze(dim=-1))

                        ### Add the CQL  loss
                        negative_sampling = torch.mean(torch.logsumexp(w * eval_q+b, -1))
                        dataset_expec = torch.mean(q_total_eval)

                        min_q_loss = (negative_sampling - dataset_expec)



                        loss = bellman_error + self.alpha * min_q_loss # + self.alpha * constrain_error


                    logger.info(" Training loss %f", loss.item())
                    # self.writer.add_scalar('loss', loss.item(), self.global_step)
                    self.global_step += 1

                    # Optimize the Q
                    self.optimizer.zero_grad()
                    loss.backward()
                    # actor_loss.backward()
                    grad_norm_clip = config.grad_norm_clip[0]
                    torch.nn.utils.clip_grad_norm_(raw_model.parameters(), grad_norm_clip)
                    self.optimizer.step()

                    pbar.set_description(
                        f"epoch {epoch + 1} iter {it}: train loss {loss.item():.5f} .")

        for epoch in range(config.max_epochs):
            bias = 0
            num_step = 20
            # record correct actions made in the dataset
            self.n_correct = 0
            self.n_total = 0
            for i in range(num_step):
                global_states, local_obss, actions, done_idxs, rewards, time_steps, next_global_states, next_local_obss, \
                next_available_actions = load_data(int(train_episodes/num_step), bias,
                                                   data_dir, n_agents=num_agents)
                offline_dataset = SequentialDataset(1, global_states, local_obss, actions, done_idxs, rewards,
                                                    time_steps,
                                                    next_global_states, next_local_obss, next_available_actions)
                run_epoch('train', offline_dataset)
                bias += int(train_episodes/num_step)
            self.global_step += 1
            accuracy = self.n_correct / self.n_total
            logger.info(f"Training epoch {epoch + 1}: accuracy {accuracy:.5f}.")
            self.writer.add_scalar("training accuracy", accuracy, offline_iter)

            if test_episodes != 0:
                self.n_correct = 0
                self.n_total = 0
                for i in range(num_step):
                    global_states, local_obss, actions, done_idxs, rewards, time_steps, next_global_states, next_local_obss, \
                    next_available_actions = load_data(int(test_episodes / num_step), bias,
                                                       data_dir, n_agents=num_agents)
                    offline_dataset = SequentialDataset(1, global_states, local_obss, actions, done_idxs, rewards,
                                                        time_steps,
                                                        next_global_states, next_local_obss, next_available_actions)
                    run_epoch('test', offline_dataset)
                    bias += int(test_episodes / num_step)
                accuracy = self.n_correct / self.n_total
                logger.info(f"Epoch {epoch + 1}: test accuracy {accuracy:.5f}.")
                self.writer.add_scalar("testing accuracy", accuracy, offline_iter)
        self.raw_model = raw_model

