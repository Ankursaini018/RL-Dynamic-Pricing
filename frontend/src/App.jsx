import React, { useState, useEffect } from "react";
import {
  LayoutDashboard,
  Swords,
  TrendingDown,
  LineChart,
  Calculator,
} from "lucide-react";
import ParticleBackground from "./components/ParticleBackground";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import DashboardPage from "./pages/DashboardPage";
import AgentArenaPage from "./pages/AgentArenaPage";
import PriceTrajectoryPage from "./pages/PriceTrajectoryPage";
import TrainingProgressPage from "./pages/TrainingProgressPage";
import BusinessValuePage from "./pages/BusinessValuePage";

const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "arena", label: "Arena", icon: Swords },
  { id: "trajectory", label: "Trajectory", icon: TrendingDown },
  { id: "training", label: "Training", icon: LineChart },
  { id: "calculator", label: "Calculator", icon: Calculator },
];

export default function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [currentSeason, setCurrentSeason] = useState(1482);
  const [isAutoSeason, setIsAutoSeason] = useState(true);

  // Live season counter ticking
  useEffect(() => {
    let interval;
    if (isAutoSeason) {
      interval = setInterval(() => {
        setCurrentSeason((s) => s + 1);
      }, 4500);
    }
    return () => clearInterval(interval);
  }, [isAutoSeason]);

  return (
    <div className="relative min-h-screen bg-[#0d0d1a] text-slate-100 font-sans selection:bg-[#ffd700] selection:text-black">
      {/* Animated Subtle Floating Particle Background */}
      <ParticleBackground />

      {/* Grid Pattern Overlay for Bloomberg terminal ambiance */}
      <div className="fixed inset-0 pointer-events-none z-0 bg-grid-pattern opacity-60" />

      {/* Main App Layout */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Top Header */}
        <Header
          currentSeason={currentSeason}
          onSeasonChange={setCurrentSeason}
          isAutoSeason={isAutoSeason}
          setIsAutoSeason={setIsAutoSeason}
        />

        {/* Content Body: Sidebar + Main Content Area */}
        <div className="flex flex-1 overflow-hidden">
          {/* Left Sidebar Navigation (Desktop) */}
          <Sidebar
            activePage={activePage}
            setActivePage={setActivePage}
          />

          {/* Main Page Viewport */}
          <main className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 lg:px-8 max-w-[1700px] w-full mx-auto pb-20 md:pb-6">
            {activePage === "dashboard" && (
              <DashboardPage onNavigate={setActivePage} />
            )}
            {activePage === "arena" && <AgentArenaPage />}
            {activePage === "trajectory" && <PriceTrajectoryPage />}
            {activePage === "training" && <TrainingProgressPage />}
            {activePage === "calculator" && <BusinessValuePage />}
          </main>
        </div>

        {/* Mobile Bottom Navigation Bar */}
        <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#0d0d1a]/95 backdrop-blur-xl border-t border-white/10 px-2 py-2 flex justify-around items-center shadow-2xl">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                className={`flex flex-col items-center gap-1 py-1 px-2.5 rounded-lg transition-all ${
                  isActive
                    ? "text-[#ffd700] font-bold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? "text-[#ffd700]" : "text-slate-400"}`} />
                <span className="text-[10px] font-mono tracking-tight">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
