"""
training_visualizer.py
======================
Visualization utilities for
RL training progress.

Infotact DS/ML Internship — Project 2
Week 1 : Training Visualization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_learning_curve(
        rewards: list,
        agent_name: str,
        window: int = 100,
        save_path: str = None):
    """
    Plot smoothed learning curve.

    Parameters
    ----------
    rewards : list
        Episode rewards.
    agent_name : str
        Agent name for title.
    window : int
        Smoothing window size.
    save_path : str
        Save path.
    """
    smooth = pd.Series(rewards).rolling(
        window=window
    ).mean()

    plt.figure(figsize=(12, 5))
    plt.plot(
        rewards,
        alpha=0.2,
        color='steelblue',
        linewidth=0.8,
        label='Raw'
    )
    plt.plot(
        smooth,
        color='red',
        linewidth=2.5,
        label=f'{window}-ep Average'
    )
    plt.title(
        f'{agent_name} — Learning Curve',
        fontweight='bold',
        fontsize=13
    )
    plt.xlabel('Episode')
    plt.ylabel('Total Revenue ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path,
                    bbox_inches='tight',
                    dpi=150)
        print(f"✅ Saved: {save_path}")
    plt.show()


def plot_price_trajectory(
        prices: list,
        agent_name: str,
        revenue: float,
        save_path: str = None):
    """
    Plot price trajectory for one episode.

    Parameters
    ----------
    prices : list
        Prices used each day.
    agent_name : str
        Agent name.
    revenue : float
        Total revenue.
    save_path : str
        Save path.
    """
    plt.figure(figsize=(12, 5))
    plt.plot(
        prices,
        marker='o',
        markersize=5,
        linewidth=2,
        color='steelblue'
    )
    plt.fill_between(
        range(len(prices)),
        prices,
        alpha=0.15,
        color='steelblue'
    )
    plt.title(
        f'{agent_name} — Price Trajectory\n'
        f'Total Revenue: ${revenue:.0f}',
        fontweight='bold',
        fontsize=13
    )
    plt.xlabel('Day')
    plt.ylabel('Price ($)')
    plt.ylim([0, 350])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path,
                    bbox_inches='tight',
                    dpi=150)
        print(f"✅ Saved: {save_path}")
    plt.show()


def plot_revenue_comparison(
        results: dict,
        title: str = 'Agent Comparison',
        save_path: str = None):
    """
    Bar chart comparing agent revenues.

    Parameters
    ----------
    results : dict
        {agent_name: mean_revenue}
    title : str
        Chart title.
    save_path : str
        Save path.
    """
    names    = list(results.keys())
    revenues = list(results.values())
    colors   = [
        'gold' if 'Q-Learning' in n or 'DQN' in n
        else 'steelblue'
        for n in names
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(
        names, revenues,
        color=colors,
        edgecolor='black',
        width=0.6
    )
    ax.set_title(title, fontweight='bold',
                 fontsize=13)
    ax.set_ylabel('Mean Revenue ($)')
    plt.xticks(rotation=15, fontsize=9)

    for bar, val in zip(bars, revenues):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            val + 50,
            f'${val:.0f}',
            ha='center',
            fontweight='bold',
            fontsize=10
        )

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path,
                    bbox_inches='tight',
                    dpi=150)
        print(f"✅ Saved: {save_path}")
    plt.show()


if __name__ == "__main__":
    print("✅ training_visualizer.py loaded!")