# 🎯 RL Dynamic Pricing
## Infotact DS/ML Technical Internship 2026

![Status](https://img.shields.io/badge/Status-Mid%20Review%20Ready-brightgreen)
![Week](https://img.shields.io/badge/Week-2%20of%204%20Complete-blue)
![Model](https://img.shields.io/badge/Model-DQN%20PyTorch-red)
![Tests](https://img.shields.io/badge/Tests-19%20Passing-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)

---

## 🎯 Problem Statement
Selling finite inventory over limited time
is a complex optimization problem.

**RL Solution:** Agent learns optimal
pricing policy through 1000s of episodes!

---

## 🏗️ MDP Formulation
| Component | Value |
|---|---|
| State | (inventory, days_left) |
| Actions | 6 prices ($50-$300) |
| Reward | Revenue from sale |
| Penalty | -10 per unsold ticket |
| State Space | 1,581 discrete states |

---

## 🧠 DQN Architecture
Input  : 2 neurons (inventory, days_left)
Hidden : 128 neurons (ReLU)
Hidden : 64 neurons (ReLU)
Output : 6 neurons (Q-value per price)
Total Parameters: ~10,000

## 🔑 Key Innovations
| Innovation | Purpose |
|---|---|
| Experience Replay | Breaks correlations |
| Target Network | Stable training |
| Epsilon Greedy | Exploration |
| Gradient Clipping | Prevents explosions |

---

## ✅ Week 1 — MDP + Q-Learning

### Deliverables
- Custom DynamicPricingEnv (Gymnasium)
- 5 Baseline agents
- Q-Learning agent (5000 episodes)
- Q-Table policy analysis
- 8 Unit tests passing

---

## ✅ Week 2 — Deep Q-Network

### Training Config
| Parameter | Value |
|---|---|
| Episodes | 2,000 |
| Batch Size | 64 |
| Buffer Size | 10,000 |
| Target Update | Every 10 eps |
| Optimizer | Adam (lr=0.001) |

### Results (1000 Seasons)
| Rank | Agent | Type |
|---|---|---|
| 🥇 | DQN | Neural RL |
| 🥈 | Q-Learning | Tabular RL |
| 🥉 | Time Based | Baseline |
| 4 | Demand Based | Baseline |
| 5 | Linear Decay | Baseline |
| 6 | Fixed Price | Baseline |

### Proven Behaviors
- ✅ Drops prices near deadline
- ✅ Scarcity premium pricing
- ✅ Beats all baselines (p<0.05)

---

## 🔬 How to Run

```bash
# Install
pip install -r requirements.txt

# Quick test
cd src
python project_runner.py --quick

# Full pipeline
python project_runner.py

# Run tests
python tests/test_agents.py
python tests/test_environment.py
```

---

## 📊 Project Structure
RL-Dynamic-Pricing/
├── src/
│   ├── config.py
│   ├── project_runner.py
│   ├── environment/
│   │   ├── pricing_env.py
│   │   └── env_config.py
│   ├── agents/
│   │   ├── baseline_agents.py
│   │   ├── q_learning_agent.py
│   │   ├── agent_registry.py
│   │   └── dqn/
│   │       ├── dqn_network.py
│   │       ├── dqn_agent.py
│   │       ├── replay_buffer.py
│   │       └── dqn_utils.py
│   ├── training/
│   │   ├── q_learning_trainer.py
│   │   └── dqn_trainer.py
│   ├── simulation/
│   │   ├── season_simulator.py
│   │   └── business_report.py
│   ├── visualization/
│   │   ├── price_dashboard.py
│   │   └── trajectory_insights.py
│   ├── analysis/
│   │   ├── week2_analyzer.py
│   │   └── dqn_insights.py
│   ├── utils/
│   │   ├── evaluator.py
│   │   ├── training_visualizer.py
│   │   └── results_consolidator.py
│   └── tests/
│       ├── test_environment.py
│       └── test_agents.py
├── notebooks/
│   ├── week1/
│   └── week2/
├── results/
├── models/     (gitignored)
└── data/       (gitignored)

---

## 📊 GitHub Issues
| Issue | Title | Status |
|---|---|---|
| #1-#9 | Week 1 + 2 core | ✅ Done |
| #10 | Refactor DQN | ✅ Done |
| #14 | Week 2 docs | ✅ Done |
| #15 | Mid Review prep | ✅ Done |
| #11 | PPO agent | 📅 Week 3 |
| #12 | Hyperparameter tuning | 📅 Week 3 |
| #13 | Final comparison | 📅 Week 3 |
| #16 | Final documentation | 📅 Week 4 |
| #17 | Optimization | 📅 Week 4 |
| #18 | Final submission | 📅 Week 4 |