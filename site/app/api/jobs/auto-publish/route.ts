import { NextResponse } from "next/server";
import { rpc } from "@/lib/db";

export const dynamic = "force-dynamic";

const SITE = "https://prop-firm-newsletter.vercel.app";

type Result = { result: "published" | "held" | "skipped"; reasons: string[]; subject: string | null; edition_date: string };

const nyParts = (d: Date) =>
  Object.fromEntries(
    new Intl.DateTimeFormat("en-CA", { timeZone: "America/New_York", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", hourCycle: "h23" })
      .formatToParts(d)
      .map((p) => [p.type, p.value]),
  );

async function notify(r: Result) {
  const key = process.env.RESEND_API_KEY;
  const to = process.env.NOTIFY_EMAIL;
  if (!key || !to) return "email not configured";
  const head =
    r.result === "published"
      ? `Published: ${r.subject}`
      : r.result === "held"
        ? `HELD, needs you: ${r.edition_date} edition`
        : `Skipped: ${r.edition_date} already published`;
  const text = [
    r.result === "published" ? `The ${r.edition_date} edition passed the auto-review and is live:` : `The ${r.edition_date} edition was NOT published.`,
    r.result === "published" ? `${SITE}/daily/${r.edition_date}` : "",
    ...(r.result === "held" ? ["", "Why:", ...r.reasons.map((x) => `- ${x}`), "", "Fix it with FT-grok, or review and publish it yourself on the draft page (preview link + owner key)."] : []),
    "",
    "— Funded Tape auto-publish (local FT-team)",
  ].join("\n");
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: "Funded Tape <onboarding@resend.dev>", to: [to], subject: `[Funded Tape] ${head}`, text }),
  });
  return res.ok ? "sent" : `email failed: ${res.status}`;
}

// Called by pg_cron at 11:45 and 12:45 UTC (see supabase/migrations/*_auto_publish.sql).
// Acts only in the 7 AM hour in New York, so it runs once a day at 7:45 ET in EST and EDT.
// ?date=YYYY-MM-DD&force=1 runs it by hand for a given edition.
export async function POST(req: Request) {
  const secret = process.env.FT_JOB_SECRET;
  if (!secret || req.headers.get("x-job-secret") !== secret) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }
  const q = new URL(req.url).searchParams;
  const ny = nyParts(new Date());
  if (q.get("force") !== "1" && ny.hour !== "07") {
    return NextResponse.json({ ok: true, idle: `not 7 AM in New York (hour ${ny.hour})` });
  }
  const date = q.get("date") ?? `${ny.year}-${ny.month}-${ny.day}`;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return NextResponse.json({ error: "bad date" }, { status: 400 });
  const r = await rpc<Result>("ft_auto_publish", { d: date });
  const email = await notify(r);
  return NextResponse.json({ ok: true, ...r, email });
}
