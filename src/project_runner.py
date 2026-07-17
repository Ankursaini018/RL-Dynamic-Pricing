"""
project_runner.py
=================
Master runner script for complete
Project 2 pipeline execution.

Run this to reproduce all results
from scratch!

Infotact DS/ML Internship — Project 2
"""

import numpy as np
import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = CURRENT_DIR

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv
from agents.dqn.dqn_agent import DQNAgent
from agents.dqn.dqn_utils import (
    save_dqn_model,
    TrainingMonitor
)
from agents.q_learning_agent import (
    QLearningAgent,
    QL_CONFIG
)
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)
from utils.evaluator import evaluate_agent
from config import DQN, EVAL

os.makedirs('../results', exist_ok=True)
os.makedirs('../models', exist_ok=True)


def run_complete_pipeline(
        quick_mode: bool = False):
    """
    Run complete Project 2 pipeline.

    Parameters
    ----------
    quick_mode : bool
        If True use fewer episodes
        for quick testing.
    """
    print("=" * 60)
    print("  RL DYNAMIC PRICING")
    print("  COMPLETE PIPELINE")
    print("  Infotact DS/ML Internship 2026")
    print("=" * 60)

    # Config
    dqn_eps = 500 if quick_mode else 2000
    ql_eps  = 1000 if quick_mode else 3000
    n_eval  = 50 if quick_mode else 100
    n_sim   = 100 if quick_mode else 1000

    env = DynamicPricingEnv()

    # ── Step 1: Baselines ──
    print("\n[STEP 1] Evaluating Baselines...")
    baselines = {
        'Fixed Price'  : FixedPriceAgent(env),
        'Time Based'   : TimedPricingAgent(env),
        'Demand Based' : DemandBasedAgent(env),
        'Linear Decay' : LinearDecayAgent(env),
    }

    baseline_results = {}
    for name, agent in baselines.items():
        df = evaluate_agent(agent, n_eval)
        baseline_results[name] = (
            df['total_revenue'].mean()
        )
        print(f"  {name:<15}: "
              f"${baseline_results[name]:.0f}")

    best_bl = max(baseline_results.values())

    # ── Step 2: Q-Learning ──
    print(f"\n[STEP 2] Training Q-Learning "
          f"({ql_eps} episodes)...")
    ql_agent = QLearningAgent(env, QL_CONFIG)
    ql_agent.train(
        n_episodes=ql_eps,
        verbose=False
    )
    ql_eval = ql_agent.evaluate(n_eval)
    print(f"  Q-Learning: "
          f"${ql_eval['mean_revenue']:.0f}")

    # ── Step 3: DQN ──
    print(f"\n[STEP 3] Training DQN "
          f"({dqn_eps} episodes)...")
    monitor   = TrainingMonitor(print_every=200)
    dqn_agent = DQNAgent(env, DQN)
    rewards   = dqn_agent.train(
        n_episodes=dqn_eps,
        verbose=True
    )
    dqn_eval = dqn_agent.evaluate(n_eval)
    monitor.print_summary()

    # ── Step 4: Save Model ──
    print("\n[STEP 4] Saving DQN model...")
    save_dqn_model(dqn_agent)

    # ── Step 5: Final Comparison ──
    print("\n[STEP 5] Final Results...")
    all_results = {
        **baseline_results,
        'Q-Learning': ql_eval['mean_revenue'],
        'DQN 🤖'    : dqn_eval['mean_revenue']
    }

    ranked = sorted(
        all_results.items(),
        key=lambda x: x[1],
        reverse=True
    )

    medals = ['🥇', '🥈', '🥉',
              '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    print("\n" + "=" * 60)
    print("  FINAL RANKINGS")
    print("=" * 60)
    for i, (name, rev) in enumerate(ranked):
        print(f"  {medals[i]} {name:<15}: ${rev:.0f}")

    dqn_rev = dqn_eval['mean_revenue']
    imp = (dqn_rev - best_bl) / best_bl * 100

    print(f"\n  DQN vs Best Baseline: {imp:+.1f}%")
    if imp > 0:
        print(f"  ✅ DQN WINS!")
    else:
        print(f"  ⚠️  Need more training!")

    # Save final results
    final = {
        'rankings'    : [
            {'rank': i+1, 'agent': n, 'revenue': float(r)}
            for i, (n, r) in enumerate(ranked)
        ],
        'dqn_improvement': float(imp),
        'quick_mode'      : quick_mode
    }
    with open('../results/final_results.json',
              'w') as f:
        json.dump(final, f, indent=4)
    print("\n✅ Final results saved!")
    print("=" * 60)

    return all_results, dqn_agent


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--quick', action='store_true',
        help='Quick mode with fewer episodes'
    )
    args = parser.parse_args()

    results, agent = run_complete_pipeline(
        quick_mode=args.quick
    )