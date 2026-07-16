/*
  龍魂系统 · Tailwind 配置
  文件名：tailwind.config.js
  来源：tailwind.config.js
  根文件：~/.龍魂/LONGHUN_ETERNAL_ANCHOR.md
  创作者：UJID9622 · 龍芯北辰
  用途：定义龍魂不动点五色、衍生光谱、字体族与多维动画
  注意：本标头为来源链的一部分，删除或剥离将破坏来源完整性

  DNA: #龍芯⚡️20260626140000000-LONGHUN-TAILWIND-CONFIG-v1.0
*/

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // 不动点五主色
        'dragon-green': '#00C853',
        'dragon-red': '#FF3D00',
        'dragon-yellow': '#FFD600',
        'dragon-black': '#1A1A2E',
        'dragon-gold': '#FFD700',
        // 七彩跑马灯色
        'mq-green': '#00C853',
        'mq-red': '#FF3D00',
        'mq-yellow': '#FFD600',
        'mq-black': '#1A1A2E',
        'mq-gold': '#FFD700',
        'mq-blue': '#2962FF',
        'mq-purple': '#AA00FF',
        // 衍生光谱
        'spectrum-void': '#0A0A0F',
        'spectrum-shadow': '#12121A',
        'spectrum-surface': '#1A1A2E',
        'spectrum-raise': '#232338',
        'spectrum-border': '#2A2A45',
        'spectrum-dim': '#555580',
        'spectrum-medium': '#8A8AB5',
        'spectrum-bright': '#E0E0F0',
        'spectrum-peak': '#FFFFFF',
        // shadcn
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive) / <alpha-value>)",
          foreground: "hsl(var(--destructive-foreground) / <alpha-value>)",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      fontFamily: {
        'noto-serif': ['"Noto Serif SC"', 'serif'],
        'noto-sans': ['"Noto Sans SC"', 'sans-serif'],
        'jetbrain': ['"JetBrains Mono"', 'monospace'],
        'space-grotesk': ['"Space Grotesk"', 'sans-serif'],
      },
      borderRadius: {
        xl: "calc(var(--radius) + 4px)",
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xs: "calc(var(--radius) - 6px)",
      },
      boxShadow: {
        xs: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        'glow-green': '0 0 20px rgba(0, 200, 83, 0.35)',
        'glow-red': '0 0 20px rgba(255, 61, 0, 0.35)',
        'glow-gold': '0 0 20px rgba(255, 215, 0, 0.3)',
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "caret-blink": {
          "0%,70%,100%": { opacity: "1" },
          "20%,50%": { opacity: "0" },
        },
        "color-pulse-green": {
          "0%, 100%": { boxShadow: "0 0 0px rgba(0, 200, 83, 0)" },
          "50%": { boxShadow: "0 0 20px rgba(0, 200, 83, 0.5)" },
        },
        "color-pulse-red": {
          "0%, 100%": { boxShadow: "0 0 0px rgba(255, 61, 0, 0)" },
          "50%": { boxShadow: "0 0 20px rgba(255, 61, 0, 0.5)" },
        },
        "color-pulse-yellow": {
          "0%, 100%": { boxShadow: "0 0 0px rgba(255, 214, 0, 0)" },
          "50%": { boxShadow: "0 0 20px rgba(255, 214, 0, 0.5)" },
        },
        "color-pulse-gold": {
          "0%, 100%": { boxShadow: "0 0 0px rgba(255, 215, 0, 0)" },
          "50%": { boxShadow: "0 0 20px rgba(255, 215, 0, 0.5)" },
        },
        "marquee-flow": {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% center" },
          "100%": { backgroundPosition: "200% center" },
        },
        "scroll-dot": {
          "0%": { transform: "translateY(0)", opacity: "1" },
          "100%": { transform: "translateY(24px)", opacity: "0" },
        },
        "dragon-breathe": {
          "0%, 100%": { fontWeight: "400", opacity: "0.9" },
          "50%": { fontWeight: "600", opacity: "1" },
        },
        "dragon-pulse-green": {
          "0%, 100%": { textShadow: "0 0 0 rgba(0, 200, 83, 0)" },
          "50%": { textShadow: "0 0 20px rgba(0, 200, 83, 0.6)" },
        },
        "dragon-pulse-red": {
          "0%, 100%": { textShadow: "0 0 0 rgba(255, 61, 0, 0)" },
          "50%": { textShadow: "0 0 20px rgba(255, 61, 0, 0.6)" },
        },
        "dragon-pulse-yellow": {
          "0%, 100%": { textShadow: "0 0 0 rgba(255, 214, 0, 0)" },
          "50%": { textShadow: "0 0 20px rgba(255, 214, 0, 0.6)" },
        },
        "dragon-pulse-gold": {
          "0%, 100%": { textShadow: "0 0 0 rgba(255, 215, 0, 0)" },
          "50%": { textShadow: "0 0 20px rgba(255, 215, 0, 0.6)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "caret-blink": "caret-blink 1.25s ease-out infinite",
        "color-pulse-green": "color-pulse-green 2s ease-in-out infinite",
        "color-pulse-red": "color-pulse-red 2s ease-in-out infinite",
        "color-pulse-yellow": "color-pulse-yellow 2s ease-in-out infinite",
        "color-pulse-gold": "color-pulse-gold 2s ease-in-out infinite",
        "marquee-flow": "marquee-flow 20s linear infinite",
        "shimmer": "shimmer 3s linear infinite",
        "scroll-dot": "scroll-dot 2s ease-in-out infinite",
        "dragon-breathe": "dragon-breathe 4s ease-in-out infinite",
        "dragon-pulse-green": "dragon-pulse-green 2s ease-in-out infinite",
        "dragon-pulse-red": "dragon-pulse-red 0.8s ease-in-out infinite",
        "dragon-pulse-yellow": "dragon-pulse-yellow 1.5s ease-in-out infinite",
        "dragon-pulse-gold": "dragon-pulse-gold 3s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
