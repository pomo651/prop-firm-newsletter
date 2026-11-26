import { isAdmin, fmtDay, fmtWhen } from "@/lib/admin";
import { getMonitor, type MonDay, type MonState } from "@/lib/monitor";
import { Head, Pill } from "@/components/admin/ui";

export const dynamic = "force-dynamic";
export const metadata = { title: "Monitor" };

const ICON: Record<MonState, string> = { ok: "✓", late: "!", needs: "!", fail: "×", wait: "·", off: "–" };
const CLS: Record<MonState, string> = { ok: "done", late: "late", needs: "late", fail: "fail", wait: "wait", off: "wait" };
const DAY_LABEL: Record<MonDay["state"], string> = { ok: "All green", late: "Needs a look", fail: "Red", wait: "In progress", off: "Before launch" };
const DAY_PILL: Record<MonDay["state"], string> = { ok: "done", late: "late", fail: "fail", wait: "wait", off: "off" };
const STEP_LABEL: Record<string, string> = { late: "Late", needs: "Needs you" };

export default async function Monitor() {
  if (!(await isAdmin())) return null;
  const m = await getMonitor(14);
  const today = m.days[0];
  const live = m.days.filter((d) => d.state !== "off");
  const green = live.filter((d) => d.state === "ok").length;
  const red = today.steps.filter((s) => s.state === "fail");
  const cols = (live[0] ?? today).steps.length ? (live[0] ?? today).steps : [];

  return (
    <>
      <Head title="Monitor" sub="Every step, every day. Green each day is the goal. Red or blocked emails pomo651 at 7:20 and 8:55 AM ET." />

      {red.length > 0 && (
        <div className="bz-alert">
          <span>Today is red: {red.map((s) => `${s.title.toLowerCase()} (${s.detail})`).join(", ")}.</span>
          <a href="#today">Show</a>
        </div>
      )}

      <div className="bz-kpis">
        <div className={`bz-kpi${today.state === "fail" ? " warn" : ""}`}><span>Today · {fmtDay(today.date)}</span><b>{DAY_LABEL[today.state]}</b><small>{today.steps.filter((s) => s.state === "ok").length} of {today.steps.filter((s) => s.state !== "off").length} steps done</small></div>
        <div className="bz-kpi"><span>Green days</span><b className="bz-num">{green}<small> / {live.length}</small></b><small>since launch, last 14 days</small></div>
        <div className="bz-kpi"><span>Red steps, last 14 days</span><b className="bz-num">{live.reduce((n, d) => n + d.steps.filter((s) => s.state === "fail").length, 0)}</b><small>missing or held</small></div>
        <div className="bz-kpi"><span>Alerts sent</span><b className="bz-num">{m.alerts.length}</b><small>{m.alerts[0] ? `last ${fmtWhen(m.alerts[0].sent_at)} ET` : "none yet"}</small></div>
      </div>

      <div className="bz-card flush" id="today">
        <div className="bz-bar"><b>Today, step by step</b><span className="bz-sp" /><span className="bz-small">checked {fmtWhen(m.at)} ET</span></div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Step</th><th>Who</th><th className="r">Due (ET)</th><th>Status</th><th>Detail</th></tr></thead>
            <tbody>
              {today.steps.length === 0 && <tr><td colSpan={5} className="bz-small">Before launch: monitoring starts with the first live edition (Thu Nov 26).</td></tr>}
              {today.steps.map((s) => (
                <tr key={s.key} className={s.state === "fail" ? "bad" : s.state === "late" || s.state === "needs" ? "warn" : ""}>
                  <td><div className="ft-step"><i className={CLS[s.state]}>{ICON[s.state]}</i><b>{s.title}</b></div></td>
                  <td className="bz-small">{s.who}</td>
                  <td className="r bz-num">{s.due}</td>
                  <td><Pill v={s.state === "off" ? "off" : CLS[s.state]} label={STEP_LABEL[s.state] ?? (s.state === "off" ? "Off" : undefined)} /></td>
                  <td className="bz-small">{s.detail}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bz-card flush">
        <div className="bz-bar"><b>Last 14 days</b><span className="bz-sp" /><span className="bz-small">{green} of {live.length} live days all green</span></div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Day</th><th>Overall</th>{cols.map((c) => <th key={c.key}>{c.title}</th>)}</tr></thead>
            <tbody>
              {live.length === 0 && <tr><td colSpan={cols.length + 2} className="bz-small">No live days yet. The first live edition is Thu Nov 26.</td></tr>}
              {live.map((d) => (
                <tr key={d.date} className={d.state === "fail" ? "bad" : d.state === "late" ? "warn" : ""}>
                  <td className="nw"><b>{fmtDay(d.date)}</b></td>
                  <td><Pill v={DAY_PILL[d.state]} label={DAY_LABEL[d.state]} /></td>
                  {d.steps.length === 0
                    ? <td colSpan={cols.length} className="bz-small">—</td>
                    : d.steps.map((s) => (
                      <td key={s.key} title={`${s.title}: ${s.detail}`}>
                        <div className="ft-step"><i className={CLS[s.state]}>{ICON[s.state]}</i></div>
                      </td>
                    ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bz-card flush">
        <div className="bz-bar"><b>Alerts sent</b><span className="bz-sp" /><span className="bz-small">Each problem is emailed once per day</span></div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Sent (ET)</th><th>Edition</th><th>Step</th><th>Status</th><th>Detail</th></tr></thead>
            <tbody>
              {m.alerts.length === 0 && <tr><td colSpan={5} className="bz-small">No alerts yet.</td></tr>}
              {m.alerts.map((a, k) => (
                <tr key={k}>
                  <td className="nw bz-num">{fmtWhen(a.sent_at)}</td>
                  <td className="nw">{fmtDay(a.edition_date)}</td>
                  <td>{a.step}</td>
                  <td><Pill v={a.state === "fail" ? "fail" : "late"} label={a.state === "fail" ? "Red" : STEP_LABEL[a.state] ?? a.state} /></td>
                  <td className="bz-small">{a.detail}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <details className="bz-help">
        <summary>How each step is graded · <u>Show</u></summary>
        <ol>
          <li><b>Collect</b>: green once at least one item arrived in the 24h window up to 6:00 AM ET; red if none.</li>
          <li><b>Picks</b>: green if a pick was marked by 6:45; amber if only between 6:45 and 7:45; red if none.</li>
          <li><b>Draft</b>: green if first posted by 7:15; amber if later; red if missing.</li>
          <li><b>Auto-review + publish</b>: green when published; red when held or not run by 7:55.</li>
          <li><b>Build Short / Approve Short</b>: off until FT-video posts its first Short. Then red if missing by 8:45, amber &ldquo;Needs you&rdquo; until you approve.</li>
          <li>Alerts: 7:20 AM ET (collect, picks, draft: red only) and 8:55 AM ET (everything, incl. amber). The 7:45 publish also emails its own result.</li>
        </ol>
      </details>
    </>
  );
}
