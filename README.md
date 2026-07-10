# 🎯 RL Dynamic Pricing
## Infotact DS/ML Technical Internship 2026

![Status](https://img.shields.io/badge/Status-Week%201%20Complete-brightgreen)
![Issues](https://img.shields.io/badge/Issues-4%2F9%20Closed-blue)
![Model](https://img.shields.io/badge/Model-Q--Learning%20→%20DQN-red)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![Gym](https://img.shields.io/badge/Gymnasium-Custom%20Env-orange)

---

## 🎯 Problem Statement
Selling finite inventory over limited time
is a complex optimization problem.

**Static pricing fails because:**
- Market demand fluctuates daily
- Time pressure creates urgency
- Unsold inventory = lost revenue forever!

**Our Solution:**
RL agent that learns optimal pricing policy
through 1000s of simulated booking seasons!

---

## 🏗️ Project Architecture
RL-Dynamic-Pricing/
│
├── src/
│   ├── config.py              # Master config ⚙️
│   ├── environment/
│   │   ├── pricing_env.py     # Custom Gym env 🎮
│   │   ├── env_config.py      # Env parameters
│   │   └── env_validator.py   # Interface checks
│   ├── agents/
│   │   ├── baseline_agents.py # 5 baselines 📊
│   │   ├── q_learning_agent.py# Q-Learning 🧠
│   │   └── agent_registry.py  # Agent factory
│   ├── utils/
│   │   ├── evaluator.py       # Agent evaluation
│   │   ├── demand_analyzer.py # Market analysis
│   │   ├── q_table_analyzer.py# Policy analysis
│   │   ├── policy_extractor.py# Policy export
│   │   ├── training_visualizer.py
│   │   ├── results_consolidator.py
│   │   └── logger.py          # Experiment logs
│   ├── training/
│   │   └── q_learning_trainer.py
│   └── tests/
│       └── test_environment.py # 8 tests ✅
│
├── notebooks/
│   └── week1/
│       ├── week1_day1_mdp_environment.ipynb
│       ├── week1_day2_baseline_agents.ipynb
│       ├── week1_day3_q_learning.ipynb
│       ├── week1_day4_q_table_analysis.ipynb
│       └── week1_day5_final_wrap.ipynb
│
├── results/               # Generated outputs
├── models/                # Trained models (gitignored)
├── data/                  # Data files (gitignored)
├── requirements.txt
└── README.md

---

## ✅ Week 1 Complete

### Environment
| Spec | Value |
|---|---|
| Inventory | 50 tickets/rooms |
| Time Horizon | 30 days |
| Price Levels | $50, $100, $150, $200, $250, $300 |
| State Space | 1,581 discrete states |
| Demand Model | Stochastic (price + time sensitive) |

### Agents Implemented
| Agent | Strategy |
|---|---|
| Fixed Price | Always $150 |
| Random | Random each day |
| Time Based | High early → Low late |
| Demand Based | Based on inventory level |
| Linear Decay | Decreases linearly |
| **Q-Learning** | **Learned optimal policy** |

### How to Run
```bash
# Run environment test
cd src
python environment/pricing_env.py

# Run unit tests
python tests/test_environment.py

# Run validation
python environment/env_validator.py

# Run Week 1 comparison
python utils/results_consolidator.py
```

---

## 🔄 Week 2 — Deep Q-Network Starting 12th July