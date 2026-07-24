"""
test_ppo.py
===========
Unit tests for PPO agent components.

Infotact DS/ML Internship — Project 2
Week 3 : PPO Testing
"""

import numpy as np
import torch
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from environment.pricing_env import DynamicPricingEnv
from agents.ppo.ppo_network import ActorCriticNetwork
from agents.ppo.ppo_agent import (
    PPOAgent, RolloutBuffer
)
from config import PPO


def test_actor_critic_network():
    """Test Actor-Critic network."""
    net   = ActorCriticNetwork(2, 6, [128, 64])
    state = torch.FloatTensor([[0.5, 0.5]])
    probs, value = net(state)

    assert probs.shape == (1, 6)
    assert value.shape == (1, 1)
    assert abs(probs.sum().item() - 1.0) < 0.001
    assert all(p >= 0 for p in probs[0].tolist())
    print("✅ test_actor_critic_network passed!")


def test_rollout_buffer():
    """Test Rollout Buffer."""
    buffer = RolloutBuffer(100, 2)

    for i in range(50):
        buffer.push(
            np.array([0.5, 0.5]),
            2, 150.0, 100.0, -0.5, False
        )

    assert len(buffer) == 50
    buffer.compute_returns(0.99, 0.95, 0.0)
    assert hasattr(buffer, 'advantages')
    assert hasattr(buffer, 'returns')
    assert len(buffer.advantages) == 50
    print("✅ test_rollout_buffer passed!")


def test_ppo_action_selection():
    """Test PPO action selection."""
    env   = DynamicPricingEnv()
    agent = PPOAgent(env, PPO)
    state = np.array([25.0, 15.0])

    for _ in range(20):
        result = agent.select_action(
            state, training=False
        )
        if isinstance(result, tuple):
            action = result[0]
        else:
            action = result
        assert 0 <= action < 6

    print("✅ test_ppo_action_selection passed!")


def test_ppo_normalization():
    """Test state normalization."""
    env   = DynamicPricingEnv()
    agent = PPOAgent(env, PPO)

    state = np.array([50.0, 30.0])
    norm  = agent._normalize(state)

    assert norm[0] == 1.0
    assert norm[1] == 1.0

    state2 = np.array([0.0, 0.0])
    norm2  = agent._normalize(state2)

    assert norm2[0] == 0.0
    assert norm2[1] == 0.0
    print("✅ test_ppo_normalization passed!")


def test_ppo_training():
    """Test PPO trains without error."""
    env   = DynamicPricingEnv()
    agent = PPOAgent(
        env,
        {**PPO, 'n_episodes': 50}
    )
    rewards = agent.train(
        n_episodes=50,
        verbose=False
    )
    assert len(rewards) == 50
    assert agent.training_complete
    print("✅ test_ppo_training passed!")


def test_ppo_evaluation():
    """Test PPO evaluation."""
    env   = DynamicPricingEnv()
    agent = PPOAgent(env, PPO)
    agent.train(n_episodes=100, verbose=False)

    results = agent.evaluate(n_episodes=10)
    assert results['mean_revenue'] >= 0
    assert results['mean_sold'] >= 0
    assert 'revenues' in results
    print("✅ test_ppo_evaluation passed!")


def test_get_tensors():
    """Test RolloutBuffer tensor conversion."""
    buffer = RolloutBuffer(100, 2)

    for _ in range(64):
        buffer.push(
            np.array([0.5, 0.5]),
            np.random.randint(0, 6),
            np.random.uniform(0, 300),
            np.random.uniform(0, 500),
            -0.5, False
        )

    buffer.compute_returns(0.99, 0.95)
    tensors = buffer.get_tensors('cpu')

    assert len(tensors) == 5
    states, actions, log_probs, \
        returns, advantages = tensors

    assert states.shape == (64, 2)
    assert actions.shape == (64,)
    print("✅ test_get_tensors passed!")


def run_all_ppo_tests():
    """Run all PPO unit tests."""
    print("=" * 50)
    print("  RUNNING PPO UNIT TESTS")
    print("=" * 50)

    tests = [
        test_actor_critic_network,
        test_rollout_buffer,
        test_ppo_action_selection,
        test_ppo_normalization,
        test_ppo_training,
        test_ppo_evaluation,
        test_get_tensors,
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

    print("\n" + "=" * 50)
    print(f"  Results: {passed} passed, "
          f"{failed} failed")
    if failed == 0:
        print("  ✅ ALL PPO TESTS PASSED!")
    else:
        print("  ❌ Some tests failed!")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    run_all_ppo_tests()