import { NextResponse } from "next/server";
import { rpc } from "@/lib/db";
import { getMonitor, type MonStep } from "@/lib/monitor";

export const dynamic = "force-dynamic";

const SITE = "https://prop-firm-newsletter.vercel.app";
// 7:20 AM ET: the steps due before the 7:45 publish. 8:55 AM ET: everything.
const EARLY = ["collect", "picks", "draft"];

const ny = () =>
  Object.fromEntries(
    new Intl.DateTimeFormat("en-CA", { timeZone: "America/New_York", hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
      .formatToParts(new Date()).map((p) => [p.type, +p.value || p.value]),
  ) as { hour: number; minute: number };

async function email(subject: string, text: string) {
  const key = process.env.RESEND_API_KEY;
  const to = process.env.NOTIFY_EMAIL;
  if (!key || !to) return "email not configured";
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: "Funded Tape <onboarding@resend.dev>", to: [to], subject: `[Funded Tape] ${subject}`, text }),
  });
  return res.ok ? "sent" : `email failed: ${res.status}`;
}

// Called by pg_cron (funded-tape-monitor-early / -full). Emails pomo651 once per
// problem per day: red (fail) steps, plus amber "needs you" / late at the full check.
// ?check=early|full runs a checkpoint by hand.
export async function POST(req: Request) {
  const secret = process.env.FT_JOB_SECRET;
  if (!secret || req.headers.get("x-job-secret") !== secret) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }
  const forced = new URL(req.url).searchParams.get("check");
  const t = ny();
  const check = forced ?? (t.hour === 7 && t.minute >= 15 && t.minute < 35 ? "early" : t.hour === 8 && t.minute >= 50 ? "full" : null);
  if (check !== "early" && check !== "full") return NextResponse.json({ ok: true, idle: `not a checkpoint (${t.hour}:${t.minute} ET)` });

  let today;
  try {
    today = (await getMonitor(1)).days[0];
  } catch (e) {
    // the DB itself is unreachable: that's the most important alert of all
    const sent = await email("RED: monitor can't read the database", `The ${check} check couldn't read Supabase:\n${(e as Error).message}\n\nThe 7:45 publish will fail too until this is fixed.\n${SITE}/admin/monitor`);
    return NextResponse.json({ ok: false, error: (e as Error).message, email: sent }, { status: 500 });
  }
  if (today.state === "off") return NextResponse.json({ ok: true, idle: "before launch" });

  const watch = (s: MonStep) =>
    (check === "full" || EARLY.includes(s.key)) && (s.state === "fail" || (check === "full" && (s.state === "needs" || s.state === "late")));
  const problems = today.steps.filter(watch);
  if (problems.length === 0) return NextResponse.json({ ok: true, check, date: today.date, state: today.state, alerts: 0 });

  // only what hasn't been emailed before
  const fresh = await rpc<{ step: string; state: string; detail: string }[]>("ft_monitor_record", {
    rows: problems.map((s) => ({ edition_date: today.date, step: s.key, state: s.state, detail: s.detail })),
  });
  if (fresh.length === 0) return NextResponse.json({ ok: true, check, date: today.date, alerts: 0, note: "already emailed" });

  const red = fresh.some((f) => f.state === "fail");
  const byKey = Object.fromEntries(today.steps.map((s) => [s.key, s]));
  const lines = fresh.map((f) => {
    const s = byKey[f.step];
    const tag = f.state === "fail" ? "RED" : f.state === "needs" ? "NEEDS YOU" : "LATE";
    return `- ${tag} · ${s.title} (${s.who}, due ${s.due} ET): ${f.detail}`;
  });
  const sent = await email(
    `${red ? "RED" : "Needs you"}: ${fresh.length} step${fresh.length === 1 ? "" : "s"} on ${today.date}`,
    [`${check === "early" ? "7:20 AM ET check (before the 7:45 publish)" : "8:55 AM ET check"} for the ${today.date} edition:`, "", ...lines, "", `Monitor: ${SITE}/admin/monitor`, "", "— Funded Tape monitor (local FT-team)"].join("\n"),
  );
  return NextResponse.json({ ok: true, check, date: today.date, alerts: fresh.length, email: sent });
}
