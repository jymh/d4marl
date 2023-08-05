Usage Guide
===========

Quick Facts
-----------

.. card::
    :class-card: sd-outline-info  sd-rounded-1
    :class-body: sd-font-weight-bold

    #. Here we provide :bdg-info-line:`Examples` of how to use D4MARL .
    #. You can train offline MARL policy by runnning :bdg-info-line:`python run_**` .
    #. You can customize the configuration of the algorithm by running on the visible platform :bdg-info-line:`streamlit run visualize.py` .
    #. You can run a run to download and train policy by setting :bdg-info-line:`download_dataset` as True .
    #. You can run an evaluation by simply clicking the :bdg-info-line:`compare methods` .
    #. You can choose the training curve color of each method by clicking the :bdg-info-line:`color` .
  

Train Policy
------------

.. card::
    :class-header: sd-bg-success sd-text-white
    :class-card: sd-outline-success  sd-rounded-1

    Example
    ^^^

    You can train an offline MARL policy by running:

    .. code-block:: bash

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


.. hint::
    The above command will train a policy with baseline algorithms including ICQ, BCQ, CQL, or MADT, and the total training steps is 1024. The vector environment number is 1. The ``algo_cfgs:steps_per_epoch`` is default as 500. If there is no local offline dataset in the :bdg-info-line:`offline_data_dir`, the command will download the dataset automatically from our online storage.

Customize Configuration
-----------------------

.. card::
    :class-header: sd-bg-success sd-text-white
    :class-card: sd-outline-success  sd-rounded-1

    Example
    ^^^

    You can also customize the configuration of the algorithm by running:

    .. code-block:: bash

        streamlit run visualize.py

    Here we provide a user interface, in this platform, you can choose which specific task and approach need to be trained offline:

    
.. hint::
    We developed a visible training tool that integrates data preparation, hyperparameter configuration, model training, and evaluation of pre-trained models based on the Streamlit platform `Link to Write the Docs <https://www.writethedocs.org/>`_.


==========
Usage Guide
===========

Quick Facts
-----------

.. card::
    :class-card: sd-outline-info  sd-rounded-1
    :class-body: sd-font-weight-bold

    #. Here we provide :bdg-info-line:`Examples` of how to use D4MARL .
    #. You can train offline MARL policy by runnning :bdg-info-line:`python run_**` .
    #. You can customize the configuration of the algorithm by running on the visible platform :bdg-info-line:`streamlit run visualize.py` .
    #. You can run a run to download and train policy by setting :bdg-info-line:`download_dataset` as True .
    #. You can run an evaluation by simply clicking the :bdg-info-line:`compare methods` .
    #. You can choose the training curve color of each method by clicking the :bdg-info-line:`color` .
  

Train Policy
------------

.. card::
    :class-header: sd-bg-success sd-text-white
    :class-card: sd-outline-success  sd-rounded-1

    Example
    ^^^

    You can train an offline MARL policy by running:

    .. code-block:: bash

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


.. hint::
    The above command will train a policy with baseline algorithms including ICQ, BCQ, CQL, or MADT, and the total training steps is 1024. The vector environment number is 1. The ``algo_cfgs:steps_per_epoch`` is default as 500. If there is no local offline dataset in the :bdg-info-line:`offline_data_dir`, the command will download the dataset automatically from our online storage.

Customize Configuration
-----------------------

.. card::
    :class-header: sd-bg-success sd-text-white
    :class-card: sd-outline-success  sd-rounded-1

    Example
    ^^^

    You can also customize the configuration of the algorithm by running:

    .. code-block:: bash

        streamlit run visualize.py

    Here we provide a user interface, in this platform, you can choose which specific task and approach need to be trained offline:

    
.. hint::
    We developed a visible training tool that integrates data preparation, hyperparameter configuration, model training, and evaluation of pre-trained models based on the Streamlit platform `Link to Write the Docs <https://www.writethedocs.org/>`_.


