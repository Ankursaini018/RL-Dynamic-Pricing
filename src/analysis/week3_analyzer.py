"""
week3_analyzer.py
=================
Comprehensive Week 3 analysis
comparing all RL agents and baselines.

Infotact DS/ML Internship — Project 2
Week 3 : Comprehensive Analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)
from agents.ppo.ppo_agent import PPOAgent
from agents.dqn.dqn_agent import DQNAgent
from agents.q_learning_agent import (
    QLearningAgent,
    QL_CONFIG
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


# ─────────────────────────────────────────
# TRAIN ALL AGENTS
# ─────────────────────────────────────────

def train_all_agents(
        env: DynamicPricingEnv,
        n_episodes: int = 2000) -> dict:
    """
    Train all RL agents with best configs.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Training episodes.

    Returns
    -------
    dict
        All trained agents.
    """
    print("=" * 55)
    print("  TRAINING ALL AGENTS")
    print("=" * 55)

    agents = {}

    # Q-Learning
    print("\n[1] Training Q-Learning...")
    ql = QLearningAgent(env, QL_CONFIG)
    ql.train(
        n_episodes=int(n_episodes * 1.5),
        verbose=False
    )
    agents['Q-Learning'] = ql
    print(f"    ✅ Done!")

    # DQN
    print("\n[2] Training DQN (best config)...")
    dqn = DQNAgent(env, BEST_DQN_CONFIG)
    dqn.train(
        n_episodes=n_episodes,
        verbose=False
    )
    agents['DQN'] = dqn
    print(f"    ✅ Done!")

    # PPO
    print("\n[3] Training PPO (best config)...")
    ppo = PPOAgent(env, BEST_PPO_CONFIG)
    ppo.train(
        n_episodes=n_episodes,
        verbose=False
    )
    agents['PPO'] = ppo
    print(f"    ✅ Done!")

    return agents


# ─────────────────────────────────────────
# EVALUATE ALL
# ─────────────────────────────────────────

def evaluate_all_agents(
        env: DynamicPricingEnv,
        rl_agents: dict,
        n_eval: int = 100) -> pd.DataFrame:
    """
    Evaluate all agents comprehensively.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment.
    rl_agents : dict
        Trained RL agents.
    n_eval : int
        Evaluation episodes.

    Returns
    -------
    pd.DataFrame
        Complete evaluation results.
    """
    print("\n" + "=" * 55)
    print("  EVALUATING ALL AGENTS")
    print("=" * 55)

    results = []

    # Baseline agents
    baselines = {
        'Fixed Price'  : FixedPriceAgent(env),
        'Time Based'   : TimedPricingAgent(env),
        'Demand Based' : DemandBasedAgent(env),
        'Linear Decay' : LinearDecayAgent(env),
    }

    print("\n  Baselines:")
    for name, agent in baselines.items():
        df = evaluate_agent(agent, n_eval)
        rev = df['total_revenue'].mean()
        sold = df['total_sold'].mean()
        results.append({
            'Agent'        : name,
            'Type'         : 'Baseline',
            'Mean Revenue' : rev,
            'Std Revenue'  : df['total_revenue'].std(),
            'Max Revenue'  : df['total_revenue'].max(),
            'Mean Sold'    : sold,
            'Sell Through' : sold / env.max_inventory * 100
        })
        print(f"  {name:<15}: ${rev:.0f}")

    # RL agents
    print("\n  RL Agents:")
    for name, agent in rl_agents.items():
        revenues  = []
        sold_list = []

        for ep in range(n_eval):
            state, _ = env.reset(seed=ep)
            total_rev  = 0
            total_sold = 0
            done       = False

            while not done:
                if name == 'Q-Learning':
                    action = agent.select_action(
                        state, training=False
                    )
                else:
                    action = agent.select_action(
                        state, training=False
                    )
                    if isinstance(action, tuple):
                        action = action[0]

                state, reward, term, trunc, info = (
                    env.step(action)
                )
                done = term or trunc
                total_rev  += max(0, reward)
                if info['bought']:
                    total_sold += 1

            revenues.append(total_rev)
            sold_list.append(total_sold)

        revenues = np.array(revenues)
        rev_mean = revenues.mean()
        results.append({
            'Agent'        : name,
            'Type'         : 'RL',
            'Mean Revenue' : rev_mean,
            'Std Revenue'  : revenues.std(),
            'Max Revenue'  : revenues.max(),
            'Mean Sold'    : np.mean(sold_list),
            'Sell Through' : np.mean(sold_list) /
                             env.max_inventory * 100
        })
        print(f"  {name:<15}: ${rev_mean:.0f}")

    df = pd.DataFrame(results).sort_values(
        'Mean Revenue', ascending=False
    ).reset_index(drop=True)

    return df


# ─────────────────────────────────────────
# COMPREHENSIVE DASHBOARD
# ─────────────────────────────────────────

def create_week3_dashboard(
        results_df: pd.DataFrame,
        rl_agents: dict,
        save_path: str = '../results/week3_dashboard.png'):
    """
    Create comprehensive Week 3 dashboard.

    Parameters
    ----------
    results_df : pd.DataFrame
        Evaluation results.
    rl_agents : dict
        Trained RL agents.
    save_path : str
        Save path.
    """
    fig = plt.figure(figsize=(20, 16))
    gs  = gridspec.GridSpec(3, 3, figure=fig)

    colors_map = {
        'PPO'          : 'gold',
        'DQN'          : 'coral',
        'Q-Learning'   : 'green',
        'Time Based'   : 'steelblue',
        'Demand Based' : 'purple',
        'Linear Decay' : 'orange',
        'Fixed Price'  : 'lightgray',
    }

    # ── Plot 1: Revenue Ranking ──
    ax1 = fig.add_subplot(gs[0, :2])
    names    = results_df['Agent'].values
    revenues = results_df['Mean Revenue'].values
    stds     = results_df['Std Revenue'].values
    colors   = [
        colors_map.get(n, 'steelblue')
        for n in names
    ]

    bars = ax1.bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        yerr=stds, capsize=5,
        width=0.6
    )
    ax1.set_title(
        'Final Agent Rankings — Mean Revenue (±std)',
        fontweight='bold', fontsize=13
    )
    ax1.set_ylabel('Mean Revenue ($)')
    ax1.set_xticklabels(
        names, rotation=15, fontsize=9
    )
    for bar, val in zip(bars, revenues):
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            val + 20,
            f'${val:.0f}',
            ha='center', fontsize=9,
            fontweight='bold'
        )

    # ── Plot 2: Sell Through ──
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.bar(
        results_df['Agent'],
        results_df['Sell Through'],
        color=colors,
        edgecolor='black'
    )
    ax2.axhline(
        y=100, color='red',
        linestyle='--', label='100% target'
    )
    ax2.set_title(
        'Sell-Through Rate (%)',
        fontweight='bold'
    )
    ax2.set_ylabel('%')
    ax2.set_xticklabels(
        results_df['Agent'],
        rotation=20, fontsize=7
    )
    ax2.legend()

    # ── Plot 3: RL Training Curves ──
    ax3 = fig.add_subplot(gs[1, :])
    for name, agent in rl_agents.items():
        rewards = agent.episode_rewards
        smooth  = pd.Series(rewards).rolling(
            window=50
        ).mean()
        color   = colors_map.get(name, 'steelblue')
        ax3.plot(
            smooth, color=color,
            linewidth=2.5, label=name
        )

    ax3.set_title(
        'RL Agent Training Curves\n'
        'Q-Learning vs DQN vs PPO',
        fontweight='bold', fontsize=12
    )
    ax3.set_xlabel('Episode')
    ax3.set_ylabel('Revenue ($)')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)

    # ── Plot 4: Max Revenue ──
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.bar(
        results_df['Agent'],
        results_df['Max Revenue'],
        color=colors,
        edgecolor='black'
    )
    ax4.set_title(
        'Best Single Episode\nRevenue',
        fontweight='bold'
    )
    ax4.set_ylabel('Max Revenue ($)')
    ax4.set_xticklabels(
        results_df['Agent'],
        rotation=20, fontsize=7
    )

    # ── Plot 5: RL Journey ──
    ax5 = fig.add_subplot(gs[2, 1])
    rl_names = ['Q-Learning', 'DQN', 'PPO']
    rl_revs  = [
        results_df[
            results_df['Agent'] == n
        ]['Mean Revenue'].values[0]
        if n in results_df['Agent'].values
        else 0
        for n in rl_names
    ]
    rl_colors = ['green', 'coral', 'gold']

    bars = ax5.bar(
        rl_names, rl_revs,
        color=rl_colors,
        edgecolor='black',
        width=0.5
    )
    ax5.set_title(
        'RL Agent Evolution\nQ-Learning → DQN → PPO',
        fontweight='bold'
    )
    ax5.set_ylabel('Mean Revenue ($)')
    for bar, val in zip(bars, rl_revs):
        ax5.text(
            bar.get_x() + bar.get_width()/2,
            val + 10,
            f'${val:.0f}',
            ha='center',
            fontweight='bold'
        )

    # ── Plot 6: Revenue Distribution ──
    ax6 = fig.add_subplot(gs[2, 2])
    for name, agent in rl_agents.items():
        revenues = agent.episode_rewards[-200:]
        ax6.hist(
            revenues, bins=25,
            alpha=0.6,
            color=colors_map.get(name, 'gray'),
            label=name,
            edgecolor='black',
            linewidth=0.5
        )
    ax6.set_title(
        'Revenue Distribution\n(Last 200 Episodes)',
        fontweight='bold'
    )
    ax6.set_xlabel('Revenue ($)')
    ax6.set_ylabel('Frequency')
    ax6.legend(fontsize=8)

    plt.suptitle(
        'Week 3 — Comprehensive Analysis Dashboard\n'
        'PPO vs DQN vs Q-Learning vs Baselines',
        fontsize=15, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Dashboard saved: {save_path}")


# ─────────────────────────────────────────
# STATISTICAL PROOF
# ─────────────────────────────────────────

def prove_ppo_superiority(
        env: DynamicPricingEnv,
        rl_agents: dict,
        n_test: int = 200) -> dict:
    """
    Statistical proof that PPO beats all.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment.
    rl_agents : dict
        Trained RL agents.
    n_test : int
        Test episodes.

    Returns
    -------
    dict
        Statistical test results.
    """
    print("=" * 55)
    print("  STATISTICAL PROOF")
    print("  PPO vs All Other Agents")
    print("=" * 55)

    # Get revenues for each agent
    all_revenues = {}
    for name, agent in rl_agents.items():
        revs = []
        for ep in range(n_test):
            state, _ = env.reset(seed=ep)
            total = 0
            done  = False
            while not done:
                action = agent.select_action(
                    state, training=False
                )
                if isinstance(action, tuple):
                    action = action[0]
                state, r, term, trunc, _ = (
                    env.step(action)
                )
                done = term or trunc
                total += max(0, r)
            revs.append(total)
        all_revenues[name] = np.array(revs)

    # Compare PPO vs each
    ppo_revs = all_revenues.get('PPO')
    if ppo_revs is None:
        print("⚠️  PPO not found!")
        return {}

    proof_results = {}
    for name, revs in all_revenues.items():
        if name == 'PPO':
            continue

        t_stat, p_val = stats.ttest_ind(
            ppo_revs, revs
        )
        improvement = (
            ppo_revs.mean() - revs.mean()
        ) / revs.mean() * 100

        proof_results[name] = {
            'ppo_mean'   : ppo_revs.mean(),
            'other_mean' : revs.mean(),
            'improvement': improvement,
            'p_value'    : p_val,
            'significant': p_val < 0.05
        }

        print(f"\n  PPO vs {name}:")
        print(f"  Improvement: {improvement:+.1f}%")
        print(f"  p-value    : {p_val:.4f}")
        print(f"  Significant: "
              f"{'✅ Yes' if p_val < 0.05 else '❌ No'}")

    return proof_results


if __name__ == "__main__":
    env     = DynamicPricingEnv()
    agents  = train_all_agents(env, n_episodes=1000)
    results = evaluate_all_agents(env, agents)
    create_week3_dashboard(results, agents)
    proof   = prove_ppo_superiority(env, agents)
    print("\n✅ Week 3 analysis complete!")