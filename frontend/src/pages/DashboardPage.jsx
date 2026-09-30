import React, { useState } from "react";
import {
  TrendingUp,
  DollarSign,
  PackageCheck,
  AlertTriangle,
  Award,
  Zap,
  ArrowUpRight,
  ShieldCheck,
  Flame,
  Activity,
  Layers,
  Sparkles,
  ChevronDown,
  CheckCircle,
  Clock,
  BarChart2,
} from "lucide-react";
import {
  LEADERBOARD_DATA,
  PROJECT_METADATA,
  AGENT_COLORS,
} from "../data/simulationData";

export default function DashboardPage({ onNavigate }) {
  const [selectedMetric, setSelectedMetric] = useState("meanRevenue");
  const [hoveredAgent, setHoveredAgent] = useState(null);

  const sortedLeaderboard = [...LEADERBOARD_DATA].sort((a, b) => {
    return b[selectedMetric] - a[selectedMetric];
  });

  const maxMetricVal = Math.max(...LEADERBOARD_DATA.map((d) => d[selectedMetric]));

  return (
    <div className="space-y-6 pb-12 animate-fadeIn">
      {/* Top Hero Banner: Bloomberg Terminal Meets Modern AI SaaS */}
      <div className="relative overflow-hidden rounded-2xl border border-[#ffd700]/25 bg-gradient-to-r from-[#16162a]/90 via-[#1f1738]/80 to-[#121224]/90 p-6 shadow-glass-gold">
        {/* Glow backdrop shapes */}
        <div className="pointer-events-none absolute -right-12 -top-12 h-64 w-64 rounded-full bg-[#ffd700]/10 blur-3xl" />
        <div className="pointer-events-none absolute right-1/3 -bottom-16 h-48 w-48 rounded-full bg-[#9c27b0]/20 blur-3xl" />

        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-[#ffd700]/15 px-3 py-1 font-semibold text-[#ffd700] border border-[#ffd700]/30 shadow-glow-gold">
                <Sparkles className="h-3.5 w-3.5" />
                ENTERPRISE REVENUE ENGINE
              </span>
              <span className="rounded-full bg-white/5 px-2.5 py-1 text-slate-300 border border-white/10">
                1,000 Monte Carlo Simulation Seasons
              </span>
              <span className="rounded-full bg-emerald-500/15 text-emerald-400 px-2.5 py-1 border border-emerald-500/30">
                Statistical Proof p &lt; 0.05
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white font-sans">
              Reinforcement Learning <span className="text-[#ffd700]">Dynamic Pricing</span> Dashboard
            </h1>

            <p className="text-sm text-slate-300 leading-relaxed font-sans">
              Autonomous multi-algorithm yield optimization for fixed-expiry inventory (hospitality & ticketing). 
              Trained deep policy agents learn micro-economic game dynamics—achieving 
              <span className="text-[#ffd700] font-semibold"> +18.2% revenue alpha</span> over static and rule-based heuristics.
            </p>
          </div>

          <div className="flex flex-row lg:flex-col items-center lg:items-end justify-between gap-3 shrink-0 border-t lg:border-t-0 lg:border-l border-white/10 pt-4 lg:pt-0 lg:pl-6">
            <div className="text-left lg:text-right">
              <div className="text-[11px] font-mono text-slate-400">Deployed Champion Agent</div>
              <div className="text-xl font-mono font-bold text-[#ffd700] flex items-center lg:justify-end gap-1.5">
                <Award className="h-5 w-5 text-[#ffd700]" />
                PPO Actor-Critic
              </div>
              <div className="text-xs font-mono text-emerald-400">#1 of 7 Algorithms Evaluated</div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => onNavigate("arena")}
                className="flex items-center gap-1.5 rounded-xl bg-[#ffd700] px-4 py-2.5 text-xs font-mono font-bold text-black shadow-glow-gold hover:bg-[#ffe55c] transition-all"
              >
                <Zap className="h-3.5 w-3.5" />
                Launch Live Arena
              </button>
              <button
                onClick={() => onNavigate("trajectory")}
                className="flex items-center gap-1.5 rounded-xl bg-white/10 px-4 py-2.5 text-xs font-mono text-white hover:bg-white/15 border border-white/15 transition-all"
              >
                Inspect Proof
                <ArrowUpRight className="h-3.5 w-3.5 text-slate-400" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* KPI Stat Cards (4 columns) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Mean Season Revenue */}
        <div className="glass-panel glass-panel-interactive rounded-2xl p-4 relative overflow-hidden border-t-2 border-t-[#ffd700]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Mean Season Revenue</span>
            <div className="p-2 rounded-lg bg-[#ffd700]/10 text-[#ffd700]">
              <DollarSign className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-mono font-bold text-white tracking-tight">
            $2,245.00
          </div>
          <div className="mt-2 flex items-center gap-1.5 text-xs font-mono">
            <span className="flex items-center text-emerald-400 font-bold bg-emerald-500/10 px-1.5 py-0.5 rounded">
              <TrendingUp className="h-3 w-3 mr-0.5" /> +18.2%
            </span>
            <span className="text-slate-400">vs Best Baseline</span>
          </div>
          <div className="mt-3 pt-2 border-t border-white/[0.06] text-[11px] font-mono text-slate-400 flex justify-between">
            <span>Range:</span>
            <span className="text-slate-300 font-semibold">$1,910 - $2,590</span>
          </div>
        </div>

        {/* Card 2: Sell-Through Rate */}
        <div className="glass-panel glass-panel-interactive rounded-2xl p-4 relative overflow-hidden border-t-2 border-t-[#00e676]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Sell-Through Rate</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-[#00e676]">
              <PackageCheck className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-mono font-bold text-white tracking-tight">
            94.2%
          </div>
          <div className="mt-2 flex items-center gap-1.5 text-xs font-mono">
            <span className="flex items-center text-emerald-400 font-bold bg-emerald-500/10 px-1.5 py-0.5 rounded">
              <TrendingUp className="h-3 w-3 mr-0.5" /> +15.6%
            </span>
            <span className="text-slate-400">vs 78.6% Baseline</span>
          </div>
          <div className="mt-3 pt-2 border-t border-white/[0.06] text-[11px] font-mono text-slate-400 flex justify-between">
            <span>Avg Unsold:</span>
            <span className="text-slate-300 font-semibold">2.9 / 50 seats</span>
          </div>
        </div>

        {/* Card 3: Stockout Risk */}
        <div className="glass-panel glass-panel-interactive rounded-2xl p-4 relative overflow-hidden border-t-2 border-t-[#9c27b0]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Early Stockout Rate</span>
            <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
              <ShieldCheck className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-mono font-bold text-white tracking-tight">
            0.8%
          </div>
          <div className="mt-2 flex items-center gap-1.5 text-xs font-mono">
            <span className="text-emerald-400 font-bold bg-emerald-500/10 px-1.5 py-0.5 rounded">
              OPTIMAL
            </span>
            <span className="text-slate-400">Paced inventory depletion</span>
          </div>
          <div className="mt-3 pt-2 border-t border-white/[0.06] text-[11px] font-mono text-slate-400 flex justify-between">
            <span>Burn Control:</span>
            <span className="text-slate-300 font-semibold">Protected to Day 28+</span>
          </div>
        </div>

        {/* Card 4: Unsold Penalty Aversion */}
        <div className="glass-panel glass-panel-interactive rounded-2xl p-4 relative overflow-hidden border-t-2 border-t-[#ff6b6b]">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Penalty Aversion</span>
            <div className="p-2 rounded-lg bg-red-500/10 text-[#ff6b6b]">
              <Flame className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-mono font-bold text-white tracking-tight">
            98.6%
          </div>
          <div className="mt-2 flex items-center gap-1.5 text-xs font-mono">
            <span className="text-coral-400 font-bold bg-red-500/10 text-[#ff6b6b] px-1.5 py-0.5 rounded">
              -$10 / Unit Penalty
            </span>
            <span className="text-slate-400">Preempted</span>
          </div>
          <div className="mt-3 pt-2 border-t border-white/[0.06] text-[11px] font-mono text-slate-400 flex justify-between">
            <span>Deadline Discount:</span>
            <span className="text-[#ffd700] font-semibold">Triggered Day 25+</span>
          </div>
        </div>
      </div>

      {/* Main Grid: Visual Agent Performance Matrix & Live Event Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Agent Ranking & Revenue Spread Visualizer */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/[0.08] pb-3">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <BarChart2 className="h-4 w-4 text-[#ffd700]" />
                Algorithm Performance Matrix (1,000 Seasons)
              </h2>
              <p className="text-xs font-mono text-slate-400">
                Direct comparative benchmark across deep RL models and baseline heuristics
              </p>
            </div>

            {/* Metric Selector Buttons */}
            <div className="flex items-center gap-1 bg-black/40 p-1 rounded-xl border border-white/10 text-xs font-mono">
              <button
                onClick={() => setSelectedMetric("meanRevenue")}
                className={`px-2.5 py-1 rounded-lg transition-all ${
                  selectedMetric === "meanRevenue"
                    ? "bg-[#ffd700] text-black font-bold shadow-glow-gold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Revenue ($)
              </button>
              <button
                onClick={() => setSelectedMetric("sellThrough")}
                className={`px-2.5 py-1 rounded-lg transition-all ${
                  selectedMetric === "sellThrough"
                    ? "bg-[#ffd700] text-black font-bold shadow-glow-gold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Sell-Through %
              </button>
              <button
                onClick={() => setSelectedMetric("winRate")}
                className={`px-2.5 py-1 rounded-lg transition-all ${
                  selectedMetric === "winRate"
                    ? "bg-[#ffd700] text-black font-bold shadow-glow-gold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Win Rate %
              </button>
            </div>
          </div>

          {/* Bar Chart Representation */}
          <div className="space-y-3 pt-2">
            {sortedLeaderboard.map((agent) => {
              const val = agent[selectedMetric];
              const pct = (val / maxMetricVal) * 100;
              const isPPO = agent.name === "PPO";

              return (
                <div
                  key={agent.name}
                  onMouseEnter={() => setHoveredAgent(agent)}
                  onMouseLeave={() => setHoveredAgent(null)}
                  className={`group relative rounded-xl p-3 transition-all duration-200 border ${
                    isPPO
                      ? "bg-[#ffd700]/[0.06] border-[#ffd700]/30 shadow-glass-gold"
                      : "bg-black/20 hover:bg-white/[0.04] border-white/[0.05]"
                  }`}
                >
                  <div className="flex items-center justify-between text-xs font-mono mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-400 w-5">#{agent.rank}</span>
                      <span
                        className="h-2.5 w-2.5 rounded-full shrink-0 shadow-sm"
                        style={{ backgroundColor: agent.color }}
                      />
                      <span className="font-semibold text-white group-hover:text-[#ffd700] transition-colors">
                        {agent.name}
                      </span>
                      <span className="text-[10px] text-slate-400 hidden sm:inline">
                        ({agent.type})
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="text-slate-400 text-[11px]">
                        {selectedMetric === "meanRevenue"
                          ? `±$${agent.stdRevenue.toFixed(0)}`
                          : selectedMetric === "sellThrough"
                          ? `${agent.sellThrough}% sold`
                          : `${agent.winRate}% seasons`}
                      </span>
                      <span
                        className="font-bold text-sm font-mono"
                        style={{ color: agent.color }}
                      >
                        {selectedMetric === "meanRevenue"
                          ? `$${val.toFixed(1)}`
                          : `${val.toFixed(1)}%`}
                      </span>
                    </div>
                  </div>

                  {/* Visual Progress Bar with Glow */}
                  <div className="relative h-3 w-full rounded-full bg-white/[0.06] overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500 relative"
                      style={{
                        width: `${pct}%`,
                        backgroundColor: agent.color,
                        boxShadow: `0 0 10px ${agent.color}80`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Quick takeaway note */}
          <div className="rounded-xl border border-white/10 bg-black/40 p-3 text-xs font-mono text-slate-300 flex items-center justify-between">
            <span className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-[#ffd700]" />
              PPO achieves highest mean ($2,245.0) and highest win rate (38.4%) across 1,000 stochastic seeds.
            </span>
            <button
              onClick={() => onNavigate("arena")}
              className="text-[#ffd700] hover:underline font-bold shrink-0 ml-3"
            >
              Simulate Match →
            </button>
          </div>
        </div>

        {/* Right Col: Two Proved Behaviors & Environment Context */}
        <div className="space-y-4">
          {/* Behavior 1 Card */}
          <div className="glass-panel rounded-2xl p-4 border-l-4 border-l-[#ffd700] space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono uppercase tracking-wider text-[#ffd700] font-bold">
                Behavior Proof #1
              </span>
              <span className="rounded-full bg-[#ffd700]/15 px-2 py-0.5 text-[10px] font-mono text-[#ffd700] border border-[#ffd700]/30">
                PROVED (p &lt; 0.01)
              </span>
            </div>
            <h3 className="text-sm font-bold text-white">
              Deadline Discounting Protocol
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              When remaining season duration drops below Day 25, the agent systematically slashes prices 
              from <span className="text-white font-mono">$180+ down to $50</span>. This guarantees complete inventory clearance 
              and avoids the -$10/unit penalty.
            </p>
            <div className="pt-1 flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span>Avg Drop:</span>
              <span className="text-[#ffd700] font-bold">-58.4% Price Cut</span>
            </div>
          </div>

          {/* Behavior 2 Card */}
          <div className="glass-panel rounded-2xl p-4 border-l-4 border-l-[#9c27b0] space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono uppercase tracking-wider text-purple-400 font-bold">
                Behavior Proof #2
              </span>
              <span className="rounded-full bg-purple-500/15 px-2 py-0.5 text-[10px] font-mono text-purple-300 border border-purple-500/30">
                PROVED (p &lt; 0.05)
              </span>
            </div>
            <h3 className="text-sm font-bold text-white">
              Scarcity Premium Dynamic Surge
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              If inventory is drawn down prematurely during Days 1–15, the agent detects scarcity and 
              spikes prices to the highest tiers (<span className="text-[#ffd700] font-mono">$250 - $300</span>), extracting maximum consumer surplus.
            </p>
            <div className="pt-1 flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span>Peak Markup:</span>
              <span className="text-purple-300 font-bold">+45.2% Margin Lift</span>
            </div>
          </div>

          {/* Environment Specs Card */}
          <div className="glass-panel rounded-2xl p-4 space-y-2.5">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400 border-b border-white/[0.08] pb-2">
              <span className="text-white font-semibold flex items-center gap-1.5">
                <Layers className="h-3.5 w-3.5 text-[#ffd700]" />
                MDP Environment Specs
              </span>
              <span className="text-[10px] text-emerald-400">Gym Compliant</span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs font-mono text-slate-300">
              <div className="bg-black/30 rounded-lg p-2 border border-white/5">
                <div className="text-[10px] text-slate-400">Max Inventory</div>
                <div className="text-sm font-bold text-white">50 units</div>
              </div>
              <div className="bg-black/30 rounded-lg p-2 border border-white/5">
                <div className="text-[10px] text-slate-400">Season Duration</div>
                <div className="text-sm font-bold text-white">30 days</div>
              </div>
              <div className="bg-black/30 rounded-lg p-2 border border-white/5">
                <div className="text-[10px] text-slate-400">Price Granularity</div>
                <div className="text-sm font-bold text-[#ffd700]">6 actions ($50-$300)</div>
              </div>
              <div className="bg-black/30 rounded-lg p-2 border border-white/5">
                <div className="text-[10px] text-slate-400">Unsold Penalty</div>
                <div className="text-sm font-bold text-red-400">-$10 / ticket</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Full Leaderboard Detailed Table */}
      <div className="glass-panel rounded-2xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Award className="h-4 w-4 text-[#ffd700]" />
              Official 7-Algorithm Benchmark Standings
            </h3>
            <p className="text-xs font-mono text-slate-400">
              Complete evaluation across 1,000 independent simulation seasons with identical demand distributions
            </p>
          </div>
          <span className="text-xs font-mono text-slate-400 bg-white/5 px-3 py-1.5 rounded-lg border border-white/10 hidden sm:inline">
            Seed = 42 (Fixed Evaluation Protocol)
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 uppercase tracking-wider text-[11px]">
                <th className="py-3 px-3">Rank &amp; Agent</th>
                <th className="py-3 px-3">Type</th>
                <th className="py-3 px-3">Mean Revenue</th>
                <th className="py-3 px-3">Std Dev (σ)</th>
                <th className="py-3 px-3">Min / Max Range</th>
                <th className="py-3 px-3">Sell-Through</th>
                <th className="py-3 px-3">Win Rate</th>
                <th className="py-3 px-3">Alpha Uplift</th>
                <th className="py-3 px-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06]">
              {LEADERBOARD_DATA.map((row) => {
                const isChampion = row.rank === 1;

                return (
                  <tr
                    key={row.name}
                    className={`transition-colors ${
                      isChampion
                        ? "bg-[#ffd700]/[0.08] hover:bg-[#ffd700]/[0.12]"
                        : "hover:bg-white/[0.03]"
                    }`}
                  >
                    <td className="py-3.5 px-3 font-semibold flex items-center gap-2">
                      <span className="w-5 text-slate-400 font-bold">#{row.rank}</span>
                      <span
                        className="h-2.5 w-2.5 rounded-full"
                        style={{ backgroundColor: row.color }}
                      />
                      <span className={isChampion ? "text-[#ffd700] font-bold text-sm" : "text-white"}>
                        {row.name}
                      </span>
                    </td>
                    <td className="py-3.5 px-3 text-slate-300">{row.type}</td>
                    <td className="py-3.5 px-3 font-bold text-sm text-white">
                      ${row.meanRevenue.toFixed(1)}
                    </td>
                    <td className="py-3.5 px-3 text-slate-400">±${row.stdRevenue.toFixed(1)}</td>
                    <td className="py-3.5 px-3 text-slate-400">
                      ${row.minRevenue.toFixed(0)} - ${row.maxRevenue.toFixed(0)}
                    </td>
                    <td className="py-3.5 px-3 font-semibold text-emerald-400">
                      {row.sellThrough.toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-slate-200">{row.winRate.toFixed(1)}%</td>
                    <td className="py-3.5 px-3">
                      <span
                        className={`font-bold px-1.5 py-0.5 rounded text-[11px] ${
                          row.upliftVsBaseline.startsWith("+")
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                            : "bg-slate-500/10 text-slate-400"
                        }`}
                      >
                        {row.upliftVsBaseline}
                      </span>
                    </td>
                    <td className="py-3.5 px-3">
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${
                          isChampion
                            ? "bg-[#ffd700]/20 text-[#ffd700] border border-[#ffd700]/40"
                            : "bg-white/5 text-slate-400 border border-white/10"
                        }`}
                      >
                        {row.status}
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
