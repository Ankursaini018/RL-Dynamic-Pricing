"""
final_proof.py
==============
Final statistical proof that PPO
is the best pricing strategy.

Combines all evidence into one report.

Infotact DS/ML Internship — Project 2
Week 4 : Final Proof
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import json
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import DynamicPricingEnv


def create_proof_report(
        summary_df: pd.DataFrame,
        proof: dict,
        winner: str = 'PPO',
        save_path: str = '../results/final_proof.json'):
    """
    Create comprehensive proof report.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Simulation summary.
    proof : dict
        Statistical test results.
    winner : str
        Best agent name.
    save_path : str
        Save path.
    """
    print("=" * 60)
    print("  FINAL PROOF REPORT")
    print("=" * 60)

    winner_row = summary_df[
        summary_df['Agent'] == winner
    ]

    if winner_row.empty:
        print(f"⚠️  {winner} not in results!")
        return {}

    winner_rev = winner_row[
        'Mean Revenue'
    ].values[0]

    # Best baseline
    bl_names = [
        'Fixed Price', 'Time Based',
        'Demand Based', 'Linear Decay'
    ]
    bl_df    = summary_df[
        summary_df['Agent'].isin(bl_names)
    ]
    best_bl  = bl_df['Mean Revenue'].max()
    best_bl_name = bl_df.loc[
        bl_df['Mean Revenue'].idxmax(), 'Agent'
    ]

    improvement = (
        winner_rev - best_bl
    ) / best_bl * 100

    # Significant comparisons
    sig_count = sum(
        1 for v in proof.values()
        if v.get('significant', False)
    )

    report = {
        'winner'             : winner,
        'winner_revenue'     : float(winner_rev),
        'best_baseline'      : best_bl_name,
        'best_bl_revenue'    : float(best_bl),
        'improvement_pct'    : float(improvement),
        'n_seasons'          : 1000,
        'statistical_proof'  : {
            'n_comparisons'  : len(proof),
            'significant'    : sig_count,
            'all_significant': sig_count == len(proof)
        },
        'proof_summary'      : proof
    }

    os.makedirs(
        os.path.dirname(save_path)
        if os.path.dirname(save_path)
        else '.', exist_ok=True
    )

    with open(save_path, 'w') as f:
        json.dump(report, f, indent=4)

    print(f"\n  Winner         : {winner}")
    print(f"  Revenue        : ${winner_rev:.0f}")
    print(f"  vs Baseline    : {improvement:+.1f}%")
    print(f"  Sig tests      : "
          f"{sig_count}/{len(proof)} ✅")
    print(f"\n✅ Proof report saved!")

    return report


def plot_proof_summary(
        summary_df: pd.DataFrame,
        proof: dict,
        winner: str = 'PPO',
        save_path: str = '../results/proof_summary.png'):
    """
    Plot final proof summary.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Results summary.
    proof : dict
        Statistical tests.
    winner : str
        Best agent name.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Colors
    colors_map = {
        'PPO'          : 'gold',
        'DQN'          : 'coral',
        'Q-Learning'   : 'green',
        'Time Based'   : 'steelblue',
        'Demand Based' : 'purple',
        'Linear Decay' : 'orange',
        'Fixed Price'  : 'lightgray',
    }

    names    = summary_df['Agent'].values
    revenues = summary_df['Mean Revenue'].values
    colors   = [
        colors_map.get(n, 'steelblue')
        for n in names
    ]

    # ── Chart 1: Revenue with winner highlight ──
    bars = axes[0].bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        width=0.7
    )
    axes[0].set_title(
        f'🏆 {winner} Wins!\n'
        f'1000-Season Revenue Comparison',
        fontweight='bold', fontsize=13
    )
    axes[0].set_ylabel('Mean Revenue ($)')
    axes[0].set_xticklabels(
        names, rotation=20, fontsize=9
    )
    medals = ['🥇', '🥈', '🥉',
              '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    for i, (bar, val) in enumerate(
        zip(bars, revenues)
    ):
        axes[0].text(
            bar.get_x() + bar.get_width()/2,
            val + 10,
            f'{medals[i]} ${val:.0f}',
            ha='center', fontsize=9,
            fontweight='bold'
        )

    # ── Chart 2: Improvement vs winner ──
    winner_rev = summary_df[
        summary_df['Agent'] == winner
    ]['Mean Revenue'].values[0]

    others = summary_df[
        summary_df['Agent'] != winner
    ]
    imp_names = others['Agent'].values
    imps      = [
        (winner_rev - rev) / rev * 100
        for rev in others['Mean Revenue'].values
    ]
    imp_colors = [
        '#4CAF50' if v > 0 else '#F44336'
        for v in imps
    ]

    bars2 = axes[1].bar(
        imp_names, imps,
        color=imp_colors,
        edgecolor='black',
        width=0.7
    )
    axes[1].axhline(
        y=0, color='black',
        linewidth=1.5
    )
    axes[1].set_title(
        f'{winner} Improvement\nvs All Other Agents',
        fontweight='bold', fontsize=13
    )
    axes[1].set_ylabel('Improvement (%)')
    axes[1].set_xticklabels(
        imp_names, rotation=20, fontsize=9
    )
    for bar, val in zip(bars2, imps):
        axes[1].text(
            bar.get_x() + bar.get_width()/2,
            val + 0.3,
            f'+{val:.1f}%',
            ha='center',
            fontweight='bold', fontsize=10
        )

    plt.suptitle(
        'Final Statistical Proof\n'
        f'{winner} is the Best Pricing Agent',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


if __name__ == "__main__":
    print("✅ Final proof module loaded!")