# 🎯 RL Dynamic Pricing
### Infotact DS/ML Internship 2026 | Ankur Saini

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red)
![Best](https://img.shields.io/badge/Best_Agent-PPO-gold)
![Tests](https://img.shields.io/badge/Tests-26_Passing-success)
![Issues](https://img.shields.io/badge/Issues-21%2F21_Closed-success)
![Commits](https://img.shields.io/badge/Daily_Commits-30%2B-yellow)

---

## 🎯 Overview

A complete Reinforcement Learning system that trains an AI agent to learn optimal dynamic pricing for travel and hospitality through thousands of simulated booking seasons — **without any labeled data!**

> **Fun Fact:** PPO (the winning algorithm) is the **same algorithm used to train ChatGPT** through RLHF!

---

## 🏗️ MDP Formulation

| Component | Value |
|---|---|
| State | (remaining_inventory, days_left) |
| Actions | 6 prices: $50 · $100 · $150 · $200 · $250 · $300 |
| Reward | Revenue earned per sale |
| Penalty | -10 per unsold ticket |
| State Space | 1,581 discrete states |
| Max Inventory | 50 tickets / rooms |
| Max Days | 30 days per season |

---

## 🧠 Algorithms

| Algorithm | Type | Architecture | Result |
|---|---|---|---|
| Q-Learning | Tabular RL | Q-table (9,486 entries) | Beats all baselines |
| DQN | Value-based RL | 2 → 128 → 64 → 6 | Beats Q-Learning |
| **PPO** | **Policy-based RL** | **Actor-Critic** | **🥇 WINNER** |

### Best PPO Config

| Parameter | Value |
|---|---|
| Learning Rate | 0.0005 |
| Clip Range | 0.2 |
| N Epochs | 15 |
| Entropy Coef | 0.02 |
| GAE Lambda | 0.95 |

---

## 🏆 Final Rankings (1000 Seasons)

| Rank | Agent | Type |
|---|---|---|
| 🥇 | PPO | Actor-Critic RL |
| 🥈 | DQN | Value-based RL |
| 🥉 | Q-Learning | Tabular RL |
| 4️⃣ | Time Based | Heuristic |
| 5️⃣ | Demand Based | Heuristic |
| 6️⃣ | Linear Decay | Heuristic |
| 7️⃣ | Fixed Price | Heuristic |

---

## ✅ Proven Behaviors

**PPO discovered these strategies completely on its own!**

| Behavior | Description | Proof |
|---|---|---|
| Deadline Discounting | Drops prices near departure to clear inventory | ~60% price drop |
| Scarcity Premium | Raises prices for low inventory | +67% premium |

Both proved with **t-test p < 0.05** over 200 episodes.

---

## 📁 Project Structure

```
RL-Dynamic-Pricing/
├── src/
│   ├── config.py
│   ├── project_runner.py
│   ├── run_all_checks.py
│   ├── final_verification.py
│   ├── project_summary.py
│   ├── environment/
│   │   ├── pricing_env.py
│   │   ├── env_config.py
│   │   └── env_validator.py
│   ├── agents/
│   │   ├── baseline_agents.py
│   │   ├── q_learning_agent.py
│   │   ├── agent_registry.py
│   │   ├── dqn/
│   │   │   ├── dqn_network.py
│   │   │   ├── dqn_agent.py
│   │   │   ├── replay_buffer.py
│   │   │   └── dqn_utils.py
│   │   └── ppo/
│   │       ├── ppo_network.py
│   │       ├── ppo_agent.py
│   │       └── ppo_utils.py
│   ├── training/
│   │   ├── dqn_trainer.py
│   │   ├── ppo_trainer.py
│   │   ├── ppo_hypertuner.py
│   │   └── config_manager.py
│   ├── simulation/
│   │   ├── final_simulation.py
│   │   ├── season_simulator.py
│   │   └── business_value.py
│   ├── analysis/
│   │   ├── final_comparison.py
│   │   ├── final_proof.py
│   │   └── week3_analyzer.py
│   ├── visualization/
│   │   ├── business_dashboard.py
│   │   └── price_dashboard.py
│   └── tests/
│       ├── test_environment.py
│       ├── test_agents.py
│       └── test_ppo.py
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
├── notebooks/
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   └── week4/
├── results/
├── models/             ← gitignored
├── data/               ← gitignored
├── requirements.txt
├── PROJECT_COMPLETE.md
└── README.md
```

---

## 🚀 How to Run

### Backend (ML Pipeline)

```bash
# Clone repo
git clone https://github.com/Ankursaini018/RL-Dynamic-Pricing.git
cd RL-Dynamic-Pricing

# Install dependencies
pip install -r requirements.txt

# Run all checks first
python src/run_all_checks.py

# Quick test (5 minutes)
python src/project_runner.py --quick

# Full pipeline (30 minutes)
python src/project_runner.py
```

### Run Individual Agents

```bash
# Environment test
python src/environment/pricing_env.py

# PPO — Best agent
python src/agents/ppo/ppo_agent.py

# DQN
python src/agents/dqn/dqn_agent.py

# Q-Learning
python src/agents/q_learning_agent.py

# Final 1000-season simulation
python src/simulation/final_simulation.py
```

### Run All Tests

```bash
python src/tests/test_environment.py
python src/tests/test_agents.py
python src/tests/test_ppo.py
```

### Frontend (Dashboard)

```bash
# Go to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser at:
# http://localhost:5173
```

### Run Both Together

```bash
# Terminal 1 — Backend
python src/project_runner.py --quick

# Terminal 2 — Frontend
cd frontend
npm run dev
```

---

## 🛠️ Tech Stack

**Backend:** Python 3.11 · PyTorch 2.0 · Gymnasium · NumPy · Pandas · SciPy · Matplotlib

**Frontend:** React · Tailwind CSS · Recharts · Vite

**DevOps:** Git · GitHub · Vercel

---

## 🧪 Unit Tests

| Module | Tests | Status |
|---|---|---|
| Environment | 8 | ✅ |
| Agents | 11 | ✅ |
| PPO | 7 | ✅ |
| **Total** | **26** | **✅ All Pass** |

---

## 📈 GitHub Stats

| Metric | Value |
|---|---|
| Issues Closed | 21 / 21 |
| Consecutive Commits | 30+ days |
| Python Scripts | 50+ |
| Unit Tests | 26 passing |
| Notebooks | 26 |

---

## 🔗 Links

| Resource | Link |
|---|---|
| GitHub | [RL-Dynamic-Pricing](https://github.com/Ankursaini018/RL-Dynamic-Pricing) |
| Certificate | IF475373 |

---

*Ankur Saini · Infotact DS/ML Internship 2026 · 5th July - 4th August 2026*