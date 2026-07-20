"""
config.py
=========
Master configuration file for
RL Dynamic Pricing project.

Single source of truth for all
hyperparameters and settings.

Infotact DS/ML Internship — Project 2
"""

import os
import json


# ─────────────────────────────────────────
# PROJECT INFO
# ─────────────────────────────────────────

PROJECT_INFO = {
    'name'     : 'RL Dynamic Pricing',
    'domain'   : 'Travel & Hospitality',
    'intern'   : 'Solo Worker',
    'program'  : 'Infotact DS/ML Internship 2026',
    'github'   : 'Ankursaini018/RL-Dynamic-Pricing',
}

# ─────────────────────────────────────────
# ENVIRONMENT
# ─────────────────────────────────────────

ENV = {
    'max_inventory'    : 50,
    'max_days'         : 30,
    'price_levels'     : [50, 100, 150,
                          200, 250, 300],
    'base_demand'      : 0.7,
    'price_sensitivity': 0.6,
    'unsold_penalty'   : -10,
}

# ─────────────────────────────────────────
# Q-LEARNING
# ─────────────────────────────────────────

Q_LEARNING = {
    'learning_rate'  : 0.1,
    'discount_factor': 0.99,
    'epsilon_start'  : 1.0,
    'epsilon_end'    : 0.01,
    'epsilon_decay'  : 0.995,
    'n_episodes'     : 5000,
}

# ─────────────────────────────────────────
# DQN (Week 2)
# ─────────────────────────────────────────

DQN = {
    'lr'           : 0.001,
    'gamma'        : 0.99,
    'eps_start'    : 1.0,
    'eps_end'      : 0.01,
    'eps_decay'    : 0.995,
    'n_episodes'   : 2000,
    'batch_size'   : 64,
    'memory_size'  : 10000,
    'target_update': 10,
    'hidden_size'  : [128, 64],
}

# ─────────────────────────────────────────
# EVALUATION
# ─────────────────────────────────────────

EVAL = {
    'n_episodes'   : 100,
    'n_seasons'    : 1000,
    'seed'         : 42,
}

# ─────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
PATHS = {
    'results'  : os.path.join(
        BASE_DIR, '..', 'results'
    ),
    'models'   : os.path.join(
        BASE_DIR, '..', 'models'
    ),
    'notebooks': os.path.join(
        BASE_DIR, '..', 'notebooks'
    ),
}

# Create directories
for path in PATHS.values():
    os.makedirs(path, exist_ok=True)


# ─────────────────────────────────────────
# SAVE / LOAD CONFIG
# ─────────────────────────────────────────

def save_config(filepath: str = None):
    """Save all config to JSON."""
    if filepath is None:
        filepath = os.path.join(
            PATHS['results'],
            'project_config.json'
        )
    config = {
        'project' : PROJECT_INFO,
        'env'     : ENV,
        'q_learn' : Q_LEARNING,
        'dqn'     : DQN,
        'eval'    : EVAL,
    }
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"✅ Config saved: {filepath}")
    return config


def print_config():
    """Print all configuration."""
    print("=" * 50)
    print("  PROJECT CONFIGURATION")
    print("=" * 50)
    print(f"\n📋 Project: {PROJECT_INFO['name']}")
    print(f"\n🎮 Environment:")
    for k, v in ENV.items():
        print(f"   {k:<20}: {v}")
    print(f"\n🧠 Q-Learning:")
    for k, v in Q_LEARNING.items():
        print(f"   {k:<20}: {v}")
    print(f"\n🤖 DQN (Week 2):")
    for k, v in DQN.items():
        print(f"   {k:<20}: {v}")
    print("=" * 50)


if __name__ == "__main__":
    print_config()
    save_config()

PPO = {
    'learning_rate'     : 0.0003,
    'n_steps'           : 2048,
    'batch_size'        : 64,
    'n_epochs'          : 10,
    'gamma'             : 0.99,
    'gae_lambda'        : 0.95,
    'clip_range'        : 0.2,
    'ent_coef'          : 0.01,
    'vf_coef'           : 0.5,
    'max_grad_norm'     : 0.5,
    'n_episodes'        : 2000,
    'hidden_size'       : [128, 64],
}    