StarCraft Multi-Agent Challenge (SMAC)
================================================

What is SMAC
------------

The StarCraft Multi-Agent Challenge (SMAC) is a benchmark problem for deep multi-agent reinforcement learning. Focusing on partially observable, cooperative multi-agent learning, SMAC is based on the real-time strategy game StarCraft II and provides a diverse set of micromanagement scenarios for agents to learn. The challenge emphasizes the lack of standardized benchmarks in cooperative multi-agent RL and introduces SMAC as a solution.

How is SMAC Designed
--------------------

SMAC scenarios are carefully designed to evaluate how individual agents learn to coordinate to solve complex tasks. Each scenario is a confrontation between two armies, with varying initial positions, quantities, and unit types. Sometimes, there are also terrain features like high ground or impassable areas. The goal is to maximize the win rate, the ratio of games won to games played.

Why We Choose SMAC
------------------

The scenarios cover a wide range of combat combinations and tactical challenges, providing a rich testing platform for multi-agent reinforcement learning algorithms. Through these detailed parameters, researchers can precisely control and understand the characteristics of each scenario, better evaluating and optimizing their algorithms.

Information of SMAC Scenarios
-----------------------------

Below is a detailed description of the scenarios, including the number of agents, enemies, time limits, races, and other specific parameters.

.. card::
    :class-header: sd-bg-info sd-text-white sd-font-weight-bold
    :class-card: sd-outline-info  sd-rounded-1
    :class-footer: sd-font-weight-bold
    :link: appendix-theorem1
    :link-type: ref

    SMAC Maps Information
    ^^^

    .. list-table::
       :widths: 8 7 7 7 7 7 7
       :header-rows: 1

       * - Map Name
         - Difficulty
         - Agents
         - Enemies
         - Limit
         - Agent Race
         - Enemy Race
       * - 2m_vs_1z
         - Easy
         - 2
         - 1
         - 150
         - T
         - P
       * - 2s3z
         - Easy
         - 5
         - 5
         - 120
         - P
         - P
       * - 2s_vs_1sc
         - Easy
         - 2
         - 1
         - 300
         - P
         - Z
       * - 3m
         - Easy
         - 3
         - 3
         - 60
         - T
         - T
       * - 3s_vs_3z
         - Easy
         - 3
         - 3
         - 150
         - P
         - P
       * - 3s_vs_4z
         - Easy
         - 3
         - 4
         - 200
         - P
         - P
       * - 8m
         - Easy
         - 8
         - 8
         - 120
         - T
         - T
       * - so_many_baneling
         - Easy
         - 7
         - 32
         - 100
         - P
         - Z
       * - MMM
         - Hard
         - 10
         - 10
         - 150
         - T
         - T
       * - 1c3s5z
         - Easy
         - 9
         - 9
         - 180
         - P
         - P
       * - bane_vs_bane
         - Easy
         - 24
         - 24
         - 200
         - Z
         - Z
       * - 2c_vs_64zg
         - Hard
         - 2
         - 64
         - 400
         - P
         - Z
       * - 3s5z
         - Hard
         - 8
         - 8
         - 150
         - P
         - P
       * - 5m_vs_6m
         - Hard
         - 5
         - 6
         - 70
         - T
         - T
       * - 3s_vs_5z
         - Hard
         - 3
         - 5
         - 250
         - P
         - P
       * - 8m_vs_9m
         - Hard
         - 8
         - 9
         - 120
         - T
         - T
       * - 25m
         - Hard
         - 25
         - 25
         - 150
         - T
         - T
       * - 10m_vs_11m
         - Hard
         - 10
         - 11
         - 150
         - T
         - T
       * - 27m_vs_30m
         - Super Hard
         - 27
         - 30
         - 180
         - T
         - T
       * - 3s5z_vs_3s6z
         - Super Hard
         - 8
         - 9
         - 170
         - P
         - P
       * - 6h_vs_8z
         - Super Hard
         - 6
         - 8
         - 150
         - Z
         - P
       * - MMM2
         - Super Hard
         - 10
         - 12
         - 180
         - T
         - T
       * - corridor
         - Super Hard
         - 6
         - 24
         - 400
         - P
         - Z

.. hint::
    In the naming of SMAC maps, certain letters represent specific unit types. Here's an explanation of these abbreviations:

    - **m**: Marine (Terran infantry unit)
    - **h**: Hydralisk (Zerg ranged unit)
    - **z**: Zealot (Protoss melee unit)
    - **c**: Colossus (Protoss massive unit)
    - **zg**: Zergling (Zerg basic melee unit)

    Additionally, the map information includes the three main StarCraft races:

    - **T**: Terran (Human race)
    - **Z**: Zerg (Insect-like race)
    - **P**: Protoss (Advanced alien race)

    These units and races appear in various combinations across the maps, defining the characteristics and difficulty of each scenario.

Explanation of Parameters:
- **Agents**: Number of agents in the scenario.
- **Enemies**: Number of enemy units.
- **Limit**: Maximum length of action sequence allowed.
- **Agent Race**: Race of the agents (Terran, Protoss, Zerg).
- **Enemy Race**: Race of the enemies (Terran, Protoss, Zerg).

For the full details of the scenarios and the research, please refer to the `original paper <https://arxiv.org/abs/1902.04043v5>`_.
