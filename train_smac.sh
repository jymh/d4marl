#!/bin/bash

model_type="madt"

if [ $model_type = "baseline" ]
then
        data_dir='/data/bk/d4marl/hdf5_files/3m/good'
        offline_log_filename='/home/lhmeng/Datasetproj/d4marl/algorithms/sc2/evaluation/baseline/3m_good_icq.log'
        offline_episodes=200
        offline_test_episodes=20
        algorithm='bc'
        map_name='3m'
        batch_size=16
        CUDA_VISIBLE_DEVICES=1,2 python -u algorithms/sc2/run_baseline_sc2.py \
                --offline_log_filename $offline_log_filename \
                --offline_data_dir $data_dir \
                --offline_episodes $offline_episodes \
                --offline_test_episodes $offline_test_episodes \
                --algorithm $algorithm \
                --map_name $map_name \
                --offline_batch_size $batch_size
elif [ $model_type = 'madt' ]
then
        data_dir='/data/bk/d4marl/hdf5_files/'
        offline_epochs=100
        online_epochs=1000
        offline_batch_size=16
        offline_test_episodes=20
        CUDA_VISIBLE_DEVICES=1,2 python -u algorithms/sc2/run_madt_sc2.py \
                --offline_data_dir $data_dir \
                --offline_map_lists '2c_vs_64zg' \
                --offline_data_quality 'good'\
                --offline_epochs $offline_epochs \
                --offline_episode_num 200 \
                --offline_mini_batch_size $offline_batch_size \
                --offline_test_episodes $offline_test_episodes \
                --online_epochs=$online_epochs
else
        echo "Model type can either be baseline or madt."
fi
