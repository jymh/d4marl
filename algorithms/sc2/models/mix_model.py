import torch.nn as nn
import torch
import torch.nn.functional as F


class QMixNet(nn.Module):
    def __init__(self, state_shape, n_agents, hyper_hidden_dim, qmix_hidden_dim):
        super(QMixNet, self).__init__()
        self.state_shape = state_shape * n_agents  # concat state from agents
        self.n_agents = n_agents
        self.hyper_hidden_dim = hyper_hidden_dim
        self.qmix_hidden_dim = qmix_hidden_dim

        self.hyper_w1 = nn.Sequential(nn.Linear(self.state_shape, hyper_hidden_dim),
                                      nn.ReLU(),
                                      nn.Linear(hyper_hidden_dim, n_agents * qmix_hidden_dim))
        self.hyper_w2 = nn.Sequential(nn.Linear(self.state_shape, hyper_hidden_dim),
                                      nn.ReLU(),
                                      nn.Linear(hyper_hidden_dim, qmix_hidden_dim))

        self.hyper_b1 = nn.Linear(self.state_shape, qmix_hidden_dim)
        self.hyper_b2 =nn.Sequential(nn.Linear(self.state_shape, qmix_hidden_dim),
                                     nn.ReLU(),
                                     nn.Linear(qmix_hidden_dim, 1)
                                     )

    def forward(self, q_values, states):
        # states: (batch_size, context_length, n_agents, state_shape)
        # q_values: (batch_size, context_length， n_agents, 1)
        batch_size = q_values.size(0)
        context_length = q_values.size(1)
        q_values = q_values.view(-1, 1, self.n_agents)  # (batch_size, 1, n_agent)

        states = torch.cat([states[:, :, j, :] for j in range(self.n_agents)], dim=-1)
        states = states.reshape(-1, self.state_shape)  # (batch_size * context_length, state_shape)

        w1 = torch.abs(self.hyper_w1(states))
        b1 = self.hyper_b1(states)

        w1 = w1.view(-1, self.n_agents, self.qmix_hidden_dim)  # (batch_size, n_agent, qmix_hidden_dim)
        b1 = b1.view(-1, 1, self.qmix_hidden_dim)  # (batch_size, 1, qmix_hidden_dim)

        hidden = F.elu(torch.bmm(q_values, w1) + b1)  # (batch_size, 1, qmix_hidden_dim)

        w2 = torch.abs(self.hyper_w2(states))
        b2 = self.hyper_b2(states)

        w2 = w2.view(-1, self.qmix_hidden_dim, 1)
        b2 = b2.view(-1, 1, 1)

        q_total = torch.bmm(hidden, w2) + b2
        q_total = q_total.view(batch_size, context_length, -1)
        return q_total
