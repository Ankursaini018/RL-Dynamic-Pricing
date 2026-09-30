import React, { useState } from "react";
import {
  LineChart,
  Cpu,
  Layers,
  Activity,
  Sliders,
  Sparkles,
  Info,
  CheckCircle2,
  Database,
  Grid,
} from "lucide-react";
import { TRAINING_METRICS, PROJECT_METADATA } from "../data/simulationData";

export default function TrainingProgressPage() {
  const [selectedAgent, setSelectedAgent] = useState("PPO");
  const [showRawCurve, setShowRawCurve] = useState(true);
  const [hoveredCell, setHoveredCell] = useState(null);

  // Generate a sampled 10x10 representation of the 51x31 state space Q-Table / Policy matrix
  const daysSteps = [30, 26, 22, 18, 14, 10, 7, 4, 2, 0];
  const invSteps = [50, 44, 38, 32, 26, 20, 15, 10, 5, 0];

  const getHeatmapAction = (daysLeft, inv) => {
    if (inv === 0) return { price: 300, color: "#ffd700", label: "$300" };
    if (daysLeft <= 4) {
      if (inv > 8) return { price: 50, color: "#00e676", label: "$50" };
      return { price: 100, color: "#64b5f6", label: "$100" };
    }
    if (inv < daysLeft * 0.75) return { price: 250, color: "#ffd700", label: "$250" };
    if (inv > daysLeft * 1.5) return { price: 100, color: "#64b5f6", label: "$100" };
    return { price: 200, color: "#ba68c8", label: "$200" };
  };

  return (
    <div className="space-y-6 pb-12 animate-fadeIn">
      {/* Title & Hyperparameters Header */}
      <div className="glass-panel glass-panel-gold rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-mono text-[#ffd700] mb-1">
              <Cpu className="h-4 w-4" />
              <span>NEURAL NETWORK &amp; TABULAR TRAINING DYNAMICS</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Model Training Progress &amp; Convergence
            </h1>
            <p className="text-xs sm:text-sm text-slate-300">
              Reward trajectory curves, loss minimization, epsilon exploration decay, and 2D state-action policy map.
            </p>
          </div>

          {/* Agent Switcher */}
          <div className="flex items-center gap-2 bg-black/40 border border-white/10 p-1.5 rounded-xl font-mono text-xs">
            {["PPO", "DQN", "Q-Learning"].map((algo) => (
              <button
                key={algo}
                onClick={() => setSelectedAgent(algo)}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  selectedAgent === algo
                    ? "bg-[#ffd700] text-black font-bold shadow-glow-gold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {algo}
              </button>
            ))}
          </div>
        </div>

        {/* Hyperparameter Quick Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-2 mt-6 pt-4 border-t border-white/10 text-xs font-mono">
          <div className="bg-black/30 p-2 rounded-lg border border-white/5">
            <span className="text-[10px] text-slate-400 block">Framework:</span>
            <span className="text-white font-bold">PyTorch 2.x</span>
          </div>
          <div className="bg-black/30 p-2 rounded-lg border border-white/5">
            <span className="text-[10px] text-slate-400 block">Architecture:</span>
            <span className="text-[#ffd700] font-bold">2 → 128 → 64 → 6</span>
          </div>
          <div className="bg-black/30 p-2 rounded-lg border border-white/5">
            <span className="text-[10px] text-slate-400 block">Discount (γ):</span>
            <span className="text-white font-bold">0.99</span>
          </div>
          <div className="bg-black/30 p-2 rounded-lg border border-white/5">
            <span className="text-[10px] text-slate-400 block">GAE Lambda (λ):</span>
            <span className="text-white font-bold">0.95</span>
          </div>
          <div className="bg-black/30 p-2 rounded-lg border border-white/5">
            <span className="text-[10px] text-slate-400 block">Clip Range (ε):</span>
            <span className="text-purple-300 font-bold">0.20</span>
          </div>
          <div className="bg-black/30 p-2 rounded-lg border border-white/5">
            <span className="text-[10px] text-slate-400 block">Replay Buffer:</span>
            <span className="text-emerald-400 font-bold">10,000 tuples</span>
          </div>
        </div>
      </div>

      {/* Main Learning Curves Grid: Reward Convergence & Loss / Epsilon */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Cumulative Episode Reward Curve */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-3">
            <div>
              <h3 className="font-bold text-white text-base flex items-center gap-2">
                <LineChart className="h-4 w-4 text-[#ffd700]" />
                Cumulative Reward Convergence (2,000 Episodes)
              </h3>
              <p className="text-xs font-mono text-slate-400">
                Tracking policy improvement from early random exploration ($1,100) to mature equilibrium ($2,245)
              </p>
            </div>

            <div className="flex items-center gap-2 text-xs font-mono">
              <label className="flex items-center gap-1.5 cursor-pointer text-slate-300">
                <input
                  type="checkbox"
                  checked={showRawCurve}
                  onChange={(e) => setShowRawCurve(e.target.checked)}
                  className="rounded bg-black/40 border-white/20 text-[#ffd700] accent-[#ffd700]"
                />
                <span>Raw Noise</span>
              </label>

              <span className="text-slate-500">|</span>

              <div className="flex items-center gap-1">
                <span className="h-2 w-2 rounded-full bg-[#ffd700]" />
                <span className="text-white font-bold">{selectedAgent} Smooth (w=100)</span>
              </div>
            </div>
          </div>

          {/* SVG Learning Curve */}
          <div className="relative h-72 w-full pt-4">
            <svg className="w-full h-full overflow-visible" viewBox="0 0 600 240">
              {/* Horizontal Grid lines */}
              {[1000, 1300, 1600, 1900, 2200, 2500].map((r) => {
                const y = 220 - ((r - 900) / 1600) * 190;
                return (
                  <g key={r}>
                    <line
                      x1="45"
                      y1={y}
                      x2="590"
                      y2={y}
                      stroke="rgba(255,255,255,0.06)"
                      strokeDasharray="4 4"
                    />
                    <text
                      x="35"
                      y={y + 4}
                      fill="#64748b"
                      fontSize="9"
                      fontFamily="JetBrains Mono"
                      textAnchor="end"
                    >
                      ${r}
                    </text>
                  </g>
                );
              })}

              {/* X Axis Episode markers */}
              {[200, 500, 1000, 1500, 2000].map((ep) => {
                const x = 45 + (ep / 2000) * 540;
                return (
                  <g key={ep}>
                    <line x1={x} y1="218" x2={x} y2="224" stroke="#64748b" />
                    <text
                      x={x}
                      y="238"
                      fill="#94a3b8"
                      fontSize="9"
                      fontFamily="JetBrains Mono"
                      textAnchor="middle"
                    >
                      Ep {ep}
                    </text>
                  </g>
                );
              })}

              {/* Raw Noisy Curve */}
              {showRawCurve && (
                <polyline
                  fill="none"
                  stroke={
                    selectedAgent === "PPO"
                      ? "#ffd700"
                      : selectedAgent === "DQN"
                      ? "#ff6b6b"
                      : "#00e676"
                  }
                  strokeWidth="1"
                  strokeOpacity="0.25"
                  points={TRAINING_METRICS.map((pt) => {
                    const x = 45 + (pt.episode / 2000) * 540;
                    const val =
                      selectedAgent === "PPO"
                        ? pt.ppoRaw
                        : selectedAgent === "DQN"
                        ? pt.dqnRaw
                        : pt.qlRaw;
                    const y = 220 - ((val - 900) / 1600) * 190;
                    return `${x},${y}`;
                  }).join(" ")}
                />
              )}

              {/* Smoothed Curve */}
              <polyline
                fill="none"
                stroke={
                  selectedAgent === "PPO"
                    ? "#ffd700"
                    : selectedAgent === "DQN"
                    ? "#ff6b6b"
                    : "#00e676"
                }
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={TRAINING_METRICS.map((pt) => {
                  const x = 45 + (pt.episode / 2000) * 540;
                  const val =
                    selectedAgent === "PPO"
                      ? pt.ppoSmooth
                      : selectedAgent === "DQN"
                      ? pt.dqnSmooth
                      : pt.qlSmooth;
                  const y = 220 - ((val - 900) / 1600) * 190;
                  return `${x},${y}`;
                }).join(" ")}
                style={{
                  filter: `drop-shadow(0 0 8px ${
                    selectedAgent === "PPO"
                      ? "rgba(255, 215, 0, 0.4)"
                      : selectedAgent === "DQN"
                      ? "rgba(255, 107, 107, 0.4)"
                      : "rgba(0, 230, 118, 0.4)"
                  })`,
                }}
              />
            </svg>
          </div>
        </div>

        {/* Right Col: Exploration Epsilon Decay & Loss Diagnostics */}
        <div className="space-y-4">
          {/* Epsilon Decay Plot */}
          <div className="glass-panel rounded-2xl p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-white/10 pb-2">
              <span className="text-xs font-mono font-bold text-white flex items-center gap-1.5">
                <Activity className="h-3.5 w-3.5 text-purple-400" />
                Exploration Decay (ε: 1.0 → 0.01)
              </span>
              <span className="text-[10px] font-mono text-[#ffd700]">Factor: 0.995</span>
            </div>

            <div className="relative h-28 w-full">
              <svg className="w-full h-full" viewBox="0 0 300 90">
                <polyline
                  fill="none"
                  stroke="#9c27b0"
                  strokeWidth="2.5"
                  points={TRAINING_METRICS.map((pt) => {
                    const x = 20 + (pt.episode / 2000) * 260;
                    const y = 80 - pt.epsilon * 70;
                    return `${x},${y}`;
                  }).join(" ")}
                />
                <circle cx="20" cy="10" r="3" fill="#9c27b0" />
                <circle cx="280" cy="79" r="3" fill="#9c27b0" />
              </svg>
            </div>

            <div className="text-[11px] font-mono text-slate-400 flex justify-between">
              <span>Ep 1: ε = 1.0 (Explore)</span>
              <span>Ep 2000: ε = 0.01 (Exploit)</span>
            </div>
          </div>

          {/* Loss Convergence */}
          <div className="glass-panel rounded-2xl p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-white/10 pb-2">
              <span className="text-xs font-mono font-bold text-white flex items-center gap-1.5">
                <Cpu className="h-3.5 w-3.5 text-coral-400 text-[#ff6b6b]" />
                Critic / Value Loss Minimization
              </span>
              <span className="text-[10px] font-mono text-emerald-400">Converged</span>
            </div>

            <div className="relative h-28 w-full">
              <svg className="w-full h-full" viewBox="0 0 300 90">
                <polyline
                  fill="none"
                  stroke="#ff6b6b"
                  strokeWidth="2.5"
                  points={TRAINING_METRICS.map((pt) => {
                    const x = 20 + (pt.episode / 2000) * 260;
                    const y = 80 - (pt.ppoLoss / 0.45) * 70;
                    return `${x},${y}`;
                  }).join(" ")}
                />
              </svg>
            </div>

            <div className="text-[11px] font-mono text-slate-400 flex justify-between">
              <span>Initial Loss: 0.420</span>
              <span className="text-emerald-400 font-bold">Final Loss: 0.032</span>
            </div>
          </div>
        </div>
      </div>

      {/* 2D State-Action Policy Heatmap (Q-Table Visualizer) */}
      <div className="glass-panel rounded-2xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-3">
          <div>
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <Grid className="h-4 w-4 text-[#ffd700]" />
              2D Policy Landscape Heatmap: Inventory vs. Days Left
            </h3>
            <p className="text-xs font-mono text-slate-400">
              Color indicates the optimal action chosen at state (Inventory, Days Remaining). Notice the green liquidation band at low days left!
            </p>
          </div>

          {/* Action Color Legend */}
          <div className="flex flex-wrap items-center gap-3 text-xs font-mono">
            <div className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded bg-[#00e676]" />
              <span>$50 (Clearance)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded bg-[#64b5f6]" />
              <span>$100 (Decay)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded bg-[#ba68c8]" />
              <span>$200 (Equilibrium)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded bg-[#ffd700]" />
              <span>$250-$300 (Premium)</span>
            </div>
          </div>
        </div>

        {/* Heatmap Grid */}
        <div className="overflow-x-auto pb-2">
          <div className="min-w-[620px]">
            {/* Grid Header: Days Left */}
            <div className="flex items-center mb-1 text-[11px] font-mono text-slate-400 pl-24">
              <span className="w-full text-center tracking-widest text-[#ffd700] uppercase">
                ← Horizon: Days Remaining in Season (30 → 0) →
              </span>
            </div>

            <div className="flex pl-24 mb-2 text-[10px] font-mono text-slate-400 justify-between">
              {daysSteps.map((d) => (
                <div key={d} className="w-10 text-center font-bold">
                  {d}d
                </div>
              ))}
            </div>

            {/* Rows: Inventory Levels */}
            <div className="space-y-1.5">
              {invSteps.map((inv) => (
                <div key={inv} className="flex items-center gap-2">
                  <div className="w-20 text-right text-[11px] font-mono text-slate-400 font-bold shrink-0">
                    {inv} items
                  </div>

                  <div className="flex items-center justify-between w-full gap-1">
                    {daysSteps.map((daysLeft) => {
                      const action = getHeatmapAction(daysLeft, inv);
                      const isHovered =
                        hoveredCell &&
                        hoveredCell.inv === inv &&
                        hoveredCell.daysLeft === daysLeft;

                      return (
                        <div
                          key={`${inv}-${daysLeft}`}
                          onMouseEnter={() =>
                            setHoveredCell({
                              inv,
                              daysLeft,
                              price: action.price,
                              label: action.label,
                            })
                          }
                          onMouseLeave={() => setHoveredCell(null)}
                          className={`h-9 flex-1 rounded flex items-center justify-center text-[10px] font-mono font-bold transition-all cursor-pointer ${
                            isHovered
                              ? "scale-110 z-10 shadow-lg ring-2 ring-white"
                              : "hover:opacity-90"
                          }`}
                          style={{
                            backgroundColor: `${action.color}35`,
                            color: action.color,
                            border: `1px solid ${action.color}60`,
                          }}
                        >
                          {action.label}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Hovered State Tooltip / Inspector */}
        <div className="rounded-xl border border-white/10 bg-black/40 p-3 text-xs font-mono text-slate-300 flex items-center justify-between">
          {hoveredCell ? (
            <div className="flex items-center gap-4">
              <span>
                State:{" "}
                <strong className="text-white">
                  (Inventory: {hoveredCell.inv}, Days Remaining: {hoveredCell.daysLeft})
                </strong>
              </span>
              <span>
                Optimal Action:{" "}
                <strong className="text-[#ffd700] text-sm">
                  {hoveredCell.label}
                </strong>
              </span>
            </div>
          ) : (
            <span className="text-slate-500">
              Hover over any cell in the policy heatmap to inspect state-action values.
            </span>
          )}

          <span className="text-slate-400 text-[11px]">
            Policy Table: 1,581 discrete state-actions trained
          </span>
        </div>
      </div>
    </div>
  );
}
