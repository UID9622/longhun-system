/**
 * Injects CSS keyframe animations for the marquee system.
 * Pure CSS animations — no JS-driven animation loops.
 */
export default function MarqueeKeyframes() {
  return (
    <style>{`
      /* === Marquee Flow Animation === */
      @keyframes marquee-flow-left {
        0% { transform: translateX(0); }
        100% { transform: translateX(-33.333%); }
      }

      @keyframes marquee-flow-right {
        0% { transform: translateX(-33.333%); }
        100% { transform: translateX(0); }
      }

      /* === Color Pulse per segment === */
      @keyframes color-pulse-0 {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 200, 83, 0.3), inset 0 0 40px rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 40px rgba(0, 200, 83, 0.6), inset 0 0 40px rgba(255,255,255,0.15); }
      }
      @keyframes color-pulse-1 {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 61, 0, 0.3), inset 0 0 40px rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 40px rgba(255, 61, 0, 0.6), inset 0 0 40px rgba(255,255,255,0.15); }
      }
      @keyframes color-pulse-2 {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 214, 0, 0.3), inset 0 0 40px rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 40px rgba(255, 214, 0, 0.6), inset 0 0 40px rgba(255,255,255,0.15); }
      }
      @keyframes color-pulse-3 {
        0%, 100% { box-shadow: 0 0 20px rgba(26, 26, 46, 0.5), inset 0 0 40px rgba(255,255,255,0.05); }
        50% { box-shadow: 0 0 40px rgba(138, 138, 181, 0.4), inset 0 0 40px rgba(255,255,255,0.1); }
      }
      @keyframes color-pulse-4 {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.3), inset 0 0 40px rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 40px rgba(255, 215, 0, 0.6), inset 0 0 40px rgba(255,255,255,0.15); }
      }
      @keyframes color-pulse-5 {
        0%, 100% { box-shadow: 0 0 20px rgba(41, 98, 255, 0.3), inset 0 0 40px rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 40px rgba(41, 98, 255, 0.6), inset 0 0 40px rgba(255,255,255,0.15); }
      }
      @keyframes color-pulse-6 {
        0%, 100% { box-shadow: 0 0 20px rgba(170, 0, 255, 0.3), inset 0 0 40px rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 40px rgba(170, 0, 255, 0.6), inset 0 0 40px rgba(255,255,255,0.15); }
      }

      /* === Segment Flash Animation === */
      @keyframes segment-flash {
        0%, 100% { opacity: 1; filter: brightness(1); }
        50% { opacity: 0.6; filter: brightness(1.3); }
      }

      /* === Machine Scan Line === */
      @keyframes machine-scan {
        0% { top: 0; opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { top: 100%; opacity: 0; }
      }

      /* === Blinking Cursor === */
      @keyframes blink-cursor {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0; }
      }

      /* === Log Entry Fade === */
      @keyframes log-entry-in {
        0% { opacity: 0; transform: translateY(8px); }
        100% { opacity: 1; transform: translateY(0); }
      }

      /* === Smooth animation-duration transition === */
      .marquee-track {
        transition: animation-duration 0.3s ease;
        will-change: transform;
      }

      .marquee-track.paused {
        animation-play-state: paused !important;
      }

      /* === Custom scrollbar for color list === */
      .color-list-scroll::-webkit-scrollbar {
        width: 4px;
      }
      .color-list-scroll::-webkit-scrollbar-track {
        background: var(--spectrum-border);
        border-radius: 2px;
      }
      .color-list-scroll::-webkit-scrollbar-thumb {
        background: var(--dragon-gold);
        border-radius: 2px;
      }

      /* === Custom range slider === */
      .marquee-slider {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        height: 6px;
        border-radius: 3px;
        background: linear-gradient(to right, var(--dragon-gold) 0%, var(--dragon-gold) var(--slider-percent, 50%), var(--spectrum-border) var(--slider-percent, 50%), var(--spectrum-border) 100%);
        outline: none;
        cursor: pointer;
      }
      .marquee-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: var(--dragon-gold);
        cursor: pointer;
        box-shadow: 0 0 12px rgba(255, 215, 0, 0.5);
        border: 2px solid var(--spectrum-peak);
      }
      .marquee-slider::-moz-range-thumb {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: var(--dragon-gold);
        cursor: pointer;
        box-shadow: 0 0 12px rgba(255, 215, 0, 0.5);
        border: 2px solid var(--spectrum-peak);
      }
    `}</style>
  );
}
