import React, { useState, useEffect, useRef } from "react";
import {
  Play,
  Pause,
  RotateCcw,
  FastForward,
  Swords,
  Trophy,
  Package,
  DollarSign,
  AlertCircle,
  Flame,
  Clock,
  Sparkles,
  Info,
  CheckCircle2,
  XCircle,
} from "lucide-react";
import confetti from "canvas-confetti";
import { runSimulationStep, AGENT_COLORS } from "../data/simulationData";

const ARENA_AGENTS = [
  { name: "PPO", type: "Actor-Critic", color: "#ffd700", icon: "🥇" },
  { name: "DQN", type: "Deep Q-Network", color: "#ff6b6b", icon: "🥈" },
  { name: "Q-Learning", type: "Tabular TD", color: "#00e676", icon: "🥉" },
  { name: "Time Based", type: "Heuristic Baseline", color: "#64b5f6", icon: "⏱️" },
];

export default function AgentArenaPage() {
  const [day, setDay] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(500); // ms per day
  const [seasonSeed, setSeasonSeed] = useState(101);
  const [logs, setLogs] = useState([]);

  // Per-agent simulation state
  const [agentStates, setAgentStates] = useState({
    PPO: { inventory: 50, revenue: 0, currentPrice: 200, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 200 }] },
    DQN: { inventory: 50, revenue: 0, currentPrice: 150, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 150 }] },
    "Q-Learning": { inventory: 50, revenue: 0, currentPrice: 200, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 200 }] },
    "Time Based": { inventory: 50, revenue: 0, currentPrice: 50, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 50 }] },
  });

  const isSeasonComplete = day > 30;

  // Reset season
  const handleReset = (newSeed = null) => {
    const s = newSeed !== null ? newSeed : Math.floor(Math.random() * 900) + 100;
    setSeasonSeed(s);
    setDay(1);
    setIsPlaying(false);
    setLogs([]);
    setAgentStates({
      PPO: { inventory: 50, revenue: 0, currentPrice: 200, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 200 }] },
      DQN: { inventory: 50, revenue: 0, currentPrice: 150, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 150 }] },
      "Q-Learning": { inventory: 50, revenue: 0, currentPrice: 200, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 200 }] },
      "Time Based": { inventory: 50, revenue: 0, currentPrice: 50, lastAction: "Init", history: [{ day: 0, revenue: 0, inventory: 50, price: 50 }] },
    });
  };

  // Step simulation by 1 day
  const stepSimulation = () => {
    if (day > 30) {
      setIsPlaying(false);
      return;
    }

    const currentDay = day;
    const newLogs = [];

    setAgentStates((prev) => {
      const next = { ...prev };

      ARENA_AGENTS.forEach((agent) => {
        const cur = next[agent.name];
        // Use deterministic pseudo-random seed linked to day and seasonSeed
        const stepSeed = Math.abs(Math.sin(seasonSeed * 37 + currentDay * 19 + agent.name.length * 13)) % 1;

        const result = runSimulationStep({
          inventory: cur.inventory,
          day: currentDay,
          agentName: agent.name,
          randomSeed: stepSeed,
        });

        const newRevenue = cur.revenue + result.revenueGained;

        next[agent.name] = {
          inventory: result.newInventory,
          revenue: newRevenue,
          currentPrice: result.price,
          lastAction: result.rationale,
          history: [
            ...cur.history,
            {
              day: currentDay,
              revenue: newRevenue,
              inventory: result.newInventory,
              price: result.price,
              bought: result.bought,
            },
          ],
        };

        newLogs.push({
          day: currentDay,
          agent: agent.name,
          color: agent.color,
          price: result.price,
          bought: result.bought,
          demandProb: result.demandProb,
          remainingInv: result.newInventory,
          rationale: result.rationale,
        });
      });

      return next;
    });

    setLogs((prev) => [...newLogs.reverse(), ...prev.slice(0, 30)]);
    setDay((d) => d + 1);
  };

  // Run automatically when playing
  useEffect(() => {
    let timer;
    if (isPlaying && day <= 30) {
      timer = setTimeout(stepSimulation, speed);
    } else if (day > 30 && isPlaying) {
      setIsPlaying(false);
      // Trigger confetti celebration on victory
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ["#ffd700", "#ff6b6b", "#00e676", "#9c27b0"],
      });
    }
    return () => clearTimeout(timer);
  }, [isPlaying, day, speed]);

  // Run Instant Full Season
  const runInstant = () => {
    let currentDay = day;
    let localStates = { ...agentStates };
    const allNewLogs = [];

    while (currentDay <= 30) {
      ARENA_AGENTS.forEach((agent) => {
        const cur = localStates[agent.name];
        const stepSeed = Math.abs(Math.sin(seasonSeed * 37 + currentDay * 19 + agent.name.length * 13)) % 1;

        const result = runSimulationStep({
          inventory: cur.inventory,
          day: currentDay,
          agentName: agent.name,
          randomSeed: stepSeed,
        });

        const newRevenue = cur.revenue + result.revenueGained;

        localStates[agent.name] = {
          inventory: result.newInventory,
          revenue: newRevenue,
          currentPrice: result.price,
          lastAction: result.rationale,
          history: [
            ...cur.history,
            {
              day: currentDay,
              revenue: newRevenue,
              inventory: result.newInventory,
              price: result.price,
              bought: result.bought,
            },
          ],
        };

        allNewLogs.push({
          day: currentDay,
          agent: agent.name,
          color: agent.color,
          price: result.price,
          bought: result.bought,
          demandProb: result.demandProb,
          remainingInv: result.newInventory,
          rationale: result.rationale,
        });
      });
      currentDay++;
    }

    setAgentStates(localStates);
    setLogs((prev) => [...allNewLogs.slice(-20).reverse(), ...prev.slice(0, 20)]);
    setDay(31);
    setIsPlaying(false);

    confetti({
      particleCount: 100,
      spread: 80,
      origin: { y: 0.6 },
      colors: ["#ffd700", "#ff6b6b", "#00e676", "#9c27b0"],
    });
  };

  // Rank agents based on current score
  const sortedArena = [...ARENA_AGENTS].sort((a, b) => {
    return agentStates[b.name].revenue - agentStates[a.name].revenue;
  });

  return (
    <div className="space-y-6 pb-12 animate-fadeIn">
      {/* Arena Title & Control Panel */}
      <div className="glass-panel glass-panel-gold rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-mono text-[#ffd700] mb-1">
              <Swords className="h-4 w-4" />
              <span>HEAD-TO-HEAD SYNCHRONOUS ARENA</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Live Multi-Agent Competition Arena
            </h1>
            <p className="text-xs sm:text-sm text-slate-300">
              Watch PPO, DQN, Q-Learning, and the Baseline compete in real-time under identical customer demand curves.
            </p>
          </div>

          {/* Interactive Controller */}
          <div className="flex flex-wrap items-center gap-2 bg-black/40 border border-white/10 p-2 rounded-2xl">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              disabled={isSeasonComplete}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-mono font-bold transition-all ${
                isPlaying
                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                  : isSeasonComplete
                  ? "bg-white/5 text-slate-500 cursor-not-allowed border border-white/5"
                  : "bg-[#ffd700] text-black hover:bg-[#ffe55c] shadow-glow-gold"
              }`}
            >
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              <span>{isPlaying ? "PAUSE" : isSeasonComplete ? "FINISHED" : "SIMULATE"}</span>
            </button>

            <button
              onClick={stepSimulation}
              disabled={isPlaying || isSeasonComplete}
              className="px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-white text-xs font-mono border border-white/10 disabled:opacity-40 transition-all"
              title="Advance 1 Day"
            >
              Step +1d
            </button>

            <button
              onClick={runInstant}
              disabled={isSeasonComplete}
              className="flex items-center gap-1 px-3 py-2 rounded-xl bg-purple-900/40 hover:bg-purple-800/50 text-purple-300 text-xs font-mono border border-purple-500/30 disabled:opacity-40 transition-all"
            >
              <FastForward className="h-3.5 w-3.5" />
              Instant 30d
            </button>

            <button
              onClick={() => handleReset()}
              className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white border border-white/10 transition-all"
              title="Reset Season"
            >
              <RotateCcw className="h-4 w-4" />
            </button>

            {/* Speed Selector */}
            <div className="flex items-center gap-1 border-l border-white/10 pl-2 text-[11px] font-mono">
              <span className="text-slate-400 hidden sm:inline">Speed:</span>
              {[
                { label: "1x", val: 600 },
                { label: "3x", val: 200 },
                { label: "10x", val: 50 },
              ].map((s) => (
                <button
                  key={s.label}
                  onClick={() => setSpeed(s.val)}
                  className={`px-2 py-1 rounded-lg transition-all ${
                    speed === s.val
                      ? "bg-[#ffd700]/20 text-[#ffd700] border border-[#ffd700]/40 font-bold"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Season Timeline / Deadline Zone Meter */}
        <div className="mt-6 pt-4 border-t border-white/10 space-y-2">
          <div className="flex items-center justify-between text-xs font-mono">
            <div className="flex items-center gap-2">
              <span className="text-slate-400">SEASON PROGRESS:</span>
              <span className="text-white font-bold">
                DAY {Math.min(30, day)} / 30
              </span>
              <span className="text-slate-500">
                (Seed #{seasonSeed})
              </span>
            </div>

            <div className="flex items-center gap-3">
              {day >= 25 && (
                <span className="flex items-center gap-1 text-red-400 font-bold bg-red-500/10 px-2 py-0.5 rounded border border-red-500/30 animate-pulse text-[11px]">
                  <Flame className="h-3 w-3" />
                  DEADLINE LIQUIDATION ZONE ACTIVE
                </span>
              )}
              <span className="text-slate-400">
                Days Remaining: <strong className="text-white font-mono">{Math.max(0, 30 - day)}</strong>
              </span>
            </div>
          </div>

          {/* Progress Bar with highlighted Deadline Zone (Days 25-30) */}
          <div className="relative h-4 w-full rounded-full bg-black/50 border border-white/10 overflow-hidden flex">
            {/* Days 1 to 24 Normal Zone */}
            <div className="relative w-[80%] h-full border-r border-red-500/30">
              <div
                className="h-full bg-gradient-to-r from-[#ffd700] to-[#00e676] transition-all duration-300"
                style={{ width: `${Math.min(100, ((day - 1) / 24) * 100)}%` }}
              />
            </div>
            {/* Days 25 to 30 Deadline Zone */}
            <div className="relative w-[20%] h-full bg-red-950/30 flex items-center justify-center">
              <div
                className="h-full bg-red-500 transition-all duration-300 w-full"
                style={{
                  width: `${day <= 24 ? 0 : Math.min(100, ((day - 24) / 6) * 100)}%`,
                }}
              />
              <span className="absolute inset-0 flex items-center justify-center text-[9px] font-mono font-bold text-red-300 tracking-wider">
                DEADLINE ZONE
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Agent Status Cards (Head-to-Head Grid) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {ARENA_AGENTS.map((agent) => {
          const state = agentStates[agent.name];
          const rankIndex = sortedArena.findIndex((a) => a.name === agent.name);
          const isLeader = rankIndex === 0 && state.revenue > 0;
          const invPct = (state.inventory / 50) * 100;
          const unsoldPenalty = isSeasonComplete ? Math.max(0, state.inventory) * 10 : 0;
          const netProfit = state.revenue - unsoldPenalty;

          return (
            <div
              key={agent.name}
              className={`glass-panel rounded-2xl p-5 relative overflow-hidden transition-all duration-300 border-t-4 ${
                isLeader ? "shadow-glow-gold" : ""
              }`}
              style={{ borderTopColor: agent.color }}
            >
              {/* Leader Badge */}
              {isLeader && (
                <div className="absolute top-2 right-2 flex items-center gap-1 rounded-full bg-[#ffd700]/20 px-2 py-0.5 text-[10px] font-mono font-bold text-[#ffd700] border border-[#ffd700]/40">
                  <Trophy className="h-3 w-3" />
                  LEADER
                </div>
              )}

              <div className="flex items-center gap-2 mb-3">
                <span className="text-xl">{agent.icon}</span>
                <div>
                  <h3 className="font-bold text-base text-white flex items-center gap-1.5">
                    {agent.name}
                  </h3>
                  <span className="text-[11px] font-mono text-slate-400">
                    {agent.type}
                  </span>
                </div>
              </div>

              {/* Cumulative Revenue Counter */}
              <div className="bg-black/40 rounded-xl p-3 border border-white/5 mb-4">
                <div className="text-[10px] font-mono text-slate-400 flex items-center justify-between">
                  <span>CUMULATIVE REVENUE</span>
                  <span className="text-xs font-bold" style={{ color: agent.color }}>
                    Rank #{rankIndex + 1}
                  </span>
                </div>
                <div
                  className="text-2xl font-mono font-bold tracking-tight mt-0.5"
                  style={{ color: agent.color }}
                >
                  ${state.revenue.toFixed(0)}
                </div>

                {isSeasonComplete && (
                  <div className="mt-2 pt-1.5 border-t border-white/10 text-[10px] font-mono flex justify-between text-slate-400">
                    <span>Penalty ({state.inventory} left):</span>
                    <span className="text-red-400 font-semibold">-${unsoldPenalty}</span>
                  </div>
                )}
                {isSeasonComplete && (
                  <div className="text-[11px] font-mono flex justify-between text-white font-bold">
                    <span>Net Profit:</span>
                    <span className="text-emerald-400">${netProfit.toFixed(0)}</span>
                  </div>
                )}
              </div>

              {/* Current Day Price Action */}
              <div className="space-y-2 mb-4">
                <div className="flex justify-between items-center text-xs font-mono">
                  <span className="text-slate-400">Current Price Tag:</span>
                  <span
                    className="font-bold text-sm px-2 py-0.5 rounded font-mono"
                    style={{
                      backgroundColor: `${agent.color}20`,
                      color: agent.color,
                      border: `1px solid ${agent.color}40`,
                    }}
                  >
                    ${state.currentPrice}
                  </span>
                </div>

                <div className="text-[11px] font-mono text-slate-400 truncate bg-white/[0.02] p-1.5 rounded border border-white/5">
                  <span className="text-slate-500">Policy: </span>
                  <span className="text-slate-200">{state.lastAction}</span>
                </div>
              </div>

              {/* Inventory Tank Gauging */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs font-mono">
                  <span className="text-slate-400 flex items-center gap-1">
                    <Package className="h-3 w-3 text-slate-400" />
                    Remaining Inventory:
                  </span>
                  <span className="font-bold text-white">
                    {state.inventory} <span className="text-slate-500 font-normal">/ 50</span>
                  </span>
                </div>

                <div className="h-2 w-full rounded-full bg-white/10 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-300"
                    style={{
                      width: `${invPct}%`,
                      backgroundColor:
                        state.inventory <= 5
                          ? "#00e676"
                          : state.inventory <= 15
                          ? "#ffd700"
                          : agent.color,
                    }}
                  />
                </div>

                <div className="flex justify-between text-[10px] font-mono text-slate-500">
                  <span>Sold: {50 - state.inventory}</span>
                  <span>{((50 - state.inventory) / 50 * 100).toFixed(0)}% Clear</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Real-time Cumulative Revenue Line Race & Live Arena Event Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cumulative Revenue Progress Chart (SVG Line Chart) */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-white/10 pb-3">
            <div>
              <h3 className="font-bold text-white text-base flex items-center gap-2">
                <Trophy className="h-4 w-4 text-[#ffd700]" />
                Live Season Revenue Trajectory Race
              </h3>
              <p className="text-xs font-mono text-slate-400">
                Tracking cumulative earnings day by day across 30 season steps
              </p>
            </div>
            <div className="flex items-center gap-3 text-xs font-mono">
              {ARENA_AGENTS.map((a) => (
                <div key={a.name} className="flex items-center gap-1.5">
                  <span
                    className="h-2 w-2 rounded-full"
                    style={{ backgroundColor: a.color }}
                  />
                  <span className="text-slate-300">{a.name}</span>
                </div>
              ))}
            </div>
          </div>

          {/* SVG Chart Renderer */}
          <div className="relative h-64 w-full pt-4">
            <svg className="w-full h-full overflow-visible" viewBox="0 0 600 220">
              {/* Background horizontal grid lines */}
              {[0, 500, 1000, 1500, 2000, 2500].map((tick) => {
                const y = 200 - (tick / 2500) * 180;
                return (
                  <g key={tick}>
                    <line
                      x1="40"
                      y1={y}
                      x2="590"
                      y2={y}
                      stroke="rgba(255,255,255,0.06)"
                      strokeDasharray="4 4"
                    />
                    <text
                      x="32"
                      y={y + 4}
                      fill="#64748b"
                      fontSize="9"
                      fontFamily="JetBrains Mono"
                      textAnchor="end"
                    >
                      ${tick}
                    </text>
                  </g>
                );
              })}

              {/* Deadline Zone vertical banner (Day 25-30) */}
              <rect
                x={40 + (24 / 30) * 550}
                y="10"
                width={(6 / 30) * 550}
                height="190"
                fill="rgba(255, 107, 107, 0.08)"
                stroke="rgba(255, 107, 107, 0.2)"
                strokeDasharray="3 3"
              />
              <text
                x={40 + (27 / 30) * 550}
                y="25"
                fill="#ff6b6b"
                fontSize="9"
                fontFamily="JetBrains Mono"
                textAnchor="middle"
                fontWeight="bold"
              >
                DEADLINE ZONE
              </text>

              {/* X Axis Day markers */}
              {[1, 5, 10, 15, 20, 25, 30].map((d) => {
                const x = 40 + ((d - 1) / 29) * 550;
                return (
                  <g key={d}>
                    <line x1={x} y1="198" x2={x} y2="204" stroke="#64748b" />
                    <text
                      x={x}
                      y="216"
                      fill="#94a3b8"
                      fontSize="9"
                      fontFamily="JetBrains Mono"
                      textAnchor="middle"
                    >
                      d{d}
                    </text>
                  </g>
                );
              })}

              {/* Agent Curves */}
              {ARENA_AGENTS.map((agent) => {
                const history = agentStates[agent.name].history;
                if (!history || history.length === 0) return null;

                const points = history
                  .map((pt) => {
                    const x = 40 + (Math.max(0, pt.day - 1) / 29) * 550;
                    const y = 200 - (pt.revenue / 2500) * 180;
                    return `${x},${y}`;
                  })
                  .join(" ");

                const lastPoint = history[history.length - 1];
                const lastX = 40 + (Math.max(0, lastPoint.day - 1) / 29) * 550;
                const lastY = 200 - (lastPoint.revenue / 2500) * 180;

                return (
                  <g key={agent.name}>
                    <polyline
                      fill="none"
                      stroke={agent.color}
                      strokeWidth={agent.name === "PPO" ? "3" : "2"}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      points={points}
                      opacity={agent.name === "PPO" ? "1" : "0.8"}
                    />
                    {/* Head point indicator */}
                    <circle
                      cx={lastX}
                      cy={lastY}
                      r="4"
                      fill={agent.color}
                      stroke="#0d0d1a"
                      strokeWidth="1.5"
                    />
                  </g>
                );
              })}
            </svg>
          </div>
        </div>

        {/* Live Arena Order Stream & Action Log */}
        <div className="glass-panel rounded-2xl p-5 space-y-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-white/10 pb-2 mb-2">
              <span className="font-bold text-white text-sm flex items-center gap-1.5 font-mono">
                <Clock className="h-3.5 w-3.5 text-[#ffd700]" />
                Live Decision Log
              </span>
              <span className="text-[10px] font-mono text-emerald-400">
                ● Streaming
              </span>
            </div>

            <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
              {logs.length === 0 ? (
                <div className="text-center py-12 text-slate-500 text-xs font-mono">
                  Press <strong>SIMULATE</strong> or <strong>Step +1d</strong> to start season execution...
                </div>
              ) : (
                logs.map((log, idx) => (
                  <div
                    key={idx}
                    className="p-2 rounded-lg bg-black/40 border border-white/[0.04] text-[11px] font-mono space-y-1"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1.5">
                        <span
                          className="font-bold px-1.5 py-0.2 rounded text-[10px]"
                          style={{
                            backgroundColor: `${log.color}20`,
                            color: log.color,
                          }}
                        >
                          {log.agent}
                        </span>
                        <span className="text-slate-400">Day {log.day}</span>
                      </div>

                      <div className="flex items-center gap-1">
                        {log.bought ? (
                          <span className="text-emerald-400 font-bold flex items-center gap-0.5">
                            <CheckCircle2 className="h-3 w-3" /> SOLD +${log.price}
                          </span>
                        ) : (
                          <span className="text-slate-500 flex items-center gap-0.5">
                            <XCircle className="h-3 w-3" /> No Sale ($0)
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="text-[10px] text-slate-400 flex justify-between">
                      <span>P(Buy): {log.demandProb}%</span>
                      <span>Stock Left: {log.remainingInv}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="pt-2 border-t border-white/[0.06] text-[11px] font-mono text-slate-400 flex items-center justify-between">
            <span>Customer Demand Formula:</span>
            <span className="text-slate-300">0.7 * exp(-0.6 * P/100)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
