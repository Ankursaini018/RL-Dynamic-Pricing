import React, { useState, useEffect } from "react";
import ParticleBackground from "./components/ParticleBackground";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import DashboardPage from "./pages/DashboardPage";
import AgentArenaPage from "./pages/AgentArenaPage";
import PriceTrajectoryPage from "./pages/PriceTrajectoryPage";
import TrainingProgressPage from "./pages/TrainingProgressPage";
import BusinessValuePage from "./pages/BusinessValuePage";

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
          {/* Left Sidebar Navigation */}
          <Sidebar
            activePage={activePage}
            setActivePage={setActivePage}
          />

          {/* Main Page Viewport */}
          <main className="flex-1 overflow-y-auto px-6 py-6 lg:px-8 max-w-[1700px] w-full mx-auto">
            {activePage === "dashboard" && (
              <DashboardPage onNavigate={setActivePage} />
            )}
            {activePage === "arena" && <AgentArenaPage />}
            {activePage === "trajectory" && <PriceTrajectoryPage />}
            {activePage === "training" && <TrainingProgressPage />}
            {activePage === "calculator" && <BusinessValuePage />}
          </main>
        </div>
      </div>
    </div>
  );
}
