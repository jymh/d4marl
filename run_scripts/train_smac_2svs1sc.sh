#!/bin/bash

model_type="madt"
map_name="2s_vs_1sc"
quality="medium"

if [ $model_type = "baseline" ]
then
        data_dir="/data/d4marl/demo_files/$map_name/$quality"
        algorithm='cql'
        offline_log_filename="/home/xingdp/lhmeng/Datasetproj/d4marl/algorithms/sc2/evaluation/baseline/${map_name}_${quality}_${algorithm}.log"
        offline_log_dir="/home/xingdp/lhmeng/Datasetproj/d4marl/algorithms/sc2/evaluation/baseline/${map_name}_${quality}_${algorithm}"
        offline_episodes=200
        offline_test_episodes=20
        batch_size=16
        CUDA_VISIBLE_DEVICES=2 python -u ../algorithms/sc2/run_baseline_sc2.py \
                --offline_log_filename $offline_log_filename \
                --offline_log_dir $offline_log_dir \
                --offline_data_dir $data_dir \
		--offline_data_quality $quality \
                --offline_episodes $offline_episodes \
                --offline_test_episodes $offline_test_episodes \
                --algorithm $algorithm \
                --map_name $map_name \
                --offline_batch_size $batch_size 
elif [ $model_type = 'madt' ]
then
        data_dir='/data/d4marl/hdf5_files/'
        log_dir="/home/xingdp/lhmeng/Datasetproj/d4marl/algorithms/sc2/evaluation/madt/${map_name}_${quality}_madt"
        offline_epochs=10
        online_epochs=1000
        offline_batch_size=128
        offline_test_episodes=20
        CUDA_VISIBLE_DEVICES=0 python -u ../algorithms/sc2/run_madt_sc2.py \
		--map_name 2s_vs_1sc \
                --offline_data_dir $data_dir \
                --log_dir $log_dir \
                --offline_map_lists $map_name \
                --offline_data_quality $quality\
		--share_obs_dim 45 \
		--obs_dim 37 \
		--action 7 \
                --offline_epochs $offline_epochs \
                --offline_episode_num 1000 \
                --offline_mini_batch_size $offline_batch_size \
		--offline_lr 5e-5\
                --offline_test_episodes $offline_test_episodes \
                --online_epochs $online_epochs \
		--online_ppo_epochs 15 \
		--online_lr 5e-4 \
		--online_pre_train_model_load \
		--online_pre_train_model_id 99
else
        echo "Model type can either be baseline or madt."
fi
