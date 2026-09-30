# RL Dynamic Pricing Terminal — Frontend

Autonomous Yield AI & Multi-Agent Revenue Management Platform built with **React**, **Vite**, and **Tailwind CSS**. Designed with the precision of a Bloomberg Terminal meets modern enterprise AI SaaS.

---

## 🎨 Design System & Palette

- **Dark Theme Background**: `#0d0d1a`
- **Primary Accent**: Gold/Yellow (`#ffd700`)
- **Secondary Accent**: Purple (`#9c27b0`)
- **Agent Spectrum**:
  - **PPO (RL Agent)**: Gold (`#ffd700`)
  - **DQN**: Coral (`#ff6b6b`)
  - **Q-Learning**: Emerald (`#00e676`)
  - **Time-Based Baseline**: Steel Blue (`#64b5f6`)
- **Typography**:
  - **Headings & UI**: `Space Grotesk`
  - **Metrics, Tickers & Code**: `JetBrains Mono`
- **Aesthetic Elements**:
  - Glassmorphism cards with multi-layered backdrop blurs and subtle neon borders
  - High-performance HTML5 canvas animated particle background (subtle floating gold & purple dots with mouse interactivity)
  - Real-time Bloomberg-style order feed ticker
  - Live season counter (`Season #1,482`) with interactive play/step controls

---

## 🚀 Modules & Pages

1. **Dashboard (Main Overview)**
   - 4 Top-line KPI Cards (Mean Season Revenue `$2,245.00`, Sell-Through `94.2%`, Early Stockout Risk `0.8%`, Penalty Aversion `98.6%`)
   - Interactive Algorithm Performance Matrix with sorting (Revenue, Sell-Through %, Win Rate %)
   - Verified Economic Behavior Badges (Deadline Discounting & Scarcity Premium)
   - Official 7-Algorithm Benchmark Standings Table
2. **Agent Arena (Live Multi-Agent Competition)**
   - Synchronous head-to-head simulation across 30-day seasons
   - Controls: Play, Pause, Step (+1d), Instant (30d), Speed selector (1x, 3x, 10x), and Seed selector
   - Real-time fluid inventory tanks (50 starting items draining per sale)
   - Cumulative revenue race tickers and dynamic SVG line race chart
   - Live customer transaction event log
3. **Price Trajectory (Behavioral Proof)**
   - 30-Day average price trajectory comparison chart with highlighted red **Deadline Zone (Days 25–30)**
   - 4-Stage empirical lifecycle period breakdown
   - Interactive **Live Policy Decision Sandbox**: sliders for Days Remaining (1–30) and Inventory (0–50) with instant PPO action recommendation and actor head softmax probabilities
4. **Training Progress**
   - Cumulative reward convergence curves across 2,000 episodes (raw noise + 100-episode moving average)
   - Epsilon exploration decay curve ($\epsilon: 1.0 \to 0.01$)
   - Critic/Value loss minimization tracking
   - 2D Policy Landscape Heatmap (Inventory vs. Days Left) with hover state inspection
5. **Business Value Calculator**
   - Enterprise ROI & Revenue Expansion Engine
   - Interactive sliders: Annual Flight/Season Scale, Seat Capacity, Baseline Revenue, RL Alpha Uplift %, Cloud Compute Cost
   - Key dynamic financial outputs: Net Annual Profit Lift, ROI Multiple, Payback Days, Penalty Avoidance Savings
   - Volume vs. Uplift Sensitivity Matrix
   - Export Executive Brief button with clipboard copy and celebration confetti

---

## 💻 Running Locally

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start development server
npm run dev

# Build for production
npm run build
```
The application will be served at `http://localhost:5173/`.
