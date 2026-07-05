"""
pricing_env.py
==============
Custom OpenAI Gymnasium environment
for airline/hotel dynamic pricing.

State  : (remaining_inventory, days_until_departure)
Action : price_level (0-5)
Reward : Revenue earned per step

Internship Spec:
"build a custom OpenAI Gym environment
representing the airline/hotel booking
process"

Infotact DS/ML Internship — Project 2
Week 1 : MDP + Gym Environment
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces


# ─────────────────────────────────────────
# PRICE LEVELS
# ─────────────────────────────────────────

PRICE_LEVELS = [50, 100, 150, 200, 250, 300]


# ─────────────────────────────────────────
# PRICING ENVIRONMENT
# ─────────────────────────────────────────

class DynamicPricingEnv(gym.Env):
    """
    Custom Gymnasium environment for
    dynamic pricing of finite inventory.

    The agent must learn to price airline
    tickets or hotel rooms optimally to
    maximize total revenue.

    Parameters
    ----------
    max_inventory : int
        Starting inventory (default=50)
    max_days : int
        Days in selling season (default=30)
    """

    metadata = {'render_modes': ['human']}

    def __init__(self,
                 max_inventory: int = 50,
                 max_days: int = 30):

        super(DynamicPricingEnv, self).__init__()

        # Environment parameters
        self.max_inventory = max_inventory
        self.max_days      = max_days
        self.price_levels  = PRICE_LEVELS
        self.n_prices      = len(PRICE_LEVELS)

        # ── State Space ──
        # (remaining_inventory, days_until_departure)
        self.observation_space = spaces.Box(
            low   = np.array([0, 0]),
            high  = np.array([max_inventory, max_days]),
            dtype = np.float32
        )

        # ── Action Space ──
        # Discrete price levels
        self.action_space = spaces.Discrete(
            self.n_prices
        )

        # Initialize state
        self.inventory = max_inventory
        self.days_left = max_days
        self.total_revenue = 0

    # ─────────────────────────────────────
    # DEMAND FUNCTION
    # ─────────────────────────────────────

    def _get_demand_probability(
            self,
            price: float,
            days_left: int) -> float:
        """
        Stochastic demand function.

        Purchase probability depends on:
        1. Price → Higher price = lower demand
        2. Days left → Less time = lower demand
           (urgency effect)

        Parameters
        ----------
        price : float
            Current price level.
        days_left : int
            Days remaining in season.

        Returns
        -------
        float
            Probability of customer purchase.
        """
        # Base probability
        base_prob = 0.7

        # Price sensitivity
        # Higher price → lower probability
        price_factor = 1 - (
            (price - min(PRICE_LEVELS)) /
            (max(PRICE_LEVELS) - min(PRICE_LEVELS))
        ) * 0.6

        # Time sensitivity
        # Fewer days → slightly lower probability
        # (less time for customers to find deal)
        time_factor = 0.7 + 0.3 * (
            days_left / self.max_days
        )

        # Combined probability
        prob = base_prob * price_factor * time_factor

        # Add stochastic noise
        noise = np.random.normal(0, 0.05)
        prob  = np.clip(prob + noise, 0.05, 0.95)

        return prob

    # ─────────────────────────────────────
    # STEP FUNCTION
    # ─────────────────────────────────────

    def step(self, action: int) -> tuple:
        """
        Execute one pricing step.

        Parameters
        ----------
        action : int
            Price level index (0-5).

        Returns
        -------
        tuple
            (observation, reward, terminated,
             truncated, info)
        """
        # Get price for this action
        price = self.price_levels[action]

        # Calculate demand probability
        prob = self._get_demand_probability(
            price, self.days_left
        )

        # Simulate customer arrival
        customer_bought = np.random.random() < prob

        # Calculate reward
        if self.inventory > 0 and customer_bought:
            reward = float(price)
            self.inventory -= 1
            self.total_revenue += price
        else:
            reward = 0.0

        # Advance time
        self.days_left -= 1

        # Check termination
        terminated = (self.inventory == 0)
        truncated  = (self.days_left == 0)

        # Penalty for unsold inventory
        if truncated and self.inventory > 0:
            penalty = -10 * self.inventory
            reward += penalty
            self.total_revenue += penalty

        # Get observation
        observation = self._get_observation()

        info = {
            'price'          : price,
            'bought'         : customer_bought,
            'inventory'      : self.inventory,
            'days_left'      : self.days_left,
            'total_revenue'  : self.total_revenue,
            'demand_prob'    : prob
        }

        return observation, reward, terminated, \
               truncated, info

    # ─────────────────────────────────────
    # RESET FUNCTION
    # ─────────────────────────────────────

    def reset(self, seed=None,
              options=None) -> tuple:
        """
        Reset environment to initial state.

        Parameters
        ----------
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple
            (observation, info)
        """
        super().reset(seed=seed)

        self.inventory     = self.max_inventory
        self.days_left     = self.max_days
        self.total_revenue = 0

        observation = self._get_observation()
        info        = {}

        return observation, info

    # ─────────────────────────────────────
    # HELPER FUNCTIONS
    # ─────────────────────────────────────

    def _get_observation(self) -> np.ndarray:
        """Get current state observation."""
        return np.array(
            [self.inventory, self.days_left],
            dtype=np.float32
        )

    def get_state_tuple(self) -> tuple:
        """Get state as tuple for Q-table."""
        return (self.inventory, self.days_left)

    def render(self):
        """Render current environment state."""
        print(f"  Days Left  : {self.days_left}")
        print(f"  Inventory  : {self.inventory}")
        print(f"  Revenue    : ${self.total_revenue}")

    def close(self):
        """Close environment."""
        pass


# ─────────────────────────────────────────
# ENVIRONMENT INIT FILE
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("Testing DynamicPricingEnv...")
    print("=" * 40)

    env = DynamicPricingEnv(
        max_inventory=50,
        max_days=30
    )

    # Test reset
    obs, info = env.reset(seed=42)
    print(f"Initial State: {obs}")
    print(f"Action Space : {env.action_space}")
    print(f"Obs Space    : {env.observation_space}")

    # Test one episode with random actions
    total_reward = 0
    steps = 0

    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = (
            env.step(action)
        )
        total_reward += reward
        steps += 1

        if terminated or truncated:
            break

    print(f"\nRandom Episode:")
    print(f"  Steps        : {steps}")
    print(f"  Total Revenue: ${total_reward:.0f}")
    print(f"  Final State  : {obs}")
    print("\n✅ Environment working correctly!")