"""
code_quality.py
===============
Code quality utilities and
final project verification.

Infotact DS/ML Internship — Project 2
Week 4 : Code Quality
"""

import os
import sys
import json
import numpy as np
sys.path.append('../')


# ─────────────────────────────────────────
# PROJECT STRUCTURE CHECKER
# ─────────────────────────────────────────

def check_project_structure() -> bool:
    """
    Verify all required files exist.

    Returns
    -------
    bool
        True if all files present.
    """
    print("=" * 55)
    print("  PROJECT STRUCTURE CHECK")
    print("=" * 55)

    required_files = {
        'Core': [
            '../src/config.py',
            '../src/project_runner.py',
            '../src/project_summary.py',
            '../requirements.txt',
            '../README.md',
        ],
        'Environment': [
            '../src/environment/pricing_env.py',
            '../src/environment/env_config.py',
            '../src/environment/env_validator.py',
        ],
        'Agents': [
            '../src/agents/baseline_agents.py',
            '../src/agents/q_learning_agent.py',
            '../src/agents/agent_registry.py',
            '../src/agents/dqn/dqn_network.py',
            '../src/agents/dqn/dqn_agent.py',
            '../src/agents/dqn/replay_buffer.py',
            '../src/agents/dqn/dqn_utils.py',
            '../src/agents/ppo/ppo_network.py',
            '../src/agents/ppo/ppo_agent.py',
            '../src/agents/ppo/ppo_utils.py',
        ],
        'Training': [
            '../src/training/q_learning_trainer.py',
            '../src/training/dqn_trainer.py',
            '../src/training/ppo_trainer.py',
            '../src/training/ppo_hypertuner.py',
            '../src/training/config_manager.py',
        ],
        'Simulation': [
            '../src/simulation/final_simulation.py',
            '../src/simulation/season_simulator.py',
            '../src/simulation/business_value.py',
        ],
        'Analysis': [
            '../src/analysis/final_comparison.py',
            '../src/analysis/final_proof.py',
            '../src/analysis/week3_analyzer.py',
        ],
        'Visualization': [
            '../src/visualization/business_dashboard.py',
            '../src/visualization/price_dashboard.py',
        ],
        'Tests': [
            '../src/tests/test_environment.py',
            '../src/tests/test_agents.py',
            '../src/tests/test_ppo.py',
        ],
    }

    all_ok    = True
    total     = 0
    missing   = 0

    for category, files in required_files.items():
        print(f"\n  {category}:")
        for f in files:
            total += 1
            exists = os.path.exists(f)
            status = '✅' if exists else '❌ MISSING'
            name   = os.path.basename(f)
            print(f"    {status} {name}")
            if not exists:
                missing += 1
                all_ok  = False

    print(f"\n  {'='*40}")
    print(f"  Total  : {total} files")
    print(f"  Present: {total - missing} files")
    print(f"  Missing: {missing} files")
    if all_ok:
        print(f"  ✅ ALL FILES PRESENT!")
    else:
        print(f"  ❌ {missing} FILES MISSING!")
    print(f"  {'='*40}")

    return all_ok


# ─────────────────────────────────────────
# RESULTS CHECKER
# ─────────────────────────────────────────

def check_results_files() -> bool:
    """
    Verify all result files exist.

    Returns
    -------
    bool
        True if all results present.
    """
    print("\n" + "=" * 55)
    print("  RESULTS FILES CHECK")
    print("=" * 55)

    results_files = {
        'Charts': [
            '../results/final_simulation.png',
            '../results/business_dashboard.png',
            '../results/behavior_proof.png',
            '../results/proof_summary.png',
            '../results/ppo_training.png',
            '../results/week3_final_dashboard.png',
        ],
        'Data': [
            '../results/final_simulation_summary.csv',
        ],
        'JSON': [
            '../results/final_project_report.json',
            '../results/model_card.json',
            '../results/business_value.json',
            '../results/statistical_proof.json',
        ]
    }

    all_ok  = True
    missing = []

    for category, files in results_files.items():
        print(f"\n  {category}:")
        for f in files:
            exists = os.path.exists(f)
            status = '✅' if exists else '⚠️  Missing'
            name   = os.path.basename(f)
            print(f"    {status} {name}")
            if not exists:
                missing.append(name)
                all_ok = False

    if all_ok:
        print(f"\n  ✅ All result files present!")
    else:
        print(f"\n  ⚠️  Missing: {missing}")
        print(f"  Run notebooks to generate!")

    return all_ok


# ─────────────────────────────────────────
# COMMIT REMINDER
# ─────────────────────────────────────────

def print_commit_reminder():
    """Print daily commit reminder."""
    print("\n" + "=" * 55)
    print("  DAILY COMMIT REMINDER")
    print("=" * 55)
    print("""
  Final Review needs 20 consecutive days!

  Remaining days:
  ✅ 2nd August (today)
  ✅ 3rd August
  ✅ 4th August (last day!)

  Then: Final Review 5th-10th August

  KEEP COMMITTING! NO GAPS! 🔥
  """)


# ─────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────

def print_final_project_stats():
    """Print final project statistics."""
    print("=" * 55)
    print("  FINAL PROJECT STATISTICS")
    print("=" * 55)

    stats = {
        'Environment'    : {
            'Max Inventory': 50,
            'Max Days'     : 30,
            'Price Levels' : 6,
            'State Space'  : 1581,
        },
        'Algorithms'     : {
            'Q-Learning'   : 'Tabular (9,486 entries)',
            'DQN'          : '2→128→64→6 (~10K params)',
            'PPO'          : 'Actor-Critic (~10K params)',
        },
        'Training'       : {
            'Q-Learning'   : '3,000 episodes',
            'DQN'          : '2,000 episodes',
            'PPO'          : '2,000 episodes',
        },
        'Evaluation'     : {
            'Seasons'      : '1,000',
            'Method'       : 't-test + Cohen\'s d',
            'Result'       : 'PPO wins p<0.05',
        },
        'Code Quality'   : {
            'Unit Tests'   : '26 passing',
            'Notebooks'    : '25+',
            'Scripts'      : '50+',
            'Issues'       : '21/21 closed',
        }
    }

    for category, items in stats.items():
        print(f"\n  {category}:")
        for k, v in items.items():
            print(f"    {k:<20}: {v}")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    ok1 = check_project_structure()
    ok2 = check_results_files()
    print_final_project_stats()
    print_commit_reminder()

    if ok1:
        print("\n✅ Project structure complete!")
    else:
        print("\n⚠️  Fix missing files!")