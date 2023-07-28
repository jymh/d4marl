import os
import random

import torch
import h5py
import numpy as np

def movable_actions(src_path, map_name, quality, steps=1000):
    cur_size = 0

    data_path = os.path.join(src_path, map_name, quality)
    file_path = os.listdir(data_path)
    file_num = len(file_path)
    episode_ifchosen = np.zeros((file_num, 100000))

    movable_actions_num = 0
    functional_actions_num = 0

    with h5py.File(os.path.join(data_path, file_path[0])) as data_file:
        ava_actions = np.array(data_file["available_actions"])
        action_dim = ava_actions.shape[2]

    while (cur_size < steps):
        file_id = random.randint(0, file_num - 1)
        with h5py.File(os.path.join(data_path, file_path[file_id])) as data_file:
            step_cuts = data_file["step_cuts"]
            episode_num = step_cuts.shape[0] - 1
            episode_id = random.randint(0, episode_num - 1)
            if not episode_ifchosen[file_id][episode_id]:
                episode_length = step_cuts[episode_id + 1] - step_cuts[episode_id]
                if cur_size + episode_length < steps:
                    actions = np.array(data_file["actions"])[:, step_cuts[episode_id]:step_cuts[episode_id + 1], ...]
                else:
                    actions = np.array(data_file["actions"])[:,
                              step_cuts[episode_id]:step_cuts[episode_id] + episode_length, ...]
                agent_num = actions.shape[0]
                for agent in range(agent_num):
                    agent_episode_actions = actions[agent, ...]
                    episode_length = agent_episode_actions.shape[0]
                    for step in range(episode_length):
                        agent_step_action = agent_episode_actions[step][0]
                        if 3 < agent_step_action < action_dim - 2:
                            functional_actions_num += 1
                        else:
                            movable_actions_num += 1
                cur_size += episode_length
                episode_ifchosen[file_id][episode_id] = 1

    total_actions_num = movable_actions_num + functional_actions_num
    print("map name: {}, quality: {}, movable actions(%): {:.2f}, functional actions(%): {:.2f}".format(
        map_name, quality, movable_actions_num/total_actions_num * 100, functional_actions_num/total_actions_num * 100
    ))

if __name__=="__main__":
    map_list = ['3m', '8m', '2s3z', '2s_vs_1sc', '3s_vs_4z', 'MMM', 'MMM2', 'so_many_baneling', '3s_vs_3z', '2m_vs_1z',
                'bane_vs_bane', '1c3s5z', '5m_vs_6m', '10m_vs_11m', '2c_vs_64zg', '8m_vs_9m', '3s_vs_5z', '25m', '3s5z',
                '3s5z_vs_3s6z', '27m_vs_30m', '6h_vs_8z', 'corridor']
    for map_name in map_list:
        movable_actions("/data/d4marl/hdf5_files", map_name, "good")
        if map_name != "3m":
            movable_actions("/data/d4marl/hdf5_files", map_name, "medium")
        movable_actions("/data/d4marl/hdf5_files", map_name, "poor")

