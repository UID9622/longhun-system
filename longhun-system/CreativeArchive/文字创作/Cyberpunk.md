# Cyberpunk

High contrast neon on black, glitch animations, terminal/monospace fonts, tech-oriented decorations. A dystopian digital aesthetic inspired by 80s sci-fi and hacker culture.

## Best Used For

High-impact marketing sites, gaming communities, crypto/web3 marketing sites, music streaming apps, and immersive storytelling experiences.

## Not Recommended For

Government or legal services, healthcare portals, minimalist productivity tools, or apps requiring long-form reading (high eye strain).

## Key Features

Neon，Fluorescent，High Contrast，Glitch Art，Grid Systems，Retro-futurism，Distopia

## Color Palette

background:          #0a0a0f      // Deep void black with slight blue undertone
foreground:          #e0e0e0      // Primary text, not pure white (less harsh)
card:                #12121a      // Card background, deep purple-black
muted:               #1c1c2e      // UI chrome/elevated backgrounds
mutedForeground:     #6b7280      // Secondary text, reduced contrast
accent:              #00ff88      // PRIMARY NEON - Electric green (Matrix-inspired)
accentSecondary:     #ff00ff      // SECONDARY NEON - Hot magenta/pink
accentTertiary:      #00d4ff      // TERTIARY NEON - Cyan/electric blue
border:              #2a2a3a      // Subtle borders
input:               #12121a      // Deep input background
ring:                #00ff88      // Focus ring matches accent
destructive:         #ff3366      // Error/danger red-pink

---

## Typography

**Font Stack**:
- **Headings**: `"Orbitron", "Share Tech Mono", monospace` — Geometric, futuristic, robotic
- **Body**: `"JetBrains Mono", "Fira Code", "Consolas", monospace` — Clean monospace for that terminal feel
- **Accent/Labels**: `"Share Tech Mono", monospace` — For UI labels, timestamps, badges

---

## Effects & Animation

**Motion Feel**: Sharp, digital, slightly mechanical. Quick snaps rather than smooth eases.

**Transitions**:
```css
transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
/* Or for more digital feel: */
transition: all 100ms steps(4);
```

**Keyframe Animations**:

```css
/* Blink cursor */
@keyframes blink {
  50% { opacity: 0; }
}

/* Glitch effect */
@keyframes glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(2px, -2px); }

---

## Accessibility

**Contrast**: All text meets WCAG AA (accent green on dark bg = 7.5:1 ratio - excellent)

**Focus States**:
```css
focus-visible:outline-none
focus-visible:ring-2
focus-visible:ring-accent
focus-visible:ring-offset-2
focus-visible:ring-offset-background
```
Plus add glow effect matching the neon aesthetic.

**Reduced Motion**: Respect `prefers-reduced-motion` - disable glitch animations, keep static chromatic aberration

---

## Anti-Patterns (What to Avoid)

**Low Contrast Text：** Placing thin, neon text on a busy background makes it unreadable.
**LOver-Glitching：** Too much movement distracts from the core UI tasks.
**Muddy Gradients：**: Using generic linear gradients that don't mimic light emission.
