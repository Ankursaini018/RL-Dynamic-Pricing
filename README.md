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

## Week 2 ✅ Complete — Deep Q-Network

### Week 2 Day 5 — Analysis Results
| Rank | Agent | Type | Revenue |
|---|---|---|---|
| 🥇 | DQN | Neural RL | Best |
| 🥈 | Q-Learning | Tabular RL | 2nd |
| 🥉 | Time Based | Baseline | 3rd |
| 4 | Demand Based | Baseline | 4th |
| 5 | Linear Decay | Baseline | 5th |
| 6 | Fixed Price | Baseline | 6th |

### DQN Proven Behaviors
- ✅ Drops prices near deadline
- ✅ Scarcity premium pricing
- ✅ Beats all baselines (p<0.05)

## 🔄 Mid Review Prep
**Review Window: 20th-27th July**

### GitHub Status
| Metric | Value |
|---|---|
| Commit Days | 12+ days |
| Required | 10 days |
| Status | ✅ Ready! |

### New Issues Created
| Issue | Title | Status |
|---|---|---|
| #10 | Refactor DQN codebase | 🔄 |
| #11 | PPO agent | 📅 |
| #12 | Hyperparameter tuning | 📅 |
| #13 | Final comparison | 📅 |
| #14 | Week 2 documentation | ✅ |
| #15 | Mid Review prep | ✅ |
| #16 | Final documentation | 📅 |
| #17 | Performance optimization | 📅 |
| #18 | Final submission | 📅 |

## Week 2 Day 6 — Refactoring + Docs

### Code Quality Improvements
| Item | Details |
|---|---|
| DQN Utilities | Model save/load + monitor |
| Project Runner | One command pipeline |
| Agent Tests | 11 unit tests passing |
| Agent README | Full documentation |
| Environment README | Full documentation |

### How to Run Complete Pipeline
```bash
# Quick test (fewer episodes)
cd src
python project_runner.py --quick

# Full training
python project_runner.py

# Run all tests
python tests/test_agents.py
python tests/test_environment.py
```

### Issues Updated
| Issue | Status |
|---|---|
| #10 Refactor DQN | ✅ Closed |
| #14 Week 2 docs | ✅ Closed |
| #15 Mid Review prep | ✅ Closed |
| #16 Final docs | 🔄 In Progress |