"""
baseline_agents.py
==================
Naive baseline pricing agents that
RL agent must outperform.

Agents Implemented:
-------------------
1. FixedPriceAgent    : Always same price
2. RandomAgent        : Random price each day
3. TimedPricingAgent  : Price increases over time
4. DemandBasedAgent   : Price based on inventory
5. LinearDecayAgent   : Price decays linearly

Internship Spec:
"first code naive heuristic agents
(e.g., sell at fixed price,
discount by 10% every day)"

Infotact DS/ML Internship — Project 2
Week 1 : Baseline Agents
"""

import numpy as np
import os
import sys

# --------------------------------------------------
# Add project src directory to Python path
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)


# ─────────────────────────────────────────
# BASE AGENT CLASS
# ─────────────────────────────────────────

class BaseAgent:
    """
    Base class for all pricing agents.

    Parameters
    ----------
    env : DynamicPricingEnv
        The pricing environment.
    name : str
        Agent name for identification.
    """

    def __init__(self,
                 env: DynamicPricingEnv,
                 name: str):
        self.env  = env
        self.name = name
        self.n_prices = len(PRICE_LEVELS)

    def select_action(self,
                      state: np.ndarray) -> int:
        """
        Select pricing action given state.

        Parameters
        ----------
        state : np.ndarray
            Current state (inventory, days_left)

        Returns
        -------
        int
            Action index (price level)
        """
        raise NotImplementedError

    def run_episode(self,
                    seed: int = None) -> dict:
        """
        Run one complete episode.

        Parameters
        ----------
        seed : int
            Random seed.

        Returns
        -------
        dict
            Episode results.
        """
        obs, info = self.env.reset(seed=seed)
        total_revenue = 0
        total_sold    = 0
        prices_used   = []
        step          = 0

        while True:
            action = self.select_action(obs)
            obs, reward, terminated, \
                truncated, info = self.env.step(action)

            total_revenue += max(0, reward)
            if info['bought']:
                total_sold += 1
            prices_used.append(info['price'])
            step += 1

            if terminated or truncated:
                break

        return {
            'agent'         : self.name,
            'total_revenue' : total_revenue,
            'total_sold'    : total_sold,
            'steps'         : step,
            'avg_price'     : np.mean(prices_used),
            'prices_used'   : prices_used,
            'sell_through'  : total_sold /
                              self.env.max_inventory
        }


# ─────────────────────────────────────────
# AGENT 1: FIXED PRICE
# ─────────────────────────────────────────

class FixedPriceAgent(BaseAgent):
    """
    Always charges the same fixed price.
    Simplest possible strategy.

    Parameters
    ----------
    env : DynamicPricingEnv
        Pricing environment.
    price_idx : int
        Index of fixed price (default=2 = $150)
    """

    def __init__(self,
                 env: DynamicPricingEnv,
                 price_idx: int = 2):
        super().__init__(env, 'Fixed Price')
        self.price_idx = price_idx
        self.fixed_price = PRICE_LEVELS[price_idx]

    def select_action(self,
                      state: np.ndarray) -> int:
        return self.price_idx


# ─────────────────────────────────────────
# AGENT 2: RANDOM
# ─────────────────────────────────────────

class RandomAgent(BaseAgent):
    """
    Selects random price each step.
    True random baseline.
    """

    def __init__(self,
                 env: DynamicPricingEnv):
        super().__init__(env, 'Random')

    def select_action(self,
                      state: np.ndarray) -> int:
        return self.env.action_space.sample()


# ─────────────────────────────────────────
# AGENT 3: TIME BASED
# ─────────────────────────────────────────

class TimedPricingAgent(BaseAgent):
    """
    Adjusts price based on time remaining.

    Strategy:
    - Early days (>20 days): High price
    - Middle days (10-20):   Medium price
    - Late days (<10):       Low price
      (discount to clear inventory)

    Internship Spec:
    "Time-Based Pricing baseline"
    """

    def __init__(self,
                 env: DynamicPricingEnv):
        super().__init__(env, 'Time Based')

    def select_action(self,
                      state: np.ndarray) -> int:
        inventory = int(state[0])
        days_left = int(state[1])

        if days_left > 20:
            return 4    # $250 — premium early
        elif days_left > 10:
            return 3    # $200 — moderate mid
        elif days_left > 5:
            return 2    # $150 — standard late
        else:
            return 1    # $100 — discount urgent


# ─────────────────────────────────────────
# AGENT 4: DEMAND BASED
# ─────────────────────────────────────────

class DemandBasedAgent(BaseAgent):
    """
    Adjusts price based on remaining inventory.

    Strategy:
    - High inventory remaining: Lower price
      (need to sell more)
    - Low inventory remaining: Higher price
      (scarcity premium)

    Internship Spec:
    "flat Demand-Based Pricing baseline"
    """

    def __init__(self,
                 env: DynamicPricingEnv):
        super().__init__(env, 'Demand Based')

    def select_action(self,
                      state: np.ndarray) -> int:
        inventory = int(state[0])
        days_left = int(state[1])
        max_inv   = self.env.max_inventory

        # Inventory ratio
        inv_ratio = inventory / max_inv

        if inv_ratio > 0.8:
            return 1    # $100 — lots left, go cheap
        elif inv_ratio > 0.6:
            return 2    # $150 — moderate stock
        elif inv_ratio > 0.4:
            return 3    # $200 — selling well
        elif inv_ratio > 0.2:
            return 4    # $250 — running low
        else:
            return 5    # $300 — almost sold out!


# ─────────────────────────────────────────
# AGENT 5: LINEAR DECAY
# ─────────────────────────────────────────

class LinearDecayAgent(BaseAgent):
    """
    Linearly decreases price over time.
    Starts high, ends low.

    Internship Spec:
    "discount by 10% every day"
    """

    def __init__(self,
                 env: DynamicPricingEnv):
        super().__init__(env, 'Linear Decay')

    def select_action(self,
                      state: np.ndarray) -> int:
        inventory = int(state[0])
        days_left = int(state[1])
        max_days  = self.env.max_days

        # Linear decay from high to low
        progress = 1 - (days_left / max_days)
        idx = int(progress *
                  (self.n_prices - 1))
        idx = self.n_prices - 1 - idx
        return max(0, min(idx,
                          self.n_prices - 1))


# ─────────────────────────────────────────
# INIT FILE
# ─────────────────────────────────────────

if __name__ == "__main__":
    env = DynamicPricingEnv()

    agents = [
        FixedPriceAgent(env),
        RandomAgent(env),
        TimedPricingAgent(env),
        DemandBasedAgent(env),
        LinearDecayAgent(env)
    ]

    print("=" * 50)
    print("  BASELINE AGENTS TEST")
    print("=" * 50)

    for agent in agents:
        result = agent.run_episode(seed=42)
        print(f"\n  {agent.name}")
        print(f"  Revenue : ${result['total_revenue']:.0f}")
        print(f"  Sold    : {result['total_sold']}/50")
        print(f"  Avg $   : ${result['avg_price']:.0f}")