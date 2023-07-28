d4marl

原始文件存储格式 episode_thread [ [ [share_obs[2], obs[], ..., step, episode_id], [], [], .... ], [], []] size(agent_num3, step_size, attributes8, ...)

.hdf5文件存储格式 
actions: [ [ [[. . .]], [], [], .... step_concate], [], []] (agent_num, total_step_size, attribute_dim )
share_obs:
observations:
...


模型需求文件格式
一个episode [ agent_trajectory[ g, o, a, r, d, ava] , [], [], []]

load data读入格式：
baseline 一个episode读入
actions[ [ ], [], [] ]  (n_agents)
done_idxs
rewards
time_steps
next_available_actions
global_states
local_obs
next_global_states
next_local_obs

d4rl

.hdf5文件存储格式 
{actions: [1000000], infos/goal: [], infos/qpos: [], infos/qvel: [], observations: [1000000 x 2], rewards: [], terminals: [], timeouts: []}

