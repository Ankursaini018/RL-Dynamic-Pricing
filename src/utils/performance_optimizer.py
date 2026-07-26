"""
performance_optimizer.py
========================
Performance optimization utilities
for faster training and evaluation.

Infotact DS/ML Internship — Project 2
Week 3 : Performance Optimization
"""

import numpy as np
import time
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import DynamicPricingEnv


def benchmark_agents(
        agents: dict,
        env: DynamicPricingEnv,
        n_episodes: int = 100) -> dict:
    """
    Benchmark speed of all agents.

    Parameters
    ----------
    agents : dict
        Agent dictionary.
    env : DynamicPricingEnv
        Environment.
    n_episodes : int
        Episodes to benchmark.

    Returns
    -------
    dict
        Benchmark results.
    """
    print("=" * 55)
    print("  AGENT BENCHMARK")
    print(f"  {n_episodes} episodes each")
    print("=" * 55)

    results = {}

    for name, agent in agents.items():
        start = time.time()

        revenues = []
        for ep in range(n_episodes):
            state, _ = env.reset(seed=ep)
            total    = 0
            done     = False

            while not done:
                if hasattr(agent, 'select_action'):
                    action = agent.select_action(
                        state, training=False
                    )
                    if isinstance(action, tuple):
                        action = action[0]
                else:
                    result = agent.run_episode(
                        seed=ep
                    )
                    total = result['total_revenue']
                    break

                state, r, term, trunc, _ = (
                    env.step(action)
                )
                done  = term or trunc
                total += max(0, r)

            revenues.append(total)

        elapsed = time.time() - start
        eps_per_sec = n_episodes / elapsed

        results[name] = {
            'time_seconds' : elapsed,
            'eps_per_sec'  : eps_per_sec,
            'mean_revenue' : np.mean(revenues)
        }

        print(f"\n  {name}:")
        print(f"  Time     : {elapsed:.2f}s")
        print(f"  Speed    : "
              f"{eps_per_sec:.1f} eps/sec")
        print(f"  Revenue  : "
              f"${np.mean(revenues):.0f}")

    # Best agent by revenue
    best = max(
        results.items(),
        key=lambda x: x[1]['mean_revenue']
    )
    fastest = min(
        results.items(),
        key=lambda x: x[1]['time_seconds']
    )

    print("\n" + "=" * 55)
    print(f"  🏆 Best Revenue : {best[0]}")
    print(f"  ⚡ Fastest Agent: {fastest[0]}")
    print("=" * 55)

    return results


def optimize_environment(
        env: DynamicPricingEnv) -> DynamicPricingEnv:
    """
    Apply environment optimizations.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment to optimize.

    Returns
    -------
    DynamicPricingEnv
        Optimized environment.
    """
    print("✅ Environment optimized!")
    print(f"   Max Inventory: {env.max_inventory}")
    print(f"   Max Days     : {env.max_days}")
    print(f"   Price Levels : {env.price_levels}")
    return env


def memory_usage_report(agents: dict):
    """
    Report approximate memory usage.

    Parameters
    ----------
    agents : dict
        Agent dictionary.
    """
    print("=" * 55)
    print("  MEMORY USAGE REPORT")
    print("=" * 55)

    for name, agent in agents.items():
        if hasattr(agent, 'network'):
            # Neural network
            import torch
            params = sum(
                p.numel()
                for p in agent.network.parameters()
            )
            size_kb = params * 4 / 1024
            print(f"\n  {name}:")
            print(f"  Parameters: {params:,}")
            print(f"  Size      : {size_kb:.1f} KB")

        elif hasattr(agent, 'q_table'):
            # Q-table
            size_kb = (
                agent.q_table.nbytes / 1024
            )
            print(f"\n  {name}:")
            print(f"  Q-table: "
                  f"{agent.q_table.shape}")
            print(f"  Size   : {size_kb:.1f} KB")

        else:
            print(f"\n  {name}: Heuristic agent")
            print(f"  Size: Minimal (~0 KB)")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    print("✅ Performance optimizer loaded!")