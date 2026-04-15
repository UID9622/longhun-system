# Linear Aesthetic

A modern SaaS dark precision aesthetic with ultra-fine strokes, depth, shimmer, and glassmorphism effects.

## Color Palette

- **Background (Canvas)**: `#080808` or `#030303` (Ultra Dark)
- **Card Surface**: `#080808` or `#0A0A0A` (with subtle transparency)
- **Primary Text**: `#FFFFFF` (85%-90% Opacity)
- **Secondary Text**: `#A1A1AA` (Zinc-400)
- **Accent Glow (Indigo)**: `#6366F1` - Used for subtle light effects
- **Accent Glow (Purple)**: `#A855F7` - Used for subtle light effects
- **Border Highlighting**: `rgba(255, 255, 255, 0.1)` (The "Micro-border")

## Typography

- **Primary Font**: Geist, Inter, SF Pro (sans-serif, geometric)
- **Font Weight**: Semi-bold for titles, regular for body text
- **Letter Spacing**: -0.02em for tighter spacing
- **Type Scale**: Clear hierarchical structure

## Best Used For

Developer tools, AI platforms, project management, high-tech SaaS platforms, fintech dashboards, cryptocurrency/Web3 trading interfaces.

## Not Recommended For

Children's education products, traditional government systems, mass retail e-commerce, brands that need to show warmth/affinity.

## Key Features

- **Precision**: Meticulous attention to detail and clean lines
- **Ultra-fine Strokes**: 1px or 0.5px solid borders, often using linear gradients to simulate light hitting edges
- **Depth & Space**: Create visual hierarchy through layering and z-index
- **Shimmer Animation**: 45-degree light ray sweeping across cards on hover or loop
- **Breathing Effect**: Subtle, rhythmic animations that mimic breathing
- **Dark Mode**: Optimized for low-light environments with high contrast
- **Glassmorphism**: Translucent elements with backdrop blur effects

## Design Elements

- **Micro-border**: Ultra-thin 1px or 0.5px borders using `rgba(255, 255, 255, 0.1)`
- **Backdrop Blur**: `backdrop-blur-xl` (16px - 24px) for overlays and navigation bars
- **Bloom/Glow**: Subtle radial gradients behind components to create a "soft glow"
- **Spring Motion**: Precise, snappy transitions using Framer Motion: `stiffness: 150, damping: 20`

## Animation Guidelines

- **Shimmer Effect**: Use CSS linear gradients with transform animations for light sweeps
- **Hover States**: Subtle glow intensification and micro-translations
- **Transitions**: Implement spring physics for natural-feeling animations
- **Loading States**: Animated skeletons with subtle shimmer effects

## Anti-Patterns (What to Avoid)

- **Flat backgrounds**: Never use a single solid color. Always layer gradients, noise, and ambient light
- **Pure black (#000000)**: Use near-blacks like `#050506` or `#020203` for softer appearance
- **Pure white text**: `#EDEDEF` or similar off-white to reduce harshness
- **Large hover movements**: Keep transforms under 8px. This isn't playful—it's precise
- **Uniform grids**: Bento layouts should have variety in card sizes. Avoid same-size-everything
- **Harsh borders**: Borders should be nearly invisible (`6-10%` white opacity), not prominent
- **Colorful accent overuse**:  The accent color is for highlights and interaction, not decoration. Most of the UI is monochromatic
- **Bouncy animations**: Use expo-out easing, not spring physics. Movements should be swift and decisive
- **Missing glow effects**: Accent buttons without glow look incomplete. The soft light emission is part of the language

## Accessibility Considerations

**Contrast:**
- Primary text (`#EDEDEF` on `#050506`): ~15:1 ratio ✓
- Muted text (`#8A8F98` on `#050506`): ~6:1 ratio ✓
- Accent on dark: Ensure 4.5:1 minimum for interactive elements

**Focus States:**
- Always visible focus rings using accent color
- `ring-offset` matches background color

**Motion:**
- Respect `prefers-reduced-motion`
- Provide fallbacks for parallax and floating animations
- Essential interactions should work without animation

**Color Independence:**
- Don't rely solely on accent color for meaning
- Use icons, labels, and position to reinforce state
</design-system>