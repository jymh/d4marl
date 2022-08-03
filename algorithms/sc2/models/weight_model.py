import torch.nn as nn
import torch
import torch.nn.functional as F


class QMixNet(nn.Module):
    def __init__(self, state_shape, n_agents, hyper_hidden_dim, num_action):
        super(QMixNet, self).__init__()
        self.state_shape = state_shape * n_agents  # concat state from agents
        self.n_agents = n_agents
        self.hyper_hidden_dim = hyper_hidden_dim
        self.num_action = num_action

        self.hyper_w = nn.Sequential(nn.Linear(self.state_shape, hyper_hidden_dim),
                                      nn.ReLU(),
                                      nn.Linear(hyper_hidden_dim, n_agents))

        self.hyper_b =nn.Sequential(nn.Linear(self.state_shape, hyper_hidden_dim),
                                     nn.ReLU(),
                                     nn.Linear(hyper_hidden_dim, 1)
                                     )

    def forward(self, states):
        # states: (batch_size, context_length, n_agents, state_shape)
        # q_values: (batch_size, context_length， n_agents, 1)
        batch_size = states.size(0)
        context_length = states.size(1)
        states = torch.cat([states[:, :, j, :] for j in range(self.n_agents)], dim=-1)
        states = states.reshape(-1, self.state_shape)  # (batch_size * context_length, state_shape)
        w = self.hyper_w(states).reshape(batch_size, context_length, self.n_agents, 1)

        b = self.hyper_b(states).reshape(batch_size, context_length, 1, 1)

        return torch.abs(w), b
