import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/**
 * Simple replacement for @gsap/react's useGSAP.
 * Runs a GSAP setup function inside useEffect with proper cleanup.
 */
export function useGsapScroll(
  setup: (ctx: { scope: HTMLElement | null }) => void,
  deps: unknown[] = []
) {
  const scopeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!scopeRef.current) return;

    const ctx = gsap.context(() => {
      setup({ scope: scopeRef.current });
    }, scopeRef.current);

    return () => ctx.revert();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return scopeRef;
}

export { gsap, ScrollTrigger };
