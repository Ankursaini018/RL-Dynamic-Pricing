"""
ppo_agent.py
============
Proximal Policy Optimization (PPO)
agent for dynamic pricing.

PPO Key Features:
→ Actor-Critic architecture
→ Clipped objective function
→ Generalized Advantage Estimation
→ Multiple update epochs per batch

Infotact DS/ML Internship — Project 2
Week 3 : PPO Agent
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)
from agents.ppo.ppo_network import ActorCriticNetwork
from config import PPO


# ─────────────────────────────────────────
# ROLLOUT BUFFER
# ─────────────────────────────────────────

class RolloutBuffer:
    """
    Stores experience rollouts for PPO.
    Different from DQN replay buffer!
    PPO is ON-POLICY so buffer is
    cleared after each update.

    Parameters
    ----------
    buffer_size : int
        Maximum rollout size.
    state_size : int
        State dimensions.
    """

    def __init__(self,
                 buffer_size: int = 2048,
                 state_size: int = 2):
        self.buffer_size = buffer_size
        self.state_size  = state_size
        self.clear()

    def clear(self):
        """Clear buffer for new rollout."""
        self.states      = []
        self.actions     = []
        self.rewards     = []
        self.values      = []
        self.log_probs   = []
        self.dones       = []

    def push(self,
             state, action, reward,
             value, log_prob, done):
        """Add single step to buffer."""
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.values.append(value)
        self.log_probs.append(log_prob)
        self.dones.append(done)

    def compute_returns(self,
                        gamma: float = 0.99,
                        gae_lambda: float = 0.95,
                        last_value: float = 0):
        """
        Compute GAE advantages and returns.

        GAE = Generalized Advantage Estimation
        Balances bias vs variance in advantage.

        Parameters
        ----------
        gamma : float
            Discount factor.
        gae_lambda : float
            GAE lambda parameter.
        last_value : float
            Bootstrap value for last state.
        """
        advantages = []
        returns    = []
        gae        = 0

        values = self.values + [last_value]

        for step in reversed(
            range(len(self.rewards))
        ):
            delta = (
                self.rewards[step] +
                gamma * values[step+1] *
                (1 - self.dones[step]) -
                values[step]
            )
            gae = (
                delta +
                gamma * gae_lambda *
                (1 - self.dones[step]) * gae
            )
            advantages.insert(0, gae)
            returns.insert(0, gae + values[step])

        self.advantages = advantages
        self.returns    = returns

    def get_tensors(self, device: str = 'cpu'):
        """Convert buffer to tensors."""
        states     = torch.FloatTensor(
            np.array(self.states)
        ).to(device)
        actions    = torch.LongTensor(
            self.actions
        ).to(device)
        log_probs  = torch.FloatTensor(
            self.log_probs
        ).to(device)
        returns    = torch.FloatTensor(
            self.returns
        ).to(device)
        advantages = torch.FloatTensor(
            self.advantages
        ).to(device)

        # Normalize advantages
        advantages = (
            (advantages - advantages.mean()) /
            (advantages.std() + 1e-8)
        )

        return (states, actions, log_probs,
                returns, advantages)

    def __len__(self):
        return len(self.states)


# ─────────────────────────────────────────
# PPO AGENT
# ─────────────────────────────────────────

class PPOAgent:
    """
    Proximal Policy Optimization agent
    for dynamic pricing.

    Parameters
    ----------
    env : DynamicPricingEnv
        Pricing environment.
    config : dict
        PPO hyperparameters.
    device : str
        Compute device.
    """

    def __init__(self,
                 env: DynamicPricingEnv,
                 config: dict = None,
                 device: str = None):

        self.env    = env
        self.config = config or PPO
        self.name   = 'PPO'

        # Device
        self.device = device or (
            'cuda' if torch.cuda.is_available()
            else 'cpu'
        )
        print(f"  PPO using device: {self.device}")

        # Dimensions
        self.state_size  = 2
        self.action_size = env.action_space.n

        # Extract config
        self.lr          = self.config['learning_rate']
        self.n_steps     = self.config['n_steps']
        self.batch_size  = self.config['batch_size']
        self.n_epochs    = self.config['n_epochs']
        self.gamma       = self.config['gamma']
        self.gae_lambda  = self.config['gae_lambda']
        self.clip_range  = self.config['clip_range']
        self.ent_coef    = self.config['ent_coef']
        self.vf_coef     = self.config['vf_coef']
        self.max_grad    = self.config['max_grad_norm']

        # Network
        self.network = ActorCriticNetwork(
            self.state_size,
            self.action_size,
            self.config['hidden_size']
        ).to(self.device)

        # Optimizer
        self.optimizer = optim.Adam(
            self.network.parameters(),
            lr=self.lr,
            eps=1e-5
        )

        # Rollout buffer
        self.buffer = RolloutBuffer(
            self.n_steps,
            self.state_size
        )

        # Training history
        self.episode_rewards  = []
        self.episode_losses   = []
        self.training_complete = False

    # ─────────────────────────────────────
    # NORMALIZE STATE
    # ─────────────────────────────────────

    def _normalize(self,
                   state: np.ndarray) -> np.ndarray:
        """Normalize state to [0,1]."""
        return np.array([
            state[0] / self.env.max_inventory,
            state[1] / self.env.max_days
        ], dtype=np.float32)

    # ─────────────────────────────────────
    # ACTION SELECTION
    # ─────────────────────────────────────

    def select_action(self,
                      state: np.ndarray,
                      training: bool = True
                      ) -> tuple:
        """
        Select action using current policy.

        Parameters
        ----------
        state : np.ndarray
            Current state.
        training : bool
            Training or evaluation mode.

        Returns
        -------
        tuple
            (action, log_prob, value)
            or just action if not training
        """
        norm  = self._normalize(state)
        action, log_prob, value = (
            self.network.get_action(
                norm, self.device
            )
        )

        if training:
            return action, log_prob, value
        return action

    # ─────────────────────────────────────
    # PPO UPDATE
    # ─────────────────────────────────────

    def update(self) -> dict:
        """
        Perform PPO policy update.

        Key steps:
        1. Compute advantages (GAE)
        2. For K epochs:
           a. Sample mini-batches
           b. Compute ratio
           c. Clip ratio
           d. Compute losses
           e. Update network

        Returns
        -------
        dict
            Update metrics.
        """
        # Get tensors from buffer
        states, actions, old_log_probs, \
            returns, advantages = (
                self.buffer.get_tensors(self.device)
            )

        total_loss   = 0
        policy_loss  = 0
        value_loss   = 0
        entropy_loss = 0
        n_updates    = 0

        buffer_size = len(self.buffer)

        # Multiple epochs
        for epoch in range(self.n_epochs):
            # Mini-batch indices
            indices = np.random.permutation(
                buffer_size
            )

            for start in range(
                0, buffer_size, self.batch_size
            ):
                end        = start + self.batch_size
                batch_idx  = indices[start:end]

                # Batch data
                b_states      = states[batch_idx]
                b_actions     = actions[batch_idx]
                b_old_lp      = old_log_probs[batch_idx]
                b_returns     = returns[batch_idx]
                b_advantages  = advantages[batch_idx]

                # Evaluate current policy
                new_log_probs, values, entropy = (
                    self.network.evaluate_action(
                        b_states, b_actions
                    )
                )

                # PPO ratio
                ratio = torch.exp(
                    new_log_probs - b_old_lp
                )

                # Clipped surrogate objective
                surr1 = ratio * b_advantages
                surr2 = torch.clamp(
                    ratio,
                    1 - self.clip_range,
                    1 + self.clip_range
                ) * b_advantages

                # Policy loss
                p_loss = -torch.min(
                    surr1, surr2
                ).mean()

                # Value loss
                v_loss = nn.MSELoss()(
                    values, b_returns
                )

                # Entropy bonus
                e_loss = -entropy.mean()

                # Total loss
                loss = (
                    p_loss +
                    self.vf_coef * v_loss +
                    self.ent_coef * e_loss
                )

                # Update
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(
                    self.network.parameters(),
                    self.max_grad
                )
                self.optimizer.step()

                total_loss   += loss.item()
                policy_loss  += p_loss.item()
                value_loss   += v_loss.item()
                entropy_loss += e_loss.item()
                n_updates    += 1

        # Clear buffer
        self.buffer.clear()

        return {
            'loss'         : total_loss / n_updates,
            'policy_loss'  : policy_loss / n_updates,
            'value_loss'   : value_loss / n_updates,
            'entropy'      : -entropy_loss / n_updates
        }

    # ─────────────────────────────────────
    # TRAINING
    # ─────────────────────────────────────

    def train(self,
              n_episodes: int = None,
              verbose: bool = True) -> list:
        """
        Train PPO agent.

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
        n_episodes = n_episodes or \
                     self.config['n_episodes']

        print("=" * 55)
        print("  PPO TRAINING")
        print(f"  Episodes   : {n_episodes}")
        print(f"  n_steps    : {self.n_steps}")
        print(f"  n_epochs   : {self.n_epochs}")
        print(f"  clip_range : {self.clip_range}")
        print(f"  lr         : {self.lr}")
        print("=" * 55)

        total_steps = 0

        for episode in range(n_episodes):
            state, _     = self.env.reset()
            total_reward = 0
            done         = False

            while not done:
                # Get action
                norm   = self._normalize(state)
                action, log_prob, value = (
                    self.network.get_action(
                        norm, self.device
                    )
                )

                # Step environment
                next_state, reward, terminated, \
                    truncated, _ = self.env.step(action)
                done = terminated or truncated

                # Store in buffer
                self.buffer.push(
                    norm, action, reward,
                    value, log_prob, done
                )

                state        = next_state
                total_reward += reward
                total_steps  += 1

                # Update when buffer full
                if len(self.buffer) >= self.n_steps:
                    # Bootstrap last value
                    last_norm = self._normalize(state)
                    last_t    = torch.FloatTensor(
                        last_norm
                    ).unsqueeze(0).to(self.device)

                    with torch.no_grad():
                        _, last_val = self.network(last_t)

                    self.buffer.compute_returns(
                        self.gamma,
                        self.gae_lambda,
                        last_val.item()
                    )
                    metrics = self.update()
                    self.episode_losses.append(
                        metrics['loss']
                    )

            self.episode_rewards.append(total_reward)

            if verbose and \
               (episode+1) % 200 == 0:
                mean_r = np.mean(
                    self.episode_rewards[-100:]
                )
                print(f"  Ep {episode+1:5d} | "
                      f"Rev: {mean_r:8.0f}")

        self.training_complete = True
        final = np.mean(
            self.episode_rewards[-100:]
        )
        print(f"\n✅ PPO Training Complete!")
        print(f"   Final 100-ep mean: ${final:.0f}")

        return self.episode_rewards

    # ─────────────────────────────────────
    # EVALUATION
    # ─────────────────────────────────────

    def evaluate(self,
                 n_episodes: int = 100,
                 seed: int = 42) -> dict:
        """
        Evaluate trained PPO agent.

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

        print(f"\n  PPO Evaluation:")
        print(f"  Mean Revenue: "
              f"${results['mean_revenue']:.0f}"
              f" ± ${results['std_revenue']:.0f}")
        print(f"  Mean Sold   : "
              f"{results['mean_sold']:.1f}/50")

        return results


if __name__ == "__main__":
    print("Testing PPO Agent...\n")

    env   = DynamicPricingEnv()
    agent = PPOAgent(env)

    agent.network.print_architecture()

    print("\nRunning short test (100 episodes)...")
    rewards = agent.train(
        n_episodes=100,
        verbose=True
    )

    print(f"\n✅ PPO Agent working correctly!")
    print(f"   Mean reward: ${np.mean(rewards):.0f}")