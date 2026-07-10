# 🛠️ Utils Module Documentation

## Overview
Utility modules for RL Dynamic Pricing project.

---

## 📁 Files

### evaluator.py
Evaluation framework for comparing agents.

```python
from utils.evaluator import evaluate_agent, compare_agents

# Evaluate single agent
df = evaluate_agent(agent, n_episodes=100)

# Compare multiple agents
all_results, summary = compare_agents(agents, n_episodes=100)
```

### demand_analyzer.py
Analyzes stochastic demand function.

```python
from utils.demand_analyzer import analyze_demand
df = analyze_demand()
```

### q_table_analyzer.py
Deep analysis of trained Q-table.

```python
from utils.q_table_analyzer import (
    analyze_q_table,
    plot_policy_heatmaps,
    analyze_learned_behavior
)
results = analyze_q_table(agent)
```

### policy_extractor.py
Extracts learned policy from Q-table.

```python
from utils.policy_extractor import (
    extract_policy_table,
    save_policy_summary
)
policy_df = extract_policy_table(agent)
summary   = save_policy_summary(agent)
```

### training_visualizer.py
Visualization for training progress.

```python
from utils.training_visualizer import (
    plot_learning_curve,
    plot_price_trajectory,
    plot_revenue_comparison
)
plot_learning_curve(rewards, 'Q-Learning')
```

### results_consolidator.py
Consolidates all agent results.

```python
from utils.results_consolidator import (
    consolidate_week1_results
)
df = consolidate_week1_results()
```

---

## 📊 Output Files
All outputs saved to `results/` folder:
- `agent_comparison.png`
- `baseline_comparison.png`
- `demand_analysis.png`
- `ql_training.png`
- `q_table_policy.png`
- `policy_analysis.png`
- `week1_consolidated.csv`
- `policy_summary.json`