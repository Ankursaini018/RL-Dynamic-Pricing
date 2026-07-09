"""
results_consolidator.py
========================
Consolidates all Week 1 results
into single comparison report.

Infotact DS/ML Internship — Project 2
Week 1 : Results Consolidation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)
from agents.q_learning_agent import (
    QLearningAgent,
    QL_CONFIG
)
from utils.evaluator import evaluate_agent


def consolidate_week1_results(
        n_episodes: int = 100) -> pd.DataFrame:
    """
    Run all agents and consolidate results.

    Parameters
    ----------
    n_episodes : int
        Evaluation episodes.

    Returns
    -------
    pd.DataFrame
        Consolidated results.
    """
    print("=" * 55)
    print("  WEEK 1 RESULTS CONSOLIDATION")
    print("=" * 55)

    env = DynamicPricingEnv()

    # Train Q-Learning
    print("\n[1] Training Q-Learning...")
    ql = QLearningAgent(env, QL_CONFIG)
    ql.train(n_episodes=3000, verbose=False)

    # All agents
    agents = [
        FixedPriceAgent(env),
        TimedPricingAgent(env),
        DemandBasedAgent(env),
        LinearDecayAgent(env),
        ql
    ]

    # Evaluate all
    print("\n[2] Evaluating all agents...")
    rows = []
    for agent in agents:
        name = getattr(agent, 'name', 'Q-Learning')
        print(f"  Evaluating: {name}...")

        revenues = []
        sold_list = []

        for ep in range(n_episodes):
            if hasattr(agent, 'run_episode'):
                r = agent.run_episode(seed=ep)
                revenues.append(r['total_revenue'])
                sold_list.append(r['total_sold'])
            else:
                state, _ = env.reset(seed=ep)
                total_rev = 0
                total_sold = 0
                done = False
                while not done:
                    action = agent.select_action(
                        state, training=False
                    )
                    state, reward, term, trunc, info = (
                        env.step(action)
                    )
                    done = term or trunc
                    total_rev += max(0, reward)
                    if info['bought']:
                        total_sold += 1
                revenues.append(total_rev)
                sold_list.append(total_sold)

        rows.append({
            'Agent'        : name,
            'Type'         : 'RL' if name == 'Q-Learning'
                             else 'Baseline',
            'Mean Revenue' : np.mean(revenues),
            'Std Revenue'  : np.std(revenues),
            'Max Revenue'  : np.max(revenues),
            'Min Revenue'  : np.min(revenues),
            'Mean Sold'    : np.mean(sold_list),
            'Sell Through' : np.mean(sold_list) /
                             env.max_inventory * 100
        })

    df = pd.DataFrame(rows).sort_values(
        'Mean Revenue', ascending=False
    ).reset_index(drop=True)

    # Print results
    print("\n" + "=" * 55)
    print("  CONSOLIDATED RESULTS")
    print("=" * 55)
    for _, row in df.iterrows():
        tag = '🤖' if row['Type'] == 'RL' else '📊'
        print(f"  {tag} {row['Agent']:<15}: "
              f"${row['Mean Revenue']:.0f} "
              f"± ${row['Std Revenue']:.0f}")

    # Save
    os.makedirs('../results', exist_ok=True)
    df.to_csv(
        '../results/week1_consolidated.csv',
        index=False
    )
    print("\n✅ Saved: results/week1_consolidated.csv")

    return df


if __name__ == "__main__":
    df = consolidate_week1_results()
    print(f"\n✅ Week 1 best agent: "
          f"{df.iloc[0]['Agent']} "
          f"(${df.iloc[0]['Mean Revenue']:.0f})")