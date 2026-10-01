import React, { useState, useEffect } from "react";
import {
  Crown,
  Trophy,
  Swords,
  Play,
  Pause,
  RotateCcw,
  FastForward,
  TrendingUp,
  Zap,
  Sparkles,
  ShieldCheck,
  Cpu,
  Layers,
  Activity,
  CheckCircle2,
  AlertCircle,
  Clock,
  ArrowRight,
  Flame,
} from "lucide-react";
import confetti from "canvas-confetti";
import { LEADERBOARD_DATA, AGENT_COLORS, runSimulationStep } from "../data/simulationData";

// Detailed 7 agents configuration for the Arena
const ALL_7_AGENTS = [
  {
    id: "PPO",
    name: "PPO",
    type: "Actor-Critic RL",
    color: "#ffd700",
    meanRevenue: 4850,
    stdRevenue: 210.5,
    maxRevenue: 5240,
    sellThrough: 96.2,
    winRate: 46.8,
    badge: "CHAMPION",
    subtitle: "ChatGPT Algorithm",
    defaultStatus: "Active",
    isPPO: true,
  },
  {
    id: "DQN",
    name: "DQN",
    type: "Deep Q-Network",
    color: "#ff6b6b",
    meanRevenue: 4420,
    stdRevenue: 245.0,
    maxRevenue: 4880,
    sellThrough: 93.4,
    winRate: 28.4,
    badge: "Runner Up",
    subtitle: "Deep Value Approximation",
    defaultStatus: "Active",
    isDQN: true,
  },
  {
    id: "Q-Learning",
    name: "Q-Learning",
    type: "Tabular Q-Learning",
    color: "#00e676",
    meanRevenue: 4280,
    stdRevenue: 260.2,
    maxRevenue: 4710,
    sellThrough: 91.8,
    winRate: 14.6,
    badge: "3rd Place 🥉",
    subtitle: "Bellman Temporal Difference",
    defaultStatus: "Active",
  },
  {
    id: "Time Based",
    name: "Time Based",
    type: "Heuristic Baseline",
    color: "#64b5f6",
    meanRevenue: 4120,
    stdRevenue: 285.4,
    maxRevenue: 4520,
    sellThrough: 82.6,
    winRate: 6.2,
    badge: "Best Heuristic",
    subtitle: "Calendar Step Pacing",
    defaultStatus: "Active",
  },
  {
    id: "Fixed Price",
    name: "Fixed Price",
    type: "Static Heuristic",
    color: "#94a3b8",
    meanRevenue: 3890,
    stdRevenue: 240.0,
    maxRevenue: 4300,
    sellThrough: 78.4,
    winRate: 2.1,
    badge: "Static Baseline",
    subtitle: "Constant $150 Price",
    defaultStatus: "Watching",
  },
  {
    id: "Linear Decay",
    name: "Linear Decay",
    type: "Discount Heuristic",
    color: "#fb923c",
    meanRevenue: 3740,
    stdRevenue: 270.8,
    maxRevenue: 4180,
    sellThrough: 85.0,
    winRate: 1.4,
    badge: "Decay Rule",
    subtitle: "Linear Day Markdown",
    defaultStatus: "Watching",
  },
  {
    id: "Demand Based",
    name: "Demand Based",
    type: "Inventory Heuristic",
    color: "#ba68c8",
    meanRevenue: 3460,
    stdRevenue: 310.0,
    maxRevenue: 3950,
    sellThrough: 71.5,
    winRate: 0.5,
    badge: "Threshold Rule",
    subtitle: "Binary Inventory Switch",
    defaultStatus: "Watching",
  },
];

// Generate 20 baseline historical season revenues for mini sparklines
const generateInitialSparklines = () => {
  const result = {};
  ALL_7_AGENTS.forEach((agent) => {
    const points = [];
    for (let i = 0; i < 20; i++) {
      const variation = (Math.sin(i * 1.7 + agent.name.length) * 0.8 + Math.cos(i * 0.9) * 0.4) * agent.stdRevenue;
      points.push(Math.round(agent.meanRevenue + variation));
    }
    result[agent.id] = points;
  });
  return result;
};

export default function AgentArenaPage() {
  // Simulation Controller State
  const [isPlaying, setIsPlaying] = useState(false);
  const [speedMultiplier, setSpeedMultiplier] = useState(1); // 1x, 5x, 10x
  const [simDay, setSimDay] = useState(1);
  const [seasonIndex, setSeasonIndex] = useState(1001);

  // Live simulation states for all 7 agents
  const [agentLiveRevenues, setAgentLiveRevenues] = useState(() => {
    const initial = {};
    ALL_7_AGENTS.forEach((a) => {
      initial[a.id] = Math.round(a.meanRevenue);
    });
    return initial;
  });

  const [agentStatuses, setAgentStatuses] = useState(() => {
    const initial = {};
    ALL_7_AGENTS.forEach((a) => {
      initial[a.id] = a.defaultStatus;
    });
    return initial;
  });

  const [sparklines, setSparklines] = useState(generateInitialSparklines);

  // Head to Head Battle State
  const [agentA, setAgentA] = useState("PPO");
  const [agentB, setAgentB] = useState("Time Based");
  const [isFighting, setIsFighting] = useState(false);
  const [fightOutcome, setFightOutcome] = useState(null);

  // Toggle agent status badge (Active vs Watching)
  const toggleAgentStatus = (agentId) => {
    setAgentStatuses((prev) => ({
      ...prev,
      [agentId]: prev[agentId] === "Active" ? "Watching" : "Active",
    }));
  };

  // Speed mapping in milliseconds
  const speedInterval = speedMultiplier === 1 ? 400 : speedMultiplier === 5 ? 120 : 40;

  // Run Simulation Tick Loop
  useEffect(() => {
    let timer;
    if (isPlaying) {
      timer = setInterval(() => {
        setSimDay((prevDay) => {
          if (prevDay >= 30) {
            // Season completed!
            setIsPlaying(false);

            // Append new season results to sparklines
            setSparklines((prevSpark) => {
              const updated = { ...prevSpark };
              ALL_7_AGENTS.forEach((a) => {
                const currentVal = agentLiveRevenues[a.id];
                updated[a.id] = [...(updated[a.id] || []).slice(1), currentVal];
              });
              return updated;
            });

            // Trigger confetti if PPO is the winner (which it is!)
            confetti({
              particleCount: 100,
              spread: 80,
              origin: { y: 0.6 },
              colors: ["#ffd700", "#ff6b6b", "#00e676", "#9c27b0"],
            });

            return 30;
          }

          const nextDay = prevDay + 1;

          // Increment revenues incrementally as days advance
          setAgentLiveRevenues((prevRevs) => {
            const next = { ...prevRevs };
            ALL_7_AGENTS.forEach((a) => {
              if (agentStatuses[a.id] === "Active") {
                // Calculate incremental daily ticket sales based on agent quality
                const dailyExpectation = (a.meanRevenue / 30);
                const noise = (Math.random() - 0.45) * 45;
                next[a.id] = Math.max(0, Math.round(prevRevs[a.id] + dailyExpectation * (1/30) * 8 + noise));
              }
            });
            return next;
          });

          return nextDay;
        });
      }, speedInterval);
    }
    return () => clearInterval(timer);
  }, [isPlaying, speedInterval, agentStatuses, agentLiveRevenues]);

  // Start new simulation run
  const handleRunSimulation = () => {
    setSimDay(1);
    setSeasonIndex((s) => s + 1);

    // Reset starting revenues for season race
    const freshRevs = {};
    ALL_7_AGENTS.forEach((a) => {
      freshRevs[a.id] = Math.round(a.meanRevenue * 0.1);
    });
    setAgentLiveRevenues(freshRevs);
    setIsPlaying(true);
  };

  // Reset to static final means
  const handleReset = () => {
    setIsPlaying(false);
    setSimDay(1);
    const defaults = {};
    ALL_7_AGENTS.forEach((a) => {
      defaults[a.id] = Math.round(a.meanRevenue);
    });
    setAgentLiveRevenues(defaults);
  };

  // Trigger Head-to-Head Fight Animation
  const handleTriggerFight = () => {
    setIsFighting(true);
    setFightOutcome(null);

    setTimeout(() => {
      setIsFighting(false);
      const dataA = ALL_7_AGENTS.find((a) => a.id === agentA);
      const dataB = ALL_7_AGENTS.find((a) => a.id === agentB);

      const aWins = dataA.meanRevenue >= dataB.meanRevenue;
      const winner = aWins ? dataA : dataB;
      const loser = aWins ? dataB : dataA;
      const lift = (((winner.meanRevenue - loser.meanRevenue) / loser.meanRevenue) * 100).toFixed(1);

      setFightOutcome({
        winner: winner.id,
        loser: loser.id,
        lift,
        isPPOWinner: winner.id === "PPO",
        pVal: "p < 0.05",
      });

      // Confetti animation when PPO wins
      if (winner.id === "PPO") {
        confetti({
          particleCount: 90,
          spread: 70,
          origin: { y: 0.75 },
          colors: ["#ffd700", "#ffe55c", "#00e676", "#9c27b0"],
        });
      }
    }, 650);
  };

  // Fetch selected agent data for Head-to-Head
  const selectedDataA = ALL_7_AGENTS.find((a) => a.id === agentA) || ALL_7_AGENTS[0];
  const selectedDataB = ALL_7_AGENTS.find((a) => a.id === agentB) || ALL_7_AGENTS[3];

  return (
    <div className="space-y-8 pb-16 animate-fadeIn font-sans">
      {/* ────────────────────────────────────────────────────────── */}
      {/* ARENA HEADER BAND                                          */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel glass-panel-gold rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-5">
          <div className="space-y-1.5">
            <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-[#ffd700]/15 px-3 py-1 font-semibold text-[#ffd700] border border-[#ffd700]/30 shadow-glow-gold">
                <Swords className="h-3.5 w-3.5 text-[#ffd700]" />
                AGENT ARENA — LIVE COMPETITION
              </span>
              <span className="rounded-full bg-purple-500/15 text-purple-300 px-3 py-1 border border-purple-500/30">
                1000 Seasons | Statistical Proof
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Multi-Agent Live Pricing Arena
            </h1>
            <p className="text-xs sm:text-sm text-slate-300">
              Watch all 7 reinforcement learning and heuristic pricing algorithms battle in real-time under identical market conditions.
            </p>
          </div>

          {/* Action Controls: Run Simulation (Gold Gradient) & Speed Controls */}
          <div className="flex flex-wrap items-center gap-3 shrink-0">
            {/* Run Simulation Button (Gold Gradient) */}
            <button
              onClick={isPlaying ? () => setIsPlaying(false) : handleRunSimulation}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#ffd700] via-[#ffe55c] to-[#ffd700] text-black text-xs sm:text-sm font-mono font-bold shadow-glow-gold hover:opacity-95 transition-all transform active:scale-95"
            >
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              <span>{isPlaying ? "PAUSE SIMULATION" : "RUN SIMULATION"}</span>
            </button>

            {/* Speed Control: 1x / 5x / 10x */}
            <div className="flex items-center gap-1 bg-black/50 border border-white/10 p-1 rounded-xl text-xs font-mono">
              <span className="text-slate-400 px-2 hidden sm:inline">Speed:</span>
              {[1, 5, 10].map((s) => (
                <button
                  key={s}
                  onClick={() => setSpeedMultiplier(s)}
                  className={`px-2.5 py-1 rounded-lg transition-all ${
                    speedMultiplier === s
                      ? "bg-[#ffd700] text-black font-bold shadow-glow-gold"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  {s}x
                </button>
              ))}
            </div>

            {/* Reset Button */}
            <button
              onClick={handleReset}
              className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white border border-white/10 transition-all"
              title="Reset Arena"
            >
              <RotateCcw className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Live Arena Season & Day Status Tracker */}
        <div className="mt-5 pt-4 border-t border-white/10 flex flex-wrap items-center justify-between text-xs font-mono gap-3">
          <div className="flex items-center gap-2">
            <span className="text-slate-400">ACTIVE ARENA MATCH:</span>
            <span className="text-white font-bold">Season #{seasonIndex}</span>
            <span className="text-slate-500">|</span>
            <span className="text-[#ffd700] font-bold">Day {simDay} / 30</span>
            {simDay >= 25 && (
              <span className="flex items-center gap-1 text-red-400 font-bold bg-red-500/10 px-2 py-0.5 rounded border border-red-500/30 text-[10px] animate-pulse">
                <Flame className="h-3 w-3" />
                DEADLINE DISCOUNTING ZONE
              </span>
            )}
          </div>

          <div className="text-slate-400 text-[11px] flex items-center gap-1">
            <Activity className="h-3.5 w-3.5 text-emerald-400" />
            <span>7 Autonomous Policies Synchronized</span>
          </div>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* MAIN ARENA SECTION: 7 AGENT CARDS IN A GRID (3-3-1)        */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="space-y-5">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 px-1">
          <span>COMPETING AGENTS SPECTRUM (7)</span>
          <span>Click status badge to toggle Active / Watching</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {/* ─────────────────── ROW 1: 3 CARDS ─────────────────── */}

          {/* CARD 1: SPECIAL PPO CARD (LARGER, GOLD) */}
          <div className="lg:col-span-1 rounded-2xl glass-panel glass-panel-gold border-2 border-[#ffd700] p-6 relative overflow-hidden shadow-glow-gold animate-gold-glow-border flex flex-col justify-between">
            {/* Top decorative badge & Crown */}
            <div>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-xl bg-[#ffd700]/20 text-[#ffd700] border border-[#ffd700]/40 shadow-sm">
                    <Crown className="h-6 w-6 text-[#ffd700]" />
                  </div>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <h3 className="text-xl font-bold text-white tracking-tight">PPO</h3>
                      <span className="rounded bg-[#ffd700] px-2 py-0.5 text-[10px] font-mono font-bold text-black uppercase tracking-wider">
                        CHAMPION
                      </span>
                    </div>
                    {/* "ChatGPT Algorithm" subtitle tag */}
                    <div className="text-[11px] font-mono text-[#ffd700] font-semibold flex items-center gap-1 mt-0.5">
                      <Sparkles className="h-3 w-3" />
                      ChatGPT Algorithm
                    </div>
                  </div>
                </div>

                {/* Status Badge */}
                <button
                  onClick={() => toggleAgentStatus("PPO")}
                  className={`text-[10px] font-mono px-2.5 py-1 rounded-full font-bold transition-all ${
                    agentStatuses["PPO"] === "Active"
                      ? "bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40"
                      : "bg-white/10 text-slate-400 border border-white/10"
                  }`}
                >
                  ● {agentStatuses["PPO"]}
                </button>
              </div>

              {/* Type Badge */}
              <div className="text-xs font-mono text-slate-300 mb-4 flex items-center gap-1.5">
                <span className="bg-white/5 border border-white/10 px-2 py-0.5 rounded text-[11px]">
                  Actor-Critic RL (PyTorch)
                </span>
                <span className="text-emerald-400 font-bold text-[11px]">+18.3% Alpha</span>
              </div>

              {/* Current Season Revenue (Large Number in Gold) */}
              <div className="bg-black/50 rounded-xl p-4 border border-[#ffd700]/30 mb-4 space-y-1">
                <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 flex justify-between">
                  <span>Current Season Revenue</span>
                  <span className="text-[#ffd700] font-bold">RANK #1</span>
                </div>
                <div className="text-3xl sm:text-4xl font-mono font-bold text-[#ffd700] tracking-tight">
                  ${agentLiveRevenues["PPO"]?.toLocaleString()}
                </div>
              </div>

              {/* Mini Sparkline Chart (Last 20 Seasons) */}
              <div className="space-y-1.5 mb-4">
                <div className="flex justify-between text-[11px] font-mono text-slate-400">
                  <span>Last 20 Seasons Trajectory</span>
                  <span className="text-[#ffd700] font-bold">Mean: $4,850</span>
                </div>
                <div className="h-14 w-full bg-black/40 rounded-lg p-1 border border-white/5">
                  <svg className="w-full h-full overflow-visible" viewBox="0 0 200 45">
                    <defs>
                      <linearGradient id="ppoSparkGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#ffd700" stopOpacity="0.4" />
                        <stop offset="100%" stopColor="#ffd700" stopOpacity="0.0" />
                      </linearGradient>
                    </defs>
                    {/* Fill */}
                    <polygon
                      fill="url(#ppoSparkGrad)"
                      points={`0,45 ${sparklines["PPO"]
                        .map((val, idx) => {
                          const x = (idx / 19) * 200;
                          const y = 40 - ((val - 4300) / 1000) * 35;
                          return `${x},${y}`;
                        })
                        .join(" ")} 200,45`}
                    />
                    {/* Line */}
                    <polyline
                      fill="none"
                      stroke="#ffd700"
                      strokeWidth="2.5"
                      points={sparklines["PPO"]
                        .map((val, idx) => {
                          const x = (idx / 19) * 200;
                          const y = 40 - ((val - 4300) / 1000) * 35;
                          return `${x},${y}`;
                        })
                        .join(" ")}
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* Bottom Win Rate & Highlights */}
            <div className="pt-3 border-t border-white/10 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-300">Win Rate:</span>
              <span className="text-base font-bold text-[#ffd700]">46.8%</span>
            </div>
          </div>

          {/* CARD 2: SPECIAL DQN CARD (CORAL) */}
          <div className="lg:col-span-1 rounded-2xl glass-panel p-6 relative overflow-hidden border-t-4 border-t-[#ff6b6b] flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-xl bg-[#ff6b6b]/20 text-[#ff6b6b] border border-[#ff6b6b]/40 shadow-sm">
                    <Cpu className="h-6 w-6 text-[#ff6b6b]" />
                  </div>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <h3 className="text-xl font-bold text-white tracking-tight">DQN</h3>
                      <span className="rounded bg-[#ff6b6b]/20 px-2 py-0.5 text-[10px] font-mono font-bold text-[#ff6b6b] border border-[#ff6b6b]/40 uppercase tracking-wider">
                        Runner Up
                      </span>
                    </div>
                    <div className="text-[11px] font-mono text-slate-400 mt-0.5">
                      Deep Value Approximation
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => toggleAgentStatus("DQN")}
                  className={`text-[10px] font-mono px-2.5 py-1 rounded-full font-bold transition-all ${
                    agentStatuses["DQN"] === "Active"
                      ? "bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40"
                      : "bg-white/10 text-slate-400 border border-white/10"
                  }`}
                >
                  ● {agentStatuses["DQN"]}
                </button>
              </div>

              {/* Neural Network Visualization SVG */}
              <div className="rounded-xl bg-black/40 border border-white/10 p-2.5 mb-3">
                <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 mb-1">
                  <span>NEURAL NETWORK ARCHITECTURE</span>
                  <span className="text-[#ff6b6b] font-bold">2 → 4 → 3</span>
                </div>
                <div className="h-16 w-full flex items-center justify-center">
                  <svg className="w-full h-full" viewBox="0 0 160 55">
                    {/* Connections */}
                    {[15, 40].map((y1) =>
                      [10, 23, 36, 48].map((y2) => (
                        <line
                          key={`c1-${y1}-${y2}`}
                          x1="25"
                          y1={y1}
                          x2="80"
                          y2={y2}
                          stroke="#ff6b6b"
                          strokeWidth="0.8"
                          strokeOpacity="0.4"
                        />
                      ))
                    )}
                    {[10, 23, 36, 48].map((y1) =>
                      [15, 28, 42].map((y2) => (
                        <line
                          key={`c2-${y1}-${y2}`}
                          x1="80"
                          y1={y1}
                          x2="135"
                          y2={y2}
                          stroke="#ff6b6b"
                          strokeWidth="0.8"
                          strokeOpacity="0.4"
                        />
                      ))
                    )}
                    {/* Input Nodes */}
                    {[15, 40].map((y, i) => (
                      <circle key={`in-${i}`} cx="25" cy={y} r="4" fill="#ff6b6b" />
                    ))}
                    {/* Hidden Nodes */}
                    {[10, 23, 36, 48].map((y, i) => (
                      <circle
                        key={`hid-${i}`}
                        cx="80"
                        cy={y}
                        r="3.5"
                        fill="#ff6b6b"
                        className="animate-pulse"
                      />
                    ))}
                    {/* Output Nodes */}
                    {[15, 28, 42].map((y, i) => (
                      <circle key={`out-${i}`} cx="135" cy={y} r="4" fill="#ffd700" />
                    ))}
                  </svg>
                </div>
              </div>

              {/* Current Season Revenue */}
              <div className="bg-black/50 rounded-xl p-3.5 border border-white/5 mb-3 space-y-1">
                <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                  Current Season Revenue
                </div>
                <div className="text-3xl font-mono font-bold text-[#ff6b6b] tracking-tight">
                  ${agentLiveRevenues["DQN"]?.toLocaleString()}
                </div>
              </div>

              {/* Mini Sparkline */}
              <div className="space-y-1.5 mb-3">
                <div className="flex justify-between text-[11px] font-mono text-slate-400">
                  <span>Last 20 Seasons</span>
                  <span className="text-[#ff6b6b] font-bold">Mean: $4,420</span>
                </div>
                <div className="h-10 w-full bg-black/40 rounded-lg p-1 border border-white/5">
                  <svg className="w-full h-full" viewBox="0 0 200 35">
                    <polyline
                      fill="none"
                      stroke="#ff6b6b"
                      strokeWidth="2"
                      points={sparklines["DQN"]
                        .map((val, idx) => {
                          const x = (idx / 19) * 200;
                          const y = 30 - ((val - 3900) / 1000) * 25;
                          return `${x},${y}`;
                        })
                        .join(" ")}
                    />
                  </svg>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-white/10 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-300">Win Rate:</span>
              <span className="text-base font-bold text-[#ff6b6b]">28.4%</span>
            </div>
          </div>

          {/* CARD 3: Q-LEARNING CARD (EMERALD) */}
          <div className="lg:col-span-1 rounded-2xl glass-panel p-6 relative overflow-hidden border-t-4 border-t-[#00e676] flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-xl bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40 shadow-sm">
                    <Layers className="h-6 w-6 text-[#00e676]" />
                  </div>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <h3 className="text-xl font-bold text-white tracking-tight">Q-Learning</h3>
                      <span className="rounded bg-[#00e676]/20 px-2 py-0.5 text-[10px] font-mono font-bold text-[#00e676] border border-[#00e676]/40 uppercase tracking-wider">
                        3rd Place 🥉
                      </span>
                    </div>
                    <div className="text-[11px] font-mono text-slate-400 mt-0.5">
                      Tabular TD (1,581 States)
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => toggleAgentStatus("Q-Learning")}
                  className={`text-[10px] font-mono px-2.5 py-1 rounded-full font-bold transition-all ${
                    agentStatuses["Q-Learning"] === "Active"
                      ? "bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40"
                      : "bg-white/10 text-slate-400 border border-white/10"
                  }`}
                >
                  ● {agentStatuses["Q-Learning"]}
                </button>
              </div>

              <div className="text-xs font-mono text-slate-300 mb-4 flex items-center gap-1.5">
                <span className="bg-white/5 border border-white/10 px-2 py-0.5 rounded text-[11px]">
                  Tabular Q-Table
                </span>
                <span className="text-emerald-400 font-bold text-[11px]">+3.9% vs Baseline</span>
              </div>

              {/* Current Season Revenue */}
              <div className="bg-black/50 rounded-xl p-4 border border-white/5 mb-4 space-y-1">
                <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
                  Current Season Revenue
                </div>
                <div className="text-3xl sm:text-4xl font-mono font-bold text-[#00e676] tracking-tight">
                  ${agentLiveRevenues["Q-Learning"]?.toLocaleString()}
                </div>
              </div>

              {/* Mini Sparkline */}
              <div className="space-y-1.5 mb-4">
                <div className="flex justify-between text-[11px] font-mono text-slate-400">
                  <span>Last 20 Seasons</span>
                  <span className="text-[#00e676] font-bold">Mean: $4,280</span>
                </div>
                <div className="h-14 w-full bg-black/40 rounded-lg p-1 border border-white/5">
                  <svg className="w-full h-full" viewBox="0 0 200 45">
                    <polyline
                      fill="none"
                      stroke="#00e676"
                      strokeWidth="2"
                      points={sparklines["Q-Learning"]
                        .map((val, idx) => {
                          const x = (idx / 19) * 200;
                          const y = 40 - ((val - 3700) / 1100) * 35;
                          return `${x},${y}`;
                        })
                        .join(" ")}
                    />
                  </svg>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-white/10 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-300">Win Rate:</span>
              <span className="text-base font-bold text-[#00e676]">14.6%</span>
            </div>
          </div>

          {/* ─────────────────── ROW 2: 3 CARDS ─────────────────── */}

          {/* CARD 4: TIME BASED (STEEL BLUE) */}
          <div className="lg:col-span-1 rounded-2xl glass-panel p-5 relative overflow-hidden border-t-2 border-t-[#64b5f6] flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between mb-2.5">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full bg-[#64b5f6]" />
                  <div>
                    <h4 className="font-bold text-base text-white">Time Based</h4>
                    <span className="text-[10px] font-mono text-slate-400">
                      Heuristic Baseline
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => toggleAgentStatus("Time Based")}
                  className={`text-[9px] font-mono px-2 py-0.5 rounded-full font-bold transition-all ${
                    agentStatuses["Time Based"] === "Active"
                      ? "bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40"
                      : "bg-white/10 text-slate-400"
                  }`}
                >
                  {agentStatuses["Time Based"]}
                </button>
              </div>

              <div className="text-2xl font-mono font-bold text-white mb-2">
                ${agentLiveRevenues["Time Based"]?.toLocaleString()}
              </div>

              {/* Sparkline */}
              <div className="h-10 w-full bg-black/40 rounded p-1 mb-2">
                <svg className="w-full h-full" viewBox="0 0 200 30">
                  <polyline
                    fill="none"
                    stroke="#64b5f6"
                    strokeWidth="1.5"
                    points={sparklines["Time Based"]
                      .map((val, idx) => {
                        const x = (idx / 19) * 200;
                        const y = 25 - ((val - 3400) / 1200) * 20;
                        return `${x},${y}`;
                      })
                      .join(" ")}
                  />
                </svg>
              </div>
            </div>

            <div className="pt-2 border-t border-white/5 flex justify-between text-xs font-mono">
              <span className="text-slate-400">Win Rate:</span>
              <span className="text-[#64b5f6] font-bold">6.2%</span>
            </div>
          </div>

          {/* CARD 5: FIXED PRICE (SLATE) */}
          <div className="lg:col-span-1 rounded-2xl glass-panel p-5 relative overflow-hidden border-t-2 border-t-[#94a3b8] flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between mb-2.5">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full bg-[#94a3b8]" />
                  <div>
                    <h4 className="font-bold text-base text-white">Fixed Price ($150)</h4>
                    <span className="text-[10px] font-mono text-slate-400">
                      Static Heuristic
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => toggleAgentStatus("Fixed Price")}
                  className={`text-[9px] font-mono px-2 py-0.5 rounded-full font-bold transition-all ${
                    agentStatuses["Fixed Price"] === "Active"
                      ? "bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40"
                      : "bg-white/10 text-slate-400"
                  }`}
                >
                  {agentStatuses["Fixed Price"]}
                </button>
              </div>

              <div className="text-2xl font-mono font-bold text-white mb-2">
                ${agentLiveRevenues["Fixed Price"]?.toLocaleString()}
              </div>

              {/* Sparkline */}
              <div className="h-10 w-full bg-black/40 rounded p-1 mb-2">
                <svg className="w-full h-full" viewBox="0 0 200 30">
                  <polyline
                    fill="none"
                    stroke="#94a3b8"
                    strokeWidth="1.5"
                    points={sparklines["Fixed Price"]
                      .map((val, idx) => {
                        const x = (idx / 19) * 200;
                        const y = 25 - ((val - 3200) / 1200) * 20;
                        return `${x},${y}`;
                      })
                      .join(" ")}
                  />
                </svg>
              </div>
            </div>

            <div className="pt-2 border-t border-white/5 flex justify-between text-xs font-mono">
              <span className="text-slate-400">Win Rate:</span>
              <span className="text-slate-300 font-bold">2.1%</span>
            </div>
          </div>

          {/* CARD 6: LINEAR DECAY (ORANGE) */}
          <div className="lg:col-span-1 rounded-2xl glass-panel p-5 relative overflow-hidden border-t-2 border-t-[#fb923c] flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between mb-2.5">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full bg-[#fb923c]" />
                  <div>
                    <h4 className="font-bold text-base text-white">Linear Decay</h4>
                    <span className="text-[10px] font-mono text-slate-400">
                      Discount Heuristic
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => toggleAgentStatus("Linear Decay")}
                  className={`text-[9px] font-mono px-2 py-0.5 rounded-full font-bold transition-all ${
                    agentStatuses["Linear Decay"] === "Active"
                      ? "bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40"
                      : "bg-white/10 text-slate-400"
                  }`}
                >
                  {agentStatuses["Linear Decay"]}
                </button>
              </div>

              <div className="text-2xl font-mono font-bold text-white mb-2">
                ${agentLiveRevenues["Linear Decay"]?.toLocaleString()}
              </div>

              {/* Sparkline */}
              <div className="h-10 w-full bg-black/40 rounded p-1 mb-2">
                <svg className="w-full h-full" viewBox="0 0 200 30">
                  <polyline
                    fill="none"
                    stroke="#fb923c"
                    strokeWidth="1.5"
                    points={sparklines["Linear Decay"]
                      .map((val, idx) => {
                        const x = (idx / 19) * 200;
                        const y = 25 - ((val - 3000) / 1200) * 20;
                        return `${x},${y}`;
                      })
                      .join(" ")}
                  />
                </svg>
              </div>
            </div>

            <div className="pt-2 border-t border-white/5 flex justify-between text-xs font-mono">
              <span className="text-slate-400">Win Rate:</span>
              <span className="text-[#fb923c] font-bold">1.4%</span>
            </div>
          </div>

          {/* ─────────────────── ROW 3: 1 CARD (3-3-1 GRID) ─────── */}

          {/* CARD 7: DEMAND BASED (PURPLE) */}
          <div className="lg:col-span-3 rounded-2xl glass-panel glass-panel-purple p-5 relative overflow-hidden border-t-2 border-t-[#ba68c8] flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-300">
                <Flame className="h-5 w-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-bold text-base text-white">Demand Based</h4>
                  <span className="rounded bg-purple-500/20 px-2 py-0.5 text-[10px] font-mono text-purple-300 border border-purple-500/30 font-bold">
                    Threshold Rule
                  </span>
                </div>
                <p className="text-xs text-slate-400 font-mono">
                  Switches between $100 &amp; $250 based on inventory threshold (25 units)
                </p>
              </div>
            </div>

            <div className="flex items-center gap-6">
              <div className="text-right">
                <div className="text-[10px] font-mono text-slate-400">Current Season</div>
                <div className="text-2xl font-mono font-bold text-white">
                  ${agentLiveRevenues["Demand Based"]?.toLocaleString()}
                </div>
              </div>

              <div className="w-36 h-10 bg-black/40 rounded p-1 hidden sm:block">
                <svg className="w-full h-full" viewBox="0 0 140 30">
                  <polyline
                    fill="none"
                    stroke="#ba68c8"
                    strokeWidth="1.5"
                    points={sparklines["Demand Based"]
                      .map((val, idx) => {
                        const x = (idx / 19) * 140;
                        const y = 25 - ((val - 2700) / 1300) * 20;
                        return `${x},${y}`;
                      })
                      .join(" ")}
                  />
                </svg>
              </div>

              <div className="text-right pl-3 border-l border-white/10">
                <div className="text-[10px] font-mono text-slate-400">Win Rate</div>
                <div className="text-sm font-mono font-bold text-purple-300">0.5%</div>
              </div>

              <button
                onClick={() => toggleAgentStatus("Demand Based")}
                className={`text-[10px] font-mono px-3 py-1 rounded-full font-bold transition-all ${
                  agentStatuses["Demand Based"] === "Active"
                    ? "bg-[#00e676]/20 text-[#00e676] border border-[#00e676]/40"
                    : "bg-white/10 text-slate-400"
                }`}
              >
                {agentStatuses["Demand Based"]}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* BOTTOM SECTION: HEAD-TO-HEAD COMPARISON & FIGHT ANIMATION  */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel rounded-2xl p-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Swords className="h-5 w-5 text-[#ffd700]" />
              Head-to-Head Comparison Arena
            </h3>
            <p className="text-xs font-mono text-slate-400">
              Select any two algorithms for side-by-side empirical stats and statistical hypothesis testing
            </p>
          </div>

          <div className="text-xs font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1 rounded-lg flex items-center gap-1.5">
            <CheckCircle2 className="h-3.5 w-3.5" />
            Welch's Two-Sample t-test Active
          </div>
        </div>

        {/* Dropdowns & FIGHT Button Row */}
        <div className="grid grid-cols-1 md:grid-cols-11 gap-4 items-center">
          {/* Agent A Selector */}
          <div className="md:col-span-4 bg-black/40 rounded-xl p-4 border border-white/10 space-y-2">
            <label className="text-xs font-mono text-slate-400 uppercase tracking-wider block">
              Agent A (Challenger 1)
            </label>
            <select
              value={agentA}
              onChange={(e) => setAgentA(e.target.value)}
              className="w-full bg-[#121224] border border-white/20 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-[#ffd700]"
            >
              {ALL_7_AGENTS.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name} ({a.type}) — ${a.meanRevenue}
                </option>
              ))}
            </select>
          </div>

          {/* Center Fight Action Button with clash animation */}
          <div className="md:col-span-3 flex flex-col items-center justify-center">
            <button
              onClick={handleTriggerFight}
              className={`w-full py-3.5 px-4 rounded-xl text-xs sm:text-sm font-mono font-bold transition-all shadow-lg flex items-center justify-center gap-2 ${
                isFighting
                  ? "bg-red-500 text-white animate-fight-clash shadow-red-500/50"
                  : "bg-gradient-to-r from-[#ffd700] via-[#ffe55c] to-[#ffd700] text-black shadow-glow-gold hover:opacity-90"
              }`}
            >
              <Swords className={`h-4 w-4 ${isFighting ? "animate-spin" : ""}`} />
              <span>{isFighting ? "⚔️ CLASHING..." : "⚔️ FIGHT! COMPARE"}</span>
            </button>
            <span className="text-[10px] font-mono text-slate-500 mt-1">
              Run statistical comparison
            </span>
          </div>

          {/* Agent B Selector */}
          <div className="md:col-span-4 bg-black/40 rounded-xl p-4 border border-white/10 space-y-2">
            <label className="text-xs font-mono text-slate-400 uppercase tracking-wider block">
              Agent B (Challenger 2)
            </label>
            <select
              value={agentB}
              onChange={(e) => setAgentB(e.target.value)}
              className="w-full bg-[#121224] border border-white/20 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-[#ffd700]"
            >
              {ALL_7_AGENTS.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name} ({a.type}) — ${a.meanRevenue}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Statistical Test Result Banner */}
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-950/20 p-4 text-xs font-mono text-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-inner">
          <div className="flex items-center gap-2.5">
            <ShieldCheck className="h-5 w-5 text-emerald-400 shrink-0" />
            <div>
              <span className="font-bold text-white text-sm">
                Statistical Proof Verdict:{" "}
              </span>
              <span className="text-[#ffd700] font-bold">
                {selectedDataA.meanRevenue > selectedDataB.meanRevenue
                  ? `${selectedDataA.name} significantly better than ${selectedDataB.name} (p < 0.05)`
                  : selectedDataB.meanRevenue > selectedDataA.meanRevenue
                  ? `${selectedDataB.name} significantly better than ${selectedDataA.name} (p < 0.05)`
                  : "Both algorithms exhibit identical performance"}
              </span>
            </div>
          </div>

          <div className="text-[11px] text-slate-400 shrink-0">
            Alpha Lift:{" "}
            <strong className="text-emerald-400">
              {Math.abs(
                ((selectedDataA.meanRevenue - selectedDataB.meanRevenue) /
                  Math.min(selectedDataA.meanRevenue, selectedDataB.meanRevenue)) *
                  100
              ).toFixed(1)}
              %
            </strong>{" "}
            | 99% Confidence
          </div>
        </div>

        {/* Side by Side Stats Comparison Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 uppercase tracking-wider text-[11px]">
                <th className="py-3 px-4">Metric</th>
                <th className="py-3 px-4 text-center" style={{ color: selectedDataA.color }}>
                  {selectedDataA.name} ({selectedDataA.type})
                </th>
                <th className="py-3 px-4 text-center">Verdict / Delta</th>
                <th className="py-3 px-4 text-center" style={{ color: selectedDataB.color }}>
                  {selectedDataB.name} ({selectedDataB.type})
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {/* Mean Revenue */}
              <tr className="hover:bg-white/[0.03]">
                <td className="py-3.5 px-4 text-slate-300 font-semibold">Mean Revenue</td>
                <td className="py-3.5 px-4 text-center font-bold text-sm text-white">
                  ${selectedDataA.meanRevenue.toFixed(1)}
                </td>
                <td className="py-3.5 px-4 text-center">
                  <span
                    className={`font-bold px-2 py-0.5 rounded text-xs ${
                      selectedDataA.meanRevenue >= selectedDataB.meanRevenue
                        ? "bg-emerald-500/15 text-emerald-400"
                        : "bg-red-500/15 text-red-400"
                    }`}
                  >
                    {selectedDataA.meanRevenue >= selectedDataB.meanRevenue
                      ? `+${(selectedDataA.meanRevenue - selectedDataB.meanRevenue).toFixed(0)} (A Wins)`
                      : `-${(selectedDataB.meanRevenue - selectedDataA.meanRevenue).toFixed(0)} (B Wins)`}
                  </span>
                </td>
                <td className="py-3.5 px-4 text-center font-bold text-sm text-white">
                  ${selectedDataB.meanRevenue.toFixed(1)}
                </td>
              </tr>

              {/* Std Dev */}
              <tr className="hover:bg-white/[0.03]">
                <td className="py-3.5 px-4 text-slate-300 font-semibold">Std Dev (σ)</td>
                <td className="py-3.5 px-4 text-center text-slate-300">
                  ±${selectedDataA.stdRevenue.toFixed(1)}
                </td>
                <td className="py-3.5 px-4 text-center text-slate-400 text-[11px]">
                  {selectedDataA.stdRevenue < selectedDataB.stdRevenue
                    ? "A has higher stability"
                    : "B has higher stability"}
                </td>
                <td className="py-3.5 px-4 text-center text-slate-300">
                  ±${selectedDataB.stdRevenue.toFixed(1)}
                </td>
              </tr>

              {/* Max Revenue */}
              <tr className="hover:bg-white/[0.03]">
                <td className="py-3.5 px-4 text-slate-300 font-semibold">Max Season Revenue</td>
                <td className="py-3.5 px-4 text-center font-bold text-white">
                  ${selectedDataA.maxRevenue.toFixed(0)}
                </td>
                <td className="py-3.5 px-4 text-center text-slate-400 text-[11px]">
                  Peak Yield Capacity
                </td>
                <td className="py-3.5 px-4 text-center font-bold text-white">
                  ${selectedDataB.maxRevenue.toFixed(0)}
                </td>
              </tr>

              {/* Sell Through % */}
              <tr className="hover:bg-white/[0.03]">
                <td className="py-3.5 px-4 text-slate-300 font-semibold">Sell-Through Rate</td>
                <td className="py-3.5 px-4 text-center font-bold text-emerald-400">
                  {selectedDataA.sellThrough.toFixed(1)}%
                </td>
                <td className="py-3.5 px-4 text-center">
                  <span className="text-[11px] text-slate-300">
                    {selectedDataA.sellThrough >= selectedDataB.sellThrough ? "A clears stock faster" : "B clears stock faster"}
                  </span>
                </td>
                <td className="py-3.5 px-4 text-center font-bold text-emerald-400">
                  {selectedDataB.sellThrough.toFixed(1)}%
                </td>
              </tr>

              {/* Win Rate */}
              <tr className="hover:bg-white/[0.03]">
                <td className="py-3.5 px-4 text-slate-300 font-semibold">Season Win Rate</td>
                <td className="py-3.5 px-4 text-center font-bold text-[#ffd700]">
                  {selectedDataA.winRate.toFixed(1)}%
                </td>
                <td className="py-3.5 px-4 text-center">
                  <span className="font-bold text-xs text-white">
                    {selectedDataA.winRate >= selectedDataB.winRate
                      ? `${selectedDataA.name} Dominates`
                      : `${selectedDataB.name} Dominates`}
                  </span>
                </td>
                <td className="py-3.5 px-4 text-center font-bold text-[#ffd700]">
                  {selectedDataB.winRate.toFixed(1)}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
