import React from "react";
import { Sparkles, X, Bot, Heart } from "lucide-react";

export default function EasterEggModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fadeIn">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-md" onClick={onClose} />

      {/* Modal */}
      <div className="relative z-10 max-w-sm w-full rounded-3xl p-6 bg-gradient-to-b from-[#1b1535] to-[#0d0d1a] border-2 border-[#ffd700] shadow-[0_0_50px_rgba(255,215,0,0.5)] text-center space-y-4 animate-fight-clash">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1 rounded-full bg-white/10 hover:bg-white/20 text-slate-300"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[#ffd700]/20 border border-[#ffd700] text-[#ffd700] shadow-glow-gold">
          <Bot className="h-9 w-9" />
        </div>

        <div className="space-y-1">
          <div className="text-xs font-mono font-bold uppercase tracking-widest text-[#ffd700] flex items-center justify-center gap-1">
            <Sparkles className="h-3.5 w-3.5" />
            Secret Easter Egg Unlocked!
          </div>
          <h3 className="text-xl font-bold text-white font-sans">
            Fun fact: PPO trains ChatGPT too!
          </h3>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed font-sans">
          The exact same algorithm optimizing ticket prices in this dashboard—<strong>Proximal Policy Optimization (PPO)</strong>—is 
          the foundational Reinforcement Learning from Human Feedback (RLHF) engine that aligns models like ChatGPT and Claude!
        </p>

        <div className="pt-2">
          <button
            onClick={onClose}
            className="w-full py-2.5 rounded-xl bg-[#ffd700] text-black font-mono font-bold text-xs shadow-glow-gold hover:bg-[#ffe55c] transition-all"
          >
            Awesome! 🚀
          </button>
        </div>
      </div>
    </div>
  );
}
