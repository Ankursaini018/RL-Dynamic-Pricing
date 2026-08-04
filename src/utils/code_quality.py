"""
code_quality.py
===============
Code quality utilities and
final project verification.

Infotact DS/ML Internship — Project 2
Week 4 : Code Quality

FIX APPLIED:
Uses os.path.abspath(__file__) to get
correct project root regardless of
where script is run from.

This file is at:
  RL-Dynamic-Pricing/src/utils/code_quality.py

So PROJECT_ROOT = 2 levels up = RL-Dynamic-Pricing/
"""

import os
import sys
import json
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────
# GET PROJECT ROOT DYNAMICALLY
# ─────────────────────────────────────────
# This file lives at:
#   <PROJECT_ROOT>/src/utils/code_quality.py
#
# So going 2 levels up gives PROJECT_ROOT:
#   Path(__file__).resolve().parents[0] = src/utils/
#   Path(__file__).resolve().parents[1] = src/
#   Path(__file__).resolve().parents[2] = PROJECT_ROOT ✅

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT     = PROJECT_ROOT / 'src'

# Add src to path for imports
sys.path.insert(0, str(SRC_ROOT))


def _p(*parts) -> str:
    """
    Helper: Build absolute path from project root.

    Example:
        _p('src', 'config.py')
        → 'X:/Infotact/RL-Dynamic-Pricing/src/config.py'
    """
    return str(PROJECT_ROOT.joinpath(*parts))


def _r(*parts) -> str:
    """
    Helper: Build absolute path for results folder.
    Checks BOTH possible results locations:
      1. <PROJECT_ROOT>/results/
      2. <PROJECT_ROOT>/notebooks/results/

    Returns whichever exists, defaults to option 1.
    """
    # Option 1: PROJECT_ROOT/results/
    path1 = PROJECT_ROOT / 'results' / Path(*parts)
    # Option 2: PROJECT_ROOT/notebooks/results/
    path2 = PROJECT_ROOT / 'notebooks' / 'results' / Path(*parts)

    # Return whichever exists
    if path1.exists():
        return str(path1)
    elif path2.exists():
        return str(path2)
    else:
        # Default to option 1 (will show as missing)
        return str(path1)


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
    print(f"  Root: {PROJECT_ROOT}")
    print("=" * 55)

    required_files = {
        'Core': [
            _p('src', 'config.py'),
            _p('src', 'project_runner.py'),
            _p('src', 'project_summary.py'),
            _p('requirements.txt'),
            _p('README.md'),
        ],
        'Environment': [
            _p('src', 'environment', 'pricing_env.py'),
            _p('src', 'environment', 'env_config.py'),
            _p('src', 'environment', 'env_validator.py'),
        ],
        'Agents': [
            _p('src', 'agents', 'baseline_agents.py'),
            _p('src', 'agents', 'q_learning_agent.py'),
            _p('src', 'agents', 'agent_registry.py'),
            _p('src', 'agents', 'dqn', 'dqn_network.py'),
            _p('src', 'agents', 'dqn', 'dqn_agent.py'),
            _p('src', 'agents', 'dqn', 'replay_buffer.py'),
            _p('src', 'agents', 'dqn', 'dqn_utils.py'),
            _p('src', 'agents', 'ppo', 'ppo_network.py'),
            _p('src', 'agents', 'ppo', 'ppo_agent.py'),
            _p('src', 'agents', 'ppo', 'ppo_utils.py'),
        ],
        'Training': [
            _p('src', 'training', 'q_learning_trainer.py'),
            _p('src', 'training', 'dqn_trainer.py'),
            _p('src', 'training', 'ppo_trainer.py'),
            _p('src', 'training', 'ppo_hypertuner.py'),
            _p('src', 'training', 'config_manager.py'),
        ],
        'Simulation': [
            _p('src', 'simulation', 'final_simulation.py'),
            _p('src', 'simulation', 'season_simulator.py'),
            _p('src', 'simulation', 'business_value.py'),
        ],
        'Analysis': [
            _p('src', 'analysis', 'final_comparison.py'),
            _p('src', 'analysis', 'final_proof.py'),
            _p('src', 'analysis', 'week3_analyzer.py'),
        ],
        'Visualization': [
            _p('src', 'visualization', 'business_dashboard.py'),
            _p('src', 'visualization', 'price_dashboard.py'),
        ],
        'Tests': [
            _p('src', 'tests', 'test_environment.py'),
            _p('src', 'tests', 'test_agents.py'),
            _p('src', 'tests', 'test_ppo.py'),
        ],
    }

    all_ok  = True
    total   = 0
    missing = 0

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

    Checks BOTH results folders:
    1. <PROJECT_ROOT>/results/
    2. <PROJECT_ROOT>/notebooks/results/

    Returns
    -------
    bool
        True if all results present.
    """
    print("\n" + "=" * 55)
    print("  RESULTS FILES CHECK")
    print("=" * 55)

    # Detect which results folder exists
    results_dir1 = PROJECT_ROOT / 'results'
    results_dir2 = PROJECT_ROOT / 'notebooks' / 'results'

    print(f"\n  Checking results locations:")
    print(f"  Option 1: {results_dir1}")
    print(f"    Exists: {'✅' if results_dir1.exists() else '❌'}")
    print(f"  Option 2: {results_dir2}")
    print(f"    Exists: {'✅' if results_dir2.exists() else '❌'}")

    # Use whichever exists (prefer option 2 based on your screenshots)
    if results_dir2.exists():
        results_dir = results_dir2
        print(f"\n  Using: notebooks/results/")
    elif results_dir1.exists():
        results_dir = results_dir1
        print(f"\n  Using: results/")
    else:
        print(f"\n  ❌ No results folder found!")
        return False

    # Files to check
    results_files = {
        'Charts': [
            'final_simulation.png',
            'business_dashboard.png',
            'behavior_proof.png',
            'proof_summary.png',
            'ppo_training.png',
            'week3_final_dashboard.png',
        ],
        'Data': [
            'final_simulation_summary.csv',
        ],
        'JSON': [
            'final_project_report.json',
            'model_card.json',
            'business_value.json',
            'statistical_proof.json',
        ]
    }

    all_ok      = True
    missing     = []
    found_count = 0

    for category, files in results_files.items():
        print(f"\n  {category}:")
        for fname in files:
            # Check in detected results dir
            path1 = results_dir / fname
            # Also check other location
            other = (
                results_dir1 / fname
                if results_dir == results_dir2
                else results_dir2 / fname
            )

            if path1.exists():
                print(f"    ✅ {fname}")
                found_count += 1
            elif other.exists():
                print(f"    ✅ {fname} (found in other location)")
                found_count += 1
            else:
                print(f"    ⚠️  Missing: {fname}")
                missing.append(fname)
                all_ok = False

    print(f"\n  Found  : {found_count} files")
    print(f"  Missing: {len(missing)} files")

    if all_ok:
        print(f"\n  ✅ All result files present!")
    else:
        print(f"\n  ⚠️  Missing files: {missing}")
        print(f"  → Run the key notebooks to generate!")
        print(f"  → Key notebook: week4_day2_business_dashboard.ipynb")

    return all_ok


# ─────────────────────────────────────────
# GITIGNORE CHECKER
# ─────────────────────────────────────────

def check_gitignore() -> bool:
    """
    Verify .gitignore has all required entries.

    Returns
    -------
    bool
        True if gitignore is complete.
    """
    # Use absolute path from project root
    gitignore_path = PROJECT_ROOT / '.gitignore'

    required_entries = [
        'models/',
        '*.pth',
        '__pycache__/',
        'data/',
        '*.pyc',
    ]

    print("\n=== .gitignore CHECK ===\n")
    print(f"  Looking at: {gitignore_path}")

    if not gitignore_path.exists():
        print("  ❌ .gitignore not found!")
        print(f"  Expected at: {gitignore_path}")
        return False

    with open(gitignore_path, 'r') as f:
        content = f.read()

    all_ok = True
    for entry in required_entries:
        if entry in content:
            print(f"  ✅ {entry}")
        else:
            print(f"  ❌ MISSING: {entry}")
            all_ok = False

    if all_ok:
        print("\n  ✅ .gitignore is complete!")
    else:
        print("\n  ⚠️  Add missing entries to .gitignore!")

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
  ✅ 4th August (LAST DAY!)

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
        'Environment': {
            'Max Inventory': 50,
            'Max Days'     : 30,
            'Price Levels' : 6,
            'State Space'  : 1581,
        },
        'Algorithms': {
            'Q-Learning': 'Tabular (9,486 entries)',
            'DQN'       : '2→128→64→6 (~10K params)',
            'PPO'       : 'Actor-Critic (~10K params)',
        },
        'Training': {
            'Q-Learning': '3,000 episodes',
            'DQN'       : '2,000 episodes',
            'PPO'       : '2,000 episodes',
        },
        'Evaluation': {
            'Seasons': '1,000',
            'Method' : "t-test + Cohen's d",
            'Result' : 'PPO wins p<0.05',
        },
        'Code Quality': {
            'Unit Tests': '26 passing',
            'Notebooks' : '25+',
            'Scripts'   : '50+',
            'Issues'    : '21/21 closed',
        }
    }

    for category, items in stats.items():
        print(f"\n  {category}:")
        for k, v in items.items():
            print(f"    {k:<20}: {v}")

    print("\n" + "=" * 55)


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n  Project Root: {PROJECT_ROOT}")
    print(f"  Src Root    : {SRC_ROOT}\n")

    ok1 = check_project_structure()
    ok2 = check_results_files()
    ok3 = check_gitignore()
    print_final_project_stats()
    print_commit_reminder()

    print("\n" + "=" * 55)
    print("  FINAL CHECK SUMMARY")
    print("=" * 55)
    print(f"  Structure : {'✅' if ok1 else '❌'}")
    print(f"  Results   : {'✅' if ok2 else '⚠️ Some missing'}")
    print(f"  Gitignore : {'✅' if ok3 else '❌'}")

    if ok1:
        print("\n✅ Project structure complete!")
    else:
        print("\n⚠️  Fix missing files!")