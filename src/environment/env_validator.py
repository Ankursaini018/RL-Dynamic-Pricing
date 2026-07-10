"""
env_validator.py
================
Validates the Gymnasium environment
follows correct interface standards.

Infotact DS/ML Internship — Project 2
Week 1 : Environment Validation
"""

import numpy as np
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from environment.pricing_env import DynamicPricingEnv


def validate_gym_interface(
        env: DynamicPricingEnv) -> bool:
    """
    Validate environment follows
    Gymnasium interface correctly.

    Checks:
    1. reset() returns (obs, info)
    2. step() returns 5 values
    3. Observation space valid
    4. Action space valid
    5. Episode terminates properly

    Parameters
    ----------
    env : DynamicPricingEnv
        Environment to validate.

    Returns
    -------
    bool
        True if all checks pass.
    """
    print("=" * 50)
    print("  GYM INTERFACE VALIDATION")
    print("=" * 50)

    checks = []

    # ── Check 1: Reset ──
    try:
        result = env.reset(seed=42)
        assert len(result) == 2
        obs, info = result
        assert obs.shape == (2,)
        assert isinstance(info, dict)
        print("  ✅ reset() interface correct")
        checks.append(True)
    except Exception as e:
        print(f"  ❌ reset() failed: {e}")
        checks.append(False)

    # ── Check 2: Step ──
    try:
        result = env.step(0)
        assert len(result) == 5
        obs, rew, term, trunc, info = result
        assert obs.shape == (2,)
        assert isinstance(rew, float)
        assert isinstance(term, bool)
        assert isinstance(trunc, bool)
        assert isinstance(info, dict)
        print("  ✅ step() interface correct")
        checks.append(True)
    except Exception as e:
        print(f"  ❌ step() failed: {e}")
        checks.append(False)

    # ── Check 3: Observation Space ──
    try:
        obs_space = env.observation_space
        assert obs_space.shape == (2,)
        assert obs_space.low[0] == 0
        assert obs_space.low[1] == 0
        print("  ✅ Observation space correct")
        checks.append(True)
    except Exception as e:
        print(f"  ❌ Observation space: {e}")
        checks.append(False)

    # ── Check 4: Action Space ──
    try:
        act_space = env.action_space
        assert act_space.n == 6
        for _ in range(20):
            a = act_space.sample()
            assert 0 <= a < 6
        print("  ✅ Action space correct")
        checks.append(True)
    except Exception as e:
        print(f"  ❌ Action space: {e}")
        checks.append(False)

    # ── Check 5: Full Episode ──
    try:
        env.reset(seed=42)
        steps = 0
        done  = False
        while not done:
            obs, rew, term, trunc, info = (
                env.step(env.action_space.sample())
            )
            done = term or trunc
            steps += 1
            assert steps <= 100
        assert steps > 0
        print(f"  ✅ Full episode runs "
              f"({steps} steps)")
        checks.append(True)
    except Exception as e:
        print(f"  ❌ Full episode: {e}")
        checks.append(False)

    # ── Summary ──
    all_passed = all(checks)
    print("\n" + "=" * 50)
    if all_passed:
        print("  ✅ ALL VALIDATION CHECKS PASSED!")
        print("  Environment is Gym-compatible!")
    else:
        failed = checks.count(False)
        print(f"  ❌ {failed} checks failed!")
    print("=" * 50)

    return all_passed


if __name__ == "__main__":
    env  = DynamicPricingEnv()
    ok   = validate_gym_interface(env)
    print(f"\nValidation result: "
          f"{'✅ PASS' if ok else '❌ FAIL'}")