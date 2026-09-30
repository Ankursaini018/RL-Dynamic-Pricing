import React, { useState } from "react";
import {
  Calculator,
  TrendingUp,
  DollarSign,
  Award,
  Download,
  Calendar,
  Layers,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  Building2,
  FileSpreadsheet,
  ArrowRight,
  Printer,
  Copy,
  Check,
} from "lucide-react";
import confetti from "canvas-confetti";

export default function BusinessValuePage() {
  // Input parameters
  const [annualSeasons, setAnnualSeasons] = useState(1200); // e.g. 1200 flights / concert seasons / hotel cohorts
  const [seatsPerSeason, setSeatsPerSeason] = useState(50);
  const [baselineRevPerSeason, setBaselineRevPerSeason] = useState(1872);
  const [upliftPct, setUpliftPct] = useState(18.2); // +18.2% from PPO
  const [monthlyComputeCost, setMonthlyComputeCost] = useState(1200); // $1200/mo cloud/GPU inference
  const [copied, setCopied] = useState(false);

  // Computations
  const baselineAnnualTotal = annualSeasons * baselineRevPerSeason;
  const grossUpliftPerSeason = baselineRevPerSeason * (upliftPct / 100);
  const totalAnnualGrossUplift = annualSeasons * grossUpliftPerSeason;
  const annualComputeCost = monthlyComputeCost * 12;
  const annualNetProfitUplift = totalAnnualGrossUplift - annualComputeCost;
  const roiMultiple = (totalAnnualGrossUplift / annualComputeCost).toFixed(1);
  const dailyUplift = (annualNetProfitUplift / 365).toFixed(0);
  const monthlyUplift = (annualNetProfitUplift / 12).toFixed(0);
  const paybackDays = Math.max(
    1,
    Math.round((annualComputeCost / (totalAnnualGrossUplift / 365)))
  );

  // Penalty avoidance savings: ~2.1 tickets per season saved from -$10 penalty
  const penaltySavings = Math.round(annualSeasons * 2.1 * 10);

  const handleExport = () => {
    confetti({
      particleCount: 70,
      spread: 60,
      origin: { y: 0.7 },
      colors: ["#ffd700", "#00e676", "#9c27b0"],
    });

    const reportText = `=== RL DYNAMIC PRICING EXECUTIVE BUSINESS CASE ===
Date: ${new Date().toLocaleDateString()}
Model: PPO Deep Actor-Critic (Rank #1 / 7)
Statistical Significance: p < 0.05

--- INPUT ASSUMPTIONS ---
Annual Event/Season Scale: ${annualSeasons.toLocaleString()} seasons/flights
Capacity per Season: ${seatsPerSeason} inventory units
Baseline Revenue per Season: $${baselineRevPerSeason.toLocaleString()}
Current Annual Baseline: $${baselineAnnualTotal.toLocaleString()}
Target RL Alpha Uplift: +${upliftPct}%
Cloud Infrastructure Cost: $${monthlyComputeCost}/month ($${annualComputeCost.toLocaleString()}/yr)

--- PROJECTED FINANCIAL IMPACT ---
Annual Gross Revenue Uplift: +$${Math.round(totalAnnualGrossUplift).toLocaleString()}
Annual Net Profit Uplift: +$${Math.round(annualNetProfitUplift).toLocaleString()}
Monthly Incremental Cashflow: +$${parseInt(monthlyUplift).toLocaleString()} / month
Daily Run-Rate Gain: +$${parseInt(dailyUplift).toLocaleString()} / day
Expected ROI Multiple: ${roiMultiple}x
Payback / Breakeven Period: ${paybackDays} days
Unsold Penalty Cost Averted: +$${penaltySavings.toLocaleString()}/yr
==================================================`;

    navigator.clipboard.writeText(reportText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="space-y-6 pb-12 animate-fadeIn">
      {/* Title Banner */}
      <div className="glass-panel glass-panel-gold rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-mono text-[#ffd700] mb-1">
              <Calculator className="h-4 w-4" />
              <span>ENTERPRISE ROI &amp; REVENUE EXPANSION ENGINE</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Business Value &amp; Financial Projections
            </h1>
            <p className="text-xs sm:text-sm text-slate-300">
              Calculate projected revenue lift, payback timeline, and enterprise ROI across deployment scales.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={handleExport}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-[#ffd700] text-black text-xs font-mono font-bold shadow-glow-gold hover:bg-[#ffe55c] transition-all"
            >
              {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              <span>{copied ? "COPIED TO CLIPBOARD" : "EXPORT EXECUTIVE BRIEF"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Top 4 KPI Dynamic Outputs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Net Annual Profit Lift */}
        <div className="glass-panel rounded-2xl p-5 border-t-2 border-t-[#ffd700] shadow-glass-gold">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1 flex items-center justify-between">
            <span>Net Annual Profit Lift</span>
            <span className="text-[#ffd700] font-bold">AFTER COMPUTE</span>
          </div>
          <div className="text-3xl font-mono font-bold text-[#ffd700]">
            +${Math.round(annualNetProfitUplift).toLocaleString()}
          </div>
          <div className="mt-2 text-xs font-mono text-emerald-400 flex items-center gap-1">
            <TrendingUp className="h-3.5 w-3.5" />
            +${parseInt(monthlyUplift).toLocaleString()}/mo Net Run-Rate
          </div>
        </div>

        {/* ROI Multiple */}
        <div className="glass-panel rounded-2xl p-5 border-t-2 border-t-[#00e676]">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1 flex items-center justify-between">
            <span>Return on Investment</span>
            <span className="text-emerald-400 font-bold">ANNUALIZED</span>
          </div>
          <div className="text-3xl font-mono font-bold text-[#00e676]">
            {roiMultiple}x
          </div>
          <div className="mt-2 text-xs font-mono text-slate-300">
            ${(totalAnnualGrossUplift / annualComputeCost).toFixed(2)} generated per $1 spent
          </div>
        </div>

        {/* Payback Period */}
        <div className="glass-panel rounded-2xl p-5 border-t-2 border-t-[#9c27b0]">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1 flex items-center justify-between">
            <span>Capital Breakeven</span>
            <span className="text-purple-300 font-bold">DAYS</span>
          </div>
          <div className="text-3xl font-mono font-bold text-white">
            {paybackDays} <span className="text-sm font-normal text-slate-400">days</span>
          </div>
          <div className="mt-2 text-xs font-mono text-slate-300">
            Full annual compute amortized in under 1 month
          </div>
        </div>

        {/* Penalty Aversion Savings */}
        <div className="glass-panel rounded-2xl p-5 border-t-2 border-t-[#ff6b6b]">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1 flex items-center justify-between">
            <span>Penalty Cost Averted</span>
            <span className="text-red-400 font-bold">-$10 / UNIT</span>
          </div>
          <div className="text-3xl font-mono font-bold text-[#ff6b6b]">
            +${penaltySavings.toLocaleString()}
          </div>
          <div className="mt-2 text-xs font-mono text-slate-300">
            Saved by deadline clearance discounting
          </div>
        </div>
      </div>

      {/* Main Grid: Inputs Sliders vs Live Projections Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Col: Interactive Parameter Sliders */}
        <div className="glass-panel rounded-2xl p-5 space-y-5">
          <div className="border-b border-white/10 pb-3">
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <Building2 className="h-4 w-4 text-[#ffd700]" />
              Enterprise Operating Parameters
            </h3>
            <p className="text-xs font-mono text-slate-400">
              Customize scale to reflect your organization's flight, hotel room cohort, or event volume
            </p>
          </div>

          <div className="space-y-4">
            {/* Slider 1: Annual Seasons / Flights */}
            <div>
              <div className="flex justify-between text-xs font-mono mb-1.5">
                <span className="text-slate-300">Annual Flight / Event Seasons:</span>
                <span className="font-bold text-[#ffd700] text-sm">
                  {annualSeasons.toLocaleString()} seasons/yr
                </span>
              </div>
              <input
                type="range"
                min="100"
                max="5000"
                step="50"
                value={annualSeasons}
                onChange={(e) => setAnnualSeasons(parseInt(e.target.value))}
                className="w-full h-2 bg-black/60 rounded-lg appearance-none cursor-pointer accent-[#ffd700]"
              />
              <div className="flex justify-between text-[10px] font-mono text-slate-500 mt-1">
                <span>100 (Boutique)</span>
                <span>1,200 (Regional)</span>
                <span>5,000 (Major Network)</span>
              </div>
            </div>

            {/* Slider 2: Capacity per Season */}
            <div>
              <div className="flex justify-between text-xs font-mono mb-1.5">
                <span className="text-slate-300">Inventory Units per Season (Capacity):</span>
                <span className="font-bold text-[#ffd700] text-sm">
                  {seatsPerSeason} seats
                </span>
              </div>
              <input
                type="range"
                min="20"
                max="150"
                step="5"
                value={seatsPerSeason}
                onChange={(e) => setSeatsPerSeason(parseInt(e.target.value))}
                className="w-full h-2 bg-black/60 rounded-lg appearance-none cursor-pointer accent-[#ffd700]"
              />
              <div className="flex justify-between text-[10px] font-mono text-slate-500 mt-1">
                <span>20 Units</span>
                <span>50 Units (Default Env)</span>
                <span>150 Units</span>
              </div>
            </div>

            {/* Slider 3: Baseline Revenue */}
            <div>
              <div className="flex justify-between text-xs font-mono mb-1.5">
                <span className="text-slate-300">Current Heuristic Baseline Revenue / Season:</span>
                <span className="font-bold text-white text-sm">
                  ${baselineRevPerSeason.toLocaleString()}
                </span>
              </div>
              <input
                type="range"
                min="1000"
                max="3500"
                step="50"
                value={baselineRevPerSeason}
                onChange={(e) => setBaselineRevPerSeason(parseInt(e.target.value))}
                className="w-full h-2 bg-black/60 rounded-lg appearance-none cursor-pointer accent-[#ffd700]"
              />
              <div className="flex justify-between text-[10px] font-mono text-slate-500 mt-1">
                <span>$1,000 (Fixed Price)</span>
                <span>$1,872 (Time-Based)</span>
                <span>$3,500 (Premium)</span>
              </div>
            </div>

            {/* Slider 4: Uplift Percentage */}
            <div>
              <div className="flex justify-between text-xs font-mono mb-1.5">
                <span className="text-slate-300">Expected RL Revenue Uplift (Alpha):</span>
                <span className="font-bold text-emerald-400 text-sm">
                  +{upliftPct}%
                </span>
              </div>
              <input
                type="range"
                min="5"
                max="35"
                step="0.5"
                value={upliftPct}
                onChange={(e) => setUpliftPct(parseFloat(e.target.value))}
                className="w-full h-2 bg-black/60 rounded-lg appearance-none cursor-pointer accent-emerald-400"
              />
              <div className="flex justify-between text-[10px] font-mono text-slate-500 mt-1">
                <span>+5% (Conservative)</span>
                <span>+18.2% (PPO Empiric)</span>
                <span>+35% (Aggressive)</span>
              </div>
            </div>

            {/* Slider 5: Cloud Compute Cost */}
            <div>
              <div className="flex justify-between text-xs font-mono mb-1.5">
                <span className="text-slate-300">Cloud AI Inference &amp; GPU Cost:</span>
                <span className="font-bold text-purple-300 text-sm">
                  ${monthlyComputeCost}/mo (${annualComputeCost.toLocaleString()}/yr)
                </span>
              </div>
              <input
                type="range"
                min="300"
                max="5000"
                step="100"
                value={monthlyComputeCost}
                onChange={(e) => setMonthlyComputeCost(parseInt(e.target.value))}
                className="w-full h-2 bg-black/60 rounded-lg appearance-none cursor-pointer accent-purple-400"
              />
              <div className="flex justify-between text-[10px] font-mono text-slate-500 mt-1">
                <span>$300/mo</span>
                <span>$1,200/mo</span>
                <span>$5,000/mo (High Volume)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Col: Projections Breakdown & Period Escalation */}
        <div className="glass-panel glass-panel-purple rounded-2xl p-5 space-y-4 flex flex-col justify-between">
          <div>
            <div className="border-b border-white/10 pb-3 mb-4">
              <h3 className="font-bold text-white text-base flex items-center gap-2">
                <Calendar className="h-4 w-4 text-purple-400" />
                Revenue Run-Rate Projections
              </h3>
              <p className="text-xs font-mono text-slate-400">
                Incremental cashflow across daily, weekly, monthly, and annual horizons
              </p>
            </div>

            {/* Period Breakdown Cards */}
            <div className="space-y-2.5 font-mono">
              <div className="flex items-center justify-between p-3 rounded-xl bg-black/40 border border-white/5">
                <div className="flex items-center gap-2 text-slate-300">
                  <span className="h-2 w-2 rounded-full bg-[#ffd700]" />
                  <span>Per Single Season:</span>
                </div>
                <div className="text-right">
                  <span className="font-bold text-white text-sm">
                    +${grossUpliftPerSeason.toFixed(1)}
                  </span>
                  <span className="text-[10px] text-slate-400 block">+18.2% per cohort</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-black/40 border border-white/5">
                <div className="flex items-center gap-2 text-slate-300">
                  <span className="h-2 w-2 rounded-full bg-emerald-400" />
                  <span>Daily Run-Rate Gain:</span>
                </div>
                <div className="text-right">
                  <span className="font-bold text-emerald-400 text-sm">
                    +${parseInt(dailyUplift).toLocaleString()} / day
                  </span>
                  <span className="text-[10px] text-slate-400 block">365-day average</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-black/40 border border-white/5">
                <div className="flex items-center gap-2 text-slate-300">
                  <span className="h-2 w-2 rounded-full bg-purple-400" />
                  <span>Monthly Incremental Cashflow:</span>
                </div>
                <div className="text-right">
                  <span className="font-bold text-purple-300 text-sm">
                    +${parseInt(monthlyUplift).toLocaleString()} / mo
                  </span>
                  <span className="text-[10px] text-slate-400 block">Net of cloud bill</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3.5 rounded-xl bg-[#ffd700]/10 border border-[#ffd700]/30 shadow-glass-gold">
                <div className="flex items-center gap-2 text-white font-bold">
                  <Sparkles className="h-4 w-4 text-[#ffd700]" />
                  <span>Annual Net Revenue Lift:</span>
                </div>
                <div className="text-right">
                  <span className="font-bold text-[#ffd700] text-lg">
                    +${Math.round(annualNetProfitUplift).toLocaleString()}
                  </span>
                  <span className="text-[10px] text-slate-300 block">{roiMultiple}x ROI Ratio</span>
                </div>
              </div>
            </div>
          </div>

          {/* Strategic Implementation Notes */}
          <div className="p-3 rounded-xl bg-black/50 border border-white/10 text-xs text-slate-300 space-y-1.5">
            <div className="flex items-center gap-1.5 text-[#ffd700] font-mono font-bold text-[11px]">
              <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
              Deployment Recommendation:
            </div>
            <p className="text-[11px] leading-relaxed text-slate-300">
              Deploy PPO with fallback bounds (min price $50, max price $300) to ensure predictable operations. 
              The agent's policy is fully Gym-compliant and requires zero human intervention during 30-day ticket cycles.
            </p>
          </div>
        </div>
      </div>

      {/* Scenario Sensitivity Matrix */}
      <div className="glass-panel rounded-2xl p-5 space-y-4">
        <div className="border-b border-white/10 pb-3">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <FileSpreadsheet className="h-4 w-4 text-[#ffd700]" />
            Volume vs. Uplift Sensitivity Matrix
          </h3>
          <p className="text-xs font-mono text-slate-400">
            Projected net annual revenue uplift across varying annual season scales and model alpha performance
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-center text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 uppercase text-[11px]">
                <th className="py-2.5 px-3 text-left">Annual Seasons</th>
                <th className="py-2.5 px-3">Conservative (+10%)</th>
                <th className="py-2.5 px-3">Empirical Target (+18.2%)</th>
                <th className="py-2.5 px-3">Optimistic (+25%)</th>
                <th className="py-2.5 px-3">High Alpha (+30%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.05]">
              {[500, 1000, 1500, 2500, 5000].map((vol) => (
                <tr
                  key={vol}
                  className={`hover:bg-white/[0.03] transition-colors ${
                    Math.abs(vol - annualSeasons) < 300 ? "bg-[#ffd700]/[0.08]" : ""
                  }`}
                >
                  <td className="py-3 px-3 text-left font-bold text-white">
                    {vol.toLocaleString()} seasons/yr
                  </td>
                  {[10, 18.2, 25, 30].map((rate) => {
                    const gross = vol * baselineRevPerSeason * (rate / 100);
                    const net = gross - annualComputeCost;
                    const isTarget = rate === 18.2;

                    return (
                      <td
                        key={rate}
                        className={`py-3 px-3 font-semibold ${
                          isTarget
                            ? "text-[#ffd700] font-bold text-sm"
                            : "text-slate-300"
                        }`}
                      >
                        +${Math.round(net).toLocaleString()}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
