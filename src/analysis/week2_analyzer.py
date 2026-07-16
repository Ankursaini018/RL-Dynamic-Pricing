"""
week2_analyzer.py
=================
Deep analysis of Week 2 results
comparing DQN vs all other agents.

Infotact DS/ML Internship — Project 2
Week 2 : Deep Analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)
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
from config import DQN

os.makedirs('../results', exist_ok=True)
os.makedirs('../src/analysis', exist_ok=True)


# ─────────────────────────────────────────
# COMPREHENSIVE ANALYSIS
# ─────────────────────────────────────────

def run_comprehensive_analysis(
        dqn_agent: DQNAgent,
        ql_agent: QLearningAgent,
        env: DynamicPricingEnv,
        n_episodes: int = 200) -> dict:
    """
    Run comprehensive Week 2 analysis.

    Parameters
    ----------
    dqn_agent : DQNAgent
        Trained DQN agent.
    ql_agent : QLearningAgent
        Trained Q-Learning agent.
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Evaluation episodes.

    Returns
    -------
    dict
        Analysis results.
    """
    print("=" * 55)
    print("  WEEK 2 COMPREHENSIVE ANALYSIS")
    print("=" * 55)

    # ── All agents ──
    agents = {
        'Fixed Price'  : FixedPriceAgent(env),
        'Random'       : None,
        'Time Based'   : TimedPricingAgent(env),
        'Demand Based' : DemandBasedAgent(env),
        'Linear Decay' : LinearDecayAgent(env),
        'Q-Learning'   : ql_agent,
        'DQN'          : dqn_agent,
    }

    # ── Evaluate all ──
    print("\n[1] Evaluating all agents...")
    results = {}
    for name, agent in agents.items():
        if agent is None:
            continue
        if hasattr(agent, 'run_episode'):
            df = evaluate_agent(
                agent, n_episodes
            )
            results[name] = {
                'mean' : df['total_revenue'].mean(),
                'std'  : df['total_revenue'].std(),
                'max'  : df['total_revenue'].max(),
                'min'  : df['total_revenue'].min(),
                'sold' : df['total_sold'].mean()
            }
        else:
            revenues = []
            sold_list = []
            for ep in range(n_episodes):
                state, _ = env.reset(seed=ep)
                total_rev  = 0
                total_sold = 0
                done       = False
                while not done:
                    action = agent.select_action(
                        state, training=False
                    )
                    state, reward, term, \
                        trunc, info = env.step(action)
                    done = term or trunc
                    total_rev  += max(0, reward)
                    if info['bought']:
                        total_sold += 1
                revenues.append(total_rev)
                sold_list.append(total_sold)
            results[name] = {
                'mean' : np.mean(revenues),
                'std'  : np.std(revenues),
                'max'  : np.max(revenues),
                'min'  : np.min(revenues),
                'sold' : np.mean(sold_list)
            }

        print(f"  {name:<15}: "
              f"${results[name]['mean']:.0f}"
              f" ± ${results[name]['std']:.0f}")

    # ── Rankings ──
    ranked = sorted(
        results.items(),
        key=lambda x: x[1]['mean'],
        reverse=True
    )

    print("\n" + "=" * 55)
    print("  FINAL RANKINGS")
    print("=" * 55)
    medals = ['🥇', '🥈', '🥉',
              '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    for i, (name, res) in enumerate(ranked):
        print(f"  {medals[i]} {name:<15}: "
              f"${res['mean']:.0f}")

    # ── Improvement Analysis ──
    print("\n" + "=" * 55)
    print("  DQN IMPROVEMENT vs BASELINES")
    print("=" * 55)
    dqn_mean = results['DQN']['mean']
    for name, res in results.items():
        if name == 'DQN':
            continue
        imp = (dqn_mean - res['mean']) / \
               res['mean'] * 100
        print(f"  vs {name:<15}: {imp:+.1f}%")

    return results, ranked


# ─────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────

def plot_comprehensive_results(
        results: dict,
        save_path: str = '../results/week2_analysis.png'):
    """
    Plot comprehensive Week 2 results.

    Parameters
    ----------
    results : dict
        Analysis results.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    names    = list(results.keys())
    means    = [r['mean'] for r in results.values()]
    stds     = [r['std']  for r in results.values()]
    maxes    = [r['max']  for r in results.values()]
    mines    = [r['min']  for r in results.values()]
    sold     = [r['sold'] for r in results.values()]

    colors = [
        'gold' if 'DQN' in n
        else 'coral' if 'Q-Learning' in n
        else 'steelblue'
        for n in names
    ]

    # ── Plot 1: Mean Revenue ──
    bars = axes[0,0].bar(
        names, means,
        color=colors,
        edgecolor='black',
        yerr=stds, capsize=5,
        width=0.6
    )
    axes[0,0].set_title(
        'Mean Revenue by Agent\n(±std)',
        fontweight='bold'
    )
    axes[0,0].set_ylabel('Revenue ($)')
    axes[0,0].set_xticklabels(
        names, rotation=20, fontsize=8
    )
    for bar, val in zip(bars, means):
        axes[0,0].text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 20,
            f'${val:.0f}',
            ha='center', fontsize=8,
            fontweight='bold'
        )

    # ── Plot 2: Max Revenue ──
    axes[0,1].bar(
        names, maxes,
        color=colors,
        edgecolor='black',
        width=0.6
    )
    axes[0,1].set_title(
        'Best Single Season Revenue',
        fontweight='bold'
    )
    axes[0,1].set_ylabel('Max Revenue ($)')
    axes[0,1].set_xticklabels(
        names, rotation=20, fontsize=8
    )

    # ── Plot 3: Tickets Sold ──
    axes[1,0].bar(
        names, sold,
        color=colors,
        edgecolor='black',
        width=0.6
    )
    axes[1,0].axhline(
        y=50, color='red',
        linestyle='--',
        label='Max (50 tickets)'
    )
    axes[1,0].set_title(
        'Average Tickets Sold per Season',
        fontweight='bold'
    )
    axes[1,0].set_ylabel('Tickets Sold')
    axes[1,0].set_xticklabels(
        names, rotation=20, fontsize=8
    )
    axes[1,0].legend()

    # ── Plot 4: Revenue Range ──
    for i, (name, res) in enumerate(
        results.items()
    ):
        axes[1,1].barh(
            i,
            res['max'] - res['min'],
            left=res['min'],
            color=colors[i],
            edgecolor='black',
            alpha=0.7,
            height=0.6,
            label=name
        )
        axes[1,1].axvline(
            x=res['mean'],
            color=colors[i],
            linewidth=1.5,
            linestyle='--'
        )

    axes[1,1].set_yticks(range(len(names)))
    axes[1,1].set_yticklabels(names, fontsize=9)
    axes[1,1].set_title(
        'Revenue Range (Min-Max)\nwith Mean Line',
        fontweight='bold'
    )
    axes[1,1].set_xlabel('Revenue ($)')

    plt.suptitle(
        'Week 2 Comprehensive Analysis\n'
        'DQN vs All Pricing Strategies',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


if __name__ == "__main__":
    print("✅ Week 2 analyzer loaded!")