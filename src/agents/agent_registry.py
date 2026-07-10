"""
agent_registry.py
=================
Central registry for all pricing agents.
Makes it easy to create and compare agents.

Infotact DS/ML Internship — Project 2
Week 1 : Agent Registry
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv
from environment.env_config import (
    ENV_CONFIG,
    Q_LEARNING_CONFIG
)
from agents.baseline_agents import (
    FixedPriceAgent,
    RandomAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)
from agents.q_learning_agent import QLearningAgent


# ─────────────────────────────────────────
# AGENT REGISTRY
# ─────────────────────────────────────────

AGENT_REGISTRY = {
    'fixed'    : FixedPriceAgent,
    'random'   : RandomAgent,
    'timed'    : TimedPricingAgent,
    'demand'   : DemandBasedAgent,
    'decay'    : LinearDecayAgent,
    'qlearning': QLearningAgent,
}


def create_agent(agent_type: str,
                 env: DynamicPricingEnv,
                 **kwargs):
    """
    Create agent by type name.

    Parameters
    ----------
    agent_type : str
        Agent type from registry.
    env : DynamicPricingEnv
        Environment instance.
    **kwargs
        Additional agent parameters.

    Returns
    -------
    Agent instance.
    """
    if agent_type not in AGENT_REGISTRY:
        raise ValueError(
            f"Unknown agent: {agent_type}\n"
            f"Available: {list(AGENT_REGISTRY.keys())}"
        )
    return AGENT_REGISTRY[agent_type](env, **kwargs)


def create_all_baseline_agents(
        env: DynamicPricingEnv) -> list:
    """
    Create all baseline agents.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment instance.

    Returns
    -------
    list
        List of baseline agents.
    """
    return [
        FixedPriceAgent(env),
        RandomAgent(env),
        TimedPricingAgent(env),
        DemandBasedAgent(env),
        LinearDecayAgent(env)
    ]


def create_ql_agent(
        env: DynamicPricingEnv,
        config: dict = None,
        train: bool = True,
        n_episodes: int = 5000) -> QLearningAgent:
    """
    Create and optionally train Q-Learning agent.

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment instance.
    config : dict
        Q-Learning config.
    train : bool
        Whether to train immediately.
    n_episodes : int
        Training episodes.

    Returns
    -------
    QLearningAgent
        Created (and optionally trained) agent.
    """
    config = config or Q_LEARNING_CONFIG
    agent  = QLearningAgent(env, config)

    if train:
        print(f"Training Q-Learning "
              f"({n_episodes} episodes)...")
        agent.train(
            n_episodes=n_episodes,
            verbose=False
        )
        print(f"✅ Training complete!")

    return agent


def list_available_agents() -> None:
    """Print all available agents."""
    print("=" * 40)
    print("  AVAILABLE AGENTS")
    print("=" * 40)
    for key, cls in AGENT_REGISTRY.items():
        print(f"  '{key}' → {cls.__name__}")
    print("=" * 40)


if __name__ == "__main__":
    list_available_agents()

    env   = DynamicPricingEnv()
    agent = create_agent('timed', env)
    print(f"\n✅ Created: {agent.name}")

    baselines = create_all_baseline_agents(env)
    print(f"✅ Created {len(baselines)} baselines")