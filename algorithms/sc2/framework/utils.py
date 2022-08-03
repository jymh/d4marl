import os
import copy
import h5py
import random
import numpy as np
import torch
from torch.nn import functional as F
from gym.spaces.discrete import Discrete

def list2array(input_list):
    return np.array(input_list)

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def sample(model, critic_model, state, obs, sample=False, actions=None, rtgs=None,
           timesteps=None, available_actions=None):
    """
    take a conditioning sequence of indices in x (of shape (b,t)) and predict the next token in
    the sequence, feeding the predictions back into the model each time. Clearly the sampling
    has quadratic complexity unlike an RNN that is only linear, and has a finite context window
    of block_size, unlike an RNN that has an infinite context window.
    """
    if torch.cuda.is_available():
        block_size = model.module.get_block_size()
    else:
        block_size = model.get_block_size()
    model.eval()
    critic_model.eval()

    # x: (batch_size, context_length, dim)
    # x_cond = x if x.size(1) <= block_size else x[:, -block_size:] # crop context if needed
    obs_cond = obs if obs.size(1) <= block_size//3 else obs[:, -block_size//3:] # crop context if needed
    state_cond = state if state.size(1) <= block_size//3 else state[:, -block_size//3:] # crop context if needed
    if actions is not None:
        actions = actions if actions.size(1) <= block_size//3 else actions[:, -block_size//3:] # crop context if needed
    rtgs = rtgs if rtgs.size(1) <= block_size//3 else rtgs[:, -block_size//3:] # crop context if needed
    timesteps = timesteps if timesteps.size(1) <= block_size//3 else timesteps[:, -block_size//3:] # crop context if needed

    logits = model(obs_cond, pre_actions=actions, rtgs=rtgs, timesteps=timesteps)
    # pluck the logits at the final step and scale by temperature
    logits = logits[:, -1, :]
    # apply softmax to convert to probabilities
    if available_actions is not None:
        logits[available_actions == 0] = -1e10
    probs = F.softmax(logits, dim=-1)

    if sample:
        a = torch.multinomial(probs, num_samples=1)
    else:
        _, a = torch.topk(probs, k=1, dim=-1)

    v = critic_model(state_cond, pre_actions=actions, rtgs=rtgs, timesteps=timesteps).detach()
    v = v[:, -1, :]

    return a, v


def get_dim_from_space(space):
    if isinstance(space[0], Discrete):
        return space[0].n
    elif isinstance(space[0], list):
        return space[0][0]


def get_episode(index, bias, data_dir):

    # episode = toy_example[index]
    begin_index = index + bias
    end_index = index + bias + 1

    with h5py.File(data_dir, 'r') as data_file:

        # TODO: handle online circumstances

        step_cuts = list(data_file["step_cuts"])
        share_obs = np.array(data_file["share_observations"])[:, step_cuts[begin_index]:step_cuts[end_index], :].tolist()
        obs = np.array(data_file["observations"])[:, step_cuts[begin_index]:step_cuts[end_index], :].tolist()
        actions = np.array(data_file["actions"])[:, step_cuts[begin_index]:step_cuts[end_index], :].tolist()
        rewards = np.array(data_file["rewards"])[:, step_cuts[begin_index]:step_cuts[end_index], :].tolist()
        terminals = np.array(data_file["terminals"])[:, step_cuts[begin_index]:step_cuts[end_index]].tolist()
        ava_actions = np.array(data_file["available_actions"])[:, step_cuts[begin_index]:step_cuts[end_index], :].tolist()
        #np_episode_ids = np.array(data_file["episode_ids"])[:, step_cuts[begin_index]:step_cuts[end_index], :].tolist()
        #np_thread_ids = np.array(data_file["thread_ids"])[:, step_cuts[begin_index]:step_cuts[end_index], :].tolist()

    for agent_trajectory in rewards:
        rtgs = 0
        for i in reversed(range(len(agent_trajectory[0]))):
            rtgs += agent_trajectory[i][0]
            agent_trajectory[i][0] = rtgs

    return share_obs, obs, actions, rewards, terminals, ava_actions


def load_data(episode_num, bias, data_dir=None, min_return=0, n_agents=0):
    global_states = [[] for i in range(n_agents)]
    local_obss = [[] for i in range(n_agents)]
    actions = [[] for i in range(n_agents)]
    rewards = [[] for i in range(n_agents)]
    done_idxs = [[] for i in range(n_agents)]
    time_steps = [[] for i in range(n_agents)]
    next_global_states = [[] for i in range(n_agents)]
    next_local_obss = [[] for i in range(n_agents)]
    next_available_actions = [[] for i in range(n_agents)]

    for episode_idx in range(episode_num):
        epi_share_obs, epi_obs, epi_actions, epi_rewards, epi_terminals, epi_ava_actions = get_episode(episode_idx, bias, data_dir)
        assert len(epi_share_obs[0]) == len(epi_obs[0]) == len(epi_actions[0]) == len(epi_rewards[0]) == len(epi_terminals[0]) == len(epi_ava_actions[0]), \
            "step lengths of attributes are not equal"
        length = len(epi_share_obs[0])
        for j in range(n_agents):
            time_step = 0
            agent_share_obs = epi_share_obs[j]
            agent_obs = epi_obs[j]
            agent_actions = epi_actions[j]
            agent_rewards = epi_rewards[j]
            agent_terminals = epi_terminals[j]
            agent_ava_actions = epi_ava_actions[j]
            for i in range(length):
                g, o, a, r, d, ava = agent_share_obs[i], agent_obs[i], agent_actions[i], agent_rewards[i], agent_terminals[i], agent_ava_actions[i]
                if i < length - 1:
                    g_next = agent_share_obs[i + 1]
                    o_next = agent_obs[i + 1]
                    ava_next = agent_ava_actions[i + 1]
                else:
                    g_next = g
                    o_next = o
                    ava_next = ava

                global_states[j].append(g)
                local_obss[j].append(o)
                actions[j].append(a)
                rewards[j].append(r[0])
                time_steps[j].append(time_step)
                time_step += 1
                next_global_states[j].append(g_next)
                next_local_obss[j].append(o_next)
                next_available_actions[j].append(ava_next)
            done_idxs[j].append(len(global_states[j]))


    actions = list2array(actions).swapaxes(1, 0).tolist()
    done_idxs = list2array(done_idxs).swapaxes(1, 0).tolist()
    rewards = list2array(rewards).swapaxes(1, 0).tolist()
    time_steps = list2array(time_steps).swapaxes(1, 0).tolist()
    next_available_actions = list2array(next_available_actions).swapaxes(1, 0).tolist()
    global_states = list2array(global_states).swapaxes(1, 0).tolist()
    local_obss = list2array(local_obss).swapaxes(1, 0).tolist()
    next_global_states = list2array(next_global_states).swapaxes(1, 0).tolist()
    next_local_obss = list2array(next_local_obss).swapaxes(1, 0).tolist()

    # [s, o, a, d, r, t, s_next, o_next, ava_next]
    return global_states, local_obss, actions, done_idxs, rewards, time_steps, next_global_states, next_local_obss, \
           next_available_actions

def load_data_bc(episode_num, bias, data_dir=None, min_return=0):
    global_states = []
    local_obss = []
    actions = []
    rtgs = []
    done_idxs = []
    time_steps = []

    for episode_idx in range(episode_num):
        epi_share_obs, epi_obs, epi_actions, epi_rewards, epi_terminals, epi_ava_actions = get_episode(episode_idx, bias, data_dir)
        assert len(epi_share_obs[0]) == len(epi_obs[0]) == len(epi_actions[0]) == len(epi_rewards[0]) == len(
            epi_terminals[0]) == len(epi_ava_actions[0]), \
            "step lengths of attributes are not equal"
        length = len(epi_share_obs[0])
        n_agents = len(epi_share_obs)
        for j in range(n_agents):
            time_step = 0
            agent_share_obs = epi_share_obs[j]
            agent_obs = epi_obs[j]
            agent_actions = epi_actions[j]
            agent_rewards = epi_rewards[j]
            agent_terminals = epi_terminals[j]
            agent_ava_actions = epi_ava_actions[j]
            for i in range(length):
                g, o, a, r, d, ava = agent_share_obs[i], agent_obs[i], agent_actions[i], agent_rewards[i], \
                                     agent_terminals[i], agent_ava_actions[i]
                global_states.append(g)
                local_obss.append(o)
                actions.append(a)
                rtgs.append(r[0])
                time_steps.append(time_step)
                time_step += 1
            done_idxs.append(len(global_states))

    states = np.concatenate((global_states, local_obss), axis=1)

    return states, actions, done_idxs, rtgs, time_steps

def padding_obs(obs, target_dim):
    len_obs = np.shape(obs)[-1]
    if len_obs > target_dim:
        print("target_dim (%s) too small, obs dim is %s." % (target_dim, len(obs)))
        raise NotImplementedError
    elif len_obs < target_dim:
        padding_size = target_dim - len_obs
        if isinstance(obs, list):
            obs = np.array(copy.deepcopy(obs))
            shape = np.shape(obs)
            padding = np.zeros((shape[0], shape[1], padding_size))
            obs = np.concatenate((obs, padding), axis=-1).tolist()
        elif isinstance(obs, np.ndarray):
            obs = copy.deepcopy(obs)
            shape = np.shape(obs)
            padding = np.zeros((shape[0], shape[1], padding_size))
            obs = np.concatenate((obs, padding), axis=-1)
        else:
            print("unknwon type %s." % type(obs))
            raise NotImplementedError
    return obs


def padding_ava(ava, target_dim):
    len_ava = np.shape(ava)[-1]
    if len_ava > target_dim:
        print("target_dim (%s) too small, ava dim is %s." % (target_dim, len(ava)))
        raise NotImplementedError
    elif len_ava < target_dim:
        padding_size = target_dim - len_ava
        if isinstance(ava, list):
            ava = np.array(copy.deepcopy(ava), dtype=np.long)
            shape = np.shape(ava)
            padding = np.zeros((shape[0], shape[1], padding_size), dtype=np.long)
            ava = np.concatenate((ava, padding), axis=-1).tolist()
        elif isinstance(ava, np.ndarray):
            ava = copy.deepcopy(ava)
            shape = np.shape(ava)
            padding = np.zeros((shape[0], shape[1], padding_size), dtype=np.long)
            ava = np.concatenate((ava, padding), axis=-1)
        else:
            print("unknwon type %s." % type(ava))
            raise NotImplementedError
    return ava