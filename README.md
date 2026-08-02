# 🎯 RL Dynamic Pricing
## Infotact DS/ML Technical Internship 2026

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Week](https://img.shields.io/badge/Week-4%20Complete-blue)
![Tests](https://img.shields.io/badge/Tests-26%20Passing-green)
![Best](https://img.shields.io/badge/Best%20Agent-PPO-gold)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)

---

## 🎯 Problem Statement

Airlines and hotels must sell **finite inventory**
over **limited time**. Traditional fixed pricing
leaves significant revenue on the table.

**RL Solution:** Train an agent that learns
optimal dynamic pricing through thousands of
simulated booking seasons!

---

## 🏗️ MDP Formulation

| Component | Value |
|---|---|
| **State** | (remaining_inventory, days_until_departure) |
| **Actions** | 6 price levels ($50, $100, $150, $200, $250, $300) |
| **Reward** | Revenue from each sale |
| **Penalty** | -10 per unsold ticket |
| **State Space** | 1,581 discrete states |

---

## 📊 Final Results (1000 Seasons)

| Rank | Agent | Type | Notes |
|---|---|---|---|
| 🥇 | **PPO** | Actor-Critic RL | **WINNER!** |
| 🥈 | DQN | Value-based RL | Strong |
| 🥉 | Q-Learning | Tabular RL | Good |
| 4️⃣ | Time Based | Heuristic | Best baseline |
| 5️⃣ | Demand Based | Heuristic | |
| 6️⃣ | Linear Decay | Heuristic | |
| 7️⃣ | Fixed Price | Heuristic | Worst |

---

## ✅ Proven PPO Behaviors

### 1. Deadline Discounting
PPO drops prices near departure
to clear remaining inventory!

Early (20-30 days) : $250 avg
Urgent (0-5 days) : $100 avg
Price Drop : ~60% ✅

### 2. Scarcity Premium Pricing
PPO raises prices when
inventory is running low!

High inventory (>40) : $150 avg
Low inventory (<10) : $250 avg
Price Premium : ~67% ✅

---

## 🧠 Algorithm Comparison

| Feature | Q-Learning | DQN | PPO |
|---|---|---|---|
| Type | Value | Value | Policy |
| Network | Q-table | Neural Net | Actor-Critic |
| Training | TD Update | Off-policy | On-policy |
| Exploration | ε-greedy | ε-greedy | Entropy bonus |
| Stability | Medium | Good | Best |
| Used in | Classic RL | Atari games | **ChatGPT!** |

---

## 🏗️ PPO ArchitectureInput : 2 neurons (inventory, days_left)
↓
Shared : 128 neurons (ReLU)
↓
Shared : 64 neurons (ReLU)
↓
┌────┴────┐
↓ ↓
Actor Critic
6 neurons 1 neuron
(Softmax) (Linear)
↓ ↓
Probability State
per price Value

---

## 🔑 DQN Key Innovations

| Innovation | Purpose |
|---|---|
| Experience Replay (10,000) | Breaks correlations |
| Target Network | Stable training targets |
| Epsilon Greedy (1.0→0.01) | Exploration strategy |
| Gradient Clipping | Prevents explosions |

---

## 🔑 PPO Key Innovations

| Innovation | Purpose |
|---|---|
| Clipped Objective (ε=0.2) | Stable updates |
| GAE (λ=0.95) | Better advantages |
| On-policy Rollouts | Fresh experience |
| Entropy Bonus | Encourages exploration |

---

## 📁 Project Structure
## 📁 Project Structure

```text
RL-Dynamic-Pricing/
│
├── src/
│   ├── config.py                     # All hyperparameters
│   ├── project_runner.py             # Complete pipeline
│   ├── project_summary.py            # Project summary
│   │
│   ├── environment/
│   │   ├── pricing_env.py            # Custom Gym environment
│   │   ├── env_config.py             # Environment parameters
│   │   └── env_validator.py          # Interface validation
│   │
│   ├── agents/
│   │   ├── baseline_agents.py        # Five baseline pricing agents
│   │   ├── q_learning_agent.py       # Q-Learning implementation
│   │   ├── agent_registry.py         # Agent factory
│   │   │
│   │   ├── dqn/
│   │   │   ├── dqn_network.py        # DQN neural network
│   │   │   ├── dqn_agent.py          # DQN agent
│   │   │   ├── replay_buffer.py      # Experience replay buffer
│   │   │   └── dqn_utils.py          # DQN utilities
│   │   │
│   │   └── ppo/
│   │       ├── ppo_network.py        # PPO Actor-Critic network
│   │       ├── ppo_agent.py          # PPO agent
│   │       └── ppo_utils.py          # PPO utilities
│   │
│   ├── training/
│   │   ├── q_learning_trainer.py
│   │   ├── dqn_trainer.py
│   │   ├── ppo_trainer.py
│   │   ├── ppo_hypertuner.py         # Hyperparameter search
│   │   └── config_manager.py         # Best configurations
│   │
│   ├── simulation/
│   │   ├── final_simulation.py       # 1000-season simulation
│   │   ├── season_simulator.py       # Simulation utilities
│   │   └── business_value.py         # Business value analysis
│   │
│   ├── analysis/
│   │   ├── week3_analyzer.py
│   │   ├── final_comparison.py
│   │   ├── final_proof.py
│   │   └── trajectory_insights_final.py
│   │
│   ├── visualization/
│   │   ├── business_dashboard.py     # Main dashboard
│   │   ├── price_dashboard.py        # Price trajectory dashboard
│   │   └── trajectory_insights.py
│   │
│   └── tests/
│       ├── test_environment.py       # 8 environment tests
│       ├── test_agents.py            # 11 agent tests
│       └── test_ppo.py               # 7 PPO tests
│
├── notebooks/
│   ├── week1/                        # Week 1 notebooks
│   ├── week2/                        # Week 2 notebooks
│   ├── week3/                        # Week 3 notebooks
│   └── week4/                        # Week 4 notebooks
│
├── results/                          # Generated outputs
├── models/                           # Trained models (gitignored)
├── FINAL_SUBMISSION_CHECKLIST.md
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### Quick Start (5 minutes)
```bash
git clone https://github.com/Ankursaini018/
RL-Dynamic-Pricing.git
cd RL-Dynamic-Pricing
pip install -r requirements.txt
cd src
python project_runner.py --quick
```

### Full Pipeline (30 minutes)
```bash
cd src
python project_runner.py
```

### Run All Tests (26 tests)
```bash
cd src
python tests/test_environment.py
python tests/test_agents.py
python tests/test_ppo.py
```

### Individual Components
```bash
# Environment
python environment/pricing_env.py

# PPO (Best Agent)
python agents/ppo/ppo_agent.py

# Final 1000-season Simulation
python simulation/final_simulation.py

# Project Summary
python project_summary.py
```

---

## 📊 Hyperparameter Summary

### Best PPO Config
| Parameter | Value |
|---|---|
| Learning Rate | 0.0005 |
| Clip Range | 0.2 |
| N Epochs | 15 |
| Entropy Coef | 0.02 |
| GAE Lambda | 0.95 |
| Gamma | 0.99 |

### Best DQN Config
| Parameter | Value |
|---|---|
| Learning Rate | 0.001 |
| Batch Size | 64 |
| Buffer Size | 10,000 |
| Target Update | Every 10 eps |
| Gamma | 0.99 |

---

## 🧪 Unit Tests

| Module | Tests | Status |
|---|---|---|
| Environment | 8 | ✅ All Pass |
| Agents (baseline + QL) | 11 | ✅ All Pass |
| PPO | 7 | ✅ All Pass |
| **Total** | **26** | **✅ All Pass** |

---

## 📅 Week-by-Week Progress

| Week | Focus | Key Achievement |
|---|---|---|
| Week 1 | MDP + Q-Learning | Q-Learning beats baselines |
| Week 2 | Deep Q-Network | DQN beats Q-Learning |
| Week 3 | PPO Agent | PPO beats DQN! |
| Week 4 | Final Polish | 1000-season proof complete |

---

---

## 🎯 Final Status — 2nd August 2026

### Everything Complete!
| Component | Status |
|---|---|
| Week 1 MDP + Q-Learning | ✅ |
| Week 2 Deep Q-Network | ✅ |
| Week 3 PPO Agent | ✅ |
| Week 4 Final Polish | ✅ |
| All 21 Issues | ✅ Closed |
| All 26 Tests | ✅ Passing |
| 28+ Commit Days | ✅ |
| Business Dashboard | ✅ |
| 1000-Season Proof | ✅ |

### Final Review
**Window: 5th - 10th August 2026**
**Status: READY! 💪**

## 📊 GitHub Stats

| Metric | Value |
|---|---|
| Commit Days | 28+ consecutive |
| Issues Closed | 21/21 |
| Python Scripts | 50+ |
| Notebooks | 25+ |
| Unit Tests | 26 |

---

## 🔗 Links

- **GitHub**: github.com/Ankursaini018/RL-Dynamic-Pricing
- **Intern**: Solo Worker
- **Program**: Infotact DS/ML Internship 2026
- **Duration**: 5th July - 4th August 2026

