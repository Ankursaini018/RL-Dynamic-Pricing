"""
project_runner.py (UPDATED)
============================
Master runner with PPO added.
Runs complete pipeline:
Baselines → Q-Learning → DQN → PPO

Infotact DS/ML Internship — Project 2
"""

import numpy as np
import json
import os
import sys
sys.path.append('../')

from environment.pricing_env import DynamicPricingEnv
from agents.ppo.ppo_agent import PPOAgent
from agents.ppo.ppo_utils import (
    save_ppo_model,
    PPOMonitor
)
from agents.dqn.dqn_agent import DQNAgent
from agents.dqn.dqn_utils import save_dqn_model
from agents.q_learning_agent import (
    QLearningAgent, QL_CONFIG
)
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)
from utils.evaluator import evaluate_agent
from training.config_manager import (
    BEST_PPO_CONFIG,
    BEST_DQN_CONFIG
)

os.makedirs('../results', exist_ok=True)
os.makedirs('../models', exist_ok=True)


def run_complete_pipeline(
        quick_mode: bool = False):
    """
    Run complete Project 2 pipeline.
    Includes PPO as the final agent.

    Parameters
    ----------
    quick_mode : bool
        Fewer episodes for quick test.
    """
    print("=" * 60)
    print("  RL DYNAMIC PRICING")
    print("  COMPLETE PIPELINE v2.0")
    print("  Now with PPO! 🚀")
    print("  Infotact DS/ML Internship 2026")
    print("=" * 60)

    ppo_eps = 300  if quick_mode else 2000
    dqn_eps = 300  if quick_mode else 2000
    ql_eps  = 500  if quick_mode else 3000
    n_eval  = 20   if quick_mode else 100

    env = DynamicPricingEnv()

    # ── Step 1: Baselines ──
    print("\n[STEP 1] Evaluating Baselines...")
    baselines = {
        'Fixed Price'  : FixedPriceAgent(env),
        'Time Based'   : TimedPricingAgent(env),
        'Demand Based' : DemandBasedAgent(env),
        'Linear Decay' : LinearDecayAgent(env),
    }
    bl_results = {}
    for name, agent in baselines.items():
        df = evaluate_agent(agent, n_eval)
        bl_results[name] = (
            df['total_revenue'].mean()
        )
        print(f"  {name:<15}: "
              f"${bl_results[name]:.0f}")

    best_bl = max(bl_results.values())

    # ── Step 2: Q-Learning ──
    print(f"\n[STEP 2] Q-Learning "
          f"({ql_eps} eps)...")
    ql = QLearningAgent(env, QL_CONFIG)
    ql.train(n_episodes=ql_eps, verbose=False)
    ql_eval = ql.evaluate(n_eval)
    print(f"  Q-Learning: "
          f"${ql_eval['mean_revenue']:.0f}")

    # ── Step 3: DQN ──
    print(f"\n[STEP 3] DQN ({dqn_eps} eps)...")
    dqn = DQNAgent(env, BEST_DQN_CONFIG)
    dqn.train(n_episodes=dqn_eps, verbose=False)
    dqn_eval = dqn.evaluate(n_eval)
    print(f"  DQN: ${dqn_eval['mean_revenue']:.0f}")
    save_dqn_model(dqn)

    # ── Step 4: PPO ──
    print(f"\n[STEP 4] PPO ({ppo_eps} eps)...")
    monitor = PPOMonitor(print_every=200)
    ppo     = PPOAgent(env, BEST_PPO_CONFIG)
    ppo.train(n_episodes=ppo_eps, verbose=True)
    ppo_eval = ppo.evaluate(n_eval)
    print(f"  PPO: ${ppo_eval['mean_revenue']:.0f}")
    save_ppo_model(ppo)
    monitor.print_summary()

    # ── Step 5: Rankings ──
    all_results = {
        **bl_results,
        'Q-Learning' : ql_eval['mean_revenue'],
        'DQN'        : dqn_eval['mean_revenue'],
        'PPO 🏆'     : ppo_eval['mean_revenue'],
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

    ppo_rev = ppo_eval['mean_revenue']
    imp_bl  = (ppo_rev - best_bl) / best_bl * 100
    imp_dqn = (
        ppo_rev - dqn_eval['mean_revenue']
    ) / dqn_eval['mean_revenue'] * 100

    print(f"\n  PPO vs Best Baseline: {imp_bl:+.1f}%")
    print(f"  PPO vs DQN          : {imp_dqn:+.1f}%")

    if imp_bl > 0 and imp_dqn > 0:
        print(f"\n  ✅ PPO WINS! Best overall agent!")
    elif imp_bl > 0:
        print(f"\n  ✅ PPO beats baselines!")

    # Save results
    final = {
        'rankings'      : [
            {
                'rank'   : i+1,
                'agent'  : n,
                'revenue': float(r)
            }
            for i, (n, r) in enumerate(ranked)
        ],
        'ppo_vs_baseline': float(imp_bl),
        'ppo_vs_dqn'     : float(imp_dqn),
        'quick_mode'      : quick_mode
    }

    with open('../results/final_results.json', 'w') as f:
        json.dump(
            final,
            f,
            indent=4,
            default=lambda x: (
                int(x) if isinstance(x, np.integer)
                else float(x) if isinstance(x, np.floating)
                else bool(x) if isinstance(x, np.bool_)
                else list(x) if isinstance(x, dict.keys)
                else str(x)
            )
        )

    print("\n✅ Final results saved!")
    print("=" * 60)

    return all_results, ppo, dqn, ql


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick mode'
    )
    args = parser.parse_args()

    results, ppo, dqn, ql = (
        run_complete_pipeline(
            quick_mode=args.quick
        )
    )