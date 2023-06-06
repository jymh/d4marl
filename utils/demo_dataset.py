import os
import sys
import random

import torch
import h5py
import numpy as np

sys.path.append("..")

from algorithms.sc2.envs.starcraft2.smac_maps import get_map_params


def generate_demo_dataset(save_dir, source_dir, map_name):
    print(f"Generating demo dataset of map {map_name}")
    dataset_path = os.path.join(save_dir, map_name)
    source_path = os.path.join(source_dir, map_name)
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    generate_quality_demo(dataset_path, os.path.join(source_path, "good"), "good", 300)
    generate_quality_demo(dataset_path, os.path.join(source_path, "poor"), "poor", 300)
    if map_name != "3m":
        generate_quality_demo(dataset_path, os.path.join(source_path, "medium"), "medium", 300)

def generate_quality_demo(save_dir, srcfile_path, quality, dataset_size):
    cur_size = 0
    save_dir = os.path.join(save_dir, quality)
    file_names = os.listdir(srcfile_path)
    file_num = len(file_names)
    episode_ifchosen = np.zeros((file_num, 100000))

    demo_step_cuts = [0]
    step_pos = 0

    while(cur_size < dataset_size):
        file_id = random.randint(0, file_num-1)
        with h5py.File(os.path.join(srcfile_path, file_names[file_id])) as data_file:
            step_cuts = data_file["step_cuts"]
            episode_num = step_cuts.shape[0] - 1
            episode_id = random.randint(0, episode_num-1)
            if not episode_ifchosen[file_id][episode_id]:
                if cur_size == 0:
                    demo_obs = np.array(data_file["observations"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    demo_share_obs = np.array(data_file["share_observations"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    demo_actions = np.array(data_file["actions"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    demo_rewards = np.array(data_file["rewards"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    demo_dones = np.array(data_file["terminals"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    demo_available_actions = np.array(data_file["available_actions"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    demo_episode_ids = np.array(data_file["episode_ids"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                    demo_thread_ids = np.array(data_file["thread_ids"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]
                else:
                    demo_obs = np.concatenate((demo_obs, np.array(data_file["observations"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                    demo_share_obs = np.concatenate((demo_share_obs, np.array(data_file["share_observations"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                    demo_actions = np.concatenate((demo_actions, np.array(data_file["actions"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                    demo_rewards = np.concatenate((demo_rewards, np.array(data_file["rewards"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                    demo_dones = np.concatenate((demo_dones, np.array(data_file["terminals"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                    demo_available_actions = np.concatenate((demo_available_actions, np.array(data_file["available_actions"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                    demo_episode_ids = np.concatenate((demo_episode_ids, np.array(data_file["episode_ids"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                    demo_thread_ids = np.concatenate((demo_thread_ids, np.array(data_file["thread_ids"])[:, step_cuts[episode_id]:step_cuts[episode_id+1], ...]), axis=1)
                step_length = step_cuts[episode_id + 1] - step_cuts[episode_id]
                step_pos += step_length
                demo_step_cuts.append(step_pos)

                episode_ifchosen[file_id][episode_id] = 1
                cur_size += 1

    with h5py.File(f"{save_dir}/{quality}.hdf5", 'w') as f:
        f.create_dataset("observations", data=demo_obs, chunks=True)
        f.create_dataset("share_observations", data=demo_share_obs, chunks=True)
        f.create_dataset("actions", data=demo_actions, chunks=True)
        f.create_dataset("rewards", data=demo_rewards, chunks=True)
        f.create_dataset("terminals", data=demo_dones, chunks=True)
        f.create_dataset("available_actions", data=demo_available_actions, chunks=True)
        f.create_dataset("episode_ids", data=demo_episode_ids, chunks=True)
        f.create_dataset("thread_ids", data=demo_thread_ids, chunks=True)
        f.create_dataset("step_cuts", data=np.array(demo_step_cuts), chunks=True)


if __name__=="__main__":
    #map_list = ['3m', '8m', '2s3z', '2s_vs_1sc', '3s_vs_4z', 'MMM', 'so_many_baneling', '3s_vs_3z', '2m_vs_1z',
    #            'bane_vs_bane', '1c3s5z', '5m_vs_6m', '10m_vs_11m', '2c_vs_64zg', '8m_vs_9m', '3s_vs_5z']
    map_list = ['6h_vs_8z']
    for map_name in map_list:
        generate_demo_dataset("/data/d4marl/demo_files", "/data/d4marl/hdf5_files", map_name)
