# 🎮 Environment Module Documentation

## Overview
Custom Gymnasium environment for dynamic pricing.

---

## DynamicPricingEnv

### MDP Formulation
| Component | Details |
|---|---|
| State | (remaining_inventory, days_until_departure) |
| Action | price_level index (0-5) |
| Reward | Revenue from sale |
| Penalty | -10 per unsold ticket |

### Price Levels
$50, $100, $150, $200, $250, $300

### Usage
```python
from environment.pricing_env import DynamicPricingEnv

env = DynamicPricingEnv(
    max_inventory=50,
    max_days=30
)

# Reset
obs, info = env.reset(seed=42)

# Step
obs, reward, terminated, truncated, info = (
    env.step(action)
)

# Info dict contains:
# - price, bought, inventory
# - days_left, total_revenue
# - demand_prob
```

### Demand Function
- Higher price → Lower demand
- Fewer days → Lower demand
- Stochastic noise for realism