"""
ppo_utils.py
============
Utility functions for PPO agent.
Model saving, loading and monitoring.

Infotact DS/ML Internship — Project 2
Week 3 : PPO Utilities
"""

import numpy as np
import torch
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import PRICE_LEVELS


# ─────────────────────────────────────────
# MODEL SAVING
# ─────────────────────────────────────────

def save_ppo_model(
        agent,
        save_dir: str = '../../models/',
        model_name: str = 'ppo_model'):
    """
    Save PPO model weights and metadata.

    Parameters
    ----------
    agent : PPOAgent
        Trained PPO agent.
    save_dir : str
        Directory to save.
    model_name : str
        Model name.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Save weights
    model_path = os.path.join(
        save_dir, f'{model_name}.pth'
    )
    torch.save(
        agent.network.state_dict(),
        model_path
    )

    # Save metadata
    metadata = {
        'model_name'       : model_name,
        'agent_type'       : 'PPO',
        'state_size'       : agent.state_size,
        'action_size'      : agent.action_size,
        'training_episodes': len(
            agent.episode_rewards
        ),
        'mean_reward_last100': float(
            np.mean(agent.episode_rewards[-100:])
            if agent.episode_rewards else 0
        ),
        'config'           : {
            k: v for k, v in
            agent.config.items()
            if not isinstance(v, list)
        }
    }

    meta_path = os.path.join(
        save_dir, f'{model_name}_metadata.json'
    )
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ PPO Model saved!")
    print(f"   Weights  : {model_path}")
    print(f"   Metadata : {meta_path}")
    print(f"   Note: .pth gitignored!")

    return model_path, meta_path


def load_ppo_model(agent,
                   model_path: str) -> bool:
    """
    Load PPO model weights.

    Parameters
    ----------
    agent : PPOAgent
        Agent to load into.
    model_path : str
        Path to .pth file.

    Returns
    -------
    bool
        True if loaded successfully.
    """
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return False

    agent.network.load_state_dict(
        torch.load(
            model_path,
            map_location=agent.device
        )
    )
    print(f"✅ PPO Model loaded: {model_path}")
    return True


# ─────────────────────────────────────────
# PPO MONITOR
# ─────────────────────────────────────────

class PPOMonitor:
    """
    Monitors PPO training progress.

    Parameters
    ----------
    print_every : int
        Print interval.
    """

    def __init__(self, print_every: int = 200):
        self.print_every = print_every
        self.rewards     = []
        self.losses      = []
        self.best_reward = float('-inf')
        self.best_episode = 0

    def update(self,
               episode: int,
               reward: float,
               loss: float = 0):
        """Update monitor."""
        self.rewards.append(reward)
        self.losses.append(loss)

        if reward > self.best_reward:
            self.best_reward  = reward
            self.best_episode = episode

        if (episode+1) % self.print_every == 0:
            mean_r = np.mean(
                self.rewards[-self.print_every:]
            )
            print(
                f"  Ep {episode+1:5d} | "
                f"Rev: {mean_r:8.0f} | "
                f"Best: ${self.best_reward:.0f}"
                f" (ep{self.best_episode+1})"
            )

    def get_summary(self) -> dict:
        """Get training summary."""
        return {
            'total_episodes'   : len(self.rewards),
            'final_mean_100'   : float(
                np.mean(self.rewards[-100:])
                if self.rewards else 0
            ),
            'best_reward'      : float(
                self.best_reward
            ),
            'best_episode'     : self.best_episode,
        }

    def print_summary(self):
        """Print summary."""
        s = self.get_summary()
        print("\n" + "=" * 50)
        print("  PPO TRAINING SUMMARY")
        print("=" * 50)
        for k, v in s.items():
            if isinstance(v, float):
                print(f"  {k:<25}: {v:.4f}")
            else:
                print(f"  {k:<25}: {v}")
        print("=" * 50)


def print_ppo_reproduction_guide():
    """Print PPO reproduction instructions."""
    print("""
PPO REPRODUCTION GUIDE
=======================
Since .pth files are gitignored:

1. Clone repository
2. pip install -r requirements.txt
3. cd src
4. python agents/ppo/ppo_agent.py

Expected:
→ PPO beats all baselines
→ Deadline discounting learned
→ Scarcity pricing learned
""")


if __name__ == "__main__":
    print("✅ PPO utilities loaded!")
    print_ppo_reproduction_guide()