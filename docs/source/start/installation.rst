Installation
============

Installation Guide
------------------

You can install D4MARL from source:

.. code-block:: bash

    $ git clone https://github.com/jymh/d4marl.git
    $ conda create -n d4marl python=3.7
    $ conda activate d4marl
    $ pip install -r requirements.txt

Data download Guide
-------------------

You can download the demonstration dataset in advance by:

.. code-block:: bash

    $ wget https://d4marl.oss-cn-beijing.aliyuncs.com/demo_files/$map_name/$quality/$quality.hdf5

Here, replace replay `$map_name` and `$quality` with the map and quality you want.

Or you can also set the parameter `download_dataset` in the running shell.
