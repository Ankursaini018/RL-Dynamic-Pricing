# 🧠 Deep Q-Network (DQN) Agent

## Week 2 Implementation Plan

### Why DQN over Q-Learning?
| Feature | Q-Learning | DQN |
|---|---|---|
| State Space | Small discrete | Large/continuous |
| Storage | Q-table (memory) | Neural Network |
| Scalability | Limited | Highly scalable |
| Performance | Good for small | Better for complex |

### DQN Components
1. **Neural Network** → Replaces Q-table
2. **Experience Replay** → Stabilizes training
3. **Target Network** → Prevents oscillation
4. **Epsilon Greedy** → Exploration strategy

### Architecture
Input Layer  : 2 neurons (inventory, days_left)
Hidden Layer1: 128 neurons (ReLU)
Hidden Layer2: 64 neurons (ReLU)
Output Layer : 6 neurons (Q-value per price)

### Files (Coming Week 2)
- `dqn_network.py` → Neural network architecture
- `replay_buffer.py` → Experience replay memory
- `dqn_agent.py` → Complete DQN agent