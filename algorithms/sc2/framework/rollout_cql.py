import torch
import numpy as np
import torch.nn.functional as F

def sample(model, raw_model, state, device, available_actions=None, sample=False):
    """
    take a conditioning sequence of indices in x (of shape (b,t)) and predict the next token in
    the sequence, feeding the predictions back into the model each time. Clearly the sampling
    has quadratic complexity unlike an RNN that is only linear, and has a finite context window
    of block_size, unlike an RNN that has an infinite context window.
    """
    model.eval()

    q, actor_q = model(state)
    # pluck the logits at the final step and scale by temperature
    # apply softmax to convert to probabilities

    if available_actions is not None:
        actor_q[available_actions == 0] = -1e8
        q[available_actions == 0] = -1e8

    # next_action = actor_q.argmax(-1, keepdim=False)
    next_action = q.argmax(-1, keepdim=False)

    if sample and np.random.uniform(0, 1) < model.eval_eps:
        probs = torch.ones_like(q)
        if available_actions is not None:
            probs[available_actions.squeeze(0) == 0] = 0.
        next_action = torch.multinomial(probs, num_samples=1)

    return next_action


class RolloutWorker:

    def __init__(self, model, buffer, context_length=1):
        self.buffer = buffer
        self.model = model
        self.context_length = context_length
        self.device = 'cpu'
        if torch.cuda.is_available() and not isinstance(self.model, torch.nn.DataParallel):
            self.device = torch.cuda.current_device()
            self.raw_model = model
            self.model = torch.nn.DataParallel(model).to(self.device)

    def rollout(self, env, ret, num_episodes, train=True, random_rate=1.0):
        self.model.train(False)

        T_rewards, T_wins = [], 0.
        for i in range(num_episodes):
            obs, share_obs, available_actions = env.real_env.reset()
            state = torch.from_numpy(obs).to(self.device)
            reward_sum = 0
            rtgs = np.ones((1, env.num_agents, 1)) * ret
            sampled_action = [
                sample(self.model, self.raw_model, state[:, j].unsqueeze(0),
                       device=self.device,
                       available_actions=torch.from_numpy(available_actions)[:, j].unsqueeze(0),
                       sample=train
                       )
                for j in range(env.num_agents)]

            actions = []
            all_states = state
            m = 0
            while True:
                action = [a.cpu().numpy()[0, -1] for a in sampled_action]
                actions += [action]

                cur_global_obs = share_obs
                cur_local_obs = obs
                cur_ava = available_actions

                obs, share_obs, rewards, dones, infos, available_actions = env.real_env.step([action])

                if train:
                    self.buffer.insert(cur_global_obs, cur_local_obs, action, rewards, dones, cur_ava)

                reward_sum += np.mean(rewards)
                m += 1
                if np.all(dones):
                    T_rewards.append(reward_sum)
                    if infos[0][0]['won']:
                        T_wins += 1.
                    break

                state = torch.from_numpy(obs).to(self.device)
                all_states = torch.cat([all_states, state], dim=0)
                sampled_action = [
                    sample(self.model, self.raw_model, state[:, j].unsqueeze(0),
                           device=self.device,
                           available_actions=torch.from_numpy(available_actions)[:, j].unsqueeze(0),
                           sample=train
                           )
                    for j in range(env.num_agents)]

        aver_return = np.mean(T_rewards)
        aver_win_rate = T_wins / num_episodes
        self.model.train(True)
        return aver_return, aver_win_rate