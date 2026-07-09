"""
test_environment.py
===================
Unit tests for DynamicPricingEnv.
Verifies environment works correctly.

Infotact DS/ML Internship — Project 2
Week 1 : Environment Testing
"""

import numpy as np
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


def test_environment_creation():
    """Test environment initializes correctly."""
    env = DynamicPricingEnv(
        max_inventory=50,
        max_days=30
    )
    assert env.max_inventory == 50
    assert env.max_days == 30
    assert len(env.price_levels) == 6
    print("✅ test_environment_creation passed!")


def test_reset():
    """Test environment resets correctly."""
    env = DynamicPricingEnv()
    obs, info = env.reset(seed=42)

    assert obs.shape == (2,)
    assert obs[0] == env.max_inventory
    assert obs[1] == env.max_days
    assert env.total_revenue == 0
    print("✅ test_reset passed!")


def test_action_space():
    """Test action space is correct."""
    env = DynamicPricingEnv()
    env.reset()

    assert env.action_space.n == 6
    for _ in range(100):
        action = env.action_space.sample()
        assert 0 <= action < 6
    print("✅ test_action_space passed!")


def test_step_returns():
    """Test step returns correct format."""
    env = DynamicPricingEnv()
    env.reset(seed=42)

    obs, reward, terminated, truncated, info = (
        env.step(2)
    )

    assert obs.shape == (2,)
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert 'price' in info
    assert 'bought' in info
    assert 'inventory' in info
    print("✅ test_step_returns passed!")


def test_inventory_decreases():
    """Test inventory decreases when sold."""
    env = DynamicPricingEnv()
    env.reset(seed=42)

    initial_inv = env.inventory
    # Run many steps to ensure at least one sale
    for _ in range(50):
        env.step(0)  # Lowest price = max demand

    assert env.inventory < initial_inv
    print("✅ test_inventory_decreases passed!")


def test_episode_terminates():
    """Test episode terminates correctly."""
    env = DynamicPricingEnv(
        max_inventory=5,
        max_days=10
    )
    env.reset(seed=42)

    steps = 0
    done  = False

    while not done:
        _, _, terminated, truncated, _ = (
            env.step(0)
        )
        done = terminated or truncated
        steps += 1
        assert steps <= 15

    print(f"✅ test_episode_terminates passed! "
          f"(steps={steps})")


def test_demand_probability():
    """Test demand probability is valid."""
    env = DynamicPricingEnv()

    for price in PRICE_LEVELS:
        for days in [1, 10, 20, 30]:
            prob = env._get_demand_probability(
                price, days
            )
            assert 0 <= prob <= 1, \
                f"Invalid prob {prob} for " \
                f"price={price}, days={days}"

    print("✅ test_demand_probability passed!")


def test_price_sensitivity():
    """Test higher price = lower demand."""
    env = DynamicPricingEnv()

    probs = [
        env._get_demand_probability(p, 15)
        for p in PRICE_LEVELS
    ]

    # Generally decreasing (with noise)
    # Check first and last
    assert probs[0] > probs[-1], \
        "Demand should decrease with price!"
    print("✅ test_price_sensitivity passed!")


def run_all_tests():
    """Run all unit tests."""
    print("=" * 50)
    print("  RUNNING ENVIRONMENT UNIT TESTS")
    print("=" * 50)

    tests = [
        test_environment_creation,
        test_reset,
        test_action_space,
        test_step_returns,
        test_inventory_decreases,
        test_episode_terminates,
        test_demand_probability,
        test_price_sensitivity,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"  Results: {passed} passed, "
          f"{failed} failed")
    if failed == 0:
        print("  ✅ ALL TESTS PASSED!")
    else:
        print("  ❌ Some tests failed!")
    print("=" * 50)
    return failed == 0


if __name__ == "__main__":
    run_all_tests()