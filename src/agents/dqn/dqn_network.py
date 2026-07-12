"""
dqn_network.py
==============
Neural Network architecture for
Deep Q-Network (DQN) agent.

Architecture:
Input  : 2 neurons (inventory, days_left)
Hidden1: 128 neurons (ReLU)
Hidden2: 64 neurons (ReLU)
Output : 6 neurons (Q-value per price)

Internship Spec:
"replace the Q-table with a Neural Network
(Deep Q-Network)"

Infotact DS/ML Internship — Project 2
Week 2 : DQN Architecture
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
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
# DQN NETWORK
# ─────────────────────────────────────────

class DQNNetwork(nn.Module):
    """
    Deep Q-Network neural network.

    Takes state as input and outputs
    Q-value for each possible action.

    Parameters
    ----------
    state_size : int
        Number of state features (default=2)
    action_size : int
        Number of possible actions (default=6)
    hidden_sizes : list
        Hidden layer sizes (default=[128, 64])
    """

    def __init__(self,
                 state_size: int = 2,
                 action_size: int = 6,
                 hidden_sizes: list = None):

        super(DQNNetwork, self).__init__()

        if hidden_sizes is None:
            hidden_sizes = DQN['hidden_size']

        self.state_size  = state_size
        self.action_size = action_size

        # ── Build Network Layers ──
        layers = []
        input_size = state_size

        for hidden_size in hidden_sizes:
            layers.append(
                nn.Linear(input_size, hidden_size)
            )
            layers.append(nn.ReLU())
            input_size = hidden_size

        # Output layer
        layers.append(
            nn.Linear(input_size, action_size)
        )

        self.network = nn.Sequential(*layers)

        # Initialize weights
        self._initialize_weights()

    def _initialize_weights(self):
        """
        Initialize network weights using
        He initialization for ReLU networks.
        """
        for layer in self.network:
            if isinstance(layer, nn.Linear):
                nn.init.kaiming_uniform_(
                    layer.weight,
                    nonlinearity='relu'
                )
                nn.init.constant_(layer.bias, 0)

    def forward(self,
                x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through network.

        Parameters
        ----------
        x : torch.Tensor
            State tensor of shape (batch, state_size)

        Returns
        -------
        torch.Tensor
            Q-values of shape (batch, action_size)
        """
        return self.network(x)

    def get_action(self,
                   state: np.ndarray,
                   device: str = 'cpu') -> int:
        """
        Get greedy action for a state.

        Parameters
        ----------
        state : np.ndarray
            Current state.
        device : str
            Compute device.

        Returns
        -------
        int
            Best action index.
        """
        state_tensor = torch.FloatTensor(
            state
        ).unsqueeze(0).to(device)

        with torch.no_grad():
            q_values = self.forward(state_tensor)

        return q_values.argmax().item()

    def print_architecture(self):
        """Print network architecture summary."""
        print("=" * 50)
        print("  DQN NETWORK ARCHITECTURE")
        print("=" * 50)
        print(f"  Input  : {self.state_size} neurons"
              f" (inventory, days_left)")

        for i, layer in enumerate(self.network):
            if isinstance(layer, nn.Linear):
                print(f"  Linear : "
                      f"{layer.in_features} → "
                      f"{layer.out_features}")
            elif isinstance(layer, nn.ReLU):
                print(f"  Activation: ReLU")

        print(f"  Output : {self.action_size} neurons"
              f" (Q-value per price)")

        total_params = sum(
            p.numel()
            for p in self.parameters()
        )
        print(f"\n  Total Parameters: {total_params}")
        print("=" * 50)


# ─────────────────────────────────────────
# DUELING DQN (ADVANCED)
# ─────────────────────────────────────────

class DuelingDQNNetwork(nn.Module):
    """
    Dueling DQN architecture.

    Splits network into:
    1. Value stream    : V(s) - how good is state?
    2. Advantage stream: A(s,a) - how good is action?

    Q(s,a) = V(s) + A(s,a) - mean(A(s,a))

    Better than standard DQN for pricing!

    Parameters
    ----------
    state_size : int
        State features.
    action_size : int
        Number of actions.
    hidden_size : int
        Hidden layer size.
    """

    def __init__(self,
                 state_size: int = 2,
                 action_size: int = 6,
                 hidden_size: int = 128):

        super(DuelingDQNNetwork, self).__init__()

        self.state_size  = state_size
        self.action_size = action_size

        # Shared feature layer
        self.feature_layer = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU()
        )

        # Value stream
        self.value_stream = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        # Advantage stream
        self.advantage_stream = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )

    def forward(self,
                x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with dueling architecture.

        Parameters
        ----------
        x : torch.Tensor
            State tensor.

        Returns
        -------
        torch.Tensor
            Q-values.
        """
        features   = self.feature_layer(x)
        values     = self.value_stream(features)
        advantages = self.advantage_stream(features)

        # Combine: Q = V + A - mean(A)
        q_values = (
            values +
            advantages -
            advantages.mean(dim=1, keepdim=True)
        )
        return q_values

    def print_architecture(self):
        """Print dueling architecture."""
        print("=" * 50)
        print("  DUELING DQN ARCHITECTURE")
        print("=" * 50)
        print(f"  Input      : {self.state_size}")
        print(f"  Shared     : → 128 (ReLU)")
        print(f"  Value      : → 64 → 1")
        print(f"  Advantage  : → 64 → {self.action_size}")
        print(f"  Output     : Q = V + A - mean(A)")
        total = sum(
            p.numel() for p in self.parameters()
        )
        print(f"  Parameters : {total}")
        print("=" * 50)


# ─────────────────────────────────────────
# MAIN TEST
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("Testing DQN Networks...\n")

    # Standard DQN
    dqn = DQNNetwork(
        state_size=2,
        action_size=6,
        hidden_sizes=[128, 64]
    )
    dqn.print_architecture()

    # Test forward pass
    test_state = torch.FloatTensor([[25, 15]])
    q_values   = dqn(test_state)
    print(f"\n  Test state  : [25 inventory, 15 days]")
    print(f"  Q-values    : {q_values.detach().numpy()}")
    print(f"  Best action : {q_values.argmax().item()}")
    print(f"  Best price  : $"
          f"{[50,100,150,200,250,300][q_values.argmax().item()]}")

    print("\n" + "─" * 50)

    # Dueling DQN
    dueling = DuelingDQNNetwork()
    dueling.print_architecture()

    q_dueling = dueling(test_state)
    print(f"\n  Dueling Q-values: "
          f"{q_dueling.detach().numpy()}")

    print("\n✅ Both networks working correctly!")