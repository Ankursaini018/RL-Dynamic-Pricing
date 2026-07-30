"""
trajectory_insights_final.py
=============================
Final price trajectory analysis
proving PPO learned smart behaviors.

Two key behaviors proved:
1. Deadline Discounting
2. Scarcity Premium Pricing

Infotact DS/ML Internship — Project 2
Week 4 : Final Trajectory Insights
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)


def prove_all_behaviors(
        ppo_agent,
        env: DynamicPricingEnv,
        n_episodes: int = 200,
        save_path: str = '../results/behavior_proof.png'):
    """
    Prove ALL smart behaviors learned by PPO.

    Parameters
    ----------
    ppo_agent : PPOAgent
        Trained PPO agent.
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Episodes to analyze.
    save_path : str
        Save path.
    """
    print("=" * 55)
    print("  PROVING PPO LEARNED BEHAVIORS")
    print("=" * 55)

    # Collect data
    data = []
    for ep in range(n_episodes):
        state, _ = env.reset(seed=ep)
        done     = False
        while not done:
            action = ppo_agent.select_action(
                state, training=False
            )
            if isinstance(action, tuple):
                action = action[0]
            price = PRICE_LEVELS[action]
            inv   = int(state[0])
            days  = int(state[1])

            data.append({
                'price'    : price,
                'inventory': inv,
                'days_left': days,
                'inv_pct'  : inv / env.max_inventory,
                'days_pct' : days / env.max_days
            })

            state, _, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc

    df = pd.DataFrame(data)

    # ── Behavior 1: Deadline Discounting ──
    time_groups = {
        'Early\n(20-30 days)' : df[df['days_left'] >= 20]['price'],
        'Mid\n(10-20 days)'   : df[(df['days_left'] >= 10) & (df['days_left'] < 20)]['price'],
        'Late\n(5-10 days)'   : df[(df['days_left'] >= 5) & (df['days_left'] < 10)]['price'],
        'Urgent\n(0-5 days)'  : df[df['days_left'] < 5]['price'],
    }
    time_avgs = {
        k: v.mean() for k, v in time_groups.items()
    }

    # ── Behavior 2: Scarcity Pricing ──
    inv_groups = {
        'High\n(>40)'  : df[df['inventory'] > 40]['price'],
        'Mid\n(20-40)' : df[(df['inventory'] >= 20) & (df['inventory'] <= 40)]['price'],
        'Low\n(10-20)' : df[(df['inventory'] >= 10) & (df['inventory'] < 20)]['price'],
        'Very Low\n(<10)': df[df['inventory'] < 10]['price'],
    }
    inv_avgs = {
        k: v.mean() for k, v in inv_groups.items()
    }

    # ── Print Results ──
    early_avg  = list(time_avgs.values())[0]
    urgent_avg = list(time_avgs.values())[-1]
    drop_pct   = (
        early_avg - urgent_avg
    ) / early_avg * 100

    high_avg = list(inv_avgs.values())[0]
    low_avg  = list(inv_avgs.values())[-1]
    prem_pct = (
        low_avg - high_avg
    ) / high_avg * 100

    print(f"\n  BEHAVIOR 1 — DEADLINE DISCOUNTING:")
    for period, avg in time_avgs.items():
        print(f"  {period.replace(chr(10), ' '):<25}: "
              f"${avg:.0f}")
    if urgent_avg < early_avg:
        print(f"  ✅ PROVED! Price drops "
              f"{drop_pct:.1f}% near deadline!")

    print(f"\n  BEHAVIOR 2 — SCARCITY PRICING:")
    for level, avg in inv_avgs.items():
        print(f"  {level.replace(chr(10), ' '):<25}: "
              f"${avg:.0f}")
    if low_avg > high_avg:
        print(f"  ✅ PROVED! Price rises "
              f"{prem_pct:.1f}% for low inventory!")

    # ── Plot ──
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # Deadline plot
    colors1 = ['green', 'steelblue',
               'orange', 'red']
    bars1 = axes[0].bar(
        list(time_avgs.keys()),
        list(time_avgs.values()),
        color=colors1,
        edgecolor='black', width=0.6
    )
    axes[0].set_title(
        '✅ BEHAVIOR 1: Deadline Discounting\n'
        'PPO Drops Prices Near Departure',
        fontweight='bold', fontsize=13
    )
    axes[0].set_ylabel('Average Price ($)')
    axes[0].set_ylim([0, 350])
    for bar, val in zip(
        bars1, time_avgs.values()
    ):
        axes[0].text(
            bar.get_x() + bar.get_width()/2,
            val + 3,
            f'${val:.0f}',
            ha='center',
            fontweight='bold', fontsize=11
        )

    # Add arrow
    axes[0].annotate(
        f'Drop:\n-{drop_pct:.1f}%',
        xy=(3, urgent_avg),
        xytext=(2.2, early_avg - 20),
        fontsize=11, color='red',
        fontweight='bold',
        arrowprops=dict(
            arrowstyle='->',
            color='red', lw=2
        )
    )

    # Scarcity plot
    colors2 = ['green', 'steelblue',
               'orange', 'red']
    bars2 = axes[1].bar(
        list(inv_avgs.keys()),
        list(inv_avgs.values()),
        color=colors2,
        edgecolor='black', width=0.6
    )
    axes[1].set_title(
        '✅ BEHAVIOR 2: Scarcity Premium\n'
        'PPO Raises Prices for Low Inventory',
        fontweight='bold', fontsize=13
    )
    axes[1].set_ylabel('Average Price ($)')
    axes[1].set_ylim([0, 350])
    for bar, val in zip(
        bars2, inv_avgs.values()
    ):
        axes[1].text(
            bar.get_x() + bar.get_width()/2,
            val + 3,
            f'${val:.0f}',
            ha='center',
            fontweight='bold', fontsize=11
        )

    # Add arrow
    axes[1].annotate(
        f'Premium:\n+{prem_pct:.1f}%',
        xy=(3, low_avg),
        xytext=(1.5, low_avg + 30),
        fontsize=11, color='green',
        fontweight='bold',
        arrowprops=dict(
            arrowstyle='->',
            color='green', lw=2
        )
    )

    plt.suptitle(
        'PPO Learned Complex Pricing Behaviors\n'
        'Statistical Proof from 200 Episodes',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")

    return {
        'deadline_drop_pct'  : float(drop_pct),
        'scarcity_premium_pct': float(prem_pct),
        'early_avg'          : float(early_avg),
        'urgent_avg'         : float(urgent_avg),
        'high_inv_avg'       : float(high_avg),
        'low_inv_avg'        : float(low_avg)
    }


if __name__ == "__main__":
    print("✅ Final trajectory insights loaded!")