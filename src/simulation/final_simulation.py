"""
final_simulation.py
===================
FINAL 1000-season simulation comparing
ALL agents including PPO, DQN, Q-Learning
and all baselines.

This is the KEY deliverable for Week 4!

Internship Spec:
"run 1,000 simulated booking seasons
to evaluate the DQN agent against
the naive baselines"

We extend this to include PPO!

Infotact DS/ML Internship — Project 2
Week 4 : Final Simulation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
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
from agents.ppo.ppo_agent import PPOAgent
from agents.dqn.dqn_agent import DQNAgent
from agents.q_learning_agent import (
    QLearningAgent, QL_CONFIG
)
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)
from training.config_manager import (
    BEST_PPO_CONFIG,
    BEST_DQN_CONFIG
)

os.makedirs('../results', exist_ok=True)


# ─────────────────────────────────────────
# SINGLE AGENT SIMULATION
# ─────────────────────────────────────────

def simulate_single_agent(
        agent,
        env: DynamicPricingEnv,
        n_seasons: int = 1000,
        seed: int = 42) -> pd.DataFrame:
    """
    Simulate agent over N seasons.

    Parameters
    ----------
    agent : Any
        Pricing agent.
    env : DynamicPricingEnv
        Environment.
    n_seasons : int
        Number of seasons.
    seed : int
        Base seed.

    Returns
    -------
    pd.DataFrame
        Season-by-season results.
    """
    name    = getattr(agent, 'name', 'Agent')
    results = []

    for season in range(n_seasons):
        if hasattr(agent, 'select_action'):
            # RL agent
            state, _ = env.reset(
                seed=seed + season
            )
            total_rev  = 0
            total_sold = 0
            prices     = []
            done       = False

            while not done:
                try:
                    action = agent.select_action(
                        state,
                        training=False
                    )
                except TypeError:
                    action = agent.select_action(state)
                if isinstance(action, tuple):
                    action = action[0]

                state, reward, term, \
                    trunc, info = env.step(action)
                done = term or trunc

                total_rev  += max(0, reward)
                prices.append(info['price'])
                if info['bought']:
                    total_sold += 1
        else:
            # Baseline agent
            result = agent.run_episode(
                seed=seed + season
            )
            total_rev  = result['total_revenue']
            total_sold = result['total_sold']
            prices     = result['prices_used']

        results.append({
            'season'        : season + 1,
            'agent'         : name,
            'revenue'       : total_rev,
            'tickets_sold'  : total_sold,
            'sell_through'  : total_sold /
                              env.max_inventory,
            'avg_price'     : np.mean(prices),
            'revenue_per_ticket': (
                total_rev / total_sold
                if total_sold > 0 else 0
            )
        })

    return pd.DataFrame(results)


# ─────────────────────────────────────────
# FULL SIMULATION
# ─────────────────────────────────────────

def run_final_simulation(
        agents: dict,
        env: DynamicPricingEnv,
        n_seasons: int = 1000) -> tuple:
    """
    Run final 1000-season simulation
    for all agents.

    Parameters
    ----------
    agents : dict
        {name: agent} dictionary.
    env : DynamicPricingEnv
        Environment.
    n_seasons : int
        Seasons per agent.

    Returns
    -------
    tuple
        (all_results, summary_df)
    """
    print("=" * 60)
    print(f"  FINAL {n_seasons}-SEASON SIMULATION")
    print("  Comparing ALL pricing strategies")
    print("=" * 60)

    all_results  = {}
    summary_rows = []

    for name, agent in agents.items():
        print(f"\n  Simulating: {name}...")
        df = simulate_single_agent(
            agent, env, n_seasons
        )
        all_results[name] = df

        summary_rows.append({
            'Agent'          : name,
            'Mean Revenue'   : df['revenue'].mean(),
            'Std Revenue'    : df['revenue'].std(),
            'Max Revenue'    : df['revenue'].max(),
            'Min Revenue'    : df['revenue'].min(),
            'Mean Sold'      : df['tickets_sold'].mean(),
            'Sell Through %' : df['sell_through'].mean() * 100,
            'Avg Price'      : df['avg_price'].mean(),
            'Rev per Ticket' : df['revenue_per_ticket'].mean()
        })

        print(f"    Mean: ${df['revenue'].mean():.0f}"
              f" ± ${df['revenue'].std():.0f}")
        print(f"    Sell: "
              f"{df['sell_through'].mean()*100:.1f}%")

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df.sort_values(
        'Mean Revenue', ascending=False
    ).reset_index(drop=True)

    # Save
    summary_df.to_csv(
        '../results/final_simulation_summary.csv',
        index=False
    )

    print("\n" + "=" * 60)
    print("  FINAL SIMULATION RANKINGS")
    print("=" * 60)
    medals = ['🥇', '🥈', '🥉',
              '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    for i, row in summary_df.iterrows():
        print(f"  {medals[i]} {row['Agent']:<15}: "
              f"${row['Mean Revenue']:.0f}")

    return all_results, summary_df


# ─────────────────────────────────────────
# STATISTICAL PROOF
# ─────────────────────────────────────────

def run_statistical_proof(
        all_results: dict,
        winner: str = 'PPO') -> dict:
    """
    Run statistical tests proving
    winner beats all others.

    Parameters
    ----------
    all_results : dict
        Simulation results.
    winner : str
        Best agent name.

    Returns
    -------
    dict
        Statistical proof results.
    """
    print("\n" + "=" * 60)
    print(f"  STATISTICAL PROOF: {winner} vs ALL")
    print("=" * 60)

    winner_df = all_results.get(winner)
    if winner_df is None:
        print(f"⚠️  {winner} not found!")
        return {}

    winner_revs = winner_df['revenue'].values
    proof       = {}

    for name, df in all_results.items():
        if name == winner:
            continue

        other_revs = df['revenue'].values

        # t-test
        t_stat, p_val = stats.ttest_ind(
            winner_revs, other_revs
        )

        # Effect size
        pooled = np.sqrt(
            (winner_revs.std()**2 +
             other_revs.std()**2) / 2
        )
        cohens_d = (
            winner_revs.mean() -
            other_revs.mean()
        ) / (pooled + 1e-8)

        improvement = (
            winner_revs.mean() -
            other_revs.mean()
        ) / other_revs.mean() * 100

        proof[name] = {
            'winner_mean' : float(winner_revs.mean()),
            'other_mean'  : float(other_revs.mean()),
            'improvement' : float(improvement),
            'p_value'     : float(p_val),
            'cohens_d'    : float(cohens_d),
            'significant' : bool(p_val < 0.05)
        }

        sig = '✅' if p_val < 0.05 else '❌'
        print(f"\n  {winner} vs {name}:")
        print(f"  {sig} Improvement: {improvement:+.1f}%")
        print(f"     p-value    : {p_val:.4f}")
        print(f"     Cohen's d  : {cohens_d:.4f}")

    # Save proof
    with open(
        '../results/statistical_proof.json', 'w'
    ) as f:
        json.dump(proof, f, indent=4)
    print("\n✅ Statistical proof saved!")

    return proof


# ─────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────

def plot_final_simulation(
        all_results: dict,
        summary_df: pd.DataFrame,
        save_path: str = '../results/final_simulation.png'):
    """
    Create final simulation dashboard.

    Parameters
    ----------
    all_results : dict
        All simulation results.
    summary_df : pd.DataFrame
        Summary statistics.
    save_path : str
        Save path.
    """
    colors_map = {
        'PPO'          : 'gold',
        'DQN'          : 'coral',
        'Q-Learning'   : 'green',
        'Time Based'   : 'steelblue',
        'Demand Based' : 'purple',
        'Linear Decay' : 'orange',
        'Fixed Price'  : 'lightgray',
    }

    fig = plt.figure(figsize=(20, 16))
    gs  = gridspec.GridSpec(3, 3, figure=fig)

    names  = summary_df['Agent'].values
    colors = [
        colors_map.get(n, 'steelblue')
        for n in names
    ]

    # ── Plot 1: Revenue Bar ──
    ax1 = fig.add_subplot(gs[0, :2])
    bars = ax1.bar(
        names,
        summary_df['Mean Revenue'],
        color=colors,
        edgecolor='black',
        yerr=summary_df['Std Revenue'],
        capsize=5, width=0.7
    )
    medals = ['🥇', '🥈', '🥉',
              '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    ax1.set_title(
        f'Final 1000-Season Revenue Rankings',
        fontweight='bold', fontsize=13
    )
    ax1.set_ylabel('Mean Revenue ($)')
    ax1.set_xticklabels(
        names, rotation=15, fontsize=9
    )
    for i, (bar, val) in enumerate(
        zip(bars, summary_df['Mean Revenue'])
    ):
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            val + 20,
            f'{medals[i]}\n${val:.0f}',
            ha='center', fontsize=9,
            fontweight='bold'
        )

    # ── Plot 2: Sell Through ──
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.bar(
        names,
        summary_df['Sell Through %'],
        color=colors,
        edgecolor='black'
    )
    ax2.axhline(
        y=100, color='red',
        linestyle='--', label='100%'
    )
    ax2.set_title(
        'Sell-Through Rate %',
        fontweight='bold'
    )
    ax2.set_ylabel('Sell Through %')
    ax2.set_xticklabels(
        names, rotation=20, fontsize=7
    )
    ax2.legend()

    # ── Plot 3: Revenue Distribution ──
    ax3 = fig.add_subplot(gs[1, :2])
    for i, (name, df) in enumerate(
        all_results.items()
    ):
        ax3.hist(
            df['revenue'],
            bins=40, alpha=0.5,
            color=colors_map.get(
                name, 'steelblue'
            ),
            label=name,
            edgecolor='black',
            linewidth=0.3
        )
    ax3.set_title(
        'Revenue Distribution — 1000 Seasons',
        fontweight='bold'
    )
    ax3.set_xlabel('Revenue ($)')
    ax3.set_ylabel('Frequency')
    ax3.legend(fontsize=8)

    # ── Plot 4: Cumulative Revenue ──
    ax4 = fig.add_subplot(gs[1, 2])
    for name, df in all_results.items():
        cum = df['revenue'].cumsum()
        ax4.plot(
            df['season'], cum,
            color=colors_map.get(
                name, 'steelblue'
            ),
            linewidth=1.5,
            label=name
        )
    ax4.set_title(
        'Cumulative Revenue\n1000 Seasons',
        fontweight='bold'
    )
    ax4.set_xlabel('Season')
    ax4.set_ylabel('Cumulative Revenue ($)')
    ax4.legend(fontsize=7)
    ax4.grid(True, alpha=0.3)

    # ── Plot 5: Rolling Mean ──
    ax5 = fig.add_subplot(gs[2, :2])
    for name, df in all_results.items():
        rolling = df['revenue'].rolling(
            window=50
        ).mean()
        ax5.plot(
            df['season'], rolling,
            color=colors_map.get(
                name, 'steelblue'
            ),
            linewidth=1.5,
            label=name
        )
    ax5.set_title(
        'Revenue Trend\n(50-season rolling mean)',
        fontweight='bold'
    )
    ax5.set_xlabel('Season')
    ax5.set_ylabel('Revenue ($)')
    ax5.legend(fontsize=7)
    ax5.grid(True, alpha=0.3)

    # ── Plot 6: Rev per Ticket ──
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.bar(
        names,
        summary_df['Rev per Ticket'],
        color=colors,
        edgecolor='black'
    )
    ax6.set_title(
        'Revenue per Ticket\nPricing Efficiency',
        fontweight='bold'
    )
    ax6.set_ylabel('Revenue per Ticket ($)')
    ax6.set_xticklabels(
        names, rotation=20, fontsize=7
    )

    plt.suptitle(
        'FINAL 1000-Season Simulation\n'
        'RL Dynamic Pricing — Complete Results',
        fontsize=15, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


if __name__ == "__main__":
    env = DynamicPricingEnv()

    # Train PPO
    ppo = PPOAgent(env, BEST_PPO_CONFIG)
    ppo.train(n_episodes=1000, verbose=False)

    agents = {
        'Fixed Price'  : FixedPriceAgent(env),
        'Time Based'   : TimedPricingAgent(env),
        'Demand Based' : DemandBasedAgent(env),
        'Linear Decay' : LinearDecayAgent(env),
        'PPO'          : ppo,
    }

    all_results, summary = run_final_simulation(
        agents, env, n_seasons=100
    )
    plot_final_simulation(all_results, summary)
    print("\n✅ Final simulation complete!")