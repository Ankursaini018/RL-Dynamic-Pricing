import React, { useState } from "react";
import { Info, Sparkles, Cpu, Layers } from "lucide-react";

export const AGENT_SPECS = {
  PPO: {
    name: "PPO (Proximal Policy Optimization)",
    type: "Policy-Based Deep RL (Actor-Critic)",
    architecture: "2 → 128 → 64 → Actor & Critic Heads (PyTorch)",
    keyFeature: "Clipping (ε=0.2), GAE (λ=0.95), Deadline Discounting & Scarcity Surges",
    color: "#ffd700",
    badge: "CHAMPION 🥇",
  },
  DQN: {
    name: "DQN (Deep Q-Network)",
    type: "Value-Based Deep RL",
    architecture: "2 → 128 → 64 → 6 Action Q-Values",
    keyFeature: "Experience Replay Buffer (10,000), Target Network Update every 10 eps, MSE Bellman Loss",
    color: "#ff6b6b",
    badge: "RUNNER UP 🥈",
  },
  "Q-Learning": {
    name: "Q-Learning (Tabular)",
    type: "Tabular Reinforcement Learning",
    architecture: "Discrete Q-Table (51 × 31 × 6 = 9,486 values)",
    keyFeature: "Bellman TD Updates (α=0.10, γ=0.99), annealed ε-greedy exploration",
    color: "#00e676",
    badge: "TABULAR 🥉",
  },
  "Time Based": {
    name: "Time Based Strategy",
    type: "Calendar Heuristic Baseline",
    architecture: "Monotonic Step Function",
    keyFeature: "Stairs prices from $50 up to $300 naively by day, ignoring inventory",
    color: "#64b5f6",
    badge: "HEURISTIC",
  },
  "Fixed Price": {
    name: "Fixed Price Strategy",
    type: "Static Baseline Heuristic",
    architecture: "Invariant Constant ($150)",
    keyFeature: "Flat baseline ignoring demand, inventory burn rate, and expiry penalties",
    color: "#94a3b8",
    badge: "STATIC",
  },
  "Linear Decay": {
    name: "Linear Decay Strategy",
    type: "Markdown Heuristic",
    architecture: "Linear Markdown Function",
    keyFeature: "Uniform daily discount schedule dropping from $300 down to $50",
    color: "#fb923c",
    badge: "DISCOUNT",
  },
  "Demand Based": {
    name: "Demand Based Strategy",
    type: "Inventory Threshold Heuristic",
    architecture: "Binary Threshold (25 items)",
    keyFeature: "Flips price between $100 and $250 based only on remaining stock threshold",
    color: "#ba68c8",
    badge: "THRESHOLD",
  },
};

export default function AgentTooltip({ agentName, children, className = "" }) {
  const [isVisible, setIsVisible] = useState(false);
  const specKey = Object.keys(AGENT_SPECS).find((k) =>
    agentName?.toLowerCase().includes(k.toLowerCase())
  );
  const spec = specKey ? AGENT_SPECS[specKey] : null;

  if (!spec) {
    return <span className={className}>{children || agentName}</span>;
  }

  return (
    <span
      className={`relative inline-flex items-center cursor-pointer group ${className}`}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children || (
        <span className="hover:underline flex items-center gap-1 font-semibold">
          {agentName}
        </span>
      )}

      {/* Floating Tooltip with Smooth Fade In */}
      {isVisible && (
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-72 p-3.5 rounded-xl bg-[#0f0f22]/95 border border-white/20 backdrop-blur-xl shadow-2xl z-50 pointer-events-none text-left animate-fadeIn">
          {/* Top arrow */}
          <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-[#0f0f22]" />

          <div className="flex items-center justify-between pb-1.5 border-b border-white/10 mb-2">
            <span
              className="text-xs font-mono font-bold flex items-center gap-1.5"
              style={{ color: spec.color }}
            >
              <Sparkles className="h-3 w-3" />
              {spec.name}
            </span>
            <span
              className="text-[9px] font-mono px-1.5 py-0.5 rounded font-bold"
              style={{
                backgroundColor: `${spec.color}25`,
                color: spec.color,
                border: `1px solid ${spec.color}50`,
              }}
            >
              {spec.badge}
            </span>
          </div>

          <div className="space-y-1.5 text-[11px] font-mono text-slate-300">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Type:</span>
              <span className="text-white font-medium">{spec.type}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Architecture:</span>
              <span className="text-[#ffd700]" style={{ color: spec.color }}>
                {spec.architecture}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Key Feature:</span>
              <span className="text-slate-300 text-[10px] leading-tight block">
                {spec.keyFeature}
              </span>
            </div>
          </div>
        </div>
      )}
    </span>
  );
}
