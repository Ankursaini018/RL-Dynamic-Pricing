"""
q_learning_agent.py
===================
Tabular Q-Learning agent for
dynamic pricing optimization.

Q-Learning creates a Q-table that maps
every possible (state, action) pair to
expected future reward.

Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]

Where:
α = learning rate
γ = discount factor
r = immediate reward
s = current state
a = current action
s' = next state

Internship Spec:
"implement a fundamental Q-Learning
algorithm, creating a Q-table that maps
every possible (inventory, time) state
to the most profitable price action"

Infotact DS/ML Internship — Project 2
Week 1 : Q-Learning Implementation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import pickle
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
# Q-LEARNING CONFIG
# ─────────────────────────────────────────

QL_CONFIG = {
    'learning_rate'    : 0.1,    # α
    'discount_factor'  : 0.99,   # γ
    'epsilon_start'    : 1.0,    # exploration
    'epsilon_end'      : 0.01,   # min exploration
    'epsilon_decay'    : 0.995,  # decay rate
    'n_episodes'       : 5000,   # training episodes
}


# ─────────────────────────────────────────
# Q-LEARNING AGENT
# ─────────────────────────────────────────

class QLearningAgent:
    """
    Tabular Q-Learning agent.

    Maintains a Q-table of shape:
    (max_inventory+1, max_days+1, n_actions)

    Parameters
    ----------
    env : DynamicPricingEnv
        The pricing environment.
    config : dict
        Q-Learning hyperparameters.
    """

    def __init__(self,
                 env: DynamicPricingEnv,
                 config: dict = None):

        self.env     = env
        self.config  = config or QL_CONFIG
        self.name    = 'Q-Learning'

        # Extract config
        self.lr       = self.config['learning_rate']
        self.gamma    = self.config['discount_factor']
        self.epsilon  = self.config['epsilon_start']
        self.eps_end  = self.config['epsilon_end']
        self.eps_dec  = self.config['epsilon_decay']

        # Q-table dimensions
        self.n_inv    = env.max_inventory + 1
        self.n_days   = env.max_days + 1
        self.n_act    = env.action_space.n

        # Initialize Q-table with zeros
        self.q_table  = np.zeros((
            self.n_inv,
            self.n_days,
            self.n_act
        ))

        # Training history
        self.episode_rewards    = []
        self.episode_epsilons   = []
        self.training_complete  = False

    # ─────────────────────────────────────
    # STATE TO INDEX
    # ─────────────────────────────────────

    def _state_to_idx(self,
                       state: np.ndarray) -> tuple:
        """
        Convert continuous state to Q-table index.

        Parameters
        ----------
        state : np.ndarray
            State array (inventory, days_left)

        Returns
        -------
        tuple
            (inventory_idx, days_idx)
        """
        inv_idx  = int(np.clip(
            state[0], 0, self.n_inv - 1
        ))
        days_idx = int(np.clip(
            state[1], 0, self.n_days - 1
        ))
        return inv_idx, days_idx

    # ─────────────────────────────────────
    # ACTION SELECTION
    # ─────────────────────────────────────

    def select_action(self,
                      state: np.ndarray,
                      training: bool = True) -> int:
        """
        Epsilon-greedy action selection.

        During training:
        → With prob epsilon: explore (random)
        → With prob 1-epsilon: exploit (best Q)

        During evaluation:
        → Always exploit (greedy)

        Parameters
        ----------
        state : np.ndarray
            Current state.
        training : bool
            Whether in training mode.

        Returns
        -------
        int
            Selected action index.
        """
        if training and np.random.random() < self.epsilon:
            # Explore: random action
            return self.env.action_space.sample()
        else:
            # Exploit: best known action
            inv_idx, days_idx = self._state_to_idx(
                state
            )
            return np.argmax(
                self.q_table[inv_idx, days_idx]
            )

    # ─────────────────────────────────────
    # Q-TABLE UPDATE
    # ─────────────────────────────────────

    def update(self,
               state: np.ndarray,
               action: int,
               reward: float,
               next_state: np.ndarray,
               done: bool):
        """
        Update Q-table using Bellman equation.

        Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]

        Parameters
        ----------
        state : np.ndarray
            Current state.
        action : int
            Action taken.
        reward : float
            Reward received.
        next_state : np.ndarray
            Next state.
        done : bool
            Episode terminated.
        """
        inv_idx, days_idx = self._state_to_idx(state)
        next_inv, next_days = self._state_to_idx(
            next_state
        )

        # Current Q value
        current_q = self.q_table[
            inv_idx, days_idx, action
        ]

        # Target Q value
        if done:
            target_q = reward
        else:
            # Bellman equation
            max_next_q = np.max(
                self.q_table[next_inv, next_days]
            )
            target_q = reward + (
                self.gamma * max_next_q
            )

        # Update Q value
        self.q_table[inv_idx, days_idx, action] += (
            self.lr * (target_q - current_q)
        )

    # ─────────────────────────────────────
    # EPSILON DECAY
    # ─────────────────────────────────────

    def decay_epsilon(self):
        """Decay exploration rate."""
        self.epsilon = max(
            self.eps_end,
            self.epsilon * self.eps_dec
        )

    # ─────────────────────────────────────
    # TRAINING
    # ─────────────────────────────────────

    def train(self,
              n_episodes: int = None,
              verbose: bool = True) -> list:
        """
        Train Q-Learning agent.

        Parameters
        ----------
        n_episodes : int
            Training episodes.
        verbose : bool
            Print progress.

        Returns
        -------
        list
            Episode rewards history.
        """
        if n_episodes is None:
            n_episodes = self.config['n_episodes']

        print("=" * 55)
        print("  Q-LEARNING TRAINING")
        print(f"  Episodes : {n_episodes}")
        print(f"  α (lr)   : {self.lr}")
        print(f"  γ (disc) : {self.gamma}")
        print(f"  ε start  : {self.epsilon}")
        print("=" * 55)

        for episode in range(n_episodes):
            state, _ = self.env.reset()
            total_reward = 0
            done = False

            while not done:
                # Select action
                action = self.select_action(
                    state, training=True
                )

                # Step environment
                next_state, reward, terminated, \
                    truncated, _ = self.env.step(action)

                done = terminated or truncated

                # Update Q-table
                self.update(
                    state, action, reward,
                    next_state, done
                )

                state        = next_state
                total_reward += reward

            # Decay epsilon
            self.decay_epsilon()

            # Store history
            self.episode_rewards.append(total_reward)
            self.episode_epsilons.append(self.epsilon)

            # Print progress
            if verbose and (episode + 1) % 500 == 0:
                recent_mean = np.mean(
                    self.episode_rewards[-100:]
                )
                print(f"  Episode {episode+1:5d} | "
                      f"Reward: {recent_mean:8.0f} | "
                      f"ε: {self.epsilon:.4f}")

        self.training_complete = True
        final_mean = np.mean(
            self.episode_rewards[-100:]
        )
        print(f"\n✅ Training complete!")
        print(f"   Final 100-ep mean: "
              f"${final_mean:.0f}")

        return self.episode_rewards

    # ─────────────────────────────────────
    # EVALUATION
    # ─────────────────────────────────────

    def evaluate(self,
                 n_episodes: int = 100,
                 seed: int = 42) -> dict:
        """
        Evaluate trained agent (no exploration).

        Parameters
        ----------
        n_episodes : int
            Evaluation episodes.
        seed : int
            Random seed.

        Returns
        -------
        dict
            Evaluation results.
        """
        revenues  = []
        sold_list = []

        for ep in range(n_episodes):
            state, _ = self.env.reset(
                seed=seed + ep
            )
            total_revenue = 0
            total_sold    = 0
            done          = False

            while not done:
                # Greedy action (no exploration)
                action = self.select_action(
                    state, training=False
                )
                state, reward, terminated, \
                    truncated, info = self.env.step(
                        action
                    )
                done = terminated or truncated

                total_revenue += max(0, reward)
                if info['bought']:
                    total_sold += 1

            revenues.append(total_revenue)
            sold_list.append(total_sold)

        results = {
            'agent'         : self.name,
            'mean_revenue'  : np.mean(revenues),
            'std_revenue'   : np.std(revenues),
            'max_revenue'   : np.max(revenues),
            'mean_sold'     : np.mean(sold_list),
            'revenues'      : revenues
        }

        print(f"\n  {self.name} Evaluation:")
        print(f"  Mean Revenue: "
              f"${results['mean_revenue']:.0f}"
              f" ± ${results['std_revenue']:.0f}")
        print(f"  Mean Sold   : "
              f"{results['mean_sold']:.1f}/50")

        return results

    # ─────────────────────────────────────
    # GET LEARNED POLICY
    # ─────────────────────────────────────

    def get_policy(self) -> np.ndarray:
        """
        Extract greedy policy from Q-table.

        Returns
        -------
        np.ndarray
            Policy array (inventory × days)
            showing best price action.
        """
        policy = np.argmax(self.q_table, axis=2)
        return policy

    def get_price_policy(self) -> np.ndarray:
        """
        Get policy in terms of actual prices.

        Returns
        -------
        np.ndarray
            Price policy array.
        """
        policy = self.get_policy()
        price_policy = np.vectorize(
            lambda x: PRICE_LEVELS[x]
        )(policy)
        return price_policy


if __name__ == "__main__":
    env   = DynamicPricingEnv()
    agent = QLearningAgent(env)

    print("Training Q-Learning agent...")
    rewards = agent.train(n_episodes=1000)

    print("\nEvaluating...")
    results = agent.evaluate(n_episodes=50)
    print(f"\nFinal Revenue: ${results['mean_revenue']:.0f}")