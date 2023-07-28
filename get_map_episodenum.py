import os
import sys

import torch
import h5py
import numpy as np

def get_episode_num(src_path, map_name, quality):
    episodes = 0
    time_steps = 0
    for file_name in os.listdir(os.path.join(src_path, map_name, quality)):
        with h5py.File(os.path.join(src_path, map_name, quality, file_name)) as data_file:
            chunk_episodes = data_file["step_cuts"].shape[0] - 1
            chunk_time_steps = data_file["step_cuts"][-1]
            episodes += chunk_episodes
            time_steps += chunk_time_steps

    print(f"map name: {map_name}, quality: {quality}, episodes:{episodes}")
    return episodes, time_steps

if __name__=="__main__":
    total_episodes = 0
    total_time_steps = 0
    map_list = ['3m', '8m', '2s3z', '2s_vs_1sc', '3s_vs_4z', 'MMM', 'MMM2', 'so_many_baneling', '3s_vs_3z', '2m_vs_1z',
                'bane_vs_bane', '1c3s5z', '5m_vs_6m', '10m_vs_11m', '2c_vs_64zg', '8m_vs_9m', '3s_vs_5z', '25m', '3s5z',
                '3s5z_vs_3s6z', '27m_vs_30m', '6h_vs_8z', 'corridor']
    for map_name in map_list:
        episodes, time_steps = get_episode_num("/data/d4marl/hdf5_files", map_name, "good")
        total_episodes += episodes
        total_time_steps += time_steps
        if map_name != "3m":
            episodes, time_steps = get_episode_num("/data/d4marl/hdf5_files", map_name, "medium")
            total_episodes += episodes
            total_time_steps += time_steps
        episodes, time_steps = get_episode_num("/data/d4marl/hdf5_files", map_name, "poor")
        total_episodes += episodes
        total_time_steps += time_steps
    print(total_time_steps)