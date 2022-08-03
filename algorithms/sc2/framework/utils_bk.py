import random
import numpy as np
import torch
import glob
from torch.nn import functional as F
from gym.spaces.discrete import Discrete
# from sc2.toy_data import toy_example
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
import yaml

def to_device(*params):
    return [x.to(device) for x in params]

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

def list2array(input_list):
    return np.array(input_list)


FLOAT = torch.FloatTensor


# load an episode here, may be from local disk
# from [g, o, a, r, d, ava] to [g, o, a, rtgs, d, ava]
def get_episode(index, bias, data_dir=None, min_return=0):
    # episode = toy_example[index]
    index += bias
    path_files = glob.glob(pathname=data_dir + "*")
    episode = torch.load(path_files[index])

    for agent_trajectory in episode:
        rtgs = 0
        for i in reversed(range(len(agent_trajectory))):
            rtgs += agent_trajectory[i][3][0]
            agent_trajectory[i][3][0] = rtgs

    return episode


# share params, so mix different agent's steps together
def load_data_bc(episode_num, bias, data_dir=None, min_return=0):
    # adding elements with list will be faster
    global_states = []
    local_obss = []
    actions = []
    rtgs = []
    done_idxs = []
    time_steps = []

    for episode_idx in range(episode_num):
        episode = get_episode(episode_idx, bias, data_dir, min_return)
        if not isinstance(data_dir, str) and episode is None:
            continue
        for agent_trajectory in episode:
            time_step = 0
            # rtgs_trajectory = np.zeros(len(agent_trajectory))
            for step in agent_trajectory:
                g, o, a, r, d, ava = step
                global_states.append(g)
                local_obss.append(o)
                actions.append(a[0])
                rtgs.append(r[0])
                # rtgs_trajectory[0:time_step + 1] += r
                time_steps.append(time_step)
                time_step += 1
            # rtgs.extend(list(rtgs_trajectory))
            done_idxs.append(len(global_states))

    # or we can separate it as well
    states = np.concatenate((global_states, local_obss), axis=1)

    return states, actions, done_idxs, rtgs, time_steps

def create_dataset(episode_num, bias, data_dir=None, min_return=0):
    # adding elements with list will be faster
    global_states = []
    local_obss = []
    actions = []
    rtgs = []
    done_idxs = []
    time_steps = []

    # num_episodes = len(toy_example)


    for episode_idx in range(episode_num):
        episode = get_episode(episode_idx, bias, data_dir, min_return)
        for agent_trajectory in episode:
            time_step = 0
            rtgs_trajectory = np.zeros(len(agent_trajectory))
            for step in agent_trajectory:
                g, o, a, r, d, ava = step
                if type(g) is np.ndarray:
                    g = g.tolist()
                if type(o) is np.ndarray:
                    o = o.tolist()
                if type(a) is np.ndarray:
                    a = a.tolist()
                if type(r) is np.ndarray:
                    r = r[0]
                if type(ava) is np.ndarray:
                    ava = ava.tolist()
                global_states.append(g)
                local_obss.append(o)
                actions.append(a)
                rtgs_trajectory[0:time_step + 1] += r
                time_steps.append(time_step)
                time_step += 1
            rtgs.extend(list(rtgs_trajectory))
            done_idxs.append(len(global_states))

    # or we can separate it as well
    states = np.concatenate((global_states, local_obss), axis=1)

    return states, actions, done_idxs, rtgs, time_steps

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
        episode = get_episode(episode_idx, bias, data_dir, min_return)
        if not isinstance(data_dir, str) and episode is None:
            continue
        length = len(episode[0])
        flag = True
        for agent_trajectory in episode:
            if not len(agent_trajectory) == length:
                flag = False
        if flag:
            for j, agent_trajectory in enumerate(episode):
                time_step = 0
                for i in range(len(agent_trajectory)):
                    g, o, a, r, d, ava = agent_trajectory[i]
                    if i < len(agent_trajectory) - 1:
                        g_next = agent_trajectory[i + 1][0]
                        o_next = agent_trajectory[i + 1][1]
                        ava_next = agent_trajectory[i + 1][5]
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
        else:
            print("invalid data\n")

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


def stats(states, actions, done_idxs, rtgs, timesteps):
    print("steps num: ", len(states))
    min_length = 1000
    for i in range(1, len(done_idxs)):
        length = done_idxs[i] - done_idxs[i - 1]
        if length < min_length:
            min_length = length
    print("min length: ", min_length)

    episode_begin_idx = done_idxs.copy()
    episode_begin_idx.insert(0, 0)
    episode_begin_idx = episode_begin_idx[0:-1]
    episode_return = np.array(rtgs)[episode_begin_idx]
    episode_return_mean = np.mean(episode_return)
    episode_return_max = np.max(episode_return)
    episode_return_min = np.min(episode_return)
    # print("episode_return: ", episode_return)
    print("episode_return_max: ", episode_return_max)
    print("episode_return_mean: ", episode_return_mean)
    print("episode_return_min: ", episode_return_min)


def get_dim_from_space(space):
    if isinstance(space[0], Discrete):
        return space[0].n
    elif isinstance(space[0], list):
        return space[0][0]

def config_loader():
    with open("./framework/magail_config.yml") as f:
        config = yaml.full_load(f)
    return config