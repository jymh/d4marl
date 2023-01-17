import logging
import argparse

import numpy as np

import torch

from framework.utils_bk import set_seed, load_data, load_data_bc, get_dim_from_space

from framework.buffer import ReplayBuffer, StateActionReturnDataset, SequentialDataset

from datetime import datetime, timedelta
import time
from tensorboardX.writer import SummaryWriter
from framework.utils_bk import config_loader
import gc


parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=123)
parser.add_argument('--context_length', type=int, default=1)
parser.add_argument('--algorithm', type=str, default='cql')
parser.add_argument('--game', type=str, default='StarCraft')
parser.add_argument('--eval_epochs', type=int, default=32)
parser.add_argument('--buffer_size', type=int, default=5000)
parser.add_argument('--model_type', type=str, default='reward_conditioned')
# parser.add_argument('--gamma', type=float, default=0.99)

parser.add_argument('--offline_data_dir', type=str, default='../../offline_data/3m/')
parser.add_argument('--offline_episodes', type=int, default=1000)
parser.add_argument('--offline_test_episodes', type=int, default=0)
parser.add_argument('--offline_episode_bias', type=int, default=0)
parser.add_argument('--offline_batch_size', type=int, default=128)  # episodes used for offline train
parser.add_argument('--offline_epochs', type=int, default=100)
parser.add_argument('--offline_lr', type=float, default=1e-4)
parser.add_argument('--offline_log_dir', type=str, default='./offline_logs/', help='directory of tensorboard logs')
parser.add_argument('--offline_log_filename', type=str, default='baseline.log', help='log file of runtime information')
parser.add_argument('--offline_eval_interval', type=int, default=1)
parser.add_argument('--offline_target_interval', type=int, default=20)

# for mixing net
parser.add_argument('--hyper_hidden_dim', type=int, default=64)
parser.add_argument('--qmix_hidden_dim', type=int, default=64)

parser.add_argument("--env_name", type=str, default='StarCraft2', help="specify the name of environment")
parser.add_argument("--use_obs_instead_of_state", action='store_true',
                    default=False, help="Whether to use global state or concatenated obs")

# StarCraftII environment
parser.add_argument('--map_name', type=str, default='3m', help="Which smac map to run on")
parser.add_argument("--add_move_state", action='store_true', default=False)
parser.add_argument("--add_local_obs", action='store_true', default=False)
parser.add_argument("--add_distance_state", action='store_true', default=False)
parser.add_argument("--add_enemy_action_state", action='store_true', default=False)
parser.add_argument("--add_agent_id", action='store_true', default=True)
parser.add_argument("--add_visible_state", action='store_true', default=False)
parser.add_argument("--add_xy_state", action='store_true', default=False)
parser.add_argument("--use_state_agent", action='store_true', default=True)
parser.add_argument("--use_mustalive", action='store_false', default=True)
parser.add_argument("--add_center_xy", action='store_true', default=True)
parser.add_argument("--stacked_frames", type=int, default=1,
                    help="Dimension of hidden layers for actor/critic networks")
parser.add_argument("--use_stacked_frames", action='store_true',
                    default=False, help="Whether to use stacked_frames")
parser.add_argument("--n_eval_rollout_threads", type=int, default=1,
                    help="Number of parallel envs for evaluating rollouts")

args = parser.parse_args()

from envs.env import Env


if __name__ == '__main__':
    set_seed(args.seed)

    logging.basicConfig(filename=args.offline_log_filename, filemode='a',
                        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
                        datefmt="%m/%d/%Y %H:%M:%S",
                        level=logging.INFO)
    print(1)
    eval_env = Env(args)
    online_train_env = Env(args)
    global_obs_dim = get_dim_from_space(online_train_env.real_env.share_observation_space)
    local_obs_dim = get_dim_from_space(online_train_env.real_env.observation_space)
    action_dim = get_dim_from_space(online_train_env.real_env.action_space)
    num_agents = online_train_env.num_agents
    block_size = args.context_length * 1
    print(2)
    buffer = ReplayBuffer(online_train_env.num_agents, args.buffer_size, args.context_length)
    buffer.reset()

    print("using algorithm: {}".format(args.algorithm))
    cur_time = datetime.now() + timedelta(hours=0)
    args.offline_log_dir += args.algorithm + "_" + args.offline_data_dir.split("/")[-2] + "_" + str(args.seed)
    args.offline_log_dir += cur_time.strftime("[%m-%d]%H.%M.%S")
    writer = SummaryWriter(args.offline_log_dir)
    print(3)
    device = 'cpu'
    if torch.cuda.is_available():
        device = torch.cuda.current_device()
    print(4)
    if args.algorithm == 'icq':
        # from sc2.models.gpt_model import GPT, GPTConfig
        from models.icq_model import ICQ, ICQConfig
        from models.weight_model import QMixNet
        from framework.trainer_icq import Trainer, TrainerConfig
        from framework.rollout_icq import RolloutWorker

        mix_model = QMixNet(global_obs_dim, num_agents, args.hyper_hidden_dim, action_dim)

        mconf = ICQConfig(
                num_actions=action_dim,
                state_dim=local_obs_dim,
                )
        model = ICQ(mix_model, mconf)

        rollout_worker = RolloutWorker(model.pi, buffer, args.context_length)

        offline_tconf = TrainerConfig(max_epochs=1, num_agents=num_agents, batch_size=args.offline_batch_size, learning_rate=1e-4, num_workers=1,
                                      seed=args.seed, game=args.game, log_dir=args.offline_log_dir, actor_lr=5e-4,
                                      lamda=0.8, writer=writer)
        offline_trainer = Trainer(model, offline_tconf)
        gc.collect()

    elif args.algorithm == 'bcq':
        from models.bcq_model import BCQ, BCQConfig
        from models.mix_model import QMixNet
        from framework.trainer_bcq import Trainer, TrainerConfig
        from framework.rollout_bcq import RolloutWorker

        mix_model = QMixNet(global_obs_dim, num_agents, args.hyper_hidden_dim, args.qmix_hidden_dim)

        mconf = BCQConfig(
                num_actions=action_dim,
                state_dim=local_obs_dim,
                )
        model = BCQ(mix_model, mconf)

        rollout_worker = RolloutWorker(model, buffer, args.context_length)
        offline_tconf = TrainerConfig(max_epochs=1, num_agents=num_agents, batch_size=args.offline_batch_size, learning_rate=args.offline_lr, num_workers=1,
                                      seed=args.seed, game=args.game, log_dir=args.offline_log_dir, writer=writer)
        offline_trainer = Trainer(model, offline_tconf)
        gc.collect()

    elif args.algorithm == 'cql':
        from models.cql_model import CQL, CQLConfig
        from models.weight_model import QMixNet
        from framework.trainer_cql import Trainer, TrainerConfig
        from framework.rollout_cql import RolloutWorker

        mix_model = QMixNet(global_obs_dim, num_agents, args.hyper_hidden_dim, action_dim)

        mconf = CQLConfig(
                num_actions=action_dim,
                state_dim=local_obs_dim,
                )
        model = CQL(mix_model, mconf)

        rollout_worker = RolloutWorker(model, buffer, args.context_length)

        offline_tconf = TrainerConfig(max_epochs=1, num_agents=num_agents, batch_size=args.offline_batch_size, learning_rate=args.offline_lr, num_workers=1,
                                      seed=args.seed, game=args.game, log_dir=args.offline_log_dir, writer=writer)
        offline_trainer = Trainer(model, offline_tconf)
        gc.collect()

    elif args.algorithm == 'bc':
        from models.bc_model import BCConfig, BC
        from framework.trainer_bc import Trainer, TrainerConfig
        from framework.rollout_bc import RolloutWorker
        mconf = BCConfig(global_obs_dim + local_obs_dim, action_dim,
                         num_hiddens=(
                         32, 32, 64, 64, 128, 128, 256, 256, 128, 128, 64, 64, 32, 32, 64, 64, 128, 128, 256,
                         256))
        model = BC(mconf)
        rollout_worker = RolloutWorker(model, buffer)
        offline_tconf = TrainerConfig(max_epochs=1, batch_size=args.offline_batch_size, learning_rate=args.offline_lr,
                                      lr_decay=True, warmup_tokens=512 * 20,
                                      num_workers=4, seed=args.seed, model_type=args.model_type, game=args.game,
                                      log_dir=args.offline_log_dir, writer=writer)
        offline_trainer = Trainer(model, offline_tconf)
        gc.collect()

    elif args.algorithm == 'magail':
        from framework.trainer_magail import Trainer
        from framework.rollout_magail import RolloutWorker
        config = config_loader()
        offline_trainer = Trainer(config=config, writer=writer, batch_size=args.offline_batch_size, seed=args.seed, num_agents=num_agents, num_actions=action_dim,
                state_dim=global_obs_dim + local_obs_dim,max_epochs=1, args=args)
        rollout_worker = RolloutWorker(offline_trainer)
        mconf = None
    else:
        model = None
        rollout_worker = None
        offline_trainer = None
        offline_dataset = None
        mconf = None
    print(5)

    #print("offline total episodes: ", buffer.cur_size)
    offline_steps = 0
    for i in range(args.offline_epochs):
        print("offline iter: ", i + 1)

        offline_trainer.train(train_episodes=args.offline_episodes, test_episodes=args.offline_test_episodes,
                              data_dir=args.offline_data_dir, num_agents=num_agents, offline_iter=i)

        if mconf is not None and (i + 1) % mconf.target_interval == 0:
            offline_trainer.update_target()

        if (i + 1) % args.offline_eval_interval == 0:
            aver_return, aver_win_rate = rollout_worker.rollout(eval_env, 20, args.eval_epochs, train=False)
            print("offline return: %s, win_rate: %s" % (aver_return, aver_win_rate))
            writer.add_scalar('aver_return', aver_return, i+1)
            writer.add_scalar('aver_win_rate', aver_win_rate, i + 1)

    online_train_env.real_env.close()
    eval_env.real_env.close()
