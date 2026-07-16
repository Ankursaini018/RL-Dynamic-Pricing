"""
dqn_insights.py
===============
Deep insights into DQN performance
and what it learned.

Infotact DS/ML Internship — Project 2
Week 2 : DQN Insights
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
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


def analyze_q_network(
        agent,
        env: DynamicPricingEnv,
        save_path: str = '../results/q_network_analysis.png'):
    """
    Analyze Q-network predictions
    across the state space.

    Parameters
    ----------
    agent : DQNAgent
        Trained DQN agent.
    env : DynamicPricingEnv
        Environment.
    save_path : str
        Save path.
    """
    print("=" * 55)
    print("  Q-NETWORK ANALYSIS")
    print("=" * 55)

    # Get Q-values for all states
    all_states  = []
    all_actions = []
    all_q_max   = []

    for inv in range(0, 51, 2):
        for days in range(0, 31, 1):
            state = np.array(
                [inv, days],
                dtype=np.float32
            )
            norm = np.array([
                inv / env.max_inventory,
                days / env.max_days
            ], dtype=np.float32)

            tensor = torch.FloatTensor(
                norm
            ).unsqueeze(0)

            with torch.no_grad():
                q_vals = agent.online_net(
                    tensor
                ).numpy()[0]

            best_action = q_vals.argmax()
            best_price  = PRICE_LEVELS[best_action]

            all_states.append((inv, days))
            all_actions.append(best_price)
            all_q_max.append(q_vals.max())

    # Create policy grid
    inv_vals  = [s[0] for s in all_states]
    day_vals  = [s[1] for s in all_states]

    df = pd.DataFrame({
        'inventory' : inv_vals,
        'days_left' : day_vals,
        'best_price': all_actions,
        'max_q'     : all_q_max
    })

    # Pivot for heatmap
    price_pivot = df.pivot(
        index='inventory',
        columns='days_left',
        values='best_price'
    )
    q_pivot = df.pivot(
        index='inventory',
        columns='days_left',
        values='max_q'
    )

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    import seaborn as sns
    sns.heatmap(
        price_pivot,
        ax=axes[0],
        cmap='RdYlGn',
        cbar_kws={'label': 'Optimal Price ($)'},
        xticklabels=5,
        yticklabels=5
    )
    axes[0].set_title(
        'DQN Learned Policy\n'
        'Optimal Price by State',
        fontweight='bold', fontsize=13
    )
    axes[0].set_xlabel('Days Until Departure')
    axes[0].set_ylabel('Remaining Inventory')

    sns.heatmap(
        q_pivot,
        ax=axes[1],
        cmap='YlOrRd',
        cbar_kws={'label': 'Max Q-Value'},
        xticklabels=5,
        yticklabels=5
    )
    axes[1].set_title(
        'DQN Confidence\n'
        'Max Q-Value by State',
        fontweight='bold', fontsize=13
    )
    axes[1].set_xlabel('Days Until Departure')
    axes[1].set_ylabel('Remaining Inventory')

    plt.suptitle(
        'DQN Neural Network — State Analysis',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")

    # Print key insights
    print("\n  Key Policy Insights:")
    for inv, days, desc in [
        (50, 30, "Full stock, lots of time"),
        (50, 5,  "Full stock, urgent!"),
        (10, 30, "Low stock, lots of time"),
        (10, 5,  "Low stock, urgent!"),
        (25, 15, "Half + half"),
    ]:
        if inv in df['inventory'].values and \
           days in df['days_left'].values:
            price = df[
                (df['inventory'] == inv) &
                (df['days_left'] == days)
            ]['best_price'].values

            if len(price) > 0:
                print(f"  ({inv:2d} inv, {days:2d} days) "
                      f"{desc:<28}: "
                      f"${price[0]}")

    return df


def compare_dqn_vs_ql_policy(
        dqn_agent,
        ql_agent,
        env: DynamicPricingEnv,
        save_path: str = '../results/dqn_vs_ql_policy.png'):
    """
    Compare DQN and Q-Learning policies.

    Parameters
    ----------
    dqn_agent : DQNAgent
        Trained DQN agent.
    ql_agent : QLearningAgent
        Trained Q-Learning agent.
    env : DynamicPricingEnv
        Environment.
    save_path : str
        Save path.
    """
    ql_prices = ql_agent.get_price_policy()

    # Get DQN prices
    dqn_prices = np.zeros(
        (env.max_inventory + 1,
         env.max_days + 1)
    )
    for inv in range(env.max_inventory + 1):
        for days in range(env.max_days + 1):
            norm = np.array([
                inv / env.max_inventory,
                days / env.max_days
            ], dtype=np.float32)
            tensor = torch.FloatTensor(
                norm
            ).unsqueeze(0)
            with torch.no_grad():
                q_vals = dqn_agent.online_net(
                    tensor
                ).numpy()[0]
            dqn_prices[inv, days] = (
                PRICE_LEVELS[q_vals.argmax()]
            )

    # Difference
    diff = dqn_prices - ql_prices

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    import seaborn as sns

    sns.heatmap(
        ql_prices, ax=axes[0],
        cmap='RdYlGn',
        xticklabels=5, yticklabels=5,
        cbar_kws={'label': 'Price ($)'}
    )
    axes[0].set_title(
        'Q-Learning Policy',
        fontweight='bold'
    )
    axes[0].set_xlabel('Days Left')
    axes[0].set_ylabel('Inventory')

    sns.heatmap(
        dqn_prices, ax=axes[1],
        cmap='RdYlGn',
        xticklabels=5, yticklabels=5,
        cbar_kws={'label': 'Price ($)'}
    )
    axes[1].set_title(
        'DQN Policy',
        fontweight='bold'
    )
    axes[1].set_xlabel('Days Left')
    axes[1].set_ylabel('Inventory')

    sns.heatmap(
        diff, ax=axes[2],
        cmap='RdBu',
        center=0,
        xticklabels=5, yticklabels=5,
        cbar_kws={'label': 'Price Diff ($)'}
    )
    axes[2].set_title(
        'Policy Difference\n(DQN - Q-Learning)',
        fontweight='bold'
    )
    axes[2].set_xlabel('Days Left')
    axes[2].set_ylabel('Inventory')

    plt.suptitle(
        'DQN vs Q-Learning Policy Comparison',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")

    return dqn_prices, ql_prices, diff


if __name__ == "__main__":
    print("✅ DQN insights module loaded!")