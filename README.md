# 🚀 RL Dynamic Pricing using Reinforcement Learning

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=for-the-badge&logo=pytorch)
![Gymnasium](https://img.shields.io/badge/Gymnasium-Custom%20Environment-orange?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-blue?style=for-the-badge&logo=numpy)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green?style=for-the-badge)
![PyTest](https://img.shields.io/badge/Tests-26%20Passing-success?style=for-the-badge)
![Status](https://img.shields.io/badge/Week-3%20Complete-brightgreen?style=for-the-badge)

</p>

---

# 📌 Project Overview

This repository contains an end-to-end **Reinforcement Learning based Dynamic Pricing System** developed as **Project 2** during the **Infotact DS/ML Technical Internship 2026**.

The project demonstrates how Reinforcement Learning algorithms can automatically learn optimal pricing strategies that maximize revenue while adapting to changes in inventory, customer demand, and selling deadlines.

Instead of relying on manually designed pricing rules, the agents continuously interact with a custom-built simulation environment to discover profitable pricing policies through experience.

The project gradually progresses from traditional rule-based approaches to advanced Deep Reinforcement Learning techniques.

---

# 🎯 Problem Statement

Dynamic pricing is widely used in industries such as:

- Airlines
- Hotels
- E-commerce
- Retail
- Ride Sharing
- Event Ticketing

Traditional pricing methods struggle to react to rapidly changing market conditions.

This project addresses that challenge by allowing Reinforcement Learning agents to learn:

- Optimal pricing decisions
- Revenue maximization
- Inventory management
- Deadline-aware pricing
- Demand-sensitive pricing

through continuous interaction with a simulated marketplace.

---

# ✨ Project Highlights

### ✅ Custom Gymnasium Environment

- Markov Decision Process (MDP)
- Inventory Simulation
- Stochastic Customer Demand
- Reward Engineering
- Episode-based Environment

### ✅ Rule-Based Pricing Agents

- Fixed Price Agent
- Time-Based Pricing
- Demand-Based Pricing
- Linear Decay Pricing

### ✅ Reinforcement Learning Agents

- Q-Learning
- Deep Q Network (DQN)
- Proximal Policy Optimization (PPO)

### ✅ PPO Features

- Actor-Critic Architecture
- Rollout Buffer
- Generalized Advantage Estimation (GAE)
- PPO Clipped Objective
- Entropy Regularization
- Hyperparameter Grid Search

### ✅ Evaluation

- Revenue Comparison
- Agent Ranking
- Dashboard Visualization
- Training Curves
- Policy Analysis
- Statistical Evaluation

---

# 🏆 Internship Progress

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Environment + Q-Learning | ✅ Completed |
| Week 2 | Deep Q Network (DQN) | ✅ Completed |
| Week 3 | PPO + Hyperparameter Optimization | ✅ Completed |
| Week 4 | Final Documentation & Submission | 🔄 In Progress |

---

# 🧠 Algorithms Implemented

| Algorithm | Category | Status |
|------------|----------|--------|
| Fixed Price | Rule-Based | ✅ |
| Time-Based | Rule-Based | ✅ |
| Demand-Based | Rule-Based | ✅ |
| Linear Decay | Rule-Based | ✅ |
| Q-Learning | Tabular RL | ✅ |
| Deep Q Network | Deep RL | ✅ |
| PPO | Policy Gradient RL | ✅ |

---

# 🏗️ Project Architecture

```text
                  Customer Demand
                         │
                         ▼
            Custom Gymnasium Environment
                         │
     ┌───────────────────┼────────────────────┐
     │                   │                    │
     ▼                   ▼                    ▼
 Rule-Based         Q-Learning          Deep RL Agents
   Agents                                 │
                                          ▼
                                    Deep Q Network
                                          │
                                          ▼
                               Proximal Policy Optimization
                                          │
                                          ▼
                              Revenue Evaluation & Analysis
```

---

# 📂 Project Structure

```text
RL-Dynamic-Pricing/
│
├── data/
├── models/
├── notebooks/
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   └── week4/
│
├── results/
│
├── src/
│   ├── agents/
│   │   ├── baseline_agents.py
│   │   ├── q_learning_agent.py
│   │   ├── dqn/
│   │   └── ppo/
│   ├── analysis/
│   ├── environment/
│   ├── tests/
│   ├── training/
│   ├── utils/
│   ├── visualization/
│   └── config.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# ⚙️ Technology Stack

## Programming Language

- Python 3.11

## Reinforcement Learning

- Gymnasium
- NumPy
- Pandas

## Deep Learning

- PyTorch

## Data Visualization

- Matplotlib
- Seaborn

## Development Tools

- Jupyter Notebook
- VS Code
- Git
- GitHub

---

# ⚡ Installation

## Clone the Repository

```bash
git clone https://github.com/Ankursaini018/RL-Dynamic-Pricing.git

cd RL-Dynamic-Pricing
```

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 What's Next?

The next section covers:

- Running the project
- Reinforcement Learning pipeline
- Week-wise execution
- Training commands
- Evaluation workflow
- Testing
- Performance analysis

# ▶️ Running the Project

This project is organized week-by-week following the internship roadmap. Each week introduces progressively more advanced Reinforcement Learning concepts.

---

## Week 1 — Q-Learning

### Train Q-Learning Agent

```bash
python src/agents/q_learning_agent.py
```

### Extract Learned Policy

```bash
python src/utils/policy_extractor.py
```

### Analyze Price Trajectories

```bash
python src/utils/price_trajectory_analyzer.py
```

---

## Week 2 — Deep Q Network (DQN)

### Train DQN Agent

```bash
python src/training/dqn_trainer.py
```

### Compare DQN with Q-Learning

```bash
python src/analysis/dqn_vs_qlearning.py
```

### Generate Performance Dashboard

```bash
python src/visualization/price_dashboard.py
```

---

## Week 3 — Proximal Policy Optimization (PPO)

### Train PPO Agent

```bash
python src/training/ppo_trainer.py
```

### Hyperparameter Optimization

```bash
python src/training/ppo_hypertuner.py
```

### Combined Hyperparameter Search

```bash
python src/training/combined_tuner.py
```

### Week 3 Analysis

```bash
python src/analysis/week3_analyzer.py
```

### Final Comparison

```bash
python src/analysis/final_comparison.py
```

---

## Complete Project Pipeline

### Quick Test

```bash
cd src

python project_runner.py --quick
```

### Full Training Pipeline

```bash
python project_runner.py
```

### Run All Unit Tests

```bash
python tests/test_environment.py

python tests/test_agents.py

python tests/test_ppo.py
```

---

# 📓 Jupyter Notebooks

Each notebook represents a milestone in the internship journey.

| Week | Notebook | Purpose |
|------|----------|---------|
| Week 1 | MDP + Q-Learning | RL Foundations |
| Week 2 | Deep Q Network | Deep Reinforcement Learning |
| Week 3 | PPO + Hyperparameter Search | Advanced RL |
| Week 4 | Final Documentation | Submission Preparation |

---

# 🔄 Reinforcement Learning Workflow

```text
Environment

        │

        ▼

Observe Current State

        │

        ▼

Agent Selects Price

        │

        ▼

Environment Executes Action

        │

        ▼

Reward is Calculated

        │

        ▼

Policy is Updated

        │

        ▼

Repeat Until Episode Ends
```

---

# 🧠 Implemented Pricing Strategies

## Rule-Based Agents

### Fixed Price Agent

A simple baseline that always selects the same price.

**Advantages**

- Easy to understand
- Fast execution
- Useful benchmark

**Limitations**

- No learning capability
- Cannot adapt to demand changes

---

### Time-Based Pricing

Prices gradually decrease as the selling deadline approaches.

Typical applications include:

- Airline tickets
- Hotel reservations
- Perishable inventory

---

### Demand-Based Pricing

Prices change according to customer demand.

**Advantages**

- Responsive pricing
- Easy implementation

**Limitations**

- Limited long-term optimization
- No policy learning

---

### Linear Decay Pricing

Prices decrease smoothly throughout the selling period to encourage sales before the deadline.

---

# 🤖 Reinforcement Learning Agents

## Q-Learning

A classic tabular Reinforcement Learning algorithm.

### Key Features

- Bellman Equation
- Q-Table Updates
- ε-Greedy Exploration
- Model-Free Learning

---

## Deep Q Network (DQN)

Extends Q-Learning by replacing the Q-table with a neural network.

### Improvements

- Deep Neural Network
- Experience Replay
- Target Network
- Stable Learning
- Better Scalability

---

## Proximal Policy Optimization (PPO)

PPO is an advanced policy-gradient algorithm based on the Actor-Critic architecture.

### Core Components

- Actor-Critic Network
- PPO Clipped Objective
- Rollout Buffer
- Generalized Advantage Estimation (GAE)
- Entropy Regularization
- On-Policy Learning

---

# 🏆 Final Agent Rankings

| Rank | Agent | Category |
|------|-------|----------|
| 🥇 | PPO | Policy Gradient RL |
| 🥈 | DQN | Deep Reinforcement Learning |
| 🥉 | Q-Learning | Tabular Reinforcement Learning |
| 4️⃣ | Time-Based | Rule-Based |
| 5️⃣ | Demand-Based | Rule-Based |
| 6️⃣ | Linear Decay | Rule-Based |
| 7️⃣ | Fixed Price | Rule-Based |

---

# 📊 Hyperparameter Optimization

Week 3 introduces automated hyperparameter tuning for PPO.

### Optimized Parameters

- Learning Rate
- Clip Range
- Entropy Coefficient
- Number of Epochs
- Batch Size

The best-performing configuration is automatically selected using average revenue across evaluation episodes.

---

# 🧪 Automated Testing

The project includes comprehensive unit tests covering all critical modules.

| Module | Tests | Status |
|---------|------:|--------|
| Environment | 8 | ✅ |
| Agents | 11 | ✅ |
| PPO | 7 | ✅ |
| **Total** | **26** | **✅ Passing** |

---

# 📈 Evaluation Metrics

Each pricing agent is evaluated using multiple performance indicators.

- Mean Revenue
- Total Revenue
- Products Sold
- Remaining Inventory
- Learning Curve
- Revenue Distribution
- Statistical Comparison
- Policy Performance

---

# 📂 Generated Outputs

Running the project produces outputs such as:

```text
results/

├── training_curves.png
├── qlearning_results.png
├── dqn_results.png
├── ppo_results.png
├── week3_dashboard.png
├── week3_final_summary.png
├── comparison_charts.png
├── hyperparameter_results.json
└── best_config.json
```

---

# 📊 Visualizations

The project automatically generates:

- 📈 Training Curves
- 💰 Revenue Analysis
- 📉 Learning Curves
- 📊 Hyperparameter Comparisons
- 📦 Inventory Trends
- 💹 Price Trajectories
- 🏆 Agent Comparison Dashboard

---

# ✅ Week 3 Complete (26 July 2026)

After three weeks of development, the project successfully includes:

### Major Deliverables

- ✅ Custom Gymnasium Environment
- ✅ Four Rule-Based Pricing Agents
- ✅ Q-Learning Implementation
- ✅ Deep Q Network (DQN)
- ✅ Proximal Policy Optimization (PPO)
- ✅ Hyperparameter Grid Search
- ✅ Performance Benchmarking
- ✅ Statistical Evaluation
- ✅ Dashboard Visualizations
- ✅ Professional Documentation
- ✅ 26 Passing Unit Tests

---

## Week 3 Final Results

| Rank | Agent | Type |
|------|--------|------|
| 🥇 | PPO | Actor-Critic RL |
| 🥈 | DQN | Value-Based RL |
| 🥉 | Q-Learning | Tabular RL |
| 4–7 | Baseline Agents | Heuristic Pricing |

---

## PPO Best Configuration

| Parameter | Value |
|-----------|-------|
| Learning Rate | 0.0005 |
| Clip Range | 0.2 |
| PPO Epochs | 15 |
| Architecture | Actor-Critic |

---

## Week 3 Refactoring Highlights

| Component | Improvement |
|-----------|-------------|
| PPO Utilities | Model Saving & Loading |
| Project Runner | Complete Training Pipeline |
| Performance Optimizer | Benchmarking & Memory Analysis |
| Testing | 26 Unit Tests Passing |

---

## 🚀 Coming Up Next

Part 3 includes:

- Week 4 Roadmap
- Learning Outcomes
- Future Improvements
- Repository Progress
- Contributing Guide
- License
- Author
- Acknowledgements
- Final Repository Summary

# 🚀 Week 4 Roadmap

Week 4 focuses on polishing the project for final submission, strengthening documentation, and demonstrating business value.

## Planned Activities

| Day | Focus Area |
|------|------------|
| Day 1 | Final 1000-Season Simulation |
| Day 2 | Business Dashboard |
| Day 3 | Complete Documentation |
| Day 4 | Submission Preparation |
| Day 5–9 | Project Polish & Final Verification |

---

# 📚 Internship Timeline

## ✅ Week 1 — Reinforcement Learning Foundations

### Topics Covered

- Markov Decision Process (MDP)
- Custom Gymnasium Environment
- Reward Engineering
- Stochastic Demand Modeling
- Baseline Pricing Agents
- Q-Learning
- Policy Extraction
- Hyperparameter Analysis

### Deliverables

- Custom Pricing Environment
- Baseline Agents
- Q-Learning Agent
- Evaluation Pipeline
- Visualizations

---

## ✅ Week 2 — Deep Reinforcement Learning

### Topics Covered

- Deep Q Network (DQN)
- Neural Network Approximation
- Experience Replay
- Target Network
- DQN Training Pipeline
- Performance Comparison

### Deliverables

- DQN Agent
- Training Framework
- Comparison Dashboard
- Analysis Reports

---

## ✅ Week 3 — Policy Gradient Methods

### Topics Covered

- Proximal Policy Optimization (PPO)
- Actor-Critic Architecture
- Rollout Buffer
- Generalized Advantage Estimation (GAE)
- PPO Clipped Objective
- Hyperparameter Optimization
- Statistical Evaluation
- Performance Benchmarking
- Unit Testing

### Deliverables

- PPO Agent
- Hyperparameter Search
- Final Dashboard
- PPO Documentation
- 26 Passing Unit Tests

---

# 🏅 Major Achievements

Throughout the internship, the following milestones were completed successfully.

## Environment

- ✅ Custom Gymnasium Environment
- ✅ Stochastic Demand Simulation
- ✅ Inventory Management
- ✅ Reward Engineering

---

## Pricing Agents

- ✅ Fixed Price Agent
- ✅ Time-Based Pricing
- ✅ Demand-Based Pricing
- ✅ Linear Decay Pricing
- ✅ Q-Learning
- ✅ Deep Q Network (DQN)
- ✅ Proximal Policy Optimization (PPO)

---

## Reinforcement Learning

- ✅ Actor-Critic Architecture
- ✅ Rollout Buffer
- ✅ Generalized Advantage Estimation
- ✅ PPO Clipped Objective
- ✅ Hyperparameter Optimization

---

## Evaluation

- ✅ Statistical Analysis
- ✅ Revenue Benchmarking
- ✅ Learning Curves
- ✅ Dashboard Visualizations
- ✅ Agent Comparison
- ✅ Automated Testing

---

# 📊 Repository Progress

| Component | Progress |
|-----------|----------|
| Environment | ✅ 100% |
| Rule-Based Agents | ✅ 100% |
| Q-Learning | ✅ 100% |
| Deep Q Network | ✅ 100% |
| PPO | ✅ 100% |
| Hyperparameter Optimization | ✅ 100% |
| Performance Analysis | ✅ 100% |
| Visualization | ✅ 100% |
| Unit Testing | ✅ 100% |
| Documentation | 🔄 In Progress |
| Final Submission | ⏳ Pending |

---

# 🎓 Learning Outcomes

This project provided practical experience in several important AI and Machine Learning domains.

## Reinforcement Learning

- Markov Decision Process
- Bellman Equation
- Exploration vs Exploitation
- Value-Based Reinforcement Learning
- Policy-Based Reinforcement Learning

---

## Deep Learning

- Neural Networks
- Experience Replay
- Target Networks
- Actor-Critic Models

---

## PPO Concepts

- Policy Gradient
- Clipped Objective Function
- Rollout Buffer
- Generalized Advantage Estimation
- Entropy Regularization

---

## Software Engineering

- Modular Project Architecture
- Git & GitHub Workflow
- Unit Testing
- Technical Documentation
- Code Refactoring
- Performance Optimization

---

# 📈 Future Improvements

The project can be extended with several advanced Reinforcement Learning techniques.

- Multi-Agent Reinforcement Learning
- Continuous Action Spaces
- SAC (Soft Actor-Critic)
- TD3
- A3C
- Rainbow DQN
- Distributed PPO
- Real-world Business Data Integration
- Web Dashboard Deployment
- Cloud-Based Model Serving

---

# 📷 Project Outputs

The project automatically generates:

- 📈 Training Curves
- 📊 Revenue Dashboards
- 📉 Learning Curves
- 📦 Inventory Trends
- 💹 Price Trajectories
- 📑 Statistical Reports
- 🏆 Agent Comparison Charts
- ⚙️ Hyperparameter Results

---

# 📚 Technologies Used

| Category | Technologies |
|-----------|--------------|
| Programming | Python 3.11 |
| Reinforcement Learning | Gymnasium |
| Deep Learning | PyTorch |
| Data Processing | NumPy, Pandas |
| Visualization | Matplotlib, Seaborn |
| Development | VS Code, Git, GitHub |
| Documentation | Markdown, Jupyter Notebook |

---

# 🤝 Contributing

Contributions are always welcome.

If you'd like to improve this project:

1. Fork this repository.

2. Create a new feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push your branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

# 📝 License

This project was developed as part of the **Infotact DS/ML Technical Internship 2026**.

It is intended for educational purposes and learning reinforcement learning concepts.

---

# 👨‍💻 Author

## Ankur Saini

**B.Tech – Artificial Intelligence**

### GitHub

https://github.com/Ankursaini018

### LinkedIn

> Add your LinkedIn profile URL here.

---

# 🙏 Acknowledgements

Special thanks to:

- Infotact Solutions
- OpenAI
- Gymnasium
- PyTorch
- NumPy Community
- Pandas Community
- Python Software Foundation

for providing excellent open-source tools and learning resources.

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the project

💡 Share suggestions

🐛 Report issues

---

# 📌 Repository Summary

| Feature | Status |
|----------|--------|
| Custom Gymnasium Environment | ✅ |
| Rule-Based Pricing Agents | ✅ |
| Q-Learning | ✅ |
| Deep Q Network | ✅ |
| PPO | ✅ |
| Hyperparameter Optimization | ✅ |
| Performance Benchmarking | ✅ |
| Statistical Evaluation | ✅ |
| Dashboard Visualization | ✅ |
| Unit Testing | ✅ |
| Professional Documentation | ✅ |

---

<div align="center">

# 🌟 RL Dynamic Pricing using Reinforcement Learning

### From Rule-Based Pricing → Q-Learning → Deep Q Network → PPO

An end-to-end Reinforcement Learning project demonstrating intelligent dynamic pricing through progressively advanced RL algorithms.

Built with ❤️ using **Python**, **PyTorch**, and **Gymnasium**.

⭐ **If you found this project helpful, consider giving it a star!**

</div>