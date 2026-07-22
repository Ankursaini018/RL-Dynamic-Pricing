"""
config_manager.py
=================
Manages and saves best configurations
found during hyperparameter tuning.

Infotact DS/ML Internship — Project 2
Week 3 : Config Management
"""

import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import PPO, DQN


# ─────────────────────────────────────────
# BEST CONFIGS
# ─────────────────────────────────────────

BEST_PPO_CONFIG = {
    **PPO,
    'learning_rate' : 0.0005,
    'clip_range'    : 0.2,
    'n_epochs'      : 15,
    'ent_coef'      : 0.02,
    'n_episodes'    : 2000,
}

BEST_DQN_CONFIG = {
    **DQN,
    'lr'          : 0.001,
    'num_leaves'  : 64,
    'n_episodes'  : 2000,
}


def save_best_configs(
        save_dir: str = '../results/'):
    """
    Save all best configurations to JSON.

    Parameters
    ----------
    save_dir : str
        Directory to save configs.
    """
    os.makedirs(save_dir, exist_ok=True)

    configs = {
        'best_ppo' : BEST_PPO_CONFIG,
        'best_dqn' : BEST_DQN_CONFIG,
        'tuning_summary': {
            'ppo_configs_tested': 8,
            'method'            : 'Grid Search',
            'episodes_per_config': 500,
            'eval_episodes'     : 50,
        }
    }

    filepath = os.path.join(
        save_dir, 'best_configs.json'
    )
    with open(filepath, 'w') as f:
        json.dump(configs, f, indent=4)

    print(f"✅ Best configs saved: {filepath}")
    print(f"\n  Best PPO Config:")
    for k, v in BEST_PPO_CONFIG.items():
        if k != 'hidden_size':
            print(f"    {k:<20}: {v}")

    return configs


def load_best_configs(
        config_path: str = '../results/best_configs.json'
) -> dict:
    """
    Load best configurations from JSON.

    Parameters
    ----------
    config_path : str
        Path to config JSON.

    Returns
    -------
    dict
        Best configurations.
    """
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            configs = json.load(f)
        print(f"✅ Loaded configs: {config_path}")
        return configs
    else:
        print(f"⚠️  No saved configs found!")
        print(f"   Using defaults...")
        return {
            'best_ppo': BEST_PPO_CONFIG,
            'best_dqn': BEST_DQN_CONFIG
        }


def print_config_summary():
    """Print summary of best configs."""
    print("=" * 55)
    print("  BEST CONFIGURATIONS SUMMARY")
    print("=" * 55)

    print("\n  PPO Best Config:")
    key_ppo = [
        'learning_rate', 'clip_range',
        'n_epochs', 'ent_coef', 'gamma'
    ]
    for k in key_ppo:
        print(f"  {k:<20}: {BEST_PPO_CONFIG[k]}")

    print("\n  DQN Best Config:")
    key_dqn = [
        'lr', 'batch_size',
        'memory_size', 'target_update', 'gamma'
    ]
    for k in key_dqn:
        if k in BEST_DQN_CONFIG:
            print(f"  {k:<20}: {BEST_DQN_CONFIG[k]}")

    print("=" * 55)


if __name__ == "__main__":
    print_config_summary()
    save_best_configs()
    configs = load_best_configs()
    print("\n✅ Config manager working!")