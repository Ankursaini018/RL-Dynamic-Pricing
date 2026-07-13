"""
dqn_trainer.py
==============
Complete DQN training pipeline with
visualization and evaluation.

Infotact DS/ML Internship — Project 2
Week 2 : DQN Training
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv
from agents.dqn.dqn_agent import DQNAgent
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent
)
from agents.q_learning_agent import (
    QLearningAgent,
    QL_CONFIG
)
from utils.evaluator import evaluate_agent
from config import DQN, Q_LEARNING

os.makedirs('../results', exist_ok=True)


# ─────────────────────────────────────────
# TRAINING CURVES
# ─────────────────────────────────────────

def plot_dqn_training(
        agent: DQNAgent,
        save_path: str = '../results/dqn_training.png'):
    """
    Plot DQN training curves.

    Parameters
    ----------
    agent : DQNAgent
        Trained DQN agent.
    save_path : str
        Save path.
    """
    rewards   = agent.episode_rewards
    losses    = agent.episode_losses
    epsilons  = agent.episode_epsilons

    window = 100
    smooth_rewards = pd.Series(rewards).rolling(
        window=window
    ).mean()
    smooth_losses  = pd.Series(losses).rolling(
        window=window
    ).mean()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Revenue curve
    axes[0].plot(
        rewards, alpha=0.2,
        color='steelblue', linewidth=0.5
    )
    axes[0].plot(
        smooth_rewards, color='red',
        linewidth=2.5,
        label=f'{window}-ep Average'
    )
    axes[0].set_title(
        'DQN Training Revenue',
        fontweight='bold'
    )
    axes[0].set_xlabel('Episode')
    axes[0].set_ylabel('Revenue ($)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Loss curve
    axes[1].plot(
        losses, alpha=0.2,
        color='coral', linewidth=0.5
    )
    axes[1].plot(
        smooth_losses, color='darkred',
        linewidth=2.5,
        label=f'{window}-ep Average'
    )
    axes[1].set_title(
        'DQN Training Loss',
        fontweight='bold'
    )
    axes[1].set_xlabel('Episode')
    axes[1].set_ylabel('MSE Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Epsilon decay
    axes[2].plot(
        epsilons, color='green',
        linewidth=2
    )
    axes[2].set_title(
        'Epsilon Decay\nExploration → Exploitation',
        fontweight='bold'
    )
    axes[2].set_xlabel('Episode')
    axes[2].set_ylabel('Epsilon (ε)')
    axes[2].axhline(
        y=agent.eps_end,
        color='red', linestyle='--',
        label=f'Min ε={agent.eps_end}'
    )
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.suptitle(
        'DQN Training Progress',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


# ─────────────────────────────────────────
# DQN vs Q-LEARNING COMPARISON
# ─────────────────────────────────────────

def compare_dqn_vs_qlearning(
        env: DynamicPricingEnv,
        n_eval: int = 100,
        save_path: str = '../results/dqn_vs_ql.png'):
    """
    Train and compare DQN vs Q-Learning.

    Parameters
    ----------
    env : DynamicPricingEnv
        Pricing environment.
    n_eval : int
        Evaluation episodes.
    save_path : str
        Save path.

    Returns
    -------
    dict
        Comparison results.
    """
    print("=" * 55)
    print("  DQN vs Q-LEARNING COMPARISON")
    print("=" * 55)

    # Train Q-Learning
    print("\n[1] Training Q-Learning (3000 eps)...")
    ql_agent = QLearningAgent(env, QL_CONFIG)
    ql_agent.train(n_episodes=3000, verbose=False)
    ql_eval  = ql_agent.evaluate(n_episodes=n_eval)
    print(f"    Q-Learning Revenue: "
          f"${ql_eval['mean_revenue']:.0f}")

    # Train DQN
    print("\n[2] Training DQN (2000 eps)...")
    dqn_agent = DQNAgent(env, DQN)
    dqn_agent.train(n_episodes=2000, verbose=True)
    dqn_eval  = dqn_agent.evaluate(n_episodes=n_eval)
    print(f"    DQN Revenue: "
          f"${dqn_eval['mean_revenue']:.0f}")

    # Evaluate baselines
    print("\n[3] Evaluating baselines...")
    baselines = {
        'Fixed Price' : FixedPriceAgent(env),
        'Time Based'  : TimedPricingAgent(env),
        'Demand Based': DemandBasedAgent(env),
    }
    baseline_revs = {}
    for name, agent in baselines.items():
        df = evaluate_agent(agent, n_eval)
        baseline_revs[name] = (
            df['total_revenue'].mean()
        )
        print(f"    {name}: "
              f"${baseline_revs[name]:.0f}")

    # All results
    all_results = {
        **baseline_revs,
        'Q-Learning' : ql_eval['mean_revenue'],
        'DQN 🤖'     : dqn_eval['mean_revenue'],
    }

    # Plot comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Bar chart
    names    = list(all_results.keys())
    revenues = list(all_results.values())
    colors   = [
        'gold'      if 'DQN' in n
        else 'coral' if 'Q-Learning' in n
        else 'steelblue'
        for n in names
    ]

    bars = axes[0].bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        width=0.6
    )
    axes[0].set_title(
        'Revenue Comparison\nAll Agents',
        fontweight='bold'
    )
    axes[0].set_ylabel('Mean Revenue ($)')
    axes[0].set_xticklabels(
        names, rotation=15, fontsize=9
    )
    for bar, val in zip(bars, revenues):
        axes[0].text(
            bar.get_x() + bar.get_width()/2,
            val + 20,
            f'${val:.0f}',
            ha='center', fontsize=9,
            fontweight='bold'
        )

    # Training curves
    ql_smooth = pd.Series(
        ql_agent.episode_rewards
    ).rolling(window=50).mean()
    dqn_smooth = pd.Series(
        dqn_agent.episode_rewards
    ).rolling(window=50).mean()

    axes[1].plot(
        ql_smooth,
        color='coral', linewidth=2,
        label='Q-Learning'
    )
    axes[1].plot(
        dqn_smooth,
        color='gold', linewidth=2,
        label='DQN'
    )
    axes[1].set_title(
        'Training Curves\nQ-Learning vs DQN',
        fontweight='bold'
    )
    axes[1].set_xlabel('Episode')
    axes[1].set_ylabel('Revenue ($)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(
        'DQN vs Q-Learning vs Baselines',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")

    return all_results, dqn_agent, ql_agent


# ─────────────────────────────────────────
# FULL TRAINING PIPELINE
# ─────────────────────────────────────────

def run_dqn_training_pipeline():
    """
    Run complete DQN training pipeline.
    """
    print("=" * 55)
    print("  DQN TRAINING PIPELINE")
    print("=" * 55)

    env   = DynamicPricingEnv()
    agent = DQNAgent(env, DQN)

    # Train
    print("\n[1] Training DQN...")
    rewards = agent.train(
        n_episodes=2000,
        verbose=True
    )

    # Plot training
    print("\n[2] Plotting training curves...")
    plot_dqn_training(agent)

    # Evaluate
    print("\n[3] Evaluating DQN...")
    results = agent.evaluate(n_episodes=100)

    # Summary
    best_baseline = 4200  # Update with actual
    improvement   = (
        (results['mean_revenue'] - best_baseline)
        / best_baseline * 100
    )

    print("\n" + "=" * 55)
    print("  DQN TRAINING RESULTS")
    print("=" * 55)
    print(f"  Mean Revenue : "
          f"${results['mean_revenue']:.0f}"
          f" ± ${results['std_revenue']:.0f}")
    print(f"  Max Revenue  : "
          f"${results['max_revenue']:.0f}")
    print(f"  Mean Sold    : "
          f"{results['mean_sold']:.1f}/50")
    print(f"  vs Baseline  : {improvement:+.1f}%")
    if results['mean_revenue'] > best_baseline:
        print(f"  ✅ DQN beats baseline!")
    else:
        print(f"  ⚠️  Need more training!")
    print("=" * 55)

    return agent, results


if __name__ == "__main__":
    agent, results = run_dqn_training_pipeline()