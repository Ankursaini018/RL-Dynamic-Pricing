"""
evaluator.py
============
Evaluation framework for comparing
pricing agents across multiple episodes.

Infotact DS/ML Internship — Project 2
Week 1 : Agent Evaluation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# --------------------------------------------------
# Add project src directory to Python path
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv


def evaluate_agent(agent,
                   n_episodes: int = 100,
                   seed: int = 42) -> pd.DataFrame:
    """
    Evaluate agent over multiple episodes.

    Parameters
    ----------
    agent : BaseAgent
        Agent to evaluate.
    n_episodes : int
        Number of episodes to run.
    seed : int
        Base random seed.

    Returns
    -------
    pd.DataFrame
        Results for all episodes.
    """
    results = []

    for ep in range(n_episodes):
        result = agent.run_episode(
            seed=seed + ep
        )
        result['episode'] = ep
        results.append(result)

    df = pd.DataFrame(results)
    return df


def compare_agents(agents: list,
                   n_episodes: int = 100) -> dict:
    """
    Compare multiple agents.

    Parameters
    ----------
    agents : list
        List of agent objects.
    n_episodes : int
        Episodes per agent.

    Returns
    -------
    dict
        Results for each agent.
    """
    print("=" * 55)
    print("  AGENT COMPARISON")
    print(f"  {n_episodes} episodes each")
    print("=" * 55)

    all_results = {}
    summary_rows = []

    for agent in agents:
        print(f"\n  Evaluating: {agent.name}...")
        df = evaluate_agent(agent, n_episodes)
        all_results[agent.name] = df

        summary_rows.append({
            'Agent'        : agent.name,
            'Mean Revenue' : df['total_revenue'].mean(),
            'Std Revenue'  : df['total_revenue'].std(),
            'Max Revenue'  : df['total_revenue'].max(),
            'Min Revenue'  : df['total_revenue'].min(),
            'Mean Sold'    : df['total_sold'].mean(),
            'Sell Through' : df['sell_through'].mean()
        })

        print(f"    Mean Revenue: "
              f"${df['total_revenue'].mean():.0f}"
              f" ± ${df['total_revenue'].std():.0f}")
        print(f"    Mean Sold   : "
              f"{df['total_sold'].mean():.1f}/50")

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df.sort_values(
        'Mean Revenue', ascending=False
    )

    print("\n" + "=" * 55)
    print("  SUMMARY RANKINGS")
    print("=" * 55)
    print(summary_df[[
        'Agent', 'Mean Revenue', 'Std Revenue',
        'Mean Sold'
    ]].to_string(index=False))

    return all_results, summary_df


def plot_agent_comparison(
        all_results: dict,
        summary_df: pd.DataFrame,
        save_path: str = '../results/agent_comparison.png'):
    """
    Plot agent comparison charts.

    Parameters
    ----------
    all_results : dict
        Results dictionary from compare_agents.
    summary_df : pd.DataFrame
        Summary statistics.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    colors = ['steelblue', 'coral', 'green',
              'purple', 'orange']
    agents = list(all_results.keys())

    # Plot 1: Revenue Distribution
    for i, (name, df) in enumerate(
        all_results.items()
    ):
        axes[0,0].hist(
            df['total_revenue'],
            bins=20,
            alpha=0.6,
            color=colors[i % len(colors)],
            label=name
        )
    axes[0,0].set_title(
        'Revenue Distribution by Agent',
        fontweight='bold'
    )
    axes[0,0].set_xlabel('Total Revenue ($)')
    axes[0,0].set_ylabel('Frequency')
    axes[0,0].legend(fontsize=8)

    # Plot 2: Mean Revenue Bar
    bars = axes[0,1].bar(
        summary_df['Agent'],
        summary_df['Mean Revenue'],
        color=colors[:len(summary_df)],
        edgecolor='black',
        yerr=summary_df['Std Revenue'],
        capsize=5
    )
    axes[0,1].set_title(
        'Mean Revenue by Agent\n(with std error)',
        fontweight='bold'
    )
    axes[0,1].set_ylabel('Mean Revenue ($)')
    axes[0,1].set_xticklabels(
        summary_df['Agent'],
        rotation=15,
        fontsize=8
    )
    for bar, val in zip(
        bars, summary_df['Mean Revenue']
    ):
        axes[0,1].text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 100,
            f'${val:.0f}',
            ha='center',
            fontsize=8,
            fontweight='bold'
        )

    # Plot 3: Sell Through Rate
    axes[1,0].bar(
        summary_df['Agent'],
        summary_df['Sell Through'] * 100,
        color=colors[:len(summary_df)],
        edgecolor='black'
    )
    axes[1,0].set_title(
        'Sell-Through Rate by Agent',
        fontweight='bold'
    )
    axes[1,0].set_ylabel('Sell Through %')
    axes[1,0].set_xticklabels(
        summary_df['Agent'],
        rotation=15,
        fontsize=8
    )
    axes[1,0].axhline(
        y=100,
        color='red',
        linestyle='--',
        label='100% sold'
    )
    axes[1,0].legend()

    # Plot 4: Revenue over Episodes
    for i, (name, df) in enumerate(
        all_results.items()
    ):
        rolling_mean = df['total_revenue'].rolling(
            window=10
        ).mean()
        axes[1,1].plot(
            rolling_mean,
            color=colors[i % len(colors)],
            linewidth=2,
            label=name
        )
    axes[1,1].set_title(
        'Revenue Trend (10-ep rolling mean)',
        fontweight='bold'
    )
    axes[1,1].set_xlabel('Episode')
    axes[1,1].set_ylabel('Revenue ($)')
    axes[1,1].legend(fontsize=8)
    axes[1,1].grid(True, alpha=0.3)

    plt.suptitle(
        'Baseline Agent Comparison\n'
        'Dynamic Pricing Environment',
        fontsize=14,
        fontweight='bold'
    )
    import os

plt.tight_layout()

# ----------------------------------------
# Create results directory automatically
# ----------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)

SAVE_PATH = os.path.join(
    RESULTS_DIR,
    "agent_comparison.png"
)

plt.savefig(
    SAVE_PATH,
    bbox_inches="tight",
    dpi=150
)

plt.show()

print(f"✅ Saved: {SAVE_PATH}")


if __name__ == "__main__":
    from agents.baseline_agents import (
        FixedPriceAgent, RandomAgent,
        TimedPricingAgent, DemandBasedAgent,
        LinearDecayAgent
    )

    env = DynamicPricingEnv()
    agents = [
        FixedPriceAgent(env),
        RandomAgent(env),
        TimedPricingAgent(env),
        DemandBasedAgent(env),
        LinearDecayAgent(env)
    ]

    all_results, summary = compare_agents(
        agents, n_episodes=100
    )
    plot_agent_comparison(all_results, summary)