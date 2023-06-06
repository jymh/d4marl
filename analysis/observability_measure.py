import os
import random
import sys

import torch
import h5py
import numpy as np

sys.path.append("..")

from algorithms.sc2.envs.starcraft2.smac_maps import get_map_params


def MutualInfo(X, Y):
    d_x = dict()
    for x in X:
        if x in d_x:
            d_x[x] += 1
        else:
            d_x[x] = 1

    p_x = dict()
    for x in d_x.keys():
        p_x[x] = d_x[x] / len(X)

    d_y = dict()
    for y in Y:
        if y in d_y:
            d_y[y] += 1
        else:
            d_y[y] = 1

    p_y = dict()
    for y in d_y.keys():
        p_y[y] = d_y[y] / len(Y)


    d_xy = dict()
    for i in range(len(X)):
        if (X[i], Y[i]) in d_xy:
            d_xy[X[i], Y[i]] += 1
        else:
            d_xy[X[i], Y[i]] = 1

    p_xy = dict()
    for xy in d_xy.keys():
        p_xy[xy] = d_xy[xy] / len(X)

    mi = 0
    for xy in p_xy.keys():
        mi += p_xy[xy] * np.log(p_xy[xy] / (p_x[xy[0]] * p_y[xy[1]]))

    return mi

def observability_measure(src_path, map_name, quality, steps=1000):
    cur_size = 0

    data_path = os.path.join(src_path, map_name, quality)
    file_path = os.listdir(data_path)
    file_num = len(file_path)
    episode_ifchosen = np.zeros((file_num, 100000))

    agent_num = get_map_params(map_name)["n_agents"]
    str_share_obs = [[] for i in range(agent_num)]
    str_obs = [[] for i in range(agent_num)]

    while (cur_size < steps):
        file_id = random.randint(0, file_num - 1)
        with h5py.File(os.path.join(data_path, file_path[file_id])) as data_file:
            step_cuts = data_file["step_cuts"]
            episode_num = step_cuts.shape[0] - 1
            episode_id = random.randint(0, episode_num - 1)
            if not episode_ifchosen[file_id][episode_id]:
                episode_length = step_cuts[episode_id + 1] - step_cuts[episode_id]
                if cur_size + episode_length < steps:
                    share_obs = np.array(data_file["share_observations"])[:,
                                step_cuts[episode_id]:step_cuts[episode_id + 1], ...]
                    obs = np.array(data_file["observations"])[:, step_cuts[episode_id]:step_cuts[episode_id + 1], ...]
                else:
                    episode_length = steps - cur_size
                    share_obs = np.array(data_file["share_observations"])[:,
                                step_cuts[episode_id]:step_cuts[episode_id] + episode_length, ...]
                    obs = np.array(data_file["observations"])[:,
                              step_cuts[episode_id]:step_cuts[episode_id] + episode_length, ...]
                assert agent_num == share_obs.shape[0]
                for agent in range(agent_num):
                    agent_episode_shareobs = share_obs[agent, ...]
                    agent_episode_obs = obs[agent, ...]
                    episode_length = agent_episode_obs.shape[0]
                    for step in range(episode_length):
                        agent_step_shareobs = str(agent_episode_shareobs[step, ...])
                        agent_step_obs = str(agent_episode_obs[step, ...])
                        str_share_obs[agent].append(agent_step_shareobs)
                        str_obs[agent].append(agent_step_obs)
                cur_size += episode_length

    mean_mi = 0
    for agent in range(agent_num):
        mean_mi += MutualInfo(str_share_obs[agent], str_obs[agent])
    mean_mi /= agent_num

    print("map name: {}, quality: {}, mutual information: {:.2f}".format(map_name, quality, mean_mi))

if __name__=="__main__":
    map_list = ['3m', '8m', '2s3z', '2s_vs_1sc', '3s_vs_4z', 'MMM', 'MMM2', 'so_many_baneling', '3s_vs_3z', '2m_vs_1z',
                'bane_vs_bane', '1c3s5z', '5m_vs_6m', '10m_vs_11m', '2c_vs_64zg', '8m_vs_9m', '3s_vs_5z', '25m', '3s5z',
                '3s5z_vs_3s6z', '27m_vs_30m', '6h_vs_8z', 'corridor']
    for map_name in map_list:
        observability_measure("/data/d4marl/hdf5_files", map_name, "good")
        if map_name != "3m":
            observability_measure("/data/d4marl/hdf5_files", map_name, "medium")
        observability_measure("/data/d4marl/hdf5_files", map_name, "poor")
