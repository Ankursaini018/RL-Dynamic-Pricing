"""
final_verification.py
=====================
Complete final verification of
Project 2 before submission.

Runs all checks and generates
final status report.

Infotact DS/ML Internship — Project 2
Week 4 : Final Verification

FIX APPLIED:
- Uses Path(__file__).resolve() for correct paths
- Saves verification report to correct results folder
- Handles both results/ and notebooks/results/ locations
"""

import numpy as np
import json
import os
from pathlib import Path
import sys

# ─────────────────────────────────────────
# GET PROJECT ROOT DYNAMICALLY
# ─────────────────────────────────────────
# This file lives at:
#   <PROJECT_ROOT>/src/final_verification.py
#
# So going 1 level up gives PROJECT_ROOT:
#   Path(__file__).resolve().parent   = src/
#   Path(__file__).resolve().parents[1] = PROJECT_ROOT ✅

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT     = PROJECT_ROOT / 'src'

# Add src to path for imports
sys.path.insert(0, str(SRC_ROOT))

# ─────────────────────────────────────────
# DETECT RESULTS FOLDER
# ─────────────────────────────────────────
# Based on your folder structure, results
# can be in TWO places:
#   1. <PROJECT_ROOT>/results/
#   2. <PROJECT_ROOT>/notebooks/results/
#
# We check both and use whichever exists!

_results_dir1 = PROJECT_ROOT / 'results'
_results_dir2 = PROJECT_ROOT / 'notebooks' / 'results'

if _results_dir2.exists():
    RESULTS_DIR = _results_dir2
elif _results_dir1.exists():
    RESULTS_DIR = _results_dir1
else:
    # Create results dir if neither exists
    RESULTS_DIR = _results_dir1
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Ensure results dir exists
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────
# IMPORTS (after path setup)
# ─────────────────────────────────────────

from environment.pricing_env import DynamicPricingEnv
from agents.ppo.ppo_agent import PPOAgent
from agents.dqn.dqn_agent import DQNAgent
from agents.q_learning_agent import (
    QLearningAgent, QL_CONFIG
)
from agents.baseline_agents import (
    FixedPriceAgent, TimedPricingAgent,
    DemandBasedAgent, LinearDecayAgent
)
from utils.evaluator import evaluate_agent
from utils.code_quality import (
    check_project_structure,
    check_results_files,
    print_final_project_stats
)
from tests.test_environment import run_all_tests
from tests.test_agents import run_all_agent_tests
from tests.test_ppo import run_all_ppo_tests
from training.config_manager import (
    BEST_PPO_CONFIG,
    BEST_DQN_CONFIG
)


# ─────────────────────────────────────────
# MAIN VERIFICATION
# ─────────────────────────────────────────

def run_final_verification():
    """
    Run complete final verification.
    All checks in one script!
    """
    print("=" * 60)
    print("  FINAL VERIFICATION")
    print("  Project 2 — RL Dynamic Pricing")
    print("  Infotact DS/ML Internship 2026")
    print("=" * 60)
    print(f"\n  Project Root : {PROJECT_ROOT}")
    print(f"  Results Dir  : {RESULTS_DIR}")

    results = {}

    # ── Check 1: Structure ──
    print("\n[CHECK 1] Project Structure...")
    results['structure'] = check_project_structure()

    # ── Check 2: Unit Tests ──
    print("\n[CHECK 2] Unit Tests...")
    env_ok   = run_all_tests()
    agent_ok = run_all_agent_tests()
    ppo_ok   = run_all_ppo_tests()
    tests_ok = env_ok and agent_ok and ppo_ok
    results['unit_tests'] = tests_ok

    print(f"\n  Test Results:")
    print(f"  Environment (8) : "
          f"{'✅' if env_ok else '❌'}")
    print(f"  Agents     (11) : "
          f"{'✅' if agent_ok else '❌'}")
    print(f"  PPO         (7) : "
          f"{'✅' if ppo_ok else '❌'}")
    print(f"  Total      (26) : "
          f"{'✅ ALL PASS' if tests_ok else '❌ FAIL'}")

    # ── Check 3: Quick Agent Test ──
    print("\n[CHECK 3] Quick Agent Verification...")
    env = DynamicPricingEnv()

    # Quick PPO test
    print("  Training PPO (100 eps)...")
    ppo = PPOAgent(
        env, {**BEST_PPO_CONFIG, 'n_episodes': 100}
    )
    ppo.train(n_episodes=100, verbose=False)
    ppo_eval = ppo.evaluate(n_episodes=20)

    # Quick DQN test
    print("  Training DQN (100 eps)...")
    dqn = DQNAgent(
        env, {**BEST_DQN_CONFIG, 'n_episodes': 100}
    )
    dqn.train(n_episodes=100, verbose=False)
    dqn_eval = dqn.evaluate(n_episodes=20)

    # Quick baseline
    bl_df  = evaluate_agent(
        TimedPricingAgent(env), n_episodes=20
    )
    bl_rev = bl_df['total_revenue'].mean()

    ppo_wins = ppo_eval['mean_revenue'] > bl_rev
    dqn_wins = dqn_eval['mean_revenue'] > bl_rev

    print(f"\n  PPO Revenue   : ${ppo_eval['mean_revenue']:.0f}")
    print(f"  DQN Revenue   : ${dqn_eval['mean_revenue']:.0f}")
    print(f"  Best Baseline : ${bl_rev:.0f}")
    print(f"  PPO > Baseline: {'✅' if ppo_wins else '⚠️'}")
    print(f"  DQN > Baseline: {'✅' if dqn_wins else '⚠️'}")

    results['agent_check'] = ppo_wins

    # ── Check 4: Results Files ──
    print("\n[CHECK 4] Results Files...")
    results['results_files'] = check_results_files()

    # ── Final Summary ──
    print("\n" + "=" * 60)
    print("  FINAL VERIFICATION SUMMARY")
    print("=" * 60)

    all_passed = all(results.values())
    checks = {
        'Project Structure': results['structure'],
        'Unit Tests (26)'  : results['unit_tests'],
        'Agent Check'      : results['agent_check'],
        'Results Files'    : results['results_files'],
    }

    for check, passed in checks.items():
        icon = '✅' if passed else '❌'
        print(f"  {icon} {check}")

    print("\n" + "─" * 60)
    if all_passed:
        print("  🎉 ALL CHECKS PASSED!")
        print("  ✅ PROJECT IS SUBMISSION READY!")
    else:
        failed = [
            k for k, v in checks.items() if not v
        ]
        print(f"  ⚠️  Fix these: {failed}")
    print("─" * 60)

    # ── Save Verification Report ──
    report = {
        'date'         : '4th August 2026',
        'project_root' : str(PROJECT_ROOT),
        'results_dir'  : str(RESULTS_DIR),
        'checks'       : {
            k: bool(v) for k, v in checks.items()
        },
        'all_passed'   : bool(all_passed),
        'ppo_revenue'  : float(ppo_eval['mean_revenue']),
        'dqn_revenue'  : float(dqn_eval['mean_revenue']),
        'bl_revenue'   : float(bl_rev),
    }

    # Save to correct results folder
    report_path = RESULTS_DIR / 'verification_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)

    print(f"\n✅ Verification report saved!")
    print(f"   Path: {report_path}")

    return all_passed


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    passed = run_final_verification()
    if passed:
        print("\n🚀 Ready for Final Review!")
    else:
        print("\n⚠️  Fix issues before review!")