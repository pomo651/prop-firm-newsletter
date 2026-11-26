import "server-only";
import { createHash, timingSafeEqual } from "node:crypto";
import { cookies } from "next/headers";
import { rpc } from "./db";
import type { Category, EditionSummary, Edition, Stats } from "./types";

// ---------- auth: the admin uses the same PREVIEW_KEY as draft previews ----------
// Logging in stores a hash of the key in an httpOnly cookie, never the key itself.
export const ADMIN_COOKIE = "ft_admin";

const hash = (s: string) => createHash("sha256").update(`ft-admin:${s}`).digest("hex");

export function keyMatches(given: string) {
  const key = process.env.PREVIEW_KEY;
  if (!key || !given) return false;
  const a = Buffer.from(hash(given));
  const b = Buffer.from(hash(key));
  return a.length === b.length && timingSafeEqual(a, b);
}

export const cookieValue = () => hash(process.env.PREVIEW_KEY ?? "");

export async function isAdmin() {
  if (!process.env.PREVIEW_KEY) return false;
  const c = (await cookies()).get(ADMIN_COOKIE)?.value;
  return !!c && c === cookieValue();
}

// ---------- data ----------
export type AdminItem = {
  id: number; url: string; title: string; summary: string | null;
  source_name: string; source_url: string | null; firm: string | null;
  collected_by: string | null; collected_at: string;
  status: "new" | "picked" | "rejected"; picked_at: string | null;
  category: Category | null; source_published_at: string | null;
  evidence: "official" | "firm_x_post" | "community" | null; evidence_url: string | null; notes: string | null;
};
export type AdminSource = {
  id: number; name: string; kind: string; url: string; active: boolean; created_at: string;
  items_total: number; items_recent: number; picks_total: number; last_item_at: string | null;
};
export type Review = { result: "published" | "held" | "skipped"; reasons: string[]; ran_at: string };
export type AdminEdition = {
  edition_date: string; subject: string; status: "draft" | "published";
  published_at: string | null; updated_at?: string; section_count: number;
  video: { status: "draft" | "approved" | "uploaded"; video_url: string | null; title: string | null; approved_at: string | null } | null;
  review: Review | null;
};
export type LogRow = { edition_date: string; ran_at: string; result: Review["result"]; reasons: string[] };

export type Snapshot = {
  mode: "full" | "partial"; // partial = ft_admin_snapshot not applied yet
  at: string;
  stats: Stats;
  totals: { items: number; new: number; picked: number; rejected: number } | null;
  items: AdminItem[] | null;
  sources: AdminSource[] | null;
  editions: AdminEdition[];
  log: LogRow[] | null;
};

type Full = Omit<Snapshot, "mode" | "stats">;

export async function getSnapshot(): Promise<Snapshot> {
  const stats = await rpc<Stats>("ft_stats");
  try {
    const s = await rpc<Full>("ft_admin_snapshot", { recent_days: 14 });
    return { mode: "full", stats, ...s };
  } catch (e) {
    if (!/Could not find the function|schema cache|does not exist/i.test((e as Error).message)) throw e;
  }
  // Fallback: only the functions that are already live.
  const list = await rpc<EditionSummary[]>("ft_editions", { include_drafts: true });
  const editions = await Promise.all(
    list.slice(0, 30).map(async (x): Promise<AdminEdition> => {
      const e = await rpc<Edition | null>("ft_edition", { d: x.edition_date, include_drafts: true });
      return {
        edition_date: x.edition_date, subject: x.subject, status: x.status, published_at: x.published_at,
        section_count: x.section_count, video: e?.video ?? null, review: e?.review ?? null,
      };
    }),
  );
  return { mode: "partial", at: stats.at, stats, totals: null, items: null, sources: null, editions, log: null };
}

// ---------- time: everything runs on New York time ----------
const TZ = "America/New_York";

function parts(d: Date, tz = TZ) {
  const p = Object.fromEntries(
    new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
      .formatToParts(d).map((x) => [x.type, x.value]),
  );
  return { y: +p.year, m: +p.month, d: +p.day, h: +p.hour, mi: +p.minute };
}

export const nyDate = (d = new Date()) => {
  const p = parts(d);
  return `${p.y}-${String(p.m).padStart(2, "0")}-${String(p.d).padStart(2, "0")}`;
};

export function addDays(date: string, n: number) {
  const t = new Date(`${date}T12:00:00Z`);
  t.setUTCDate(t.getUTCDate() + n);
  return t.toISOString().slice(0, 10);
}

/** The UTC instant of hh:mm New York time on `date` (DST-safe). */
export function nyAt(date: string, hh: number, mm = 0) {
  const [y, m, d] = date.split("-").map(Number);
  let t = Date.UTC(y, m - 1, d, hh, mm);
  for (let i = 0; i < 2; i++) {
    const p = parts(new Date(t));
    const shown = Date.UTC(p.y, p.m - 1, p.d, p.h, p.mi);
    t += Date.UTC(y, m - 1, d, hh, mm) - shown;
  }
  return new Date(t);
}

export const fmtTime = (iso: string | null, tz = TZ) =>
  iso ? new Date(iso).toLocaleTimeString("en-US", { timeZone: tz, hour: "numeric", minute: "2-digit" }) : "—";
export const fmtDay = (date: string) =>
  new Date(`${date}T12:00:00Z`).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", timeZone: "UTC" });
export const fmtWhen = (iso: string | null) =>
  iso ? new Date(iso).toLocaleString("en-US", { timeZone: TZ, month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : "—";
export const ago = (iso: string | null, now = Date.now()) => {
  if (!iso) return "never";
  const m = Math.round((now - new Date(iso).getTime()) / 60000);
  if (m < 60) return `${Math.max(m, 0)}m ago`;
  if (m < 48 * 60) return `${Math.round(m / 60)}h ago`;
  return `${Math.round(m / 1440)}d ago`;
};

// ---------- today's pipeline (plan/WORKFLOW.md timetable) ----------
export type StepState = "done" | "wait" | "late" | "fail";
export type Step = {
  key: string; title: string; who: string; due: Date; dueLabel: string; edmonton: string;
  state: StepState; detail: string; label?: string;
};

export const PICK_TARGET = 3;

export function todayPipeline(s: Snapshot, now = new Date()) {
  const today = nyDate(now);
  const windowStart = nyAt(addDays(today, -1), 6);
  const sweepDue = nyAt(today, 6);
  const picksDue = nyAt(today, 6, 45);
  const draftDue = nyAt(today, 7, 15);
  const reviewDue = nyAt(today, 7, 45);
  const shortDue = nyAt(today, 8, 45);
  const past = (d: Date, graceMin = 0) => now.getTime() > d.getTime() + graceMin * 60000;
  const edm = (d: Date) => fmtTime(d.toISOString(), "America/Edmonton");
  const et = (d: Date) => fmtTime(d.toISOString());

  const inWindow = (iso: string | null, from: Date, to?: Date) =>
    !!iso && new Date(iso) >= from && (!to || new Date(iso) < to);
  const sinceCutoff = s.items ? s.items.filter((i) => inWindow(i.collected_at, sweepDue)).length : 0;
  const collected = s.items ? s.items.filter((i) => inWindow(i.collected_at, windowStart, sweepDue)).length : s.stats.items24h;
  const picks = s.items ? s.items.filter((i) => i.status === "picked" && inWindow(i.picked_at, windowStart)).length : s.stats.picks24h;
  const ed = s.editions.find((e) => e.edition_date === today) ?? null;

  const steps: Step[] = [];
  steps.push({
    key: "sweep", title: "Collect items + final sweep", who: "FT-sources · FT-community", due: sweepDue,
    dueLabel: et(sweepDue), edmonton: edm(sweepDue),
    state: collected > 0 ? (past(sweepDue) ? "done" : "wait") : past(sweepDue) ? "fail" : "wait",
    detail: s.items
      ? `${collected} in today's window${sinceCutoff ? ` · ${sinceCutoff} since 6 AM for tomorrow` : ""}`
      : `${collected} in the last 24h`,
  });
  steps.push({
    key: "picks", title: "Fact-check + mark picks", who: "FT-PM", due: picksDue,
    dueLabel: et(picksDue), edmonton: edm(picksDue),
    state: picks >= PICK_TARGET ? "done" : picks > 0 ? (past(picksDue) ? "late" : "wait") : past(picksDue) ? "fail" : "wait",
    detail: `${picks} of ~${PICK_TARGET} picks`,
  });
  steps.push({
    key: "draft", title: "Post the edition draft", who: "FT-editor", due: draftDue,
    dueLabel: et(draftDue), edmonton: edm(draftDue),
    state: ed ? "done" : past(draftDue) ? "fail" : "wait",
    detail: ed ? `${ed.status === "published" ? "Published" : "Draft"} · ${ed.section_count} sections` : "No draft yet",
  });
  const r = ed?.review ?? null;
  steps.push({
    key: "review", title: "Auto-review publishes or holds", who: "Auto-review (for pomo651)", due: reviewDue,
    dueLabel: et(reviewDue), edmonton: edm(reviewDue),
    state: ed?.status === "published" ? "done" : r?.result === "held" ? "fail" : past(reviewDue, 10) ? "late" : "wait",
    label: ed?.status !== "published" && r?.result === "held" ? "Held" : undefined,
    detail: ed?.status === "published"
      ? `Published ${fmtTime(ed.published_at)} ET${r?.result === "published" ? " by auto-review" : ""}`
      : r?.result === "held" ? `Held: ${r.reasons.length} problem${r.reasons.length === 1 ? "" : "s"}`
      : past(reviewDue, 10) ? "Didn't run, or nothing to review" : "Runs at 7:45 AM ET",
  });
  const v = ed?.video ?? null;
  steps.push({
    key: "short", title: "Build the daily Short · owner approves", who: "FT-video → pomo651", due: shortDue,
    dueLabel: `${fmtTime(nyAt(today, 8).toISOString())}–${et(shortDue)}`, edmonton: `${fmtTime(nyAt(today, 8).toISOString(), "America/Edmonton")}–${edm(shortDue)}`,
    state: v?.status === "approved" || v?.status === "uploaded" ? "done" : v ? "late" : past(shortDue) ? "late" : "wait",
    detail: v ? (v.status === "draft" ? "Waiting for your approval" : `Short ${v.status}`) : "No Short yet",
    label: v?.status === "draft" ? "Approve" : undefined,
  });

  return { today, windowStart, steps, edition: ed, collected, picks };
}

// Last N days of editions, oldest first, for the streak strip.
export function streak(s: Snapshot, n = 14, now = new Date()) {
  const today = nyDate(now);
  return Array.from({ length: n }, (_, k) => {
    const date = addDays(today, k - n + 1);
    const e = s.editions.find((x) => x.edition_date === date);
    const state = e?.status === "published" ? "published" : e?.review?.result === "held" ? "held" : e ? "draft" : "none";
    return { date, state };
  });
}

// Things that need a human, most urgent first.
export function needsYou(s: Snapshot) {
  const out: { tone: "r" | "o"; text: string; href: string }[] = [];
  for (const e of s.editions) {
    if (e.status === "draft" && e.review?.result === "held")
      out.push({ tone: "r", text: `${fmtDay(e.edition_date)} edition held by auto-review: ${e.review.reasons[0] ?? ""}`, href: "/admin/editions" });
    if (e.video?.status === "draft")
      out.push({ tone: "o", text: `${fmtDay(e.edition_date)} Short waiting for your approval`, href: "/admin/editions" });
  }
  if (s.items) {
    const risky = s.items.filter((i) => i.status === "picked" && i.category === "allegation" && i.evidence !== "official" && i.evidence !== "firm_x_post");
    if (risky.length) out.push({ tone: "r", text: `${risky.length} picked allegation${risky.length === 1 ? "" : "s"} without official evidence`, href: "/admin/items?status=picked" });
    const noCat = s.items.filter((i) => i.status === "picked" && !i.category).length;
    if (noCat) out.push({ tone: "o", text: `${noCat} pick${noCat === 1 ? "" : "s"} with no category`, href: "/admin/items?status=picked" });
    const noEvidence = s.items.filter((i) => i.status === "picked" && !i.evidence_url).length;
    if (noEvidence) out.push({ tone: "o", text: `${noEvidence} pick${noEvidence === 1 ? "" : "s"} with no evidence link`, href: "/admin/items?status=picked" });
  }
  return out;
}

// Problems on one item (red left edge in the Items table).
export function itemFlags(i: AdminItem) {
  const f: string[] = [];
  if (i.status === "picked" && i.category === "allegation" && i.evidence !== "official" && i.evidence !== "firm_x_post") f.push("allegation without official evidence");
  if (i.status === "picked" && !i.category) f.push("no category");
  if (i.status === "picked" && !i.evidence_url) f.push("no evidence link");
  return f;
}
