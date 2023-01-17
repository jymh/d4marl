import csv
from tensorboard.backend.event_processing import event_accumulator
import json
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + './')

plt.rcParams['figure.figsize'] = (9.0, 6.0)

def read_tfevent_baseline(event):
    ea = event_accumulator.EventAccumulator(event)
    ea.Reload()

    test_accuracy = ea.scalars.Items('testing accuracy')
    test_accuracy = [[i.step, i.value] for i in test_accuracy]

    aver_return = ea.scalars.Items('aver_return')
    aver_return = [[i.step, i.value] for i in aver_return]

    return test_accuracy, aver_return

def read_tfevent_madt(event, map_name):
    ea = event_accumulator.EventAccumulator(event)
    ea.Reload()

    offline_test_acc = ea.scalars.Items(f"{map_name}/offline/testing accuracy")
    offline_aver_return = ea.scalars.Items(f"{map_name}/offline/offline_actor_loss")
    online_aver_return = ea.scalars.Items(f"{map_name}/online/aver_return")

    offline_test_acc = [[i.step, i.value] for i in offline_test_acc]
    offline_aver_return = [[i.step, i.value] for i in offline_aver_return]
    online_aver_return = [[i.step, i.value] for i in online_aver_return]

    return offline_test_acc, offline_aver_return, online_aver_return

def draw(data_dict, save_path, i):
    color = ['orange', 'hotpink', 'dodgerblue', 'mediumpurple',  'c',  'cadetblue', 'steelblue',   'mediumslateblue', 'hotpink', 'mediumturquoise']
    plt.tick_params(labelsize=20)





