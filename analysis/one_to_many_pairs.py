import os
import sys
import random
import seaborn as sns
from collections import Counter

import torch
import h5py
import numpy as np
import matplotlib.pyplot as plt


def get_state_action_pairs(src_path, map_name, quality, steps=1000):
    cur_size = 0

    data_path = os.path.join(src_path, map_name, quality)
    file_path = os.listdir(data_path)
    file_num = len(file_path)
    episode_ifchosen = np.zeros((file_num, 100000))

    state_action_dict = {}

    while(cur_size < steps):
        file_id = random.randint(0, file_num - 1)
        with h5py.File(os.path.join(data_path, file_path[file_id])) as data_file:
            step_cuts = data_file["step_cuts"]
            episode_num = step_cuts.shape[0] - 1
            episode_id = random.randint(0, episode_num - 1)
            if not episode_ifchosen[file_id][episode_id]:
                episode_length = step_cuts[episode_id + 1] - step_cuts[episode_id]
                if cur_size + episode_length < steps:
                    share_obs = np.array(data_file["share_observations"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    actions = np.array(data_file["actions"])[:, step_cuts[episode_id]:step_cuts[episode_id + 1], ...]
                else:
                    episode_length = steps - cur_size
                    share_obs = np.array(data_file["share_observations"])[:,
                                step_cuts[episode_id]:step_cuts[episode_id]+episode_length, ...]
                    actions = np.array(data_file["actions"])[:, step_cuts[episode_id]:step_cuts[episode_id]+episode_length, ...]
                agent_num = share_obs.shape[0]
                for agent in range(agent_num):
                    agent_episode_obs = share_obs[agent, ...]
                    agent_episode_actions = actions[agent, ...]
                    episode_length = agent_episode_obs.shape[0]
                    for step in range(episode_length):
                        agent_step_obs = str(agent_episode_obs[step, ...])
                        agent_step_action = agent_episode_actions[step, ...]
                        if agent_step_obs not in state_action_dict:
                            state_action_dict[agent_step_obs] = [agent_step_action]
                        else:
                            if agent_step_action not in state_action_dict[agent_step_obs]:
                                state_action_dict[agent_step_obs].append(agent_step_action)
                cur_size += episode_length
    return state_action_dict

def one_to_many_pairs_probablity(src_path, map_name, quality, steps=1000):
    state_action_dict = get_state_action_pairs(src_path, map_name, quality, steps)
    counter = np.zeros(50)
    for key in state_action_dict.keys():
        counter[len(state_action_dict[key])] += 1
    total_pairs = np.sum(counter)
    counter /= total_pairs
    print("map name: {} quality: {} X=1: {}, X=2: {}, X=3: {}, X=4: {}.".format(map_name, quality,
                                                                counter[1], counter[2], counter[3], counter[4]))


if __name__=="__main__":
    '''
    map_list = ['3m', '8m', '2s3z', '2s_vs_1sc', '3s_vs_4z', 'MMM', 'MMM2', 'so_many_baneling', '3s_vs_3z', '2m_vs_1z',
            'bane_vs_bane', '1c3s5z', '5m_vs_6m', '10m_vs_11m', '2c_vs_64zg', '8m_vs_9m', '3s_vs_5z', '25m', '3s5z',
                '3s5z_vs_3s6z', '27m_vs_30m', '6h_vs_8z', 'corridor']
    '''
    map_list = ['bane_vs_bane', 'corridor', '5m_vs_6m', '1c3s5z', '10m_vs_11m', '2c_vs_64zg', '8m_vs_9m', '3s_vs_5z', '25m', '3s5z',
                '3s5z_vs_3s6z', '27m_vs_30m', '6h_vs_8z']
    for map_name in map_list:
        one_to_many_pairs_probablity("/data/d4marl/hdf5_files/", map_name, "good")
        one_to_many_pairs_probablity("/data/d4marl/hdf5_files/", map_name, "poor")
        if map_name != "3m":
            one_to_many_pairs_probablity("/data/d4marl/hdf5_files/", map_name, "medium")


