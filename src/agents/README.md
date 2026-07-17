# 🤖 Agents Module Documentation

## Overview
All pricing agents for RL Dynamic Pricing project.

---

## 📁 Files

### baseline_agents.py
Five naive baseline pricing strategies.

```python
from agents.baseline_agents import (
    FixedPriceAgent,    # Always $150
    RandomAgent,        # Random price
    TimedPricingAgent,  # Based on time
    DemandBasedAgent,   # Based on inventory
    LinearDecayAgent    # Decreases over time
)

agent = TimedPricingAgent(env)
result = agent.run_episode(seed=42)
```

### q_learning_agent.py
Tabular Q-Learning agent.

```python
from agents.q_learning_agent import QLearningAgent

agent = QLearningAgent(env)
agent.train(n_episodes=5000)
results = agent.evaluate(n_episodes=100)
```

### dqn/dqn_agent.py
Deep Q-Network agent (MAIN AGENT).

```python
from agents.dqn.dqn_agent import DQNAgent
from config import DQN

agent = DQNAgent(env, DQN)
agent.train(n_episodes=2000)
results = agent.evaluate(n_episodes=100)
```

### dqn/dqn_network.py
Neural network architectures.

```python
from agents.dqn.dqn_network import (
    DQNNetwork,      # Standard DQN
    DuelingDQNNetwork # Advanced Dueling
)

net = DQNNetwork(state_size=2, action_size=6)
```

### dqn/replay_buffer.py
Experience replay buffer.

```python
from agents.dqn.replay_buffer import ReplayBuffer

buffer = ReplayBuffer(capacity=10000)
buffer.push(state, action, reward, next_state, done)
states, actions, rewards, next_states, dones = (
    buffer.sample(batch_size=64)
)
```

### agent_registry.py
Central agent factory.

```python
from agents.agent_registry import (
    create_agent,
    create_all_baseline_agents,
    create_ql_agent
)

agent    = create_agent('dqn', env)
baselines = create_all_baseline_agents(env)
```

---

## 🏆 Agent Performance Ranking
1. 🥇 DQN (Deep Q-Network)
2. 🥈 Q-Learning (Tabular)
3. 🥉 Time Based Baseline
4. Demand Based Baseline
5. Linear Decay Baseline
6. Fixed Price Baseline