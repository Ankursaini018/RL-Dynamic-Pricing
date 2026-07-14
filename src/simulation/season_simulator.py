"""
season_simulator.py
===================
Runs 1000 simulated booking seasons
to evaluate DQN agent performance.

Internship Spec:
"run 1,000 simulated booking seasons
to evaluate the DQN agent against
naive baselines"

Infotact DS/ML Internship — Project 2
Week 2 : 1000 Season Simulation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import sys
from tqdm import tqdm

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)
from agents.baseline_agents import (
    FixedPriceAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)

os.makedirs('../results', exist_ok=True)
os.makedirs('../src/simulation', exist_ok=True)


# ─────────────────────────────────────────
# SINGLE AGENT SIMULATION
# ─────────────────────────────────────────

def simulate_agent(agent,
                   env: DynamicPricingEnv,
                   n_seasons: int = 1000,
                   seed: int = 42) -> pd.DataFrame:

    name = getattr(agent, "name", "Agent")
    results = []

    for season in range(n_seasons):

        # -----------------------------
        # Baseline Agents
        # -----------------------------
        if hasattr(agent, "run_episode"):

            result = agent.run_episode(
                seed=seed + season
            )

            total_revenue = result["total_revenue"]
            total_sold = result["total_sold"]
            prices_used = result["prices_used"]

        # -----------------------------
        # RL Agents
        # -----------------------------
        else:

            state, _ = env.reset(seed=seed + season)

            total_revenue = 0
            total_sold = 0
            prices_used = []

            done = False

            while not done:

                try:
                    action = agent.select_action(
                        state,
                        training=False
                    )

                except TypeError:
                    action = agent.select_action(state)

                state, reward, terminated, truncated, info = (
                    env.step(action)
                )

                done = terminated or truncated

                total_revenue += max(0, reward)

                prices_used.append(
                    info["price"]
                )

                if info["bought"]:
                    total_sold += 1

        results.append({

            "season": season + 1,
            "agent": name,

            "revenue": total_revenue,

            "tickets_sold": total_sold,

            "sell_through":
                total_sold /
                env.max_inventory,

            "avg_price":
                np.mean(prices_used),

            "max_price":
                np.max(prices_used),

            "min_price":
                np.min(prices_used),

            "revenue_per_ticket":
                (
                    total_revenue /
                    total_sold
                )
                if total_sold > 0
                else 0
        })

    return pd.DataFrame(results)


# ─────────────────────────────────────────
# MULTI-AGENT SIMULATION
# ─────────────────────────────────────────

def run_1000_season_simulation(
        agents: dict,
        env: DynamicPricingEnv,
        n_seasons: int = 1000) -> dict:
    """
    Run 1000-season simulation for all agents.

    Parameters
    ----------
    agents : dict
        {name: agent} dictionary.
    env : DynamicPricingEnv
        Pricing environment.
    n_seasons : int
        Seasons per agent.

    Returns
    -------
    dict
        {name: results_df} dictionary.
    """
    print("=" * 60)
    print(f"  {n_seasons}-SEASON SIMULATION")
    print("  Comparing all pricing strategies")
    print("=" * 60)

    all_results  = {}
    summary_rows = []

    for name, agent in agents.items():
        print(f"\n  Simulating: {name}...")
        df = simulate_agent(
            agent, env,
            n_seasons=n_seasons
        )
        all_results[name] = df

        # Summary stats
        summary_rows.append({
            'Agent'            : name,
            'Mean Revenue'     : df['revenue'].mean(),
            'Std Revenue'      : df['revenue'].std(),
            'Max Revenue'      : df['revenue'].max(),
            'Min Revenue'      : df['revenue'].min(),
            'Mean Sold'        : df['tickets_sold'].mean(),
            'Sell Through %'   : df['sell_through'].mean() * 100,
            'Avg Price'        : df['avg_price'].mean(),
            'Rev per Ticket'   : df['revenue_per_ticket'].mean()
        })

        print(f"    Mean Revenue : "
              f"${df['revenue'].mean():.0f}"
              f" ± ${df['revenue'].std():.0f}")
        print(f"    Sell Through : "
              f"{df['sell_through'].mean()*100:.1f}%")

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df.sort_values(
        'Mean Revenue', ascending=False
    ).reset_index(drop=True)

    print("\n" + "=" * 60)
    print("  SIMULATION SUMMARY")
    print("=" * 60)
    print(summary_df[[
        'Agent', 'Mean Revenue',
        'Std Revenue', 'Sell Through %'
    ]].to_string(index=False))

    # Save results
    summary_df.to_csv(
        '../results/simulation_1000_summary.csv',
        index=False
    )
    print("\n✅ Summary saved!")

    return all_results, summary_df


# ─────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────

def plot_simulation_results(
        all_results: dict,
        summary_df: pd.DataFrame,
        save_path: str = '../results/simulation_results.png'):
    """
    Comprehensive visualization of 1000-season results.

    Parameters
    ----------
    all_results : dict
        Simulation results.
    summary_df : pd.DataFrame
        Summary statistics.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))

    colors = ['gold', 'coral', 'steelblue',
              'green', 'purple', 'orange']
    names  = list(all_results.keys())

    # ── Plot 1: Revenue Distribution ──
    for i, (name, df) in enumerate(
        all_results.items()
    ):
        axes[0, 0].hist(
            df['revenue'],
            bins=40, alpha=0.6,
            color=colors[i % len(colors)],
            label=name,
            edgecolor='black',
            linewidth=0.5
        )
    axes[0, 0].set_title(
        'Revenue Distribution\n1000 Seasons',
        fontweight='bold'
    )
    axes[0, 0].set_xlabel('Revenue ($)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend(fontsize=7)

    # ── Plot 2: Mean Revenue Bar ──
    bars = axes[0, 1].bar(
        summary_df['Agent'],
        summary_df['Mean Revenue'],
        color=colors[:len(summary_df)],
        edgecolor='black',
        yerr=summary_df['Std Revenue'],
        capsize=5
    )
    axes[0, 1].set_title(
        'Mean Revenue by Agent\n(±std)',
        fontweight='bold'
    )
    axes[0, 1].set_ylabel('Mean Revenue ($)')
    axes[0, 1].set_xticklabels(
        summary_df['Agent'],
        rotation=20, fontsize=8
    )
    for bar, val in zip(
        bars, summary_df['Mean Revenue']
    ):
        axes[0, 1].text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 50,
            f'${val:.0f}',
            ha='center', fontsize=8,
            fontweight='bold'
        )

    # ── Plot 3: Sell Through Rate ──
    axes[0, 2].bar(
        summary_df['Agent'],
        summary_df['Sell Through %'],
        color=colors[:len(summary_df)],
        edgecolor='black'
    )
    axes[0, 2].set_title(
        'Sell-Through Rate\n(% tickets sold)',
        fontweight='bold'
    )
    axes[0, 2].set_ylabel('Sell Through %')
    axes[0, 2].set_xticklabels(
        summary_df['Agent'],
        rotation=20, fontsize=8
    )
    axes[0, 2].axhline(
        y=100, color='red',
        linestyle='--',
        label='100% target'
    )
    axes[0, 2].legend()

    # ── Plot 4: Revenue Rolling Mean ──
    for i, (name, df) in enumerate(
        all_results.items()
    ):
        rolling = df['revenue'].rolling(
            window=50
        ).mean()
        axes[1, 0].plot(
            df['season'],
            rolling,
            color=colors[i % len(colors)],
            linewidth=1.5,
            label=name
        )
    axes[1, 0].set_title(
        'Revenue Trend\n(50-season rolling mean)',
        fontweight='bold'
    )
    axes[1, 0].set_xlabel('Season')
    axes[1, 0].set_ylabel('Revenue ($)')
    axes[1, 0].legend(fontsize=7)
    axes[1, 0].grid(True, alpha=0.3)

    # ── Plot 5: Revenue per Ticket ──
    axes[1, 1].bar(
        summary_df['Agent'],
        summary_df['Rev per Ticket'],
        color=colors[:len(summary_df)],
        edgecolor='black'
    )
    axes[1, 1].set_title(
        'Revenue per Ticket Sold\n(Pricing Efficiency)',
        fontweight='bold'
    )
    axes[1, 1].set_ylabel('Revenue per Ticket ($)')
    axes[1, 1].set_xticklabels(
        summary_df['Agent'],
        rotation=20, fontsize=8
    )

    # ── Plot 6: Avg Price Used ──
    axes[1, 2].bar(
        summary_df['Agent'],
        summary_df['Avg Price'],
        color=colors[:len(summary_df)],
        edgecolor='black'
    )
    axes[1, 2].set_title(
        'Average Price Used\nby Agent',
        fontweight='bold'
    )
    axes[1, 2].set_ylabel('Average Price ($)')
    axes[1, 2].set_xticklabels(
        summary_df['Agent'],
        rotation=20, fontsize=8
    )

    plt.suptitle(
        '1000-Season Simulation Results\n'
        'Dynamic Pricing Strategy Comparison',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


# ─────────────────────────────────────────
# STATISTICAL ANALYSIS
# ─────────────────────────────────────────

def statistical_comparison(
        all_results: dict,
        dqn_name: str = 'DQN 🤖') -> pd.DataFrame:
    """
    Statistical comparison of DQN vs baselines.

    Parameters
    ----------
    all_results : dict
        Simulation results.
    dqn_name : str
        Name of DQN agent.

    Returns
    -------
    pd.DataFrame
        Statistical comparison results.
    """
    from scipy import stats

    if dqn_name not in all_results:
        print(f"⚠️ {dqn_name} not found!")
        return pd.DataFrame()

    dqn_revenues = all_results[dqn_name]['revenue']

    print("=" * 55)
    print("  STATISTICAL COMPARISON")
    print(f"  DQN vs each baseline")
    print("=" * 55)

    rows = []
    for name, df in all_results.items():
        if name == dqn_name:
            continue

        bl_revenues = df['revenue']

        # t-test
        t_stat, p_value = stats.ttest_ind(
            dqn_revenues, bl_revenues
        )

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(
            (dqn_revenues.std()**2 +
             bl_revenues.std()**2) / 2
        )
        cohens_d = (
            dqn_revenues.mean() -
            bl_revenues.mean()
        ) / pooled_std

        improvement = (
            (dqn_revenues.mean() -
             bl_revenues.mean()) /
            bl_revenues.mean() * 100
        )

        rows.append({
            'Baseline'     : name,
            'DQN Mean'     : dqn_revenues.mean(),
            'BL Mean'      : bl_revenues.mean(),
            'Improvement%' : improvement,
            'p-value'      : p_value,
            'Significant'  : p_value < 0.05,
            "Cohen's d"    : cohens_d
        })

        print(f"\n  vs {name}")
        print(f"  Improvement : {improvement:+.1f}%")
        print(f"  p-value     : {p_value:.4f}")
        print(f"  Significant : "
              f"{'✅ Yes' if p_value < 0.05 else '❌ No'}")
        print(f"  Cohen's d   : {cohens_d:.4f}")

    return pd.DataFrame(rows)


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    from agents.dqn.dqn_agent import DQNAgent
    from config import DQN

    env = DynamicPricingEnv()

    # Train DQN
    dqn = DQNAgent(env, DQN)
    dqn.train(n_episodes=1000, verbose=False)

    # Create agents
    agents = {
        'Fixed Price'  : FixedPriceAgent(env),
        'Time Based'   : TimedPricingAgent(env),
        'Demand Based' : DemandBasedAgent(env),
        'Linear Decay' : LinearDecayAgent(env),
        'DQN 🤖'       : dqn,
    }

    # Run simulation
    all_results, summary = run_1000_season_simulation(
        agents, env, n_seasons=100
    )

    # Plot
    plot_simulation_results(all_results, summary)

    # Statistical comparison
    stats_df = statistical_comparison(all_results)
    print(f"\n✅ Simulation complete!")