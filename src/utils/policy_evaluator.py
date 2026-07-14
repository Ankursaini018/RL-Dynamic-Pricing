"""
policy_evaluator.py
===================
Comprehensive policy evaluation for
DQN agent across different scenarios.

Infotact DS/ML Internship — Project 2
Week 2 : Policy Evaluation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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


def evaluate_across_scenarios(
        agent,
        scenarios: list = None) -> pd.DataFrame:
    """
    Evaluate agent across different
    inventory and day scenarios.

    Parameters
    ----------
    agent : DQNAgent
        Trained agent.
    scenarios : list
        List of (max_inventory, max_days) tuples.

    Returns
    -------
    pd.DataFrame
        Results for each scenario.
    """
    if scenarios is None:
        scenarios = [
            (50, 30, 'Standard'),
            (100, 30, 'Large Inventory'),
            (50, 60, 'Long Season'),
            (20, 15, 'Small + Short'),
            (50, 7,  'Last Week'),
        ]

    print("=" * 55)
    print("  SCENARIO-BASED EVALUATION")
    print("=" * 55)

    rows = []
    for max_inv, max_days, label in scenarios:
        env = DynamicPricingEnv(
            max_inventory=max_inv,
            max_days=max_days
        )

        revenues = []
        for ep in range(100):
            state, _ = env.reset(seed=ep)
            total_rev = 0
            done      = False

            while not done:
                action = agent.select_action(
                    state, training=False
                )
                state, reward, term, trunc, _ = (
                    env.step(action)
                )
                done = term or trunc
                total_rev += max(0, reward)

            revenues.append(total_rev)

        rows.append({
            'Scenario'     : label,
            'Max Inventory': max_inv,
            'Max Days'     : max_days,
            'Mean Revenue' : np.mean(revenues),
            'Std Revenue'  : np.std(revenues),
            'Per Ticket'   : (
                np.mean(revenues) / max_inv
            )
        })

        print(f"\n  {label}:")
        print(f"  ({max_inv} inv, {max_days} days)")
        print(f"  Mean Revenue: "
              f"${np.mean(revenues):.0f}")

    df = pd.DataFrame(rows)
    print(f"\n✅ Scenario evaluation complete!")
    return df


def evaluate_robustness(
        agent,
        env: DynamicPricingEnv,
        n_episodes: int = 200) -> dict:
    """
    Evaluate agent robustness and consistency.

    Parameters
    ----------
    agent : DQNAgent
        Trained agent.
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Evaluation episodes.

    Returns
    -------
    dict
        Robustness metrics.
    """
    revenues = []

    for ep in range(n_episodes):
        state, _ = env.reset(seed=ep)
        total_rev = 0
        done      = False

        while not done:
            action = agent.select_action(
                state, training=False
            )
            state, reward, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc
            total_rev += max(0, reward)

        revenues.append(total_rev)

    revenues = np.array(revenues)

    metrics = {
        'mean'          : revenues.mean(),
        'std'           : revenues.std(),
        'cv'            : revenues.std() /
                          revenues.mean(),
        'min'           : revenues.min(),
        'max'           : revenues.max(),
        'p10'           : np.percentile(revenues, 10),
        'p25'           : np.percentile(revenues, 25),
        'p75'           : np.percentile(revenues, 75),
        'p90'           : np.percentile(revenues, 90),
        'consistency'   : 1 - (revenues.std() /
                               revenues.mean()),
    }

    print("=" * 55)
    print("  ROBUSTNESS METRICS")
    print("=" * 55)
    print(f"  Mean Revenue    : ${metrics['mean']:.0f}")
    print(f"  Std Revenue     : ±${metrics['std']:.0f}")
    print(f"  CV (lower=better): {metrics['cv']:.3f}")
    print(f"  Min Revenue     : ${metrics['min']:.0f}")
    print(f"  Max Revenue     : ${metrics['max']:.0f}")
    print(f"  10th Percentile : ${metrics['p10']:.0f}")
    print(f"  90th Percentile : ${metrics['p90']:.0f}")
    print(f"  Consistency     : "
          f"{metrics['consistency']*100:.1f}%")

    return metrics


if __name__ == "__main__":
    print("✅ Policy evaluator loaded!")