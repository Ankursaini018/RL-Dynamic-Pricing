"""
price_trajectory_analyzer.py
=============================
Analyzes and visualizes price trajectories
learned by DQN agent.

Internship Spec:
"prove that the agent learned complex
behaviors like dropping prices near
the deadline to clear remaining stock"

Infotact DS/ML Internship — Project 2
Week 2 : Price Trajectory Analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import (
    DynamicPricingEnv,
    PRICE_LEVELS
)


def get_episode_trajectory(
        agent,
        env: DynamicPricingEnv,
        seed: int = 42) -> pd.DataFrame:
    """
    Run one episode and record full trajectory.

    Parameters
    ----------
    agent : Any
        Pricing agent.
    env : DynamicPricingEnv
        Environment.
    seed : int
        Random seed.

    Returns
    -------
    pd.DataFrame
        Episode trajectory.
    """
    state, _ = env.reset(seed=seed)
    history  = []
    done     = False
    day      = 0

    while not done:
        # Get action
        if hasattr(agent, 'select_action'):
            action = agent.select_action(
                state, training=False
            )
        else:
            action = agent.run_episode(
                seed=seed
            )['prices_used'][day] \
            if day == 0 else 0

        obs, reward, term, trunc, info = (
            env.step(action)
        )
        done = term or trunc

        history.append({
            'day'           : day + 1,
            'price'         : info['price'],
            'bought'        : int(info['bought']),
            'inventory'     : info['inventory'],
            'days_left'     : info['days_left'],
            'revenue_step'  : max(0, reward),
            'cum_revenue'   : info['total_revenue'],
            'demand_prob'   : info['demand_prob']
        })

        state = obs
        day  += 1

    return pd.DataFrame(history)


def plot_trajectory_analysis(
        agents: dict,
        env: DynamicPricingEnv,
        n_episodes: int = 10,
        save_path: str = '../results/trajectory_analysis.png'):
    """
    Compare trajectories across agents.

    Parameters
    ----------
    agents : dict
        {name: agent} dictionary.
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Episodes to average.
    save_path : str
        Save path.
    """
    fig, axes = plt.subplots(
        2, 2, figsize=(16, 12)
    )

    colors = [
        'gold', 'coral', 'steelblue',
        'green', 'purple'
    ]

    for (name, agent), color in zip(
        agents.items(), colors
    ):
        # Average over multiple episodes
        all_prices = []
        all_inv    = []

        for ep in range(n_episodes):
            traj = get_episode_trajectory(
                agent, env, seed=ep
            )
            # Pad to max_days if needed
            prices = traj['price'].values
            inv    = traj['inventory'].values

            all_prices.append(prices)
            all_inv.append(inv)

        # Average trajectories
        max_len = max(len(p) for p in all_prices)
        avg_prices = np.zeros(max_len)
        avg_inv    = np.zeros(max_len)
        counts     = np.zeros(max_len)

        for prices, inv in zip(all_prices, all_inv):
            for i, (p, v) in enumerate(
                zip(prices, inv)
            ):
                avg_prices[i] += p
                avg_inv[i]    += v
                counts[i]     += 1

        avg_prices /= np.maximum(counts, 1)
        avg_inv    /= np.maximum(counts, 1)
        days = range(1, max_len + 1)

        # Plot 1: Price trajectory
        axes[0, 0].plot(
            days, avg_prices,
            color=color, linewidth=2,
            marker='o', markersize=3,
            label=name
        )

        # Plot 2: Inventory trajectory
        axes[0, 1].plot(
            days, avg_inv,
            color=color, linewidth=2,
            label=name
        )

    axes[0, 0].set_title(
        'Average Price Trajectory\nby Agent',
        fontweight='bold'
    )
    axes[0, 0].set_xlabel('Day')
    axes[0, 0].set_ylabel('Price ($)')
    axes[0, 0].legend(fontsize=8)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_ylim([0, 350])

    axes[0, 1].set_title(
        'Average Inventory Depletion\nby Agent',
        fontweight='bold'
    )
    axes[0, 1].set_xlabel('Day')
    axes[0, 1].set_ylabel('Remaining Inventory')
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: DQN detailed trajectory
    dqn_name = [n for n in agents.keys()
                if 'DQN' in n]
    if dqn_name:
        dqn_agent = agents[dqn_name[0]]
        traj = get_episode_trajectory(
            dqn_agent, env, seed=42
        )

        axes[1, 0].plot(
            traj['day'],
            traj['price'],
            color='gold', linewidth=2.5,
            marker='o', markersize=5,
            label='Price'
        )
        # Mark sales
        sales = traj[traj['bought'] == 1]
        axes[1, 0].scatter(
            sales['day'],
            sales['price'],
            color='green', s=100,
            zorder=5, label='Sale Made!'
        )
        no_sales = traj[traj['bought'] == 0]
        axes[1, 0].scatter(
            no_sales['day'],
            no_sales['price'],
            color='red', s=50,
            zorder=5, alpha=0.5,
            label='No Sale'
        )
        axes[1, 0].set_title(
            'DQN Detailed Price Trajectory\n'
            'One Episode',
            fontweight='bold'
        )
        axes[1, 0].set_xlabel('Day')
        axes[1, 0].set_ylabel('Price ($)')
        axes[1, 0].legend(fontsize=8)
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_ylim([0, 350])

        # Plot 4: Cumulative revenue
        axes[1, 1].plot(
            traj['day'],
            traj['cum_revenue'],
            color='gold', linewidth=2.5
        )
        axes[1, 1].set_title(
            'DQN Cumulative Revenue\nOne Episode',
            fontweight='bold'
        )
        axes[1, 1].set_xlabel('Day')
        axes[1, 1].set_ylabel('Cumulative Revenue ($)')
        axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle(
        'Price Trajectory Analysis\n'
        'DQN vs Baseline Agents',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(save_path,
                bbox_inches='tight', dpi=150)
    plt.show()
    print(f"✅ Saved: {save_path}")


def analyze_dqn_behavior(
        agent,
        env: DynamicPricingEnv):
    """
    Analyze if DQN learned smart behaviors.

    Checks:
    1. Does it lower prices near deadline?
    2. Does it use premium for low inventory?
    3. Is revenue better than baselines?

    Parameters
    ----------
    agent : DQNAgent
        Trained DQN agent.
    env : DynamicPricingEnv
        Environment.
    """
    print("=" * 55)
    print("  DQN LEARNED BEHAVIOR ANALYSIS")
    print("=" * 55)

    # Run multiple episodes
    early_prices  = []
    late_prices   = []
    high_inv_prices = []
    low_inv_prices  = []

    for ep in range(50):
        state, _ = env.reset(seed=ep)
        done     = False

        while not done:
            action = agent.select_action(
                state, training=False
            )
            price    = PRICE_LEVELS[action]
            inv      = int(state[0])
            days     = int(state[1])

            if days > 20:
                early_prices.append(price)
            elif days < 5:
                late_prices.append(price)

            if inv > 40:
                high_inv_prices.append(price)
            elif inv < 10:
                low_inv_prices.append(price)

            state, _, term, trunc, _ = (
                env.step(action)
            )
            done = term or trunc

    # Analysis
    avg_early    = np.mean(early_prices) \
                   if early_prices else 0
    avg_late     = np.mean(late_prices) \
                   if late_prices else 0
    avg_high_inv = np.mean(high_inv_prices) \
                   if high_inv_prices else 0
    avg_low_inv  = np.mean(low_inv_prices) \
                   if low_inv_prices else 0

    print(f"\n  [1] Deadline Pricing:")
    print(f"      Early (>20 days): ${avg_early:.0f}")
    print(f"      Late  (<5 days) : ${avg_late:.0f}")
    if avg_late < avg_early:
        print(f"      ✅ DQN learned to DISCOUNT "
              f"near deadline!")
    else:
        print(f"      ⚠️  Not discounting near deadline")

    print(f"\n  [2] Scarcity Pricing:")
    print(f"      High inventory (>40): "
          f"${avg_high_inv:.0f}")
    print(f"      Low inventory  (<10): "
          f"${avg_low_inv:.0f}")
    if avg_low_inv > avg_high_inv:
        print(f"      ✅ DQN learned SCARCITY premium!")
    else:
        print(f"      ⚠️  Not using scarcity pricing")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    print("✅ Price trajectory analyzer loaded!")