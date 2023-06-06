import os

import torch
import h5py
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_reward_distribution(map_name='3m'):
    rewards = []

    cnt = 0
    for file_path in os.listdir(f"/home/lhmeng/Datasetproj/on-policy/offline_datasets/{map_name}/no_quality"):
        cnt += 1
        if cnt % 1000 == 0:
            print("loaded {} files".format(cnt))

        raw_file = torch.load(os.path.join(f"/home/lhmeng/Datasetproj/on-policy/offline_datasets/{map_name}/no_quality", file_path))

        #agents share_rewards
        agent_info = raw_file[0]
        T_rewards = 0

        for step_info in agent_info:
            T_rewards += step_info[3][0]

        rewards.append(T_rewards)

    reward_mean = np.mean(np.array(rewards))
    reward_std = np.std(np.array(rewards))

    print(f"mean of {map_name}: {reward_mean}")
    print(f"std of {map_name}: {reward_std}")

    sns.set()
    ax = sns.displot(rewards, bins=50, kde=True)
    plt.title(map_name)
    plt.savefig(f'/home/lhmeng/Datasetproj/on-policy/maps_reward_distribution/{map_name}.png', bbox_inches='tight')
    #plt.show()

map_list = ['3m', '8m', '2s3z', '2s_vs_1sc', '3s_vs_4z', 'MMM', 'so_many_baneling', '3s_vs_3z', '2m_vs_1z',
            'bane_vs_bane', '1c3s5z', '5m_vs_6m', '10m_vs_11m', '2c_vs_64zg', '8m_vs_9m', '3s_vs_5z']
for map_name in map_list:
    plot_reward_distribution(map_name)

