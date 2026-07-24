# 🤖 PPO Agent Documentation

## What is PPO?
Proximal Policy Optimization (PPO) by OpenAI.
Used in ChatGPT training (RLHF)!

## Why PPO for Dynamic Pricing?
| Feature | Benefit |
|---|---|
| Policy-based | Direct optimization |
| Clipping | Stable training |
| Actor-Critic | Value + Policy |
| On-policy | Fresh experience |

## Architecture
Input   : 2 (inventory, days_left)
Shared  : 128 → 64 (ReLU)
Actor   : → 6 (Softmax) = probabilities
Critic  : → 1 (Linear)  = state value

## Key Components

### 1. Actor Head
Outputs probability for each price level.
Agent samples from this distribution!

### 2. Critic Head
Outputs state value V(s).
Used to compute advantage A(s,a).

### 3. Rollout Buffer
Stores on-policy experience.
Cleared after each update (on-policy!).

### 4. GAE (Generalized Advantage)
Better advantage estimation.
Balances bias vs variance.

### 5. Clipping
ratio = new_prob / old_prob
clip(ratio, 1-ε, 1+ε)
ε = 0.2
Prevents too-large policy updates!

## Usage
```python
from agents.ppo.ppo_agent import PPOAgent
from config import PPO

agent = PPOAgent(env, PPO)
agent.train(n_episodes=2000)
results = agent.evaluate(n_episodes=100)
```

## Best Config (from tuning)
| Parameter | Value |
|---|---|
| Learning Rate | 0.0005 |
| Clip Range | 0.2 |
| N Epochs | 15 |
| Entropy Coef | 0.02 |
| GAE Lambda | 0.95 |