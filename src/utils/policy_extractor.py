"""
policy_extractor.py
===================
Extracts and saves the learned policy
from Q-Learning agent for later use.

Infotact DS/ML Internship — Project 2
Week 1 : Policy Extraction
"""

import numpy as np
import pandas as pd
import json
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


def extract_policy_table(
        agent: QLearningAgent) -> pd.DataFrame:
    """
    Extract policy as readable DataFrame.

    Parameters
    ----------
    agent : QLearningAgent
        Trained agent.

    Returns
    -------
    pd.DataFrame
        Policy table with readable format.
    """
    prices = agent.get_price_policy()
    rows = []

    for inv in range(0, agent.env.max_inventory + 1, 5):
        for days in range(0, agent.env.max_days + 1, 5):
            rows.append({
                'Inventory': inv,
                'Days Left': days,
                'Optimal Price': prices[inv, days],
                'Category': _categorize_state(
                    inv,
                    days,
                    agent.env.max_inventory,
                    agent.env.max_days
                )
            })

    return pd.DataFrame(rows)


def _categorize_state(
        inv: int,
        days: int,
        max_inv: int,
        max_days: int) -> str:
    """
    Categorize state for analysis.
    """
    inv_pct = inv / max_inv
    days_pct = days / max_days

    if inv_pct > 0.7 and days_pct > 0.7:
        return 'Early + Full'
    elif inv_pct > 0.7 and days_pct <= 0.3:
        return 'Urgent + Full'
    elif inv_pct <= 0.3 and days_pct > 0.7:
        return 'Early + Low Stock'
    elif inv_pct <= 0.3 and days_pct <= 0.3:
        return 'Urgent + Low Stock'
    else:
        return 'Mid State'


def save_policy_summary(
        agent: QLearningAgent):
    """
    Save policy summary as JSON.

    Parameters
    ----------
    agent : QLearningAgent
        Trained agent.
    """

    # --------------------------------------------------
    # Create results directory automatically
    # --------------------------------------------------

    PROJECT_ROOT = os.path.abspath(
        os.path.join(CURRENT_DIR, "..", "..")
    )

    RESULTS_DIR = os.path.join(
        PROJECT_ROOT,
        "results"
    )

    os.makedirs(RESULTS_DIR, exist_ok=True)

    SAVE_PATH = os.path.join(
        RESULTS_DIR,
        "policy_summary.json"
    )

    prices = agent.get_price_policy()

    summary = {
        "agent_type": "Q-Learning",
        "training_episodes": len(agent.episode_rewards),
        "final_epsilon": float(agent.epsilon),
        "mean_revenue_last100": float(
            np.mean(agent.episode_rewards[-100:])
        ),
        "q_table_shape": list(agent.q_table.shape),
        "price_levels": PRICE_LEVELS,
        "policy_insights": {
            "early_avg_price": float(
                prices[:, 20:].mean()
            ),
            "late_avg_price": float(
                prices[:, :5].mean()
            ),
            "high_inv_price": float(
                prices[40:, :].mean()
            ),
            "low_inv_price": float(
                prices[:10, :].mean()
            ),
            "most_used_price": int(
                pd.Series(
                    prices.flatten()
                ).mode()[0]
            )
        }
    }

    with open(SAVE_PATH, "w") as f:
        json.dump(
            summary,
            f,
            indent=4
        )

    print(f"✅ Saved: {SAVE_PATH}")

    print("\nPolicy Insights:")
    for k, v in summary["policy_insights"].items():
        print(f"  {k:<25}: {v}")

    return summary


if __name__ == "__main__":

    env = DynamicPricingEnv()

    agent = QLearningAgent(env)

    agent.train(
        n_episodes=2000,
        verbose=False
    )

    print("\nExtracting policy...")

    policy_df = extract_policy_table(agent)

    print(policy_df.head(20))

    print("\nSaving policy summary...")

    summary = save_policy_summary(agent)

    print("\n✅ Policy extraction complete!")