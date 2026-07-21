"""
ppo_vs_dqn.py
=============
Detailed comparison between
PPO and DQN agents.

Compares:
1. Revenue performance
2. Training stability
3. Convergence speed
4. Price trajectories
5. Learned behaviors

Infotact DS/ML Internship — Project 2
Week 3 : PPO vs DQN Analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]   # src
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)


def compare_stability(
        ppo_rewards: list,
        dqn_rewards: list,
        save_path: str = '../results/stability_comparison.png'):
    """
    Compare training stability between
    PPO and DQN.

    Parameters
    ----------
    ppo_rewards : list
        PPO episode rewards.
    dqn_rewards : list
        DQN episode rewards.
    save_path : str
        Save path.
    """
    print("=" * 55)
    print("  STABILITY COMPARISON")
    print("=" * 55)

    # Rolling statistics
    window     = 100
    ppo_series = pd.Series(ppo_rewards)
    dqn_series = pd.Series(dqn_rewards)

    ppo_mean = ppo_series.rolling(window).mean()
    dqn_mean = dqn_series.rolling(window).mean()
    ppo_std  = ppo_series.rolling(window).std()
    dqn_std  = dqn_series.rolling(window).std()

    # Stability metrics
    ppo_cv = ppo_series[-500:].std() / \
             ppo_series[-500:].mean()
    dqn_cv = dqn_series[-500:].std() / \
             dqn_series[-500:].mean()

    print(f"\n  Coefficient of Variation (lower=stable):")
    print(f"  PPO CV: {ppo_cv:.4f}")
    print(f"  DQN CV: {dqn_cv:.4f}")
    if ppo_cv < dqn_cv:
        print(f"  ✅ PPO is MORE stable!")
    else:
        print(f"  ✅ DQN is MORE stable!")

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # Mean comparison
    axes[0, 0].plot(
        ppo_mean, color='gold',
        linewidth=2, label='PPO'
    )
    axes[0, 0].plot(
        dqn_mean, color='coral',
        linewidth=2, label='DQN'
    )
    axes[0, 0].set_title(
        'Rolling Mean Revenue\nPPO vs DQN',
        fontweight='bold'
    )
    axes[0, 0].set_xlabel('Episode')
    axes[0, 0].set_ylabel('Revenue ($)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Std comparison (stability)
    axes[0, 1].plot(
        ppo_std, color='gold',
        linewidth=2, label='PPO'
    )
    axes[0, 1].plot(
        dqn_std, color='coral',
        linewidth=2, label='DQN'
    )
    axes[0, 1].set_title(
        'Rolling Std Revenue\n(Lower = More Stable)',
        fontweight='bold'
    )
    axes[0, 1].set_xlabel('Episode')
    axes[0, 1].set_ylabel('Std Revenue ($)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Distribution last 500 episodes
    axes[1, 0].hist(
        ppo_rewards[-500:],
        bins=30, alpha=0.7,
        color='gold', label='PPO',
        edgecolor='black'
    )
    axes[1, 0].hist(
        dqn_rewards[-500:],
        bins=30, alpha=0.7,
        color='coral', label='DQN',
        edgecolor='black'
    )
    axes[1, 0].axvline(
        x=np.mean(ppo_rewards[-500:]),
        color='darkgoldenrod',
        linewidth=2, linestyle='--',
        label=f"PPO mean: "
              f"${np.mean(ppo_rewards[-500:]):.0f}"
    )
    axes[1, 0].axvline(
        x=np.mean(dqn_rewards[-500:]),
        color='darkred',
        linewidth=2, linestyle='--',
        label=f"DQN mean: "
              f"${np.mean(dqn_rewards[-500:]):.0f}"
    )
    axes[1, 0].set_title(
        'Revenue Distribution\nLast 500 Episodes',
        fontweight='bold'
    )
    axes[1, 0].set_xlabel('Revenue ($)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].legend(fontsize=8)

    # CV comparison
    agents = ['PPO', 'DQN']
    cvs    = [ppo_cv, dqn_cv]
    colors = ['gold', 'coral']
    axes[1, 1].bar(
        agents, cvs,
        color=colors,
        edgecolor='black',
        width=0.4
    )
    axes[1, 1].set_title(
        'Stability (CV Score)\nLower = More Stable',
        fontweight='bold'
    )
    axes[1, 1].set_ylabel(
        'Coefficient of Variation'
    )
    for i, (a, cv) in enumerate(zip(agents, cvs)):
        axes[1, 1].text(
            i, cv + 0.001,
            f'{cv:.4f}',
            ha='center',
            fontweight='bold'
        )

    plt.suptitle(
        'PPO vs DQN — Stability Analysis',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")

    return ppo_cv, dqn_cv


def compare_trajectories(
        ppo_agent,
        dqn_agent,
        env: DynamicPricingEnv,
        save_path: str = '../results/ppo_dqn_trajectories.png'):
    """
    Compare price trajectories of PPO vs DQN.

    Parameters
    ----------
    ppo_agent : PPOAgent
        Trained PPO agent.
    dqn_agent : DQNAgent
        Trained DQN agent.
    env : DynamicPricingEnv
        Environment.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    agents_info = [
        (ppo_agent, 'PPO', 'gold', axes[0]),
        (dqn_agent, 'DQN', 'coral', axes[1]),
    ]

    for agent, name, color, ax in agents_info:
        # Run 5 episodes
        for ep in range(5):
            state, _ = env.reset(seed=ep)
            prices   = []
            done     = False

            while not done:
                if hasattr(agent, 'select_action'):
                    if name == 'PPO':
                        action = agent.select_action(
                            state, training=False
                        )
                    else:
                        action = agent.select_action(
                            state, training=False
                        )
                prices.append(
                    PRICE_LEVELS[action]
                )
                state, _, term, trunc, _ = (
                    env.step(action)
                )
                done = term or trunc

            ax.plot(
                prices,
                color=color,
                alpha=0.5,
                linewidth=1.5
            )

        ax.set_title(
            f'{name} Price Trajectories\n'
            f'5 Episodes Overlaid',
            fontweight='bold'
        )
        ax.set_xlabel('Day')
        ax.set_ylabel('Price ($)')
        ax.set_ylim([0, 350])
        ax.grid(True, alpha=0.3)
        ax.axvspan(
            25, 30, alpha=0.1,
            color='red',
            label='Deadline Zone'
        )
        ax.legend()

    plt.suptitle(
        'Price Trajectory Comparison\nPPO vs DQN',
        fontsize=13, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


def statistical_ppo_vs_dqn(
        ppo_agent,
        dqn_agent,
        env: DynamicPricingEnv,
        n_episodes: int = 200):
    """
    Statistical test: PPO vs DQN.

    Parameters
    ----------
    ppo_agent : PPOAgent
        Trained PPO agent.
    dqn_agent : DQNAgent
        Trained DQN agent.
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Test episodes.
    """
    print("=" * 55)
    print("  STATISTICAL TEST: PPO vs DQN")
    print("=" * 55)

    # Get revenues
    ppo_revs = []
    dqn_revs = []

    for ep in range(n_episodes):
        # PPO
        state, _ = env.reset(seed=ep)
        total    = 0
        done     = False
        while not done:
            action = ppo_agent.select_action(
                state, training=False
            )
            state, r, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc
            total += max(0, r)
        ppo_revs.append(total)

        # DQN
        state, _ = env.reset(seed=ep)
        total    = 0
        done     = False
        while not done:
            action = dqn_agent.select_action(
                state, training=False
            )
            state, r, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc
            total += max(0, r)
        dqn_revs.append(total)

    ppo_revs = np.array(ppo_revs)
    dqn_revs = np.array(dqn_revs)

    # t-test
    t_stat, p_value = stats.ttest_ind(
        ppo_revs, dqn_revs
    )

    # Effect size
    pooled_std = np.sqrt(
        (ppo_revs.std()**2 +
         dqn_revs.std()**2) / 2
    )
    cohens_d = (
        ppo_revs.mean() - dqn_revs.mean()
    ) / pooled_std

    improvement = (
        ppo_revs.mean() - dqn_revs.mean()
    ) / dqn_revs.mean() * 100

    print(f"\n  PPO Mean Revenue: "
          f"${ppo_revs.mean():.0f}"
          f" ± ${ppo_revs.std():.0f}")
    print(f"  DQN Mean Revenue: "
          f"${dqn_revs.mean():.0f}"
          f" ± ${dqn_revs.std():.0f}")
    print(f"\n  Improvement: {improvement:+.1f}%")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value    : {p_value:.4f}")
    print(f"  Cohen's d  : {cohens_d:.4f}")

    if p_value < 0.05:
        print(f"\n  ✅ PPO significantly better "
              f"than DQN! (p<0.05)")
    else:
        print(f"\n  ⚠️  No significant difference")

    print("=" * 55)

    return {
        'ppo_mean'   : ppo_revs.mean(),
        'dqn_mean'   : dqn_revs.mean(),
        'improvement': improvement,
        'p_value'    : p_value,
        'cohens_d'   : cohens_d
    }


if __name__ == "__main__":
    print("✅ PPO vs DQN analysis loaded!")