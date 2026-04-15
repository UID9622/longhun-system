# Apple Minimalist

A design language centered around clarity, generous whitespace, and high-quality typography. It mimics the "Apple aesthetic" by prioritizing content over decorative elements, using subtle depth, and ensuring a premium, breathable user experience.

## Best Used For

High-end consumer goods websites, efficiency tools (note-taking, task management) that require high concentration

## Not Recommended For

Gaming communities, e-commerce platforms that need cost-effective promotional campaigns, high-density data analysis backends, and traditional enterprise applications

## Key Features

Breathing room、Squircle corners、Continuous curvature、Layered shadows、Airy、Precise、Subtle、Content-First、 Sophisticated

## Color Palette

**Primary (Background):** #FFFFFF-The absolute white base creates "Negative Space".
**Secondary (Surface):** #F5F5F7-Light grey for subtle separation/grouping.
**Accent (Action)：** #0071E3 / #000000-Classic Apple Blue for CTAs.
**Text (Primary)：** #1D1D1F-Off-black for better reading comfort than pure black.
**Text (Secondary)：** #86868B-Medium grey for captions and hints.

---

### Typography

- **Primary Font:** San Francisco (SF Pro), Inter, or Helvetica Now
- **Hierarchy:** Large, bold headings contrast with significantly smaller, lighter body text.headings.
- **Line Height:**  Generous (1.5x - 1.6x for body) to enhance readability.

---

## Effects & Animation

**Soft Shadows:** Use very large blur radii with low opacity (e.g., rgba(0,0,0,0.05)).
**Glassmorphism (Background Blur):** Use backdrop-filter: blur() for navigation bars and overlays to maintain context.
**Spring Physics:** Animations should feel organic and fluid, not linear.

---

## Anti-Patterns (What to Avoid)

**Heavy Borders:** Avoid hard, high-contrast borders; use shadows or background color shifts instead.
**Clutter:** Do not fill every empty pixel. If it's not functional, remove it.
**Loud Gradients:** Avoid multi-color, aggressive gradients. Use subtle, near-solid transitions.

---

## Accessibility Considerations

**Contrast Ratio:**  Ensure text-to-background contrast meets WCAG 2.1 AA standards (especially for light grey text).
**Touch Targets:**  Minimum 44x44pt for all interactive elements to ensure ease of use.
**Dynamic Type:** Support font scaling without breaking the "breathable" layout.