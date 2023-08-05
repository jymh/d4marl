# *D4MARL*: A Dataset and Benchmark for Diverse, Measurable Offline Multi-Agent Reinforcement Learning



### Installation Guide

```bash
git clone https://github.com/jymh/d4marl.git
conda create -n d4marl python==3.7
conda activate d4marl
cd d4marl
pip install -r requirements.txt
```



### Data Download Guide

You can download the whole dataset in advance by:

```bash
wget https://
```

Or you can also set the command in terminal **`download_dataset`** as **True**. 

> In the following part, we will show how to pre-train the policy with default or customized configuration based on the downloaded dataset.



### Usage Guide

- Here we provide `Examples` of how to use D4MARL.
- You can train offline MARL policy by running `python run_**`.
- You can run command for an easy-to-download dataset and train policy by setting `download_dataset` as **True**.
- You can customize the configuration of the algorithm by running on the visible paltform `streamlit run visualize.py`.
- You can run an evaluation process by simply clicking the `compare methods` on the platform.
- You can choose the training curve colors of each method by clicking the `color` button.

#### Train Policy

```bash
Example
if [ mode == "baseline" ]
then
    python -u run_baseline_sc2.py \ 
        --offline_data_dir $path_to_data \
        --download_dataset true \   # download demo dataset to start a quick training
        --algorithm $baseline_algorithm \
elif [ mode == "madt" ]
then
    python -u run_madt_sc2.py \
        --offline_data_dir $path_to_data \
        --download_dataset true \
fi
```

> The above command will train a policy with baseline algorithms including ICQ, BCQ, CQL, or MADT, and the total training steps is 1024. The vector environment number is 1. The ``steps_per_epoch`` is default as 500. If there is no local offline dataset in the `offline_data_dir`, the command will download the dataset automatically from our online storage.

You can also customize the configutation of the offline algorithm by running

```bash
streamlit run visualize.py
```

Here we provide a user interface, in this platform, you can choose which specific task and approach need to be trained offline:

> We developed a visible training tool that integrates data preparation, hyperparameter configuration, model training, and evaluation of pre-trained models based on the Streamlit platform [Read the docs](https://www.writethedocs.org/).
