import requests
import argparse
import torch
import os

from tensorboardX.writer import SummaryWriter
from framework.utils import set_seed
from framework.trainer_madt import Trainer, TrainerConfig
from envs.madt_env import Env
from framework.buffer import MadtReplayBuffer
from framework.rollout_madt import RolloutWorker
from datetime import datetime, timedelta
from models.gpt_model import GPT, GPTConfig
from envs.config import get_config
# from models.mlp_model import GPT, GPTConfig

# args = sys.argv[1:]
parser = get_config()
#parser.add_argument('--seed', type=int, default=123)
parser.add_argument('--context_length', type=int, default=1)
parser.add_argument('--model_type', type=str, default='state_only')
#parser.add_argument('--eval_episodes', type=int, default=32)
parser.add_argument('--max_timestep', type=int, default=400)
parser.add_argument('--log_dir', type=str, default='./madt_logs/')
parser.add_argument('--save_log', type=bool, default=True)
parser.add_argument('--exp_name', type=str, default='easy_trans')
parser.add_argument('--pre_train_model_path', type=str, default='../../offline_model/')

parser.add_argument('--share_obs_dim', type=int, default=500, help="dimension of share observation of each map")
parser.add_argument('--obs_dim', type=int, default=300, help="dimension of observation of each map")
parser.add_argument('--action_dim', type=int, default=30, help="dimension of action observation of each map")
parser.add_argument('--offline_map_lists', type=str, nargs="+", help="list of map names")
parser.add_argument('--offline_episode_num', type=int, nargs="+", help="list of episode numbers drawn from each map dataset")
parser.add_argument('--offline_test_episodes', type=int, default=0, help="list of episode numbers used for testing while offline training")
parser.add_argument('--offline_data_quality', type=str, nargs="+", default=['good'], help="quality of data")
parser.add_argument('--offline_data_dir', type=str, default='../../offline_data/')
parser.add_argument('--download_dataset', action="store_true", help="add parameter if you want to download demo datasets")

parser.add_argument('--offline_epochs', type=int, default=10)
parser.add_argument('--offline_mini_batch_size', type=int, default=128)
parser.add_argument('--offline_lr', type=float, default=5e-4)
parser.add_argument('--offline_eval_interval', type=int, default=1)
parser.add_argument('--offline_train_critic', type=bool, default=True)
parser.add_argument('--offline_model_save', type=bool, default=True)

parser.add_argument('--online_buffer_size', type=int, default=64)
parser.add_argument('--online_epochs', type=int, default=5000)
parser.add_argument('--online_ppo_epochs', type=int, default=10)
parser.add_argument('--online_lr', type=float, default=5e-4)
parser.add_argument('--online_eval_interval', type=int, default=1)
parser.add_argument('--online_train_critic', type=bool, default=True)
parser.add_argument('--online_pre_train_model_load', action="store_true", help="add parameter if you want to load pretrained model")
parser.add_argument('--online_pre_train_model_id', type=int, default=9)


# args = parser.parse_args(args, parser)
args = parser.parse_args()
set_seed(args.seed)
torch.set_num_threads(8)

global_obs_dim = args.share_obs_dim
local_obs_dim = args.obs_dim
action_dim = args.action_dim

cur_time = datetime.now() + timedelta(hours=0)
args.log_dir += cur_time.strftime("[%m-%d]%H.%M.%S")
writter = SummaryWriter(args.log_dir) if args.save_log else None

eval_env = Env(args.eval_episodes)
online_train_env = Env(args.online_buffer_size)

# global_obs_dim = get_dim_from_space(online_train_env.real_env.share_observation_space)
# local_obs_dim = get_dim_from_space(online_train_env.real_env.observation_space)
# action_dim = get_dim_from_space(online_train_env.real_env.action_space)


block_size = args.context_length * 3

print("global_obs_dim: ", global_obs_dim)
print("local_obs_dim: ", local_obs_dim)
print("action_dim: ", action_dim)

mconf_actor = GPTConfig(local_obs_dim, action_dim, block_size,
                        n_layer=2, n_head=2, n_embd=32, model_type=args.model_type, max_timestep=args.max_timestep)
model = GPT(mconf_actor, model_type='actor')

mconf_critic = GPTConfig(global_obs_dim, action_dim, block_size,
                         n_layer=2, n_head=2, n_embd=32, model_type=args.model_type, max_timestep=args.max_timestep)
critic_model = GPT(mconf_critic, model_type='critic')
device = 'cpu'
if torch.cuda.is_available():
    device = torch.cuda.current_device()
    model = torch.nn.DataParallel(model).to(device)
    critic_model = torch.nn.DataParallel(critic_model).to(device)

buffer = MadtReplayBuffer(block_size, global_obs_dim, local_obs_dim, action_dim)
rollout_worker = RolloutWorker(model, critic_model, buffer, global_obs_dim, local_obs_dim, action_dim)


if args.download_dataset:
    for map_name in args.offline_map_lists:
        download_dir = os.path.join(args.offline_data_dir, map_name)
        for quality in args.offline_data_quality:
            url = f"https://d4marl.oss-cn-beijing.aliyuncs.com/demo_files/{map_name}/{quality}/{quality}.hdf5"
            if not os.path.exists(os.path.join(download_dir, quality)):
                os.makedirs(os.path.join(download_dir, quality))
            file_name = url.split('/')[-1]
            print(f"downloading dataset from {url}")
            with open(os.path.join(download_dir, quality, file_name), 'wb') as f:
                f.write(requests.get(url).content)
                print(f"download from {url} to {os.path.join(download_dir, quality, file_name)}")

used_data_dir = {}
'''
for map_name in args.offline_map_lists:
    source_dir = args.offline_data_dir + map_name
    for quality in args.offline_data_quality:
        used_data_dir.append(f"{source_dir}/{quality}.hdf5")
'''
map_names = ""
qualities = ""
for map_name in args.offline_map_lists:
    used_data_dir[map_name] = []
    source_dir = os.path.join(args.offline_data_dir, map_name)
    map_names += map_name
    if map_name != args.offline_map_lists[-1]:
        map_names += '_'
    for quality in args.offline_data_quality:
        qualities += quality
        for file_path in os.listdir(os.path.join(source_dir, quality)):
            used_data_dir[map_name].append(os.path.join(source_dir, quality, file_path))

buffer.load_offline_data(used_data_dir, args.offline_episode_num, args.offline_test_episodes,
                         max_epi_length=eval_env.max_timestep)
offline_dataset = buffer.sample()
max_epi_len, min_epi_len, max_rtgs, aver_epi_rtgs = offline_dataset.stats()

offline_tconf = TrainerConfig(max_epochs=1, batch_size=args.offline_mini_batch_size, learning_rate=args.offline_lr,
                              num_workers=0, mode="offline", aver_epi_len=(max_epi_len+min_epi_len)/2)
offline_trainer = Trainer(model, critic_model, offline_tconf)

# target_rtgs = offline_dataset.max_rtgs
target_rtgs = 20.
print("offline target_rtgs: ", target_rtgs)
for i in range(args.offline_epochs):
    offline_actor_loss, offline_critic_loss, _, __, ___ = offline_trainer.train(offline_dataset, i,
                                                                                args.offline_test_episodes,
                                                                                args.offline_train_critic)
    if args.save_log:
        train_acc = offline_trainer.train_n_correct / (offline_trainer.train_n_total + 1)
        test_acc = offline_trainer.test_n_correct / (offline_trainer.test_n_total + 1)
        writter.add_scalar(f"{map_names}/offline/training accuracy", train_acc, i)
        writter.add_scalar(f"{map_names}/offline/testing accuracy", test_acc, i)
        writter.add_scalar(f'{map_names}/offline/offline_actor_loss', offline_actor_loss, i)
        writter.add_scalar(f'{map_names}/offline/offline_critic_loss', offline_critic_loss, i)
    if i % args.offline_eval_interval == 0:
        aver_return, aver_win_rate, _ = rollout_worker.rollout(eval_env, target_rtgs, train=False)
        print("offline epoch: %s, return: %s, eval_win_rate: %s" % (i + 1, aver_return, aver_win_rate))
        if args.save_log:
            writter.add_scalar(f'{map_names}/aver_return', aver_return.item(), i)
            writter.add_scalar(f'{map_names}/aver_win_rate', aver_win_rate, i)
    if args.offline_model_save:
        actor_path = args.pre_train_model_path + args.exp_name + '/' + map_names + '_' + qualities + '/actor'
        if not os.path.exists(actor_path):
            os.makedirs(actor_path)
        critic_path = args.pre_train_model_path + args.exp_name + '/' + map_names + '_' + qualities + '/critic'
        if not os.path.exists(critic_path):
            os.makedirs(critic_path)
        torch.save(model.state_dict(), actor_path + os.sep + str(i) + '.pkl')
        torch.save(critic_model.state_dict(), critic_path + os.sep + str(i) + '.pkl')
del offline_dataset

if args.online_epochs > 0 and args.online_pre_train_model_load:
    actor_path = args.pre_train_model_path + args.exp_name + '/' + map_names + '_' + qualities + '/actor/' + str(args.online_pre_train_model_id) + '.pkl'
    critic_path = args.pre_train_model_path + args.exp_name + '/' + map_names + '_' + qualities + '/critic/' + str(args.online_pre_train_model_id) + '.pkl'
    model.load_state_dict(torch.load(actor_path))
    critic_model.load_state_dict(torch.load(critic_path))

online_tconf = TrainerConfig(max_epochs=args.online_ppo_epochs, batch_size=0,
                             learning_rate=args.online_lr, num_workers=0, mode="online")
online_trainer = Trainer(model, critic_model, online_tconf)
buffer.reset(num_keep=0, buffer_size=args.online_buffer_size)

total_steps = 0
time_to_threshold = 0
epochs_above_threshold = 0
step_when_reach = 0
for i in range(args.online_epochs):
    sample_return, _, steps = rollout_worker.rollout(online_train_env, target_rtgs, train=True)
    total_steps += steps
    online_dataset = buffer.sample()
    online_actor_loss, online_critic_loss, entropy, ratio, confidence = online_trainer.train(online_dataset, i,
                                                                                             train_critic=args.online_train_critic)
    del online_dataset
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    if args.save_log:
        writter.add_scalar(f'{map_names}/online/online_actor_loss', online_actor_loss, total_steps)
        writter.add_scalar(f'{map_names}/online/online_critic_loss', online_critic_loss, total_steps)
        writter.add_scalar(f'{map_names}/online/entropy', entropy, total_steps)
        writter.add_scalar(f'{map_names}/online/ratio', ratio, total_steps)
        writter.add_scalar(f'{map_names}/online/confidence', confidence, total_steps)
        writter.add_scalar(f'{map_names}/online/sample_return', sample_return, total_steps)

    # if online_dataset.max_rtgs > target_rtgs:
    #     target_rtgs = online_dataset.max_rtgs
    print("sample return: %s, online target_rtgs: %s" % (sample_return, target_rtgs))
    if i % args.online_eval_interval == 0:
        aver_return, aver_win_rate, _ = rollout_worker.rollout(eval_env, target_rtgs, train=False)
        print("online steps: %s, return: %s, eval_win_rate: %s" % (total_steps, aver_return, aver_win_rate))

        if aver_return >= 18 and time_to_threshold == 0: # average return reach threshold just right
            if epochs_above_threshold == 0: # record time steps of first reach
                step_when_reach = total_steps
            epochs_above_threshold += 1
            if epochs_above_threshold >= 10: # average return reach threshold for at least 10 epochs
                time_to_threshold = step_when_reach
                print("time to threshold: {}".format(time_to_threshold))
        else: # maybe reach threshold occasionally
            epochs_above_threshold = 0
            step_when_reach = 0

        if args.save_log:
            writter.add_scalar(f'{map_names}/online/aver_return', aver_return.item(), total_steps)
            writter.add_scalar(f'{map_names}/online/aver_win_rate', aver_win_rate, total_steps)
            writter.add_scalar(f'{map_names}/online/time_to_threshold', time_to_threshold, i)


online_train_env.real_env.close()
eval_env.real_env.close()
