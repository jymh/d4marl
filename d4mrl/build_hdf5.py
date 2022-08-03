import os

import torch
import h5py
import numpy as np

obs = []
share_obs = []
rewards = []
dones = []
actions = []
available_actions = []
episode_ids = []
thread_ids = []

pad_to_length = 0

'''
def numpy_and_pad(attr_list, step_length, pad_to_length, attr_type):
    np_attr = np.array(attr_list)
    if attr_type in ["obs", "share_obs", "rewards", "actions", "ava_actions"]:
        np_attr = np.pad(np_attr, [(0, 0), (0, pad_to_length-step_length), (0, 0)], "constant", constant_values=0)
    elif attr_type in ["episode_ids", "thread_ids"]:
        np_attr = np.pad(np_attr, [(0, 0), (0, pad_to_length-step_length)], "constant", constant_values=0)
    else:
        np_attr = np.pad(np_attr, [(0, 0), (0, pad_to_length-step_length)], "constant", constant_values=True)

    return np_attr
'''

'''
def numpy_and_pad(attr_list, pad_to_length, attr_type):
    if attr_type in ["obs", "share_obs", "rewards", "actions", "ava_actions"]:
        np_attr = np.zeros([len(attr_list), pad_to_length, len(attr_list[0][0])])
        for i in range(len(attr_list)):
            for j in range(len(attr_list[0])):
                for k in range(len(attr_list[0][0])):
                    np_attr[i][j][k] = attr_list[i][j][k]
    elif attr_type in ["episode_ids", "thread_ids"]:
        np_attr = np.zeros([len(attr_list), pad_to_length])
        for i in range(len(attr_list)):
            for j in range(len(attr_list[0])):
                np_attr[i][j] = attr_list[i][j]
    else:
        np_attr = np.ones([len(attr_list), pad_to_length], dtype=np.bool)
        for i in range(len(attr_list)):
            for j in range(len(attr_list[0])):
                np_attr[i][j] = attr_list[i][j]
    return np_attr
'''

cnt = 0

for file_path in os.listdir("/home/lhmeng/Datasetproj/on-policy/offline_datasets/3m"):
    print("{} loaded".format(file_path))
    raw_file = torch.load(os.path.join("/home/lhmeng/Datasetproj/on-policy/offline_datasets/3m", file_path))

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

    share_obs.append(thread_share_obs)
    obs.append(thread_obs)
    actions.append(thread_actions)
    rewards.append(thread_rewards)
    dones.append(thread_dones)
    available_actions.append(thread_available_actions)
    episode_ids.append(thread_episode_ids)
    thread_ids.append(this_thread_ids)



'''
step_lengths = []

for i in range(len(share_obs)):
    if i == 0:
        step_length = len(share_obs[0][0])
        np_share_obs = numpy_and_pad(share_obs[0], pad_to_length, attr_type="share_obs")
        np_obs = numpy_and_pad(obs[0], pad_to_length, attr_type="obs")
        np_actions = numpy_and_pad(actions[0], pad_to_length, attr_type="actions")
        np_rewards = numpy_and_pad(rewards[0], pad_to_length, attr_type="rewards")
        np_dones = numpy_and_pad(dones[0], pad_to_length, attr_type="dones")
        np_ava_actions = numpy_and_pad(available_actions[0], pad_to_length, attr_type="ava_actions")
        np_episode_ids = numpy_and_pad(episode_ids[0], pad_to_length, attr_type="episode_ids")
        np_thread_ids = numpy_and_pad(thread_ids[0], pad_to_length, attr_type="thread_ids")
        step_lengths.append(step_length)
    elif i == 1:
        step_length = len(share_obs[1][0])
        cur_share_obs = numpy_and_pad(share_obs[1], pad_to_length, attr_type="share_obs")
        cur_obs = numpy_and_pad(obs[1], pad_to_length, attr_type="obs")
        cur_actions = numpy_and_pad(actions[1], pad_to_length, attr_type="actions")
        cur_dones = numpy_and_pad(dones[1], pad_to_length, attr_type="dones")
        cur_ava_actions = numpy_and_pad(available_actions[1], pad_to_length, attr_type="ava_actions")
        cur_episode_ids = numpy_and_pad(episode_ids[1], pad_to_length, attr_type="episode_ids")
        cur_thread_ids = numpy_and_pad(thread_ids[1], pad_to_length, attr_type="thread_ids")
        np_share_obs = np.stack((np_share_obs, cur_share_obs))
        np_obs = np.stack((np_obs, cur_obs))
        np_actions = np.stack((np_actions, cur_actions))
        np_dones = np.stack((np_dones, cur_dones))
        np_ava_actions = np.stack((np_ava_actions, cur_ava_actions))
        np_episode_ids = np.stack((np_episode_ids, cur_episode_ids))
        np_thread_ids = np.stack((np_thread_ids, cur_thread_ids))
        step_lengths.append(step_length)
    else:
        step_length = len(share_obs[i][0])
        cur_share_obs = numpy_and_pad(share_obs[i], pad_to_length, attr_type="share_obs")
        cur_obs = numpy_and_pad(obs[i], pad_to_length, attr_type="obs")
        cur_actions = numpy_and_pad(actions[i], pad_to_length, attr_type="actions")
        cur_dones = numpy_and_pad(dones[i], pad_to_length, attr_type="dones")
        cur_ava_actions = numpy_and_pad(available_actions[i], pad_to_length, attr_type="ava_actions")
        cur_episode_ids = numpy_and_pad(episode_ids[i], pad_to_length, attr_type="episode_ids")
        cur_thread_ids = numpy_and_pad(thread_ids[i], pad_to_length, attr_type="thread_ids")
        np_share_obs = np.concatenate((np_share_obs, np.array([cur_share_obs])), axis=0)
        np_obs = np.concatenate((np_obs, np.array([cur_obs])), axis=0)
        np_actions = np.concatenate((np_actions, np.array([cur_actions])), axis=0)
        np_dones = np.concatenate((np_dones, np.array([cur_dones])), axis=0)
        np_ava_actions = np.concatenate((np_ava_actions, np.array([cur_ava_actions])), axis=0)
        np_episode_ids = np.concatenate((np_episode_ids, np.array([cur_episode_ids])), axis=0)
        np_thread_ids = np.concatenate((np_thread_ids, np.array([cur_thread_ids])), axis=0)
        step_lengths.append(step_length)
        print("Step {} inserted".format(i))
'''

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
        print("thread {} inserted".format(i))

        np_share_obs = np.concatenate((np_share_obs, np.array(share_obs[i])), axis=1)       #(agent_num, concate_step_length, obs_dim)
        np_obs = np.concatenate((np_obs, np.array(obs[i])), axis=1)
        np_actions = np.concatenate((np_actions, np.array(actions[i])), axis=1)
        np_rewards = np.concatenate((np_rewards, np.array(rewards[i])), axis=1)
        np_dones = np.concatenate((np_dones, np.array(dones[i])), axis=1)
        np_ava_actions = np.concatenate((np_ava_actions, np.array(available_actions[i])), axis=1)
        np_episode_ids = np.concatenate((np_episode_ids, np.array(episode_ids[i])), axis=1)
        np_thread_ids = np.concatenate((np_thread_ids, np.array(thread_ids[i])), axis=1)



with h5py.File("/home/lhmeng/Datasetproj/on-policy/offline_datasets/hdf5_files/3m_test.hdf5", 'w') as f:
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
