"""
trajectory_insights.py
======================
Advanced trajectory insights showing
what DQN learned about pricing strategy.

Infotact DS/ML Internship — Project 2
Week 2 : Trajectory Insights
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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


def analyze_scarcity_pricing(
        agent,
        env: DynamicPricingEnv,
        n_episodes: int = 100,
        save_path: str = '../results/scarcity_pricing.png'):
    """
    Prove DQN raises prices when inventory low.

    Parameters
    ----------
    agent : DQNAgent
        Trained agent.
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Episodes.
    save_path : str
        Save path.
    """
    print("=" * 55)
    print("  SCARCITY PRICING ANALYSIS")
    print("=" * 55)

    # Collect prices by inventory level
    inv_price_data = []

    for ep in range(n_episodes):
        state, _ = env.reset(seed=ep)
        done     = False

        while not done:
            action = agent.select_action(
                state, training=False
            )
            price = PRICE_LEVELS[action]
            inv   = int(state[0])

            inv_price_data.append({
                'inventory'  : inv,
                'price'      : price,
                'inv_bucket' : (
                    'Very Low (0-10)' if inv <= 10
                    else 'Low (11-20)'   if inv <= 20
                    else 'Mid (21-35)'   if inv <= 35
                    else 'High (36-50)'
                )
            })

            state, _, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc

    df = pd.DataFrame(inv_price_data)

    # Average price by bucket
    bucket_avg = df.groupby(
        'inv_bucket'
    )['price'].mean().sort_index()

    print(f"\n  Average Price by Inventory Level:")
    for bucket, avg in bucket_avg.items():
        print(f"  {bucket:<20}: ${avg:.0f}")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar chart
    colors_b = ['red', 'orange',
                 'steelblue', 'green']
    buckets  = [
        'Very Low (0-10)', 'Low (11-20)',
        'Mid (21-35)', 'High (36-50)'
    ]
    avgs = [
        df[df['inv_bucket'] == b]['price'].mean()
        for b in buckets
    ]

    bars = axes[0].bar(
        buckets, avgs,
        color=colors_b,
        edgecolor='black', width=0.6
    )
    axes[0].set_title(
        'DQN Pricing by Inventory Level\n'
        'Scarcity Premium Effect',
        fontweight='bold'
    )
    axes[0].set_ylabel('Average Price ($)')
    axes[0].set_xticklabels(
        buckets, rotation=15, fontsize=9
    )
    for bar, val in zip(bars, avgs):
        axes[0].text(
            bar.get_x() + bar.get_width()/2,
            val + 2,
            f'${val:.0f}',
            ha='center',
            fontweight='bold', fontsize=10
        )

    # Scatter
    sample = df.sample(
        min(2000, len(df)),
        random_state=42
    )
    axes[1].scatter(
        sample['inventory'],
        sample['price'],
        alpha=0.2, s=5,
        c=sample['price'],
        cmap='RdYlGn'
    )
    # Trend line
    z = np.polyfit(
        sample['inventory'],
        sample['price'], 1
    )
    p = np.poly1d(z)
    x_line = np.linspace(0, 50, 100)
    axes[1].plot(
        x_line, p(x_line),
        'r--', linewidth=2,
        label='Trend'
    )
    axes[1].set_title(
        'Price vs Inventory Scatter\n'
        'Showing Scarcity Effect',
        fontweight='bold'
    )
    axes[1].set_xlabel('Remaining Inventory')
    axes[1].set_ylabel('Price ($)')
    axes[1].legend()

    plt.suptitle(
        'Scarcity Pricing Analysis\n'
        'DQN Raises Prices When Inventory Low',
        fontsize=13, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")

    return df


def compare_trajectory_patterns(
        agents: dict,
        env: DynamicPricingEnv,
        save_path: str = '../results/pattern_comparison.png'):
    """
    Compare pricing patterns across agents.

    Parameters
    ----------
    agents : dict
        {name: agent} dictionary.
    env : DynamicPricingEnv
        Environment.
    save_path : str
        Save path.
    """
    colors = ['gold', 'coral', 'steelblue',
              'green', 'purple']

    fig, axes = plt.subplots(
        len(agents), 1,
        figsize=(14, 4 * len(agents))
    )

    if len(agents) == 1:
        axes = [axes]

    for i, (name, agent) in enumerate(
        agents.items()
    ):
        # Run 5 episodes and overlay
        for ep in range(5):
            prices = []
            if hasattr(agent, 'select_action'):
                state, _ = env.reset(seed=ep)
                done     = False
                while not done:
                    action = agent.select_action(
                        state, training=False
                    )
                    prices.append(
                        PRICE_LEVELS[action]
                    )
                    state, _, term, trunc, _ = (
                        env.step(action)
                    )
                    done = term or trunc
            else:
                result = agent.run_episode(seed=ep)
                prices = result['prices_used']

            axes[i].plot(
                prices,
                color=colors[i % len(colors)],
                alpha=0.4, linewidth=1.5
            )

        axes[i].set_title(
            f'{name} — Price Trajectories '
            f'(5 episodes)',
            fontweight='bold'
        )
        axes[i].set_ylabel('Price ($)')
        axes[i].set_ylim([0, 350])
        axes[i].grid(True, alpha=0.3)
        axes[i].axvspan(
            25, 30, alpha=0.1, color='red'
        )

    axes[-1].set_xlabel('Day of Season')
    plt.suptitle(
        'Pricing Pattern Comparison\n'
        'All Agents — Multiple Episodes',
        fontsize=13, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


if __name__ == "__main__":
    print("✅ Trajectory insights loaded!")