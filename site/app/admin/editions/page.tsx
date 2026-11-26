import Link from "next/link";
import { getSnapshot, isAdmin, fmtDay, fmtWhen } from "@/lib/admin";
import { Head, Pill } from "@/components/admin/ui";

export const dynamic = "force-dynamic";
export const metadata = { title: "Editions & Shorts" };

export default async function Editions() {
  if (!(await isAdmin())) return null;
  const s = await getSnapshot();
  const q = `?preview=${encodeURIComponent(process.env.PREVIEW_KEY ?? "")}`;
  const drafts = s.editions.filter((e) => e.status === "draft").length;
  const shorts = s.editions.filter((e) => e.video?.status === "draft").length;

  return (
    <>
      <Head title="Editions & Shorts" sub="Publish, unpublish and approve Shorts on the draft page (owner key).">
        <a className="bz-btn sm" href={`/daily${q}`} target="_blank" rel="noreferrer">Open drafts view</a>
      </Head>
      {shorts > 0 && <div className="bz-alert o"><span>{shorts} Short{shorts === 1 ? "" : "s"} waiting for your approval. Nothing uploads without it.</span></div>}
      <div className="bz-card flush">
        <div className="bz-bar"><b>Editions</b><span className="bz-small">{s.editions.length} · {drafts} draft{drafts === 1 ? "" : "s"}</span><span className="bz-sp" /><span className="bz-small">Newest first</span></div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Date</th><th>Subject</th><th className="r">Sections</th><th>Edition</th><th>Auto-review</th><th>Short</th><th className="r"></th></tr></thead>
            <tbody>
              {s.editions.length === 0 && <tr><td colSpan={7}><div className="bz-empty">No editions yet. FT-editor posts the first draft by 7:15 AM ET.</div></td></tr>}
              {s.editions.map((e) => (
                <tr key={e.edition_date} className={e.review?.result === "held" && e.status === "draft" ? "bad" : ""}>
                  <td className="time bz-num"><b>{fmtDay(e.edition_date)}</b></td>
                  <td><div className="ft-title"><b>{e.subject}</b>{e.review?.result === "held" && <em>{e.review.reasons.join(" · ")}</em>}</div></td>
                  <td className="r bz-num">{e.section_count}</td>
                  <td><Pill v={e.status} label={e.status === "published" ? `Published ${fmtWhen(e.published_at)}` : "Draft"} /></td>
                  <td>{e.review ? <Pill v={e.review.result} label={`${e.review.result[0].toUpperCase()}${e.review.result.slice(1)} ${fmtWhen(e.review.ran_at)}`} /> : <span className="bz-small">Not run</span>}</td>
                  <td>{e.video ? <Pill v={e.video.status} label={e.video.status === "draft" ? "Needs approval" : e.video.status[0].toUpperCase() + e.video.status.slice(1)} /> : <span className="bz-small">None</span>}</td>
                  <td className="r">
                    {e.status === "published" && <Link className="bz-btn ghost sm" href={`/daily/${e.edition_date}`} target="_blank">Public page</Link>}
                    <Link className={`bz-btn sm${e.status === "published" && e.video?.status !== "draft" ? " ghost" : ""}`} href={`/daily/${e.edition_date}${q}`} target="_blank">{e.status === "draft" ? "Review" : e.video?.status === "draft" ? "Approve Short" : "Owner view"}</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {s.log && (
        <div className="bz-card flush">
          <div className="bz-bar"><b>Auto-review log</b><span className="bz-small">7:45 AM ET daily · last 30 runs</span></div>
          <div className="bz-table">
            <table className="bz-t">
              <thead><tr><th>Ran (ET)</th><th>Edition</th><th>Result</th><th>Why</th></tr></thead>
              <tbody>
                {s.log.length === 0 && <tr><td colSpan={4}><div className="bz-empty">No runs yet. The first is due the morning of the first live edition.</div></td></tr>}
                {s.log.map((l, k) => (
                  <tr key={k} className={l.result === "held" ? "bad" : ""}>
                    <td className="bz-num">{fmtWhen(l.ran_at)}</td>
                    <td className="bz-num">{fmtDay(l.edition_date)}</td>
                    <td><Pill v={l.result} /></td>
                    <td className="bz-small">{l.reasons.join(" · ") || "All checks passed"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </>
  );
}
