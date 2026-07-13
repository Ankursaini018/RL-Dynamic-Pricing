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

## ✅ Week 1 Complete — 11th July 2026

### Day-wise Summary
| Day | Date | Focus | Status |
|---|---|---|---|
| Day 1 | 5 July | MDP + Gym Environment | ✅ |
| Day 2 | 6 July | Baseline Agents | ✅ |
| Day 3 | 7 July | Q-Learning | ✅ |
| Day 4 | 8 July | Q-Table Analysis | ✅ |
| Day 5 | 9 July | Final Wrap | ✅ |
| Day 6 | 10 July | Refactoring + Docs | ✅ |
| Day 7 | 11 July | Cleanup + Week 2 Prep | ✅ |

### Issues Closed This Week
- ✅ Issue #1 — MDP + Gym Environment
- ✅ Issue #2 — Stochastic Demand Function
- ✅ Issue #3 — Baseline Agents (5)
- ✅ Issue #4 — Q-Learning Implementation

### Files Created This Week
- 19+ Python source scripts
- 7 Jupyter notebooks
- 8 unit tests (all passing)
- Complete documentation

## 🔄 Week 2 — Deep Q-Network (DQN)

### Day 1 — DQN Architecture ✅
| Component | Details |
|---|---|
| Network | 2 → 128 → 64 → 6 (ReLU) |
| Parameters | ~10,000 |
| Optimizer | Adam (lr=0.001) |
| Loss | MSE Loss |
| Replay Buffer | 10,000 experiences |
| Target Update | Every 10 episodes |

### Why DQN over Q-Learning?
| Feature | Q-Learning | DQN |
|---|---|---|
| Storage | Q-table | Neural Network |
| State Space | Small discrete | Any size |
| Scalability | Limited | High |
| Generalization | None | Yes |

### Issues Status
| Issue | Status |
|---|---|
| #5 DQN Agent | 🔄 In Progress |
| #6 Experience Replay | ✅ Done |
| #7 Train DQN | 📅 Tomorrow |

### Week 2 Day 2 — DQN Training ✅
| Metric | Value |
|---|---|
| Training Episodes | 2,000 |
| Batch Size | 64 |
| Replay Buffer | 10,000 |
| Target Update | Every 10 eps |
| DQN Revenue | See results/ |
| vs Best Baseline | Improvement! |

### Key DQN Behaviors Learned
- ✅ Discounts prices near deadline
- ✅ Premium pricing for low inventory
- ✅ Beats all baseline agents

### Issues Updated
| Issue | Status |
|---|---|
| #5 DQN Agent | ✅ Closed |
| #6 Experience Replay | ✅ Closed |
| #7 Train + Evaluate | 🔄 In Progress |
| #8 1000 Seasons | 📅 Tomorrow |