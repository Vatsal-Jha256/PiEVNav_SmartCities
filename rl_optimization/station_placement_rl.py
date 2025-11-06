#!/usr/bin/env python3
"""
RL-Based Station Placement Algorithm
Multi-Armed Bandit (MAB) approach for optimal EV charging station placement in Bhubaneswar

This module implements a simplified but functional RL algorithm for placing 25 charging stations
across Bhubaneswar using a multi-armed bandit framework.
"""

import numpy as np
import random
import json
import os
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import logging
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UCB_Bandit:
    """
    Upper Confidence Bound (UCB) bandit algorithm for station placement.
    
    UCB balances exploration and exploitation by selecting arms with high
    estimated rewards and high uncertainty.
    """
    
    def __init__(self, exploration_param: float = 2.0):
        """
        Initialize UCB bandit.
        
        Args:
            exploration_param: Exploration parameter (c in UCB formula)
        """
        self.c = exploration_param
        self.counts = defaultdict(int)  # Number of times each arm was pulled
        self.rewards = defaultdict(list)  # Reward history for each arm
        self.total_pulls = 0
    
    def select_arm(self, arms: List[Dict]) -> Dict:
        """
        Select arm using UCB algorithm.
        
        Args:
            arms: List of candidate placement configurations (arms)
            
        Returns:
            Selected arm (placement configuration)
        """
        if not arms:
            return None
        
        # If any arm hasn't been tried, select it
        untried_arms = [arm for arm in arms if self.counts[arm['id']] == 0]
        if untried_arms:
            return random.choice(untried_arms)
        
        # Calculate UCB value for each arm
        ucb_values = {}
        for arm in arms:
            arm_id = arm['id']
            avg_reward = np.mean(self.rewards[arm_id]) if self.rewards[arm_id] else 0
            confidence = self.c * math.sqrt(
                math.log(self.total_pulls) / self.counts[arm_id]
            )
            ucb_values[arm_id] = avg_reward + confidence
        
        # Select arm with highest UCB value
        best_arm_id = max(ucb_values, key=ucb_values.get)
        return next(arm for arm in arms if arm['id'] == best_arm_id)
    
    def update(self, arm: Dict, reward: float):
        """
        Update bandit with observed reward.
        
        Args:
            arm: The arm that was pulled
            reward: Observed reward
        """
        arm_id = arm['id']
        self.counts[arm_id] += 1
        self.rewards[arm_id].append(reward)
        self.total_pulls += 1
    
    def get_best_arm(self, arms: List[Dict]) -> Optional[Dict]:
        """Get the arm with highest average reward."""
        if not arms:
            return None
        
        best_arm = None
        best_avg = -float('inf')
        
        for arm in arms:
            arm_id = arm['id']
            if self.rewards[arm_id]:
                avg_reward = np.mean(self.rewards[arm_id])
                if avg_reward > best_avg:
                    best_avg = avg_reward
                    best_arm = arm
        
        return best_arm if best_arm else arms[0]


class EpsilonGreedy_Bandit:
    """
    Epsilon-Greedy bandit algorithm.
    
    Explores randomly with probability epsilon, otherwise exploits
    the arm with highest average reward.
    """
    
    def __init__(self, epsilon: float = 0.3, epsilon_decay: float = 0.95):
        """
        Initialize Epsilon-Greedy bandit.
        
        Args:
            epsilon: Exploration probability
            epsilon_decay: Decay factor for epsilon over episodes
        """
        self.epsilon = epsilon
        self.initial_epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.rewards = defaultdict(list)
        self.counts = defaultdict(int)
    
    def select_arm(self, arms: List[Dict]) -> Dict:
        """Select arm using epsilon-greedy strategy."""
        if not arms:
            return None
        
        # Explore: select random arm
        if random.random() < self.epsilon:
            return random.choice(arms)
        
        # Exploit: select arm with highest average reward
        best_arm = None
        best_avg = -float('inf')
        
        for arm in arms:
            arm_id = arm['id']
            if self.rewards[arm_id]:
                avg_reward = np.mean(self.rewards[arm_id])
                if avg_reward > best_avg:
                    best_avg = avg_reward
                    best_arm = arm
        
        return best_arm if best_arm else random.choice(arms)
    
    def update(self, arm: Dict, reward: float):
        """Update bandit with observed reward."""
        arm_id = arm['id']
        self.counts[arm_id] += 1
        self.rewards[arm_id].append(reward)
    
    def decay_epsilon(self):
        """Decay epsilon for next episode."""
        self.epsilon = max(0.1, self.epsilon * self.epsilon_decay)


class StationPlacementRL:
    """
    RL-based system for placing EV charging stations in Bhubaneswar.
    
    Uses multi-armed bandit algorithms to optimize station placement
    over multiple episodes, learning from reward feedback.
    """
    
    def __init__(self, num_stations: int = 25, num_episodes: int = 10):
        """
        Initialize RL placement system.
        
        Args:
            num_stations: Number of stations to place
            num_episodes: Number of learning episodes
        """
        self.num_stations = num_stations
        self.num_episodes = num_episodes
        
        # Bhubaneswar bounds
        self.city_bounds = {
            'min_lat': 20.20,
            'max_lat': 20.40,
            'min_lon': 85.70,
            'max_lon': 85.95
        }
        
        # Initialize bandit algorithms
        self.ucb_bandit = UCB_Bandit(exploration_param=2.0)
        self.epsilon_bandit = EpsilonGreedy_Bandit(epsilon=0.3)
        
        # Key locations in Bhubaneswar (demand centers)
        self.demand_centers = [
            {'lat': 20.2961, 'lon': 85.8245, 'weight': 1.0, 'name': 'City Center'},
            {'lat': 20.2644, 'lon': 85.8281, 'weight': 0.9, 'name': 'KIIT Area'},
            {'lat': 20.3100, 'lon': 85.8500, 'weight': 0.8, 'name': 'Patia IT Hub'},
            {'lat': 20.2500, 'lon': 85.8500, 'weight': 0.7, 'name': 'Railway Station'},
            {'lat': 20.3000, 'lon': 85.8800, 'weight': 0.6, 'name': 'Airport Area'},
        ]
        
        # Results storage
        self.episode_rewards = []
        self.best_placements = []
    
    def generate_candidate_placements(self) -> List[Dict]:
        """
        Generate candidate station placement configurations.
        
        Each configuration is an "arm" in the bandit problem.
        
        Returns:
            List of candidate placement configurations
        """
        candidates = []
        
        # Strategy 1: Place at demand centers (high priority locations)
        for i, center in enumerate(self.demand_centers[:self.num_stations]):
            candidates.append({
                'id': f'strategic_{i}',
                'lat': center['lat'],
                'lon': center['lon'],
                'type': 'strategic',
                'name': center['name']
            })
        
        # Strategy 2: Grid-based placement (uniform distribution)
        grid_size = int(np.ceil(np.sqrt(self.num_stations)))
        lat_range = self.city_bounds['max_lat'] - self.city_bounds['min_lat']
        lon_range = self.city_bounds['max_lon'] - self.city_bounds['min_lon']
        
        for i in range(self.num_stations):
            row = i // grid_size
            col = i % grid_size
            
            lat = self.city_bounds['min_lat'] + (row / grid_size) * lat_range
            lon = self.city_bounds['min_lon'] + (col / grid_size) * lon_range
            
            # Add some randomness
            lat += random.uniform(-0.01, 0.01)
            lon += random.uniform(-0.01, 0.01)
            
            candidates.append({
                'id': f'grid_{i}',
                'lat': np.clip(lat, self.city_bounds['min_lat'], self.city_bounds['max_lat']),
                'lon': np.clip(lon, self.city_bounds['min_lon'], self.city_bounds['max_lon']),
                'type': 'grid',
                'name': f'Grid Station {i+1}'
            })
        
        # Strategy 3: Random placements
        for i in range(self.num_stations):
            candidates.append({
                'id': f'random_{i}',
                'lat': random.uniform(self.city_bounds['min_lat'], self.city_bounds['max_lat']),
                'lon': random.uniform(self.city_bounds['min_lon'], self.city_bounds['max_lon']),
                'type': 'random',
                'name': f'Random Station {i+1}'
            })
        
        return candidates
    
    def calculate_reward(self, placement: List[Dict]) -> float:
        """
        Calculate reward for a placement configuration.
        
        Reward function: R = -α·T - β·D + γ·C
        - T: Average travel time to stations
        - D: Distance from demand centers
        - C: Coverage score
        
        Args:
            placement: List of station locations
            
        Returns:
            Reward value (higher is better)
        """
        if not placement:
            return -1000.0
        
        # Calculate average distance to nearest station from demand centers
        total_distance = 0.0
        for center in self.demand_centers:
            min_dist = float('inf')
            for station in placement:
                dist = self._haversine_distance(
                    center['lat'], center['lon'],
                    station['lat'], station['lon']
                )
                min_dist = min(min_dist, dist)
            total_distance += min_dist * center['weight']
        
        avg_distance = total_distance / len(self.demand_centers)
        
        # Calculate coverage (percentage of city within 2km of a station)
        coverage = self._calculate_coverage(placement)
        
        # Calculate spread (penalize clustering)
        spread = self._calculate_spread(placement)
        
        # Reward components (normalized)
        distance_score = -avg_distance * 10  # Penalize long distances
        coverage_score = coverage * 100  # Reward high coverage
        spread_score = spread * 50  # Reward good distribution
        
        reward = distance_score + coverage_score + spread_score
        
        return reward
    
    def _haversine_distance(self, lat1: float, lon1: float, 
                           lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula."""
        R = 6371.0  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _calculate_coverage(self, stations: List[Dict]) -> float:
        """Calculate coverage percentage (stations within 2km of demand centers)."""
        if not stations:
            return 0.0
        
        covered_centers = 0
        for center in self.demand_centers:
            for station in stations:
                dist = self._haversine_distance(
                    center['lat'], center['lon'],
                    station['lat'], station['lon']
                )
                if dist <= 2.0:  # Within 2km
                    covered_centers += 1
                    break
        
        return covered_centers / len(self.demand_centers)
    
    def _calculate_spread(self, stations: List[Dict]) -> float:
        """Calculate spread score (reward good distribution)."""
        if len(stations) < 2:
            return 0.0
        
        # Calculate average distance between stations
        total_dist = 0.0
        count = 0
        
        for i, s1 in enumerate(stations):
            for s2 in stations[i+1:]:
                dist = self._haversine_distance(
                    s1['lat'], s1['lon'],
                    s2['lat'], s2['lon']
                )
                total_dist += dist
                count += 1
        
        avg_dist = total_dist / count if count > 0 else 0.0
        
        # Normalize (ideal spread is around 3-5km between stations)
        if avg_dist < 1.0:
            return 0.0
        elif avg_dist > 5.0:
            return 1.0
        else:
            return avg_dist / 5.0
    
    def optimize_placement(self, algorithm: str = 'ucb') -> List[Dict]:
        """
        Optimize station placement using RL over multiple episodes.
        
        Args:
            algorithm: 'ucb' or 'epsilon_greedy'
            
        Returns:
            Best placement configuration found
        """
        logger.info(f"🚀 Starting RL optimization with {algorithm} algorithm")
        logger.info(f"   Stations: {self.num_stations}, Episodes: {self.num_episodes}")
        
        # Generate candidate placements
        candidates = self.generate_candidate_placements()
        logger.info(f"   Generated {len(candidates)} candidate placements")
        
        # Select bandit algorithm
        if algorithm == 'ucb':
            bandit = self.ucb_bandit
        else:
            bandit = self.epsilon_bandit
        
        # Run episodes
        best_reward = -float('inf')
        best_placement = None
        
        for episode in range(1, self.num_episodes + 1):
            logger.info(f"\n📊 Episode {episode}/{self.num_episodes}")
            
            # Select a placement configuration (arm)
            selected_arm = bandit.select_arm(candidates)
            
            # Create placement from selected arm
            # In real implementation, this would select multiple stations
            # For simplicity, we create a placement based on the arm type
            placement = self._create_placement_from_arm(selected_arm)
            
            # Calculate reward
            reward = self.calculate_reward(placement)
            
            # Update bandit
            bandit.update(selected_arm, reward)
            
            # Track best
            if reward > best_reward:
                best_reward = reward
                best_placement = placement.copy()
            
            self.episode_rewards.append(reward)
            
            logger.info(f"   Reward: {reward:.2f}, Best: {best_reward:.2f}")
            
            # Decay epsilon for epsilon-greedy
            if algorithm == 'epsilon_greedy':
                bandit.decay_epsilon()
        
        logger.info(f"\n✅ Optimization complete!")
        logger.info(f"   Best reward: {best_reward:.2f}")
        logger.info(f"   Final placement: {len(best_placement)} stations")
        
        return best_placement
    
    def _create_placement_from_arm(self, arm: Dict) -> List[Dict]:
        """
        Create a full placement configuration from a selected arm.
        
        In a full implementation, this would use the arm to generate
        a complete set of station locations. For this simplified version,
        we create a placement based on the arm type.
        """
        placement = []
        
        if arm['type'] == 'strategic':
            # Use strategic locations
            for i, center in enumerate(self.demand_centers[:self.num_stations]):
                placement.append({
                    'station_id': f'ST{i+1:02d}',
                    'lat': center['lat'],
                    'lon': center['lon'],
                    'name': center['name'],
                    'type': 'strategic'
                })
        elif arm['type'] == 'grid':
            # Use grid-based placement
            grid_size = int(np.ceil(np.sqrt(self.num_stations)))
            lat_range = self.city_bounds['max_lat'] - self.city_bounds['min_lat']
            lon_range = self.city_bounds['max_lon'] - self.city_bounds['min_lon']
            
            for i in range(self.num_stations):
                row = i // grid_size
                col = i % grid_size
                
                lat = self.city_bounds['min_lat'] + (row / grid_size) * lat_range
                lon = self.city_bounds['min_lon'] + (col / grid_size) * lon_range
                
                placement.append({
                    'station_id': f'ST{i+1:02d}',
                    'lat': lat,
                    'lon': lon,
                    'name': f'Grid Station {i+1}',
                    'type': 'grid'
                })
        else:  # random
            # Use random placement
            for i in range(self.num_stations):
                placement.append({
                    'station_id': f'ST{i+1:02d}',
                    'lat': random.uniform(
                        self.city_bounds['min_lat'], 
                        self.city_bounds['max_lat']
                    ),
                    'lon': random.uniform(
                        self.city_bounds['min_lon'],
                        self.city_bounds['max_lon']
                    ),
                    'name': f'Random Station {i+1}',
                    'type': 'random'
                })
        
        return placement
    
    def save_results(self, placement: List[Dict], output_file: str = "data/bhubaneswar_stations_rl.json"):
        """Save optimized placement to JSON file."""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        results = {
            'city': 'Bhubaneswar',
            'algorithm': 'RL (Multi-Armed Bandit)',
            'num_stations': len(placement),
            'num_episodes': self.num_episodes,
            'episode_rewards': self.episode_rewards,
            'final_reward': max(self.episode_rewards) if self.episode_rewards else 0,
            'stations': placement,
            'metrics': {
                'coverage': self._calculate_coverage(placement),
                'avg_distance': self._calculate_avg_distance_to_demand(placement),
                'spread': self._calculate_spread(placement)
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"💾 Results saved to: {output_file}")
    
    def _calculate_avg_distance_to_demand(self, stations: List[Dict]) -> float:
        """Calculate average distance from demand centers to nearest station."""
        total = 0.0
        for center in self.demand_centers:
            min_dist = float('inf')
            for station in stations:
                dist = self._haversine_distance(
                    center['lat'], center['lon'],
                    station['lat'], station['lon']
                )
                min_dist = min(min_dist, dist)
            total += min_dist
        return total / len(self.demand_centers)


def main():
    """Main function to run RL station placement."""
    print("=" * 60)
    print("RL-Based EV Charging Station Placement")
    print("Bhubaneswar - 25 Stations Optimization")
    print("=" * 60)
    
    # Initialize RL system
    rl_system = StationPlacementRL(num_stations=25, num_episodes=10)
    
    # Run optimization with UCB
    print("\n🔬 Running UCB algorithm...")
    ucb_placement = rl_system.optimize_placement(algorithm='ucb')
    rl_system.save_results(ucb_placement, "data/bhubaneswar_stations_ucb.json")
    
    # Reset for epsilon-greedy
    rl_system.ucb_bandit = UCB_Bandit()
    rl_system.epsilon_bandit = EpsilonGreedy_Bandit()
    rl_system.episode_rewards = []
    
    # Run optimization with Epsilon-Greedy
    print("\n🔬 Running Epsilon-Greedy algorithm...")
    epsilon_placement = rl_system.optimize_placement(algorithm='epsilon_greedy')
    rl_system.save_results(epsilon_placement, "data/bhubaneswar_stations_epsilon.json")
    
    # Compare results
    print("\n📊 Results Comparison:")
    print(f"   UCB Best Reward: {max(rl_system.episode_rewards) if rl_system.episode_rewards else 0:.2f}")
    print(f"   UCB Coverage: {rl_system._calculate_coverage(ucb_placement):.1%}")
    print(f"   Epsilon Coverage: {rl_system._calculate_coverage(epsilon_placement):.1%}")
    
    print("\n✅ RL optimization complete!")
    print("   Check data/ folder for results JSON files")


if __name__ == "__main__":
    main()

