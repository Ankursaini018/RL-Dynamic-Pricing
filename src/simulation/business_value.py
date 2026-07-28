"""
business_value.py
=================
Translates RL simulation results
into business value metrics.

Shows the REAL WORLD impact of
using PPO over traditional pricing!

Infotact DS/ML Internship — Project 2
Week 4 : Business Value
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.makedirs('../results', exist_ok=True)


def calculate_business_value(
        summary_df: pd.DataFrame,
        winner: str = 'PPO',
        seasons_per_year: int = 365) -> dict:
    """
    Calculate real business value.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Simulation results.
    winner : str
        Best agent name.
    seasons_per_year : int
        Seasons in a year (daily flights).

    Returns
    -------
    dict
        Business value metrics.
    """
    print("=" * 60)
    print("  BUSINESS VALUE ANALYSIS")
    print("=" * 60)

    winner_rev = summary_df[
        summary_df['Agent'] == winner
    ]['Mean Revenue'].values[0]

    bl_names = [
        'Fixed Price', 'Time Based',
        'Demand Based', 'Linear Decay'
    ]
    bl_revs  = summary_df[
        summary_df['Agent'].isin(bl_names)
    ]['Mean Revenue']
    best_bl  = bl_revs.max()

    # Revenue uplift
    daily_uplift   = winner_rev - best_bl
    monthly_uplift = daily_uplift * 30
    annual_uplift  = daily_uplift * seasons_per_year
    uplift_pct     = (
        daily_uplift / best_bl * 100
    )

    # Sell through
    winner_sell = summary_df[
        summary_df['Agent'] == winner
    ]['Sell Through %'].values[0]
    bl_sell     = summary_df[
        summary_df['Agent'].isin(bl_names)
    ]['Sell Through %'].max()
    sell_imp    = winner_sell - bl_sell

    print(f"\n  REVENUE ANALYSIS:")
    print(f"  Best Baseline Revenue : ${best_bl:.0f}")
    print(f"  {winner} Revenue      : ${winner_rev:.0f}")
    print(f"  Daily Uplift          : "
          f"+${daily_uplift:.0f}")
    print(f"  Monthly Uplift        : "
          f"+${monthly_uplift:.0f}")
    print(f"  Annual Uplift         : "
          f"+${annual_uplift:.0f}")
    print(f"  Improvement %         : "
          f"+{uplift_pct:.1f}%")

    print(f"\n  SELL-THROUGH:")
    print(f"  Best Baseline : {bl_sell:.1f}%")
    print(f"  {winner}      : {winner_sell:.1f}%")
    print(f"  Improvement   : +{sell_imp:.1f}%")

    bv = {
        'winner'            : winner,
        'winner_revenue'    : float(winner_rev),
        'baseline_revenue'  : float(best_bl),
        'daily_uplift'      : float(daily_uplift),
        'monthly_uplift'    : float(monthly_uplift),
        'annual_uplift'     : float(annual_uplift),
        'uplift_pct'        : float(uplift_pct),
        'winner_sell_pct'   : float(winner_sell),
        'baseline_sell_pct' : float(bl_sell),
        'sell_improvement'  : float(sell_imp),
        'recommendation'    : (
            f"Deploy {winner} for "
            f"+{uplift_pct:.1f}% revenue!"
        )
    }

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Revenue comparison
    rev_data = {
        'Best Baseline'    : best_bl,
        f'{winner} Daily'  : winner_rev,
        f'{winner} Monthly': monthly_uplift / 30
                             + best_bl,
    }
    axes[0].bar(
        list(rev_data.keys()),
        list(rev_data.values()),
        color=['steelblue', 'gold', 'green'],
        edgecolor='black',
        width=0.5
    )
    axes[0].set_title(
        'Revenue Comparison\nPer Season',
        fontweight='bold'
    )
    axes[0].set_ylabel('Revenue ($)')

    # Annual projection
    time_periods = [
        'Day', 'Week', 'Month', 'Year'
    ]
    multipliers  = [1, 7, 30, 365]
    uplifts      = [
        daily_uplift * m for m in multipliers
    ]
    axes[1].bar(
        time_periods, uplifts,
        color='gold',
        edgecolor='black',
        width=0.5
    )
    axes[1].set_title(
        f'{winner} Revenue Uplift\nProjections',
        fontweight='bold'
    )
    axes[1].set_ylabel('Uplift ($)')
    for i, val in enumerate(uplifts):
        axes[1].text(
            i, val + 10,
            f'+${val:.0f}',
            ha='center',
            fontweight='bold'
        )

    plt.suptitle(
        'Business Value Analysis\n'
        f'{winner} Pricing Strategy',
        fontsize=13, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(
        '../results/business_value.png',
        bbox_inches='tight', dpi=150
    )
    plt.show()

    # Save
    with open(
        '../results/business_value.json', 'w'
    ) as f:
        json.dump(bv, f, indent=4)
    print(f"\n✅ Business value saved!")
    print(f"   {bv['recommendation']}")

    return bv


if __name__ == "__main__":
    print("✅ Business value module loaded!")