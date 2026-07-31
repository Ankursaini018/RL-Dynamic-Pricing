# 🎯 RL Dynamic Pricing using Reinforcement Learning

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gymnasium](https://img.shields.io/badge/Gymnasium-Environment-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red.svg)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-orange.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-yellow.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple.svg)
![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)

**A Reinforcement Learning based Dynamic Pricing System for Revenue Optimization**

</div>

---

# 📖 Project Overview

Dynamic pricing is a pricing strategy where product prices continuously change based on demand, inventory, seasonality, and customer behavior.

Instead of using fixed prices, businesses use intelligent algorithms that maximize long-term revenue while adapting to changing market conditions.

This project implements a complete Reinforcement Learning pipeline where multiple pricing agents compete in a simulated marketplace.

The objective is to learn the optimal pricing policy that generates maximum revenue over thousands of simulated selling seasons.

---

# 🚀 Project Objectives

- Build a custom Dynamic Pricing environment using Gymnasium
- Simulate realistic customer demand
- Compare traditional pricing strategies with RL agents
- Train Q-Learning, DQN and PPO agents
- Evaluate policies using statistical analysis
- Measure long-term revenue improvement
- Demonstrate real-world business value

---

# ✨ Key Features

✅ Custom Gymnasium Environment

✅ Stochastic Customer Demand Simulation

✅ Inventory Management

✅ Price Elasticity Modeling

✅ Seasonal Demand

✅ Five Baseline Pricing Agents

✅ Q-Learning Agent

✅ Deep Q Network (DQN)

✅ Proximal Policy Optimization (PPO)

✅ Hyperparameter Analysis

✅ Policy Visualization

✅ Statistical Proof

✅ Revenue Comparison Dashboard

✅ Business Value Estimation

---

# 🧠 Reinforcement Learning Algorithms

| Algorithm | Type | Status |
|------------|------|--------|
| Fixed Price | Rule-Based | ✅ |
| Linear Decay | Rule-Based | ✅ |
| Time-Based Pricing | Rule-Based | ✅ |
| Demand-Based Pricing | Rule-Based | ✅ |
| Inventory-Based Pricing | Rule-Based | ✅ |
| Q-Learning | Tabular RL | ✅ |
| Deep Q Network (DQN) | Deep Reinforcement Learning | ✅ |
| PPO | Policy Gradient | ✅ |

---

# 🏗️ Project Architecture

```text
                    Dynamic Pricing Problem
                              │
                              ▼
                 Customer Demand Simulation
                              │
                              ▼
               Custom Gymnasium Environment
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Baseline Agents    Q-Learning      Deep RL
                                               │
                                 ┌─────────────┴─────────────┐
                                 ▼                           ▼
                               DQN                          PPO
                                 │                           │
                                 └─────────────┬─────────────┘
                                               ▼
                                   Revenue Evaluation
                                               │
                                               ▼
                                  Statistical Comparison
                                               │
                                               ▼
                                    Business Insights
```

---

# 📂 Project Structure

```text
RL-Dynamic-Pricing/
│
├── notebooks/
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   └── week4/
│
├── src/
│   ├── environment/
│   ├── agents/
│   ├── training/
│   ├── analysis/
│   ├── simulation/
│   └── utils/
│
├── models/
│
├── results/
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/RL-Dynamic-Pricing.git

cd RL-Dynamic-Pricing
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Run the main training scripts

```bash
python src/training/train_q_learning.py
```

```bash
python src/training/train_dqn.py
```

```bash
python src/training/train_ppo.py
```

Run the final simulation

```bash
python src/simulation/final_simulation.py
```

Generate statistical proof

```bash
python src/analysis/final_proof.py
```

Generate business value report

```bash
python src/simulation/business_value.py
```

---

# 📅 Internship Progress

## ✅ Week 1 — MDP + Environment + Q-Learning

### Deliverables

- Markov Decision Process Design
- Custom Gymnasium Environment
- Stochastic Demand Function
- Baseline Pricing Agents
- Q-Learning Agent
- Policy Evaluation
- Reward Visualization

### Skills Learned

- Reinforcement Learning Fundamentals
- Markov Decision Processes
- Bellman Equation
- Exploration vs Exploitation
- Q-Table Learning
- Environment Design

---

## ✅ Week 2 — Deep Reinforcement Learning

### Deliverables

- Neural Network Function Approximation
- Deep Q Network (DQN)
- Experience Replay Buffer
- Target Network
- Epsilon Decay
- DQN Training Pipeline
- Performance Evaluation

### Skills Learned

- Deep Learning
- PyTorch
- Replay Memory
- Neural Network Optimization
- Stable RL Training

---

## ✅ Week 3 — PPO + Analysis

### Deliverables

- PPO Agent
- Advantage Estimation
- Policy Gradient Optimization
- Hyperparameter Tuning
- Policy Visualization
- Learning Curve Analysis
- Agent Comparison

### Skills Learned

- Policy Gradient Methods
- PPO Algorithm
- Generalized Advantage Estimation
- Deep Reinforcement Learning
- Policy Optimization

---

## Week 4 Day 3 — Documentation ✅

### Documentation Complete
| Document | Status |
|---|---|
| Project Summary | ✅ |
| Model Card | ✅ |
| Reproduction Guide | ✅ |
| Submission Checklist | ✅ |
| Final Review Prep | ✅ |

### How to Reproduce Results
```bash
# Quick test (5 minutes)
cd src
python project_runner.py --quick

# Full pipeline (30 minutes)
python project_runner.py

# Run all tests
python tests/test_ppo.py
python tests/test_agents.py
python tests/test_environment.py
```

### Issues Updated
| Issue | Status |
|---|---|
| #16 Final documentation | ✅ Closed |
| #17 Performance optimization | ✅ Closed |
| #18 Final submission | 🔄 Tomorrow |
| #21 Submission ready | 📅 Day 5 |

### Deliverables

- Final Simulation
- Statistical Proof
- Business Value Analysis
- Revenue Dashboard
- Documentation
- Final Report

---

# 🧠 Q-Learning

Q-Learning is a model-free reinforcement learning algorithm that learns the expected future reward for every state-action pair.

The agent updates a Q-Table using the Bellman Equation and gradually learns the optimal pricing strategy.

### Advantages

- Easy to implement
- Fast convergence for small state spaces
- Strong theoretical foundation

### Limitations

- Large memory requirement
- Doesn't scale well to continuous environments

---

# 🤖 Deep Q Network (DQN)

Deep Q Network replaces the traditional Q-Table with a Neural Network.

Instead of storing every Q-value explicitly, the neural network predicts the Q-values for every action.

Major improvements include:

- Experience Replay
- Target Network
- Neural Function Approximation
- Stable Learning

### Advantages

- Handles large state spaces
- Better generalization
- Learns complex pricing patterns

### Limitations

- Longer training time
- Hyperparameter sensitive

---

# 🚀 Proximal Policy Optimization (PPO)

PPO is one of the most successful policy-gradient reinforcement learning algorithms.

Instead of learning Q-values, PPO directly learns the pricing policy.

The clipped objective function prevents unstable updates and significantly improves convergence.

### Advantages

- Stable training
- Excellent convergence
- High sample efficiency
- Strong real-world performance

### Limitations

- Computationally expensive
- Requires policy optimization

---

# 📊 Evaluation Metrics

The project evaluates each pricing strategy using multiple business metrics.

| Metric | Description |
|----------|-------------|
| Total Revenue | Total earnings generated |
| Average Revenue | Mean revenue across seasons |
| Profit | Revenue after pricing decisions |
| Inventory Sold | Units successfully sold |
| Remaining Inventory | Unsold stock |
| Customer Demand | Market demand generated |
| Reward | RL optimization objective |

---

# 📈 Results Summary

The reinforcement learning agents consistently outperform traditional pricing strategies.

Key observations:

- PPO achieved the highest average revenue.
- DQN demonstrated strong learning performance.
- Q-Learning provided an effective baseline RL solution.
- Rule-based agents remained consistent but less adaptive.
- Statistical testing confirmed significant improvements.

---

# 🏆 Agent Comparison

| Agent | Learning Type | Performance |
|--------|---------------|------------|
| PPO | Policy Gradient | 🥇 Excellent |
| DQN | Deep RL | 🥈 Very Good |
| Q-Learning | Tabular RL | 🥉 Good |
| Inventory-Based | Rule-Based | Good |
| Demand-Based | Rule-Based | Average |
| Time-Based | Rule-Based | Average |
| Linear Decay | Rule-Based | Basic |
| Fixed Price | Rule-Based | Baseline |

---

# 📊 Business Impact

The final pricing policies demonstrate the practical benefits of Reinforcement Learning in dynamic pricing scenarios.

Business outcomes include:

- Increased revenue
- Better inventory utilization
- Improved pricing decisions
- Reduced manual intervention
- Adaptive response to demand fluctuations
- Data-driven pricing optimization

---

# 🛠️ Technologies Used

| Category | Technologies |
|-----------|--------------|
| Programming Language | Python |
| Reinforcement Learning | Gymnasium |
| Deep Learning | PyTorch |
| Data Analysis | NumPy, Pandas |
| Visualization | Matplotlib |
| IDE | VS Code, Jupyter Notebook |
| Version Control | Git & GitHub |

---

# 📊 Project Workflow

```text
Market Environment
        │
        ▼
Customer Demand Simulation
        │
        ▼
Dynamic Pricing Environment
        │
        ▼
Baseline Pricing Agents
        │
        ├───────────────┐
        ▼               ▼
  Q-Learning         Deep RL
                        │
                ┌───────┴────────┐
                ▼                ▼
              DQN               PPO
                │
                ▼
      Performance Evaluation
                │
                ▼
      Statistical Validation
                │
                ▼
      Business Value Analysis
```

---

# 🎯 Learning Outcomes

This project helped me gain practical experience in:

- Reinforcement Learning Fundamentals
- Markov Decision Processes (MDP)
- Custom Gymnasium Environment Design
- Q-Learning Implementation
- Deep Q Networks (DQN)
- Proximal Policy Optimization (PPO)
- Neural Network Training using PyTorch
- Experience Replay
- Target Networks
- Policy Gradient Algorithms
- Hyperparameter Optimization
- Statistical Performance Evaluation
- Business Impact Analysis
- Data Visualization
- Software Engineering Best Practices
- Git & GitHub Workflow

---

# 📈 Future Improvements

Some exciting enhancements that can be added to this project include:

- Multi-Product Dynamic Pricing
- Multi-Agent Reinforcement Learning
- Continuous Action Spaces
- SAC (Soft Actor-Critic)
- A3C / A2C Algorithms
- Demand Forecasting Integration
- Customer Segmentation
- Real-Time Pricing Dashboard
- REST API Deployment
- Docker Containerization
- Cloud Deployment (AWS/Azure/GCP)
- MLOps Pipeline Integration

---

# 📂 Repository Highlights

✔️ Custom Gymnasium Environment

✔️ Realistic Customer Demand Simulation

✔️ Multiple Rule-Based Pricing Agents

✔️ Q-Learning Agent

✔️ Deep Q Network (DQN)

✔️ PPO Agent

✔️ Statistical Analysis

✔️ Business Value Report

✔️ Modular Code Structure

✔️ Professional Documentation

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve this project:

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to your branch

```bash
git push origin feature-name
```

5. Open a Pull Request

Please ensure your code follows good coding practices and includes appropriate documentation.

---

# 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this project for educational and research purposes.

---

# 👨‍💻 Author

**Ankur Saini**

B.Tech Artificial Intelligence Student

Passionate about:

- Artificial Intelligence
- Machine Learning
- Reinforcement Learning
- Deep Learning
- Generative AI
- MLOps
- Data Science

GitHub:
https://github.com/Ankursaini018

---

# 🙏 Acknowledgements

Special thanks to:

- OpenAI
- Gymnasium
- PyTorch
- NumPy
- Pandas
- Matplotlib
- The Reinforcement Learning Community

for providing excellent open-source tools and learning resources.

---

# ⭐ Support

If you found this project helpful:

⭐ Star the repository

🍴 Fork the repository

📢 Share it with others

💡 Suggest improvements

Your support is greatly appreciated!

---

# 📬 Contact

If you'd like to connect or discuss Reinforcement Learning, AI, or Machine Learning projects:

- GitHub: https://github.com/Ankursaini018

---

<div align="center">

# 🎉 Thank You!

**RL Dynamic Pricing using Reinforcement Learning**

*A complete end-to-end Reinforcement Learning project demonstrating intelligent pricing strategies through Q-Learning, Deep Q Networks (DQN), and Proximal Policy Optimization (PPO).*

⭐ **If you enjoyed this project, don't forget to Star the repository!** ⭐

</div>