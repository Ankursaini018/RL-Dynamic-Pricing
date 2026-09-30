"""
demand_analyzer.py
==================
Analyzes the stochastic demand function
to understand market dynamics.

Infotact DS/ML Internship — Project 2
Week 1 : Demand Analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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


def analyze_demand(save_dir: str = '../results/'):
    """
    Comprehensive demand function analysis.

    Parameters
    ----------
    save_dir : str
        Directory to save plots.
    """
    env = DynamicPricingEnv()

    print("=" * 50)
    print("  DEMAND FUNCTION ANALYSIS")
    print("=" * 50)

    # Simulate demand at each price
    n_simulations = 1000
    results = []

    for price_idx, price in enumerate(PRICE_LEVELS):
        for days in [5, 15, 30]:
            purchases = []
            for _ in range(n_simulations):
                bought = (
    np.random.random()
    < env._get_demand_probability(
        price, days
    )
)
                purchases.append(bought)

            results.append({
                'price'         : price,
                'days_left'     : days,
                'purchase_rate' : np.mean(purchases),
                'expected_rev'  : (
                    price * np.mean(purchases)
                )
            })

    df = pd.DataFrame(results)

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for days in [5, 15, 30]:
        subset = df[df['days_left'] == days]
        axes[0].plot(
            subset['price'],
            subset['purchase_rate'],
            marker='o',
            linewidth=2,
            label=f'{days} days left'
        )

    axes[0].set_title(
        'Purchase Rate vs Price',
        fontweight='bold'
    )
    axes[0].set_xlabel('Price ($)')
    axes[0].set_ylabel('Purchase Rate')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    for days in [5, 15, 30]:
        subset = df[df['days_left'] == days]
        axes[1].plot(
            subset['price'],
            subset['expected_rev'],
            marker='s',
            linewidth=2,
            label=f'{days} days left'
        )

    axes[1].set_title(
        'Expected Revenue per Step vs Price',
        fontweight='bold'
    )
    axes[1].set_xlabel('Price ($)')
    axes[1].set_ylabel('Expected Revenue ($)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(
        'Demand Function Analysis\n'
        'Market Dynamics',
        fontsize=13,
        fontweight='bold'
    )

    plt.tight_layout()

    # --------------------------------------------------
    # Create results directory automatically
    # --------------------------------------------------

    PROJECT_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    SAVE_PATH = os.path.join(
        RESULTS_DIR,
        "demand_analysis.png"
    )

    plt.savefig(
        SAVE_PATH,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()

    print(f"✅ Saved: {SAVE_PATH}")

    # Print optimal prices
    print("\n=== OPTIMAL PRICE BY DAYS LEFT ===")
    for days in [30, 20, 10, 5, 1]:

        best = df[
            df['days_left'] == min(
                [5, 15, 30],
                key=lambda x: abs(x - days)
            )
        ].nlargest(1, 'expected_rev')

        print(
            f"  {days} days: "
            f"Best price ≈ "
            f"${best['price'].values[0]}"
        )

    return df


if __name__ == "__main__":
    df = analyze_demand()
    print("\n✅ Demand analysis complete!")