"""
run_all_checks.py
=================
Single script to run ALL checks.
Use this before Final Review!

Usage:
    cd RL-Dynamic-Pricing
    python src/run_all_checks.py

Infotact DS/ML Internship — Project 2
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_ROOT))

from utils.code_quality import (
    check_project_structure,
    check_results_files,
    check_gitignore,
    print_final_project_stats,
    print_commit_reminder
)
from tests.test_environment import run_all_tests
from tests.test_agents import run_all_agent_tests
from tests.test_ppo import run_all_ppo_tests


def run_all_checks():
    """Run every check in one command."""

    print("=" * 60)
    print("  COMPLETE PROJECT VERIFICATION")
    print("  RL Dynamic Pricing — Project 2")
    print("  Infotact DS/ML Internship 2026")
    print("=" * 60)
    print(f"\n  Root: {PROJECT_ROOT}\n")

    results = {}

    # ── 1. Structure ──
    print("\n[1/5] Project Structure Check...")
    results['structure'] = check_project_structure()

    # ── 2. Unit Tests ──
    print("\n[2/5] Running Unit Tests...")
    env_ok   = run_all_tests()
    agent_ok = run_all_agent_tests()
    ppo_ok   = run_all_ppo_tests()
    tests_ok = env_ok and agent_ok and ppo_ok
    results['tests'] = tests_ok

    print(f"\n  Environment (8)  : "
          f"{'✅' if env_ok else '❌'}")
    print(f"  Agents     (11)  : "
          f"{'✅' if agent_ok else '❌'}")
    print(f"  PPO        (7)   : "
          f"{'✅' if ppo_ok else '❌'}")
    print(f"  Total      (26)  : "
          f"{'✅ ALL PASS' if tests_ok else '❌ FAIL'}")

    # ── 3. Results Files ──
    print("\n[3/5] Results Files Check...")
    results['results'] = check_results_files()

    # ── 4. Gitignore ──
    print("\n[4/5] Gitignore Check...")
    results['gitignore'] = check_gitignore()

    # ── 5. Stats ──
    print("\n[5/5] Project Statistics...")
    print_final_project_stats()

    # ── Final Summary ──
    print("\n" + "=" * 60)
    print("  COMPLETE VERIFICATION SUMMARY")
    print("=" * 60)

    all_ok = all(results.values())
    icons  = {
        'structure' : 'Project Structure',
        'tests'     : 'Unit Tests (26)',
        'results'   : 'Results Files',
        'gitignore' : '.gitignore',
    }
    for key, label in icons.items():
        icon = '✅' if results[key] else '❌'
        print(f"  {icon} {label}")

    print("\n" + "─" * 60)
    if all_ok:
        print("  🎉 ALL CHECKS PASSED!")
        print("  ✅ PROJECT IS COMPLETE!")
        print("  🎯 READY FOR FINAL REVIEW!")
    else:
        failed = [
            icons[k] for k, v in results.items()
            if not v
        ]
        print(f"  ⚠️  Fix: {failed}")
    print("─" * 60)

    print_commit_reminder()
    return all_ok


if __name__ == "__main__":
    ok = run_all_checks()
    sys.exit(0 if ok else 1)