# 🚀 RL Dynamic Pricing using Reinforcement Learning

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=for-the-badge&logo=pytorch)
![Gymnasium](https://img.shields.io/badge/Gymnasium-Custom%20Environment-orange?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-blue?style=for-the-badge&logo=numpy)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green?style=for-the-badge)
![Reinforcement%20Learning-Project-success?style=for-the-badge)

</p>

---

# 📌 Project Overview

This project demonstrates an **end-to-end Reinforcement Learning solution for Dynamic Pricing**, developed during the **Infotact DS/ML Internship – Project 2**.

The objective is to train intelligent pricing agents capable of maximizing revenue while adapting to changing demand, inventory levels, and remaining selling days.

Instead of using fixed pricing strategies, multiple Reinforcement Learning algorithms learn optimal pricing policies through continuous interaction with a custom-built environment.

The project progressively evolves from:

- Traditional Rule-Based Pricing
- Tabular Reinforcement Learning
- Deep Reinforcement Learning
- Policy Gradient Reinforcement Learning

Ultimately producing an intelligent pricing system that outperforms heuristic pricing strategies.

---

# 🎯 Problem Statement

Businesses constantly face pricing challenges such as:

- Unsold inventory
- Over-discounting
- Revenue loss
- Demand uncertainty
- Seasonal fluctuations

Static pricing strategies fail to adapt to these changing conditions.

This project solves this problem using Reinforcement Learning agents that dynamically decide the best price at every timestep based on the current state of the environment.

---

# ✨ Key Features

## Environment

- Custom Gymnasium Environment
- Markov Decision Process (MDP)
- Stochastic Customer Demand
- Inventory Management
- Episode-based Simulation
- Reward Engineering

---

## Pricing Agents

### Baseline Agents

- Fixed Price Agent
- Time-Based Pricing Agent
- Demand-Based Pricing Agent
- Linear Decay Pricing Agent

### Reinforcement Learning Agents

- Q-Learning
- Deep Q Network (DQN)
- Proximal Policy Optimization (PPO)

---

## Reinforcement Learning

- Custom State Representation
- Discrete Action Space
- Q-Table Learning
- Experience Replay
- Target Networks
- Actor-Critic Architecture
- PPO Clipped Objective
- Generalized Advantage Estimation (GAE)
- Hyperparameter Optimization

---

## Evaluation

- Revenue Comparison
- Agent Rankings
- Statistical Analysis
- Learning Curves
- Dashboard Visualization
- Hyperparameter Study
- Policy Visualization

---

# 🏆 Internship Progress

| Week | Topic | Status |
|------|--------|--------|
| Week 1 | MDP + Environment + Q-Learning | ✅ |
| Week 2 | Deep Q Network (DQN) | ✅ |
| Week 3 | PPO + Hyperparameter Tuning | ✅ |
| Week 4 | Documentation & Final Submission | 🔄 |

---

# 🧠 Algorithms Implemented

| Algorithm | Type | Status |
|------------|------|--------|
| Fixed Price | Rule-Based | ✅ |
| Time Based | Rule-Based | ✅ |
| Demand Based | Rule-Based | ✅ |
| Linear Decay | Rule-Based | ✅ |
| Q-Learning | Tabular RL | ✅ |
| Deep Q Network | Deep RL | ✅ |
| PPO | Policy Gradient RL | ✅ |

---

# 🏗️ Project Architecture

```
                     Customer Demand
                            │
                            ▼
                Custom Gymnasium Environment
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   Baseline Agents     Q-Learning          Deep RL
                                              │
                                              ▼
                                         DQN Agent
                                              │
                                              ▼
                                         PPO Agent
                                              │
                                              ▼
                                   Policy Evaluation
                                              │
                                              ▼
                              Revenue Comparison Dashboard
```

---

# 📂 Project Structure

```
RL-Dynamic-Pricing/
│
├── data/
│
├── models/
│
├── notebooks/
│   ├── week1/
│   ├── week2/
│   └── week3/
│
├── results/
│
├── src/
│   ├── agents/
│   │   ├── baseline_agents.py
│   │   ├── q_learning_agent.py
│   │   ├── dqn/
│   │   └── ppo/
│   │
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

# ⚙️ Tech Stack

## Programming Language

- Python 3.11

## Reinforcement Learning

- Gymnasium
- NumPy
- Pandas

## Deep Learning

- PyTorch

## Visualization

- Matplotlib
- Seaborn

## Development Tools

- Jupyter Notebook
- VS Code
- Git
- GitHub

---

# 📊 State Space

Each environment state consists of:

| Feature | Description |
|----------|-------------|
| Inventory | Remaining products |
| Days Left | Remaining selling days |

Example:

```python
state = [inventory, days_left]
```

---

# 🎮 Action Space

The agent selects one of six pricing levels.

| Action | Price |
|---------|-------|
| 0 | Lowest Price |
| 1 | Low Price |
| 2 | Medium-Low |
| 3 | Medium |
| 4 | High |
| 5 | Premium |

The chosen action directly influences customer demand and overall revenue.

---

# 🎁 Reward Function

The reward is based on total revenue generated during each interaction.

Higher sales at optimal prices receive larger rewards while poor pricing strategies receive lower cumulative returns.

This enables the agent to gradually learn an optimal pricing policy through trial and error.

---

# 🚀 Project Goals

- Build a realistic Dynamic Pricing simulator
- Compare heuristic and RL pricing strategies
- Implement progressively advanced RL algorithms
- Evaluate policy performance using statistical metrics
- Demonstrate the effectiveness of Deep Reinforcement Learning in pricing optimization
- Produce a production-quality internship project

---

# 📌 Current Status

| Module | Status |
|----------|--------|
| Environment | ✅ Complete |
| Baseline Agents | ✅ Complete |
| Q-Learning | ✅ Complete |
| DQN | ✅ Complete |
| PPO | ✅ Complete |
| Hyperparameter Tuning | ✅ Complete |
| Statistical Analysis | ✅ Complete |
| Unit Testing | ✅ Complete |
| Documentation | 🔄 In Progress |

---

# ➡️ Next Section

The next part covers:

- Installation
- How to Run
- Training
- Testing
- Results
- Performance Comparison
- Week-wise Progress
- Dashboards
- Agent Rankings

---

# 💻 Installation

## Clone the Repository

```bash
git clone https://github.com/Ankursaini018/RL-Dynamic-Pricing.git
cd RL-Dynamic-Pricing
```

---

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

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

---

## Week 1

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

## Week 2

### Train DQN

```bash
python src/training/dqn_trainer.py
```

### Compare DQN with Q-Learning

```bash
python src/analysis/dqn_vs_qlearning.py
```

### Generate Dashboard

```bash
python src/visualization/price_dashboard.py
```

---

## Week 3

### Train PPO

```bash
python src/training/ppo_trainer.py
```

### Hyperparameter Tuning

```bash
python src/training/ppo_hypertuner.py
```

### Combined Tuning

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

# 📒 Jupyter Notebooks

The internship is organized using notebooks for each learning milestone.

| Week | Notebook |
|-------|----------|
| Week 1 | MDP + Q-Learning |
| Week 2 | Deep Q Network |
| Week 3 | PPO + Hyperparameter Tuning |

---

# 🤖 Reinforcement Learning Pipeline

```
Environment

↓

State Observation

↓

Agent chooses Price

↓

Environment executes Action

↓

Reward Received

↓

Policy Update

↓

Repeat
```

---

# 🧠 Algorithms

---

## 1️⃣ Fixed Price Agent

Always sells at a fixed price.

### Advantages

- Extremely simple
- Fast execution

### Limitations

- No learning
- No adaptation

---

## 2️⃣ Time-Based Pricing

Price decreases as selling deadline approaches.

Suitable for:

- Airline tickets
- Hotel bookings
- Perishable products

---

## 3️⃣ Demand-Based Pricing

Prices change according to market demand.

Advantages

- Reactive strategy
- Easy implementation

Limitations

- No long-term optimization

---

## 4️⃣ Linear Decay Pricing

Gradually reduces prices throughout the selling period.

Commonly used in retail inventory clearance.

---

# 🧠 Q-Learning

Q-Learning is a model-free reinforcement learning algorithm that learns an optimal action-value function.

### Features

- Tabular learning
- ε-Greedy exploration
- Bellman Equation
- Q-table updates

---

# 🧠 Deep Q Network (DQN)

DQN replaces the Q-table with a neural network.

Major improvements include:

- Deep Neural Network
- Experience Replay
- Target Network
- Stable training
- Better scalability

---

# 🧠 Proximal Policy Optimization (PPO)

PPO is a policy-gradient reinforcement learning algorithm developed by OpenAI.

Key Components:

- Actor-Critic Network
- Clipped Objective
- GAE
- Entropy Regularization
- On-Policy Learning

---

# 🏆 Agent Performance

| Rank | Agent |
|------|--------|
| 🥇 | PPO |
| 🥈 | DQN |
| 🥉 | Q-Learning |
| 4️⃣ | Time-Based |
| 5️⃣ | Demand-Based |
| 6️⃣ | Linear Decay |
| 7️⃣ | Fixed Price |

---

# 📈 Model Evolution

```
Rule-Based Pricing

↓

Q-Learning

↓

Deep Q Network

↓

Proximal Policy Optimization
```

---

# 📊 Hyperparameter Optimization

Week 3 introduced automated hyperparameter tuning.

Optimized Parameters

- Learning Rate
- Clip Range
- Entropy Coefficient
- Number of Epochs
- Batch Size

The best configuration was automatically selected using revenue performance.

---

# 🧪 Testing

The project includes automated tests covering all major components.

| Module | Tests |
|---------|-------|
| Environment | 8 |
| Baseline + Q-Learning | 11 |
| PPO | 7 |

### Total Tests

```
26 Tests Passing
```

---

# 📈 Evaluation Metrics

Each agent is evaluated using:

- Mean Revenue
- Total Revenue
- Products Sold
- Remaining Inventory
- Learning Curve
- Revenue Distribution
- Statistical Significance

---

# 📊 Generated Outputs

Running the project produces:

```
results/

├── training_curves.png
├── qlearning_results.png
├── dqn_results.png
├── ppo_results.png
├── week3_dashboard.png
├── week3_final_dashboard.png
├── comparison_charts.png
├── hyperparameter_results.json
└── best_config.json
```

---

# 📉 Visualizations

The project automatically generates:

- Revenue Curves
- Training Curves
- Dashboard
- Price Distribution
- Inventory Trends
- Agent Comparison Charts
- Hyperparameter Graphs

---

# 📌 Current Repository Status

| Component | Status |
|-----------|--------|
| Environment | ✅ |
| Baselines | ✅ |
| Q-Learning | ✅ |
| DQN | ✅ |
| PPO | ✅ |
| Unit Tests | ✅ |
| Analysis | ✅ |
| Visualization | ✅ |
| Documentation | 🔄 |

---

# ➡️ Next Section

Part 3 includes:

- Week-wise Internship Timeline
- Achievements
- Learning Outcomes
- Future Improvements
- Roadmap
- Contributing
- License
- Author
- GitHub Stats

---

# 📅 Internship Timeline

## ✅ Week 1 — Reinforcement Learning Foundations

### Topics Covered

- Markov Decision Process (MDP)
- Custom Gymnasium Environment
- Reward Engineering
- Stochastic Demand Simulation
- Baseline Pricing Agents
- Q-Learning
- Policy Extraction
- Hyperparameter Analysis

### Deliverables

- Custom Environment
- Q-Learning Agent
- Evaluation Pipeline
- Visualizations

---

## ✅ Week 2 — Deep Reinforcement Learning

### Topics Covered

- Deep Q Network (DQN)
- Experience Replay
- Target Network
- Neural Network Approximation
- DQN Training
- Performance Analysis

### Deliverables

- DQN Agent
- Training Pipeline
- Comparison Dashboard
- Performance Reports

---

## ✅ Week 3 — Policy Gradient Methods

### Topics Covered

- PPO (Proximal Policy Optimization)
- Actor-Critic Architecture
- Rollout Buffer
- GAE (Generalized Advantage Estimation)
- PPO Clipped Objective
- Hyperparameter Tuning
- Statistical Analysis
- Unit Testing

### Deliverables

- PPO Agent
- Hyperparameter Tuning
- Week 3 Dashboard
- Final Agent Comparison
- PPO Documentation
- 26 Unit Tests

---

# 🏅 Final Project Achievements

✅ Custom Gymnasium Environment

✅ 7 Intelligent Pricing Agents

✅ Q-Learning Implementation

✅ Deep Q Network

✅ PPO Implementation

✅ Hyperparameter Optimization

✅ Statistical Evaluation

✅ Dashboard Visualizations

✅ Automated Testing

✅ Professional Documentation

---

# 📊 Final Agent Rankings

| Rank | Agent | Category |
|------|---------|----------|
| 🥇 | PPO | Policy Gradient |
| 🥈 | DQN | Deep Reinforcement Learning |
| 🥉 | Q-Learning | Tabular Reinforcement Learning |
| 4️⃣ | Time-Based | Rule-Based |
| 5️⃣ | Demand-Based | Rule-Based |
| 6️⃣ | Linear Decay | Rule-Based |
| 7️⃣ | Fixed Price | Rule-Based |

---

# 🎯 Learning Outcomes

Throughout this project I gained hands-on experience with:

## Reinforcement Learning

- Markov Decision Process
- Bellman Equation
- Exploration vs Exploitation
- Value-Based RL
- Policy-Based RL

---

## Deep Learning

- Neural Networks
- Experience Replay
- Target Networks
- Actor-Critic Models

---

## PPO Concepts

- Policy Gradient
- Clipped Objective
- Rollout Buffer
- Generalized Advantage Estimation
- Entropy Regularization

---

## Software Engineering

- Project Structuring
- Git & GitHub Workflow
- Unit Testing
- Documentation
- Modular Development

---

# 📈 Repository Progress

| Module | Progress |
|----------|----------|
| Environment | ✅ 100% |
| Baseline Agents | ✅ 100% |
| Q-Learning | ✅ 100% |
| Deep Q Network | ✅ 100% |
| PPO | ✅ 100% |
| Hyperparameter Tuning | ✅ 100% |
| Testing | ✅ 100% |
| Visualization | ✅ 100% |
| Documentation | 🔄 90% |
| Final Submission | ⏳ Pending |

---

## Week 3 Day 6 — Refactoring ✅

### Code Quality Improvements

| Item | Details |
|---|---|
| PPO Utilities | Model save/load + monitor |
| Project Runner | Complete pipeline with PPO |
| Performance Optimizer | Benchmarking + memory |
| Unit Tests | 26 total all passing |

### How to Run Complete Pipeline

```bash
# Quick test
cd src
python project_runner.py --quick

# Full pipeline
python project_runner.py

# Run all tests
python tests/test_ppo.py
python tests/test_agents.py
python tests/test_environment.py
```

### Tomorrow → Week 3 Final Wrap



# 🚀 Week 4 Roadmap

## Planned Tasks

- Final 1000-Season Simulation
- Performance Optimization
- Complete Documentation
- Final Dashboard Improvements
- README Refinement
- Internship Submission

---

# 📷 Project Outputs

The project generates multiple outputs including:

- Training Curves
- Revenue Analysis
- Policy Comparison
- Hyperparameter Results
- Dashboard Visualizations
- Agent Rankings
- Statistical Reports

---

# 📚 Key Technologies

| Category | Technologies |
|-----------|--------------|
| Programming | Python |
| RL | Gymnasium |
| Deep Learning | PyTorch |
| Data Analysis | NumPy, Pandas |
| Visualization | Matplotlib |
| Development | Git, GitHub, VS Code |
| Documentation | Markdown, Jupyter Notebook |

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push your branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📝 License

This project was developed as part of the **Infotact DS/ML Internship – Project 2**.

It is intended for educational and learning purposes.

---

# 👨‍💻 Author

**Ankur Saini**

B.Tech Artificial Intelligence

GitHub

https://github.com/Ankursaini018

LinkedIn

(Add your LinkedIn profile link here)

---

# ⭐ Support

If you found this project useful:

⭐ Star this repository

🍴 Fork the repository

📝 Share your feedback

---

# 🙏 Acknowledgements

Special thanks to:

- Infotact Solutions
- OpenAI
- Gymnasium
- PyTorch Community
- Python Community

for providing excellent learning resources and open-source tools.

---

# 📌 Repository Summary

| Feature | Status |
|-----------|--------|
| Custom Environment | ✅ |
| Baseline Agents | ✅ |
| Q-Learning | ✅ |
| Deep Q Network | ✅ |
| PPO | ✅ |
| Hyperparameter Tuning | ✅ |
| Statistical Analysis | ✅ |
| Unit Testing | ✅ |
| Documentation | ✅ |

---

<div align="center">

## 🌟 Reinforcement Learning for Intelligent Dynamic Pricing 🌟

**From Rule-Based Pricing → Q-Learning → DQN → PPO**

Built with ❤️ using Python, PyTorch and Reinforcement Learning.

⭐ If you like this project, don't forget to star the repository!

</div>