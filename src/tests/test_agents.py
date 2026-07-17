"""
test_agents.py
==============
Unit tests for all pricing agents.

Infotact DS/ML Internship — Project 2
Week 2 : Agent Testing
"""

import numpy as np
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv
from agents.baseline_agents import (
    FixedPriceAgent,
    RandomAgent,
    TimedPricingAgent,
    DemandBasedAgent,
    LinearDecayAgent
)
from agents.q_learning_agent import QLearningAgent
from agents.dqn.dqn_agent import DQNAgent
from agents.dqn.replay_buffer import ReplayBuffer
from agents.dqn.dqn_network import DQNNetwork
from config import DQN, Q_LEARNING


# ─────────────────────────────────────────
# BASELINE TESTS
# ─────────────────────────────────────────

def test_fixed_price_agent():
    """Test Fixed Price agent works."""
    env   = DynamicPricingEnv()
    agent = FixedPriceAgent(env, price_idx=2)

    result = agent.run_episode(seed=42)
    assert result['total_revenue'] >= 0
    assert result['total_sold'] >= 0
    assert result['total_sold'] <= env.max_inventory
    assert len(result['prices_used']) > 0
    assert all(
        p == 150 for p in result['prices_used']
    )
    print("✅ test_fixed_price_agent passed!")


def test_random_agent():
    """Test Random agent works."""
    env   = DynamicPricingEnv()
    agent = RandomAgent(env)

    result = agent.run_episode(seed=42)
    assert result['total_revenue'] >= 0
    assert len(result['prices_used']) > 0
    print("✅ test_random_agent passed!")


def test_timed_pricing_agent():
    """Test Timed Pricing agent works."""
    env   = DynamicPricingEnv()
    agent = TimedPricingAgent(env)

    result = agent.run_episode(seed=42)
    assert result['total_revenue'] >= 0
    print("✅ test_timed_pricing_agent passed!")


def test_demand_based_agent():
    """Test Demand Based agent works."""
    env   = DynamicPricingEnv()
    agent = DemandBasedAgent(env)

    result = agent.run_episode(seed=42)
    assert result['total_revenue'] >= 0
    print("✅ test_demand_based_agent passed!")


# ─────────────────────────────────────────
# Q-LEARNING TESTS
# ─────────────────────────────────────────

def test_q_learning_training():
    """Test Q-Learning trains without error."""
    env   = DynamicPricingEnv()
    agent = QLearningAgent(
        env,
        {**Q_LEARNING, 'n_episodes': 100}
    )
    rewards = agent.train(
        n_episodes=100,
        verbose=False
    )
    assert len(rewards) == 100
    assert agent.training_complete
    assert agent.epsilon < 1.0
    print("✅ test_q_learning_training passed!")


def test_q_learning_evaluation():
    """Test Q-Learning evaluation."""
    env   = DynamicPricingEnv()
    agent = QLearningAgent(env)
    agent.train(n_episodes=200, verbose=False)

    results = agent.evaluate(n_episodes=10)
    assert results['mean_revenue'] >= 0
    assert 'revenues' in results
    print("✅ test_q_learning_evaluation passed!")


def test_q_table_shape():
    """Test Q-table has correct shape."""
    env   = DynamicPricingEnv()
    agent = QLearningAgent(env)

    expected = (
        env.max_inventory + 1,
        env.max_days + 1,
        env.action_space.n
    )
    assert agent.q_table.shape == expected
    print(f"✅ test_q_table_shape passed! "
          f"({expected})")


# ─────────────────────────────────────────
# DQN TESTS
# ─────────────────────────────────────────

def test_dqn_network():
    """Test DQN network forward pass."""
    import torch
    net   = DQNNetwork(2, 6, [128, 64])
    state = torch.FloatTensor([[0.5, 0.5]])
    out   = net(state)

    assert out.shape == (1, 6)
    print("✅ test_dqn_network passed!")


def test_replay_buffer():
    """Test replay buffer push and sample."""
    buffer = ReplayBuffer(capacity=100)

    for i in range(50):
        buffer.push(
            np.array([25.0, 15.0]),
            2, 150.0,
            np.array([24.0, 14.0]),
            False
        )

    assert len(buffer) == 50
    states, actions, rewards, \
        next_states, dones = buffer.sample(32)
    assert states.shape == (32, 2)
    assert actions.shape == (32,)
    print("✅ test_replay_buffer passed!")


def test_dqn_training():
    """Test DQN trains without error."""
    env   = DynamicPricingEnv()
    agent = DQNAgent(
        env,
        {**DQN, 'n_episodes': 50}
    )
    rewards = agent.train(
        n_episodes=50,
        verbose=False
    )
    assert len(rewards) == 50
    assert agent.training_complete
    print("✅ test_dqn_training passed!")


def test_dqn_action_selection():
    """Test DQN selects valid actions."""
    env   = DynamicPricingEnv()
    agent = DQNAgent(env, DQN)
    state = np.array([25.0, 15.0])

    for _ in range(20):
        action = agent.select_action(
            state, training=False
        )
        assert 0 <= action < 6

    print("✅ test_dqn_action_selection passed!")


# ─────────────────────────────────────────
# RUN ALL TESTS
# ─────────────────────────────────────────

def run_all_agent_tests():
    """Run all agent unit tests."""
    print("=" * 55)
    print("  RUNNING AGENT UNIT TESTS")
    print("=" * 55)

    tests = [
        test_fixed_price_agent,
        test_random_agent,
        test_timed_pricing_agent,
        test_demand_based_agent,
        test_q_learning_training,
        test_q_learning_evaluation,
        test_q_table_shape,
        test_dqn_network,
        test_replay_buffer,
        test_dqn_training,
        test_dqn_action_selection,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1

    print("\n" + "=" * 55)
    print(f"  Results: {passed} passed, "
          f"{failed} failed")
    if failed == 0:
        print("  ✅ ALL AGENT TESTS PASSED!")
    else:
        print("  ❌ Some tests failed!")
    print("=" * 55)
    return failed == 0


if __name__ == "__main__":
    run_all_agent_tests()