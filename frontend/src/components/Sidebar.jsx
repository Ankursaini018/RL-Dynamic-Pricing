import React from "react";
import {
  LayoutDashboard,
  Swords,
  TrendingDown,
  LineChart,
  Calculator,
  ShieldCheck,
  CheckCircle2,
  ChevronRight,
  Sparkles,
  GitBranch,
} from "lucide-react";

export default function Sidebar({ activePage, setActivePage }) {
  const navItems = [
    {
      id: "dashboard",
      name: "Dashboard",
      subtitle: "Main Overview & KPIs",
      icon: LayoutDashboard,
      badge: "PROD",
      badgeColor: "gold",
    },
    {
      id: "arena",
      name: "Agent Arena",
      subtitle: "Live Multi-Agent Race",
      icon: Swords,
      badge: "LIVE",
      badgeColor: "coral",
    },
    {
      id: "trajectory",
      name: "Price Trajectory",
      subtitle: "Behavior & Proof",
      icon: TrendingDown,
      badge: "PROVED",
      badgeColor: "emerald",
    },
    {
      id: "training",
      name: "Training Progress",
      subtitle: "Curves & Q-Heatmap",
      icon: LineChart,
      badge: "2k Eps",
      badgeColor: "purple",
    },
    {
      id: "calculator",
      name: "Business Value",
      subtitle: "Enterprise ROI Engine",
      icon: Calculator,
      badge: "ROI",
      badgeColor: "gold",
    },
  ];

  return (
    <aside className="hidden md:flex w-64 shrink-0 flex-col justify-between border-r border-white/[0.08] bg-[#0d0d1a]/90 backdrop-blur-xl min-h-[calc(100vh-6.5rem)] p-4 select-none">
      {/* Navigation Links */}
      <div className="space-y-6">
        <div>
          <div className="px-3 pb-2 text-[10px] font-mono uppercase tracking-widest text-slate-400 flex items-center justify-between">
            <span>Terminal Modules</span>
            <span className="text-[9px] bg-white/5 px-1.5 py-0.5 rounded text-slate-400">
              5/5 READY
            </span>
          </div>

          <nav className="space-y-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activePage === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => setActivePage(item.id)}
                  className={`group relative flex w-full items-center justify-between rounded-xl px-3.5 py-3 text-left transition-all duration-200 ${
                    isActive
                      ? "bg-gradient-to-r from-[#ffd700]/15 to-[#9c27b0]/10 text-white border border-[#ffd700]/30 shadow-glass-gold"
                      : "text-slate-400 hover:text-white hover:bg-white/[0.04] border border-transparent"
                  }`}
                >
                  {/* Left accent bar on active */}
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 rounded-r-full bg-[#ffd700] shadow-glow-gold" />
                  )}

                  <div className="flex items-center gap-3">
                    <div
                      className={`flex h-8 w-8 items-center justify-center rounded-lg transition-colors ${
                        isActive
                          ? "bg-[#ffd700] text-black shadow-glow-gold"
                          : "bg-white/5 text-slate-400 group-hover:text-white group-hover:bg-white/10"
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                    </div>

                    <div>
                      <div className="text-sm font-semibold tracking-tight">
                        {item.name}
                      </div>
                      <div className="text-[11px] font-mono text-slate-400 group-hover:text-slate-300">
                        {item.subtitle}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-1.5">
                    {item.badge && (
                      <span
                        className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ${
                          isActive
                            ? "bg-[#ffd700]/20 text-[#ffd700] border border-[#ffd700]/40"
                            : "bg-white/5 text-slate-400 border border-white/10"
                        }`}
                      >
                        {item.badge}
                      </span>
                    )}
                    <ChevronRight
                      className={`h-3.5 w-3.5 transition-transform ${
                        isActive ? "text-[#ffd700] translate-x-0.5" : "text-slate-600 opacity-0 group-hover:opacity-100"
                      }`}
                    />
                  </div>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Legend / Agent Color Code Section */}
        <div className="rounded-xl border border-white/[0.06] bg-black/30 p-3">
          <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 mb-2.5 flex items-center justify-between">
            <span>Agent Spectrum</span>
            <span className="text-[10px] text-[#ffd700]">7 Agents</span>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-mono">
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-[#ffd700] shadow-[0_0_6px_#ffd700]"></span>
              <span className="text-slate-200">PPO (RL)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-[#ff6b6b] shadow-[0_0_6px_#ff6b6b]"></span>
              <span className="text-slate-200">DQN</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-[#00e676] shadow-[0_0_6px_#00e676]"></span>
              <span className="text-slate-200">Q-Learning</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-[#64b5f6] shadow-[0_0_6px_#64b5f6]"></span>
              <span className="text-slate-200">Baseline</span>
            </div>
          </div>
        </div>
      </div>

      {/* System Integrity & Info Card at bottom */}
      <div className="mt-6 rounded-xl border border-[#9c27b0]/25 bg-gradient-to-b from-[#16162a]/90 to-[#0d0d1a] p-3 text-xs shadow-glass-purple">
        <div className="flex items-center justify-between text-slate-300 font-mono text-[11px] mb-2 pb-1.5 border-b border-white/10">
          <span className="flex items-center gap-1 text-[#ffd700]">
            <Sparkles className="h-3 w-3" />
            Model Integrity
          </span>
          <span className="text-emerald-400 flex items-center gap-0.5">
            <CheckCircle2 className="h-3 w-3" /> 26/26 Unit
          </span>
        </div>

        <div className="space-y-1.5 text-[11px] font-mono text-slate-400">
          <div className="flex justify-between">
            <span>Statistical Proof:</span>
            <span className="text-white font-semibold">p &lt; 0.05</span>
          </div>
          <div className="flex justify-between">
            <span>Inventory Space:</span>
            <span className="text-white">50 units / 30d</span>
          </div>
          <div className="flex justify-between">
            <span>Price Granularity:</span>
            <span className="text-[#ffd700]">6 discrete ($50-$300)</span>
          </div>
        </div>

        <div className="mt-2.5 pt-2 border-t border-white/[0.06] flex items-center justify-between text-[10px] text-slate-400">
          <span className="flex items-center gap-1">
            <GitBranch className="h-2.5 w-2.5 text-purple-400" />
            main @ Ankursaini018
          </span>
          <span className="text-slate-300">v4.2</span>
        </div>
      </div>
    </aside>
  );
}
