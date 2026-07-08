"""
week1_summary.py
================
Week 1 complete summary for
RL Dynamic Pricing project.

Infotact DS/ML Internship — Project 2
Week 1 : Summary
"""

import numpy as np
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

# --------------------------------------------------
# Results directory
# --------------------------------------------------

PROJECT_ROOT = os.getcwd()

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def generate_week1_summary():
    """
    Generate complete Week 1 summary.
    """

    print("=" * 60)
    print("  WEEK 1 SUMMARY REPORT")
    print("  RL Dynamic Pricing — Project 2")
    print("=" * 60)

    env = DynamicPricingEnv()

    # --------------------------------------------------
    # Baseline Results
    # --------------------------------------------------

    print("\n[1] Evaluating baseline agents...")

    baselines = {
        "Fixed Price": FixedPriceAgent(env),
        "Time Based": TimedPricingAgent(env),
        "Demand Based": DemandBasedAgent(env),
        "Linear Decay": LinearDecayAgent(env)
    }

    baseline_results = {}

    for name, agent in baselines.items():

        df = evaluate_agent(
            agent,
            n_episodes=100
        )

        baseline_results[name] = {
            "mean_revenue": float(df["total_revenue"].mean()),
            "std_revenue": float(df["total_revenue"].std()),
            "mean_sold": float(df["total_sold"].mean())
        }

    best_baseline_name = max(
        baseline_results,
        key=lambda k: baseline_results[k]["mean_revenue"]
    )

    best_baseline_rev = baseline_results[
        best_baseline_name
    ]["mean_revenue"]

    # --------------------------------------------------
    # Q-Learning
    # --------------------------------------------------

    print("\n[2] Training Q-Learning agent...")

    ql_agent = QLearningAgent(env, QL_CONFIG)

    ql_agent.train(
        n_episodes=5000,
        verbose=False
    )

    ql_eval = ql_agent.evaluate(
        n_episodes=100
    )

    improvement = (
        (ql_eval["mean_revenue"] - best_baseline_rev)
        / best_baseline_rev
        * 100
    )

    # --------------------------------------------------
    # Print Summary
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("  WEEK 1 COMPLETE RESULTS")
    print("=" * 60)

    print("\nBASELINE AGENTS")

    for name, res in baseline_results.items():
        print(f"{name:<15}: ${res['mean_revenue']:.0f}")

    print("\nQ-LEARNING")

    print(
        f"Revenue : "
        f"${ql_eval['mean_revenue']:.0f} ± "
        f"${ql_eval['std_revenue']:.0f}"
    )

    print(f"vs Best : {improvement:+.1f}%")

    print("\nENVIRONMENT")

    print(f"Max Inventory : {env.max_inventory}")
    print(f"Max Days      : {env.max_days}")
    print(f"Price Levels  : {env.price_levels}")

    print(
        f"State Space   : "
        f"{(env.max_inventory+1)*(env.max_days+1)}"
    )

    # --------------------------------------------------
    # Save Summary
    # --------------------------------------------------

    summary = {
    "week": 1,
    "project": "RL Dynamic Pricing",

    "environment": {
        "max_inventory": int(env.max_inventory),
        "max_days": int(env.max_days),
        "price_levels": [int(x) for x in env.price_levels],
        "state_space": int(
            (env.max_inventory + 1) *
            (env.max_days + 1)
        )
    },

    "baseline_results": {
        name: {
            "mean_revenue": float(res["mean_revenue"]),
            "std_revenue": float(res["std_revenue"]),
            "mean_sold": float(res["mean_sold"])
        }
        for name, res in baseline_results.items()
    },

    "q_learning": {
        "mean_revenue": float(ql_eval["mean_revenue"]),
        "std_revenue": float(ql_eval["std_revenue"]),
        "improvement_pct": float(improvement),
        "beats_baseline": bool(improvement > 0),

        "config": {
            k: (
                int(v) if isinstance(v, (np.integer, int))
                else float(v) if isinstance(v, (np.floating, float))
                else bool(v) if isinstance(v, (np.bool_, bool))
                else v
            )
            for k, v in QL_CONFIG.items()
        }
    },

    "week1_status": {
        "mdp_designed": True,
        "gym_env_built": True,
        "demand_fn_done": True,
        "baselines_done": True,
        "q_learning_done": True,
        "q_table_analyzed": True
    }
}

    SAVE_PATH = os.path.join(
        RESULTS_DIR,
        "week1_summary.json"
    )

    with open(SAVE_PATH, "w") as f:
        json.dump(summary, f, indent=4, default=str)

    print(f"\n✅ Summary saved: {SAVE_PATH}")

    print("=" * 60)
    print(" WEEK 2 PREVIEW: Deep Q-Network (DQN)")
    print(" → Neural Network replaces Q-table")
    print(" → Handles continuous state spaces")
    print(" → Experience replay for stability")
    print(" → Epsilon-greedy exploration")
    print("=" * 60)

    return summary


if __name__ == "__main__":
    summary = generate_week1_summary()