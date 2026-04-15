# Skeuomorphism

The core of skeuomorphism design lies in simulating real-world materials, lighting, and physical textures. In modern UI, it often evolves into Neumorphism or Glassmorphism, providing users with an extremely high level of visual immersion.

## Best Used For

Smart home control panel, professional audio editor, gaming interface

## Not Recommended For

News websites with a large amount of text, enterprise backend management systems (CRUD), or mobile applications that pursue ultimate simplicity and high information density.

## Key Features

Tactile, Physicality,Depth, Shadows & Highlights,Materiality, Bevel & Emboss，Analog


## Color Palette

 **Background (Chassis)**: `#e0e5ec` - Cool mid-tone industrial grey. The base "plastic" material everything is mounted to. This is Level 0.
-   **Foreground (Panel)**: `#f0f2f5` - Slightly lighter raised panel surface. Used sparingly for contrast.
-   **Muted (Recessed)**: `#d1d9e6` - Darker grey for sunken areas (input fields, screen bezels, grooves). Creates the "below surface" appearance.
-   **Text (Primary)**: `#2d3436` - Dark charcoal ink. High contrast but softer than pure black for reduced eye strain.
-   **Text Muted (Labels)**: `#4a5568` - Darker slate grey (improved from `#636e72` for WCAG AA compliance). Used for secondary text, labels, and metadata.
-   **Accent (Safety Orange)**: `#ff4757` - High-visibility "Braun Red" / "Safety Orange". Reserved exclusively for:
  - Interactive elements (primary buttons, links, toggles)
  - Status indicators (active LEDs, online badges)
  - Critical alerts or highlights
  This color should appear sparingly—it's the "emergency stop button" of the palette.
-   **Accent Foreground**: `#ffffff` - White text on accent backgrounds for maximum legibility.
-   **Border (Shadow)**: `#babecc` - The shadow color in neumorphic pairs. Represents the darker half of the lighting equation.
-   **Border Light (Highlight)**: `#ffffff` - The highlight color. The brighter half that creates dimensionality.
-   **Border Dark (Deep Shadow)**: `#a3b1c6` - Used for prominent borders and dividers where extra contrast is needed.

**Dark Accent Surfaces**: For dark technical panels (stats strip, benefits section), use:
- Background: `#2d3436` or `#2c3e50` (charcoal to slate)
- Text: `#ffffff`, `#e0e5ec`, or `#a8b2d1` (graded whites)
- Accent: Same `#ff4757` maintains brand consistency

---

### Typography

**Font Pairing**:
-   **Primary (Sans-serif)**: **Inter** (weights 400/500/600/700/800) - Humanist sans-serif with excellent legibility. Objective, neutral, and highly functional. Perfect for body text, headings, and UI labels.
-   **Technical (Monospace)**: **JetBrains Mono** or **Roboto Mono** (weights 400/500) - Engineered typeface optimized for code and data. Use exclusively for:
  - All numeric displays (stats, pricing, dates)
  - Technical labels and badges
  - Small uppercase metadata ("SYSTEM OPERATIONAL", "LOG #123")
  - Input fields (simulates terminal/data entry aesthetic)

---

## Effects & Animation

**Motion Philosophy**: Mechanical spring physics with subtle bounce—mimicking real physical switches and buttons.

**Easing Curve**:
- Primary: `cubic-bezier(0.175, 0.885, 0.32, 1.275)` - Slight overshoot/bounce
- Fast interactions: `duration-150` to `duration-200`
- Smooth transitions: `duration-300`
- Image/scale effects: `duration-500`

**Framer Motion Integration**:
- Hero section uses staggered entrance animations
- Mechanical easing constant: `[0.175, 0.885, 0.32, 1.275]`
- Variants: `slideUp` (opacity + y-translate), `stagger` (staggerChildren)

**Key Micro-interactions**:
- **Button Press**: `active:translate-y-[2px]` + shadow inversion (150ms)
- **Card Hover**: `-translate-y-1` elevation with shadow upgrade (300ms)
- **Icon Hover**: `group-hover:scale-110` + `group-hover:rotate-12` (200ms)
- **Image Hover**: Grayscale to color (500ms)
- **LED Pulse**: `animate-pulse` (Tailwind default, ~2s cycle)
- **Loading Spinner**: `animate-spin` on border technique (1s linear)

**Advanced Animations**:
- Radar sweep in benefits: `animate-spin` with `conic-gradient` and long duration (4s)
- Device screen scanlines: Static background pattern (no animation needed)
- Mobile menu: Slide down with opacity fade (200ms ease-out)

---


##  Radius & Depth

**Border Radius Scale**:
-   **sm**: `4px` - Tight mechanical edges (small buttons, badges)
-   **md**: `8px` - Standard controls (inputs, small cards)
-   **lg**: `16px` - Large panels (cards, modals)
-   **xl**: `24px` - Hero components (device bezels, major sections)
-   **2xl**: `30px+` - Oversized containers (benefit panels, final CTA)
-   **full**: `9999px` - Perfect circles (icon housings, LEDs, step indicators)

Curves are soft and organic—mimicking injection-molded plastic, not sharp machined metal.

**Neumorphic Shadow System** (The Core Visual Signature):

These dual-shadow combinations create depth through light simulation:

-   **Card (Base Lift)**: `8px 8px 16px #babecc, -8px -8px 16px #ffffff`
  - Standard elevation for panels and cards. Dark shadow bottom-right, light highlight top-left.

-   **Floating (High Elevation)**: `12px 12px 24px #babecc, -12px -12px 24px #ffffff, inset 1px 1px 0 rgba(255,255,255,0.5)`
  - Enhanced lift for interactive elements (buttons, elevated cards). Optional inner highlight rim for extra polish.

-   **Pressed (Active State)**: `inset 6px 6px 12px #babecc, inset -6px -6px 12px #ffffff`
  - Shadow direction reverses—element appears pushed INTO the surface. Critical for button interactions.

-   **Recessed (Inputs/Screens)**: `inset 4px 4px 8px #babecc, inset -4px -4px 8px #ffffff`
  - Subtle inward depth for input fields, grooves, and display panels.

-   **Sharp (Mechanical Edge)**: `4px 4px 8px rgba(0,0,0,0.15), -1px -1px 1px rgba(255,255,255,0.8)`
  - Harder-edged shadow for specific components (metal tags, borders).

-   **Glow (LED/Status Indicator)**: `0 0 10px 2px rgba(255, 71, 87, 0.6)`
  - Colored bloom for active LEDs, focus states, and alerts. Can adjust color to green (`rgba(34,197,94,1)`) for "online" states.

**Layered Shadows**: On hover, add additional shadows or increase spread to simulate elevation change. Example:
```css
transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
hover:shadow-[var(--shadow-floating)]
```
---

## Accessibility Anti-Patterns (What to Avoid)

**Contrast Ratio**: Ensure text-to-background contrast meets WCAG 2.1 AA standards (especially for light grey text).
**Touch Targets**: Minimum 44x44pt for all interactive elements to ensure ease of use.
**Dynamic Type**: Support font scaling without breaking the "breathable" layout.

---

##  Anti-Patterns (What to Avoid)
**Over-cluttering**: Too many 3D elements create visual noise and fatigue.
**Inconsistent Light Source**: Ensure all shadows follow a single, global light direction (usually top-left).
**Flat Icons on 3D Buttons**: Avoid mixing flat 2D icons with hyper-realistic containers.