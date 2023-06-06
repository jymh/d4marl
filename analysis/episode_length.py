import os
import sys
import random
import seaborn as sns

import torch
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def episode_lengths_in_chunk(src_path, map_name, quality, episodes=1000):
    step_lengths = []
    cur_size = 0
    while (cur_size < episodes):
        for file in os.listdir(os.path.join(src_path, map_name, quality)):
            with h5py.File(os.path.join(src_path, map_name, quality, file), 'r') as data_file:
                step_cuts = np.array(data_file["step_cuts"])
                for i in range(step_cuts.shape[0] - 1):
                    if quality == "good":
                        str_quality = "expert"
                    else:
                        str_quality = quality
                    step_lengths.append([step_cuts[i + 1] - step_cuts[i], str_quality])
                    cur_size += 1
    return step_lengths

def organize_epl_dataframe(src_path, map_name):
    episode_lengths_good = episode_lengths_in_chunk(src_path, map_name, "good")
    episode_lengths_medium = episode_lengths_in_chunk(src_path, map_name, "medium")
    episode_lengths_poor = episode_lengths_in_chunk(src_path, map_name, "poor")
    episode_lengths_good.extend(episode_lengths_medium)
    episode_lengths_good.extend(episode_lengths_poor)
    episode_lengths = episode_lengths_good

    epl_df = pd.DataFrame(np.array(episode_lengths), columns=['Length', 'quality'])

    epl_df = epl_df.explode('Length')
    epl_df['Length'] = epl_df['Length'].astype('int')

    return epl_df


def plot_episode_length(src_path):

    fig = plt.figure(figsize=(16, 8))

    ax1 = fig.add_subplot(2, 3, 1)
    epl_8m = organize_epl_dataframe(src_path, "8m")
    sns.histplot(x='Length', data=epl_8m, hue='quality', bins=60, ax=ax1)
    ax1.set_title("8m (easy)")

    ax2 = fig.add_subplot(2, 3, 4)
    epl_MMM = organize_epl_dataframe(src_path, "MMM")
    sns.histplot(x='Length', data=epl_MMM, hue='quality', bins=60, legend=False, ax=ax2)
    ax2.set_title("MMM (easy)")

    ax3 = fig.add_subplot(2, 3, 2)
    epl_5mvs6m = organize_epl_dataframe(src_path, "5m_vs_6m")
    sns.histplot(x='Length', data=epl_5mvs6m, hue='quality', bins=60, legend=False, ax=ax3)
    ax3.set_title("5m_vs_6m (hard)")

    ax4 = fig.add_subplot(2, 3, 5)
    epl_3s5z= organize_epl_dataframe(src_path, "3s5z")
    sns.histplot(x='Length', data=epl_3s5z, hue='quality', bins=60, legend=False, ax=ax4)
    ax4.set_title("3s5z (hard)")

    ax5 = fig.add_subplot(2, 3, 3)
    epl_6hvs8z = organize_epl_dataframe(src_path, "6h_vs_8z")
    sns.histplot(x='Length', data=epl_6hvs8z, hue='quality', bins=60, legend=False, ax=ax5)
    ax5.set_title("6h_vs_8z (super hard)")

    ax6 = fig.add_subplot(2, 3, 6)
    epl_corridor = organize_epl_dataframe(src_path, "corridor")
    sns.histplot(x='Length', data=epl_corridor, hue='quality', bins=60, legend=False, ax=ax6)
    ax6.set_title("corridor (super hard)")

    plt.tight_layout()
    plt.savefig("episode_length.pdf")

plot_episode_length("/data/d4marl/hdf5_files/")
