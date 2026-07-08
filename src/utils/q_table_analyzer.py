"""
q_table_analyzer.py
===================
Deep analysis of trained Q-table.
Understands what the agent learned
about optimal pricing strategy.

Infotact DS/ML Internship — Project 2
Week 1 : Q-Table Analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# --------------------------------------------------
# Add project src directory to Python path
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)
from agents.q_learning_agent import QLearningAgent


# ─────────────────────────────────────────
# Q-TABLE STATISTICS
# ─────────────────────────────────────────

def analyze_q_table(agent: QLearningAgent) -> dict:
    """
    Analyze Q-table statistics and patterns.

    Parameters
    ----------
    agent : QLearningAgent
        Trained Q-Learning agent.

    Returns
    -------
    dict
        Analysis results.
    """
    q_table = agent.q_table
    policy  = agent.get_policy()
    prices  = agent.get_price_policy()

    print("=" * 55)
    print("  Q-TABLE ANALYSIS")
    print("=" * 55)

    # Basic stats
    print(f"\n  Q-table shape : {q_table.shape}")
    print(f"  Total states  : "
          f"{q_table.shape[0] * q_table.shape[1]}")
    print(f"  Total entries : {q_table.size}")
    print(f"\n  Q-value stats :")
    print(f"  Min Q    : {q_table.min():.4f}")
    print(f"  Max Q    : {q_table.max():.4f}")
    print(f"  Mean Q   : {q_table.mean():.4f}")
    print(f"  Std Q    : {q_table.std():.4f}")

    # Price distribution in policy
    print(f"\n  Policy Price Distribution:")
    for price in PRICE_LEVELS:
        count = (prices == price).sum()
        pct   = count / prices.size * 100
        bar   = '█' * int(pct / 2)
        print(f"  ${price:<5}: {bar:<25} "
              f"{count:4d} states ({pct:.1f}%)")

    # Key state analysis
    print(f"\n  Key State Optimal Prices:")
    print(f"  {'State':<35} Price")
    print("  " + "─" * 45)

    key_states = [
        (50, 30, "Full stock, lots of time"),
        (50, 15, "Full stock, half time"),
        (50, 5,  "Full stock, urgent!"),
        (25, 30, "Half stock, lots of time"),
        (25, 15, "Half stock, half time"),
        (25, 5,  "Half stock, urgent!"),
        (10, 30, "Low stock, lots of time"),
        (10, 10, "Low stock, some time"),
        (10, 3,  "Low stock, very urgent!"),
        (5,  2,  "Almost sold out!"),
        (1,  1,  "Last ticket, last day!"),
    ]

    insights = []
    for inv, days, desc in key_states:
        if inv <= agent.env.max_inventory and \
           days <= agent.env.max_days:
            price = prices[inv, days]
            print(f"  ({inv:2d} inv, {days:2d} days) "
                  f"{desc:<22}: ${price}")
            insights.append({
                'inventory' : inv,
                'days_left' : days,
                'description': desc,
                'opt_price'  : price
            })

    return {
        'q_table'     : q_table,
        'policy'      : policy,
        'prices'      : prices,
        'insights'    : pd.DataFrame(insights)
    }


# ─────────────────────────────────────────
# POLICY HEATMAPS
# ─────────────────────────────────────────

def plot_policy_heatmaps(
        agent: QLearningAgent,
        save_path: str = '../results/policy_analysis.png'):
    """
    Plot detailed policy analysis heatmaps.

    Parameters
    ----------
    agent : QLearningAgent
        Trained agent.
    save_path : str
        Save path.
    """
    prices = agent.get_price_policy()
    q_table = agent.q_table

    fig, axes = plt.subplots(2, 2, figsize=(18, 14))

    # ── Plot 1: Full Policy Heatmap ──
    sns.heatmap(
        prices,
        ax=axes[0, 0],
        cmap='RdYlGn',
        cbar_kws={'label': 'Optimal Price ($)'},
        xticklabels=5,
        yticklabels=5
    )
    axes[0, 0].set_title(
        'Learned Policy — Optimal Price\n'
        'by (Inventory, Days Left)',
        fontweight='bold',
        fontsize=12
    )
    axes[0, 0].set_xlabel('Days Until Departure')
    axes[0, 0].set_ylabel('Remaining Inventory')

    # ── Plot 2: Max Q-Value Heatmap ──
    max_q = q_table.max(axis=2)
    sns.heatmap(
        max_q,
        ax=axes[0, 1],
        cmap='YlOrRd',
        cbar_kws={'label': 'Max Q-Value'},
        xticklabels=5,
        yticklabels=5
    )
    axes[0, 1].set_title(
        'Max Q-Value by State\n'
        '(Confidence of Agent)',
        fontweight='bold',
        fontsize=12
    )
    axes[0, 1].set_xlabel('Days Until Departure')
    axes[0, 1].set_ylabel('Remaining Inventory')

    # ── Plot 3: Price by Days (avg over inv) ──
    avg_price_by_days = prices.mean(axis=0)
    axes[1, 0].plot(
        range(agent.env.max_days + 1),
        avg_price_by_days,
        color='steelblue',
        linewidth=2.5,
        marker='o',
        markersize=4
    )
    axes[1, 0].set_title(
        'Average Optimal Price\nvs Days Until Departure',
        fontweight='bold',
        fontsize=12
    )
    axes[1, 0].set_xlabel('Days Until Departure')
    axes[1, 0].set_ylabel('Average Optimal Price ($)')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axvline(
        x=10,
        color='red',
        linestyle='--',
        label='10-day mark'
    )
    axes[1, 0].legend()

    # ── Plot 4: Price by Inventory (avg over days) ──
    avg_price_by_inv = prices.mean(axis=1)
    axes[1, 1].plot(
        range(agent.env.max_inventory + 1),
        avg_price_by_inv,
        color='coral',
        linewidth=2.5,
        marker='s',
        markersize=4
    )
    axes[1, 1].set_title(
        'Average Optimal Price\nvs Remaining Inventory',
        fontweight='bold',
        fontsize=12
    )
    axes[1, 1].set_xlabel('Remaining Inventory')
    axes[1, 1].set_ylabel('Average Optimal Price ($)')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axvline(
        x=25,
        color='red',
        linestyle='--',
        label='Half inventory'
    )
    axes[1, 1].legend()

    plt.suptitle(
        'Q-Learning Policy Deep Analysis\n'
        'Understanding What the Agent Learned',
        fontsize=14,
        fontweight='bold'
    )

    plt.tight_layout()

    # --------------------------------------------------
    # Create results directory automatically
    # --------------------------------------------------

    PROJECT_ROOT = os.path.abspath(
        os.path.join(CURRENT_DIR, "..", "..")
    )

    RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    SAVE_PATH = os.path.join(
        RESULTS_DIR,
        "policy_analysis.png"
    )

    plt.savefig(
        SAVE_PATH,
        bbox_inches="tight",
        dpi=150
    )

    print(f"✅ Saved: {SAVE_PATH}")

    plt.show()
# ─────────────────────────────────────────
# BEHAVIOR ANALYSIS
# ─────────────────────────────────────────

def analyze_learned_behavior(
        agent: QLearningAgent):
    """
    Analyze if agent learned smart behaviors.

    Checks:
    1. Does agent lower price near deadline?
    2. Does agent raise price for low inventory?
    3. Does agent use premium pricing early?

    Parameters
    ----------
    agent : QLearningAgent
        Trained agent.
    """
    prices = agent.get_price_policy()

    print("\n" + "=" * 55)
    print("  LEARNED BEHAVIOR ANALYSIS")
    print("=" * 55)

    # Check 1: Price near deadline
    early_price = prices[:, 25:30].mean()
    late_price  = prices[:, 0:5].mean()
    print(f"\n  [1] Deadline Pricing:")
    print(f"      Early (25-30 days): ${early_price:.0f}")
    print(f"      Late  (0-5 days)  : ${late_price:.0f}")
    if late_price < early_price:
        print(f"      ✅ Agent learned to DISCOUNT "
              f"near deadline!")
    else:
        print(f"      ⚠️  Agent not discounting "
              f"near deadline")

    # Check 2: Scarcity pricing
    high_inv_price = prices[40:50, :].mean()
    low_inv_price  = prices[0:10, :].mean()
    print(f"\n  [2] Scarcity Pricing:")
    print(f"      High inventory (40-50): "
          f"${high_inv_price:.0f}")
    print(f"      Low inventory  (0-10) : "
          f"${low_inv_price:.0f}")
    if low_inv_price > high_inv_price:
        print(f"      ✅ Agent learned SCARCITY "
              f"premium pricing!")
    else:
        print(f"      ⚠️  Agent not using scarcity "
              f"pricing")

    # Check 3: Early premium
    early_avg = prices[:, 20:30].mean()
    mid_avg   = prices[:, 10:20].mean()
    late_avg  = prices[:, 0:10].mean()
    print(f"\n  [3] Price Trajectory Pattern:")
    print(f"      Early (20-30 days): ${early_avg:.0f}")
    print(f"      Mid   (10-20 days): ${mid_avg:.0f}")
    print(f"      Late  (0-10 days) : ${late_avg:.0f}")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    env   = DynamicPricingEnv()
    agent = QLearningAgent(env)
    agent.train(n_episodes=2000, verbose=False)

    results = analyze_q_table(agent)
    plot_policy_heatmaps(agent)
    analyze_learned_behavior(agent)
    print("\n✅ Q-table analysis complete!")