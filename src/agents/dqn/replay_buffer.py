"""
replay_buffer.py
================
Experience Replay Buffer for DQN.

WHY EXPERIENCE REPLAY?
======================
Problem: Consecutive experiences are
highly correlated! Training on correlated
data makes learning unstable.

Solution: Store experiences in memory.
Sample RANDOM mini-batches for training.
This breaks temporal correlations!

Buffer stores transitions:
(state, action, reward, next_state, done)

Internship Spec:
"implement experience replay to
stabilize training"

Infotact DS/ML Internship — Project 2
Week 2 : Experience Replay
"""

import numpy as np
import random
from collections import deque
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from config import DQN


# ─────────────────────────────────────────
# EXPERIENCE REPLAY BUFFER
# ─────────────────────────────────────────

class ReplayBuffer:
    """
    Fixed-size experience replay buffer.

    Stores transitions and samples random
    mini-batches for DQN training.

    Parameters
    ----------
    capacity : int
        Maximum buffer size (default=10000)
    seed : int
        Random seed for reproducibility.
    """

    def __init__(self,
                 capacity: int = None,
                 seed: int = 42):

        self.capacity = capacity or DQN['memory_size']
        self.buffer   = deque(maxlen=self.capacity)
        self.seed     = seed
        random.seed(seed)

    def push(self,
             state: np.ndarray,
             action: int,
             reward: float,
             next_state: np.ndarray,
             done: bool):
        """
        Add experience to buffer.

        Parameters
        ----------
        state : np.ndarray
            Current state.
        action : int
            Action taken.
        reward : float
            Reward received.
        next_state : np.ndarray
            Next state.
        done : bool
            Episode terminated flag.
        """
        experience = (
            state,
            action,
            reward,
            next_state,
            done
        )
        self.buffer.append(experience)

    def sample(self,
               batch_size: int) -> tuple:
        """
        Sample random mini-batch.

        Parameters
        ----------
        batch_size : int
            Number of experiences to sample.

        Returns
        -------
        tuple
            (states, actions, rewards,
             next_states, dones) as numpy arrays.
        """
        assert len(self.buffer) >= batch_size, \
            f"Buffer has {len(self.buffer)} " \
            f"experiences but need {batch_size}!"

        batch = random.sample(
            self.buffer, batch_size
        )

        states      = np.array([e[0] for e in batch])
        actions     = np.array([e[1] for e in batch])
        rewards     = np.array([e[2] for e in batch],
                                dtype=np.float32)
        next_states = np.array([e[3] for e in batch])
        dones       = np.array([e[4] for e in batch],
                                dtype=np.float32)

        return states, actions, rewards, \
               next_states, dones

    def __len__(self) -> int:
        """Return current buffer size."""
        return len(self.buffer)

    def is_ready(self, batch_size: int) -> bool:
        """
        Check if buffer has enough experiences.

        Parameters
        ----------
        batch_size : int
            Required minimum experiences.

        Returns
        -------
        bool
            True if ready for sampling.
        """
        return len(self.buffer) >= batch_size

    def get_stats(self) -> dict:
        """
        Get buffer statistics.

        Returns
        -------
        dict
            Buffer statistics.
        """
        if len(self.buffer) == 0:
            return {'size': 0}

        rewards = [e[2] for e in self.buffer]
        return {
            'size'        : len(self.buffer),
            'capacity'    : self.capacity,
            'fill_pct'    : len(self.buffer) /
                            self.capacity * 100,
            'mean_reward' : np.mean(rewards),
            'max_reward'  : np.max(rewards),
            'min_reward'  : np.min(rewards),
            'n_done'      : sum(
                e[4] for e in self.buffer
            )
        }

    def print_stats(self):
        """Print buffer statistics."""
        stats = self.get_stats()
        print(f"  Buffer Size   : "
              f"{stats['size']}/{stats['capacity']}"
              f" ({stats.get('fill_pct', 0):.1f}%)")
        if stats['size'] > 0:
            print(f"  Mean Reward   : "
                  f"{stats['mean_reward']:.2f}")
            print(f"  Episodes Done : "
                  f"{stats['n_done']}")


# ─────────────────────────────────────────
# PRIORITIZED REPLAY (ADVANCED)
# ─────────────────────────────────────────

class PrioritizedReplayBuffer:
    """
    Prioritized Experience Replay (PER).

    Samples important experiences MORE often.
    Importance = |TD error| (bigger error = more important)

    Parameters
    ----------
    capacity : int
        Buffer capacity.
    alpha : float
        Prioritization strength (0=uniform, 1=full)
    beta : float
        Importance sampling weight.
    """

    def __init__(self,
                 capacity: int = 10000,
                 alpha: float = 0.6,
                 beta: float = 0.4):

        self.capacity   = capacity
        self.alpha      = alpha
        self.beta       = beta
        self.buffer     = []
        self.priorities = np.zeros(
            capacity, dtype=np.float32
        )
        self.pos        = 0

    def push(self,
             state, action, reward,
             next_state, done):
        """Add experience with max priority."""
        max_priority = self.priorities.max() \
                       if self.buffer else 1.0

        if len(self.buffer) < self.capacity:
            self.buffer.append(
                (state, action, reward,
                 next_state, done)
            )
        else:
            self.buffer[self.pos] = (
                state, action, reward,
                next_state, done
            )

        self.priorities[self.pos] = max_priority
        self.pos = (self.pos + 1) % self.capacity

    def sample(self,
               batch_size: int) -> tuple:
        """Sample based on priorities."""
        n = len(self.buffer)
        priorities = self.priorities[:n]
        probs = priorities ** self.alpha
        probs /= probs.sum()

        indices = np.random.choice(
            n, batch_size, p=probs
        )
        samples = [self.buffer[i] for i in indices]

        weights = (n * probs[indices]) ** (-self.beta)
        weights /= weights.max()

        states      = np.array([s[0] for s in samples])
        actions     = np.array([s[1] for s in samples])
        rewards     = np.array([s[2] for s in samples])
        next_states = np.array([s[3] for s in samples])
        dones       = np.array([s[4] for s in samples])

        return (states, actions, rewards,
                next_states, dones,
                indices, weights)

    def update_priorities(self,
                          indices: np.ndarray,
                          priorities: np.ndarray):
        """Update priorities after learning."""
        for idx, priority in zip(
            indices, priorities
        ):
            self.priorities[idx] = priority

    def __len__(self):
        return len(self.buffer)


# ─────────────────────────────────────────
# MAIN TEST
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("Testing Experience Replay Buffer...\n")

    # Standard buffer
    buffer = ReplayBuffer(capacity=1000)

    print("Filling buffer with 200 experiences...")
    for i in range(200):
        state      = np.array([
            np.random.randint(0, 51),
            np.random.randint(0, 31)
        ], dtype=np.float32)
        action     = np.random.randint(0, 6)
        reward     = np.random.uniform(0, 300)
        next_state = np.array([
            max(0, state[0]-1),
            max(0, state[1]-1)
        ], dtype=np.float32)
        done = bool(state[0] == 0 or state[1] == 0)

        buffer.push(
            state, action, reward,
            next_state, done
        )

    print(f"\nBuffer Statistics:")
    buffer.print_stats()

    print(f"\nSampling batch of 32...")
    states, actions, rewards, \
        next_states, dones = buffer.sample(32)

    print(f"  States shape      : {states.shape}")
    print(f"  Actions shape     : {actions.shape}")
    print(f"  Rewards shape     : {rewards.shape}")
    print(f"  Next states shape : {next_states.shape}")
    print(f"  Dones shape       : {dones.shape}")
    print(f"\n✅ Replay buffer working correctly!")