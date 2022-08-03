#### How to run experiments
1. setup python environment with 'requirements.txt'
2. to install StarCraft II & SMAC, you could run 'bash install_sc2.sh'. Or you could install them manually to other path you like, following the official link: https://github.com/oxwhirl/smac.
2. enter the 'sc2' folder.
4. set hyper-parameters in 'run_baseline_sc2.py' line 19-64. 
5. run the 'run_baseline_sc2.py' script. You may use '--algorithm' to choose one algorithm from 'cql', 'bcq', 'bc' and 'icq', and use '--map_name' to choose the map to test on.

