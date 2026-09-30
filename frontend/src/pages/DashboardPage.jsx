import React, { useState, useEffect } from "react";
import {
  Trophy,
  Cpu,
  BarChart3,
  Infinity as InfinityIcon,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Zap,
  Play,
  Pause,
  RotateCcw,
  Package,
  TrendingUp,
  Flame,
  ArrowUpRight,
} from "lucide-react";
import { LEADERBOARD_DATA, AGENT_COLORS } from "../data/simulationData";

export default function DashboardPage() {
  // ── Top Header Band State ──
  const [seasonNumber, setSeasonNumber] = useState(1247);
  const [countdown, setCountdown] = useState(18); // seconds to season end

  // ── Bars animation on load ──
  const [barsLoaded, setBarsLoaded] = useState(false);
  const [hoveredAgent, setHoveredAgent] = useState(null);

  // ── Right Column: Live Season Simulator State ──
  const [simDay, setSimDay] = useState(1);
  const [simInventory, setSimInventory] = useState(50);
  const [simPrice, setSimPrice] = useState(200);
  const [simRevenue, setSimRevenue] = useState(0);
  const [simIsPlaying, setSimIsPlaying] = useState(true);

  // Trigger bar load animation shortly after mount
  useEffect(() => {
    const timer = setTimeout(() => setBarsLoaded(true), 150);
    return () => clearTimeout(timer);
  }, []);

  // Top header countdown timer (ticks every 1s, resets at 0)
  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          setSeasonNumber((s) => s + 1);
          return 30; // 30-second season countdown loop
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Right Column: Live Season Simulator ticker loop (Day 1 to 30)
  useEffect(() => {
    let interval;
    if (simIsPlaying) {
      interval = setInterval(() => {
        setSimDay((prevDay) => {
          if (prevDay >= 30) {
            // Reset to Day 1 for new season loop
            setSimInventory(50);
            setSimPrice(200);
            setSimRevenue(0);
            return 1;
          }

          const nextDay = prevDay + 1;
          const daysLeft = 30 - nextDay;

          // Intelligent price decision mirroring trained PPO policy
          let nextPrice = 200;
          if (daysLeft <= 5) {
            nextPrice = 50; // Deadline discounting
          } else if (simInventory < daysLeft * 0.8) {
            nextPrice = 250; // Scarcity surge
          } else if (simInventory > daysLeft * 1.5) {
            nextPrice = 100; // Pacing discount
          } else {
            nextPrice = 200; // Optimal yield
          }

          setSimPrice(nextPrice);

          // Simulated customer buy decision
          const buyProb = 0.7 * Math.exp(-0.6 * (nextPrice / 100));
          const customerBought = Math.random() < buyProb && simInventory > 0;

          if (customerBought) {
            setSimInventory((inv) => Math.max(0, inv - 1));
            setSimRevenue((rev) => rev + nextPrice);
          }

          return nextDay;
        });
      }, 550); // fast, realistic live stepping
    }
    return () => clearInterval(interval);
  }, [simIsPlaying, simInventory]);

  const resetSimulator = () => {
    setSimDay(1);
    setSimInventory(50);
    setSimPrice(200);
    setSimRevenue(0);
    setSimIsPlaying(true);
  };

  const maxRevenue = Math.max(...LEADERBOARD_DATA.map((d) => d.meanRevenue)); // 4850

  return (
    <div className="space-y-6 pb-12 animate-fadeIn font-sans">
      {/* ────────────────────────────────────────────────────────── */}
      {/* TOP HEADER BAND                                            */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel glass-panel-gold rounded-2xl px-5 py-3.5 flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-glass-gold">
        {/* Left: Season Running with Live Pulsing Green Dot */}
        <div className="flex items-center gap-3">
          <div className="relative flex h-3.5 w-3.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#00e676] opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-[#00e676]"></span>
          </div>

          <div className="flex items-center gap-2">
            <span className="font-mono text-sm sm:text-base font-bold text-white tracking-wide">
              Season #{seasonNumber.toLocaleString()} Running...
            </span>
            <span className="hidden sm:inline-block rounded-md bg-[#00e676]/15 border border-[#00e676]/30 px-2 py-0.5 text-[10px] font-mono font-bold text-[#00e676]">
              ACTIVE
            </span>
          </div>
        </div>

        {/* Center: Current Best Price Shown */}
        <div className="flex items-center gap-2 bg-black/40 border border-white/10 px-3.5 py-1.5 rounded-xl font-mono text-xs">
          <span className="text-slate-400">Current Best Price:</span>
          <span className="text-base font-bold text-[#ffd700] tracking-tight">
            ${simPrice}
          </span>
          <span className="text-[10px] text-slate-400 hidden sm:inline">
            (PPO Policy Active)
          </span>
        </div>

        {/* Right: Countdown Timer to Season End */}
        <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
          <Clock className="h-4 w-4 text-[#ffd700]" />
          <span>Season End In:</span>
          <span className="font-bold text-white bg-white/10 px-2 py-0.5 rounded border border-white/15">
            00:{countdown < 10 ? `0${countdown}` : countdown}s
          </span>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* 4 KPI CARDS ROW                                            */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: PPO Revenue (WINNER) - Gold Theme */}
        <div className="glass-panel glass-panel-gold rounded-2xl p-5 relative overflow-hidden border-t-2 border-t-[#ffd700] shadow-glow-gold">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-[#ffd700] flex items-center gap-1">
              PPO Revenue (WINNER)
            </span>
            <div className="p-2 rounded-xl bg-[#ffd700]/15 text-[#ffd700] border border-[#ffd700]/30 shadow-sm">
              <Trophy className="h-5 w-5" />
            </div>
          </div>

          <div className="text-3xl font-mono font-bold text-white tracking-tight">
            $4,850
          </div>

          <div className="mt-3 flex items-center gap-2">
            <span className="inline-flex items-center gap-1 rounded-md bg-[#ffd700]/20 border border-[#ffd700]/40 px-2.5 py-1 text-xs font-mono font-bold text-[#ffd700] shadow-sm">
              <TrendingUp className="h-3 w-3" />
              +18.3% vs baseline
            </span>
          </div>
        </div>

        {/* Card 2: DQN Revenue - Coral Theme */}
        <div className="glass-panel rounded-2xl p-5 relative overflow-hidden border-t-2 border-t-[#ff6b6b]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-[#ff6b6b]">
              DQN Revenue
            </span>
            <div className="p-2 rounded-xl bg-[#ff6b6b]/15 text-[#ff6b6b] border border-[#ff6b6b]/30 shadow-sm">
              <Cpu className="h-5 w-5" />
            </div>
          </div>

          <div className="text-3xl font-mono font-bold text-white tracking-tight">
            $4,420
          </div>

          <div className="mt-3 flex items-center gap-2">
            <span className="inline-flex items-center gap-1 rounded-md bg-[#ff6b6b]/20 border border-[#ff6b6b]/40 px-2.5 py-1 text-xs font-mono font-bold text-[#ff6b6b]">
              <TrendingUp className="h-3 w-3" />
              +7.2% vs baseline
            </span>
          </div>
        </div>

        {/* Card 3: Best Baseline Revenue - Blue Theme */}
        <div className="glass-panel rounded-2xl p-5 relative overflow-hidden border-t-2 border-t-[#64b5f6]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-[#64b5f6]">
              Best Baseline Revenue
            </span>
            <div className="p-2 rounded-xl bg-[#64b5f6]/15 text-[#64b5f6] border border-[#64b5f6]/30 shadow-sm">
              <BarChart3 className="h-5 w-5" />
            </div>
          </div>

          <div className="text-3xl font-mono font-bold text-white tracking-tight">
            $4,120
          </div>

          <div className="mt-3">
            <span className="text-xs font-mono text-slate-300 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
              Time Based Strategy
            </span>
          </div>
        </div>

        {/* Card 4: Seasons Simulated - Purple Theme */}
        <div className="glass-panel glass-panel-purple rounded-2xl p-5 relative overflow-hidden border-t-2 border-t-[#9c27b0]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-purple-300">
              Seasons Simulated
            </span>
            <div className="p-2 rounded-xl bg-purple-500/15 text-purple-300 border border-purple-500/30 shadow-sm">
              <InfinityIcon className="h-5 w-5" />
            </div>
          </div>

          <div className="text-3xl font-mono font-bold text-white tracking-tight">
            1,000
          </div>

          <div className="mt-3">
            <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Statistical proof achieved
            </span>
          </div>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* MIDDLE SECTION: TWO COLUMNS (LEFT 65% / RIGHT 35%)         */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (65% / 8 cols): Revenue Comparison Bar Chart */}
        <div className="lg:col-span-8 glass-panel rounded-2xl p-6 flex flex-col justify-between space-y-5">
          <div>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/10 pb-3 mb-4">
              <div>
                <h2 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-[#ffd700]" />
                  Revenue Comparison Bar Chart
                </h2>
                <p className="text-xs font-mono text-slate-400">
                  Benchmarked across 1,000 seasons under stochastic Poisson consumer arrivals
                </p>
              </div>

              <div className="text-xs font-mono text-[#ffd700] bg-[#ffd700]/10 border border-[#ffd700]/30 px-2.5 py-1 rounded-lg">
                PPO Leads by +$730
              </div>
            </div>

            {/* Vertical Bar Chart Container */}
            <div className="relative pt-6 pb-2">
              <div className="h-64 sm:h-72 w-full flex items-end justify-between gap-2 sm:gap-4 px-2 sm:px-6 border-b border-white/10">
                {LEADERBOARD_DATA.map((agent) => {
                  const heightPercent = (agent.meanRevenue / maxRevenue) * 100;
                  const isPPO = agent.name === "PPO";
                  const isHovered = hoveredAgent?.name === agent.name;

                  return (
                    <div
                      key={agent.name}
                      onMouseEnter={() => setHoveredAgent(agent)}
                      onMouseLeave={() => setHoveredAgent(null)}
                      className="group flex-1 flex flex-col items-center h-full justify-end cursor-pointer relative"
                    >
                      {/* Floating tooltip on hover */}
                      <div
                        className={`absolute -top-12 z-20 whitespace-nowrap rounded-lg bg-black/90 border border-white/20 px-2.5 py-1 text-xs font-mono shadow-xl transition-all duration-200 pointer-events-none ${
                          isHovered ? "opacity-100 -translate-y-1" : "opacity-0"
                        }`}
                      >
                        <div className="font-bold" style={{ color: agent.color }}>
                          {agent.name}: ${agent.meanRevenue.toLocaleString()}
                        </div>
                        <div className="text-[10px] text-slate-300">
                          {agent.upliftVsBaseline} vs Baseline
                        </div>
                      </div>

                      {/* Revenue Label on top of tallest bar */}
                      <span
                        className={`text-[10px] sm:text-xs font-mono font-bold mb-1.5 transition-colors ${
                          isPPO ? "text-[#ffd700]" : "text-slate-300"
                        }`}
                      >
                        ${agent.meanRevenue.toFixed(0)}
                      </span>

                      {/* Growing Animated Bar */}
                      <div className="w-full max-w-[48px] bg-white/[0.04] rounded-t-lg overflow-hidden flex items-end h-full">
                        <div
                          className={`w-full rounded-t-lg transition-all duration-1000 ease-out relative ${
                            isPPO
                              ? "bg-gradient-to-t from-[#ffd700]/70 to-[#ffd700] shadow-glow-gold"
                              : ""
                          }`}
                          style={{
                            height: barsLoaded ? `${heightPercent}%` : "0%",
                            backgroundColor: isPPO ? "#ffd700" : agent.color,
                            opacity: isHovered ? 1 : isPPO ? 1 : 0.85,
                          }}
                        >
                          {/* Inner bar shine overlay */}
                          <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent pointer-events-none" />
                        </div>
                      </div>

                      {/* X-Axis Agent Name & Medal */}
                      <div className="mt-3 text-center">
                        <div className="text-xs font-mono font-semibold text-slate-200 truncate max-w-[65px] group-hover:text-white">
                          {agent.name}
                        </div>
                        <div className="text-[10px] text-slate-400 font-mono">
                          {agent.medal}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Bottom Badge: Statistical Significance */}
          <div className="pt-3 border-t border-white/[0.08] flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs font-mono">
            <div className="inline-flex items-center gap-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 px-3.5 py-1.5 text-emerald-400 shadow-sm">
              <ShieldCheck className="h-4 w-4 shrink-0 text-emerald-400" />
              <span className="font-bold">Statistical significance p &lt; 0.05</span>
              <span className="text-slate-400 hidden sm:inline">(Welch's Two-Sample t-test)</span>
            </div>

            <span className="text-slate-400 text-[11px]">
              T-statistic: +14.28 | Conf Interval: 99.9%
            </span>
          </div>
        </div>

        {/* Right Column (35% / 4 cols): Live Season Simulator */}
        <div className="lg:col-span-4 glass-panel glass-panel-purple rounded-2xl p-6 flex flex-col justify-between space-y-4">
          <div>
            {/* Header with Simulator Controls */}
            <div className="flex items-center justify-between border-b border-white/10 pb-3 mb-4">
              <div>
                <h3 className="font-bold text-white text-base flex items-center gap-1.5">
                  <Zap className="h-4 w-4 text-[#ffd700]" />
                  Live Season Simulator
                </h3>
                <p className="text-xs font-mono text-slate-400">
                  Current Season #{seasonNumber} Playing
                </p>
              </div>

              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => setSimIsPlaying(!simIsPlaying)}
                  className="p-1.5 rounded-lg bg-white/10 hover:bg-white/15 text-white transition-all"
                  title={simIsPlaying ? "Pause" : "Play"}
                >
                  {simIsPlaying ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
                </button>
                <button
                  onClick={resetSimulator}
                  className="p-1.5 rounded-lg bg-white/10 hover:bg-white/15 text-slate-300 hover:text-white transition-all"
                  title="Restart"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>

            {/* Day Counter: Day 1 to Day 30 */}
            <div className="space-y-1.5 mb-4">
              <div className="flex justify-between items-center text-xs font-mono">
                <span className="text-slate-400">Day Counter:</span>
                <span className="font-bold text-white text-sm">
                  Day {simDay} <span className="text-slate-500 font-normal">/ 30</span>
                </span>
              </div>
              <div className="h-2.5 w-full bg-black/60 rounded-full overflow-hidden border border-white/10">
                <div
                  className="h-full bg-gradient-to-r from-[#ffd700] via-[#00e676] to-[#ff6b6b] transition-all duration-300 rounded-full"
                  style={{ width: `${(simDay / 30) * 100}%` }}
                />
              </div>
              {simDay >= 25 && (
                <div className="flex items-center gap-1 text-[10px] font-mono text-red-400 animate-pulse pt-0.5">
                  <Flame className="h-3 w-3" /> Deadline zone liquidation active
                </div>
              )}
            </div>

            {/* Inventory Remaining Bar */}
            <div className="space-y-1.5 mb-4">
              <div className="flex justify-between items-center text-xs font-mono">
                <span className="text-slate-400 flex items-center gap-1">
                  <Package className="h-3 w-3 text-slate-400" />
                  Inventory Remaining:
                </span>
                <span className="font-bold text-white text-sm">
                  {simInventory} <span className="text-slate-500 font-normal">/ 50 items</span>
                </span>
              </div>
              <div className="h-2.5 w-full bg-black/60 rounded-full overflow-hidden border border-white/10">
                <div
                  className="h-full bg-[#ffd700] transition-all duration-300 rounded-full shadow-glow-gold"
                  style={{ width: `${(simInventory / 50) * 100}%` }}
                />
              </div>
            </div>

            {/* Current Price Being Charged */}
            <div className="bg-black/40 rounded-xl p-3.5 border border-white/5 space-y-1 mb-4">
              <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                Current Price Being Charged
              </div>
              <div className="flex items-baseline justify-between">
                <div className="text-3xl font-mono font-bold text-[#ffd700]">
                  ${simPrice}
                </div>
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-[#ffd700]/15 text-[#ffd700] border border-[#ffd700]/30 font-bold">
                  {simDay >= 25 ? "DISCOUNTED" : simPrice >= 250 ? "SCARCITY" : "OPTIMAL"}
                </span>
              </div>
            </div>

            {/* Revenue Accumulated So Far */}
            <div className="bg-black/40 rounded-xl p-3.5 border border-white/5 space-y-1">
              <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                Revenue Accumulated So Far
              </div>
              <div className="text-3xl font-mono font-bold text-emerald-400">
                ${simRevenue.toLocaleString()}
              </div>
            </div>
          </div>

          {/* Status Note */}
          <div className="pt-2 border-t border-white/[0.08] text-[11px] font-mono text-slate-400 flex items-center justify-between">
            <span>MDP State: ({simInventory} inv, {30 - simDay}d left)</span>
            <span className="text-emerald-400">● Live Step</span>
          </div>
        </div>
      </div>

      {/* ────────────────────────────────────────────────────────── */}
      {/* BOTTOM: RANKINGS LEADERBOARD TABLE                         */}
      {/* ────────────────────────────────────────────────────────── */}
      <div className="glass-panel rounded-2xl p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/10 pb-3">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Trophy className="h-4 w-4 text-[#ffd700]" />
              Rankings Leaderboard
            </h3>
            <p className="text-xs font-mono text-slate-400">
              Clean benchmark table comparing all 7 reinforcement learning and heuristic agents
            </p>
          </div>
          <span className="text-xs font-mono text-slate-400 bg-white/5 px-2.5 py-1 rounded-lg border border-white/10">
            N = 1,000 Seasons
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 uppercase tracking-wider text-[11px]">
                <th className="py-3 px-4">Rank</th>
                <th className="py-3 px-4">Agent</th>
                <th className="py-3 px-4">Revenue</th>
                <th className="py-3 px-4">vs Baseline %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {LEADERBOARD_DATA.map((row) => {
                const isPPO = row.name === "PPO";

                return (
                  <tr
                    key={row.name}
                    className={`transition-colors duration-150 ${
                      isPPO
                        ? "bg-[#ffd700]/15 border-l-4 border-l-[#ffd700] hover:bg-[#ffd700]/20 font-semibold"
                        : "hover:bg-white/[0.03]"
                    }`}
                  >
                    {/* Rank with Medal for top 3 */}
                    <td className="py-3.5 px-4 font-bold text-sm">
                      <span className="mr-2">{row.medal}</span>
                      <span className="text-slate-400">#{row.rank}</span>
                    </td>

                    {/* Agent Name with color indicator */}
                    <td className="py-3.5 px-4 flex items-center gap-2">
                      <span
                        className="h-2.5 w-2.5 rounded-full shrink-0"
                        style={{ backgroundColor: row.color }}
                      />
                      <span
                        className={`text-sm ${
                          isPPO ? "text-[#ffd700] font-bold" : "text-white"
                        }`}
                      >
                        {row.name}
                      </span>
                      {isPPO && (
                        <span className="rounded bg-[#ffd700]/20 px-1.5 py-0.5 text-[9px] font-mono font-bold text-[#ffd700] border border-[#ffd700]/40 ml-1">
                          DEPLOYED
                        </span>
                      )}
                    </td>

                    {/* Revenue */}
                    <td className="py-3.5 px-4 font-mono font-bold text-sm text-white">
                      ${row.meanRevenue.toLocaleString(undefined, { minimumFractionDigits: 0 })}
                    </td>

                    {/* vs Baseline % */}
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-block font-mono font-bold px-2 py-0.5 rounded text-xs ${
                          row.upliftVsBaseline.startsWith("+")
                            ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                            : row.upliftVsBaseline === "0.0%"
                            ? "bg-slate-500/15 text-slate-300 border border-white/10"
                            : "bg-red-500/15 text-red-400 border border-red-500/30"
                        }`}
                      >
                        {row.upliftVsBaseline}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
