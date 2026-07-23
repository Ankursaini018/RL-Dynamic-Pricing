"""
final_comparison.py
===================
Final comparison of ALL agents
showing PPO as the best strategy.

Infotact DS/ML Internship — Project 2
Week 3 : Final Comparison
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


def create_final_summary_chart(
        results_df: pd.DataFrame,
        save_path: str = '../results/final_comparison.png'):
    """
    Create the FINAL summary comparison chart.
    This is the KEY chart for final review!

    Parameters
    ----------
    results_df : pd.DataFrame
        All agent results.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    colors_map = {
        'PPO'          : 'gold',
        'DQN'          : 'coral',
        'Q-Learning'   : 'green',
        'Time Based'   : 'steelblue',
        'Demand Based' : 'purple',
        'Linear Decay' : 'orange',
        'Fixed Price'  : 'lightgray',
    }

    names    = results_df['Agent'].values
    revenues = results_df['Mean Revenue'].values
    colors   = [
        colors_map.get(n, 'steelblue')
        for n in names
    ]

    # ── Chart 1: Revenue Bars ──
    bars = axes[0].bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        width=0.7,
        yerr=results_df['Std Revenue'].values,
        capsize=5
    )
    axes[0].set_title(
        '🏆 Final Agent Rankings\nMean Revenue per Season',
        fontweight='bold', fontsize=14
    )
    axes[0].set_ylabel('Mean Revenue ($)',
                       fontsize=12)
    axes[0].set_xticklabels(
        names, rotation=20, fontsize=10
    )

    # Add medals
    medals = ['🥇', '🥈', '🥉',
              '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    for i, (bar, val) in enumerate(
        zip(bars, revenues)
    ):
        axes[0].text(
            bar.get_x() + bar.get_width()/2,
            val + 20,
            f'{medals[i]}\n${val:.0f}',
            ha='center', fontsize=9,
            fontweight='bold'
        )

    # ── Chart 2: Improvement over baseline ──
    best_bl = results_df[
        results_df['Agent'].isin([
            'Fixed Price', 'Time Based',
            'Demand Based', 'Linear Decay'
        ])
    ]['Mean Revenue'].max()

    rl_agents = results_df[
        results_df['Agent'].isin([
            'Q-Learning', 'DQN', 'PPO'
        ])
    ]

    improvements = [
        (row['Agent'],
         (row['Mean Revenue'] - best_bl) /
         best_bl * 100)
        for _, row in rl_agents.iterrows()
    ]

    imp_names  = [x[0] for x in improvements]
    imp_values = [x[1] for x in improvements]
    imp_colors = ['green', 'coral', 'gold']

    bars2 = axes[1].bar(
        imp_names, imp_values,
        color=imp_colors,
        edgecolor='black',
        width=0.5
    )
    axes[1].axhline(
        y=0, color='black',
        linewidth=1.5
    )
    axes[1].set_title(
        'RL Agent Improvement\nvs Best Baseline',
        fontweight='bold', fontsize=14
    )
    axes[1].set_ylabel(
        'Improvement (%)', fontsize=12
    )
    for bar, val in zip(bars2, imp_values):
        axes[1].text(
            bar.get_x() + bar.get_width()/2,
            val + 0.2,
            f'+{val:.1f}%',
            ha='center',
            fontweight='bold', fontsize=12
        )

    plt.suptitle(
        'Project 2 — RL Dynamic Pricing\n'
        'FINAL RESULTS SUMMARY',
        fontsize=16, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Final chart saved: {save_path}")


def save_final_results(
        results_df: pd.DataFrame,
        proof_results: dict,
        save_path: str = '../results/final_results.json'):
    """
    Save final results summary.

    Parameters
    ----------
    results_df : pd.DataFrame
        Evaluation results.
    proof_results : dict
        Statistical proof results.
    save_path : str
        Save path.
    """
    best_agent = results_df.iloc[0]
    best_bl    = results_df[
        results_df['Agent'].isin([
            'Fixed Price', 'Time Based',
            'Demand Based', 'Linear Decay'
        ])
    ]['Mean Revenue'].max()

    summary = {
        'project'      : 'RL Dynamic Pricing',
        'best_agent'   : best_agent['Agent'],
        'best_revenue' : float(
            best_agent['Mean Revenue']
        ),
        'vs_baseline'  : float(
            (best_agent['Mean Revenue'] - best_bl)
            / best_bl * 100
        ),
        'all_agents'   : results_df[[
            'Agent', 'Mean Revenue', 'Std Revenue'
        ]].to_dict('records'),
        'statistical_proof': proof_results,
        'week3_complete'   : True,
    }

    with open(save_path, 'w') as f:
        json.dump(summary, f, indent=4)

    print(f"✅ Final results saved: {save_path}")
    print(f"\n  Best Agent  : {summary['best_agent']}")
    print(f"  Best Revenue: "
          f"${summary['best_revenue']:.0f}")
    print(f"  vs Baseline : "
          f"+{summary['vs_baseline']:.1f}%")

    return summary


if __name__ == "__main__":
    print("✅ Final comparison module loaded!")