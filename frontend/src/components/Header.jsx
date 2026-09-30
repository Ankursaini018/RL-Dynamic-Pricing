import React, { useState, useEffect } from "react";
import { 
  Zap, 
  Activity, 
  ShieldCheck, 
  Terminal, 
  Play, 
  Pause, 
  RotateCw,
  TrendingUp,
  Cpu
} from "lucide-react";

export default function Header({ 
  currentSeason, 
  onSeasonChange, 
  isAutoSeason, 
  setIsAutoSeason 
}) {
  const [tickerItems, setTickerItems] = useState([
    { agent: "PPO", price: "$50", day: 29, status: "CLEARANCE_SALE", gain: "+$50", color: "#ffd700" },
    { agent: "DQN", price: "$200", day: 14, status: "PEAK_DEMAND", gain: "+$200", color: "#ff6b6b" },
    { agent: "PPO", price: "$250", day: 4, status: "SCARCITY_PREMIUM", gain: "+$250", color: "#ffd700" },
    { agent: "Q-LEARN", price: "$100", day: 19, status: "MID_CYCLE", gain: "+$100", color: "#00e676" },
    { agent: "TIME_BASED", price: "$300", day: 30, status: "NO_SALE (EXPIRED)", gain: "$0", color: "#64b5f6" },
    { agent: "PPO", price: "$150", day: 8, status: "OPTIMAL_YIELD", gain: "+$150", color: "#ffd700" },
    { agent: "DQN", price: "$50", day: 28, status: "DEADLINE_CUT", gain: "+$50", color: "#ff6b6b" },
  ]);

  // Periodic ticker update for live Bloomberg terminal vibe
  useEffect(() => {
    const interval = setInterval(() => {
      const agents = [
        { name: "PPO", color: "#ffd700", prices: [50, 100, 200, 250] },
        { name: "DQN", color: "#ff6b6b", prices: [50, 150, 200] },
        { name: "Q-LEARN", color: "#00e676", prices: [50, 100, 150] },
        { name: "TIME_BASED", color: "#64b5f6", prices: [250, 300] },
      ];
      const selected = agents[Math.floor(Math.random() * agents.length)];
      const p = selected.prices[Math.floor(Math.random() * selected.prices.length)];
      const day = Math.floor(Math.random() * 30) + 1;
      const statuses = ["CLEARANCE_SALE", "SCARCITY_SURGE", "YIELD_MAX", "OPTIMAL_STEP", "PENALTY_AVERTED"];
      const status = statuses[Math.floor(Math.random() * statuses.length)];

      setTickerItems((prev) => [
        {
          agent: selected.name,
          price: `$${p}`,
          day,
          status,
          gain: `+$${p}`,
          color: selected.color,
        },
        ...prev.slice(0, 12),
      ]);
    }, 3200);

    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-30 w-full border-b border-white/[0.08] bg-[#0d0d1a]/85 backdrop-blur-xl">
      {/* Top Main Navigation Bar */}
      <div className="flex items-center justify-between px-6 py-3">
        {/* Left: Terminal Brand & Status */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-[#ffd700]/20 to-[#9c27b0]/20 border border-[#ffd700]/40 shadow-glow-gold">
              <Zap className="h-5 w-5 text-[#ffd700]" />
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#00e676] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-[#00e676]"></span>
              </span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold tracking-tight text-white text-base font-sans">
                  PRICING<span className="text-[#ffd700]">.RL</span>
                </span>
                <span className="rounded bg-[#ffd700]/10 px-1.5 py-0.5 text-[10px] font-mono font-semibold text-[#ffd700] border border-[#ffd700]/30">
                  TERMINAL v4.2
                </span>
              </div>
              <p className="text-[11px] font-mono text-slate-400">
                Autonomous Revenue & Yield Engine // PyTorch
              </p>
            </div>
          </div>

          <div className="hidden lg:flex items-center gap-2 pl-4 border-l border-white/10 text-xs">
            <div className="flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-2.5 py-1 text-emerald-400 border border-emerald-500/20 font-mono">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              MARKET ACTIVE
            </div>
            <div className="flex items-center gap-1 rounded-full bg-white/5 px-2.5 py-1 text-slate-300 font-mono text-[11px]">
              <Cpu className="h-3 w-3 text-purple-400" />
              <span>MDP: 1,581 States</span>
            </div>
          </div>
        </div>

        {/* Center: Live Season Counter */}
        <div className="flex items-center gap-3 bg-black/40 border border-white/10 rounded-xl px-4 py-1.5 shadow-inner">
          <div className="text-right">
            <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 flex items-center justify-end gap-1">
              <Activity className="h-3 w-3 text-[#ffd700] animate-pulse" />
              Live Season Index
            </div>
            <div className="text-base font-mono font-bold text-white tracking-wide">
              SEASON <span className="text-[#ffd700]">#{currentSeason.toLocaleString()}</span>
              <span className="text-xs text-slate-500 font-normal ml-1">/ 1,000+</span>
            </div>
          </div>

          <div className="flex items-center gap-1 border-l border-white/10 pl-3">
            <button
              onClick={() => setIsAutoSeason(!isAutoSeason)}
              className={`p-1.5 rounded-lg border transition-all text-xs flex items-center gap-1 font-mono ${
                isAutoSeason
                  ? "bg-[#ffd700]/20 border-[#ffd700]/50 text-[#ffd700] shadow-glow-gold"
                  : "bg-white/5 border-white/10 text-slate-400 hover:text-white hover:bg-white/10"
              }`}
              title={isAutoSeason ? "Pause Live Counter" : "Resume Auto Increment"}
            >
              {isAutoSeason ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
              <span className="hidden sm:inline text-[11px]">
                {isAutoSeason ? "Ticking" : "Paused"}
              </span>
            </button>
            <button
              onClick={() => onSeasonChange(currentSeason + 1)}
              className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 hover:text-white transition-all"
              title="Next Season Step"
            >
              <RotateCw className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        {/* Right: Quick Telemetry & Status Badges */}
        <div className="flex items-center gap-3">
          <div className="hidden md:flex flex-col text-right">
            <span className="text-[11px] font-mono text-slate-400">Best Model:</span>
            <span className="text-xs font-mono font-semibold text-[#ffd700] flex items-center justify-end gap-1">
              <ShieldCheck className="h-3.5 w-3.5 text-[#00e676]" />
              PPO #1 (p &lt; 0.05)
            </span>
          </div>

          <div className="flex items-center gap-2 rounded-xl bg-purple-950/30 border border-purple-500/20 px-3 py-1.5">
            <div className="text-right">
              <div className="text-[10px] font-mono text-purple-300">Alpha Uplift</div>
              <div className="text-xs font-mono font-bold text-[#ffd700] flex items-center gap-0.5">
                <TrendingUp className="h-3 w-3 text-emerald-400" />
                +18.2%
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Ticker Stream: Bloomberg Terminal Style */}
      <div className="relative flex items-center h-8 overflow-hidden bg-black/60 border-t border-white/[0.05] text-[11px] font-mono">
        <div className="shrink-0 flex items-center gap-1.5 px-3 bg-[#ffd700]/15 text-[#ffd700] border-r border-[#ffd700]/30 h-full font-bold z-10">
          <Terminal className="h-3 w-3" />
          <span>ORDER FEED</span>
        </div>

        <div className="flex items-center space-x-6 animate-ticker whitespace-nowrap pl-4 py-1 text-slate-300">
          {tickerItems.concat(tickerItems).map((item, idx) => (
            <div key={idx} className="inline-flex items-center gap-2 shrink-0">
              <span 
                className="font-bold px-1.5 py-0.2 rounded text-[10px]"
                style={{ backgroundColor: `${item.color}20`, color: item.color, border: `1px solid ${item.color}40` }}
              >
                {item.agent}
              </span>
              <span className="text-slate-400">Day {item.day}</span>
              <span className="text-white font-semibold">{item.price}</span>
              <span className="text-slate-400 text-[10px]">[{item.status}]</span>
              <span className="text-emerald-400 font-bold">{item.gain}</span>
              <span className="text-slate-600">|</span>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}
