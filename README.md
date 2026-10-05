# 🎯 RL Dynamic Pricing
## Infotact DS/ML Technical Internship 2026

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![RL](https://img.shields.io/badge/RL-PPO%20%7C%20DQN%20%7C%20Q--Learning-gold)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red)
![Issues](https://img.shields.io/badge/Issues-21%2F21%20Closed-success)
![Commits](https://img.shields.io/badge/Commits-30%2B%20Daily-orange)
![Tests](https://img.shields.io/badge/Tests-26%20Passing-green)

---

## 🎯 Problem Statement

Airlines and hotels must sell finite
inventory over limited time. Traditional
fixed pricing leaves significant revenue
on the table because it cannot adapt to
changing demand and time pressure.

**Solution:** Train a Reinforcement
Learning agent that discovers optimal
dynamic pricing through thousands of
simulated booking seasons — without
any labeled data!

---

## 🏗️ Project Architecture
RL-Dynamic-Pricing/
│
├── src/
│ ├── config.py
│ ├── project_runner.py
│ ├── project_summary.py
│ ├── final_verification.py
│ ├── run_all_checks.py
│ │
│ ├── environment/
│ │ ├── pricing_env.py
│ │ ├── env_config.py
│ │ └── env_validator.py
│ │
│ ├── agents/
│ │ ├── baseline_agents.py
│ │ ├── q_learning_agent.py
│ │ ├── agent_registry.py
│ │ ├── dqn/
│ │ │ ├── dqn_network.py
│ │ │ ├── dqn_agent.py
│ │ │ ├── replay_buffer.py
│ │ │ └── dqn_utils.py
│ │ └── ppo/
│ │ ├── ppo_network.py
│ │ ├── ppo_agent.py
│ │ └── ppo_utils.py
│ │
│ ├── training/
│ │ ├── q_learning_trainer.py
│ │ ├── dqn_trainer.py
│ │ ├── ppo_trainer.py
│ │ ├── ppo_hypertuner.py
│ │ └── config_manager.py
│ │
│ ├── simulation/
│ │ ├── final_simulation.py
│ │ ├── season_simulator.py
│ │ └── business_value.py
│ │
│ ├── analysis/
│ │ ├── final_comparison.py
│ │ ├── final_proof.py
│ │ └── week3_analyzer.py
│ │
│ ├── visualization/
│ │ ├── business_dashboard.py
│ │ └── price_dashboard.py
│ │
│ └── tests/
│ ├── test_environment.py
│ ├── test_agents.py
│ └── test_ppo.py
│
├── notebooks/
│ ├── week1/ (7 notebooks)
│ ├── week2/ (7 notebooks)
│ ├── week3/ (7 notebooks)
│ └── week4/ (7 notebooks)
│
├── results/
├── models/ (gitignored)
├── data/ (gitignored)
├── requirements.txt
├── PROJECT_COMPLETE.md
└── README.md


---

## 🏗️ MDP Formulation

| Component | Value |
|---|---|
| **State** | (remaining_inventory, days_left) |
| **Actions** | 6 prices: $50/$100/$150/$200/$250/$300 |
| **Reward** | Revenue from each sale |
| **Penalty** | -10 per unsold ticket |
| **State Space** | 1,581 discrete states |
| **Max Inventory** | 50 tickets/rooms |
| **Max Days** | 30 days per season |

---

## 🧠 Algorithms Implemented

### Week 1 — Q-Learning
Type : Tabular Value-based RL
Q-Table : 51 × 31 × 6 = 9,486 entries
Episodes : 5,000
Alpha : 0.10 (learning rate)
Gamma : 0.99 (discount factor)
Epsilon : 1.0 → 0.01 (decay)
Result : Beats all 5 baselines!


### Week 2 — DQN (Deep Q-Network)
Type : Neural Network Value-based
Architecture : 2 → 128 → 64 → 6
Parameters : ~10,000
Episodes : 2,000
Buffer : 10,000 experiences
Batch Size : 64
Target Update: Every 10 episodes
Result : Outperforms Q-Learning!


### Week 3 — PPO (WINNER! 🏆)
Type : Actor-Critic Policy-based
Architecture : Shared 2→128→64
Actor → 6 (Softmax)
Critic → 1 (Linear)
Fun Fact : Same algo as ChatGPT!
Best LR : 0.0005
Clip Range : 0.2
N Epochs : 15
Configs Tested: 8 hyperparameter configs
Result : BEST revenue! Beats all!


---

## 🏆 Final Rankings (1000 Seasons)

| Rank | Agent | Type |
|---|---|---|
| 🥇 | **PPO** | Actor-Critic RL |
| 🥈 | DQN | Value-based RL |
| 🥉 | Q-Learning | Tabular RL |
| 4️⃣ | Time Based | Heuristic |
| 5️⃣ | Demand Based | Heuristic |
| 6️⃣ | Linear Decay | Heuristic |
| 7️⃣ | Fixed Price | Heuristic |

---

## ✅ Proven Behaviors

### 1. Deadline Discounting
PPO drops prices near departure
to clear remaining inventory!

Early avg (20-30 days): ~$250
Urgent avg (0-5 days) : ~$100
Price Drop : ~60% ✅


### 2. Scarcity Premium Pricing
PPO raises prices when inventory low!

High inventory (>40): ~$150
Low inventory (<10): ~$250
Price Premium : +67% ✅


Both proved with t-test p < 0.05
over 200 episodes!

---

## 🚀 How to Run

### 1. Clone Repository
```bash
git clone https://github.com/Ankursaini018/
RL-Dynamic-Pricing.git
cd RL-Dynamic-Pricing
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run All Checks (Recommended First)
```bash
python src/run_all_checks.py
```

### 4. Quick Pipeline Test
```bash
python src/project_runner.py --quick
```

### 5. Full Pipeline
```bash
python src/project_runner.py
```

### 6. Run Individual Agents
```bash
# Environment test
python src/environment/pricing_env.py

# Q-Learning
python src/agents/q_learning_agent.py

# DQN
python src/agents/dqn/dqn_agent.py

# PPO (Best Agent!)
python src/agents/ppo/ppo_agent.py
```

### 7. Run All Tests
```bash
python src/tests/test_environment.py
python src/tests/test_agents.py
python src/tests/test_ppo.py
```

### 8. Final 1000-Season Simulation
```bash
python src/simulation/final_simulation.py
```

### 9. Open Key Notebook
```bash
jupyter notebook notebooks/week4/
week4_day2_business_dashboard.ipynb
```

### 10. Run Frontend Dashboard
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

---

## 🛠️ Tech Stack

| Category | Tool |
|---|---|
| Language | Python 3.11 |
| RL Framework | Custom (from scratch!) |
| DL Framework | PyTorch 2.0 |
| Environment | Gymnasium (OpenAI Gym) |
| Analysis | NumPy, Pandas, SciPy |
| Visualization | Matplotlib, Seaborn |
| Frontend | React + Tailwind CSS |
| Version Control | Git + GitHub |

---

## 📊 Hyperparameter Tuning

### Best PPO Config (from 8-config search)
| Parameter | Value |
|---|---|
| Learning Rate | 0.0005 |
| Clip Range | 0.2 |
| N Epochs | 15 |
| Entropy Coef | 0.02 |
| GAE Lambda | 0.95 |
| Gamma | 0.99 |

---

## 🧪 Unit Tests

| Module | Tests | Status |
|---|---|---|
| Environment | 8 | ✅ All Pass |
| Agents | 11 | ✅ All Pass |
| PPO | 7 | ✅ All Pass |
| **Total** | **26** | **✅ All Pass** |

---

## 📈 GitHub Stats

| Metric | Value |
|---|---|
| Issues Closed | 21/21 ✅ |
| Daily Commits | 30+ consecutive ✅ |
| Python Scripts | 50+ ✅ |
| Notebooks | 26 ✅ |
| Unit Tests | 26 passing ✅ |

---

## 🔗 Links

- **GitHub:** github.com/Ankursaini018/RL-Dynamic-Pricing
- **Live Demo:** [your vercel link here]
- **Intern:** Ankur Saini
- **Program:** Infotact DS/ML Internship 2026
- **Duration:** 5th July - 4th August 2026
- **Certificate:** IF475373