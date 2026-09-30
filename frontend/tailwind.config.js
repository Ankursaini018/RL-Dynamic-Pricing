/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#0d0d1a',
        'surface-card': 'rgba(20, 20, 38, 0.72)',
        'surface-card-hover': 'rgba(28, 28, 52, 0.85)',
        'surface-dark': '#090912',
        accent: {
          gold: '#ffd700',
          'gold-light': '#ffe55c',
          'gold-dim': 'rgba(255, 215, 0, 0.15)',
          purple: '#9c27b0',
          'purple-light': '#ba68c8',
          'purple-dim': 'rgba(156, 39, 176, 0.15)',
        },
        agent: {
          rl: '#ffd700',      // Gold
          dqn: '#ff6b6b',     // Coral
          qlearn: '#00e676',  // Emerald
          baseline: '#64b5f6',// Steel Blue
          timed: '#64b5f6',
          fixed: '#94a3b8',
          decay: '#fb923c',
          demand: '#c084fc',
        },
      },
      fontFamily: {
        sans: ['"Space Grotesk"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.45)',
        'glass-gold': '0 8px 32px 0 rgba(255, 215, 0, 0.12), inset 0 0 0 1px rgba(255, 215, 0, 0.2)',
        'glass-purple': '0 8px 32px 0 rgba(156, 39, 176, 0.15), inset 0 0 0 1px rgba(156, 39, 176, 0.25)',
        'glow-gold': '0 0 25px -4px rgba(255, 215, 0, 0.35)',
        'glow-purple': '0 0 25px -4px rgba(156, 39, 176, 0.35)',
      },
      backdropBlur: {
        xs: '2px',
        md: '12px',
        lg: '16px',
        xl: '24px',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'ticker': 'ticker 30s linear infinite',
      },
      keyframes: {
        ticker: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        }
      }
    },
  },
  plugins: [],
}
