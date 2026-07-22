"""
combined_tuner.py
=================
Compares best tuned PPO vs best tuned DQN
to find overall best agent.

Infotact DS/ML Internship — Project 2
Week 3 : Combined Tuning
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
from agents.dqn.dqn_agent import DQNAgent
from agents.baseline_agents import (
    TimedPricingAgent,
    DemandBasedAgent
)
from utils.evaluator import evaluate_agent
from config import PPO, DQN

os.makedirs('../results', exist_ok=True)


def find_best_combined(
        env: DynamicPricingEnv,
        n_train: int = 1000,
        n_eval: int = 100) -> dict:
    """
    Train both PPO and DQN with best configs
    and find overall winner.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment.
    n_train : int
        Training episodes.
    n_eval : int
        Evaluation episodes.

    Returns
    -------
    dict
        Best agent results.
    """
    print("=" * 55)
    print("  BEST PPO vs BEST DQN")
    print("=" * 55)

    # Best PPO config (from grid search)
    best_ppo_config = {
        **PPO,
        'learning_rate' : 0.0005,
        'clip_range'    : 0.2,
        'n_epochs'      : 15,
        'ent_coef'      : 0.02,
    }

    # Best DQN config (from Week 2)
    best_dqn_config = {
        **DQN,
        'lr'           : 0.001,
        'n_episodes'   : n_train,
    }

    # Train PPO
    print(f"\n[1] Training Best PPO "
          f"({n_train} eps)...")
    ppo = PPOAgent(env, best_ppo_config)
    ppo.train(n_episodes=n_train, verbose=False)
    ppo_eval = ppo.evaluate(n_eval)
    print(f"    PPO: ${ppo_eval['mean_revenue']:.0f}")

    # Train DQN
    print(f"\n[2] Training Best DQN "
          f"({n_train} eps)...")
    dqn = DQNAgent(env, best_dqn_config)
    dqn.train(n_episodes=n_train, verbose=False)
    dqn_eval = dqn.evaluate(n_eval)
    print(f"    DQN: ${dqn_eval['mean_revenue']:.0f}")

    # Best baselines
    print("\n[3] Evaluating Best Baseline...")
    best_bl = max(
        evaluate_agent(
            TimedPricingAgent(env), n_eval
        )['total_revenue'].mean(),
        evaluate_agent(
            DemandBasedAgent(env), n_eval
        )['total_revenue'].mean()
    )
    print(f"    Best Baseline: ${best_bl:.0f}")

    # Summary
    results = {
        'Best Baseline' : best_bl,
        'DQN'           : dqn_eval['mean_revenue'],
        'PPO 🏆'        : ppo_eval['mean_revenue'],
    }

    winner = max(results, key=results.get)

    print("\n" + "=" * 55)
    print("  FINAL COMPARISON")
    print("=" * 55)
    for name, rev in sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        tag = " ← WINNER! 🏆" if name == winner else ""
        print(f"  {name:<15}: ${rev:.0f}{tag}")

    # Save best config
    best_config = {
        'winner'          : winner,
        'ppo_revenue'     : float(
            ppo_eval['mean_revenue']
        ),
        'dqn_revenue'     : float(
            dqn_eval['mean_revenue']
        ),
        'baseline_revenue': float(best_bl),
        'ppo_vs_dqn_pct'  : float(
            (ppo_eval['mean_revenue'] -
             dqn_eval['mean_revenue']) /
            dqn_eval['mean_revenue'] * 100
        ),
        'ppo_vs_bl_pct'   : float(
            (ppo_eval['mean_revenue'] -
             best_bl) / best_bl * 100
        ),
        'best_ppo_config' : best_ppo_config,
        'best_dqn_config' : {
            k: v for k, v in
            best_dqn_config.items()
            if k != 'hidden_size'
        }
    }

    with open(
        '../results/best_combined_config.json',
        'w'
    ) as f:
        json.dump(best_config, f, indent=4)
    print("\n✅ Best config saved!")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    names    = list(results.keys())
    revenues = list(results.values())
    colors   = [
        'gold' if 'PPO' in n
        else 'coral' if 'DQN' in n
        else 'steelblue'
        for n in names
    ]
    bars = ax.bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        width=0.5
    )
    ax.set_title(
        'Best PPO vs Best DQN vs Best Baseline\n'
        'Final Comparison',
        fontweight='bold', fontsize=13
    )
    ax.set_ylabel('Mean Revenue ($)')
    for bar, val in zip(bars, revenues):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            val + 10,
            f'${val:.0f}',
            ha='center',
            fontweight='bold', fontsize=11
        )

    ppo_imp = best_config['ppo_vs_bl_pct']
    ax.set_title(
        f'Best PPO vs Best DQN vs Best Baseline\n'
        f'PPO improves baseline by +{ppo_imp:.1f}%',
        fontweight='bold', fontsize=13
    )

    plt.tight_layout()
    plt.savefig(
        '../results/best_combined.png',
        bbox_inches='tight', dpi=150
    )
    plt.show()
    print("✅ Comparison chart saved!")

    return best_config, ppo, dqn


if __name__ == "__main__":
    env = DynamicPricingEnv()
    best, ppo, dqn = find_best_combined(env)
    print(f"\n🏆 Winner: {best['winner']}")