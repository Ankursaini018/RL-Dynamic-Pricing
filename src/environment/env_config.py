"""
env_config.py
=============
Environment configuration constants
for Dynamic Pricing project.

Centralizes all environment parameters
for easy modification and experimentation.

Infotact DS/ML Internship — Project 2
Week 1 : Configuration Management
"""

# ─────────────────────────────────────────
# ENVIRONMENT DEFAULTS
# ─────────────────────────────────────────

ENV_CONFIG = {
    # Inventory settings
    'max_inventory'    : 50,
    'max_days'         : 30,

    # Price levels (in dollars)
    'price_levels'     : [50, 100, 150,
                          200, 250, 300],

    # Demand function parameters
    'base_demand_prob' : 0.7,
    'price_sensitivity': 0.6,
    'time_sensitivity' : 0.3,
    'noise_std'        : 0.05,

    # Reward parameters
    'unsold_penalty'   : -10,
}

# ─────────────────────────────────────────
# AGENT CONFIGS
# ─────────────────────────────────────────

Q_LEARNING_CONFIG = {
    'learning_rate'    : 0.1,
    'discount_factor'  : 0.99,
    'epsilon_start'    : 1.0,
    'epsilon_end'      : 0.01,
    'epsilon_decay'    : 0.995,
    'n_episodes'       : 5000,
}

DQN_CONFIG = {
    'learning_rate'    : 0.001,
    'discount_factor'  : 0.99,
    'epsilon_start'    : 1.0,
    'epsilon_end'      : 0.01,
    'epsilon_decay'    : 0.995,
    'n_episodes'       : 2000,
    'batch_size'       : 64,
    'memory_size'      : 10000,
    'target_update'    : 10,
    'hidden_layers'    : [128, 64],
}

# ─────────────────────────────────────────
# EVALUATION CONFIG
# ─────────────────────────────────────────

EVAL_CONFIG = {
    'n_eval_episodes'  : 100,
    'n_sim_seasons'    : 1000,
    'seed'             : 42,
}

# ─────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────

PATHS = {
    'results'  : '../results/',
    'models'   : '../models/',
    'notebooks': '../notebooks/',
}


if __name__ == "__main__":
    print("=" * 50)
    print("  PROJECT CONFIGURATION")
    print("=" * 50)
    print(f"\nEnvironment Config:")
    for k, v in ENV_CONFIG.items():
        print(f"  {k:<25}: {v}")
    print(f"\nQ-Learning Config:")
    for k, v in Q_LEARNING_CONFIG.items():
        print(f"  {k:<25}: {v}")
    print(f"\nDQN Config:")
    for k, v in DQN_CONFIG.items():
        print(f"  {k:<25}: {v}")
    print("\n✅ Configuration loaded!")