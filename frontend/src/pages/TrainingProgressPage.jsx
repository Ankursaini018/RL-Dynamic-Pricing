import React, { useState } from "react";
import {
  LineChart,
  Cpu,
  Layers,
  Activity,
  Sliders,
  Sparkles,
  Trophy,
  Award,
  CheckCircle2,
  Database,
  ArrowRight,
  TrendingUp,
  ShieldCheck,
  Zap,
} from "lucide-react";

// Generate 61 data points from Episode 0 to 3000 (every 50 episodes)
const DETAILED_TRAINING_CURVES = Array.from({ length: 61 }, (_, i) => {
  const ep = i * 50;
  const p = ep / 3000;

  // PPO: Fast initial ascent, plateaus at $4,850 around ep 2000
  const ppoProg = Math.min(1, ep / 2000);
  const ppoSmooth = Math.round(1800 + 3050 * (1 - Math.exp(-ppoProg * 4.2)));
  const ppoRaw = Math.round(ppoSmooth + (Math.sin(ep * 13) * 140 * (1 - p * 0.5)));

  // DQN: Steady deep Q-learning ascent, reaches $4,420 around ep 2000
  const dqnProg = Math.min(1, ep / 2000);
  const dqnSmooth = Math.round(1600 + 2820 * (1 - Math.exp(-dqnProg * 3.4)));
  const dqnRaw = Math.round(dqnSmooth + (Math.cos(ep * 11) * 170 * (1 - p * 0.4)));

  // Q-Learning: Tabular updates across 3000 episodes, reaches $4,100
  const qlSmooth = Math.round(1400 + 2700 * (1 - Math.exp(-p * 3.0)));
  const qlRaw = Math.round(qlSmooth + (Math.sin(ep * 9) * 180 * (1 - p * 0.35)));

  // Epsilon decay models
  // DQN decay: reaches 0.01 by ep 1200
  const epsDQN = Math.max(0.01, Math.exp(-ep / 260)).toFixed(3);
  // Q-Learning decay: reaches 0.01 by ep 1800
  const epsQL = Math.max(0.01, Math.exp(-ep / 390)).toFixed(3);

  return {
    ep,
    ppoSmooth,
    ppoRaw,
    dqnSmooth,
    dqnRaw,
    qlSmooth,
    qlRaw,
    epsDQN: parseFloat(epsDQN),
    epsQL: parseFloat(epsQL),
  };
});

// 8 PPO Hyperparameter Configurations (Sorted by Revenue Descending)
const PPO_HYPERPARAM_TUNING = [
  {
    config: "Config #1 (Final Champion)",
    lr: "0.0005",
    clip: "0.20",
    epochs: "15",
    revenue: 4850,
    status: "BEST (Deployed) 🥇",
    isBest: true,
  },
  {
    config: "Config #2 (Default PPO)",
    lr: "0.0003",
    clip: "0.20",
    epochs: "10",
    revenue: 4680,
    status: "Strong Candidate",
    isBest: false,
  },
  {
    config: "Config #3 (Tight Clip)",
    lr: "0.0005",
    clip: "0.10",
    epochs: "10",
    revenue: 4520,
    status: "Evaluated",
    isBest: false,
  },
  {
    config: "Config #4 (High Learning Rate)",
    lr: "0.0010",
    clip: "0.20",
    epochs: "10",
    revenue: 4390,
    status: "High Variance",
    isBest: false,
  },
  {
    config: "Config #5 (Loose Clip)",
    lr: "0.0003",
    clip: "0.30",
    epochs: "15",
    revenue: 4310,
    status: "Suboptimal",
    isBest: false,
  },
  {
    config: "Config #6 (Conservative LR)",
    lr: "0.0001",
    clip: "0.20",
    epochs: "10",
    revenue: 4150,
    status: "Slow Convergence",
    isBest: false,
  },
  {
    config: "Config #7 (High LR + Loose Clip)",
    lr: "0.0010",
    clip: "0.30",
    epochs: "5",
    revenue: 3980,
    status: "Policy Instability",
    isBest: false,
  },
  {
    config: "Config #8 (Underparameterized)",
    lr: "0.0001",
    clip: "0.10",
    epochs: "5",
    revenue: 3820,
    status: "Underfitted",
    isBest: false,
  },
];

export default function TrainingProgressPage() {
  // Visibility toggles for Section 1 multi-line chart
  const [showPPO, setShowPPO] = useState(true);
  const [showDQN, setShowDQN] = useState(true);
  const [showQL, setShowQL] = useState(true);
  const [showRaw, setShowRaw] = useState(true);

  // Epsilon hover state
  const [hoveredEpPoint, setHoveredEpPoint] = useState(null);

  return (
    <div className="space-y-8 pb-16 animate-fadeIn font-sans">
      {/* ────────────────────────────────────────────────────────── */}
      {/* HEADER                                                     */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel glass-panel-gold rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-3xl">
            <div className="flex items-center gap-2 text-xs font-mono text-[#ffd700]">
              <Activity className="h-3.5 w-3.5" />
              <span>OFFLINE &amp; ONLINE REINFORCEMENT LEARNING DIAGNOSTICS</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white tracking-tight">
              Training Progress Dashboard
            </h1>
            <p className="text-sm sm:text-base text-slate-300 font-medium">
              3 Algorithms — Complete Journey
            </p>
          </div>

          <div className="flex items-center gap-2.5 shrink-0">
            <span className="rounded-xl border border-white/10 bg-black/40 px-3.5 py-2 text-xs font-mono text-slate-300 flex items-center gap-1.5 shadow-sm">
              <Cpu className="h-3.5 w-3.5 text-purple-400" />
              PyTorch 2.x // CUDA Accelerated
            </span>
          </div>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* SECTION 1: TRAINING CURVES COMPARISON (MAIN FEATURE)       */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel rounded-2xl p-6 space-y-6 border-t-2 border-t-[#ffd700]">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
              <LineChart className="h-5 w-5 text-[#ffd700]" />
              Training Curves Comparison (0 to 3,000 Episodes)
            </h2>
            <p className="text-xs font-mono text-slate-400 mt-0.5">
              Solid lines show smooth rolling average revenue; faint background lines show raw episodic variance
            </p>
          </div>

          {/* Toggle buttons to show/hide each algorithm */}
          <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
            {/* PPO Toggle */}
            <button
              onClick={() => setShowPPO(!showPPO)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border transition-all ${
                showPPO
                  ? "bg-[#ffd700]/20 border-[#ffd700] text-[#ffd700] font-bold shadow-glow-gold"
                  : "bg-black/30 border-white/10 text-slate-500 opacity-60"
              }`}
            >
              <span className="h-2 w-2 rounded-full bg-[#ffd700]" />
              <span>PPO</span>
            </button>

            {/* DQN Toggle */}
            <button
              onClick={() => setShowDQN(!showDQN)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border transition-all ${
                showDQN
                  ? "bg-[#ff6b6b]/20 border-[#ff6b6b] text-[#ff6b6b] font-bold"
                  : "bg-black/30 border-white/10 text-slate-500 opacity-60"
              }`}
            >
              <span className="h-2 w-2 rounded-full bg-[#ff6b6b]" />
              <span>DQN</span>
            </button>

            {/* Q-Learning Toggle */}
            <button
              onClick={() => setShowQL(!showQL)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border transition-all ${
                showQL
                  ? "bg-[#00e676]/20 border-[#00e676] text-[#00e676] font-bold"
                  : "bg-black/30 border-white/10 text-slate-500 opacity-60"
              }`}
            >
              <span className="h-2 w-2 rounded-full bg-[#00e676]" />
              <span>Q-Learning</span>
            </button>

            <span className="text-slate-600 hidden sm:inline">|</span>

            {/* Raw Noise Toggle */}
            <button
              onClick={() => setShowRaw(!showRaw)}
              className={`px-2.5 py-1.5 rounded-lg border text-[11px] transition-all ${
                showRaw
                  ? "bg-white/10 border-white/20 text-slate-200"
                  : "bg-black/20 border-white/5 text-slate-500"
              }`}
            >
              Raw Noise: {showRaw ? "ON" : "OFF"}
            </button>
          </div>
        </div>

        {/* Large Multi-Line SVG Chart */}
        <div className="relative h-80 sm:h-96 w-full pt-4">
          <svg className="w-full h-full overflow-visible" viewBox="0 0 780 320">
            {/* Horizontal Grid lines (Revenue $1,000 to $5,000) */}
            {[1000, 2000, 3000, 4000, 5000].map((rev) => {
              const y = 280 - ((rev - 1000) / 4200) * 240;
              return (
                <g key={rev}>
                  <line x1="55" y1={y} x2="675" y2={y} stroke="rgba(255,255,255,0.06)" strokeDasharray="4 4" />
                  <text x="45" y={y + 4} fill="#64748b" fontSize="10" fontFamily="JetBrains Mono" textAnchor="end">
                    ${rev.toLocaleString()}
                  </text>
                </g>
              );
            })}

            {/* X-Axis Episode markers (0 to 3000) */}
            {[0, 500, 1000, 1500, 2000, 2500, 3000].map((ep) => {
              const x = 55 + (ep / 3000) * 620;
              return (
                <g key={ep}>
                  <line x1={x} y1="278" x2={x} y2="284" stroke="#64748b" />
                  <text x={x} y="302" fill="#94a3b8" fontSize="10" fontFamily="JetBrains Mono" textAnchor="middle">
                    Ep {ep}
                  </text>
                </g>
              );
            })}

            {/* ── RAW DATA NOISY CURVES (Very transparent behind) ── */}
            {showRaw && (
              <>
                {/* Q-Learning Raw */}
                {showQL && (
                  <polyline
                    fill="none"
                    stroke="#00e676"
                    strokeWidth="1"
                    strokeOpacity="0.18"
                    points={DETAILED_TRAINING_CURVES.map((pt) => {
                      const x = 55 + (pt.ep / 3000) * 620;
                      const y = 280 - ((pt.qlRaw - 1000) / 4200) * 240;
                      return `${x},${y}`;
                    }).join(" ")}
                  />
                )}
                {/* DQN Raw */}
                {showDQN && (
                  <polyline
                    fill="none"
                    stroke="#ff6b6b"
                    strokeWidth="1"
                    strokeOpacity="0.18"
                    points={DETAILED_TRAINING_CURVES.map((pt) => {
                      const x = 55 + (pt.ep / 3000) * 620;
                      const y = 280 - ((pt.dqnRaw - 1000) / 4200) * 240;
                      return `${x},${y}`;
                    }).join(" ")}
                  />
                )}
                {/* PPO Raw */}
                {showPPO && (
                  <polyline
                    fill="none"
                    stroke="#ffd700"
                    strokeWidth="1"
                    strokeOpacity="0.22"
                    points={DETAILED_TRAINING_CURVES.map((pt) => {
                      const x = 55 + (pt.ep / 3000) * 620;
                      const y = 280 - ((pt.ppoRaw - 1000) / 4200) * 240;
                      return `${x},${y}`;
                    }).join(" ")}
                  />
                )}
              </>
            )}

            {/* ── SMOOTH ROLLING AVERAGE LINES ── */}
            {/* Q-Learning Smooth (Green) */}
            {showQL && (
              <polyline
                fill="none"
                stroke="#00e676"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={DETAILED_TRAINING_CURVES.map((pt) => {
                  const x = 55 + (pt.ep / 3000) * 620;
                  const y = 280 - ((pt.qlSmooth - 1000) / 4200) * 240;
                  return `${x},${y}`;
                }).join(" ")}
              />
            )}

            {/* DQN Smooth (Coral) */}
            {showDQN && (
              <polyline
                fill="none"
                stroke="#ff6b6b"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={DETAILED_TRAINING_CURVES.map((pt) => {
                  const x = 55 + (pt.ep / 3000) * 620;
                  const y = 280 - ((pt.dqnSmooth - 1000) / 4200) * 240;
                  return `${x},${y}`;
                }).join(" ")}
              />
            )}

            {/* PPO Smooth (Gold) - Highest Final Value */}
            {showPPO && (
              <polyline
                fill="none"
                stroke="#ffd700"
                strokeWidth="3.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={DETAILED_TRAINING_CURVES.map((pt) => {
                  const x = 55 + (pt.ep / 3000) * 620;
                  const y = 280 - ((pt.ppoSmooth - 1000) / 4200) * 240;
                  return `${x},${y}`;
                }).join(" ")}
                style={{
                  filter: "drop-shadow(0 0 8px rgba(255, 215, 0, 0.45))",
                }}
              />
            )}

            {/* ── FINAL VALUE ANNOTATIONS ON RIGHT ── */}
            {/* PPO: $4,850 → 🥇 */}
            {showPPO && (
              <g transform="translate(685, 55)">
                <rect x="0" y="-12" width="90" height="24" rx="6" fill="#ffd700" fillOpacity="0.15" stroke="#ffd700" strokeWidth="1.2" />
                <text x="8" y="4" fill="#ffd700" fontSize="10" fontFamily="JetBrains Mono" fontWeight="bold">
                  $4,850 → 🥇
                </text>
              </g>
            )}

            {/* DQN: $4,420 → 🥈 */}
            {showDQN && (
              <g transform="translate(685, 85)">
                <rect x="0" y="-12" width="90" height="24" rx="6" fill="#ff6b6b" fillOpacity="0.15" stroke="#ff6b6b" strokeWidth="1.2" />
                <text x="8" y="4" fill="#ff6b6b" fontSize="10" fontFamily="JetBrains Mono" fontWeight="bold">
                  $4,420 → 🥈
                </text>
              </g>
            )}

            {/* QL: $4,100 → 🥉 */}
            {showQL && (
              <g transform="translate(685, 115)">
                <rect x="0" y="-12" width="90" height="24" rx="6" fill="#00e676" fillOpacity="0.15" stroke="#00e676" strokeWidth="1.2" />
                <text x="8" y="4" fill="#00e676" fontSize="10" fontFamily="JetBrains Mono" fontWeight="bold">
                  $4,100 → 🥉
                </text>
              </g>
            )}
          </svg>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* SECTION 2: THREE TRAINING DETAIL CARDS (ONE PER ALGORITHM) */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="space-y-4">
        <div className="border-b border-white/10 pb-3">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400 uppercase tracking-wider mb-1">
            <span>Section 2</span>
            <span>•</span>
            <span>Algorithm Architectural Details</span>
          </div>
          <h2 className="text-lg sm:text-xl font-bold text-white">
            Algorithm Training Specifications
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* PPO CARD (GOLD THEME) */}
          <div className="glass-panel glass-panel-gold rounded-2xl p-6 border-t-4 border-t-[#ffd700] shadow-glow-gold flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-bold text-[#ffd700] flex items-center gap-1.5 uppercase tracking-wider">
                  <Trophy className="h-4 w-4" />
                  PPO (CHAMPION)
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#ffd700]/20 text-[#ffd700] border border-[#ffd700]/30 font-bold">
                  Rank #1
                </span>
              </div>

              <h3 className="text-xl font-bold text-white font-mono">
                $4,850 <span className="text-xs text-slate-400 font-normal">Final Yield</span>
              </h3>

              {/* Specs List */}
              <div className="mt-4 space-y-2 text-xs font-mono">
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Algorithm:</span>
                  <span className="text-white font-semibold">Actor-Critic</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Episodes:</span>
                  <span className="text-white font-bold">2,000 eps</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Architecture:</span>
                  <span className="text-[#ffd700] font-bold">2 → 128 → 64 → 6</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Key Mechanism:</span>
                  <span className="text-white font-semibold">Clipping ε = 0.2</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-400">Best LR:</span>
                  <span className="text-emerald-400 font-bold">0.0005</span>
                </div>
              </div>
            </div>

            {/* Mini Training Curve */}
            <div className="pt-2">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block mb-1">
                Convergence Mini Curve:
              </span>
              <div className="h-12 w-full bg-black/40 rounded p-1 border border-white/5">
                <svg className="w-full h-full" viewBox="0 0 200 40">
                  <polyline
                    fill="none"
                    stroke="#ffd700"
                    strokeWidth="2"
                    points={DETAILED_TRAINING_CURVES.filter((_, i) => i % 3 === 0)
                      .map((pt, i, arr) => {
                        const x = (i / (arr.length - 1)) * 200;
                        const y = 35 - ((pt.ppoSmooth - 1800) / 3200) * 30;
                        return `${x},${y}`;
                      })
                      .join(" ")}
                  />
                </svg>
              </div>
            </div>
          </div>

          {/* DQN CARD (CORAL THEME) */}
          <div className="glass-panel rounded-2xl p-6 border-t-4 border-t-[#ff6b6b] flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-bold text-[#ff6b6b] flex items-center gap-1.5 uppercase tracking-wider">
                  <Cpu className="h-4 w-4" />
                  DQN (RUNNER UP)
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#ff6b6b]/20 text-[#ff6b6b] border border-[#ff6b6b]/30 font-bold">
                  Rank #2
                </span>
              </div>

              <h3 className="text-xl font-bold text-white font-mono">
                $4,420 <span className="text-xs text-slate-400 font-normal">Final Yield</span>
              </h3>

              {/* Specs List */}
              <div className="mt-4 space-y-2 text-xs font-mono">
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Algorithm:</span>
                  <span className="text-white font-semibold">Value-based</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Episodes:</span>
                  <span className="text-white font-bold">2,000 eps</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Buffer Size:</span>
                  <span className="text-white font-semibold">10,000 experiences</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Batch Size:</span>
                  <span className="text-white font-semibold">64 transitions</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-400">Target Update:</span>
                  <span className="text-[#ff6b6b] font-bold">every 10 eps</span>
                </div>
              </div>
            </div>

            {/* Mini Training Curve */}
            <div className="pt-2">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block mb-1">
                Convergence Mini Curve:
              </span>
              <div className="h-12 w-full bg-black/40 rounded p-1 border border-white/5">
                <svg className="w-full h-full" viewBox="0 0 200 40">
                  <polyline
                    fill="none"
                    stroke="#ff6b6b"
                    strokeWidth="2"
                    points={DETAILED_TRAINING_CURVES.filter((_, i) => i % 3 === 0)
                      .map((pt, i, arr) => {
                        const x = (i / (arr.length - 1)) * 200;
                        const y = 35 - ((pt.dqnSmooth - 1600) / 3000) * 30;
                        return `${x},${y}`;
                      })
                      .join(" ")}
                  />
                </svg>
              </div>
            </div>
          </div>

          {/* Q-LEARNING CARD (GREEN THEME) */}
          <div className="glass-panel rounded-2xl p-6 border-t-4 border-t-[#00e676] flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-bold text-[#00e676] flex items-center gap-1.5 uppercase tracking-wider">
                  <Layers className="h-4 w-4" />
                  Q-LEARNING (TABULAR)
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/30 font-bold">
                  Rank #3
                </span>
              </div>

              <h3 className="text-xl font-bold text-white font-mono">
                $4,100 <span className="text-xs text-slate-400 font-normal">Final Yield</span>
              </h3>

              {/* Specs List */}
              <div className="mt-4 space-y-2 text-xs font-mono">
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Algorithm:</span>
                  <span className="text-white font-semibold">Tabular TD</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Episodes:</span>
                  <span className="text-white font-bold">3,000 eps</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Q-Table Capacity:</span>
                  <span className="text-emerald-400 font-bold">9,486 entries</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-slate-400">Hyperparameters:</span>
                  <span className="text-white font-semibold">α = 0.10, γ = 0.99</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-400">Epsilon Schedule:</span>
                  <span className="text-white font-semibold">1.0 → 0.01</span>
                </div>
              </div>
            </div>

            {/* Mini Training Curve */}
            <div className="pt-2">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block mb-1">
                Convergence Mini Curve:
              </span>
              <div className="h-12 w-full bg-black/40 rounded p-1 border border-white/5">
                <svg className="w-full h-full" viewBox="0 0 200 40">
                  <polyline
                    fill="none"
                    stroke="#00e676"
                    strokeWidth="2"
                    points={DETAILED_TRAINING_CURVES.filter((_, i) => i % 3 === 0)
                      .map((pt, i, arr) => {
                        const x = (i / (arr.length - 1)) * 200;
                        const y = 35 - ((pt.qlSmooth - 1400) / 2800) * 30;
                        return `${x},${y}`;
                      })
                      .join(" ")}
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* SECTION 3: HYPERPARAMETER TUNING RESULTS (TABLE)           */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel rounded-2xl p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
          <div>
            <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              <Sliders className="h-5 w-5 text-[#ffd700]" />
              PPO Hyperparameter Tuning Grid Search
            </h3>
            <p className="text-xs font-mono text-slate-400">
              Comparative analysis across 8 parameter sweeps; sorted by mean revenue descending
            </p>
          </div>

          <div className="text-xs font-mono text-slate-300 bg-white/5 border border-white/10 px-3 py-1.5 rounded-lg">
            Optimum: LR = 0.0005 | Clip = 0.20 | Epochs = 15
          </div>
        </div>

        {/* 8 PPO Configurations Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 uppercase tracking-wider text-[11px]">
                <th className="py-3 px-4">Configuration</th>
                <th className="py-3 px-4">Learning Rate (LR)</th>
                <th className="py-3 px-4">Clip (ε)</th>
                <th className="py-3 px-4">Epochs</th>
                <th className="py-3 px-4">Mean Revenue</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {PPO_HYPERPARAM_TUNING.map((cfg) => (
                <tr
                  key={cfg.config}
                  className={`transition-colors duration-150 ${
                    cfg.isBest
                      ? "bg-[#ffd700]/15 border-l-4 border-l-[#ffd700] hover:bg-[#ffd700]/20 font-semibold"
                      : "hover:bg-white/[0.03]"
                  }`}
                >
                  <td className="py-3.5 px-4 flex items-center gap-2">
                    {cfg.isBest && <Sparkles className="h-3.5 w-3.5 text-[#ffd700] shrink-0" />}
                    <span className={cfg.isBest ? "text-[#ffd700] font-bold text-sm" : "text-white"}>
                      {cfg.config}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-300">{cfg.lr}</td>
                  <td className="py-3.5 px-4 text-slate-300">{cfg.clip}</td>
                  <td className="py-3.5 px-4 text-slate-300">{cfg.epochs}</td>
                  <td className="py-3.5 px-4 font-mono font-bold text-sm text-white">
                    <span className={cfg.isBest ? "text-[#ffd700]" : ""}>
                      ${cfg.revenue.toLocaleString()}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${
                        cfg.isBest
                          ? "bg-[#ffd700]/25 text-[#ffd700] border border-[#ffd700]/50"
                          : "bg-white/5 text-slate-400 border border-white/10"
                      }`}
                    >
                      {cfg.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* SECTION 4: EPSILON DECAY CHART                             */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel glass-panel-purple rounded-2xl p-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
          <div>
            <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              <Zap className="h-5 w-5 text-purple-400" />
              Epsilon Exploration Decay (ε: 1.0 → 0.01)
            </h3>
            <p className="text-xs font-mono text-slate-400">
              Tracking the systematic shift from random market exploration to pure policy exploitation
            </p>
          </div>

          {/* Legend */}
          <div className="flex items-center gap-4 text-xs font-mono">
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-[#ff6b6b]" />
              <span className="text-slate-300">DQN ε-Decay</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-[#00e676]" />
              <span className="text-slate-300">Q-Learning ε-Decay</span>
            </div>
          </div>
        </div>

        {/* Epsilon Decay SVG with 3 Labeled Phase Zones */}
        <div className="relative h-72 sm:h-80 w-full pt-4">
          <svg className="w-full h-full overflow-visible" viewBox="0 0 760 260">
            {/* 3 Labeled Phase Zones along X-Axis */}
            {/* Zone 1: Exploration Phase (0 to 400 eps) */}
            <rect
              x="50"
              y="20"
              width={(400 / 3000) * 650}
              height="200"
              fill="rgba(156, 39, 176, 0.08)"
              stroke="rgba(156, 39, 176, 0.25)"
              strokeDasharray="4 4"
            />
            <text
              x={50 + (200 / 3000) * 650}
              y="38"
              fill="#ba68c8"
              fontSize="10"
              fontFamily="JetBrains Mono"
              textAnchor="middle"
              fontWeight="bold"
            >
              Exploration Phase
            </text>

            {/* Zone 2: Transition Phase (400 to 1200 eps) */}
            <rect
              x={50 + (400 / 3000) * 650}
              y="20"
              width={(800 / 3000) * 650}
              height="200"
              fill="rgba(100, 181, 246, 0.06)"
              stroke="rgba(100, 181, 246, 0.25)"
              strokeDasharray="4 4"
            />
            <text
              x={50 + (800 / 3000) * 650}
              y="38"
              fill="#64b5f6"
              fontSize="10"
              fontFamily="JetBrains Mono"
              textAnchor="middle"
              fontWeight="bold"
            >
              Transition Phase
            </text>

            {/* Zone 3: Exploitation Phase (1200 to 3000 eps) */}
            <rect
              x={50 + (1200 / 3000) * 650}
              y="20"
              width={(1800 / 3000) * 650}
              height="200"
              fill="rgba(0, 230, 118, 0.06)"
              stroke="rgba(0, 230, 118, 0.25)"
              strokeDasharray="4 4"
            />
            <text
              x={50 + (2100 / 3000) * 650}
              y="38"
              fill="#00e676"
              fontSize="10"
              fontFamily="JetBrains Mono"
              textAnchor="middle"
              fontWeight="bold"
            >
              Exploitation Phase (Greedy Actions)
            </text>

            {/* Horizontal Grid lines (Epsilon 0.0 to 1.0) */}
            {[0.0, 0.25, 0.5, 0.75, 1.0].map((val) => {
              const y = 220 - val * 180;
              return (
                <g key={val}>
                  <line x1="50" y1={y} x2="700" y2={y} stroke="rgba(255,255,255,0.06)" strokeDasharray="3 3" />
                  <text x="42" y={y + 4} fill="#64748b" fontSize="10" fontFamily="JetBrains Mono" textAnchor="end">
                    {val.toFixed(2)}
                  </text>
                </g>
              );
            })}

            {/* X-Axis Episode markers */}
            {[0, 500, 1000, 1500, 2000, 2500, 3000].map((ep) => {
              const x = 50 + (ep / 3000) * 650;
              return (
                <g key={ep}>
                  <line x1={x} y1="218" x2={x} y2="224" stroke="#64748b" />
                  <text x={x} y="244" fill="#94a3b8" fontSize="10" fontFamily="JetBrains Mono" textAnchor="middle">
                    Ep {ep}
                  </text>
                </g>
              );
            })}

            {/* Q-Learning Epsilon Curve (Green) */}
            <polyline
              fill="none"
              stroke="#00e676"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={DETAILED_TRAINING_CURVES.map((pt) => {
                const x = 50 + (pt.ep / 3000) * 650;
                const y = 220 - pt.epsQL * 180;
                return `${x},${y}`;
              }).join(" ")}
            />

            {/* DQN Epsilon Curve (Coral) */}
            <polyline
              fill="none"
              stroke="#ff6b6b"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={DETAILED_TRAINING_CURVES.map((pt) => {
                const x = 50 + (pt.ep / 3000) * 650;
                const y = 220 - pt.epsDQN * 180;
                return `${x},${y}`;
              }).join(" ")}
            />

            {/* End Point Markers */}
            <circle cx={50 + 650} cy={220 - 0.01 * 180} r="4" fill="#00e676" />
            <circle cx={50 + (1200 / 3000) * 650} cy={220 - 0.01 * 180} r="4" fill="#ff6b6b" />
          </svg>
        </div>

        {/* Bottom Explanatory Row */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 text-xs font-mono text-slate-300">
          <div className="p-3 bg-black/40 rounded-xl border border-white/5 space-y-1">
            <span className="text-[#ba68c8] font-bold block">1. Exploration (Ep 0–400)</span>
            <p className="text-[11px] text-slate-400 leading-snug">
              High ε allows agents to randomly sample all 6 price levels across all 50 inventory states.
            </p>
          </div>

          <div className="p-3 bg-black/40 rounded-xl border border-white/5 space-y-1">
            <span className="text-[#64b5f6] font-bold block">2. Transition (Ep 400–1200)</span>
            <p className="text-[11px] text-slate-400 leading-snug">
              Gradual exponential annealing balances exploring undiscovered states against exploiting known high-yield actions.
            </p>
          </div>

          <div className="p-3 bg-black/40 rounded-xl border border-white/5 space-y-1">
            <span className="text-emerald-400 font-bold block">3. Exploitation (Ep 1200+)</span>
            <p className="text-[11px] text-slate-400 leading-snug">
              Fixed ε = 0.01 locks policy into optimal price recommendations with minimal random perturbations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
