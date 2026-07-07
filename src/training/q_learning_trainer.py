"""
q_learning_trainer.py
=====================
Complete Q-Learning training pipeline
with visualization and evaluation.

Infotact DS/ML Internship — Project 2
Week 1 : Q-Learning Training
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# --------------------------------------------------
# Add project src directory to Python path
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv
from agents.q_learning_agent import (
    QLearningAgent,
    QL_CONFIG,
    PRICE_LEVELS
)
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent
)
from utils.evaluator import SAVE_PATH, evaluate_agent

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def plot_training_curves(
        agent: QLearningAgent,
        save_path: str = '../results/ql_training.png'):
    """
    Plot Q-Learning training curves.

    Parameters
    ----------
    agent : QLearningAgent
        Trained agent.
    save_path : str
        Save path.
    """
    rewards   = agent.episode_rewards
    epsilons  = agent.episode_epsilons

    # Smooth rewards
    window = 100
    smooth = pd.Series(rewards).rolling(
        window=window
    ).mean()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Training rewards
    axes[0].plot(
        rewards,
        alpha=0.3,
        color='steelblue',
        linewidth=0.5,
        label='Episode Reward'
    )
    axes[0].plot(
        smooth,
        color='red',
        linewidth=2,
        label=f'{window}-ep Moving Avg'
    )
    axes[0].set_title(
        'Q-Learning Training Curve\n'
        'Revenue per Episode',
        fontweight='bold'
    )
    axes[0].set_xlabel('Episode')
    axes[0].set_ylabel('Total Revenue ($)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Epsilon decay
    axes[1].plot(
        epsilons,
        color='coral',
        linewidth=2
    )
    axes[1].set_title(
        'Epsilon Decay\n'
        'Exploration → Exploitation',
        fontweight='bold'
    )
    axes[1].set_xlabel('Episode')
    axes[1].set_ylabel('Epsilon (ε)')
    axes[1].axhline(
        y=agent.eps_end,
        color='red',
        linestyle='--',
        label=f'Min ε={agent.eps_end}'
    )
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(
        'Q-Learning Training Progress',
        fontsize=13,
        fontweight='bold'
    )
    plt.tight_layout()
    SAVE_PATH = os.path.join(
    RESULTS_DIR,
    "ql_training.png"
)

    plt.savefig(
    SAVE_PATH,
    bbox_inches="tight",
    dpi=150
)

    print(f"✅ Saved: {SAVE_PATH}")
    plt.show()
    print(f"✅ Saved: {save_path}")


def plot_q_table_heatmap(
        agent: QLearningAgent,
        save_path: str = '../results/q_table_policy.png'):
    """
    Visualize learned Q-table policy.

    Parameters
    ----------
    agent : QLearningAgent
        Trained agent.
    save_path : str
        Save path.
    """
    import seaborn as sns

    price_policy = agent.get_price_policy()

    # Show subset for clarity
    inv_slice  = slice(0, 51, 5)
    days_slice = slice(0, 31, 3)
    policy_sub = price_policy[
        inv_slice, days_slice
    ]

    plt.figure(figsize=(14, 8))
    sns.heatmap(
        policy_sub,
        annot=True,
        fmt='d',
        cmap='RdYlGn',
        xticklabels=range(0, 31, 3),
        yticklabels=range(0, 51, 5),
        cbar_kws={'label': 'Optimal Price ($)'}
    )
    plt.title(
        'Learned Q-Table Policy\n'
        'Optimal Price ($) by State',
        fontweight='bold',
        fontsize=13
    )
    plt.xlabel('Days Until Departure')
    plt.ylabel('Remaining Inventory')
    plt.tight_layout()
    SAVE_PATH = os.path.join(
    RESULTS_DIR,
    "q_table_policy.png"
)

    plt.savefig(
    SAVE_PATH,
    bbox_inches="tight",
    dpi=150
)

    print(f"✅ Saved: {SAVE_PATH}")
    plt.show()
    print(f"✅ Saved: {save_path}")


def run_ql_training_pipeline():
    """
    Run complete Q-Learning training.
    """
    print("=" * 55)
    print("  Q-LEARNING TRAINING PIPELINE")
    print("=" * 55)

    # Create environment
    env   = DynamicPricingEnv()
    agent = QLearningAgent(env, QL_CONFIG)

    # Train
    print("\n[1] Training Q-Learning agent...")
    rewards = agent.train(
        n_episodes=5000,
        verbose=True
    )

    # Plot training
    print("\n[2] Plotting training curves...")
    plot_training_curves(agent)

    # Evaluate
    print("\n[3] Evaluating Q-Learning agent...")
    ql_results = agent.evaluate(n_episodes=100)

    # Compare with baselines
    print("\n[4] Comparing with baselines...")
    baselines = [
        FixedPriceAgent(env),
        TimedPricingAgent(env),
        DemandBasedAgent(env)
    ]

    baseline_revenues = {}
    for b in baselines:
        df = evaluate_agent(b, n_episodes=100)
        baseline_revenues[b.name] = (
            df['total_revenue'].mean()
        )
        print(f"  {b.name}: "
              f"${df['total_revenue'].mean():.0f}")

    print(f"  Q-Learning: "
          f"${ql_results['mean_revenue']:.0f}")

    # Plot Q-table policy
    print("\n[5] Visualizing Q-table policy...")
    plot_q_table_heatmap(agent)

    # Summary
    best_baseline = max(baseline_revenues.values())
    improvement = (
        (ql_results['mean_revenue'] - best_baseline)
        / best_baseline * 100
    )

    print("\n" + "=" * 55)
    print("  Q-LEARNING RESULTS")
    print("=" * 55)
    print(f"  Best Baseline  : ${best_baseline:.0f}")
    print(f"  Q-Learning     : "
          f"${ql_results['mean_revenue']:.0f}")
    print(f"  Improvement    : {improvement:+.1f}%")
    if improvement > 0:
        print(f"  ✅ Q-Learning beats baseline!")
    else:
        print(f"  ⚠️  Need more training episodes!")
    print("=" * 55)

    return agent, ql_results


if __name__ == "__main__":
    agent, results = run_ql_training_pipeline()