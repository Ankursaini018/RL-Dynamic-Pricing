# 🔄 Reproduction Guide
## RL Dynamic Pricing — Project 2

## Quick Start
```bash
# 1. Clone repo
git clone https://github.com/Ankursaini018/
RL-Dynamic-Pricing.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Quick test (5 mins)
cd src
python project_runner.py --quick

# 4. Full pipeline (30 mins)
python project_runner.py
```

## Run Individual Components

### Environment Test
```bash
cd src
python environment/pricing_env.py
```

### Run All Tests
```bash
cd src
python tests/test_environment.py
python tests/test_agents.py
python tests/test_ppo.py
```

### Train Individual Agents
```bash
# Q-Learning
python agents/q_learning_agent.py

# DQN
python agents/dqn/dqn_agent.py

# PPO (best agent!)
python agents/ppo/ppo_agent.py
```

### Final Simulation
```bash
python simulation/final_simulation.py
```

## Expected Results
| Agent | Expected Revenue |
|---|---|
| PPO | Highest |
| DQN | 2nd |
| Q-Learning | 3rd |
| Baselines | 4th-7th |

## Key Files
| File | Purpose |
|---|---|
| config.py | All hyperparameters |
| project_runner.py | Complete pipeline |
| agents/ppo/ppo_agent.py | Best agent |
| simulation/final_simulation.py | 1000 seasons |