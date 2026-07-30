"""
business_dashboard.py
=====================
Complete business dashboard showing
all project results in one place.

KEY chart for Final Review!

Infotact DS/ML Internship — Project 2
Week 4 : Business Dashboard
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import json
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)

os.makedirs('../results', exist_ok=True)


# ─────────────────────────────────────────
# MAIN DASHBOARD
# ─────────────────────────────────────────

def create_business_dashboard(
        summary_df: pd.DataFrame,
        all_results: dict,
        ppo_agent,
        env: DynamicPricingEnv,
        save_path: str = '../results/business_dashboard.png'):
    """
    Create complete business dashboard.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Simulation summary.
    all_results : dict
        All season results.
    ppo_agent : PPOAgent
        Best trained PPO agent.
    env : DynamicPricingEnv
        Environment.
    save_path : str
        Save path.
    """
    print("=" * 60)
    print("  CREATING BUSINESS DASHBOARD")
    print("=" * 60)

    colors_map = {
        'PPO'          : 'gold',
        'DQN'          : 'coral',
        'Q-Learning'   : 'green',
        'Time Based'   : 'steelblue',
        'Demand Based' : 'purple',
        'Linear Decay' : 'orange',
        'Fixed Price'  : 'lightgray',
    }

    fig = plt.figure(figsize=(24, 20))
    gs  = gridspec.GridSpec(
        4, 3, figure=fig,
        hspace=0.4, wspace=0.3
    )

    names    = summary_df['Agent'].values
    revenues = summary_df['Mean Revenue'].values
    colors   = [
        colors_map.get(n, 'steelblue')
        for n in names
    ]
    medals   = ['🥇', '🥈', '🥉',
                '4️⃣', '5️⃣', '6️⃣', '7️⃣']

    # ── Plot 1: Main Revenue Ranking ──
    ax1 = fig.add_subplot(gs[0, :2])
    bars = ax1.bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        width=0.7,
        yerr=summary_df['Std Revenue'].values,
        capsize=5
    )
    ax1.set_title(
        '🏆 Final Agent Rankings\n'
        '1000-Season Mean Revenue',
        fontweight='bold', fontsize=14
    )
    ax1.set_ylabel('Mean Revenue ($)',
                   fontsize=12)
    ax1.set_xticklabels(
        names, rotation=15, fontsize=10
    )
    for i, (bar, val) in enumerate(
        zip(bars, revenues)
    ):
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            val + 20,
            f'{medals[i]}\n${val:.0f}',
            ha='center', fontsize=9,
            fontweight='bold'
        )

    # ── Plot 2: Sell Through ──
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.bar(
        names,
        summary_df['Sell Through %'],
        color=colors,
        edgecolor='black'
    )
    ax2.axhline(
        y=100, color='red',
        linestyle='--', alpha=0.7,
        label='100% sold'
    )
    ax2.set_title(
        'Sell-Through Rate\n(% Tickets Sold)',
        fontweight='bold'
    )
    ax2.set_ylabel('Sell Through %')
    ax2.set_xticklabels(
        names, rotation=20, fontsize=7
    )
    ax2.legend(fontsize=8)

    # ── Plot 3: PPO Price Trajectory ──
    ax3 = fig.add_subplot(gs[1, :2])
    for ep in range(5):
        state, _ = env.reset(seed=ep)
        prices   = []
        days_left_list = []
        done     = False
        while not done:
            action = ppo_agent.select_action(
                state, training=False
            )
            if isinstance(action, tuple):
                action = action[0]
            prices.append(PRICE_LEVELS[action])
            days_left_list.append(int(state[1]))
            state, _, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc

        ax3.plot(
            range(1, len(prices)+1),
            prices,
            alpha=0.6, linewidth=2,
            marker='o', markersize=3,
            label=f'Episode {ep+1}'
        )

    ax3.axvspan(
        25, 30, alpha=0.15,
        color='red', label='Deadline Zone'
    )
    ax3.set_title(
        'PPO Price Trajectories — 5 Episodes\n'
        '📉 Prices Drop Near Deadline (Day 25-30)',
        fontweight='bold', fontsize=12
    )
    ax3.set_xlabel('Day of Season')
    ax3.set_ylabel('Price ($)')
    ax3.set_ylim([0, 350])
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=8)

    # ── Plot 4: Deadline Proof ──
    ax4 = fig.add_subplot(gs[1, 2])
    early_prices  = []
    mid_prices    = []
    late_prices   = []
    urgent_prices = []

    for ep in range(100):
        state, _ = env.reset(seed=ep)
        done     = False
        while not done:
            action = ppo_agent.select_action(
                state, training=False
            )
            if isinstance(action, tuple):
                action = action[0]
            price = PRICE_LEVELS[action]
            days  = int(state[1])

            if days >= 20:
                early_prices.append(price)
            elif days >= 10:
                mid_prices.append(price)
            elif days >= 5:
                late_prices.append(price)
            else:
                urgent_prices.append(price)

            state, _, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc

    periods   = [
        'Early\n(20-30)',
        'Mid\n(10-20)',
        'Late\n(5-10)',
        'Urgent\n(0-5)'
    ]
    avgs      = [
        np.mean(early_prices),
        np.mean(mid_prices),
        np.mean(late_prices),
        np.mean(urgent_prices)
    ]
    p_colors  = ['green', 'steelblue',
                 'orange', 'red']

    bars4 = ax4.bar(
        periods, avgs,
        color=p_colors,
        edgecolor='black', width=0.6
    )
    ax4.set_title(
        '✅ Deadline Discounting PROVED!\n'
        'PPO Drops Prices Near Deadline',
        fontweight='bold'
    )
    ax4.set_ylabel('Average Price ($)')
    for bar, val in zip(bars4, avgs):
        ax4.text(
            bar.get_x() + bar.get_width()/2,
            val + 2,
            f'${val:.0f}',
            ha='center',
            fontweight='bold', fontsize=10
        )

    # ── Plot 5: Revenue Distribution ──
    ax5 = fig.add_subplot(gs[2, :2])
    for name, df in all_results.items():
        ax5.hist(
            df['revenue'],
            bins=40, alpha=0.5,
            color=colors_map.get(
                name, 'steelblue'
            ),
            label=name,
            edgecolor='black',
            linewidth=0.3
        )
    ax5.set_title(
        'Revenue Distribution — 1000 Seasons',
        fontweight='bold'
    )
    ax5.set_xlabel('Revenue ($)')
    ax5.set_ylabel('Frequency')
    ax5.legend(fontsize=8)

    # ── Plot 6: Business Value ──
    ax6 = fig.add_subplot(gs[2, 2])
    ppo_rev  = summary_df[
        summary_df['Agent'] == 'PPO'
    ]['Mean Revenue'].values[0]
    best_bl  = summary_df[
        summary_df['Agent'].isin([
            'Fixed Price', 'Time Based',
            'Demand Based', 'Linear Decay'
        ])
    ]['Mean Revenue'].max()

    uplift      = ppo_rev - best_bl
    projections = {
        'Daily'   : uplift,
        'Weekly'  : uplift * 7,
        'Monthly' : uplift * 30,
        'Annual'  : uplift * 365,
    }
    ax6.bar(
        list(projections.keys()),
        list(projections.values()),
        color='gold',
        edgecolor='black', width=0.5
    )
    ax6.set_title(
        'PPO Revenue Uplift\nBusiness Projections',
        fontweight='bold'
    )
    ax6.set_ylabel('Additional Revenue ($)')
    for i, (period, val) in enumerate(
        projections.items()
    ):
        ax6.text(
            i, val + 1,
            f'+${val:.0f}',
            ha='center',
            fontweight='bold', fontsize=9
        )

    # ── Plot 7: RL Evolution ──
    ax7 = fig.add_subplot(gs[3, :])
    rl_agents = ['Q-Learning', 'DQN', 'PPO']
    rl_revs   = []
    rl_colors = ['green', 'coral', 'gold']

    for name in rl_agents:
        row = summary_df[
            summary_df['Agent'] == name
        ]
        if not row.empty:
            rl_revs.append(
                row['Mean Revenue'].values[0]
            )
        else:
            rl_revs.append(0)

    bars7 = ax7.barh(
        rl_agents, rl_revs,
        color=rl_colors,
        edgecolor='black', height=0.5
    )
    ax7.set_title(
        'RL Agent Evolution\n'
        'Q-Learning → DQN → PPO Progress',
        fontweight='bold', fontsize=12
    )
    ax7.set_xlabel('Mean Revenue ($)')
    for bar, val in zip(bars7, rl_revs):
        ax7.text(
            val + 10,
            bar.get_y() + bar.get_height()/2,
            f'${val:.0f}',
            va='center',
            fontweight='bold', fontsize=12
        )

    plt.suptitle(
        'PROJECT 2 — RL DYNAMIC PRICING\n'
        'COMPLETE BUSINESS DASHBOARD',
        fontsize=18, fontweight='bold'
    )
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"\n✅ Business dashboard saved!")
    print(f"   Path: {save_path}")

    return {
        'ppo_revenue'    : float(ppo_rev),
        'baseline_revenue': float(best_bl),
        'daily_uplift'   : float(uplift),
        'annual_uplift'  : float(uplift * 365),
        'early_avg'      : float(np.mean(early_prices)),
        'urgent_avg'     : float(np.mean(urgent_prices))
    }


if __name__ == "__main__":
    print("✅ Business dashboard loaded!")