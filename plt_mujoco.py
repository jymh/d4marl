import csv
from tensorboard.backend.event_processing import event_accumulator
import json
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + './')

plt.rcParams['figure.figsize'] = (9.0, 6.0)

def read_tfevent(event):
    ea = event_accumulator.EventAccumulator(event)
    ea.Reload()
    # print(ea.scalars.Keys())
    episode_rewards = ea.scalars.Items('eval_average_episode_rewards')
    episode_reward = [[i.step/1e6, i.value] for i in episode_rewards]
    return episode_reward
    # return final_reward
    #
def read_tfevent_coma(event):
    ea = event_accumulator.EventAccumulator(event)
    ea.Reload()
    # print(ea.scalars.Keys())
    episode_rewards = ea.scalars.Items('eps_reward_mean')
    episode_reward = [[i.step, i.value] for i in episode_rewards]
    return episode_reward
    # return final_reward

def read_tfevent_vdn(event):
    ea = event_accumulator.EventAccumulator(event)
    ea.Reload()
    # print(ea.scalars.Keys())
    episode_rewards = ea.scalars.Items('episode_rewards_mean')
    episode_reward = [[i.step, i.value] for i in episode_rewards]
    return episode_reward

def read_tfevent_lists(path, all_files):
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            read_tfevent_lists(cur_path, all_files)
        else:
            all_files.append(os.getcwd() + "/" + path + "/" + file)
    return all_files

def return_episode_rewards(path):
    tfevents = read_tfevent_lists(path, [])
    episode_rewards = []
    for event in tfevents:
        if path == 'coma_smoothing':
            episode_reward = read_tfevent_coma(event)
        elif path == 'vdn':
            episode_reward = read_tfevent_vdn(event)
        else:
            episode_reward = read_tfevent(event)  # 10000 * 2
        episode_rewards.append(episode_reward)  # 10 * 10000 * 2
    return episode_rewards

def read_csv_2_dict(csv_str):
    csv_reader = csv.reader(open(csv_str))
    i = 0
    list_all = []
    for row in csv_reader:
        list_pair = []
        if i == 0:
            key_1, key_2 = row[0], row[1]
        else:
            list_pair.append(int(row[0]))
            list_pair.append(float(row[1]))
            list_all.append(list_pair)
        i += 1
    # print(list_all)
    return list_all

def read_csv_2_dict_qmix(csv_str):
    csv_reader = csv.reader(open(csv_str))
    i = 0
    list_all = []
    for row in csv_reader:
        list_pair = []
        if i == 0:
            key_1, key_2 = float(row[0]), row[1]
        else:
            list_pair.append(float(row[0]))
            list_pair.append(float(row[1]))
            list_all.append(list_pair)
        i += 1
    # print(list_all)
    return list_all

def read_csv_2_dict_comix(csv_str):
    csv_reader = csv.reader(open(csv_str))
    i = 0
    list_all = []
    for row in csv_reader:
        list_pair = []
        if i == 0:
            key_1, key_2 = float(row[0])*2, row[1]
        else:
            list_pair.append(float(row[0])*2)
            list_pair.append(float(row[1]))
            list_all.append(list_pair)
        i += 1
    # print(list_all)
    return list_all

def moving_average(interval, windowsize):
    window = np.ones(int(windowsize)) / float(windowsize)
    re = np.convolve(interval, window, 'same')
    return re

def draw(data_dict, save_path, i):
    color = ['orange', 'hotpink', 'dodgerblue', 'mediumpurple',  'c',  'cadetblue', 'steelblue',   'mediumslateblue', 'hotpink', 'mediumturquoise']
    plt.tick_params(labelsize=20)
    # plt.xlabel("Timesteps", fontsize=16)
    # plt.ylabel("Win Rate", fontsize=16)
    # i = np.random.choice(5)
    for k, episode_rewards in data_dict.items():
        timestep = np.array(episode_rewards)[:, :, 0][0]
        reward = np.array(episode_rewards)[:, :, 1]
        for j in range(reward.shape[0]):
            reward[j] = moving_average(reward[j], 7)
        R_mean, R_std = np.mean(reward, axis=0), np.std(reward, axis=0, ddof=1)
        plt.plot(timestep, R_mean, color=color[i], label=k, linewidth=2.5)
        plt.fill_between(timestep, R_mean - R_std, R_mean + R_std, alpha=0.2,
                             color=color[i])
        i = i + 1
    # plt.xlim([0, 2.0])
    # plt.ylim([0,1.0])


def new_draw(data_dict, save_path, i):
    # color = ['darkcyan', 'darkorange', 'mediumpurple', 'tomato', 'cadetblue', 'steelblue', 'violet',  'seagreen',  'yellowgreen', 'mediumslateblue', 'hotpink', 'mediumturquoise']
    color = ['orange', 'hotpink', 'dodgerblue', 'mediumorchid', 'darkseagreen',  'tomato', 'cadetblue', 'steelblue',   'yellowgreen', 'mediumslateblue', 'hotpink', 'mediumturquoise']
    ax = plt.subplot()
    plt.tick_params(labelsize=20)
    ax.grid(linestyle='-.', linewidth=2.5, alpha=0.6)
    # ax.set_xticks([0, 5000, 10000, 15000, 20000, 25000, 30000])
    # ax.set_xticklabels([r"0", r"$5k$", r"$10k$", r"$15k$", r"$20k$", r"$25k$", r"$30k$", r"$40k$", r"$50k$", r"$60k$"])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    # plt.ylim([-10, -3])
    plt.xlabel("Environment Steps (1e6)", fontsize=20)
    plt.ylabel("Average Episode Reward", fontsize=20)
    # i = 0
    for k, episode_rewards in data_dict.items():
        timestep = np.array(episode_rewards)[:, :, 0][0]  # only timestep  # 10000
        reward = np.array(episode_rewards)[:, :, 1]  # only reward # 10*10000
        for j in range(reward.shape[0]):
            reward[j] = moving_average(reward[j], 5)
        R_mean, R_std = np.mean(reward, axis=0), np.std(reward, axis=0, ddof=1)
        plt.plot(timestep, R_mean, color=color[i], label=k, linewidth=2.5)
        plt.fill_between(timestep, R_mean - R_std, R_mean + R_std, alpha=0.2,
                         color=color[i])
        i = i + 1
        plt.xlim([0, 3])
    # plt.legend(loc="lower right", bbox_to_anchor=(0.1, 0.06), borderaxespad=1.8, prop={'size':20}, borderpad=1.5)



if __name__ == "__main__":
    data_dict = {}
    path1 = 'Hopper-v2/logs/'
    hopper_data = return_episode_rewards(path1)
    data_dict['MAPPO w/ OB'] = hopper_data
    print("OB loaded done……")

    json_file_path = './mujoco_swimmer_logs.json'
    json_str = json.dumps(data_dict, ensure_ascii=False, indent=4)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)

    f = open(json_file_path, encoding='utf-8')
    res = f.read()  # 读文件
    data_dict = json.loads(res)  # 把json串变成python的数据类型：字典

    # draw
    save_path = "./"
    new_draw(data_dict, save_path, 0)

    # No ob
    data_dict_vanilla = {}
    path1 = 'Hopper-v2/no_ob_logs/'
    hopper_data = return_episode_rewards(path1)
    data_dict_vanilla['MAPPO w/o OB'] = hopper_data
    print("Vanilla Mappo loaded done……")

    json_file_path = './mujoco_swimmer_no_ob_logs.json'
    json_str = json.dumps(data_dict_vanilla, ensure_ascii=False, indent=4)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)

    f = open(json_file_path, encoding='utf-8')
    res = f.read()  # 读文件
    data_dict_vanilla = json.loads(res)  # 把json串变成python的数据类型：字典

    # draw
    save_path = "./"
    new_draw(data_dict_vanilla, save_path, 1)

    data_dict_comix = {}
    episode_rewards_baseline = []
    for i in range(3):
        index = i + 1
        csv_path = "Hopper-v2/comix/" + str(index) + ".csv"
        list_ = read_csv_2_dict_comix(csv_path)
        episode_rewards_baseline.append(list_)
    data_dict_comix['COMIX'] = episode_rewards_baseline
    draw(data_dict_comix, "./", 2)

    data_dict_fac = {}
    episode_rewards_fac = []
    for i in range(3):
        index = i + 1
        csv_path = "Hopper-v2/maddpg/" + str(index) + ".csv"
        list_ = read_csv_2_dict_qmix(csv_path)
        episode_rewards_fac.append(list_)
    data_dict_fac['MADDPG'] = episode_rewards_fac
    draw(data_dict_fac, "./", 4)

    plt.title("3-Agent Hopper [3x1]", fontsize=20)
    plt.legend(loc="lower right", bbox_to_anchor=(1.06, -0.1), borderaxespad=1.8, prop={'size':20}, borderpad=1.5)
    plt.savefig(save_path + '/hopper_comparison2_rebuttal.pdf', format='pdf')
    plt.rcParams['figure.figsize'] = (12.0, 8.0)
    plt.show()


    # data_dict = {}
    # data_dict_baseline = {}
    # data_dict_qmix = {}
    # episode_rewards = []
    # episode_rewards_baseline = []
    # episode_winrate = []
    # for i in range(3):
    #     index = i + 1
    #     csv_path = "new_logs/3s_vs_5z/ob_mappo/win_rate/" + str(index) + ".csv"
    #     list_ = read_csv_2_dict(csv_path)
    #     episode_rewards.append(list_)
    # data_dict['MAPPO w/ OB'] = episode_rewards
    # draw(data_dict, "./", 0)
    # for i in range(5):
    #     index = i + 1
    #     csv_path = "new_logs/3s_vs_5z/vanilla_mappo/win_rate/" + str(index) + ".csv"
    #     list_ = read_csv_2_dict(csv_path)
    #     episode_rewards_baseline.append(list_)
    # data_dict_baseline['MAPPO w/o OB'] = episode_rewards_baseline
    # draw(data_dict_baseline, "./", 1)
    #
    # for i in range(1):
    #     index = i + 1
    #     csv_path = "new_logs/3s_vs_5z/qmix/win_rate/" + str(index) + ".csv"
    #     list_ = read_csv_2_dict_qmix(csv_path)
    #     for j in range(len(list_)):
    #         list_[j][0] *= 1e7
    #     # list_[i][0]  = 10000000 * list_[i][0]
    #     episode_winrate.append(list_)
    # data_dict_qmix['QMIX'] = episode_winrate
    # draw(data_dict_qmix, "./", 2)
    #
    # plt.grid()
    # plt.title("3s vs. 5z", fontsize=16)
    # plt.savefig("./new_logs/" + 'win_rate_3s_vs_5z.pdf', format='pdf')
    # plt.show()