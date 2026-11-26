import { isAdmin } from "@/lib/admin";
import { Head, Pill } from "@/components/admin/ui";

export const dynamic = "force-dynamic";
export const metadata = { title: "Workflows" };

// Source of truth: plan/WORKFLOW.md, plan/TEAM.md, site/BOT_API.md, CLAUDE.md.
// When one of those changes, update this page in the same PR.

const DAY = [
  { t: "by 6:00", e: "5:00", who: "FT-sources · FT-community", what: "Post every item as new. Final sweep." },
  { t: "by 6:45", e: "5:45", who: "FT-PM", what: "Fact-check on the firm's own page. Mark ~3 picks." },
  { t: "by 7:15", e: "6:15", who: "FT-editor", what: "Post the edition as draft." },
  { t: "7:45", e: "6:45", who: "Auto-review", what: "Publish if every check passes, else hold + email pomo651." },
  { t: "8:00–8:45", e: "7:00–7:45", who: "FT-video → pomo651", what: "Build the Short. Upload only after approval." },
];

const C = ({ children }: { children: React.ReactNode }) => <span className="ft-code">{children}</span>;

export default async function Workflows() {
  if (!(await isAdmin())) return null;
  return (
    <>
      <Head title="Workflows" sub="How a day runs, who does what, and what to do when something breaks." />

      <div className="bz-card">
        <div className="bz-hd"><h2>1 · The daily run</h2><span className="bz-small">Edition = 24h up to 6:00 AM ET · first live Fri Nov 27</span></div>
        <div className="ft-chain">
          {DAY.map((d) => (
            <div key={d.t}><small>{d.t} ET</small><b>{d.who}</b><span>{d.what}</span></div>
          ))}
        </div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>ET</th><th>Edmonton (winter)</th><th>Who</th><th>What</th><th>API</th></tr></thead>
            <tbody>
              {DAY.map((d, k) => (
                <tr key={d.t}>
                  <td className="bz-num"><b>{d.t}</b></td><td className="bz-num bz-small">{d.e}</td><td>{d.who}</td><td className="bz-small">{d.what}</td>
                  <td className="bz-small">{[<C key="a">POST /api/bot/items</C>, <C key="b">items status: picked</C>, <C key="c">POST /api/bot/editions</C>, <C key="d">pg_cron → /api/jobs/auto-publish</C>, <C key="e">POST /api/bot/videos</C>][k]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <details className="bz-help">
          <summary>Still open for pomo651 · <u>Show</u></summary>
          <ol>
            <li>Skip weekends?</li>
            <li>Keep a weekly Beehiiv recap next to the daily edition?</li>
            <li>Test an evening edition (cutoff ~5 PM ET) once open and click data exist.</li>
          </ol>
        </details>
      </div>

      <div className="bz-card">
        <div className="bz-hd"><h2>2 · Each morning in this admin</h2><span className="bz-small">~2 minutes, around 6:15–6:45 AM Edmonton</span></div>
        <ol className="ft-list">
          <li><b>Today</b>: every pipeline row green or grey? A red row names the late step.</li>
          <li><b>Picks today</b> near 3, and no red-edged pick in <b>Items</b> (missing category / evidence, risky allegation).</li>
          <li><b>Editions</b>: draft in by 7:15 ET? After 7:45 ET it is Published or Held (with reasons).</li>
          <li>Held? Fix with FT-grok, or open <b>Review</b>, enter the owner key, <b>Publish edition</b>.</li>
          <li>Short <Pill v="draft" label="Needs approval" />: watch it, then <b>Approve Short for upload</b>. Mark uploaded with the public URL.</li>
          <li>Weekly: <b>Sources → Silent 14 days</b>. Drop or replace dead sources with FT-PM.</li>
        </ol>
      </div>

      <div className="ft-2">
        <div className="bz-card">
          <h2>3 · Who owns what</h2>
          <table className="bz-t">
            <tbody>
              <tr><td className="nw"><b>FT-PM</b></td><td className="bz-small">Source list, fact-checks, picks. Holds BOT_TOKEN.</td></tr>
              <tr><td className="nw"><b>FT-sources</b></td><td className="bz-small">Firm sites, help centers, announcements.</td></tr>
              <tr><td className="nw"><b>FT-community</b></td><td className="bz-small">X, Reddit, YouTube, Discord, reviews.</td></tr>
              <tr><td className="nw"><b>FT-editor</b></td><td className="bz-small">Edition draft (repo + site).</td></tr>
              <tr><td className="nw"><b>FT-video</b></td><td className="bz-small">Daily Short from the published edition.</td></tr>
              <tr><td className="nw"><b>Drew</b></td><td className="bz-small">Repo, infra, docs.</td></tr>
              <tr><td className="nw"><b>pomo651</b></td><td className="bz-small">Website. The only one who publishes or uploads.</td></tr>
              <tr><td className="nw"><b>local FT-team</b></td><td className="bz-small">pomo651 + Claude Code: <C>site/</C>, migrations, bot API, deploys, auto-review.</td></tr>
            </tbody>
          </table>
        </div>
        <div className="bz-card">
          <h2>4 · Picks and editorial rules</h2>
          <ol className="ft-list">
            <li><b>Only FT-PM picks</b>, only after checking the firm&apos;s own page. Picks go public at once.</li>
            <li><b>Official source first.</b> A staff or CEO reply on X is not an official statement.</li>
            <li><b>No invented numbers.</b> Not in the source, not in the edition.</li>
            <li><b>Allegations</b>: pick only with a firm response or documented policy. Always labelled.</li>
            <li><b>Payout totals</b> are unaudited and never a pick on their own.</li>
            <li><b>Views and likes</b> are not evidence.</li>
            <li><b>Caveats in notes</b> (&quot;unaudited&quot;, &quot;not confirmed for forex&quot;). Disclose affiliate links.</li>
            <li><b>Every item links its source</b> (<C>url</C> required).</li>
          </ol>
        </div>
      </div>

      <div className="ft-2">
        <div className="bz-card">
          <h2>5 · Auto-review: the 6 checks</h2>
          <ol className="ft-list">
            <li>A draft exists for today&apos;s New York date.</li>
            <li>It has a subject and at least one section.</li>
            <li>Every section has headline, body, why, and a source link.</li>
            <li>Each section cites at least one <b>picked</b> item (same <C>url</C>).</li>
            <li>A picked allegation has evidence <C>official</C> or <C>firm_x_post</C>.</li>
            <li>No placeholders: TBD, TODO, XXX, lorem ipsum, [name…].</li>
          </ol>
          <div className="bz-small">Runs once at 7:45 AM ET (pg_cron 11:45 + 12:45 UTC, acts only in the 7 AM NY hour). Shorts are never auto-approved.</div>
        </div>
        <div className="bz-card">
          <h2>6 · When something breaks</h2>
          <table className="bz-t">
            <tbody>
              <tr className="bad"><td><b>Edition held</b></td><td className="bz-small">Read the reasons (email + Editions). Ask FT-editor/FT-PM to re-post, or publish by hand.</td></tr>
              <tr className="bad"><td><b>No draft by 7:15</b></td><td className="bz-small">Auto-review will hold it. Ping FT-editor; a late draft needs a manual publish.</td></tr>
              <tr className="warn"><td><b>Fewer than 3 picks</b></td><td className="bz-small">Fine on a slow day. Never pick an unchecked item to hit the number.</td></tr>
              <tr className="warn"><td><b>Fix a published edition</b></td><td className="bz-small">Owner view → Unpublish. Bot re-posts the draft. Publish again.</td></tr>
              <tr className="warn"><td><b>Review job didn&apos;t run</b></td><td className="bz-small">Run it by hand: <C>POST /api/jobs/auto-publish?force=1&amp;date=YYYY-MM-DD</C> with <C>x-job-secret</C>.</td></tr>
              <tr><td><b>Bot gets 401</b></td><td className="bz-small">Wrong BOT_TOKEN. pomo651 re-issues it to FT-PM. Never commit it.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="ft-2">
        <div className="bz-card">
          <h2>7 · Repo and pull requests</h2>
          <ol className="ft-list">
            <li><b>FT-grok PR</b> starts with &quot;Done by FT-grok — needs local FT-team review.&quot; It never merges itself.</li>
            <li>Local FT-team, every session: <C>gh pr list --state open</C>, scan for secrets, build <C>site/</C> if touched, merge if clean, then follow through on renames and rules.</li>
            <li><b>Local PR</b> starts with &quot;Done by local FT-team (pomo651 + Claude Code).&quot; Add &quot;FT-grok: please read before your next run.&quot; when bots must act.</li>
            <li>Every change is explained in <C>README.md</C> (and <C>plan/TEAM.md</C> for roles).</li>
            <li>Merge to <C>main</C> = production deploy. Each PR gets a preview. Never <C>vercel deploy</C> from <C>site/</C>.</li>
          </ol>
        </div>
        <div className="bz-card" id="data">
          <h2>8 · Changing the data</h2>
          <ol className="ft-list">
            <li>FT-grok asks for a field or table in a PR or issue.</li>
            <li>Local FT-team writes the migration in <C>supabase/migrations/</C>, updates the bot API and <C>site/BOT_API.md</C>.</li>
            <li>Apply from <C>~/@Pomo651/blackout-clock</C>: <C>supabase db query --linked -f &lt;file&gt;</C>. Cron SQL: swap in FT_JOB_SECRET, never commit it.</li>
            <li>Deploy, then tell FT-grok in the PR.</li>
          </ol>
          <div className="bz-small">This admin reads <C>ft_admin_snapshot</C> (migration <C>20261127000000_funded_tape_admin.sql</C>, read-only). Without it, Items and Sources show partial data.</div>
        </div>
      </div>
    </>
  );
}
