"""
ppo_trainer.py
==============
Complete PPO training pipeline
with visualization and evaluation.

Infotact DS/ML Internship — Project 2
Week 3 : PPO Training
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]   # src
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import DynamicPricingEnv
from agents.ppo.ppo_agent import PPOAgent
from agents.dqn.dqn_agent import DQNAgent
from agents.q_learning_agent import (
    QLearningAgent,
    QL_CONFIG
)
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)
from utils.evaluator import evaluate_agent
from config import PPO, DQN

os.makedirs('../results', exist_ok=True)


# ─────────────────────────────────────────
# TRAINING CURVES
# ─────────────────────────────────────────

def plot_ppo_training(
        agent: PPOAgent,
        save_path: str = '../results/ppo_training.png'):
    """
    Plot PPO training curves.

    Parameters
    ----------
    agent : PPOAgent
        Trained PPO agent.
    save_path : str
        Save path.
    """
    rewards = agent.episode_rewards
    window  = 100
    smooth  = pd.Series(rewards).rolling(
        window=window
    ).mean()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Revenue curve
    axes[0].plot(
        rewards, alpha=0.2,
        color='steelblue', linewidth=0.5
    )
    axes[0].plot(
        smooth, color='red',
        linewidth=2.5,
        label=f'{window}-ep Average'
    )
    axes[0].set_title(
        'PPO Training Revenue',
        fontweight='bold'
    )
    axes[0].set_xlabel('Episode')
    axes[0].set_ylabel('Revenue ($)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Loss curve
    if agent.episode_losses:
        losses = agent.episode_losses
        smooth_loss = pd.Series(losses).rolling(
            window=50
        ).mean()
        axes[1].plot(
            losses, alpha=0.2,
            color='coral', linewidth=0.5
        )
        axes[1].plot(
            smooth_loss, color='darkred',
            linewidth=2.5,
            label='50-ep Average'
        )
        axes[1].set_title(
            'PPO Training Loss',
            fontweight='bold'
        )
        axes[1].set_xlabel('Update Step')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

    plt.suptitle(
        'PPO Training Progress',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


# ─────────────────────────────────────────
# ALL AGENTS COMPARISON
# ─────────────────────────────────────────

def compare_all_agents(
        env: DynamicPricingEnv,
        ppo_agent: PPOAgent,
        dqn_agent: DQNAgent,
        ql_agent: QLearningAgent,
        n_eval: int = 100,
        save_path: str = '../results/all_agents_comparison.png'
) -> dict:
    """
    Compare ALL agents including PPO.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment.
    ppo_agent : PPOAgent
        Trained PPO agent.
    dqn_agent : DQNAgent
        Trained DQN agent.
    ql_agent : QLearningAgent
        Trained Q-Learning agent.
    n_eval : int
        Evaluation episodes.
    save_path : str
        Save path.

    Returns
    -------
    dict
        All agent results.
    """
    print("=" * 55)
    print("  ALL AGENTS COMPARISON")
    print("=" * 55)

    # Evaluate baselines
    baselines = {
        'Fixed Price'  : FixedPriceAgent(env),
        'Time Based'   : TimedPricingAgent(env),
        'Demand Based' : DemandBasedAgent(env),
        'Linear Decay' : LinearDecayAgent(env),
    }

    all_results = {}

    print("\n  Baselines:")
    for name, agent in baselines.items():
        df = evaluate_agent(agent, n_eval)
        all_results[name] = (
            df['total_revenue'].mean()
        )
        print(f"  {name:<15}: "
              f"${all_results[name]:.0f}")

    # Q-Learning
    print("\n  RL Agents:")
    ql_eval = ql_agent.evaluate(n_eval)
    all_results['Q-Learning'] = (
        ql_eval['mean_revenue']
    )
    print(f"  {'Q-Learning':<15}: "
          f"${all_results['Q-Learning']:.0f}")

    # DQN
    dqn_eval = dqn_agent.evaluate(n_eval)
    all_results['DQN'] = dqn_eval['mean_revenue']
    print(f"  {'DQN':<15}: "
          f"${all_results['DQN']:.0f}")

    # PPO
    ppo_eval = ppo_agent.evaluate(n_eval)
    all_results['PPO 🏆'] = ppo_eval['mean_revenue']
    print(f"  {'PPO 🏆':<15}: "
          f"${all_results['PPO 🏆']:.0f}")

    # Rankings
    ranked = sorted(
        all_results.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\n" + "=" * 55)
    print("  RANKINGS")
    print("=" * 55)
    medals = ['🥇', '🥈', '🥉',
              '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    for i, (name, rev) in enumerate(ranked):
        print(f"  {medals[i]} {name:<15}: ${rev:.0f}")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    names    = [n for n, _ in ranked]
    revenues = [r for _, r in ranked]
    colors   = [
        'gold'      if 'PPO' in n
        else 'coral' if 'DQN' in n
        else 'green' if 'Q-Learning' in n
        else 'steelblue'
        for n in names
    ]

    # Bar chart
    bars = axes[0].bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        width=0.6
    )
    axes[0].set_title(
        'All Agents Revenue Comparison',
        fontweight='bold', fontsize=12
    )
    axes[0].set_ylabel('Mean Revenue ($)')
    axes[0].set_xticklabels(
        names, rotation=20, fontsize=9
    )
    for bar, val in zip(bars, revenues):
        axes[0].text(
            bar.get_x() + bar.get_width()/2,
            val + 20,
            f'${val:.0f}',
            ha='center', fontsize=9,
            fontweight='bold'
        )

    # Training curves comparison
    ppo_smooth = pd.Series(
        ppo_agent.episode_rewards
    ).rolling(window=50).mean()
    dqn_smooth = pd.Series(
        dqn_agent.episode_rewards
    ).rolling(window=50).mean()
    ql_smooth  = pd.Series(
        ql_agent.episode_rewards
    ).rolling(window=50).mean()

    axes[1].plot(
        ql_smooth,
        color='green', linewidth=2,
        label='Q-Learning', alpha=0.8
    )
    axes[1].plot(
        dqn_smooth,
        color='coral', linewidth=2,
        label='DQN', alpha=0.8
    )
    axes[1].plot(
        ppo_smooth,
        color='gold', linewidth=2.5,
        label='PPO'
    )
    axes[1].set_title(
        'Training Curves Comparison',
        fontweight='bold', fontsize=12
    )
    axes[1].set_xlabel('Episode')
    axes[1].set_ylabel('Revenue ($)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(
        'PPO vs DQN vs Q-Learning vs Baselines',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")

    return all_results, ranked


# ─────────────────────────────────────────
# FULL PIPELINE
# ─────────────────────────────────────────

def run_ppo_pipeline():
    """Run complete PPO training pipeline."""
    print("=" * 55)
    print("  PPO TRAINING PIPELINE")
    print("=" * 55)

    env = DynamicPricingEnv()

    # Train PPO
    print("\n[1] Training PPO (2000 eps)...")
    ppo = PPOAgent(env, PPO)
    ppo.train(n_episodes=2000, verbose=True)

    # Plot training
    print("\n[2] Plotting training curves...")
    plot_ppo_training(ppo)

    # Evaluate
    print("\n[3] Evaluating PPO...")
    results = ppo.evaluate(n_episodes=100)

    print("\n" + "=" * 55)
    print("  PPO RESULTS")
    print("=" * 55)
    print(f"  Mean Revenue: "
          f"${results['mean_revenue']:.0f}"
          f" ± ${results['std_revenue']:.0f}")
    print(f"  Mean Sold   : "
          f"{results['mean_sold']:.1f}/50")
    print("=" * 55)

    return ppo, results


if __name__ == "__main__":
    ppo, results = run_ppo_pipeline()