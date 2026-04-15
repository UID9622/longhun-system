# Minimalist Modern

A bold, minimalist-modern visual system combining clean aesthetics with dynamic execution. Features signature Electric Blue gradients, sophisticated dual-font pairing (Calistoga + Inter), animated hero graphics, inverted contrast sections, and micro-interactions throughout. Professional yet design-forward—confidence without clutter.

## Best Used For

Enterprise dashboards, Knowledge bases, Collaboration tools, Payment systems, Documentation, Premium subscription SaaS

## Not Recommended For

Entertainment-only social apps, Gamified interfaces, High-impact promotional landing pages, Retro-style branding

## Key Features

Breathability, Hierarchy, Intuitive, Neutral, Airy, Functional Aesthetics

## Color Palette

**Chromatic Focus:** A warm, near-monochrome palette amplified by a dual-tone accent gradient. The accent colors are used sparingly but with maximum impact—they command attention wherever they appear.

| Token | Value | Usage & Context |
|:------|:------|:----------------|
| `background` | `#FAFAFA` | Primary canvas. Warmer off-white that reduces eye strain. |
| `foreground` | `#0F172A` (Slate-900) | Primary text. Deep slate, not pure black. Also used as inverted section backgrounds. |
| `muted` | `#F1F5F9` (Slate-100) | Secondary surfaces, card backgrounds, subtle fills. |
| `muted-foreground` | `#64748B` (Slate-500) | Secondary text, descriptions, metadata. |
| `accent` | `#0052FF` (Electric Blue) | **Primary action color.** CTAs, links, highlights, icon backgrounds. |
| `accent-secondary` | `#4D7CFF` | Gradient endpoint. Used with `accent` for gradient effects. |
| `accent-foreground` | `#FFFFFF` | Text on accent backgrounds. Always white. |
| `border` | `#E2E8F0` (Slate-200) | Subtle structural borders on cards and dividers. |
| `card` | `#FFFFFF` | Elevated surfaces. Pure white for maximum lift. |
| `ring` | `#0052FF` | Focus rings. Matches the primary accent. |


---

### Typography

**Font Pairing (Dual-Font System):**
- **Display Font:** `"Plus Jakarta Sans", Satoshi, "PingFang SC" (Semibold),"Microsoft YaHei UI", sans-serif;` — A warm, characterful serif with personality. Used exclusively for h1/h2 headlines to create memorable anchor points.
- **UI & Body Font:** `"Inter", "Geist Sans", "Noto Sans SC"` — Highly legible, clean sans-serif for all body text, UI elements, and smaller headings.
- **Monospace:** `"JetBrains Mono", monospace` — For section labels, badges, and technical callouts.

---

### Borders, Surfaces & Shadows

**Surfaces:**
- Cards use pure white (`#FFFFFF`) with `1px` border in `border` color
- Elevated cards add `shadow-lg` or `shadow-xl` for lift
- Featured elements use gradient borders (2px stroke effect via nested divs)

**Shadow System:**
| Token | Value | Usage |
|:------|:------|:------|
| `shadow-sm` | `0 1px 3px rgba(0,0,0,0.06)` | Subtle lift |
| `shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | Standard cards |
| `shadow-lg` | `0 10px 15px rgba(0,0,0,0.08)` | Elevated cards |
| `shadow-xl` | `0 20px 25px rgba(0,0,0,0.1)` | Hero elements |
| `shadow-accent` | `0 4px 14px rgba(0,82,255,0.25)` | Accent-tinted lift |
| `shadow-accent-lg` | `0 8px 24px rgba(0,82,255,0.35)` | Featured elements |

**Textures (Critical for Avoiding Flatness):**
- **Dot Pattern:** `radial-gradient(circle, white 1px, transparent 1px)` at `32px` intervals, `opacity: 0.03` — Used on dark inverted sections
- **Radial Glows:** Large blurred circles (`blur-[150px]`) of accent color at `3-6%` opacity — Positioned at section corners
- **Gradient Overlays:** Subtle `radial-gradient` from accent color, `8%` opacity — Used in hero graphic backgrounds

---

## Effects & Animation

**Motion Philosophy:** Smooth, confident, and purposeful. Animations enhance understanding and add delight without being distracting. All motion follows natural easing curves.

**Transition Defaults:**
- Standard: `transition-all duration-200 ease-out`
- Entrance: `duration-700` with stagger (`0.1s` delay between children)
- Hover lifts: `duration-300`
- Button active: `duration-200` with scale down

**Entrance Animations (Framer Motion):**
```js
const easeOut = [0.16, 1, 0.3, 1] as const;

const fadeInUp = {
  hidden: { opacity: 0, y: 28 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.7, ease: easeOut } }
};

const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.7, ease: easeOut } }
};

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1, delayChildren: 0.1 } }
};
```

**Continuous Animations:**
- Rotating ring: `60s` linear infinite rotation (hero graphic)
- Floating cards: `4-5s` ease-in-out infinite y-axis bobbing (±10px amplitude)
- Pulsing dot: `2s` infinite scale/opacity pulse (scale: [1, 1.3, 1], opacity: [1, 0.7, 1])
- Activity indicators: `3s` infinite scale/opacity pulse (subtle)
