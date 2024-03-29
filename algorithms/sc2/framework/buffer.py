import torch
import copy
import glob
import h5py
import random
from tqdm import tqdm
import numpy as np
from torch.utils.data import Dataset
from .utils import padding_obs, padding_ava, get_episode


def list2array(input_list):
    return np.array(input_list)


class SequentialDataset(Dataset):

    def __init__(self, context_length, states, obss, actions, done_idxs, rewards, timesteps, next_states,
                 next_obss, next_available_actions):
        self.context_length = context_length
        self.states = states
        self.obss = obss
        self.next_states = next_states
        self.next_obss = next_obss
        self.actions = actions
        self.next_available_actions = next_available_actions
        # done_idx - 1 equals the last step's position
        self.done_idxs = done_idxs
        self.rewards = rewards
        self.timesteps = timesteps

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        context_length = self.context_length
        done_idx = idx + context_length
        for i in np.array(self.done_idxs)[:, 0].tolist():
            if i > idx:  # first done_idx greater than idx
                done_idx = min(int(i), done_idx)
                break
        idx = done_idx - context_length
        states = torch.tensor(np.array(self.states[idx:done_idx]), dtype=torch.float32)
        next_states = torch.tensor(np.array(self.next_states[idx:done_idx]), dtype=torch.float32)
        obss = torch.tensor(np.array(self.obss[idx:done_idx]), dtype=torch.float32)
        next_obss = torch.tensor(np.array(self.next_obss[idx:done_idx]), dtype=torch.float32)

        if idx == 0 or idx - 1 in self.done_idxs:
            padding = list(np.zeros_like(self.actions[idx]))
            pre_actions = np.array([padding] + self.actions[idx:done_idx - 1])
            pre_actions = torch.tensor(pre_actions, dtype=torch.int64)
        else:
            pre_actions = torch.tensor(self.actions[idx - 1:done_idx - 1], dtype=torch.int64)
        cur_actions = torch.tensor(self.actions[idx:done_idx], dtype=torch.int64)
        next_available_actions = torch.tensor(self.next_available_actions[idx:done_idx], dtype=torch.int64)

        # actions = torch.tensor(self.actions[idx:done_idx], dtype=torch.long)
        rewards = torch.tensor(self.rewards[idx:done_idx], dtype=torch.float32).unsqueeze(-1)
        timesteps = torch.tensor(self.timesteps[idx:idx+1], dtype=torch.int64)

        return states, obss, pre_actions, rewards, timesteps, next_states, next_obss, cur_actions, \
               next_available_actions

class ExpertDataSet(Dataset):
    def __init__(self, expert_data):
        self.state_size = np.shape(expert_data[0])[0]
        # self.expert_data = np.array(pd.read_csv(data_set_path))
        self.state = torch.tensor(torch.from_numpy(expert_data[0]), dtype=torch.float32)
        self.action = torch.tensor(torch.from_numpy(np.array(expert_data[1])), dtype=torch.float32)
        self.next_state = torch.tensor(torch.from_numpy(expert_data[0]), dtype=torch.float32)  # as the current state
        self.length = self.state_size

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return self.state[idx], self.action[idx]


class StateActionReturnDataset(Dataset):

    def __init__(self, data, block_size, actions, done_idxs, rtgs, timesteps):
        self.block_size = block_size
        self.data = data
        self.actions = actions
        self.done_idxs = done_idxs
        self.rtgs = rtgs
        self.timesteps = timesteps

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        block_size = self.block_size // 3
        done_idx = idx + block_size
        for i in self.done_idxs:
            if i > idx:  # first done_idx greater than idx
                done_idx = min(int(i), done_idx)
                break
        idx = done_idx - block_size
        states = torch.tensor(np.array(self.data[idx]), dtype=torch.float32)
        actions = torch.tensor(self.actions[idx], dtype=torch.long)
        rtgs = torch.tensor(self.rtgs[idx], dtype=torch.float32).unsqueeze(-1)
        timesteps = torch.tensor(self.timesteps[idx], dtype=torch.int64)

        return states, actions, rtgs, timesteps

class MadtStateActionReturnDataset(Dataset):

    def __init__(self, global_state, local_obs, block_size, actions, done_idxs, rewards, avas, v_values, rtgs, rets,
                 advs, timesteps):
        self.block_size = block_size
        self.global_state = global_state
        self.local_obs = local_obs
        self.actions = actions
        self.done_idxs = done_idxs
        self.rewards = rewards
        self.avas = avas
        self.v_values = v_values
        self.rtgs = rtgs
        self.rets = rets
        self.advs = advs
        self.timesteps = timesteps

    def __len__(self):
        # return len(self.global_state) - self.block_size
        return len(self.global_state)

    def stats(self):
        max_epi_len = max(np.array(self.done_idxs[1:]) - np.array(self.done_idxs[:-1]))
        min_epi_len = min(np.array(self.done_idxs[1:]) - np.array(self.done_idxs[:-1]))
        max_rtgs = max(self.rtgs)
        aver_epi_rtgs = np.mean([self.rtgs[i] for i in self.done_idxs[:-1]])
        print("max episode length: ", max_epi_len)
        print("min episode length: ", min_epi_len)
        print("max rtgs: ", max_rtgs)
        print("aver episode rtgs: ", aver_epi_rtgs)
        return max_epi_len, min_epi_len, max_rtgs, aver_epi_rtgs

    @property
    def max_rtgs(self):
        return max(self.rtgs)[0]

    def __getitem__(self, idx):
        context_length = self.block_size // 3
        done_idx = idx + context_length
        for i in self.done_idxs:
            if i > idx:  # first done_idx greater than idx
                done_idx = min(int(i), done_idx)
                break
        idx = done_idx - context_length
        states = torch.tensor(np.array(self.global_state[idx:done_idx]), dtype=torch.float32)
        obss = torch.tensor(np.array(self.local_obs[idx:done_idx]), dtype=torch.float32)

        if done_idx in self.done_idxs:
            next_states = [np.zeros_like(self.global_state[idx]).tolist()] + self.global_state[idx+1:done_idx] + \
                          [np.zeros_like(self.global_state[idx]).tolist()]
            next_states.pop(0)
            next_rtgs = [np.zeros_like(self.rtgs[idx]).tolist()] + self.rtgs[idx+1:done_idx] + \
                        [np.zeros_like(self.rtgs[idx]).tolist()]
            next_rtgs.pop(0)
        else:
            next_states = self.global_state[idx+1:done_idx+1]
            next_rtgs = self.rtgs[idx+1:done_idx+1]
        next_states = torch.tensor(next_states, dtype=torch.float32)
        next_rtgs = torch.tensor(next_rtgs, dtype=torch.float32)

        if idx == 0 or idx in self.done_idxs:
            pre_actions = [[0]] + self.actions[idx:done_idx-1]
        else:
            pre_actions = self.actions[idx-1:done_idx-1]
        pre_actions = torch.tensor(pre_actions, dtype=torch.long)
        actions = torch.tensor(self.actions[idx:done_idx], dtype=torch.long)

        rewards = torch.tensor(self.rewards[idx:done_idx], dtype=torch.float32)
        avas = torch.tensor(self.avas[idx:done_idx], dtype=torch.long)
        v_values = torch.tensor(self.v_values[idx:done_idx], dtype=torch.float32)
        rtgs = torch.tensor(self.rtgs[idx:done_idx], dtype=torch.float32)
        rets = torch.tensor(self.rets[idx:done_idx], dtype=torch.float32)
        advs = torch.tensor(self.advs[idx:done_idx], dtype=torch.float32)
        # timesteps = torch.tensor(self.timesteps[idx:idx+1], dtype=torch.int64)
        timesteps = torch.tensor(self.timesteps[idx:done_idx], dtype=torch.int64)

        dones = torch.zeros_like(rewards)
        if done_idx in self.done_idxs:
            dones[-1][0] = 1

        return states, obss, actions, rewards, avas, v_values, rtgs, rets, advs, timesteps, pre_actions, next_states, next_rtgs, dones


class ReplayBuffer:
    def __init__(self, n_agents, buffer_size, context_length):
        self.n_agents = n_agents
        self.buffer_size = buffer_size
        self.context_length = context_length

        self.data = []
        self.episode = [[] for i in range(self.n_agents)]

    @property
    def cur_size(self):
        return len(self.data)

    def insert(self, global_obs, local_obs, action, reward, done, available_actions):
        for i in range(self.n_agents):
            step = [global_obs[0][i], local_obs[0][i], [action[i]], reward[0][i], done[0][i], available_actions[0][i]]
            self.episode[i].append(step)
        if np.all(done):
            if self.cur_size >= self.buffer_size:
                del_count = self.cur_size - self.buffer_size + 1
                del self.data[:del_count]
            self.data.append(self.episode.copy())
            self.episode = [[] for i in range(self.n_agents)]

    def reset(self):
        self.data = []


class MadtReplayBuffer:

    def __init__(self, block_size, global_obs_dim, local_obs_dim, action_dim):
        self.block_size = block_size
        self.buffer_size = 5000
        self.global_obs_dim = global_obs_dim
        self.local_obs_dim = local_obs_dim
        self.action_dim = action_dim
        self.data = []
        self.episodes = []
        self.episode_dones = []
        self.gamma = 0.99
        self.gae_lambda = 0.95

    @property
    def size(self):
        return len(self.data)

    def insert(self, global_obs, local_obs, action, reward, done, available_actions, v_value):
        n_threads, n_agents = np.shape(reward)[0], np.shape(reward)[1]
        for n in range(n_threads):
            if len(self.episodes) < n+1:
                self.episodes.append([])
                self.episode_dones.append(False)
            if not self.episode_dones[n]:
                step_global_obs = np.expand_dims(global_obs[n], axis=1)
                step_local_obs = np.expand_dims(local_obs[n], axis=1)
                step_action = np.expand_dims(action[n], axis=1)
                step_reward = np.expand_dims(reward[n], axis=1)
                step_done = np.expand_dims(done[n], axis=1)
                step_available_actions = np.expand_dims(available_actions[n], axis=1)
                step_v_value = np.expand_dims(v_value[n], axis=1)
                if len(self.episodes[n]) == 0:
                    step = [step_global_obs.tolist(), step_local_obs.tolist(),
                            step_action.tolist(), step_reward.tolist(),
                            step_done, step_available_actions.tolist(),
                            step_v_value.tolist()]
                    self.episodes[n] = step
                else:
                    # concatenate on step dimension
                    self.episodes[n][0] = np.concatenate((np.array(self.episodes[n][0]), step_global_obs), axis=1).tolist()
                    self.episodes[n][1] = np.concatenate((np.array(self.episodes[n][1]), step_local_obs), axis=1).tolist()
                    self.episodes[n][2] = np.concatenate((np.array(self.episodes[n][2]), step_action), axis=1).tolist()
                    self.episodes[n][3] = np.concatenate((np.array(self.episodes[n][3]), step_reward), axis=1).tolist()
                    self.episodes[n][4] = np.concatenate((np.array(self.episodes[n][4]), step_done), axis=1).tolist()
                    self.episodes[n][5] = np.concatenate((np.array(self.episodes[n][5]), step_available_actions), axis=1).tolist()
                    self.episodes[n][6] = np.concatenate((np.array(self.episodes[n][6]), step_v_value), axis=1).tolist()
                if np.all(done[n]):
                    self.episode_dones[n] = True
                    if self.size > self.buffer_size:
                        raise NotImplementedError
                    if self.size == self.buffer_size:
                        del self.data[0]
                    self.data.append(copy.deepcopy(self.episodes[n]))
                    #print(self.data)
        if np.all(self.episode_dones):
            self.episodes = []
            self.episode_dones = []

    def reset(self, num_keep=0, buffer_size=5000):
        self.buffer_size = buffer_size
        if num_keep == 0:
            self.data = []
        elif self.size >= num_keep:
            keep_idx = np.random.randint(0, self.size, num_keep)
            self.data = [self.data[idx] for idx in keep_idx]

    # offline data size could be large than buffer size
    def load_offline_data(self, data_dir, offline_episode_num, offline_test_episodes, max_epi_length=400):
        map_id = 0
        for map_name in data_dir.keys():
            map_data_files = data_dir[map_name]
            accumulated_episodes = 0
            total_episodes = 0
            for j in range(len(map_data_files)):
                path_file = map_data_files[j]

                data_file = h5py.File(path_file, 'r')
                episodes_in_file = len(list(data_file['step_cuts'])) - 1
                total_episodes += episodes_in_file

            if offline_episode_num[map_id] + offline_test_episodes > total_episodes:
                raise ValueError("Required episodes larger than total {} episodes for map {}, please reduce offline "
                      "episodes.".format(total_episodes, map_name))
            for j in range(len(map_data_files)):
                path_file = map_data_files[j]
                data_file = h5py.File(path_file, 'r')
                episodes_in_file = len(list(data_file['step_cuts'])) - 1
                # for file in sorted(path_files):
                cnt = 0

                pbar = tqdm(total=offline_episode_num[map_id] + offline_test_episodes - accumulated_episodes,
                            desc="Loading offline data episodes", leave=False)

                while(accumulated_episodes <= offline_episode_num[map_id] + offline_test_episodes):
                    share_obs, obs, actions, rewards, terminals, ava_actions = get_episode(cnt, 0, data_file)

                    #print("Original dimension: obs {}, share_obs {}, available_actions {}.".format(
                    #    np.array(obs).shape[-1], np.array(share_obs).shape[-1], np.array(ava_actions).shape[-1]))
                    # padding obs
                    share_obs = padding_obs(share_obs, self.global_obs_dim)
                    obs = padding_obs(obs, self.local_obs_dim)
                    ava_actions = padding_ava(ava_actions, self.action_dim)

                    episode = [share_obs, obs, actions, rewards, terminals, ava_actions]

                    # self.data: (episode_num, attribute_num, agent_num, step_length, attribute_dim)
                    self.data.append(episode)

                    accumulated_episodes += 1
                    cnt += 1

                    pbar.update(1)
                    if cnt == episodes_in_file:
                        break
                pbar.close()
            map_id += 1

    def random_load_offline_data(self, data_dir, offline_episode_num, offline_test_episodes, max_epi_length=400):
        map_id = 0
        for map_name in data_dir.keys():
            map_data_files = data_dir[map_name]
            accumulated_episodes = 0
            file_num = len(map_data_files)
            episode_ifchosen = np.zeros((file_num, 100000))

            total_episodes = 0
            for j in range(len(map_data_files)):
                path_file = map_data_files[j]

                data_file = h5py.File(path_file, 'r')
                episodes_in_file = len(list(data_file['step_cuts'])) - 1
                total_episodes += episodes_in_file

            if offline_episode_num[map_id] + offline_test_episodes > total_episodes:
                raise ValueError("Required episodes larger than total {} episodes for map {}, please reduce offline "
                      "episodes.".format(total_episodes, map_name))


            while (accumulated_episodes <= offline_episode_num[map_id] + offline_test_episodes):
                file_id = random.randint(0, file_num - 1)
                with h5py.File(map_data_files[file_id]) as data_file:
                    step_cuts = data_file["step_cuts"]
                    episode_num = step_cuts.shape[0] - 1
                    episode_id = random.randint(0, episode_num - 1)
                    if not episode_ifchosen[file_id][episode_id]:
                        share_obs, obs, actions, rewards, terminals, ava_actions = get_episode(episode_id, 0, data_file)

                        # padding obs
                        #print("Original dimension: obs {}, share_obs {}, available_actions {}.".format(
                        #    np.array(obs).shape[-1], np.array(share_obs).shape[-1], np.array(ava_actions).shape[-1]))
                        share_obs = padding_obs(share_obs, self.global_obs_dim)
                        obs = padding_obs(obs, self.local_obs_dim)
                        ava_actions = padding_ava(ava_actions, self.action_dim)

                        episode = [share_obs, obs, actions, rewards, terminals, ava_actions]

                        # self.data: (episode_num, attribute_num, agent_num, step_length, attribute_dim)
                        self.data.append(episode)

                        accumulated_episodes += 1
                        episode_ifchosen[file_id][episode_id] = 1

            map_id += 1

    def sample(self):
        # adding elements with list will be faster
        global_states = []
        local_obss = []
        actions = []
        rewards = []
        avas = []
        v_values = []
        rtgs = []
        rets = []
        done_idxs = []
        time_steps = []
        advs = []

        for episode_idx in range(self.size):
            episode = self.preprocess_episode(episode_idx)
            # episode = self.get_episode(episode_idx, min_return)
            if episode is None:
                continue
            epi_share_obs, epi_obs, epi_actions, epi_rewards, epi_terminals, epi_ava_actions, \
                    epi_v, epi_rtg, epi_ret, epi_adv = episode
            num_agent = len(epi_share_obs)
            for i in range(num_agent):
                time_step = 0
                agent_share_obs = epi_share_obs[i]
                step_length = len(agent_share_obs)
                for j in range(step_length):
                    g = epi_share_obs[i][j]
                    o = epi_obs[i][j]
                    a = epi_actions[i][j]
                    r = epi_rewards[i][j]
                    d = epi_terminals[i][j]
                    ava = epi_ava_actions[i][j]
                    v = epi_v[i][j]
                    rtg = epi_rtg[i][j]
                    ret = epi_ret[i][j]
                    adv = epi_adv[i][j]
                    global_states.append(g)
                    local_obss.append(o)
                    actions.append(a)
                    rewards.append(r)
                    avas.append(ava)
                    v_values.append(v)
                    rtgs.append(rtg)
                    rets.append(ret)
                    advs.append(adv)
                    time_steps.append([time_step])
                    time_step += 1
                # done_idx - 1 equals the last step's position
                done_idxs.append(len(global_states))

        # or we can separate it as well
        # states = np.concatenate((global_states, local_obss), axis=1)
        dataset = MadtStateActionReturnDataset(global_states, local_obss, self.block_size, actions, done_idxs, rewards,
                                           avas, v_values, rtgs, rets, advs, time_steps)
        return dataset

    # from [g, o, a, r, d, ava]/[g, o, a, r, d, ava, v] to [g, o, a, r, d, ava, v, rtg, ret, adv]
    def preprocess_episode(self, index):
        episode = copy.deepcopy(self.data[index])
        if len(episode) == 6:  #offline
            share_obs, obs, actions, rewards, terminals, ava_actions = episode
            num_agent = np.shape(share_obs)[0]
            step_length = np.shape(share_obs)[1]
            values = [[] for i in range(num_agent)]
            offline_flag = True
        elif len(episode) == 7:  #online
            share_obs, obs, actions, rewards, terminals, ava_actions, values = episode
            num_agent = np.shape(share_obs)[0]
            step_length = np.shape(share_obs)[1]
            offline_flag = False
        else:
            raise NotImplementedError


        # TODO: handle online circumstances

        rtgs = [[] for i in range(num_agent)]
        rets = [[] for i in range(num_agent)]
        advs = [[] for i in range(num_agent)]
        for i in range(num_agent):
            rtg = 0.
            ret = 0.
            adv = 0.
            rewards_traj = rewards[i]
            if offline_flag:
                agent_values = values[i] = [[] for _ in range(step_length)]
            else:
                agent_values = values[i]
            agent_rtgs = rtgs[i] = [[] for _ in range(step_length)]
            agent_rets = rets[i] = [[] for _ in range(step_length)]
            agent_advs = advs[i] = [[] for _ in range(step_length)]
            for j in reversed(range(len(rewards_traj))):
                if offline_flag:
                    agent_values[j] = [0.] # offline, give a fake v_value, unused

                reward = rewards_traj[j][0]
                rtg += reward
                agent_rtgs[j] = [rtg]

                if j == len(rewards_traj) - 1:
                    next_v = 0.
                else:
                    next_v = agent_values[j+1][0]
                v = agent_values[j][0]
                # adv with gae
                delta = reward + self.gamma * next_v - v
                adv = delta + self.gamma * self.gae_lambda * adv

                # ret = adv + v
                ret = reward + self.gamma * ret

                agent_rets[j] = [ret]
                agent_advs[j] = [adv]

        # prune dead steps
        for i in range(num_agent):
            end_idx = 0
            for j in range(len(terminals[i])):
                if terminals[i][j]:
                    break
                else:
                    end_idx += 1
            share_obs[i] = share_obs[i][0: end_idx + 1]
            obs[i] = obs[i][0: end_idx + 1]
            actions[i] = actions[i][0: end_idx + 1]
            rewards[i] = rewards[i][0: end_idx + 1]
            terminals[i] = terminals[i][0: end_idx + 1]
            ava_actions[i] = ava_actions[i][0: end_idx + 1]
            values[i] = values[i][0: end_idx + 1]
            rtgs[i] = rtgs[i][0: end_idx + 1]
            rets[i] = rets[i][0: end_idx + 1]
            advs[i] = advs[i][0: end_idx + 1]

        episode = [share_obs, obs, actions, rewards, terminals, ava_actions, values, rtgs, rets, advs]
        return episode




