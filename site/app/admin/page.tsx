import Link from "next/link";
import { getSnapshot, isAdmin, needsYou, streak, todayPipeline, fmtDay, PICK_TARGET } from "@/lib/admin";
import { CATEGORY_LABEL, type Category } from "@/lib/types";
import { Bars, EVIDENCE, Head, PartialNote, Pill } from "@/components/admin/ui";

export const dynamic = "force-dynamic";
export const metadata = { title: "Today" };

const ICON = { done: "✓", wait: "·", late: "!", fail: "×" } as const;

export default async function Today() {
  if (!(await isAdmin())) return null;
  const s = await getSnapshot();
  const now = new Date();
  const p = todayPipeline(s, now);
  const strip = streak(s, 14, now);
  const todo = needsYou(s);
  const problems = p.steps.filter((x) => x.state === "fail" || x.state === "late");
  const published14 = strip.filter((d) => d.state === "published").length;
  const silent = s.sources ? s.sources.filter((x) => x.active && x.items_recent === 0).length : null;
  const picked = s.items?.filter((i) => i.status === "picked") ?? [];
  const count = <K extends string>(xs: (K | null)[], labels: Record<string, string>) =>
    Object.entries(labels).map(([k, label]) => ({ label, n: xs.filter((x) => x === k).length }));

  return (
    <>
      <Head title={`Today · ${fmtDay(p.today)}`} sub="Edition covers the 24 hours up to 6:00 AM ET. Times in ET, Edmonton in grey.">
        <Link className="bz-btn ghost sm" href="/admin/workflows">Timetable</Link>
        <a className="bz-btn sm" href="/daily" target="_blank" rel="noreferrer">Open /daily</a>
      </Head>

      {s.mode === "partial" && <PartialNote />}
      {problems.length > 0 && (
        <div className="bz-alert">
          <span>{problems.length} step{problems.length === 1 ? "" : "s"} behind: {problems.map((x) => x.title.toLowerCase()).join(", ")}.</span>
          <a href="#pipeline">Show</a>
        </div>
      )}

      <div className="bz-kpis">
        <Link className="bz-kpi" href="/admin/items"><span>Items, last 24h</span><b className="bz-num">{s.stats.items24h}</b><small>{s.stats.items} total</small></Link>
        <Link className={`bz-kpi${p.picks < PICK_TARGET ? " warn" : ""}`} href="/admin/items?status=picked"><span>Picks today</span><b className="bz-num">{p.picks}<small> / ~{PICK_TARGET}</small></b><small>{s.stats.picks} total</small></Link>
        <Link className="bz-kpi" href="/admin/editions"><span>Published, last 14 days</span><b className="bz-num">{published14}<small> / 14</small></b><small>{s.stats.editions} all time</small></Link>
        <Link className={`bz-kpi${silent ? " warn" : ""}`} href="/admin/sources"><span>Active sources</span><b className="bz-num">{s.stats.sources}</b><small>{silent === null ? "silent: needs migration" : `${silent} silent for 14 days`}</small></Link>
      </div>

      <div className="bz-card flush" id="pipeline">
        <div className="bz-bar"><b>Today&apos;s pipeline</b><span className="bz-sp" /><span className="bz-small">checked {now.toLocaleTimeString("en-US", { timeZone: "America/New_York", hour: "numeric", minute: "2-digit" })} ET</span></div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Step</th><th>Who</th><th className="r">Due (ET)</th><th className="r">Edmonton</th><th>Status</th><th>Detail</th></tr></thead>
            <tbody>
              {p.steps.map((x) => (
                <tr key={x.key} className={x.state === "fail" ? "bad" : x.state === "late" ? "warn" : ""}>
                  <td><div className="ft-step"><i className={x.state}>{ICON[x.state]}</i><b>{x.title}</b></div></td>
                  <td className="bz-small">{x.who}</td>
                  <td className="r bz-num">{x.dueLabel}</td>
                  <td className="r bz-num bz-small">{x.edmonton}</td>
                  <td><Pill v={x.state} label={x.label} /></td>
                  <td className="bz-small">{x.detail}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="ft-2">
        <div className="bz-card">
          <h2>Needs you</h2>
          {todo.length === 0 ? (
            <div className="bz-small">Nothing waiting. Held drafts, Shorts to approve and risky picks show up here.</div>
          ) : (
            <div className="ft-todo">
              {todo.map((t, k) => (
                <Link key={k} href={t.href}><Pill v={t.tone === "r" ? "fail" : "late"} label={t.tone === "r" ? "Fix" : "Check"} /><span>{t.text}</span></Link>
              ))}
            </div>
          )}
        </div>
        <div className="bz-card">
          <div className="bz-hd"><h2>Editions, last 14 days</h2><span className="bz-small">{published14} published</span></div>
          <div className="ft-strip">
            {strip.map((d) => (
              <div key={d.date} title={`${fmtDay(d.date)}: ${d.state}`}><b className={d.state} />{d.date.slice(8)}</div>
            ))}
          </div>
          <div className="ft-legend">
            <span style={{ "--c": "var(--ok)" } as React.CSSProperties}>Published</span>
            <span style={{ "--c": "var(--bad)" } as React.CSSProperties}>Held</span>
            <span style={{ "--c": "var(--warn-soft)" } as React.CSSProperties}>Draft only</span>
            <span style={{ "--c": "var(--zinc)" } as React.CSSProperties}>None</span>
          </div>
        </div>
      </div>

      <div className="ft-3">
        <div className="bz-card">
          <h2>Picks by category</h2>
          {s.items ? <Bars rows={[...count(picked.map((i) => i.category), CATEGORY_LABEL as Record<Category, string>), { label: "No category", n: picked.filter((i) => !i.category).length }]} /> : <div className="bz-small">Needs the admin migration.</div>}
        </div>
        <div className="bz-card">
          <h2>Picks by evidence</h2>
          {s.items ? <Bars rows={[...count(picked.map((i) => i.evidence), EVIDENCE), { label: "Not set", n: picked.filter((i) => !i.evidence).length }]} /> : <div className="bz-small">Needs the admin migration.</div>}
          <div className="bz-small">Aim: most picks backed by the firm&apos;s own page.</div>
        </div>
        <div className="bz-card">
          <h2>Items by collector</h2>
          {s.items ? <Bars rows={["FT-sources", "FT-community", "FT-PM"].map((w) => ({ label: w, n: s.items!.filter((i) => i.collected_by === w).length })).concat([{ label: "Not set", n: s.items.filter((i) => !i.collected_by).length }])} /> : <div className="bz-small">Needs the admin migration.</div>}
        </div>
      </div>

      <div className="bz-card">
        <div className="bz-hd"><h2>Audience: not connected yet</h2><span className="bz-small">Decides morning vs evening send</span></div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Metric</th><th>Where it lives</th><th>Why we watch it</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td><b>Subscribers + new per day</b></td><td className="bz-small">Beehiiv</td><td className="bz-small">Is the daily cadence growing the list?</td><td><Pill v="none" label="Not connected" /></td></tr>
              <tr><td><b>Open rate · click rate</b></td><td className="bz-small">Beehiiv</td><td className="bz-small">Morning vs 5 PM ET edition test</td><td><Pill v="none" label="Not connected" /></td></tr>
              <tr><td><b>Unsubscribes per edition</b></td><td className="bz-small">Beehiiv</td><td className="bz-small">Daily may be too often; weekend skip?</td><td><Pill v="none" label="Not connected" /></td></tr>
              <tr><td><b>Short views · watch time</b></td><td className="bz-small">YouTube Studio</td><td className="bz-small">Beta: is the Short worth making daily?</td><td><Pill v="none" label="Not connected" /></td></tr>
              <tr><td><b>/daily page views</b></td><td className="bz-small">Vercel Analytics</td><td className="bz-small">Web readers vs email readers</td><td><Pill v="none" label="Not connected" /></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
