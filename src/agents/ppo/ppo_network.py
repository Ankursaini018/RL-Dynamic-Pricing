"""
ppo_network.py
==============
Actor-Critic Neural Network
for PPO agent.

Architecture:
→ Shared layers
→ Actor head (policy)
→ Critic head (value)

Infotact DS/ML Internship — Project 2
Week 3 : PPO Network
"""

import torch
import torch.nn as nn
import numpy as np
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))



from config import PPO


# ─────────────────────────────────────────
# ACTOR CRITIC NETWORK
# ─────────────────────────────────────────

class ActorCriticNetwork(nn.Module):
    """
    Shared Actor-Critic network for PPO.

    Actor  → outputs action probabilities
    Critic → outputs state value

    Parameters
    ----------
    state_size : int
        Number of state features.
    action_size : int
        Number of discrete actions.
    hidden_sizes : list
        Hidden layer sizes.
    """

    def __init__(self,
                 state_size: int = 2,
                 action_size: int = 6,
                 hidden_sizes: list = None):

        super(ActorCriticNetwork, self).__init__()

        if hidden_sizes is None:
            hidden_sizes = PPO['hidden_size']

        self.state_size  = state_size
        self.action_size = action_size

        # ── Shared Feature Layers ──
        shared_layers = []
        input_size    = state_size

        for hidden in hidden_sizes:
            shared_layers.append(
                nn.Linear(input_size, hidden)
            )
            shared_layers.append(nn.ReLU())
            input_size = hidden

        self.shared = nn.Sequential(*shared_layers)

        # ── Actor Head ──
        # Outputs action PROBABILITIES
        self.actor = nn.Sequential(
            nn.Linear(input_size, action_size),
            nn.Softmax(dim=-1)
        )

        # ── Critic Head ──
        # Outputs STATE VALUE
        self.critic = nn.Linear(input_size, 1)

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        """Initialize network weights."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.orthogonal_(
                    module.weight, gain=np.sqrt(2)
                )
                nn.init.constant_(module.bias, 0)

        # Actor output init
        nn.init.orthogonal_(
            self.actor[0].weight, gain=0.01
        )
        # Critic output init
        nn.init.orthogonal_(
            self.critic.weight, gain=1.0
        )

    def forward(self,
                x: torch.Tensor) -> tuple:
        """
        Forward pass.

        Parameters
        ----------
        x : torch.Tensor
            State tensor.

        Returns
        -------
        tuple
            (action_probs, state_value)
        """
        features     = self.shared(x)
        action_probs = self.actor(features)
        state_value  = self.critic(features)
        return action_probs, state_value

    def get_action(self,
                   state: np.ndarray,
                   device: str = 'cpu') -> tuple:
        """
        Sample action from policy.

        Parameters
        ----------
        state : np.ndarray
            Current state.
        device : str
            Compute device.

        Returns
        -------
        tuple
            (action, log_prob, value)
        """
        state_t = torch.FloatTensor(
            state
        ).unsqueeze(0).to(device)

        with torch.no_grad():
            probs, value = self.forward(state_t)

        dist   = torch.distributions.Categorical(probs)
        action = dist.sample()

        return (
            action.item(),
            dist.log_prob(action).item(),
            value.item()
        )

    def evaluate_action(self,
                        states: torch.Tensor,
                        actions: torch.Tensor
                        ) -> tuple:
        """
        Evaluate actions for PPO update.

        Parameters
        ----------
        states : torch.Tensor
            Batch of states.
        actions : torch.Tensor
            Batch of actions.

        Returns
        -------
        tuple
            (log_probs, values, entropy)
        """
        probs, values = self.forward(states)
        dist          = torch.distributions.Categorical(
            probs
        )
        log_probs = dist.log_prob(actions)
        entropy   = dist.entropy()

        return log_probs, values.squeeze(-1), entropy

    def print_architecture(self):
        """Print network architecture."""
        print("=" * 50)
        print("  ACTOR-CRITIC NETWORK (PPO)")
        print("=" * 50)
        print(f"  Input   : {self.state_size}")
        print(f"  Shared  : {self.shared}")
        print(f"  Actor   : → {self.action_size}"
              f" (probabilities)")
        print(f"  Critic  : → 1 (state value)")
        total = sum(
            p.numel() for p in self.parameters()
        )
        print(f"\n  Parameters: {total}")
        print("=" * 50)


if __name__ == "__main__":
    import torch
    print("Testing Actor-Critic Network...\n")

    net   = ActorCriticNetwork(2, 6, [128, 64])
    net.print_architecture()

    state = torch.FloatTensor([[0.5, 0.5]])
    probs, value = net(state)

    print(f"\n  Test state   : [0.5, 0.5]")
    print(f"  Action probs : {probs.detach()}")
    print(f"  State value  : {value.item():.4f}")
    print(f"  Sum of probs : {probs.sum().item():.4f}")
    print(f"\n✅ Network working correctly!")