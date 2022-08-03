#!/usr/bin/env python
# Created at 2020/2/15
from typing import Tuple

import torch
import torch.nn as nn
import numpy as np
from torch.distributions import Normal, MultivariateNormal
from torch.nn import functional as F
import copy

def resolve_activate_function(name):
    if name.lower() == "relu":
        return nn.ReLU
    if name.lower() == "sigmoid":
        return nn.Sigmoid
    if name.lower() == "leakyrelu":
        return nn.LeakyReLU
    if name.lower() == "prelu":
        return nn.PReLU
    if name.lower() == "softmax":
        return nn.Softmax
    if name.lower() == "tanh":
        return nn.Tanh

class ICQConfig:
    """ base BCQ config"""
    def __init__(
            self,
            num_actions,
            state_dim,
            eval_eps=0.001,
            target_interval=20,
    ):
        self.state_dim = state_dim
        self.num_actions = num_actions
        self.eval_eps = eval_eps
        self.target_interval = target_interval


# Used for Box2D / Toy problems
class ICQ(nn.Module):
    def __init__(self, mix_model, config):
        super(ICQ, self).__init__()
        self.state_dim = config.state_dim
        self.num_actions = config.num_actions
        self.eval_eps = config.eval_eps
        self.mix_model = mix_model

        self.q1 = critic(self.state_dim, self.num_actions)
        self.q2 = critic(self.state_dim, self.num_actions)
        self.pi = actor(self.state_dim, self.num_actions)

    def get_block_size(self):
        return 1 # for vanilla bc, there is no need to make the context length

    def configure_optimizers(self, train_config):
        critic_optimizer = torch.optim.Adam([
                {'params': self.q1.parameters()},
                {'params': self.q2.parameters()},
            ], lr=train_config.learning_rate, betas=train_config.betas)
        actor_optimizer = torch.optim.Adam(self.pi.parameters(), lr=train_config.actor_lr, betas=train_config.betas)
        return critic_optimizer, actor_optimizer


class critic(nn.Module):
    def __init__(self, state_dim, num_actions):
        super(critic, self).__init__()
        self.state_dim = state_dim
        self.num_actions = num_actions

        self.q1 = nn.Linear(state_dim, 256)
        self.q2 = nn.Linear(256, 256)
        self.q3 = nn.Linear(256, num_actions)

    def forward(self, state):
        q = F.relu(self.q1(state))
        q = F.relu(self.q2(q))
        q = self.q3(q)

        return q

    def configure_optimizers(self, train_config):
        optimizer = torch.optim.Adam(self.parameters(), lr=train_config.learning_rate, betas=train_config.betas)
        print(optimizer)
        return optimizer


class actor(nn.Module):
    def __init__(self, state_dim, num_actions):
        super(actor, self).__init__()
        self.state_dim = state_dim
        self.num_actions = num_actions

        self.actor_q1 = nn.Linear(state_dim, 256)
        self.actor_q2 = nn.Linear(256, 256)
        self.actor_q3 = nn.Linear(256, num_actions)

    def forward(self, state):

        actor_q = F.relu(self.actor_q1(state))
        actor_q = F.relu(self.actor_q2(actor_q))
        actor_q = self.actor_q3(actor_q)

        # log_softmax_actor_q = F.log_softmax(actor_q, dim=1)
        return actor_q

    def configure_optimizers(self, train_config):
        optimizer = torch.optim.Adam(self.parameters(), lr=train_config.learning_rate, betas=train_config.betas)
        print(optimizer)
        return optimizer







