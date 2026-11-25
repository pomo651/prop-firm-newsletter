"use client";

import { useEffect, useRef } from "react";

// Animated "many sources -> few picks" picture. Each thin line is a source; lines
// gather into bundles (one story told by many sources), a gate lets only a few
// bundles through, and those merge into the newsletter at the right edge.
// Static lines are drawn once to an offscreen canvas; only the moving dashes
// redraw each frame. `pulse` bumps when a new pick arrives, sending a bright
// dash down a passing bundle.

const BUNDLES = 9;
const PASSING = new Set([1, 4, 7]);
const GATE = 0.62; // gate x as a fraction of width
const END = 0.86; // where passing bundles meet

type Line = { y0: number; bundle: number; phase: number; amp: number; pass: boolean };
type Dash = { line: number; t: number; speed: number; bright: boolean };

function rand(seed: number) {
  // small deterministic PRNG so the picture is stable between renders
  return () => {
    seed = (seed * 16807) % 2147483647;
    return (seed - 1) / 2147483646;
  };
}

const ease = (t: number) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));

export function FlowField({ sources, pulse }: { sources: number; pulse: number }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const dashes = useRef<Dash[]>([]);
  const lastPulse = useRef(pulse);

  useEffect(() => {
    if (pulse === lastPulse.current) return;
    lastPulse.current = pulse;
    dashes.current.push({ line: -1, t: 0, speed: 0.0045, bright: true });
  }, [pulse]);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const r = rand(7);
    const count = Math.max(60, Math.min(sources * 2, 140));
    // bundle by vertical rank (with a little shuffle) so lines gather without a tangle
    const starts = Array.from({ length: count }, () => r()).sort((a, b) => a - b);
    const lines: Line[] = starts.map((y0, i) => {
      const bundle = Math.min(BUNDLES - 1, Math.max(0, Math.floor((i / count) * BUNDLES + (r() - 0.5) * 1.2)));
      return { y0: 0.03 + y0 * 0.94, bundle, phase: r() * Math.PI * 2, amp: 0.006 + r() * 0.02, pass: PASSING.has(bundle) };
    });
    const passIdx = lines.map((l, i) => (l.pass ? i : -1)).filter((i) => i >= 0);

    let W = 0, H = 0, dpr = 1, raf = 0;
    const off = document.createElement("canvas");

    const bundleY = (b: number) => 0.1 + (b / (BUNDLES - 1)) * 0.8;
    // y (0..1) of line l at x (0..1)
    const yAt = (l: Line, x: number) => {
      const wave = Math.sin(x * 9 + l.phase) * l.amp * (1 - ease((x - 0.2) / 0.4));
      const gather = ease((x - 0.18) / 0.38);
      let y = l.y0 + (bundleY(l.bundle) - l.y0) * gather + wave;
      if (l.pass) y += (0.5 - bundleY(l.bundle)) * ease((x - GATE) / (END - GATE));
      return y;
    };
    const maxX = (l: Line) => (l.pass ? 0.93 : GATE + 0.06);

    function drawStatic() {
      const g = off.getContext("2d")!;
      off.width = W * dpr;
      off.height = H * dpr;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.clearRect(0, 0, W, H);
      for (const l of lines) {
        const steps = 120;
        // grey part up to the gate
        g.beginPath();
        for (let s = 0; s <= steps; s++) {
          const x = (s / steps) * Math.min(maxX(l), GATE);
          const px = x * W, py = yAt(l, x) * H;
          if (s) g.lineTo(px, py); else g.moveTo(px, py);
        }
        g.strokeStyle = "rgba(60,70,75,0.13)";
        g.lineWidth = 0.7;
        g.stroke();
        if (!l.pass) {
          // stopped lines fade out just past the gate
          const grad = g.createLinearGradient(GATE * W, 0, maxX(l) * W, 0);
          grad.addColorStop(0, "rgba(60,70,75,0.13)");
          grad.addColorStop(1, "rgba(60,70,75,0)");
          g.beginPath();
          for (let s = 0; s <= 20; s++) {
            const x = GATE + (s / 20) * (maxX(l) - GATE);
            const px = x * W, py = yAt(l, x) * H;
            if (s) g.lineTo(px, py); else g.moveTo(px, py);
          }
          g.strokeStyle = grad;
          g.stroke();
        } else {
          g.beginPath();
          for (let s = 0; s <= 60; s++) {
            const x = GATE + (s / 60) * (maxX(l) - GATE);
            const px = x * W, py = yAt(l, x) * H;
            if (s) g.lineTo(px, py); else g.moveTo(px, py);
          }
          g.strokeStyle = "rgba(23,112,95,0.32)";
          g.lineWidth = 0.9;
          g.stroke();
        }
      }
      // gate ticks
      g.strokeStyle = "rgba(60,70,75,0.25)";
      g.lineWidth = 1;
      g.beginPath();
      g.moveTo(GATE * W, 0.03 * H);
      g.lineTo(GATE * W, 0.97 * H);
      g.stroke();
      // newsletter card
      const cx = 0.93 * W, cy = 0.5 * H;
      g.fillStyle = "#fff";
      g.strokeStyle = "#17705f";
      g.lineWidth = 1.5;
      g.beginPath();
      g.roundRect(cx - 4, cy - 26, 40, 52, 5);
      g.fill();
      g.stroke();
      g.fillStyle = "#17705f";
      g.fillRect(cx + 4, cy - 17, 18, 3);
      g.fillStyle = "rgba(23,112,95,0.35)";
      for (let k = 0; k < 4; k++) g.fillRect(cx + 4, cy - 8 + k * 7, 24, 2);
    }

    function resize() {
      const rect = canvas!.getBoundingClientRect();
      W = rect.width;
      H = rect.height;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas!.width = W * dpr;
      canvas!.height = H * dpr;
      drawStatic();
    }

    function spawn() {
      const line = Math.floor(Math.random() * lines.length);
      dashes.current.push({ line, t: 0, speed: 0.0025 + Math.random() * 0.003, bright: false });
    }

    function frame() {
      ctx!.setTransform(1, 0, 0, 1, 0, 0);
      ctx!.clearRect(0, 0, canvas!.width, canvas!.height);
      ctx!.drawImage(off, 0, 0);
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (dashes.current.length < 26 && Math.random() < 0.25) spawn();
      dashes.current = dashes.current.filter((d) => {
        if (d.line < 0) d.line = passIdx[Math.floor(Math.random() * passIdx.length)];
        const l = lines[d.line];
        d.t += d.speed;
        const x1 = d.t, x0 = Math.max(0, d.t - (d.bright ? 0.08 : 0.035));
        if (x0 > maxX(l)) return false;
        const pastGate = x1 > GATE;
        ctx!.beginPath();
        for (let s = 0; s <= 8; s++) {
          const x = Math.min(x0 + ((x1 - x0) * s) / 8, maxX(l));
          const px = x * W, py = yAt(l, x) * H;
          if (s) ctx!.lineTo(px, py); else ctx!.moveTo(px, py);
        }
        const fade = l.pass ? 1 : 1 - ease((x1 - GATE) / 0.06);
        ctx!.strokeStyle = d.bright
          ? "rgba(23,112,95,1)"
          : pastGate && l.pass
            ? `rgba(23,112,95,${0.8 * fade})`
            : `rgba(40,48,52,${0.55 * fade})`;
        ctx!.lineWidth = d.bright ? 2.4 : 1.3;
        ctx!.stroke();
        return true;
      });
      raf = requestAnimationFrame(frame);
    }

    resize();
    if (reduce) {
      ctx.drawImage(off, 0, 0);
    } else {
      raf = requestAnimationFrame(frame);
    }
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);
    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
    };
  }, [sources]);

  return <canvas ref={ref} aria-hidden />;
}
