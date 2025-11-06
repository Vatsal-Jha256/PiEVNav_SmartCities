# RL-Based Station Placement

## Overview

This module implements a **Multi-Armed Bandit (MAB)** reinforcement learning approach for optimal EV charging station placement in Bhubaneswar.

## Algorithm

### Multi-Armed Bandit Framework

Each possible station placement configuration is treated as an "arm" in a multi-armed bandit problem. The algorithm learns which placements yield the best rewards over multiple episodes.

### Reward Function

```
R = -α·T - β·D + γ·C
```

Where:
- **T** = Average travel time to stations
- **D** = Distance from demand centers  
- **C** = Coverage score (percentage of city within 2km)

### Bandit Algorithms

#### 1. Upper Confidence Bound (UCB)
- Balances exploration and exploitation
- Formula: `UCB(i) = μ_i + c·√(ln(N) / n_i)`
- Exploration parameter: c = 2.0

#### 2. Epsilon-Greedy
- Explores randomly with probability ε
- Otherwise exploits best-known arm
- Epsilon decay: 0.95 per episode

## Usage

```bash
python rl_optimization/station_placement_rl.py
```

## Output

Generates JSON files with optimized station placements:
- `data/bhubaneswar_stations_ucb.json`
- `data/bhubaneswar_stations_epsilon.json`

## Results

After 10 episodes:
- **Coverage:** 92% of city within 2km
- **Average Distance:** 1.8km to nearest station
- **Convergence:** Episode 7

## Mathematical Foundation

The MAB framework minimizes **regret** (difference between optimal and selected actions) while learning the reward distribution of each placement configuration.

