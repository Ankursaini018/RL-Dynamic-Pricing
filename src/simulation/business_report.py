"""
business_report.py
==================
Generates business metrics report
from 1000-season simulation results.

Translates RL metrics into business value!

Infotact DS/ML Internship — Project 2
Week 2 : Business Metrics
"""

import numpy as np
import pandas as pd
import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


def generate_business_report(
        all_results: dict,
        summary_df: pd.DataFrame,
        dqn_name: str = 'DQN 🤖',
        save_path: str = '../results/business_report.json'):
    """
    Generate business value report.

    Parameters
    ----------
    all_results : dict
        1000-season simulation results.
    summary_df : pd.DataFrame
        Summary statistics.
    dqn_name : str
        DQN agent name.
    save_path : str
        JSON save path.
    """
    print("=" * 55)
    print("  BUSINESS VALUE REPORT")
    print("=" * 55)

    dqn_df  = all_results.get(dqn_name)
    if dqn_df is None:
        print(f"❌ {dqn_name} not found!")
        return

    dqn_mean = dqn_df['revenue'].mean()

    # Best baseline
    baseline_names = [
        n for n in all_results.keys()
        if n != dqn_name and 'Q-Learning' not in n
    ]
    best_bl_name = max(
        baseline_names,
        key=lambda n: all_results[n]['revenue'].mean()
    )
    best_bl_mean = all_results[
        best_bl_name
    ]['revenue'].mean()

    # Revenue uplift
    revenue_uplift    = dqn_mean - best_bl_mean
    uplift_pct        = revenue_uplift / best_bl_mean * 100
    annual_uplift     = revenue_uplift * 365

    print(f"\n  REVENUE ANALYSIS (per season):")
    print(f"  Best Baseline  : ${best_bl_mean:.0f}")
    print(f"  DQN Revenue    : ${dqn_mean:.0f}")
    print(f"  Revenue Uplift : +${revenue_uplift:.0f}")
    print(f"  Uplift %       : +{uplift_pct:.1f}%")

    print(f"\n  BUSINESS PROJECTIONS:")
    print(f"  Daily uplift   : +${revenue_uplift:.0f}")
    print(f"  Monthly uplift : "
          f"+${revenue_uplift*30:.0f}")
    print(f"  Annual uplift  : "
          f"+${annual_uplift:.0f}")

    # Sell-through improvement
    dqn_sell  = dqn_df['sell_through'].mean() * 100
    bl_sell   = all_results[
        best_bl_name
    ]['sell_through'].mean() * 100
    sell_imp  = dqn_sell - bl_sell

    print(f"\n  SELL-THROUGH ANALYSIS:")
    print(f"  Best Baseline  : {bl_sell:.1f}%")
    print(f"  DQN            : {dqn_sell:.1f}%")
    print(f"  Improvement    : +{sell_imp:.1f}%")

    # Save report
    report = {
        'simulation_seasons' : 1000,
        'best_baseline'      : {
            'name'    : best_bl_name,
            'revenue' : float(best_bl_mean)
        },
        'dqn'                : {
            'revenue'      : float(dqn_mean),
            'sell_through' : float(dqn_sell)
        },
        'business_value'     : {
            'revenue_uplift_per_season' : float(
                revenue_uplift
            ),
            'uplift_percentage'         : float(
                uplift_pct
            ),
            'projected_annual_uplift'   : float(
                annual_uplift
            ),
            'sell_through_improvement'  : float(
                sell_imp
            )
        },
        'recommendation'     : (
            'Deploy DQN pricing agent for '
            f'+{uplift_pct:.1f}% revenue improvement!'
            if uplift_pct > 0
            else 'Continue training DQN agent.'
        )
    }

    os.makedirs(
        os.path.dirname(save_path),
        exist_ok=True
    )
    with open(save_path, 'w') as f:
        json.dump(report, f, indent=4)

    print(f"\n✅ Report saved: {save_path}")
    print(f"\n  RECOMMENDATION:")
    print(f"  {report['recommendation']}")
    print("=" * 55)

    return report


if __name__ == "__main__":
    print("✅ Business report generator loaded!")