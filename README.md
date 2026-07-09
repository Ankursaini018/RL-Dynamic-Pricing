# 🎯 RL Dynamic Pricing
## Infotact DS/ML Technical Internship 2026

![Status](https://img.shields.io/badge/Status-Week%201%20Complete-green)
![Week](https://img.shields.io/badge/Week-1%20of%204-blue)
![Model](https://img.shields.io/badge/Model-Q--Learning%20→%20DQN-red)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)

---

## ✅ Week 1 Complete — MDP + Q-Learning

### What We Built
| Component | Details |
|---|---|
| Gym Environment | Custom DynamicPricingEnv |
| State Space | (inventory, days_left) = 1,581 states |
| Action Space | 6 price levels ($50 - $300) |
| Demand Function | Stochastic price + time sensitive |
| Baseline Agents | 5 agents implemented |
| Q-Learning | 5000 episodes trained |
| Unit Tests | 8 tests all passing |

### Week 1 Results
| Agent | Type | Mean Revenue |
|---|---|---|
| Fixed Price | Baseline | See results/ |
| Time Based | Baseline | See results/ |
| Demand Based | Baseline | See results/ |
| Linear Decay | Baseline | See results/ |
| **Q-Learning** | **RL** | **Best ✅** |

### Files Structure
src/
├── environment/
│   ├── pricing_env.py    # Custom Gym env
│   └── init.py
├── agents/
│   ├── baseline_agents.py # 5 baselines
│   ├── q_learning_agent.py # Q-Learning
│   └── init.py
├── utils/
│   ├── evaluator.py
│   ├── demand_analyzer.py
│   ├── q_table_analyzer.py
│   ├── policy_extractor.py
│   ├── training_visualizer.py
│   └── results_consolidator.py
├── training/
│   └── q_learning_trainer.py
└── tests/
└── test_environment.py

## 🔄 Week 2 — Deep Q-Network (DQN)
Starting 12th July
- Neural Network replaces Q-table
- Experience replay buffer
- Epsilon greedy exploration
- More powerful than tabular Q-Learning!

### Issues Status
| Issue | Status |
|---|---|
| #1 MDP + Gym env | ✅ Closed |
| #2 Demand function | ✅ Closed |
| #3 Baseline agents | ✅ Closed |
| #4 Q-Learning | ✅ Closed |
| #5 DQN Agent | 🔄 In Progress |
| #6 Experience replay | 📅 Todo |
| #7 Train DQN | 📅 Todo |
| #8 1000 seasons | 📅 Todo |
| #9 Price trajectories | 📅 Todo |