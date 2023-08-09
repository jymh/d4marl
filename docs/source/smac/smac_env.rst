StarCraft Multi-Agent Challenge (SMAC)
================================================

The StarCraft Multi-Agent Challenge (SMAC) is a benchmark problem for deep multi-agent reinforcement learning. Focusing on partially observable, cooperative multi-agent learning, SMAC is based on the real-time strategy game StarCraft II and provides a diverse set of micromanagement scenarios for agents to learn. The challenge emphasizes the lack of standardized benchmarks in cooperative multi-agent RL and introduces SMAC as a solution.

SMAC scenarios are carefully designed to evaluate how individual agents learn to coordinate to solve complex tasks. Each scenario is a confrontation between two armies, with varying initial positions, quantities, and unit types. Sometimes, there are also terrain features like high ground or impassable areas. The goal is to maximize the win rate, the ratio of games won to games played.

The scenarios cover a wide range of combat combinations and tactical challenges, providing a rich testing platform for multi-agent reinforcement learning algorithms. Through these detailed parameters, researchers can precisely control and understand the characteristics of each scenario, better evaluating and optimizing their algorithms.

Below is a detailed description of the scenarios, including the number of agents, enemies, time limits, races, and other specific parameters.

.. list-table:: SMAC Scenarios
   :widths: 15 10 10 10 10 10 10 10
   :header-rows: 1

   * - Scenario
     - Difficulty
     - Agents
     - Enemies
     - Limit
     - Agent Race
     - Enemy Race
     - Unit Type Bits
     - Map Type
   * - 2m_vs_1z
     - Easy
     - 2
     - 1
     - 150
     - T
     - P
     - 0
     - marines
   * - 2s3z
     - Easy
     - 5
     - 5
     - 120
     - P
     - P
     - 2
     - stalkers_and_zealots
   * - 2s_vs_1sc
     - Easy
     - 2
     - 1
     - 300
     - P
     - Z
     - 0
     - stalkers
   * - 3m
     - Easy
     - 3
     - 3
     - 60
     - T
     - T
     - 0
     - marines
   * - 3s_vs_3z
     - Easy
     - 3
     - 3
     - 150
     - P
     - P
     - 0
     - stalkers
   * - 3s_vs_4z
     - Easy
     - 3
     - 4
     - 200
     - P
     - P
     - 0
     - stalkers
   * - 8m
     - Easy
     - 8
     - 8
     - 120
     - T
     - T
     - 0
     - marines
   * - so_many_baneling
     - Easy
     - 7
     - 32
     - 100
     - P
     - Z
     - 0
     - zealots
   * - MMM
     - Hard
     - 10
     - 10
     - 150
     - T
     - T
     - 3
     - MMM
   * - 1c3s5z
     - Easy
     - 9
     - 9
     - 180
     - P
     - P
     - 3
     - colossi_stalkers_zealots
   * - bane_vs_bane
     - Easy
     - 24
     - 24
     - 200
     - Z
     - Z
     - 2
     - bane
   * - 2c_vs_64zg
     - Hard
     - 2
     - 64
     - 400
     - P
     - Z
     - 0
     - colossus
   * - 3s5z
     - Hard
     - 8
     - 8
     - 150
     - P
     - P
     - 2
     - stalkers_and_zealots
   * - 5m_vs_6m
     - Hard
     - 5
     - 6
     - 70
     - T
     - T
     - 0
     - marines
   * - 3s_vs_5z
     - Hard
     - 3
     - 5
     - 250
     - P
     - P
     - 0
     - stalkers
   * - 8m_vs_9m
     - Hard
     - 8
     - 9
     - 120
     - T
     - T
     - 0
     - marines
   * - 25m
     - Hard
     - 25
     - 25
     - 150
     - T
     - T
     - 0
     - marines
   * - 10m_vs_11m
     - Hard
     - 10
     - 11
     - 150
     - T
     - T
     - 0
     - marines
   * - 27m_vs_30m
     - Super Hard
     - 27
     - 30
     - 180
     - T
     - T
     - 0
     - marines
   * - 3s5z_vs_3s6z
     - Super Hard
     - 8
     - 9
     - 170
     - P
     - P
     - 2
     - stalkers_and_zealots
   * - 6h_vs_8z
     - Super Hard
     - 6
     - 8
     - 150
     - Z
     - P
     - 0
     - hydralisks
   * - MMM2
     - Super Hard
     - 10
     - 12
     - 180
     - T
     - T
     - 3
     - MMM
   * - corridor
     - Super Hard
     - 6
     - 24
     - 400
     - P
     - Z
     - 0
     - zealots


Races:
- T: Terran
- P: Protoss
- Z: Zerg

Explanation of Parameters:
- **Agents**: Number of agents in the scenario.
- **Enemies**: Number of enemy units.
- **Limit**: Maximum length of action sequence allowed.
- **Agent Race**: Race of the agents (Terran, Protoss, Zerg).
- **Enemy Race**: Race of the enemies (Terran, Protoss, Zerg).
- **Unit Type Bits**: Specific encoding related to unit types.
- **Map Type**: Specific type of map or scenario.

For the full details of the scenarios and the research, please refer to the `original paper <https://arxiv.org/abs/1902.04043v5>`_.
