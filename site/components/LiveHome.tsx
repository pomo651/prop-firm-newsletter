"use client";

import { useEffect, useRef, useState } from "react";
import type { Stats } from "@/lib/db";
import { FlowField } from "./FlowField";

const POLL_MS = 30_000;
const ROTATE_MS = 5_000;
const KIND_LABEL: Record<string, string> = {
  official: "Official", x: "X", press: "Press", community: "Community",
  youtube: "YouTube", review: "Review", other: "Other",
};

const n = (v: number) => v.toLocaleString("en-US");
const ago = (iso: string) => {
  const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000);
  if (m < 60) return `${Math.max(m, 1)}m ago`;
  if (m < 60 * 24) return `${Math.round(m / 60)}h ago`;
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

export function LiveHome({ initial }: { initial: Stats }) {
  const [stats, setStats] = useState(initial);
  const [pulse, setPulse] = useState(0);
  const [fresh, setFresh] = useState<Set<number>>(new Set());
  const [slot, setSlot] = useState(0);
  const seen = useRef(new Set(initial.latest.map((p) => p.id)));

  // poll for new counts and picks
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const res = await fetch("/api/stats", { cache: "no-store" });
        if (!res.ok) return;
        const next: Stats = await res.json();
        const added = next.latest.filter((p) => !seen.current.has(p.id)).map((p) => p.id);
        added.forEach((i) => seen.current.add(i));
        if (added.length) {
          setFresh(new Set(added));
          setPulse((v) => v + 1);
          setSlot(0);
        }
        setStats(next);
      } catch {
        /* offline: keep last numbers */
      }
    }, POLL_MS);
    return () => clearInterval(id);
  }, []);

  // rotate the caption through the latest picks
  useEffect(() => {
    if (stats.latest.length < 2) return;
    const id = setInterval(() => setSlot((s) => (s + 1) % stats.latest.length), ROTATE_MS);
    return () => clearInterval(id);
  }, [stats.latest.length]);

  const current = stats.latest[slot % Math.max(stats.latest.length, 1)];
  const kinds = Object.entries(stats.sourceKinds).sort((a, b) => b[1] - a[1]);

  return (
    <>
      <div className="flow">
        <FlowField sources={stats.sources} pulse={pulse} />
        <div className="flow-caption" style={{ top: "calc(50% + 52px)" }}>
          <div className="k">Latest pick</div>
          {current ? (
            <>
              <a href={current.url} target="_blank" rel="noreferrer">{current.title}</a>
              <div className="src">{current.source}</div>
            </>
          ) : (
            <div className="src">No picks yet. They appear here the moment a bot picks one.</div>
          )}
        </div>
      </div>
      <p className="flow-note">
        Each line is a source. Lines that tell the same story gather into a bundle; the gate lets only a few
        bundles through, and those become the newsletter.
      </p>

      <div className="steps">
        <div className="step">
          <h3><small>01</small>Watch</h3>
          <div className="big">{n(stats.sources)}<small>sources</small></div>
          <p>Firm help centers and rule pages, official X accounts, trade press, Reddit, YouTube and review sites.</p>
          <div className="meta">{kinds.map(([k, v]) => `${KIND_LABEL[k] ?? k} ${v}`).join(" · ") || "—"}</div>
        </div>
        <div className="step">
          <h3><small>02</small>Collect</h3>
          <div className="big">{n(stats.items)}<small>items</small></div>
          <p>Every rule change, launch, payout story and firm reply the watchers see is kept and grouped by story.</p>
          <div className="meta">Last 24 hours: {n(stats.items24h)}</div>
        </div>
        <div className="step">
          <h3><small>03</small>Pick</h3>
          <div className="big">{n(stats.picks)}<small>picks</small></div>
          <p>Marketing posts, rumours and repeats are dropped. What&apos;s left is checked against the firm&apos;s own page.</p>
          <div className="meta">Last 24 hours: {n(stats.picks24h)}</div>
        </div>
        <div className="step">
          <h3><small>04</small>Publish</h3>
          <div className="big">{n(stats.editions)}<small>editions</small></div>
          <p>The few that matter become the daily newsletter: what changed, why it matters, and the source.</p>
          <div className="meta">{stats.latestEdition ? `Latest: ${stats.latestEdition}` : "First edition coming soon"}</div>
        </div>
      </div>

      <div className="picks">
        <div className="section-head">
          <h2>Latest picks</h2>
          <span className="live">Live · updates every 30s</span>
        </div>
        {stats.latest.length === 0 && <div className="empty">Nothing picked yet.</div>}
        {stats.latest.map((p) => (
          <div key={p.id} className={`pick${fresh.has(p.id) ? " fresh" : ""}`}>
            <time dateTime={p.picked_at}>{ago(p.picked_at)}</time>
            <div>
              <a href={p.url} target="_blank" rel="noreferrer">{p.title}</a>
              <div className="src">{p.source}{p.firm ? ` · ${p.firm}` : ""}</div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
