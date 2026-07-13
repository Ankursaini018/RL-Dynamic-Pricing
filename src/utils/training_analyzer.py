"""
training_analyzer.py
====================
Analyzes and compares training results
between DQN and Q-Learning agents.

Infotact DS/ML Internship — Project 2
Week 2 : Training Analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import sys
sys.path.append('../')


def save_training_results(
        dqn_agent,
        ql_agent,
        all_results: dict,
        save_dir: str = '../results/'):
    """
    Save training results to JSON.

    Parameters
    ----------
    dqn_agent : DQNAgent
        Trained DQN agent.
    ql_agent : QLearningAgent
        Trained Q-Learning agent.
    all_results : dict
        All agent revenues.
    save_dir : str
        Save directory.
    """
    os.makedirs(save_dir, exist_ok=True)

    results = {
        'dqn': {
            'mean_revenue'    : float(
                np.mean(dqn_agent.episode_rewards[-100:])
            ),
            'training_episodes': len(
                dqn_agent.episode_rewards
            ),
            'final_epsilon'   : float(
                dqn_agent.epsilon
            ),
            'buffer_size'     : len(dqn_agent.buffer)
        },
        'q_learning': {
            'mean_revenue'    : float(
                np.mean(ql_agent.episode_rewards[-100:])
            ),
            'training_episodes': len(
                ql_agent.episode_rewards
            ),
            'final_epsilon'   : float(
                ql_agent.epsilon
            )
        },
        'all_agents'   : {
            k: float(v)
            for k, v in all_results.items()
        },
        'best_agent'   : max(
            all_results,
            key=all_results.get
        ),
        'best_revenue' : float(
            max(all_results.values())
        )
    }

    filepath = os.path.join(
        save_dir, 'week2_training_results.json'
    )
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"✅ Results saved: {filepath}")
    print(f"\n  Best Agent  : {results['best_agent']}")
    print(f"  Best Revenue: "
          f"${results['best_revenue']:.0f}")

    return results


def plot_convergence_analysis(
        dqn_rewards: list,
        ql_rewards: list,
        save_path: str = '../results/convergence.png'):
    """
    Analyze convergence speed of DQN vs Q-Learning.

    Parameters
    ----------
    dqn_rewards : list
        DQN episode rewards.
    ql_rewards : list
        Q-Learning episode rewards.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    window = 100

    # Rolling means
    dqn_smooth = pd.Series(dqn_rewards).rolling(
        window=window
    ).mean()
    ql_smooth  = pd.Series(ql_rewards).rolling(
        window=window
    ).mean()

    # Plot 1: Full training curves
    axes[0].plot(
        dqn_smooth,
        color='gold', linewidth=2.5,
        label='DQN'
    )
    axes[0].plot(
        ql_smooth,
        color='coral', linewidth=2.5,
        label='Q-Learning'
    )
    axes[0].set_title(
        'Training Convergence\nDQN vs Q-Learning',
        fontweight='bold'
    )
    axes[0].set_xlabel('Episode')
    axes[0].set_ylabel('Revenue ($)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Revenue distribution
    axes[1].hist(
        dqn_rewards[-500:],
        bins=30, alpha=0.7,
        color='gold', label='DQN (last 500)',
        edgecolor='black'
    )
    axes[1].hist(
        ql_rewards[-500:],
        bins=30, alpha=0.7,
        color='coral', label='Q-Learning (last 500)',
        edgecolor='black'
    )
    axes[1].axvline(
        x=np.mean(dqn_rewards[-500:]),
        color='darkgoldenrod', linewidth=2,
        linestyle='--',
        label=f"DQN mean: "
              f"${np.mean(dqn_rewards[-500:]):.0f}"
    )
    axes[1].axvline(
        x=np.mean(ql_rewards[-500:]),
        color='darkred', linewidth=2,
        linestyle='--',
        label=f"QL mean: "
              f"${np.mean(ql_rewards[-500:]):.0f}"
    )
    axes[1].set_title(
        'Revenue Distribution\n(Last 500 Episodes)',
        fontweight='bold'
    )
    axes[1].set_xlabel('Revenue ($)')
    axes[1].set_ylabel('Frequency')
    axes[1].legend(fontsize=8)

    plt.suptitle(
        'DQN vs Q-Learning Convergence Analysis',
        fontsize=13, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


if __name__ == "__main__":
    print("✅ Training analyzer loaded!")