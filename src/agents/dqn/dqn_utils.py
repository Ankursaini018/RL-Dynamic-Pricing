"""
dqn_utils.py
============
Utility functions for DQN agent.
Model saving, loading and monitoring.

Infotact DS/ML Internship — Project 2
Week 2 : DQN Utilities
"""

import numpy as np
import torch
import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import PRICE_LEVELS


# ─────────────────────────────────────────
# MODEL SAVING
# ─────────────────────────────────────────

def save_dqn_model(agent,
                   save_dir: str = '../../models/',
                   model_name: str = 'dqn_model'):
    """
    Save DQN model weights and config.

    Parameters
    ----------
    agent : DQNAgent
        Trained DQN agent.
    save_dir : str
        Directory to save model.
    model_name : str
        Model file name.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Save model weights
    model_path = os.path.join(
        save_dir, f'{model_name}.pth'
    )
    torch.save(
        agent.online_net.state_dict(),
        model_path
    )

    # Save config and metadata
    metadata = {
        'model_name'      : model_name,
        'state_size'      : agent.state_size,
        'action_size'     : agent.action_size,
        'hidden_sizes'    : agent.config['hidden_size'],
        'training_episodes': len(
            agent.episode_rewards
        ),
        'final_epsilon'   : float(agent.epsilon),
        'mean_reward_last100': float(
            np.mean(agent.episode_rewards[-100:])
            if agent.episode_rewards else 0
        ),
        'buffer_size'     : len(agent.buffer),
        'config'          : agent.config
    }

    meta_path = os.path.join(
        save_dir, f'{model_name}_metadata.json'
    )
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Model saved!")
    print(f"   Weights  : {model_path}")
    print(f"   Metadata : {meta_path}")
    print(f"   Note: .pth files are gitignored")

    return model_path, meta_path


def load_dqn_model(agent,
                   model_path: str):
    """
    Load DQN model weights.

    Parameters
    ----------
    agent : DQNAgent
        DQN agent to load weights into.
    model_path : str
        Path to .pth file.
    """
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return False

    agent.online_net.load_state_dict(
        torch.load(model_path,
                   map_location=agent.device)
    )
    agent.target_net.load_state_dict(
        agent.online_net.state_dict()
    )
    print(f"✅ Model loaded: {model_path}")
    return True


# ─────────────────────────────────────────
# TRAINING MONITOR
# ─────────────────────────────────────────

class TrainingMonitor:
    """
    Monitors DQN training progress.

    Tracks metrics and prints
    formatted progress updates.

    Parameters
    ----------
    print_every : int
        Print interval (episodes).
    """

    def __init__(self, print_every: int = 100):
        self.print_every  = print_every
        self.rewards      = []
        self.losses       = []
        self.epsilons     = []
        self.best_reward  = float('-inf')
        self.best_episode = 0

    def update(self,
               episode: int,
               reward: float,
               loss: float,
               epsilon: float):
        """
        Update monitor with new episode data.

        Parameters
        ----------
        episode : int
            Current episode.
        reward : float
            Episode reward.
        loss : float
            Episode loss.
        epsilon : float
            Current epsilon.
        """
        self.rewards.append(reward)
        self.losses.append(loss)
        self.epsilons.append(epsilon)

        if reward > self.best_reward:
            self.best_reward  = reward
            self.best_episode = episode

        if (episode + 1) % self.print_every == 0:
            mean_r = np.mean(
                self.rewards[-self.print_every:]
            )
            mean_l = np.mean(
                self.losses[-self.print_every:]
            )
            print(
                f"  Ep {episode+1:5d} | "
                f"Rev: {mean_r:8.0f} | "
                f"Loss: {mean_l:.4f} | "
                f"ε: {epsilon:.3f} | "
                f"Best: ${self.best_reward:.0f}"
                f" (ep{self.best_episode+1})"
            )

    def get_summary(self) -> dict:
        """Get training summary."""
        return {
            'total_episodes'  : len(self.rewards),
            'final_mean_100'  : float(
                np.mean(self.rewards[-100:])
                if self.rewards else 0
            ),
            'best_reward'     : float(
                self.best_reward
            ),
            'best_episode'    : self.best_episode,
            'final_epsilon'   : float(
                self.epsilons[-1]
                if self.epsilons else 1.0
            )
        }

    def print_summary(self):
        """Print training summary."""
        summary = self.get_summary()
        print("\n" + "=" * 50)
        print("  TRAINING SUMMARY")
        print("=" * 50)
        for k, v in summary.items():
            if isinstance(v, float):
                print(f"  {k:<25}: {v:.4f}")
            else:
                print(f"  {k:<25}: {v}")
        print("=" * 50)


# ─────────────────────────────────────────
# REPRODUCTION GUIDE
# ─────────────────────────────────────────

def print_reproduction_guide():
    """Print model reproduction instructions."""
    print("""
MODEL REPRODUCTION GUIDE
=========================
Since .pth files are gitignored,
here's how to reproduce the model:

1. Clone repository:
   git clone https://github.com/Ankursaini018/
   RL-Dynamic-Pricing.git

2. Install dependencies:
   pip install -r requirements.txt

3. Train DQN:
   cd src
   python agents/dqn/dqn_agent.py

4. Or run full pipeline:
   python training/dqn_trainer.py

5. Expected results:
   → DQN beats all baselines
   → Revenue improves over time
   → Deadline discounting learned
""")


if __name__ == "__main__":
    print("✅ DQN utilities loaded!")
    print_reproduction_guide()