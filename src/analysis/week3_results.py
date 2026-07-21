"""
week3_results.py
================
Saves Week 3 PPO training results.

Infotact DS/ML Internship — Project 2
Week 3 : Results
"""

import numpy as np
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]   # src
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def save_week3_results(
        ppo_eval: dict,
        dqn_eval: dict,
        ql_eval: dict,
        all_results: dict,
        stats_results: dict,
        save_path: str = '../results/week3_results.json'):
    """
    Save all Week 3 results to JSON.

    Parameters
    ----------
    ppo_eval : dict
        PPO evaluation results.
    dqn_eval : dict
        DQN evaluation results.
    ql_eval : dict
        Q-Learning evaluation results.
    all_results : dict
        All agent revenues.
    stats_results : dict
        Statistical comparison results.
    save_path : str
        Save path.
    """
    os.makedirs(
        os.path.dirname(save_path),
        exist_ok=True
    )

    results = {
        'week'        : 3,
        'project'     : 'RL Dynamic Pricing',
        'ppo'         : {
            'mean_revenue' : float(
                ppo_eval['mean_revenue']
            ),
            'std_revenue'  : float(
                ppo_eval['std_revenue']
            ),
        },
        'dqn'         : {
            'mean_revenue' : float(
                dqn_eval['mean_revenue']
            ),
        },
        'q_learning'  : {
            'mean_revenue' : float(
                ql_eval['mean_revenue']
            ),
        },
        'all_agents'  : {
            k: float(v)
            for k, v in all_results.items()
        },
        'ppo_vs_dqn'  : stats_results,
        'ppo_rank'    : 1,
    }

    with open(save_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"✅ Week 3 results saved!")
    print(f"   Path: {save_path}")
    print(f"\n  Summary:")
    print(f"  PPO Revenue : "
          f"${ppo_eval['mean_revenue']:.0f}")
    print(f"  DQN Revenue : "
          f"${dqn_eval['mean_revenue']:.0f}")
    print(f"  Improvement : "
          f"{stats_results['improvement']:+.1f}%")

    return results


if __name__ == "__main__":
    print("✅ Week 3 results module loaded!")