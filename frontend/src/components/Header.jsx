import React, { useState, useEffect, useRef } from "react";
import { 
  Zap, 
  Activity, 
  ShieldCheck, 
  Terminal, 
  Play, 
  Pause, 
  RotateCw,
  TrendingUp,
  Cpu,
  Trophy
} from "lucide-react";
import confetti from "canvas-confetti";
import EasterEggModal from "./EasterEggModal";

export default function Header({ 
  currentSeason, 
  onSeasonChange, 
  isAutoSeason, 
  setIsAutoSeason 
}) {
  // Easter egg click counter
  const [clickCount, setClickCount] = useState(0);
  const [isEasterEggOpen, setIsEasterEggOpen] = useState(false);
  const clickTimerRef = useRef(null);

  const handleLogoClick = () => {
    setClickCount((prev) => {
      const next = prev + 1;
      if (next >= 5) {
        setIsEasterEggOpen(true);
        confetti({
          particleCount: 100,
          spread: 80,
          origin: { y: 0.4 },
          colors: ["#ffd700", "#ff6b6b", "#00e676", "#9c27b0"],
        });
        return 0;
      }
      return next;
    });

    if (clickTimerRef.current) clearTimeout(clickTimerRef.current);
    clickTimerRef.current = setTimeout(() => {
      setClickCount(0);
    }, 1500);
  };

  // Recent season results ticker for Requirement 3
  const [seasonTickerItems] = useState([
    "Season 1247: PPO $4,892 | DQN $4,401 | QL $4,089 | TimeBased $4,120",
    "Season 1248: PPO $4,910 | DQN $4,450 | QL $4,115 | TimeBased $4,130",
    "Season 1249: PPO $4,875 | DQN $4,395 | QL $4,095 | FixedPrice $3,890",
    "Season 1250: PPO $4,930 | DQN $4,460 | QL $4,140 | LinearDecay $3,750",
    "Season 1251: PPO $4,880 | DQN $4,410 | QL $4,105 | TimeBased $4,110",
  ]);

  return (
    <>
      <header className="sticky top-0 z-30 w-full border-b border-white/[0.08] bg-[#0d0d1a]/90 backdrop-blur-xl">
        {/* Top Main Navigation Bar */}
        <div className="flex items-center justify-between px-4 sm:px-6 py-3">
          {/* Left: Terminal Brand & Logo with Easter Egg Click Handler */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleLogoClick}
              className="group relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-[#ffd700]/20 to-[#9c27b0]/20 border border-[#ffd700]/40 shadow-glow-gold transition-transform active:scale-90"
              title="PPO Engine // Click 5x for Easter Egg"
            >
              <Zap className="h-5 w-5 text-[#ffd700] group-hover:scale-110 transition-transform" />
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#00e676] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-[#00e676]"></span>
              </span>
            </button>

            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold tracking-tight text-white text-base font-sans">
                  PRICING<span className="text-[#ffd700]">.RL</span>
                </span>
                <span className="rounded bg-[#ffd700]/10 px-1.5 py-0.5 text-[10px] font-mono font-semibold text-[#ffd700] border border-[#ffd700]/30">
                  TERMINAL v4.2
                </span>
              </div>
              <p className="text-[11px] font-mono text-slate-400 hidden sm:block">
                Autonomous Revenue &amp; Yield Engine // PyTorch
              </p>
            </div>
          </div>

          {/* Center: Live Season Counter */}
          <div className="flex items-center gap-3 bg-black/40 border border-white/10 rounded-xl px-3 sm:px-4 py-1.5 shadow-inner">
            <div className="text-right">
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 flex items-center justify-end gap-1">
                <Activity className="h-3 w-3 text-[#ffd700] animate-pulse" />
                Live Season Index
              </div>
              <div className="text-xs sm:text-base font-mono font-bold text-white tracking-wide">
                SEASON <span className="text-[#ffd700]">#{currentSeason.toLocaleString()}</span>
                <span className="text-xs text-slate-500 font-normal ml-1 hidden sm:inline">/ 1,000+</span>
              </div>
            </div>

            <div className="flex items-center gap-1 border-l border-white/10 pl-2 sm:pl-3">
              <button
                onClick={() => setIsAutoSeason(!isAutoSeason)}
                className={`p-1.5 rounded-lg border transition-all text-xs flex items-center gap-1 font-mono ${
                  isAutoSeason
                    ? "bg-[#ffd700]/20 border-[#ffd700]/50 text-[#ffd700] shadow-glow-gold"
                    : "bg-white/5 border-white/10 text-slate-400 hover:text-white"
                }`}
                title={isAutoSeason ? "Pause Live Counter" : "Resume Auto Increment"}
              >
                {isAutoSeason ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
              </button>
              <button
                onClick={() => onSeasonChange(currentSeason + 1)}
                className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 hover:text-white transition-all hidden sm:block"
                title="Next Season Step"
              >
                <RotateCw className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          {/* Right: Quick Telemetry Badges */}
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="hidden lg:flex flex-col text-right">
              <span className="text-[11px] font-mono text-slate-400">Champion Agent:</span>
              <span className="text-xs font-mono font-semibold text-[#ffd700] flex items-center justify-end gap-1">
                <Trophy className="h-3.5 w-3.5 text-[#ffd700]" />
                PPO #1 (p &lt; 0.05)
              </span>
            </div>

            <div className="flex items-center gap-1.5 rounded-xl bg-purple-950/30 border border-purple-500/20 px-2.5 sm:px-3 py-1.5 text-xs font-mono">
              <TrendingUp className="h-3.5 w-3.5 text-emerald-400" />
              <span className="font-bold text-[#ffd700]">+18.3%</span>
              <span className="text-slate-400 text-[10px] hidden sm:inline">Alpha</span>
            </div>
          </div>
        </div>

        {/* ────────────────────────────────────────────────────────── */}
        {/* REQUIREMENT 3: LIVE TICKER AT TOP (SEASON RESULTS)         */}
        {/* ────────────────────────────────────────────────────────── */}
        <div className="relative flex items-center h-8 overflow-hidden bg-black/70 border-t border-white/[0.06] text-[11px] font-mono">
          <div className="shrink-0 flex items-center gap-1.5 px-3 bg-[#ffd700]/15 text-[#ffd700] border-r border-[#ffd700]/30 h-full font-bold z-10">
            <Terminal className="h-3 w-3" />
            <span className="hidden sm:inline">LIVE SEASONS</span>
          </div>

          {/* Smooth Infinite Scrolling Banner */}
          <div className="flex items-center space-x-8 animate-ticker whitespace-nowrap pl-4 py-1 text-slate-300">
            {seasonTickerItems.concat(seasonTickerItems).concat(seasonTickerItems).map((result, idx) => (
              <div key={idx} className="inline-flex items-center gap-2 shrink-0">
                <span className="text-white font-semibold">{result}</span>
                <span className="text-slate-600">///</span>
              </div>
            ))}
          </div>
        </div>
      </header>

      {/* Easter Egg Modal */}
      <EasterEggModal isOpen={isEasterEggOpen} onClose={() => setIsEasterEggOpen(false)} />
    </>
  );
}
