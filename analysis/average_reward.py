import os
import sys
import random
import seaborn as sns

import torch
import h5py
import numpy as np
import matplotlib.pyplot as plt


def average_reward_in_chunk(src_path, map_name, episodes=100):
    cur_size = 0
    average_reward = []
    episode_ifchosen = {}
    data_path = os.path.join(src_path, map_name)
    qualities = os.listdir(data_path)
    num_qualities = len(qualities)
    for quality in qualities:
        quality_file_path = os.path.join(data_path, quality)
        quality_file_num = len(os.listdir(quality_file_path))
        episode_ifchosen[quality] = np.zeros((quality_file_num, 100000))


    while (cur_size < episodes):
        quality_id = random.randint(0, num_qualities - 1)
        quality = qualities[quality_id]
        quality_file_num = episode_ifchosen[quality].shape[0]
        quality_file_names = os.listdir(os.path.join(data_path, quality))
        file_id = random.randint(0, quality_file_num - 1)
        with h5py.File(os.path.join(data_path, quality, quality_file_names[file_id])) as data_file:
            step_cuts = data_file["step_cuts"]
            episode_num = step_cuts.shape[0] - 1
            episode_id = random.randint(0, episode_num - 1)
            if not episode_ifchosen[quality][file_id][episode_id]:
                episode_reward = np.array(data_file["rewards"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
            episode_ifchosen[quality][file_id][episode_id] = 1
            cur_size += 1
        episode_aver_reward = np.mean(np.sum(episode_reward, axis=1), axis=0)
        average_reward.append(episode_aver_reward[0])

    return average_reward

def plot_reward_distribution(src_path, map_name):
    average_reward = average_reward_in_chunk(src_path, map_name)
    sns.set()
    ax = sns.displot(average_reward, bins=40, kde=True)
    plt.title("map {} reward distribution".format(map_name))
    plt.savefig("{}_reward.png".format(map_name))
    plt.show()

plot_reward_distribution("/data/bk/d4marl/hdf5_files/", "8m")