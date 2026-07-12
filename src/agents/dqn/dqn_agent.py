"""
dqn_agent.py
============
Complete Deep Q-Network (DQN) agent
for dynamic pricing optimization.

Components:
1. Online Network  : Learns Q-values
2. Target Network  : Stable training target
3. Replay Buffer   : Breaks correlations
4. Epsilon Greedy  : Exploration strategy

Internship Spec:
"replace the Q-table with a Neural Network
(Deep Q-Network). The intern must handle
the exploration-exploitation trade-off
using an epsilon-greedy strategy and
implement experience replay to
stabilize training."

Infotact DS/ML Internship — Project 2
Week 2 : DQN Agent
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import pandas as pd
import os
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)
from agents.dqn.dqn_network import DQNNetwork
from agents.dqn.replay_buffer import ReplayBuffer
from config import DQN


# ─────────────────────────────────────────
# DQN AGENT
# ─────────────────────────────────────────

class DQNAgent:
    """
    Deep Q-Network agent for dynamic pricing.

    Uses two networks:
    - Online network  : Updated every step
    - Target network  : Updated every N steps
                        (provides stable targets)

    Parameters
    ----------
    env : DynamicPricingEnv
        Pricing environment.
    config : dict
        DQN hyperparameters.
    device : str
        Compute device ('cpu' or 'cuda')
    """

    def __init__(self,
                 env: DynamicPricingEnv,
                 config: dict = None,
                 device: str = None):

        self.env    = env
        self.config = config or DQN
        self.name   = 'DQN'

        # Device setup
        if device is None:
            self.device = 'cuda' if \
                torch.cuda.is_available() \
                else 'cpu'
        else:
            self.device = device

        print(f"  Using device: {self.device}")

        # State and action sizes
        self.state_size  = 2
        self.action_size = env.action_space.n

        # Extract config
        self.lr           = self.config['lr']
        self.gamma        = self.config['gamma']
        self.epsilon      = self.config['eps_start']
        self.eps_end      = self.config['eps_end']
        self.eps_decay    = self.config['eps_decay']
        self.batch_size   = self.config['batch_size']
        self.target_update= self.config['target_update']
        self.n_episodes   = self.config['n_episodes']

        # ── Networks ──
        self.online_net = DQNNetwork(
            state_size   = self.state_size,
            action_size  = self.action_size,
            hidden_sizes = self.config['hidden_size']
        ).to(self.device)

        self.target_net = DQNNetwork(
            state_size   = self.state_size,
            action_size  = self.action_size,
            hidden_sizes = self.config['hidden_size']
        ).to(self.device)

        # Copy weights to target
        self.target_net.load_state_dict(
            self.online_net.state_dict()
        )
        self.target_net.eval()

        # ── Optimizer and Loss ──
        self.optimizer = optim.Adam(
            self.online_net.parameters(),
            lr=self.lr
        )
        self.loss_fn = nn.MSELoss()

        # ── Replay Buffer ──
        self.buffer = ReplayBuffer(
            capacity=self.config['memory_size']
        )

        # ── Training History ──
        self.episode_rewards  = []
        self.episode_losses   = []
        self.episode_epsilons = []
        self.training_complete = False
        self.steps_done        = 0

    # ─────────────────────────────────────
    # NORMALIZE STATE
    # ─────────────────────────────────────

    def _normalize_state(self,
                          state: np.ndarray
                          ) -> np.ndarray:
        """
        Normalize state to [0, 1] range.
        Helps neural network learn faster!

        Parameters
        ----------
        state : np.ndarray
            Raw state (inventory, days_left)

        Returns
        -------
        np.ndarray
            Normalized state.
        """
        norm_state = np.array([
            state[0] / self.env.max_inventory,
            state[1] / self.env.max_days
        ], dtype=np.float32)
        return norm_state

    # ─────────────────────────────────────
    # ACTION SELECTION
    # ─────────────────────────────────────

    def select_action(self,
                      state: np.ndarray,
                      training: bool = True) -> int:
        """
        Epsilon-greedy action selection.

        Training mode:
        → Explore with prob epsilon
        → Exploit with prob 1-epsilon

        Eval mode:
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
            Selected action.
        """
        if training and \
           np.random.random() < self.epsilon:
            # Explore: random action
            return self.env.action_space.sample()

        # Exploit: best Q-value action
        norm_state = self._normalize_state(state)
        state_tensor = torch.FloatTensor(
            norm_state
        ).unsqueeze(0).to(self.device)

        with torch.no_grad():
            q_values = self.online_net(state_tensor)

        return q_values.argmax().item()

    # ─────────────────────────────────────
    # LEARNING STEP
    # ─────────────────────────────────────

    def learn(self) -> float:
        """
        Sample from buffer and update network.

        Returns
        -------
        float
            Training loss value.
        """
        if not self.buffer.is_ready(self.batch_size):
            return 0.0

        # Sample mini-batch
        states, actions, rewards, \
            next_states, dones = self.buffer.sample(
                self.batch_size
            )

        # Normalize states
        states_norm = np.array([
            self._normalize_state(s)
            for s in states
        ])
        next_states_norm = np.array([
            self._normalize_state(s)
            for s in next_states
        ])

        # Convert to tensors
        states_t      = torch.FloatTensor(
            states_norm
        ).to(self.device)
        actions_t     = torch.LongTensor(
            actions
        ).to(self.device)
        rewards_t     = torch.FloatTensor(
            rewards
        ).to(self.device)
        next_states_t = torch.FloatTensor(
            next_states_norm
        ).to(self.device)
        dones_t       = torch.FloatTensor(
            dones
        ).to(self.device)

        # ── Current Q-values (online network) ──
        current_q = self.online_net(
            states_t
        ).gather(1, actions_t.unsqueeze(1))

        # ── Target Q-values (target network) ──
        with torch.no_grad():
            next_q = self.target_net(
                next_states_t
            ).max(1)[0]
            target_q = (
                rewards_t +
                self.gamma * next_q * (1 - dones_t)
            ).unsqueeze(1)

        # ── Compute Loss ──
        loss = self.loss_fn(current_q, target_q)

        # ── Backpropagate ──
        self.optimizer.zero_grad()
        loss.backward()

        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(
            self.online_net.parameters(),
            max_norm=1.0
        )
        self.optimizer.step()

        return loss.item()

    # ─────────────────────────────────────
    # UPDATE TARGET NETWORK
    # ─────────────────────────────────────

    def update_target_network(self):
        """
        Copy online network weights to target.
        Called every target_update episodes.
        """
        self.target_net.load_state_dict(
            self.online_net.state_dict()
        )

    # ─────────────────────────────────────
    # EPSILON DECAY
    # ─────────────────────────────────────

    def decay_epsilon(self):
        """Decay exploration rate."""
        self.epsilon = max(
            self.eps_end,
            self.epsilon * self.eps_decay
        )

    # ─────────────────────────────────────
    # TRAINING
    # ─────────────────────────────────────

    def train(self,
              n_episodes: int = None,
              verbose: bool = True) -> list:
        """
        Train DQN agent.

        Parameters
        ----------
        n_episodes : int
            Training episodes.
        verbose : bool
            Print progress.

        Returns
        -------
        list
            Episode rewards.
        """
        n_episodes = n_episodes or self.n_episodes

        print("=" * 55)
        print("  DQN TRAINING")
        print(f"  Episodes     : {n_episodes}")
        print(f"  Batch size   : {self.batch_size}")
        print(f"  Buffer size  : "
              f"{self.config['memory_size']}")
        print(f"  Target update: "
              f"every {self.target_update} eps")
        print(f"  Device       : {self.device}")
        print("=" * 55)

        for episode in range(n_episodes):
            state, _     = self.env.reset()
            total_reward = 0
            total_loss   = 0
            steps        = 0
            done         = False

            while not done:
                # Select action
                action = self.select_action(
                    state, training=True
                )

                # Step environment
                next_state, reward, terminated, \
                    truncated, _ = self.env.step(action)
                done = terminated or truncated

                # Store in replay buffer
                self.buffer.push(
                    state, action, reward,
                    next_state, done
                )

                # Learn from replay buffer
                loss = self.learn()

                state        = next_state
                total_reward += reward
                total_loss   += loss
                steps        += 1
                self.steps_done += 1

            # Update target network
            if (episode + 1) % self.target_update == 0:
                self.update_target_network()

            # Decay epsilon
            self.decay_epsilon()

            # Store history
            self.episode_rewards.append(total_reward)
            self.episode_losses.append(
                total_loss / max(steps, 1)
            )
            self.episode_epsilons.append(self.epsilon)

            # Print progress
            if verbose and \
               (episode + 1) % 200 == 0:
                mean_r = np.mean(
                    self.episode_rewards[-100:]
                )
                mean_l = np.mean(
                    self.episode_losses[-100:]
                )
                print(f"  Ep {episode+1:4d} | "
                      f"Rev: {mean_r:8.0f} | "
                      f"Loss: {mean_l:.4f} | "
                      f"ε: {self.epsilon:.3f} | "
                      f"Buf: {len(self.buffer)}")

        self.training_complete = True
        final_mean = np.mean(
            self.episode_rewards[-100:]
        )
        print(f"\n✅ DQN Training Complete!")
        print(f"   Final 100-ep mean: ${final_mean:.0f}")

        return self.episode_rewards

    # ─────────────────────────────────────
    # EVALUATION
    # ─────────────────────────────────────

    def evaluate(self,
                 n_episodes: int = 100,
                 seed: int = 42) -> dict:
        """
        Evaluate trained DQN agent.

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
            state, _ = self.env.reset(seed=seed+ep)
            total_rev  = 0
            total_sold = 0
            done       = False

            while not done:
                action = self.select_action(
                    state, training=False
                )
                state, reward, term, trunc, info = (
                    self.env.step(action)
                )
                done = term or trunc
                total_rev  += max(0, reward)
                if info['bought']:
                    total_sold += 1

            revenues.append(total_rev)
            sold_list.append(total_sold)

        results = {
            'agent'        : self.name,
            'mean_revenue' : np.mean(revenues),
            'std_revenue'  : np.std(revenues),
            'max_revenue'  : np.max(revenues),
            'mean_sold'    : np.mean(sold_list),
            'revenues'     : revenues
        }

        print(f"\n  DQN Evaluation:")
        print(f"  Mean Revenue: "
              f"${results['mean_revenue']:.0f}"
              f" ± ${results['std_revenue']:.0f}")
        print(f"  Mean Sold   : "
              f"{results['mean_sold']:.1f}/50")

        return results


# ─────────────────────────────────────────
# MAIN TEST
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("Testing DQN Agent...\n")

    env   = DynamicPricingEnv()
    agent = DQNAgent(env)

    agent.online_net.print_architecture()

    print("\nRunning short training test "
          "(100 episodes)...")
    rewards = agent.train(
        n_episodes=100,
        verbose=True
    )

    print(f"\nBuffer size: {len(agent.buffer)}")
    print(f"Mean reward: ${np.mean(rewards):.0f}")
    print("\n✅ DQN Agent working correctly!")