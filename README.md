# 🎯 RL Dynamic Pricing using Reinforcement Learning

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=for-the-badge&logo=pytorch)
![Gymnasium](https://img.shields.io/badge/Gymnasium-RL%20Environment-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Week%202%20Completed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)
![Internship](https://img.shields.io/badge/Infotact-Technical%20Internship-purple?style=for-the-badge)

### **AI-Powered Dynamic Pricing System using Q-Learning & Deep Q Networks (DQN)**

*A Reinforcement Learning approach for maximizing revenue through intelligent pricing decisions under uncertain customer demand.*

</div>

---

# 📚 Table of Contents

- [📖 Project Overview](#-project-overview)
- [🎯 Problem Statement](#-problem-statement)
- [✨ Key Features](#-key-features)
- [🏗️ MDP Formulation](#️-mdp-formulation)
- [🤖 Reinforcement Learning Pipeline](#-reinforcement-learning-pipeline)
- [🧠 Agents Implemented](#-agents-implemented)
- [🏛️ Project Architecture](#️-project-architecture)
- [📂 Repository Structure](#-repository-structure)
- [🛠️ Technologies Used](#️-technologies-used)
- [✅ Week 1 Achievements](#-week-1-achievements)
- [🚀 Week 2 Achievements](#-week-2-achievements)
- [🧠 Deep Q-Network Architecture](#-deep-q-network-dqn-architecture)
- [⚙️ Training Configuration](#️-training-configuration)
- [📈 Results & Analysis](#-results--analysis)
- [💻 Installation Guide](#-installation-guide)
- [▶️ Running the Project](#️-running-the-project)
- [🧪 Running Tests](#-running-tests)
- [📊 Project Workflow](#-project-workflow)
- [🛣️ Roadmap](#️-roadmap)
- [🔮 Future Improvements](#-future-improvements)
- [🙏 Acknowledgements](#-acknowledgements)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

---

# 📖 Project Overview

Dynamic Pricing is one of the most important optimization problems in industries such as:

- ✈️ Airlines
- 🎟️ Event Ticketing
- 🏨 Hotel Booking
- 🚕 Ride Sharing
- 🛒 E-commerce
- 📦 Inventory Management

Traditional pricing strategies rely on manually designed rules and heuristics.

This project applies **Reinforcement Learning (RL)** to automatically discover an optimal pricing strategy by allowing an intelligent agent to interact with a simulated business environment.

Instead of hardcoding pricing decisions, the RL agent learns **which price to choose** based on:

- Current inventory
- Remaining selling days
- Customer demand
- Expected future rewards

The objective is to **maximize total revenue** while minimizing losses due to unsold inventory.

---

# 🎯 Problem Statement

The business must sell a **limited inventory of tickets** before a fixed deadline.

Challenges include:

- Limited inventory
- Finite selling horizon
- Stochastic customer demand
- Multiple pricing choices
- Balancing immediate vs future revenue

The agent must learn an optimal pricing policy that maximizes long-term revenue under uncertainty.

---

# ✨ Key Features

## Environment

- ✅ Custom Gymnasium Environment
- ✅ Markov Decision Process (MDP)
- ✅ Stochastic Demand Function
- ✅ Reward Engineering
- ✅ Configurable Inventory
- ✅ Configurable Time Horizon

---

## Baseline Pricing Agents

- ✅ Fixed Price Agent
- ✅ Random Agent
- ✅ Time-Based Pricing Agent
- ✅ Demand-Based Pricing Agent
- ✅ Linear Decay Pricing Agent

---

## Reinforcement Learning

- ✅ Tabular Q-Learning
- ✅ Deep Q-Network (DQN)
- ✅ Experience Replay
- ✅ Target Network
- ✅ Epsilon-Greedy Exploration
- ✅ Neural Network Function Approximation

---

## Evaluation

- ✅ 1000 Season Simulation
- ✅ Revenue Comparison
- ✅ Policy Analysis
- ✅ Statistical Validation
- ✅ Learning Curves
- ✅ Price Trajectory Visualization
- ✅ Business Dashboard

---

# 🏗️ MDP Formulation

| Component | Description |
|------------|-------------|
| **State** | (Inventory Remaining, Days Remaining) |
| **Action** | Choose one of 6 discrete ticket prices |
| **Reward** | Revenue earned from ticket sales |
| **Penalty** | Unsold inventory penalty at episode end |
| **Episode End** | Inventory sold out OR final selling day |
| **Objective** | Maximize cumulative revenue |

---

## State Space

| Variable | Range |
|----------|-------|
| Inventory | 0 → 50 |
| Days Left | 0 → 30 |

Total State Space:

```
51 × 31 = 1,581 States
```

---

## Action Space

| Action | Ticket Price |
|---------|-------------:|
| 0 | $50 |
| 1 | $100 |
| 2 | $150 |
| 3 | $200 |
| 4 | $250 |
| 5 | $300 |

---

## Reward Function

Positive reward:

```
Revenue = Price × Tickets Sold
```

Penalty:

```
Unsold Inventory × Penalty Cost
```

Goal:

```
Maximize Total Episode Revenue
```

---

# 🤖 Reinforcement Learning Pipeline

```
                Environment
                      │
                      ▼
          Current State (s)
                      │
                      ▼
            RL Agent selects action
                      │
                      ▼
             Ticket Price Selected
                      │
                      ▼
        Environment Simulates Demand
                      │
                      ▼
      Reward + Next State Returned
                      │
                      ▼
           Agent Updates Policy
                      │
                      ▼
            Repeat Until Episode Ends
```

---

# 🧠 Agents Implemented

| Agent | Category | Status |
|--------|----------|--------|
| Fixed Price | Baseline | ✅ |
| Random | Baseline | ✅ |
| Time-Based Pricing | Baseline | ✅ |
| Demand-Based Pricing | Baseline | ✅ |
| Linear Decay Pricing | Baseline | ✅ |
| Q-Learning | Reinforcement Learning | ✅ |
| Deep Q Network (DQN) | Deep Reinforcement Learning | ✅ |
| PPO (Planned) | Advanced RL | 🚧 |

---

# 🏛️ Project Architecture

```
                    RL Dynamic Pricing

                  ┌────────────────────┐
                  │ Business Environment│
                  └─────────┬──────────┘
                            │
                            ▼
                 Dynamic Pricing Environment
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
   Baseline Agents                     RL Agents
                                             │
                    ┌────────────────────────┴───────────────┐
                    ▼                                        ▼
              Q-Learning                              Deep Q Network
                    │                                        │
                    └────────────────────────┬───────────────┘
                                             ▼
                                 Revenue Optimization
                                             │
                                             ▼
                              Performance Evaluation
                                             │
                                             ▼
                                 Business Insights
```

---

# 📂 Repository Structure

```text
RL-Dynamic-Pricing/
│
├── notebooks/
│   ├── week1/
│   └── week2/
│
├── src/
│   ├── agents/
│   │   ├── baseline_agents.py
│   │   ├── q_learning_agent.py
│   │   ├── agent_registry.py
│   │   └── dqn/
│   │       ├── dqn_network.py
│   │       ├── dqn_agent.py
│   │       ├── replay_buffer.py
│   │       └── dqn_utils.py
│   │
│   ├── environment/
│   ├── training/
│   ├── simulation/
│   ├── visualization/
│   ├── analysis/
│   ├── utils/
│   ├── tests/
│   ├── project_runner.py
│   └── config.py
│
├── results/
├── models/
├── data/
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

| Category | Technologies |
|-----------|--------------|
| Programming Language | Python |
| Deep Learning | PyTorch |
| Reinforcement Learning | Gymnasium |
| Data Processing | NumPy, Pandas |
| Visualization | Matplotlib |
| Statistics | SciPy |
| Notebook | Jupyter Notebook |
| Version Control | Git & GitHub |
| IDE | VS Code |

---

# ✅ Week 1 Achievements

Week 1 focused on building the foundation of the Reinforcement Learning project by designing the environment, implementing baseline agents, and developing the first learning algorithm.

---

## 📌 Deliverables

| Module | Status |
|---------|--------|
| Markov Decision Process Design | ✅ |
| Custom Gymnasium Environment | ✅ |
| Stochastic Demand Function | ✅ |
| Reward Engineering | ✅ |
| State & Action Space Definition | ✅ |
| Environment Testing | ✅ |
| Baseline Pricing Agents | ✅ |
| Fixed Price Agent | ✅ |
| Random Pricing Agent | ✅ |
| Time-Based Pricing Agent | ✅ |
| Demand-Based Pricing Agent | ✅ |
| Linear Decay Pricing Agent | ✅ |
| Q-Learning Algorithm | ✅ |
| Q-Table Training | ✅ |
| Policy Extraction | ✅ |
| Hyperparameter Analysis | ✅ |
| Results Consolidation | ✅ |

---

## 📊 Week 1 Learning Outcomes

During Week 1, the following Reinforcement Learning concepts were implemented from scratch:

- Markov Decision Process (MDP)
- Bellman Equation
- Q-Table Learning
- Epsilon-Greedy Exploration
- Reward Engineering
- Policy Evaluation
- Dynamic Pricing Environment
- Environment Simulation

---

# 🚀 Week 2 Achievements

Week 2 extended the project from classical Reinforcement Learning to **Deep Reinforcement Learning** using **Deep Q Networks (DQN)**.

The objective was to replace the tabular Q-Table with a Neural Network capable of approximating Q-values.

---

## 📌 Deliverables

| Module | Status |
|---------|--------|
| Deep Q Network | ✅ |
| Neural Network Implementation | ✅ |
| Experience Replay Buffer | ✅ |
| Target Network | ✅ |
| Epsilon Decay Strategy | ✅ |
| Gradient Clipping | ✅ |
| DQN Training Pipeline | ✅ |
| Model Saving & Loading | ✅ |
| 1000 Season Simulation | ✅ |
| Statistical Evaluation | ✅ |
| Revenue Comparison | ✅ |
| Price Trajectory Dashboard | ✅ |
| Deadline Discounting Analysis | ✅ |
| Scarcity Pricing Analysis | ✅ |
| Project Refactoring | ✅ |
| Mid Review Documentation | ✅ |

---

## 📈 Week 2 Highlights

- 🧠 Deep Q-Network implemented using PyTorch
- 🎯 Neural Network replaces traditional Q-Table
- 🔄 Experience Replay stabilizes learning
- 🎯 Target Network reduces oscillations
- 📉 Adaptive Epsilon Decay balances exploration and exploitation
- 📊 Comprehensive evaluation across 1000 simulated seasons
- 📈 Interactive dashboards for policy visualization

---

# 🧠 Deep Q-Network (DQN) Architecture

The DQN agent approximates the optimal action-value function using a fully connected neural network.

```
Input Layer
──────────────
Inventory Remaining
Days Remaining

        │

        ▼

Fully Connected Layer
128 Neurons
ReLU

        │

        ▼

Fully Connected Layer
64 Neurons
ReLU

        │

        ▼

Output Layer
6 Q-values
(One for each price level)
```

---

## Network Summary

| Layer | Configuration |
|--------|--------------|
| Input | 2 Features |
| Hidden Layer 1 | 128 Neurons + ReLU |
| Hidden Layer 2 | 64 Neurons + ReLU |
| Output | 6 Q-values |
| Framework | PyTorch |

Approximate Parameters:

```
~10,000 Trainable Parameters
```

---

# ⚙️ Training Configuration

## Q-Learning

| Parameter | Value |
|-----------|-------|
| Learning Rate | 0.1 |
| Discount Factor | 0.99 |
| Initial Epsilon | 1.0 |
| Final Epsilon | 0.01 |
| Episodes | 5000 |

---

## Deep Q Network

| Parameter | Value |
|-----------|-------|
| Episodes | 2000 |
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Batch Size | 64 |
| Replay Buffer | 10,000 |
| Target Update | Every 10 Episodes |
| Discount Factor | 0.99 |
| Initial Epsilon | 1.0 |
| Final Epsilon | 0.01 |

---

# 📈 Results & Analysis

After training, all pricing strategies were evaluated over **1000 simulated seasons**.

The DQN consistently achieved the highest revenue among all implemented agents.

---

## 🏆 Overall Performance

| Rank | Agent | Category |
|------|---------|-----------|
| 🥇 | Deep Q Network | Deep Reinforcement Learning |
| 🥈 | Q-Learning | Reinforcement Learning |
| 🥉 | Time-Based Pricing | Baseline |
| 4️⃣ | Demand-Based Pricing | Baseline |
| 5️⃣ | Linear Decay Pricing | Baseline |
| 6️⃣ | Fixed Price | Baseline |
| 7️⃣ | Random Pricing | Baseline |

---

## 📊 Business Behaviors Learned

The trained DQN automatically discovered several intelligent pricing strategies without any manually designed rules.

### ✅ Deadline Discounting

As the selling deadline approaches:

- Prices decrease automatically
- Unsold inventory risk is minimized
- Revenue remains optimized

---

### ✅ Scarcity Pricing

When inventory becomes scarce:

- Prices increase naturally
- Higher profit per ticket
- Better inventory utilization

---

### ✅ Revenue Maximization

Compared with handcrafted pricing strategies:

- Higher cumulative revenue
- Better long-term decisions
- Improved inventory management

---

# 📊 Evaluation Metrics

The project evaluates agent performance using:

| Metric | Purpose |
|---------|----------|
| Total Revenue | Business Performance |
| Average Revenue | Policy Quality |
| Tickets Sold | Inventory Efficiency |
| Remaining Inventory | Waste Analysis |
| Reward Curve | Learning Progress |
| Epsilon Curve | Exploration Analysis |
| Statistical Significance | Agent Comparison |

---

# 📸 Project Outputs

The project automatically generates various visualizations and reports.

```
results/

├── training_curve.png
├── revenue_comparison.png
├── policy_heatmap.png
├── price_trajectory.png
├── week2_final_dashboard.png
├── statistical_analysis.csv
├── business_report.csv
└── simulation_results.csv
```

---

# 📈 Example Visualizations

The project includes dashboards for:

- 📉 DQN Training Curve
- 💰 Revenue Comparison
- 🎟️ Inventory vs Revenue
- 📊 Price Trajectories
- 📈 Epsilon Decay
- 📉 Reward Distribution
- 🧠 Learned Pricing Policy
- 📊 Week 2 Final Dashboard

---

# 🎯 Key Achievements

✅ Custom Reinforcement Learning Environment

✅ 5 Baseline Pricing Strategies

✅ Tabular Q-Learning

✅ Deep Q Network

✅ Experience Replay

✅ Target Network

✅ 1000 Season Simulation

✅ Statistical Validation

✅ Business Dashboard

✅ Intelligent Dynamic Pricing Policy

---

# 💻 Installation Guide

## Prerequisites

Before running this project, ensure the following software is installed:

- Python 3.10 or higher
- Git
- pip
- Jupyter Notebook (Optional)

---

## Clone the Repository

```bash
git clone https://github.com/your-username/RL-Dynamic-Pricing.git
```

```bash
cd RL-Dynamic-Pricing
```

---

## Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

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

## Quick Pipeline

Runs a lightweight version of the project for quick verification.

```bash
cd src

python project_runner.py --quick
```

---

## Complete Pipeline

Runs the full training and evaluation pipeline.

```bash
python project_runner.py
```

---

## Running Individual Modules

### Train Q-Learning

```bash
python training/q_learning_trainer.py
```

---

### Train Deep Q Network

```bash
python training/dqn_trainer.py
```

---

### Run Business Simulation

```bash
python simulation/season_simulator.py
```

---

### Generate Business Report

```bash
python simulation/business_report.py
```

---

### Analyze Week 2 Results

```bash
python analysis/week2_analyzer.py
```

---

### Launch Notebooks

```bash
jupyter notebook
```

Open:

```
notebooks/
```

and execute the notebooks for Week 1 or Week 2.

---

# 🧪 Running Tests

Run the complete testing suite to verify the implementation.

## Environment Tests

```bash
python tests/test_environment.py
```

---

## Agent Tests

```bash
python tests/test_agents.py
```

---

## Expected Result

```
All tests passed successfully.
```

---

# 📊 Project Workflow

```
                  Start
                    │
                    ▼
         Initialize Environment
                    │
                    ▼
          Select Pricing Agent
                    │
                    ▼
        Choose Ticket Price Action
                    │
                    ▼
         Simulate Customer Demand
                    │
                    ▼
         Receive Reward & Next State
                    │
                    ▼
        Update Agent (Q-Learning/DQN)
                    │
                    ▼
          Episode Termination?
               │          │
             No           Yes
               │           │
               ▼           ▼
         Continue       Evaluate Policy
                            │
                            ▼
                 Revenue Comparison
                            │
                            ▼
                    Business Insights
```

---

# 📌 Repository Progress

| Milestone | Status |
|------------|--------|
| Environment Design | ✅ Completed |
| MDP Formulation | ✅ Completed |
| Baseline Agents | ✅ Completed |
| Q-Learning | ✅ Completed |
| Q-Table Analysis | ✅ Completed |
| Hyperparameter Analysis | ✅ Completed |
| Deep Q Network | ✅ Completed |
| Experience Replay | ✅ Completed |
| Target Network | ✅ Completed |
| Model Evaluation | ✅ Completed |
| Statistical Analysis | ✅ Completed |
| Business Dashboard | ✅ Completed |
| PPO Implementation | 🚧 Planned |
| Hyperparameter Optimization | 🚧 Planned |
| Final Project Report | 🚧 Planned |

---

# 🛣️ Development Roadmap

## ✅ Week 1

- MDP Formulation
- Environment Design
- Demand Simulation
- Baseline Agents
- Q-Learning
- Policy Analysis

---

## ✅ Week 2

- Deep Q Network
- Experience Replay
- Target Network
- DQN Evaluation
- Statistical Validation
- Mid Review Preparation

---

## 🚧 Week 3

- PPO Agent
- Hyperparameter Optimization
- Comparative Analysis
- Performance Improvements

---

## 🚧 Week 4

- Final Documentation
- Model Optimization
- Project Cleanup
- Final Internship Submission

---

# 🔮 Future Improvements

This project can be extended in several directions:

- PPO (Proximal Policy Optimization)
- Double DQN
- Dueling DQN
- Rainbow DQN
- Soft Actor-Critic (SAC)
- Continuous Action Space
- Multi-Agent Pricing
- Airline Revenue Management
- Hotel Dynamic Pricing
- Real-World Pricing Datasets
- Deployment as a Web Application
- Interactive Dashboard using Streamlit

---

# 📖 Learning Outcomes

This project demonstrates practical implementation of:

- Reinforcement Learning
- Deep Reinforcement Learning
- Markov Decision Processes
- Q-Learning
- Bellman Equation
- Deep Q Networks
- Experience Replay
- Target Networks
- Function Approximation
- Exploration vs Exploitation
- Neural Networks with PyTorch
- Business Simulation
- Revenue Optimization
- Dynamic Pricing

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to improve this project:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

Please ensure that all tests pass before submitting changes.

---

# 🙏 Acknowledgements

This project was developed as part of the:

**Infotact Solutions – Data Science & Machine Learning Technical Internship (2026)**

Special thanks to:

- Infotact Solutions
- OpenAI Gymnasium
- PyTorch
- NumPy
- Pandas
- Matplotlib
- SciPy
- Open Source Community

---

# 👨‍💻 Author

## Ankur Saini

**Artificial Intelligence Undergraduate**

Passionate about:

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Reinforcement Learning
- Data Science
- Python Development

### Connect with me

- GitHub: https://github.com/Ankursaini018
- LinkedIn: www.linkedin.com/in/ankur-saini-596173374

---

# 📄 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project for educational and research purposes.

---

# ⭐ Support

If you found this project helpful:

⭐ Star this repository

🍴 Fork the repository

📢 Share it with others

Your support motivates further development and improvements.

---

<div align="center">

## Thank You for Visiting!

**RL Dynamic Pricing using Reinforcement Learning**

*Building intelligent pricing strategies through AI and Deep Reinforcement Learning.*

⭐ **Don't forget to Star the Repository!** ⭐

</div>