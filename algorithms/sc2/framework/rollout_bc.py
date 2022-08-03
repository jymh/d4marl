import torch
import numpy as np


def sample(model, x, temperature=1.0, sample=False, actions=None, rtgs=None, timesteps=None,
           available_actions=None):
    """
    take a conditioning sequence of indices in x (of shape (b,t)) and predict the next token in
    the sequence, feeding the predictions back into the model each time. Clearly the sampling
    has quadratic complexity unlike an RNN that is only linear, and has a finite context window
    of block_size, unlike an RNN that has an infinite context window.
    """
    if torch.cuda.is_available():
        block_size = model.module.get_block_size()
    else:
        block_size = model.get_block_size()
    model.eval()

    # x_cond = x if x.size(1) <= block_size else x[:, -block_size:] # crop context if needed
    x_cond = x if x.size(1) <= block_size//3 else x[:, -block_size//3:] # crop context if needed
    logits, _ = model(x_cond, actions=None, targets=None, rtgs=None, timesteps=timesteps)
    logits = logits
    # pluck the logits at the final step and scale by temperature
    if available_actions is not None:
        logits[available_actions == 0] = -1e8

    # sample from the distribution or take the most likely
    next_action = logits.argmax(-1, keepdim=False)
    return next_action

class RolloutWorker:

    def __init__(self, model, buffer):
        self.buffer = buffer
        self.model = model
        self.device = 'cpu'
        if torch.cuda.is_available() and not isinstance(self.model, torch.nn.DataParallel):
            self.device = torch.cuda.current_device()
            self.model = torch.nn.DataParallel(model).to(self.device)

    def rollout(self, env, ret, num_episodes, train=True):
        self.model.train(False)

        T_rewards, T_wins = [], 0.
        for i in range(num_episodes):
            obs, share_obs, available_actions = env.real_env.reset()
            state = torch.from_numpy(np.concatenate((share_obs, obs), axis=-1)).to(self.device)
            reward_sum = 0
            rtgs = np.ones((1, env.num_agents, 1)) * ret
            sampled_action = [
                sample(self.model, state[:, j].unsqueeze(0),
                       temperature=1.0, sample=train, actions=None,
                       rtgs=torch.tensor(rtgs[:, j], dtype=torch.long).to(self.device).unsqueeze(1).unsqueeze(-1),
                       timesteps=torch.zeros((1, 1), dtype=torch.int64).to(self.device),
                       available_actions=torch.from_numpy(available_actions)[:, j].unsqueeze(0)) for j in
                range(env.num_agents)]
            # prev_available_actions = available_actions
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

                rtgs = np.concatenate([rtgs, (rtgs[-1] - rewards[-1])[np.newaxis, :, :]], axis=0)
                state = torch.from_numpy(np.concatenate((share_obs, obs), axis=-1)).to(self.device)
                all_states = torch.cat([all_states, state], dim=0)
                sampled_action = [
                    sample(self.model, all_states[:, j].unsqueeze(0),
                           temperature=1.0, sample=train,
                           actions=torch.tensor(actions, dtype=torch.long)[:, j].to(self.device).unsqueeze(1).unsqueeze(0),
                           rtgs=torch.tensor(rtgs[:, j], dtype=torch.long).to(self.device).unsqueeze(0),
                           timesteps=(m * torch.ones((1, 1), dtype=torch.int64).to(
                               self.device)),
                           available_actions=torch.from_numpy(available_actions)[:, j].unsqueeze(0)) for j in
                    range(env.num_agents)]

                # prev_available_actions = available_actions

        aver_return = np.mean(T_rewards)
        aver_win_rate = T_wins / num_episodes
        self.model.train(True)
        return aver_return, aver_win_rate
