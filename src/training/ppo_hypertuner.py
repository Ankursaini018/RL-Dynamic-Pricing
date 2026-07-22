"""
ppo_hypertuner.py
=================
Hyperparameter tuning for PPO agent.
Tests different configurations to find
optimal settings for dynamic pricing.

Infotact DS/ML Internship — Project 2
Week 3 : PPO Hyperparameter Tuning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import DynamicPricingEnv
from agents.ppo.ppo_agent import PPOAgent
from config import PPO

os.makedirs('../results', exist_ok=True)


# ─────────────────────────────────────────
# PPO PARAMETER GRID
# ─────────────────────────────────────────

PPO_PARAM_GRID = [
    # Config 1: Default
    {
        'label'         : 'Default',
        'learning_rate' : 0.0003,
        'clip_range'    : 0.2,
        'n_epochs'      : 10,
        'ent_coef'      : 0.01,
    },
    # Config 2: Higher LR
    {
        'label'         : 'High LR',
        'learning_rate' : 0.001,
        'clip_range'    : 0.2,
        'n_epochs'      : 10,
        'ent_coef'      : 0.01,
    },
    # Config 3: Lower LR
    {
        'label'         : 'Low LR',
        'learning_rate' : 0.0001,
        'clip_range'    : 0.2,
        'n_epochs'      : 10,
        'ent_coef'      : 0.01,
    },
    # Config 4: Wide clip
    {
        'label'         : 'Wide Clip',
        'learning_rate' : 0.0003,
        'clip_range'    : 0.3,
        'n_epochs'      : 10,
        'ent_coef'      : 0.01,
    },
    # Config 5: Narrow clip
    {
        'label'         : 'Narrow Clip',
        'learning_rate' : 0.0003,
        'clip_range'    : 0.1,
        'n_epochs'      : 10,
        'ent_coef'      : 0.01,
    },
    # Config 6: More epochs
    {
        'label'         : 'More Epochs',
        'learning_rate' : 0.0003,
        'clip_range'    : 0.2,
        'n_epochs'      : 20,
        'ent_coef'      : 0.01,
    },
    # Config 7: High entropy
    {
        'label'         : 'High Entropy',
        'learning_rate' : 0.0003,
        'clip_range'    : 0.2,
        'n_epochs'      : 10,
        'ent_coef'      : 0.05,
    },
    # Config 8: Best guess
    {
        'label'         : 'Best Guess',
        'learning_rate' : 0.0005,
        'clip_range'    : 0.2,
        'n_epochs'      : 15,
        'ent_coef'      : 0.02,
    },
]


# ─────────────────────────────────────────
# EVALUATE SINGLE CONFIG
# ─────────────────────────────────────────

def evaluate_ppo_config(
        config: dict,
        env: DynamicPricingEnv,
        n_train: int = 500,
        n_eval: int = 50) -> float:
    """
    Train and evaluate a PPO config.

    Parameters
    ----------
    config : dict
        PPO configuration.
    env : DynamicPricingEnv
        Environment.
    n_train : int
        Training episodes.
    n_eval : int
        Evaluation episodes.

    Returns
    -------
    float
        Mean evaluation revenue.
    """
    full_config = {**PPO, **config}

    agent = PPOAgent(env, full_config)
    agent.train(n_episodes=n_train, verbose=False)
    eval_result = agent.evaluate(n_eval)

    return eval_result['mean_revenue'], agent


# ─────────────────────────────────────────
# GRID SEARCH
# ─────────────────────────────────────────

def run_ppo_grid_search(
        env: DynamicPricingEnv,
        n_train: int = 500,
        n_eval: int = 50) -> tuple:
    """
    Run grid search over PPO configurations.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment.
    n_train : int
        Training episodes per config.
    n_eval : int
        Evaluation episodes.

    Returns
    -------
    tuple
        Best config and results DataFrame.
    """
    print("=" * 55)
    print("  PPO HYPERPARAMETER GRID SEARCH")
    print(f"  {len(PPO_PARAM_GRID)} configs × "
          f"{n_train} train eps")
    print("=" * 55)

    results    = []
    best_rev   = 0
    best_config = None
    best_agent  = None

    for i, config in enumerate(PPO_PARAM_GRID, 1):
        label = config['label']
        print(f"\n  Config {i}/{len(PPO_PARAM_GRID)}"
              f": {label}")
        print(f"  lr={config['learning_rate']}, "
              f"clip={config['clip_range']}, "
              f"epochs={config['n_epochs']}")

        revenue, agent = evaluate_ppo_config(
            config, env, n_train, n_eval
        )

        results.append({
            'Config'        : label,
            'LR'            : config['learning_rate'],
            'Clip Range'    : config['clip_range'],
            'N Epochs'      : config['n_epochs'],
            'Entropy Coef'  : config['ent_coef'],
            'Mean Revenue'  : revenue
        })

        print(f"  Revenue: ${revenue:.0f}", end="")
        if revenue > best_rev:
            best_rev    = revenue
            best_config = config
            best_agent  = agent
            print(" ← BEST! 🏆")
        else:
            print()

    results_df = pd.DataFrame(results).sort_values(
        'Mean Revenue', ascending=False
    )

    print("\n" + "=" * 55)
    print("  GRID SEARCH RESULTS")
    print("=" * 55)
    print(results_df[[
        'Config', 'LR', 'Clip Range',
        'N Epochs', 'Mean Revenue'
    ]].to_string(index=False))

    print(f"\n  🏆 BEST CONFIG: {best_config['label']}")
    print(f"     Revenue: ${best_rev:.0f}")
    print(f"     LR     : {best_config['learning_rate']}")
    print(f"     Clip   : {best_config['clip_range']}")
    print(f"     Epochs : {best_config['n_epochs']}")

    return best_config, results_df, best_agent


# ─────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────

def plot_tuning_results(
        results_df: pd.DataFrame,
        save_path: str = '../results/ppo_tuning.png'):
    """
    Plot hyperparameter tuning results.

    Parameters
    ----------
    results_df : pd.DataFrame
        Tuning results.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # ── Plot 1: Revenue by Config ──
    colors = [
        'gold' if i == 0 else 'steelblue'
        for i in range(len(results_df))
    ]
    bars = axes[0, 0].bar(
        results_df['Config'],
        results_df['Mean Revenue'],
        color=colors,
        edgecolor='black'
    )
    axes[0, 0].set_title(
        'Revenue by Configuration\n(Gold = Best)',
        fontweight='bold'
    )
    axes[0, 0].set_ylabel('Mean Revenue ($)')
    axes[0, 0].set_xticklabels(
        results_df['Config'],
        rotation=20, fontsize=8
    )
    for bar, val in zip(
        bars, results_df['Mean Revenue']
    ):
        axes[0, 0].text(
            bar.get_x() + bar.get_width()/2,
            val + 10,
            f'${val:.0f}',
            ha='center', fontsize=8,
            fontweight='bold'
        )

    # ── Plot 2: LR Impact ──
    axes[0, 1].scatter(
        results_df['LR'],
        results_df['Mean Revenue'],
        color='steelblue', s=100,
        edgecolors='black'
    )
    for _, row in results_df.iterrows():
        axes[0, 1].annotate(
            row['Config'],
            (row['LR'], row['Mean Revenue']),
            textcoords='offset points',
            xytext=(5, 5),
            fontsize=7
        )
    axes[0, 1].set_title(
        'Revenue vs Learning Rate',
        fontweight='bold'
    )
    axes[0, 1].set_xlabel('Learning Rate')
    axes[0, 1].set_ylabel('Mean Revenue ($)')
    axes[0, 1].grid(True, alpha=0.3)

    # ── Plot 3: Clip Range Impact ──
    axes[1, 0].scatter(
        results_df['Clip Range'],
        results_df['Mean Revenue'],
        color='coral', s=100,
        edgecolors='black'
    )
    for _, row in results_df.iterrows():
        axes[1, 0].annotate(
            row['Config'],
            (row['Clip Range'],
             row['Mean Revenue']),
            textcoords='offset points',
            xytext=(5, 5),
            fontsize=7
        )
    axes[1, 0].set_title(
        'Revenue vs Clip Range',
        fontweight='bold'
    )
    axes[1, 0].set_xlabel('Clip Range (ε)')
    axes[1, 0].set_ylabel('Mean Revenue ($)')
    axes[1, 0].grid(True, alpha=0.3)

    # ── Plot 4: Epochs Impact ──
    axes[1, 1].scatter(
        results_df['N Epochs'],
        results_df['Mean Revenue'],
        color='green', s=100,
        edgecolors='black'
    )
    for _, row in results_df.iterrows():
        axes[1, 1].annotate(
            row['Config'],
            (row['N Epochs'],
             row['Mean Revenue']),
            textcoords='offset points',
            xytext=(5, 5),
            fontsize=7
        )
    axes[1, 1].set_title(
        'Revenue vs N Epochs',
        fontweight='bold'
    )
    axes[1, 1].set_xlabel('Number of Epochs')
    axes[1, 1].set_ylabel('Mean Revenue ($)')
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle(
        'PPO Hyperparameter Tuning Results',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


if __name__ == "__main__":
    env = DynamicPricingEnv()
    best, results_df, agent = (
        run_ppo_grid_search(env)
    )
    plot_tuning_results(results_df)
    print(f"\n✅ Best PPO config: {best}")