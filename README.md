# 🎯 RL Dynamic Pricing using Reinforcement Learning

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=for-the-badge&logo=pytorch)
![Gymnasium](https://img.shields.io/badge/Gymnasium-RL%20Environment-green?style=for-the-badge)
![Stable-Baselines3](https://img.shields.io/badge/Stable--Baselines3-PPO-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Week%203%20In%20Progress-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)
![Internship](https://img.shields.io/badge/Infotact-Technical%20Internship-purple?style=for-the-badge)

# AI-Powered Dynamic Pricing using Reinforcement Learning

### **Building Intelligent Pricing Strategies with Q-Learning, Deep Q Networks (DQN), and Proximal Policy Optimization (PPO)**

*An end-to-end Reinforcement Learning project that learns optimal pricing policies for maximizing revenue under uncertain customer demand.*

</div>

---

# 📚 Table of Contents

- [📖 Introduction](#-introduction)
- [🎯 Business Problem](#-business-problem)
- [✨ Project Highlights](#-project-highlights)
- [🛠️ Technology Stack](#️-technology-stack)
- [🎓 Learning Objectives](#-learning-objectives)
- [📊 Project Scope](#-project-scope)
- [📌 Key Features](#-key-features)

---

# 📖 Introduction

Pricing is one of the most influential factors affecting business profitability. Industries such as airlines, hotels, ride-sharing platforms, ticket booking services, and e-commerce companies continuously adjust prices in response to changing market conditions.

Traditional pricing systems usually depend on manually designed rules or statistical forecasting methods. Although these approaches perform reasonably well in predictable environments, they often struggle when customer demand changes dynamically.

This project demonstrates how **Reinforcement Learning (RL)** can be used to automate pricing decisions by allowing an intelligent software agent to interact with a simulated marketplace.

Instead of relying on predefined business rules, the agent continuously learns from its own experience by observing the consequences of different pricing decisions. Over time, it discovers pricing strategies that maximize long-term revenue while adapting to inventory constraints and uncertain customer demand.

The project progresses through multiple Reinforcement Learning approaches:

- Classical Q-Learning
- Deep Q Networks (DQN)
- Proximal Policy Optimization (PPO)

Each stage introduces increasingly advanced techniques for learning optimal pricing policies.

---

# 🎯 Business Problem

Consider a company selling a limited number of products or tickets before a fixed deadline.

Every day, the company must decide:

> **"What price should we charge today to maximize overall revenue?"**

Charging a high price may increase profit per sale but reduce demand.

Charging a low price may increase sales volume but decrease profit.

The objective is to find the optimal balance between these competing goals throughout the selling period.

The Reinforcement Learning agent must continuously answer questions such as:

- Should prices be increased when inventory becomes scarce?
- Should prices decrease as the deadline approaches?
- How should pricing react to uncertain customer demand?
- Which pricing strategy produces the highest long-term revenue?

Rather than programming these decisions manually, the RL agent learns them automatically through repeated interaction with the environment.

---

# ✨ Project Highlights

## 🚀 Reinforcement Learning Journey

This repository demonstrates the progression from basic Reinforcement Learning techniques to modern Deep Reinforcement Learning algorithms.

### ✅ Week 1 — Foundations

- Custom Gymnasium Environment
- Markov Decision Process (MDP)
- Reward Engineering
- Baseline Pricing Agents
- Tabular Q-Learning
- Policy Analysis

---

### ✅ Week 2 — Deep Reinforcement Learning

- Deep Q Network (DQN)
- Neural Network Function Approximation
- Experience Replay
- Target Network
- Model Evaluation
- Statistical Analysis
- Business Dashboards

---

### 🔄 Week 3 — Advanced Reinforcement Learning

- PPO Fundamentals
- Actor-Critic Architecture
- Rollout Buffer
- Generalized Advantage Estimation (GAE)
- PPO Agent Implementation
- Policy Optimization
- Comparative Evaluation (PPO vs DQN)

---

### 🚧 Week 4 — Final Project

- Large Scale Evaluation
- Performance Benchmarking
- Hyperparameter Optimization
- Documentation
- Final Reports
- Internship Submission

---

# 🛠️ Technology Stack

| Category | Tools & Frameworks |
|------------|-------------------|
| Programming Language | Python 3.10+ |
| Deep Learning | PyTorch |
| Reinforcement Learning | Gymnasium |
| Advanced RL | Stable-Baselines3 |
| Numerical Computing | NumPy |
| Data Processing | Pandas |
| Visualization | Matplotlib |
| Statistics | SciPy |
| Development Environment | VS Code |
| Interactive Analysis | Jupyter Notebook |
| Version Control | Git & GitHub |

---

# 🎓 Learning Objectives

This project focuses on developing practical understanding of modern Reinforcement Learning concepts.

Throughout the internship, the following topics are implemented from scratch:

- Markov Decision Processes (MDP)
- Environment Design
- Reward Engineering
- Exploration vs Exploitation
- Q-Learning
- Deep Q Networks
- Neural Network Approximation
- Experience Replay
- Target Networks
- Policy Gradient Methods
- Actor-Critic Models
- PPO Optimization
- Revenue Optimization
- Business Simulation

The goal is not only to build working RL agents but also to understand the reasoning behind each algorithm and compare their performance in a realistic pricing scenario.

---

# 📊 Project Scope

The project simulates a real-world revenue management system where an intelligent pricing agent interacts with a business environment over multiple selling periods.

During each episode, the agent:

1. Observes the current business state.
2. Selects a ticket price.
3. Receives customer demand generated by the environment.
4. Earns revenue based on successful sales.
5. Updates its pricing policy using Reinforcement Learning.
6. Repeats the process until the selling period ends.

By repeating thousands of simulated seasons, the agent gradually learns pricing strategies that maximize cumulative revenue.

---

# 📌 Key Features

## 🏢 Business Environment

- ✅ Custom Gymnasium Environment
- ✅ Dynamic Inventory Management
- ✅ Configurable Selling Horizon
- ✅ Stochastic Customer Demand
- ✅ Revenue-Based Reward Function
- ✅ Episode Simulation

---

## 🤖 Pricing Agents

### Baseline Agents

- Fixed Price Strategy
- Random Pricing Strategy
- Time-Based Pricing
- Demand-Based Pricing
- Linear Price Decay

---

### Reinforcement Learning Agents

- Tabular Q-Learning
- Deep Q Network (DQN)
- Proximal Policy Optimization (PPO)

---

## 📈 Training Features

- Experience Replay
- Target Network Synchronization
- Epsilon-Greedy Exploration
- Neural Network Training
- Rollout Buffer
- Actor-Critic Learning
- PPO Clipping Objective
- Generalized Advantage Estimation (GAE)

---

## 📊 Evaluation & Analysis

- Revenue Comparison
- Learning Curves
- Policy Visualization
- Price Trajectory Analysis
- Statistical Validation
- Business Performance Reports
- Dashboard Generation
- Agent Benchmarking

---

## 🎯 Current Project Status

| Module | Status |
|----------|--------|
| Environment Design | ✅ Completed |
| Baseline Agents | ✅ Completed |
| Q-Learning | ✅ Completed |
| Deep Q Network (DQN) | ✅ Completed |
| PPO Concepts | ✅ Completed |
| PPO Network | ✅ Completed |
| PPO Agent | ✅ Completed |
| PPO Training | 🔄 In Progress |
| PPO vs DQN Comparison | ⏳ Upcoming |
| Hyperparameter Optimization | ⏳ Upcoming |
| Final Evaluation | ⏳ Upcoming |
| Documentation | 🔄 In Progress |

---

➡️ **Continue with Part 2**, where we'll cover:

- 🏗️ Markov Decision Process (MDP)
- 🤖 Reinforcement Learning Pipeline
- 🧠 Agents Overview
- 🏛️ Project Architecture
- 📂 Repository Structure

# 🏗️ Markov Decision Process (MDP)

The Dynamic Pricing problem is formulated as a **Markov Decision Process (MDP)**, which provides the mathematical foundation for Reinforcement Learning.

At every decision step, the pricing agent observes the current business state, chooses a ticket price, receives a reward, and transitions to the next state.

---

## 📌 MDP Components

| Component | Description |
|------------|-------------|
| **State (S)** | Current inventory and remaining selling days |
| **Action (A)** | Select one of the available ticket prices |
| **Reward (R)** | Revenue generated from ticket sales |
| **Transition (P)** | Customer demand determines the next state |
| **Policy (π)** | Strategy used by the agent for selecting prices |
| **Objective** | Maximize cumulative discounted revenue |

---

## 📦 State Space

The environment represents every business situation using two variables:

| Variable | Description |
|-----------|-------------|
| Inventory Remaining | Number of unsold tickets |
| Days Remaining | Remaining selling days |

Example State:

```text
State = (Inventory = 35, Days Remaining = 18)
```

Current implementation:

| Variable | Range |
|-----------|-------|
| Inventory | 0 → 50 |
| Days Remaining | 0 → 30 |

Total possible states:

```text
51 × 31 = 1,581 States
```

---

## 🎯 Action Space

The pricing agent selects one price from six predefined ticket prices.

| Action | Price |
|---------|-------|
| 0 | $50 |
| 1 | $100 |
| 2 | $150 |
| 3 | $200 |
| 4 | $250 |
| 5 | $300 |

Each action directly influences customer demand and future revenue.

---

## 💰 Reward Function

The reward is the revenue generated after selecting a ticket price.

Positive reward:

```text
Reward = Ticket Price × Tickets Sold
```

Penalty for remaining inventory:

```text
Penalty = Remaining Inventory × Unsold Cost
```

Overall objective:

```text
Maximize Total Revenue
```

---

## 🛑 Episode Termination

Each episode ends when one of the following conditions is met:

- All inventory has been sold.
- The final selling day is reached.

The accumulated revenue over an episode becomes the performance measure for the pricing strategy.

---

# 🤖 Reinforcement Learning Pipeline

The learning process follows the standard Reinforcement Learning interaction cycle.

```text
                    Customer Demand
                           ▲
                           │
                    Environment Update
                           │
                           ▼
+------------------------------------------------+
|           Dynamic Pricing Environment          |
+------------------------------------------------+
                 ▲                 │
                 │                 ▼
          Current State      Selected Price
                 ▲                 │
                 │                 ▼
+------------------------------------------------+
|             Reinforcement Learning Agent       |
+------------------------------------------------+
                 ▲                 │
                 │                 ▼
           Reward Received    Policy Update
```

---

## 🔄 Learning Cycle

For every episode:

1. Initialize the environment.
2. Observe the current state.
3. Select a ticket price.
4. Simulate customer demand.
5. Receive immediate reward.
6. Observe the next state.
7. Update the learning policy.
8. Repeat until the episode ends.

Thousands of simulated episodes gradually improve the pricing policy.

---

# 🧠 Reinforcement Learning Algorithms

The repository progressively implements increasingly sophisticated pricing agents.

---

## 1️⃣ Baseline Pricing Agents

These rule-based strategies provide reference points for comparison.

| Agent | Strategy |
|--------|----------|
| Fixed Price | Constant ticket price |
| Random | Random price selection |
| Time-Based | Price decreases over time |
| Demand-Based | Price reacts to demand |
| Linear Decay | Linear price reduction |

Although simple, these methods establish baseline business performance.

---

## 2️⃣ Tabular Q-Learning

Week 1 introduces classical Reinforcement Learning using a Q-Table.

Key concepts:

- Bellman Equation
- Q-Value Updates
- Epsilon-Greedy Exploration
- State-Action Value Function
- Policy Extraction

Advantages:

- Simple implementation
- Easy to interpret
- Suitable for small state spaces

Limitations:

- Memory intensive
- Poor scalability
- Cannot generalize unseen states

---

## 3️⃣ Deep Q Network (DQN)

Week 2 replaces the Q-Table with a neural network.

Instead of storing every state-action value explicitly, DQN approximates Q-values using deep learning.

Implemented components:

- Neural Network Function Approximation
- Experience Replay Buffer
- Target Network
- Gradient Clipping
- Epsilon Decay
- Model Saving & Loading

Advantages:

- Generalizes to unseen states
- Handles larger environments
- More scalable than tabular methods

---

## 4️⃣ Proximal Policy Optimization (PPO)

Week 3 introduces PPO, one of the most widely used modern Reinforcement Learning algorithms.

Unlike DQN, PPO directly optimizes the policy instead of estimating Q-values.

Implemented features:

- Actor-Critic Architecture
- Rollout Buffer
- Policy Gradient Learning
- Clipped Objective Function
- Generalized Advantage Estimation (GAE)

Expected advantages:

- Stable learning
- Better convergence
- More robust optimization
- Strong performance in complex environments

---

# 📊 Algorithm Progress

| Algorithm | Week | Status |
|------------|------|--------|
| Baseline Agents | Week 1 | ✅ Completed |
| Q-Learning | Week 1 | ✅ Completed |
| Deep Q Network | Week 2 | ✅ Completed |
| PPO Network | Week 3 | ✅ Completed |
| PPO Agent | Week 3 | ✅ Completed |
| PPO Training | Week 3 | 🔄 In Progress |
| PPO Evaluation | Week 3 | ⏳ Upcoming |

---

# 🏛️ Project Architecture

The project follows a modular architecture where each component has a dedicated responsibility.

```text
                   RL Dynamic Pricing System

                           User
                             │
                             ▼
                    Training Pipeline
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
 Environment          Reinforcement Agents     Analysis
        │                    │                    │
        ▼                    ▼                    ▼
 Customer Demand      Pricing Decisions     Performance Reports
        │                    │                    │
        └──────────────► Results ◄───────────────┘
                             │
                             ▼
                    Visualizations & Dashboards
```

---

# 📂 Repository Structure

```text
RL-Dynamic-Pricing/
│
├── notebooks/
│   ├── week1/
│   ├── week2/
│   └── week3/
│
├── src/
│   ├── agents/
│   │   ├── baseline_agents.py
│   │   ├── q_learning_agent.py
│   │   ├── agent_registry.py
│   │   ├── dqn/
│   │   └── ppo/
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
├── notebooks/
├── models/
├── results/
├── data/
├── requirements.txt
└── README.md
```

---

## 📦 Core Modules

| Directory | Purpose |
|------------|----------|
| `agents/` | Pricing algorithms and RL agents |
| `environment/` | Custom Gymnasium environment |
| `training/` | Model training pipelines |
| `simulation/` | Revenue simulations |
| `analysis/` | Business analytics |
| `visualization/` | Charts and dashboards |
| `tests/` | Unit and integration tests |
| `models/` | Saved trained models |
| `results/` | Generated reports and figures |

---

➡️ **Continue with Part 3**, where we'll cover:

- ✅ Week 1 Achievements
- 🚀 Week 2 Achievements
- 🔄 Week 3 Progress (PPO)
- 🧠 DQN Architecture
- 🎭 PPO Actor-Critic Architecture
- ⚙️ Training Configuration

# ✅ Week 1 Achievements

Week 1 established the foundation of the Reinforcement Learning pipeline by designing the environment, defining the pricing problem as a Markov Decision Process (MDP), implementing baseline pricing strategies, and training the first Reinforcement Learning agent using Tabular Q-Learning.

---

## 📌 Week 1 Deliverables

| Module | Status |
|---------|--------|
| Business Problem Formulation | ✅ |
| Markov Decision Process (MDP) | ✅ |
| Custom Gymnasium Environment | ✅ |
| State Space Design | ✅ |
| Action Space Design | ✅ |
| Reward Function | ✅ |
| Stochastic Demand Simulation | ✅ |
| Environment Testing | ✅ |
| Baseline Pricing Agents | ✅ |
| Q-Learning Agent | ✅ |
| Policy Extraction | ✅ |
| Hyperparameter Analysis | ✅ |
| Performance Evaluation | ✅ |

---

## 📚 Reinforcement Learning Concepts Covered

During Week 1, the project introduced several fundamental Reinforcement Learning concepts.

- Markov Decision Process (MDP)
- Bellman Equation
- Q-Table Learning
- Exploration vs Exploitation
- Epsilon-Greedy Policy
- Reward Engineering
- Policy Evaluation
- Dynamic Pricing Simulation

---

## 🎯 Outcome

By the end of Week 1, the project successfully learned an optimal pricing strategy using classical Reinforcement Learning and established a benchmark for future deep learning models.

---

# 🚀 Week 2 Achievements

Week 2 focused on scaling the solution using Deep Reinforcement Learning.

Instead of storing Q-values inside a lookup table, a neural network was introduced to approximate the action-value function, enabling the agent to generalize across unseen states.

---

## 📌 Week 2 Deliverables

| Module | Status |
|---------|--------|
| Deep Q Network (DQN) | ✅ |
| Neural Network Design | ✅ |
| Experience Replay | ✅ |
| Replay Buffer | ✅ |
| Target Network | ✅ |
| Epsilon Decay | ✅ |
| Model Checkpointing | ✅ |
| Training Pipeline | ✅ |
| Business Simulation | ✅ |
| Revenue Comparison | ✅ |
| Policy Visualization | ✅ |
| Statistical Analysis | ✅ |
| Dashboard Generation | ✅ |
| Mid-Project Documentation | ✅ |

---

## 🧠 DQN Features

The DQN implementation includes several techniques that improve learning stability.

- Experience Replay
- Target Network Synchronization
- Mini-Batch Gradient Descent
- Neural Network Function Approximation
- Gradient Clipping
- Adaptive Exploration
- Model Saving & Loading

---

## 📊 Week 2 Results

The trained DQN agent consistently outperformed the rule-based pricing strategies by learning more effective pricing policies.

### Key Improvements

- Higher cumulative revenue
- Better inventory utilization
- Stable learning curves
- Improved long-term decision making
- Intelligent price adaptation

---

# 🔄 Week 3 Progress — PPO Implementation

Week 3 marks the transition from value-based Reinforcement Learning to policy-based optimization using **Proximal Policy Optimization (PPO)**.

Instead of estimating Q-values, PPO learns a policy directly through an Actor-Critic framework, resulting in more stable and efficient training.

---

## 📌 Week 3 Objectives

| Day | Topic | Status |
|------|-------|--------|
| Day 1 | PPO Concepts & Architecture | ✅ |
| Day 2 | PPO Training | 🔄 |
| Day 3 | PPO Evaluation | ⏳ |
| Day 4 | Hyperparameter Tuning | ⏳ |
| Day 5 | Comparative Analysis | ⏳ |
| Day 6 | Code Refactoring | ⏳ |
| Day 7 | Documentation & Wrap-Up | ⏳ |

---

## ✅ Completed So Far

- PPO Configuration
- Actor-Critic Network
- PPO Agent
- PPO Notebook
- Documentation Update

---

## 🚀 Upcoming Work

- PPO Training Loop
- Reward Curve Analysis
- PPO vs DQN Comparison
- Hyperparameter Optimization
- Final Evaluation

---

# 🧠 Deep Q Network (DQN) Architecture

The DQN agent replaces the traditional Q-table with a neural network capable of approximating action values for every pricing decision.

```text
                Input Layer
          (Inventory, Remaining Days)

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

         Q-values for 6 Actions
```

---

## Network Summary

| Layer | Configuration |
|--------|--------------|
| Input Features | 2 |
| Hidden Layer 1 | 128 Units + ReLU |
| Hidden Layer 2 | 64 Units + ReLU |
| Output Layer | 6 Q-values |
| Framework | PyTorch |

Approximate trainable parameters:

```text
≈ 10,000 Parameters
```

---

# 🎭 PPO Actor-Critic Architecture

Unlike DQN, PPO uses two neural networks within a shared architecture.

The **Actor** learns the probability of selecting each pricing action, while the **Critic** estimates how good the current state is.

```text
             State
      (Inventory, Days)

                 │

                 ▼

        Shared Neural Network

      128 Units → ReLU

                 │

                 ▼

       64 Units → ReLU

          ┌─────────────┐
          │             │
          ▼             ▼

      Actor Head    Critic Head

  Action Prob.      State Value

      Softmax          Linear
```

---

## PPO Network Details

| Component | Purpose |
|-----------|----------|
| Shared Layers | Feature Extraction |
| Actor | Policy Learning |
| Critic | Value Estimation |
| Output | Action Probabilities |
| Optimization | PPO Clipping Objective |

---

# ⚖️ DQN vs PPO

| Feature | DQN | PPO |
|----------|-----|-----|
| Learning Method | Value-Based | Policy-Based |
| Architecture | Q-Network | Actor-Critic |
| Exploration | ε-Greedy | Stochastic Policy |
| Replay Buffer | Yes | No |
| Training Style | Off-Policy | On-Policy |
| Output | Q-values | Action Probabilities |
| Stability | Good | Excellent |
| Continuous Actions | Limited | Supported |

---

# ⚙️ Training Configuration

## Tabular Q-Learning

| Parameter | Value |
|-----------|------:|
| Learning Rate | 0.10 |
| Discount Factor | 0.99 |
| Initial Epsilon | 1.00 |
| Final Epsilon | 0.01 |
| Training Episodes | 5,000 |

---

## Deep Q Network (DQN)

| Parameter | Value |
|-----------|------:|
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Batch Size | 64 |
| Replay Buffer | 10,000 |
| Discount Factor | 0.99 |
| Initial Epsilon | 1.00 |
| Final Epsilon | 0.01 |
| Target Network Update | Every 10 Episodes |
| Training Episodes | 2,000 |

---

## Proximal Policy Optimization (PPO)

| Parameter | Value |
|-----------|------:|
| Learning Rate | 0.0003 |
| Discount Factor (γ) | 0.99 |
| GAE Lambda | 0.95 |
| PPO Clip Range | 0.20 |
| Epochs per Update | 10 |
| Batch Size | 64 |
| Rollout Steps | 2,048 |
| Optimizer | Adam |

---

## 📈 Training Pipeline

Each Reinforcement Learning algorithm follows the same high-level workflow.

```text
Initialize Environment
          │
          ▼
Observe Current State
          │
          ▼
Select Pricing Action
          │
          ▼
Simulate Customer Demand
          │
          ▼
Receive Reward
          │
          ▼
Update Learning Algorithm
          │
          ▼
Repeat Until Episode Ends
```

---

➡️ **Continue with Part 4**, which includes:

- 📊 Results & Analysis
- 🏆 Performance Comparison
- 📈 Evaluation Metrics
- 📸 Generated Outputs
- 💻 Installation Guide
- ▶️ Running the Project

# 📊 Results & Analysis

After training each pricing strategy, the agents are evaluated over **1,000 simulated business seasons** to measure their ability to maximize long-term revenue.

The evaluation compares traditional rule-based pricing strategies with Reinforcement Learning approaches, providing insights into how intelligent pricing decisions improve business performance.

---

# 🏆 Overall Performance Ranking

| Rank | Agent | Category | Performance |
|------|---------|-----------|-------------|
| 🥇 | Deep Q Network (DQN) | Deep Reinforcement Learning | Excellent |
| 🥈 | PPO *(Expected)* | Policy-Based Reinforcement Learning | Under Evaluation |
| 🥉 | Tabular Q-Learning | Reinforcement Learning | Very Good |
| 4️⃣ | Time-Based Pricing | Rule-Based | Good |
| 5️⃣ | Demand-Based Pricing | Rule-Based | Moderate |
| 6️⃣ | Linear Decay Pricing | Rule-Based | Moderate |
| 7️⃣ | Fixed Price | Rule-Based | Basic |
| 8️⃣ | Random Pricing | Baseline | Poor |

---

# 📈 Business Insights Learned

The Reinforcement Learning agents discover pricing strategies without manually programmed business rules.

Instead, they learn directly through interactions with the environment.

---

## 🎯 Intelligent Pricing Behaviors

### 📉 Deadline Discounting

As the selling period approaches its end, the agent automatically begins lowering ticket prices.

Benefits:

- Reduce unsold inventory
- Increase ticket sales
- Maximize total revenue

---

### 💰 Scarcity Pricing

When only a few tickets remain, the agent naturally increases prices.

Benefits:

- Higher profit per sale
- Improved inventory utilization
- Better revenue optimization

---

### 📊 Adaptive Pricing

Instead of using a fixed pricing strategy, the agent adjusts prices dynamically based on the current business state.

The learned policy adapts to:

- Remaining inventory
- Remaining selling days
- Customer demand uncertainty

---

### 📦 Inventory Management

The trained models learn to balance two conflicting objectives:

- Selling inventory quickly
- Maximizing revenue per ticket

This balance leads to significantly better long-term business performance.

---

# 📉 Learning Curves

During training, several metrics are monitored to evaluate learning progress.

These include:

- Episode Reward
- Average Revenue
- Training Loss
- Exploration Rate
- Inventory Utilization
- Tickets Sold
- Revenue Growth

The learning curves help determine whether the model has converged to a stable pricing policy.

---

# 📊 Evaluation Metrics

The project evaluates every pricing agent using multiple business-oriented metrics.

| Metric | Description |
|---------|-------------|
| Total Revenue | Overall business revenue generated |
| Average Revenue | Mean revenue per episode |
| Tickets Sold | Inventory utilization |
| Remaining Inventory | Unsold stock analysis |
| Reward Curve | Learning performance |
| Policy Stability | Consistency of pricing decisions |
| Revenue Distribution | Performance variation |
| Training Time | Computational efficiency |

---

# 📈 Comparative Analysis

The project compares Reinforcement Learning algorithms across several characteristics.

| Feature | Q-Learning | DQN | PPO |
|-----------|-----------|-----|-----|
| Learning Type | Value-Based | Value-Based | Policy-Based |
| State Representation | Q-Table | Neural Network | Actor-Critic |
| Scalability | Limited | High | Very High |
| Stability | Moderate | High | Excellent |
| Exploration | ε-Greedy | ε-Greedy | Stochastic Policy |
| Continuous Actions | No | Limited | Yes |
| Sample Efficiency | Moderate | High | High |

---

# 📸 Generated Outputs

Training automatically produces multiple visualizations and reports for analysis.

```text
results/

├── training_curve.png
├── reward_curve.png
├── epsilon_decay.png
├── revenue_comparison.png
├── policy_heatmap.png
├── inventory_analysis.png
├── price_trajectory.png
├── business_dashboard.png
├── simulation_results.csv
├── statistical_analysis.csv
└── business_report.csv
```

---

# 📊 Available Visualizations

The project generates graphical reports including:

- 📈 Training Reward Curve
- 📉 Loss Curve
- 💰 Revenue Comparison
- 🎟 Inventory Utilization
- 📊 Price Distribution
- 📈 Revenue Distribution
- 📉 Epsilon Decay
- 🧠 Learned Pricing Policy
- 📊 Business Dashboard
- 📋 Statistical Summary

---

# 🎯 Key Project Achievements

## Environment

- ✅ Custom Gymnasium Environment
- ✅ Dynamic Pricing Simulator
- ✅ Stochastic Demand Model
- ✅ Reward Engineering

---

## Reinforcement Learning

- ✅ Baseline Pricing Agents
- ✅ Tabular Q-Learning
- ✅ Deep Q Network (DQN)
- ✅ PPO Architecture
- ✅ Actor-Critic Network
- ✅ PPO Agent

---

## Deep Learning

- ✅ Neural Network Approximation
- ✅ Experience Replay
- ✅ Target Network
- ✅ Gradient Clipping
- ✅ Policy Optimization

---

## Business Analytics

- ✅ Revenue Analysis
- ✅ Statistical Comparison
- ✅ Policy Visualization
- ✅ Dashboard Generation
- ✅ Performance Benchmarking

---

# 💻 Installation Guide

## Prerequisites

Before running the project, install the following software:

- Python 3.10 or later
- Git
- pip
- Jupyter Notebook (optional)
- VS Code (recommended)

---

## Clone Repository

```bash
git clone https://github.com/your-username/RL-Dynamic-Pricing.git
```

Move into the project directory.

```bash
cd RL-Dynamic-Pricing
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate the environment:

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

## Verify Installation

Check that Python and PyTorch are installed correctly.

```bash
python --version
```

```bash
pip list
```

---

# ▶️ Running the Project

## Quick Verification

Execute a lightweight pipeline to verify the project setup.

```bash
cd src

python project_runner.py --quick
```

---

## Full Training Pipeline

Run the complete Reinforcement Learning workflow.

```bash
python project_runner.py
```

---

## Individual Modules

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

### Train PPO *(Week 3)*

```bash
python training/ppo_trainer.py
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

### Launch Jupyter Notebook

```bash
jupyter notebook
```

Open the notebook corresponding to the desired internship week and execute the cells sequentially.

---

➡️ **Continue with Part 5**, which includes:

- 🧪 Running Tests
- 📊 Complete Project Workflow
- 📌 Repository Progress
- 🛣️ Development Roadmap
- 🔮 Future Improvements
- 📚 Learning Outcomes
- 🤝 Contributing
- 👨‍💻 Author
- 📄 License
- ⭐ Support
- 🎉 Footer

# 🧪 Running Tests

Testing helps ensure that every module functions correctly before training or evaluation.

---

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

## DQN Tests

```bash
python tests/test_dqn.py
```

---

## PPO Tests

```bash
python tests/test_ppo.py
```

---

## Expected Output

```text
====================================

All tests passed successfully!

====================================
```

---

# 📊 Complete Project Workflow

The project follows a structured Reinforcement Learning workflow from environment creation to business analysis.

```text
                    START
                      │
                      ▼
        Initialize Pricing Environment
                      │
                      ▼
             Observe Current State
                      │
                      ▼
            Select Pricing Action
                      │
                      ▼
          Simulate Customer Demand
                      │
                      ▼
      Receive Reward & Next State
                      │
                      ▼
          Update Learning Policy
                      │
                      ▼
          Episode Finished?
             │            │
            No           Yes
             │            │
             ▼            ▼
      Continue Training  Evaluate Model
                           │
                           ▼
                Generate Reports & Charts
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
| Baseline Pricing Agents | ✅ Completed |
| Q-Learning | ✅ Completed |
| Policy Extraction | ✅ Completed |
| Hyperparameter Analysis | ✅ Completed |
| Deep Q Network (DQN) | ✅ Completed |
| Experience Replay | ✅ Completed |
| Target Network | ✅ Completed |
| DQN Evaluation | ✅ Completed |
| PPO Concepts | ✅ Completed |
| PPO Network | ✅ Completed |
| PPO Agent | ✅ Completed |
| PPO Training | 🔄 In Progress |
| PPO Evaluation | ⏳ Upcoming |
| Hyperparameter Optimization | ⏳ Upcoming |
| Final Internship Report | ⏳ Upcoming |

---

# 🛣️ Development Roadmap

## ✅ Week 1 — Reinforcement Learning Fundamentals

- Environment Design
- Markov Decision Process
- Demand Simulation
- Baseline Pricing Agents
- Q-Learning
- Policy Evaluation

---

## ✅ Week 2 — Deep Reinforcement Learning

- Deep Q Network
- Experience Replay
- Target Network
- DQN Training
- Statistical Evaluation
- Business Dashboard

---

## 🔄 Week 3 — PPO Implementation

- PPO Concepts
- Actor-Critic Architecture
- PPO Agent
- PPO Training
- Policy Evaluation
- PPO vs DQN Comparison

---

## 🚧 Week 4 — Final Project

- Hyperparameter Optimization
- Performance Benchmarking
- Documentation
- Code Cleanup
- Final Internship Submission

---

# 🔮 Future Improvements

The current project provides a strong foundation that can be extended in several directions.

Possible future enhancements include:

- Double DQN
- Dueling DQN
- Rainbow DQN
- Soft Actor-Critic (SAC)
- Multi-Agent Reinforcement Learning
- Continuous Action Space
- Airline Revenue Management
- Hotel Dynamic Pricing
- Retail Pricing Optimization
- Real-World Demand Datasets
- Streamlit Dashboard
- REST API Deployment
- Cloud-Based Model Serving

---

# 📚 Learning Outcomes

This project demonstrates practical implementation of modern Reinforcement Learning techniques.

Core concepts covered include:

- Markov Decision Processes
- Reward Engineering
- Dynamic Programming
- Q-Learning
- Deep Q Networks
- Policy Gradient Methods
- Actor-Critic Models
- PPO Optimization
- Neural Networks with PyTorch
- Business Simulation
- Revenue Optimization
- Model Evaluation
- Statistical Analysis
- Reinforcement Learning in Production

---

# 🤝 Contributing

Contributions are welcome!

To contribute:

1. Fork this repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

Please ensure that your code is well documented and passes all available tests before submitting.

---

➡️ **Continue with Part 6**, which includes:

- 👨‍💻 Author
- 🙏 Acknowledgements
- 📄 License
- ⭐ Support
- 🎉 Closing Footer

# 👨‍💻 Author

<div align="center">

## **Ankur Saini**

**Artificial Intelligence Undergraduate | Machine Learning Enthusiast | Reinforcement Learning Developer**

Passionate about designing intelligent systems that solve real-world business problems using Artificial Intelligence, Machine Learning, and Deep Reinforcement Learning.

</div>

---

## 🚀 Areas of Interest

- 🤖 Artificial Intelligence
- 🧠 Machine Learning
- 🎯 Reinforcement Learning
- 📊 Data Science
- 🔥 Deep Learning
- 🐍 Python Development
- 📈 Business Intelligence
- 💡 AI Product Development

---

## 🌐 Connect With Me

### GitHub

https://github.com/Ankursaini018

---

### LinkedIn

https://www.linkedin.com/in/ankur-saini-596173374/

---

### Portfolio

*Coming Soon...*

---

# 🏅 Internship Timeline

| Week | Focus Area | Status |
|-------|------------|--------|
| Week 1 | Reinforcement Learning Fundamentals | ✅ Completed |
| Week 2 | Deep Q Network (DQN) | ✅ Completed |
| Week 3 | Proximal Policy Optimization (PPO) | 🔄 In Progress |
| Week 4 | Final Evaluation & Optimization | ⏳ Upcoming |

---

# 🏆 Project Highlights

This project demonstrates the practical implementation of modern Reinforcement Learning techniques for solving a real-world Dynamic Pricing problem.

### Completed

- ✅ Custom Gymnasium Environment
- ✅ Business Simulation
- ✅ Markov Decision Process
- ✅ Reward Engineering
- ✅ Baseline Pricing Agents
- ✅ Tabular Q-Learning
- ✅ Deep Q Network (DQN)
- ✅ Experience Replay
- ✅ Target Network
- ✅ Statistical Evaluation
- ✅ Business Dashboards
- ✅ PPO Concepts
- ✅ PPO Actor-Critic Network
- ✅ PPO Agent

---

### Currently Working On

- 🔄 PPO Training
- 🔄 Policy Optimization
- 🔄 Comparative Analysis

---

### Upcoming

- ⏳ Hyperparameter Optimization
- ⏳ PPO vs DQN Evaluation
- ⏳ Final Performance Benchmark
- ⏳ Internship Documentation
- ⏳ Final Project Submission

---

# 📈 Skills Demonstrated

## Reinforcement Learning

- Q-Learning
- Deep Q Networks
- Policy Gradient Methods
- PPO
- Markov Decision Processes

---

## Deep Learning

- PyTorch
- Neural Networks
- Backpropagation
- Optimization
- Function Approximation

---

## Python Ecosystem

- NumPy
- Pandas
- Matplotlib
- Gymnasium
- Stable-Baselines3

---

## Software Engineering

- Object-Oriented Programming
- Modular Project Architecture
- Git & GitHub
- Version Control
- Documentation
- Testing

---

# 🙏 Acknowledgements

This project has been developed as part of the

## **Infotact Solutions**
### Data Science & Machine Learning Technical Internship (2026)

Special thanks to the following open-source communities and organizations for providing outstanding tools and learning resources:

- OpenAI Gymnasium
- PyTorch
- Stable-Baselines3
- NumPy
- Pandas
- Matplotlib
- SciPy
- Python Software Foundation
- Open Source Community

Their contributions have made this project possible.

---

# 📄 License

This project is licensed under the **MIT License**.

You are free to:

- Use
- Study
- Modify
- Share

for educational and research purposes while retaining the original license.

---

# 📚 References

The following resources were helpful throughout the implementation of this project:

- Sutton & Barto — *Reinforcement Learning: An Introduction*
- OpenAI Gymnasium Documentation
- PyTorch Documentation
- Stable-Baselines3 Documentation
- Reinforcement Learning Research Papers

---

# ⭐ Support

If you found this repository useful, consider supporting the project by:

⭐ Starring the repository

🍴 Forking the repository

🛠️ Contributing improvements

📢 Sharing it with others

Every contribution and star helps motivate future development.

---

# 🚀 Future Vision

This repository serves as the foundation for more advanced Reinforcement Learning applications in dynamic decision-making.

Future directions include:

- Airline Revenue Management
- Hotel Pricing Optimization
- Retail Price Optimization
- Cloud Deployment
- Interactive Web Dashboard
- Real-Time Pricing Systems
- Multi-Agent Reinforcement Learning
- Production-Ready AI Services

---

<div align="center">

# 🎯 RL Dynamic Pricing using Reinforcement Learning

### **Learning Intelligent Pricing through Artificial Intelligence**

---

### 📊 Current Progress

| Module | Progress |
|----------|-----------|
| Environment | ✅ |
| Q-Learning | ✅ |
| DQN | ✅ |
| PPO | 🔄 |
| Final Evaluation | ⏳ |

---

### 🚀 Built With

**Python • PyTorch • Gymnasium • Stable-Baselines3 • NumPy • Pandas • Matplotlib**

---

### 💡 "Teaching machines to make smarter pricing decisions through Reinforcement Learning."

---

## ⭐ Thank You for Visiting!

If you enjoyed exploring this project, don't forget to leave a ⭐ on the repository.

Happy Learning! 🚀

</div>