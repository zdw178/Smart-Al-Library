/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#0f0f12",
        "primary-soft": "#18181b",
        accent: "#8B5CF6",
        "accent-teal": "#0D9488",
        surface: "#FAFAFA",
        "surface-card": "#ffffff",
        "surface-low": "#f3f3f3",
        "surface-high": "#e8e8e8",
        "on-surface": "#18181B",
        "on-surface-muted": "#71717A",
        "outline-subtle": "#e4e4e7",
        brand: {
          night: "#18181B",
          pearl: "#FAFAFA",
          aurora_start: "#8B5CF6",
          aurora_end: "#0D9488"
        }
      },
      fontFamily: {
        headline: ["Manrope", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
      borderRadius: {
        xl: "0.75rem",
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
      boxShadow: {
        card: "0 2px 12px 0 rgba(0,0,0,0.06)",
        "card-hover": "0 8px 32px 0 rgba(0,0,0,0.10)",
        aurora: "0 20px 60px rgba(139, 92, 246, 0.12)",
      },
      animation: {
        "fade-up": "fadeUp 0.5s ease-out both",
        "scale-in": "scaleIn 0.3s ease-out both",
        "pulse-dot": "pulseDot 2s ease-in-out infinite",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        pulseDot: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.3" },
        },
      },
    },
  },
  plugins: [],
}