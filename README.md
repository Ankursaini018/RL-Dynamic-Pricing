# 🎯 RL Dynamic Pricing
## Infotact DS/ML Technical Internship 2026

![Status](https://img.shields.io/badge/Status-In%20Progress-blue)
![Week](https://img.shields.io/badge/Week-1%20of%204-orange)
![Model](https://img.shields.io/badge/Model-DQN%20%2B%20RL-red)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)

---

## 🎯 Project Overview
**Type:** Reinforcement Learning for Dynamic Pricing
**Domain:** Travel & Hospitality
**Mode:** Solo Worker
**Goal:** Build autonomous pricing agent using RL
         that maximizes revenue from finite inventory

---

## 🧠 Problem Statement
Selling finite inventory (airline tickets/hotel rooms)
over limited time is a complex optimization problem.
Static pricing fails to account for:
- Fluctuating market demand
- Competitor pricing
- Time pressure (unsold = lost revenue)

**Solution:** RL agent that learns optimal pricing
policy through environment interaction!

---

## 🏗️ MDP Formulation
| Component | Description |
|---|---|
| State | (remaining_inventory, days_until_departure) |
| Action | price_level (6 discrete prices $50-$300) |
| Reward | Revenue earned per sale |
| Penalty | -10 per unsold ticket at deadline |

---

## 📅 Week-wise Progress

### 🔄 Week 1 — MDP + Gym Environment
- ✅ MDP formulated
- ✅ Custom Gymnasium environment built
- ✅ Stochastic demand function implemented
- 🔄 Baseline agents (tomorrow)

---

## 🔬 How to Run
```bash
pip install -r requirements.txt
cd src
python environment/pricing_env.py
```

---

## 📊 GitHub Issues
| Issue | Title | Status |
|---|---|---|
| #1 | Design MDP + Gym environment | 🔄 In Progress |
| #2 | Stochastic demand function | 📅 Todo |
| #3 | Naive baseline agents | 📅 Todo |
| #4 | Q-Learning implementation | 📅 Todo |
| #5 | Deep Q-Network (DQN) | 📅 Todo |
| #6 | Experience replay + epsilon greedy | 📅 Todo |
| #7 | Train + evaluate DQN | 📅 Todo |
| #8 | 1000 season simulation | 📅 Todo |
| #9 | Price trajectories dashboard | 📅 Todo |