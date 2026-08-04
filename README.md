# 🎯 RL Dynamic Pricing
## Infotact DS/ML Technical Internship 2026

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Week](https://img.shields.io/badge/Week-4%20Complete-blue)
![Tests](https://img.shields.io/badge/Tests-26%20Passing-green)
![Best](https://img.shields.io/badge/Best%20Agent-PPO-gold)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)

---

# 🎯 Problem Statement

Airlines and hotels must sell **finite inventory**
over **limited time**. Traditional fixed pricing
leaves significant revenue on the table.

**RL Solution:** Train an agent that learns
optimal dynamic pricing through thousands of
simulated booking seasons!

---

# 🏗️ MDP Formulation

| Component | Value |
|---|---|
| **State** | (remaining_inventory, days_until_departure) |
| **Actions** | 6 price levels ($50, $100, $150, $200, $250, $300) |
| **Reward** | Revenue from each sale |
| **Penalty** | -10 per unsold ticket |
| **State Space** | 1,581 discrete states |

---

# 📊 Final Results (1000 Seasons)

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

# ✅ Proven PPO Behaviors

## 1. Deadline Discounting

PPO drops prices near departure
to clear remaining inventory!

- Early (20–30 days): **$250 avg**
- Urgent (0–5 days): **$100 avg**
- **Price Drop:** ~60% ✅

---

## 2. Scarcity Premium Pricing

PPO raises prices when
inventory is running low!

- High inventory (>40): **$150 avg**
- Low inventory (<10): **$250 avg**
- **Price Premium:** ~67% ✅

---

# 🧠 Algorithm Comparison

| Feature | Q-Learning | DQN | PPO |
|---|---|---|---|
| Type | Value | Value | Policy |
| Network | Q-table | Neural Net | Actor-Critic |
| Training | TD Update | Off-policy | On-policy |
| Exploration | ε-greedy | ε-greedy | Entropy bonus |
| Stability | Medium | Good | Best |
| Used in | Classic RL | Atari Games | **ChatGPT!** |

---

# 🏗️ PPO Architecture

```text
Input : 2 neurons (inventory, days_left)
              │
              ▼
Shared : 128 neurons (ReLU)
              │
              ▼
Shared : 64 neurons (ReLU)
              │
      ┌───────┴────────┐
      ▼                ▼
   Actor            Critic
 6 neurons         1 neuron
 (Softmax)         (Linear)
      ▼                ▼
Probability      State Value
per Price
```

---

# 🔑 DQN Key Innovations

| Innovation | Purpose |
|---|---|
| Experience Replay (10,000) | Breaks correlations |
| Target Network | Stable training targets |
| Epsilon Greedy (1.0 → 0.01) | Exploration strategy |
| Gradient Clipping | Prevents exploding gradients |

---

# 🔑 PPO Key Innovations

| Innovation | Purpose |
|---|---|
| Clipped Objective (ε = 0.2) | Stable updates |
| GAE (λ = 0.95) | Better advantages |
| On-policy Rollouts | Fresh experience |
| Entropy Bonus | Encourages exploration |

---

# 📁 Project Structure

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
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   └── week4/
│
├── results/
├── models/
├── FINAL_SUBMISSION_CHECKLIST.md
├── requirements.txt
└── README.md
```

---

# 🚀 How to Run

## Quick Start (5 Minutes)

```bash
git clone https://github.com/Ankursaini018/RL-Dynamic-Pricing.git

cd RL-Dynamic-Pricing

pip install -r requirements.txt

cd src

python project_runner.py --quick
```

---

## Full Pipeline (30 Minutes)

```bash
cd src

python project_runner.py
```

---

## Run All Tests (26 Tests)

```bash
cd src

python tests/test_environment.py

python tests/test_agents.py

python tests/test_ppo.py
```

---

## Individual Components

```bash
# Environment
python environment/pricing_env.py

# PPO (Best Agent)
python agents/ppo/ppo_agent.py

# Final 1000-Season Simulation
python simulation/final_simulation.py

# Project Summary
python project_summary.py
```

---

# 📊 Hyperparameter Summary

## Best PPO Configuration

| Parameter | Value |
|---|---:|
| Learning Rate | 0.0005 |
| Clip Range | 0.2 |
| N Epochs | 15 |
| Entropy Coefficient | 0.02 |
| GAE Lambda | 0.95 |
| Gamma | 0.99 |

---

## Best DQN Configuration

| Parameter | Value |
|---|---:|
| Learning Rate | 0.001 |
| Batch Size | 64 |
| Replay Buffer Size | 10,000 |
| Target Network Update | Every 10 Episodes |
| Gamma | 0.99 |

---

# 🧪 Unit Tests

| Module | Tests | Status |
|---|---:|---|
| Environment | 8 | ✅ All Pass |
| Agents (Baseline + Q-Learning) | 11 | ✅ All Pass |
| PPO | 7 | ✅ All Pass |
| **Total** | **26** | **✅ All Pass** |

---

# 📅 Week-by-Week Progress

| Week | Focus | Achievement |
|---|---|---|
| **Week 1** | MDP + Environment + Q-Learning | Q-Learning outperformed heuristic baselines |
| **Week 2** | Deep Q-Network (DQN) | DQN outperformed Q-Learning |
| **Week 3** | PPO Agent | PPO achieved the best overall performance |
| **Week 4** | Final Polish & Documentation | 1000-season proof, dashboard and documentation completed |

---

# 📊 GitHub Statistics

| Metric | Value |
|---|---:|
| Consecutive Commit Days | **30+** |
| GitHub Issues Closed | **21 / 21** |
| Python Scripts | **50+** |
| Jupyter Notebooks | **25+** |
| Unit Tests | **26** |
| Project Duration | **4 Weeks** |

---

# 📅 Project Timeline

| Date | Milestone |
|---|---|
| **5th July 2026** | Project Started |
| **11th July 2026** | Week 1 Completed |
| **18th July 2026** | Week 2 Completed |
| **26th July 2026** | Week 3 Completed |
| **4th August 2026** | Week 4 Completed |
| **5th–10th August 2026** | Final Review |

---

# 🎉 PROJECT COMPLETE — 4th August 2026

## Final Status

| Item | Status |
|---|---|
| All 4 Weeks | ✅ Complete |
| All 21 Issues | ✅ Closed |
| All 26 Tests | ✅ Passing |
| Daily Commits | ✅ 30+ Days |
| Business Dashboard | ✅ Done |
| 1000-Season Proof | ✅ Done |
| Documentation | ✅ Done |

---

## 🚀 How to Run

### Single Command (Recommended)

```bash
python src/run_all_checks.py
```

---

### Full Pipeline

```bash
python src/project_runner.py
```

---

### Quick Test

```bash
python src/project_runner.py --quick
```

---

# 🏆 Final Project Achievements

- ✅ Custom Gymnasium Environment
- ✅ Markov Decision Process (MDP) Formulation
- ✅ 5 Baseline Pricing Agents
- ✅ Tabular Q-Learning Agent
- ✅ Deep Q-Network (DQN)
- ✅ PPO Actor-Critic Agent
- ✅ Hyperparameter Optimization
- ✅ 1000-Season Evaluation
- ✅ Statistical Significance Testing
- ✅ Business Value Analysis
- ✅ Dynamic Pricing Dashboard
- ✅ Complete Documentation
- ✅ Professional GitHub Repository

---

# 📈 Final Performance Ranking

| Rank | Agent |
|---|---|
| 🥇 | PPO |
| 🥈 | DQN |
| 🥉 | Q-Learning |
| 4️⃣ | Time-Based Pricing |
| 5️⃣ | Demand-Based Pricing |
| 6️⃣ | Linear Decay |
| 7️⃣ | Fixed Price |

---

# 🎯 Final Review

**Review Window:** **5th – 10th August 2026**

**Project Status:**

> **READY FOR FINAL REVIEW! 💪🔥**

---

# 👨‍💻 Developer

**Completed By:** Ankur Saini

**Program:** Infotact DS/ML Internship 2026

**Project:** Reinforcement Learning Dynamic Pricing System

**Duration:** **5th July – 4th August 2026**

---

# 📌 Repository

**GitHub Repository**

```
https://github.com/Ankursaini018/RL-Dynamic-Pricing
```

---

# ⭐ Acknowledgement

This project was completed as part of the **Infotact DS/ML Technical Internship 2026**, demonstrating the application of **Reinforcement Learning** techniques—including **Q-Learning, Deep Q-Network (DQN), and Proximal Policy Optimization (PPO)**—to solve a real-world dynamic pricing problem in the travel and hospitality domain.

---

## 🚀 Project Completed Successfully

```
██████╗ ██╗     
██╔══██╗██║     
██████╔╝██║     
██╔══██╗██║     
██║  ██║███████╗
╚═╝  ╚═╝╚══════╝

Dynamic Pricing Project

Status : ✅ COMPLETE
Date   : 4th August 2026

Thank You!
```