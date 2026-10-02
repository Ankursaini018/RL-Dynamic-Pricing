import React, { useState, useEffect } from "react";
import { Trophy, Crown, Sparkles, X } from "lucide-react";
import confetti from "canvas-confetti";

export default function ChampionAnnouncement() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Reveal after 2 seconds on Dashboard load
    const showTimer = setTimeout(() => {
      setIsVisible(true);

      // Gold confetti burst
      confetti({
        particleCount: 120,
        spread: 90,
        origin: { y: 0.5 },
        colors: ["#ffd700", "#ffe55c", "#fffae0", "#ff9800"],
      });

      // Disappear after 3 seconds of being shown (total 2s + 3s = 5s)
      const hideTimer = setTimeout(() => {
        setIsVisible(false);
      }, 3000);

      return () => clearTimeout(hideTimer);
    }, 2000);

    return () => clearTimeout(showTimer);
  }, []);

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none animate-fadeIn">
      {/* Backdrop glow */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm pointer-events-auto" onClick={() => setIsVisible(false)} />

      {/* Dramatic Modal Content */}
      <div className="relative z-10 pointer-events-auto max-w-md w-full rounded-3xl p-8 bg-gradient-to-b from-[#1a1532] via-[#120f26] to-[#0d0d1a] border-2 border-[#ffd700] shadow-[0_0_50px_rgba(255,215,0,0.55)] text-center space-y-4 animate-fight-clash">
        {/* Close Button */}
        <button
          onClick={() => setIsVisible(false)}
          className="absolute top-4 right-4 p-1.5 rounded-full bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white"
        >
          <X className="h-4 w-4" />
        </button>

        {/* Animated Trophy Icon with Crown */}
        <div className="relative mx-auto flex h-24 w-24 items-center justify-center rounded-2xl bg-gradient-to-tr from-[#ffd700] via-[#ffe55c] to-[#ffb300] text-black shadow-glow-gold animate-bounce">
          <Trophy className="h-14 w-14" />
          <Crown className="absolute -top-3 h-8 w-8 text-[#ffd700] animate-pulse" />
        </div>

        <div className="space-y-1">
          <div className="text-xs font-mono font-bold tracking-widest text-[#ffd700] uppercase">
            Official Simulation Verdict
          </div>
          <h2 className="text-4xl font-extrabold tracking-tight text-white font-sans drop-shadow-md">
            PPO WINS!
          </h2>
          <div className="text-sm font-mono text-emerald-400 font-bold">
            Rank #1 of 7 Algorithms ($4,850 Revenue)
          </div>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed font-sans">
          Proximal Policy Optimization achieved statistical supremacy with{" "}
          <strong className="text-[#ffd700]">+18.3% alpha</strong> over heuristic baselines and zero stockout penalties.
        </p>

        <div className="pt-2 flex justify-center">
          <button
            onClick={() => setIsVisible(false)}
            className="px-6 py-2 rounded-xl bg-[#ffd700] text-black font-mono font-bold text-xs shadow-glow-gold hover:bg-[#ffe55c] transition-all"
          >
            ENTER DASHBOARD
          </button>
        </div>
      </div>
    </div>
  );
}
