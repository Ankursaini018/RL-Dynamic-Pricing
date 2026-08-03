"""
final_utils.py
==============
Final utility functions for
project completion and review.

Infotact DS/ML Internship — Project 2
Week 4 : Final Utilities
"""

import numpy as np
import pandas as pd
import json
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)


# ─────────────────────────────────────────
# QUICK DEMO RUNNER
# ─────────────────────────────────────────

def run_quick_demo(
        agent,
        env: DynamicPricingEnv,
        seed: int = 42) -> dict:
    """
    Run quick single episode demo.
    Perfect for live review demos!

    Parameters
    ----------
    agent : Any
        Trained pricing agent.
    env : DynamicPricingEnv
        Environment.
    seed : int
        Random seed.

    Returns
    -------
    dict
        Episode results.
    """
    print("=" * 50)
    print("  LIVE DEMO — ONE EPISODE")
    print("=" * 50)

    state, _ = env.reset(seed=seed)
    total_rev  = 0
    total_sold = 0
    day        = 1
    done       = False

    print(f"\n  Day | Inventory | Days Left | "
          f"Price | Sold? | Revenue")
    print("  " + "─" * 55)

    while not done:
        action = agent.select_action(
            state, training=False
        )
        if isinstance(action, tuple):
            action = action[0]

        price = PRICE_LEVELS[action]
        inv   = int(state[0])
        days  = int(state[1])

        state, reward, term, trunc, info = (
            env.step(action)
        )
        done = term or trunc

        sold    = info['bought']
        rev_step = max(0, reward)
        total_rev  += rev_step
        if sold:
            total_sold += 1

        sold_str = "✅ YES" if sold else "❌ No"
        print(f"  {day:3d} | {inv:9d} | "
              f"{days:9d} | ${price:4d} | "
              f"{sold_str} | ${rev_step:.0f}")
        day += 1

    print("  " + "─" * 55)
    print(f"\n  EPISODE RESULTS:")
    print(f"  Total Revenue : ${total_rev:.0f}")
    print(f"  Tickets Sold  : {total_sold}/50")
    print(f"  Sell Through  : "
          f"{total_sold/env.max_inventory*100:.1f}%")
    print(f"  Avg Price     : "
          f"${total_rev/max(total_sold,1):.0f}")
    print("=" * 50)

    return {
        'revenue'     : total_rev,
        'sold'        : total_sold,
        'sell_through': total_sold /
                        env.max_inventory
    }


# ─────────────────────────────────────────
# REVIEW DEMO SCRIPT
# ─────────────────────────────────────────

def print_review_demo_guide():
    """
    Print step by step demo guide
    for final review presentation.
    """
    print("""
╔════════════════════════════════════════════════╗
║        FINAL REVIEW DEMO GUIDE                 ║
╠════════════════════════════════════════════════╣
║                                                ║
║  STEP 1: Show GitHub (30 seconds)              ║
║  → github.com/Ankursaini018/                   ║
║    RL-Dynamic-Pricing                          ║
║  → Show README badges                          ║
║  → Click commits (28+ days!)                   ║
║  → Show Kanban (all 21 done!)                  ║
║                                                ║
║  STEP 2: Run Environment (20 seconds)          ║
║  → cd src                                      ║
║  → python environment/pricing_env.py           ║
║  → Show output                                 ║
║                                                ║
║  STEP 3: Run Tests (20 seconds)                ║
║  → python tests/test_ppo.py                    ║
║  → Show 7/7 passing                            ║
║                                                ║
║  STEP 4: Quick Pipeline (30 seconds)           ║
║  → python project_runner.py --quick            ║
║  → Show rankings appear                        ║
║                                                ║
║  STEP 5: Show Dashboard (30 seconds)           ║
║  → Open business_dashboard.png                 ║
║  → Explain each chart briefly                  ║
║                                                ║
║  STEP 6: Show Behavior Proof (20 seconds)      ║
║  → Open behavior_proof.png                     ║
║  → "PPO drops prices near deadline!"           ║
║                                                ║
║  TOTAL TIME: ~3 minutes ✅                     ║
╚════════════════════════════════════════════════╝
    """)


# ─────────────────────────────────────────
# GITIGNORE CHECKER
# ─────────────────────────────────────────

def check_gitignore() -> bool:
    """
    Verify .gitignore has all required
    entries.

    Returns
    -------
    bool
        True if gitignore is correct.
    """
    gitignore_path = '../.gitignore'

    required_entries = [
        'models/',
        '*.pth',
        '__pycache__/',
        'data/',
        '*.pyc',
        '.env',
    ]

    if not os.path.exists(gitignore_path):
        print("❌ .gitignore not found!")
        return False

    with open(gitignore_path, 'r') as f:
        content = f.read()

    print("=== .gitignore CHECK ===\n")
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
        print("\n  ⚠️  Add missing entries!")

    return all_ok


if __name__ == "__main__":
    print("✅ Final utilities loaded!")
    print_review_demo_guide()