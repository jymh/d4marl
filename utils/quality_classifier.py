import os
import sys

import torch
import h5py
import numpy as np

sys.path.append("..")

from algorithms.sc2.envs.starcraft2.smac_maps import get_map_params

agent_steps_per_chunk = 1000000 # sum of number of agent's approximate steps stored in one h5 file


def classify_quality(map_name):
    if map_name == '3m':
        quality_criterion = {'poor': 10, 'good': 20}
    else:
        quality_criterion = {'poor': 10, 'medium': 18, 'good': 20}

    map_params = get_map_params(map_name)
    episodes_per_chunk = (agent_steps_per_chunk // (map_params['limit'] * map_params['n_agents'])) // 100 * 100

    quality_episodes = {}
    quality_chunk = {}
    obs = {}
    share_obs = {}
    rewards = {}
    dones = {}
    actions = {}
    available_actions = {}
    episode_ids = {}
    thread_ids = {}
    for quality in quality_criterion.keys():
        quality_episodes[quality] = 0
        quality_chunk[quality] = 1
        obs[quality] = []
        share_obs[quality] = []
        rewards[quality] = []
        dones[quality] = []
        actions[quality] = []
        available_actions[quality] = []
        episode_ids[quality] = []
        thread_ids[quality] = []

    file_num = len(os.listdir(f"/data/d4marl/raw_data/{map_name}/no_quality"))
    cnt = 0

    print("map name: {}, {} threads in total".format(map_name, file_num))

    for file_path in os.listdir(f"/data/d4marl/raw_data/{map_name}/no_quality"):
        cnt += 1
        if cnt % 1000 == 0:
            print("{} threads loaded, current file: {}".format(cnt, file_path))

        raw_file = torch.load(os.path.join(f"/data/d4marl/raw_data/{map_name}/no_quality", file_path))

        thread_obs = []     #(thread_num, agent_num, step_length, obs_dim)
        thread_share_obs = []
        thread_rewards = []
        thread_dones = []
        thread_actions = []
        thread_available_actions = []
        thread_episode_ids = []
        this_thread_ids = []

        for agent_info in raw_file:
            agent_obs = []
            agent_share_obs = []
            agent_rewards = []
            agent_dones = []
            agent_actions = []
            agent_available_actions = []
            agent_episode_ids = []
            agent_thread_ids = []

            for step_info in agent_info:
                agent_share_obs.append(step_info[0])
                agent_obs.append(step_info[1])
                agent_actions.append(step_info[2])
                agent_rewards.append(step_info[3])
                agent_dones.append(step_info[4])
                agent_available_actions.append(step_info[5])
                agent_episode_ids.append(step_info[7])
                agent_thread_ids.append(step_info[8])


            #thread_obs: [ agent1[[obs_dim], [], ...], agent2[], agent3[]]
            thread_share_obs.append(agent_share_obs)
            thread_obs.append(agent_obs)
            thread_actions.append(agent_actions)
            thread_rewards.append(agent_rewards)
            thread_dones.append(agent_dones)
            thread_available_actions.append(agent_available_actions)
            thread_episode_ids.append(agent_episode_ids)
            this_thread_ids.append(agent_thread_ids)

        T_rewards = np.sum(agent_rewards)


        if T_rewards <= quality_criterion['poor']:
            share_obs['poor'].append(thread_share_obs)
            obs['poor'].append(thread_obs)
            actions['poor'].append(thread_actions)
            rewards['poor'].append(thread_rewards)
            dones['poor'].append(thread_dones)
            available_actions['poor'].append(thread_available_actions)
            episode_ids['poor'].append(thread_episode_ids)
            thread_ids['poor'].append(this_thread_ids)
            quality_episodes['poor'] += 1
            if quality_episodes['poor'] >= episodes_per_chunk or cnt == file_num:
                save_chunk(share_obs['poor'], obs['poor'], actions['poor'], rewards['poor'], dones['poor'],
                           available_actions['poor'], episode_ids['poor'], thread_ids['poor'], map_name,
                           'poor', quality_chunk['poor'])
                obs['poor'] = []
                share_obs['poor'] = []
                rewards['poor'] = []
                dones['poor'] = []
                actions['poor'] = []
                available_actions['poor'] = []
                episode_ids['poor'] = []
                thread_ids['poor'] = []
                quality_episodes['poor'] = 0
                quality_chunk['poor'] += 1
            else:
                continue
        else:
            if map_name == '3m':
                share_obs['good'].append(thread_share_obs)
                obs['good'].append(thread_obs)
                actions['good'].append(thread_actions)
                rewards['good'].append(thread_rewards)
                dones['good'].append(thread_dones)
                available_actions['good'].append(thread_available_actions)
                episode_ids['good'].append(thread_episode_ids)
                thread_ids['good'].append(this_thread_ids)
                quality_episodes['good'] += 1
                if quality_episodes['good'] >= episodes_per_chunk or cnt == file_num:
                    save_chunk(share_obs['good'], obs['good'], actions['good'], rewards['good'], dones['good'],
                               available_actions['good'], episode_ids['good'], thread_ids['good'], map_name,
                               'good', quality_chunk['good'])
                    obs['good'] = []
                    share_obs['good'] = []
                    rewards['good'] = []
                    dones['good'] = []
                    actions['good'] = []
                    available_actions['good'] = []
                    episode_ids['good'] = []
                    thread_ids['good'] = []
                    quality_episodes['good'] = 0
                    quality_chunk['good'] += 1
            else:
                if T_rewards <= quality_criterion['medium']:
                    share_obs['medium'].append(thread_share_obs)
                    obs['medium'].append(thread_obs)
                    actions['medium'].append(thread_actions)
                    rewards['medium'].append(thread_rewards)
                    dones['medium'].append(thread_dones)
                    available_actions['medium'].append(thread_available_actions)
                    episode_ids['medium'].append(thread_episode_ids)
                    thread_ids['medium'].append(this_thread_ids)
                    quality_episodes['medium'] += 1
                    if quality_episodes['medium'] >= episodes_per_chunk or cnt == file_num:
                        save_chunk(share_obs['medium'], obs['medium'], actions['medium'], rewards['medium'], dones['medium'],
                                   available_actions['medium'], episode_ids['medium'], thread_ids['medium'], map_name,
                                   'medium', quality_chunk['medium'])
                        obs['medium'] = []
                        share_obs['medium'] = []
                        rewards['medium'] = []
                        dones['medium'] = []
                        actions['medium'] = []
                        available_actions['medium'] = []
                        episode_ids['medium'] = []
                        thread_ids['medium'] = []
                        quality_episodes['medium'] = 0
                        quality_chunk['medium'] += 1
                else: # good
                    share_obs['good'].append(thread_share_obs)
                    obs['good'].append(thread_obs)
                    actions['good'].append(thread_actions)
                    rewards['good'].append(thread_rewards)
                    dones['good'].append(thread_dones)
                    available_actions['good'].append(thread_available_actions)
                    episode_ids['good'].append(thread_episode_ids)
                    thread_ids['good'].append(this_thread_ids)
                    quality_episodes['good'] += 1
                    if quality_episodes['good'] >= episodes_per_chunk or cnt == file_num:
                        save_chunk(share_obs['good'], obs['good'], actions['good'], rewards['good'], dones['good'],
                                   available_actions['good'], episode_ids['good'], thread_ids['good'], map_name,
                                   'good', quality_chunk['good'])
                        obs['good'] = []
                        share_obs['good'] = []
                        rewards['good'] = []
                        dones['good'] = []
                        actions['good'] = []
                        available_actions['good'] = []
                        episode_ids['good'] = []
                        thread_ids['good'] = []
                        quality_episodes['good'] = 0
                        quality_chunk['good'] += 1

    for quality in quality_criterion.keys():
        if quality_episodes[quality] != 0:
            save_chunk(share_obs[quality], obs[quality], actions[quality], rewards[quality], dones[quality],
                       available_actions[quality], episode_ids[quality], thread_ids[quality], map_name,
                       quality, quality_chunk[quality])



def save_chunk(share_obs, obs, actions, rewards, dones, available_actions, episode_ids, thread_ids,
               map_name, quality, chunk_num):
    step_cuts = [0]
    step_pos = 0
    for i in range(len(share_obs)):
        if i == 0:
            step_length = len(share_obs[0][0])
            step_pos += step_length
            step_cuts.append(step_pos)

            np_share_obs = np.array(share_obs[0])       #(agent_num, step_length, obs_dim)
            np_obs = np.array(obs[0])
            np_actions = np.array(actions[0])
            np_rewards = np.array(rewards[0])
            np_dones = np.array(dones[0])
            np_ava_actions = np.array(available_actions[0])
            np_episode_ids = np.array(episode_ids[0])
            np_thread_ids = np.array(thread_ids[0])
        else:
            step_length = len(share_obs[i][0])
            step_pos += step_length
            step_cuts.append(step_pos)


            np_share_obs = np.concatenate((np_share_obs, np.array(share_obs[i])), axis=1)       #(agent_num, concate_step_length, obs_dim)
            np_obs = np.concatenate((np_obs, np.array(obs[i])), axis=1)
            np_actions = np.concatenate((np_actions, np.array(actions[i])), axis=1)
            np_rewards = np.concatenate((np_rewards, np.array(rewards[i])), axis=1)
            np_dones = np.concatenate((np_dones, np.array(dones[i])), axis=1)
            np_ava_actions = np.concatenate((np_ava_actions, np.array(available_actions[i])), axis=1)
            np_episode_ids = np.concatenate((np_episode_ids, np.array(episode_ids[i])), axis=1)
            np_thread_ids = np.concatenate((np_thread_ids, np.array(thread_ids[i])), axis=1)

        '''
        if i % 1000 == 0:
            print("thread {} inserted".format(i))
        '''


    with h5py.File(f"/data/d4marl/hdf5_files/{map_name}/{quality}"
                   f"/{map_name}_{quality}_chunk{chunk_num}.hdf5", 'w') as f:
        f.create_dataset("observations", data=np_obs, chunks=True)
        f.create_dataset("share_observations", data=np_share_obs, chunks=True)
        f.create_dataset("actions", data=np_actions, chunks=True)
        f.create_dataset("rewards", data=np_rewards, chunks=True)
        f.create_dataset("terminals", data=np_dones, chunks=True)
        f.create_dataset("available_actions", data=np_ava_actions, chunks=True)
        f.create_dataset("episode_ids", data=np_episode_ids, chunks=True)
        f.create_dataset("thread_ids", data=np_thread_ids, chunks=True)
        #f.create_dataset("step_lengths", data=np.array(step_lengths), chunks=True)
        f.create_dataset("step_cuts", data=np.array(step_cuts), chunks=True)

if __name__=="__main__":
    map_list = ['3s_vs_4z']
    for map_name in map_list:
        classify_quality(map_name)
