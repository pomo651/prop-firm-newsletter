import Link from "next/link";
import { getSnapshot, isAdmin, itemFlags, nyDate, fmtDay, fmtTime, type AdminItem } from "@/lib/admin";
import { Cat, EVIDENCE, Head, PartialNote, Pill } from "@/components/admin/ui";

export const dynamic = "force-dynamic";
export const metadata = { title: "Items & picks" };

const FILTERS = ["all", "new", "picked", "rejected"] as const;
type F = (typeof FILTERS)[number];

export default async function Items({ searchParams }: { searchParams: Promise<{ status?: string }> }) {
  if (!(await isAdmin())) return null;
  const { status } = await searchParams;
  const f: F = (FILTERS as readonly string[]).includes(status ?? "") ? (status as F) : "all";
  const s = await getSnapshot();

  if (!s.items) {
    return (
      <>
        <Head title="Items & picks" sub="Everything the watchers collected, and what FT-PM picked." />
        <PartialNote />
        <div className="bz-card flush">
          <div className="bz-bar"><b>Latest picks</b><span className="bz-sp" /><span className="bz-small">from ft_stats, newest 8</span></div>
          <table className="bz-t"><tbody>
            {s.stats.latest.map((x) => (
              <tr key={x.id}><td><div className="ft-title"><a href={x.url} target="_blank" rel="noreferrer">{x.title}</a><span>{x.source}</span></div></td><td><Cat c={x.category} /></td><td className="r bz-small">{fmtDay(x.picked_at.slice(0, 10))}</td></tr>
            ))}
          </tbody></table>
        </div>
      </>
    );
  }

  const n = (k: F) => (k === "all" ? s.items!.length : s.items!.filter((i) => i.status === k).length);
  const rows = s.items.filter((i) => f === "all" || i.status === f);
  const groups = new Map<string, AdminItem[]>();
  for (const i of rows) {
    const d = nyDate(new Date(i.collected_at));
    groups.set(d, [...(groups.get(d) ?? []), i]);
  }
  const flagged = s.items.filter((i) => itemFlags(i).length).length;

  return (
    <>
      <Head title="Items & picks" sub="Everything the watchers collected, and what FT-PM picked. Picks are public the moment they're marked." />
      {flagged > 0 && <div className="bz-alert o"><span>{flagged} pick{flagged === 1 ? "" : "s"} missing a category or evidence link (red edge below). Ask FT-PM to re-send them.</span></div>}
      <div className="bz-card flush">
        <div className="bz-bar">
          <div className="bz-filters">
            {FILTERS.map((k) => (
              <Link key={k} className={f === k ? "on" : ""} href={k === "all" ? "/admin/items" : `/admin/items?status=${k}`}>
                {k[0].toUpperCase() + k.slice(1)}<i>{n(k)}</i>
              </Link>
            ))}
          </div>
          <span className="bz-sp" />
          <span className="bz-small">Newest 500 · grouped by day collected (ET)</span>
        </div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Time</th><th>Item</th><th>Firm</th><th>Category</th><th>Evidence</th><th>By</th><th>Status</th></tr></thead>
            <tbody>
              {rows.length === 0 && <tr><td colSpan={7}><div className="bz-empty">No items here.</div></td></tr>}
              {[...groups].map(([day, list]) => [
                <tr className="grp" key={day}><td colSpan={7}>{fmtDay(day)}<span className="n">{list.length} item{list.length === 1 ? "" : "s"} · {list.filter((i) => i.status === "picked").length} picked</span></td></tr>,
                ...list.map((i) => {
                  const flags = itemFlags(i);
                  return (
                    <tr key={i.id} className={`${flags.length ? "bad" : ""} ${i.status === "rejected" ? "off" : ""}`}>
                      <td className="time bz-num"><b>{fmtTime(i.collected_at)}</b></td>
                      <td>
                        <div className="ft-title">
                          <a href={i.url} target="_blank" rel="noreferrer">{i.title}</a>
                          <span>{i.source_name}{i.source_published_at ? ` · posted ${fmtDay(i.source_published_at.slice(0, 10))}` : ""}{i.notes ? ` · ${i.notes}` : ""}</span>
                          {flags.length > 0 && <em>{flags.join(" · ")}</em>}
                        </div>
                      </td>
                      <td className="bz-small">{i.firm ?? "—"}</td>
                      <td><Cat c={i.category} /></td>
                      <td className="bz-small">{i.evidence ? (i.evidence_url ? <a href={i.evidence_url} target="_blank" rel="noreferrer">{EVIDENCE[i.evidence]}</a> : EVIDENCE[i.evidence]) : "—"}</td>
                      <td className="bz-small">{i.collected_by ?? "—"}</td>
                      <td><Pill v={i.status} /></td>
                    </tr>
                  );
                }),
              ])}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
