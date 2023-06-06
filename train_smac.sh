#!/bin/bash

model_type="madt"
map_name="6h_vs_8z"
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
        CUDA_VISIBLE_DEVICES=2 python -u algorithms/sc2/run_baseline_sc2.py \
                --offline_log_filename $offline_log_filename \
                --offline_log_dir $offline_log_dir \
                --offline_data_dir $data_dir \
		--offline_data_quality $quality \
                --offline_episodes $offline_episodes \
                --offline_test_episodes $offline_test_episodes \
                --algorithm $algorithm \
                --map_name $map_name \
                --offline_batch_size $batch_size \
		--use_stacked_frames \
		--stacked_frames 1
elif [ $model_type = 'madt' ]
then
        data_dir='/data/d4marl/demo_files/'
        log_dir="/home/xingdp/lhmeng/Datasetproj/d4marl/algorithms/sc2/evaluation/madt/${map_name}_${quality}_madt"
        offline_epochs=100
        online_epochs=1000
        offline_batch_size=16
        offline_test_episodes=20
        CUDA_VISIBLE_DEVICES=0 python -u algorithms/sc2/run_madt_sc2.py \
                --offline_data_dir $data_dir \
                --log_dir $log_dir \
                --offline_map_lists $map_name \
                --offline_data_quality $quality\
                --offline_epochs $offline_epochs \
                --offline_episode_num 200 \
                --offline_mini_batch_size $offline_batch_size \
                --offline_test_episodes $offline_test_episodes \
                --online_epochs $online_epochs
else
        echo "Model type can either be baseline or madt."
fi
