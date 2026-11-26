import Link from "next/link";
import { getSnapshot, isAdmin, ago, type AdminSource } from "@/lib/admin";
import { Head, PartialNote, Pill } from "@/components/admin/ui";

export const dynamic = "force-dynamic";
export const metadata = { title: "Sources" };

const KINDS: Record<string, string> = { official: "Official sites", x: "X accounts", press: "Press", community: "Community", youtube: "YouTube", review: "Reviews", other: "Other" };

export default async function Sources({ searchParams }: { searchParams: Promise<{ show?: string }> }) {
  if (!(await isAdmin())) return null;
  const { show } = await searchParams;
  const s = await getSnapshot();
  const kinds = Object.entries(s.stats.sourceKinds).sort((a, b) => b[1] - a[1]);

  if (!s.sources) {
    return (
      <>
        <Head title="Sources" sub="The master list FT-PM owns. Watchers only post items from these." />
        <PartialNote />
        <div className="bz-kpis">{kinds.slice(0, 4).map(([k, n]) => <div className="bz-kpi" key={k}><span>{KINDS[k] ?? k}</span><b className="bz-num">{n}</b></div>)}</div>
      </>
    );
  }

  const silentOnly = show === "silent";
  const list = s.sources.filter((x) => !silentOnly || (x.active && x.items_recent === 0));
  const silent = s.sources.filter((x) => x.active && x.items_recent === 0).length;
  const byKind = new Map<string, AdminSource[]>();
  for (const x of list) byKind.set(x.kind, [...(byKind.get(x.kind) ?? []), x]);

  return (
    <>
      <Head title="Sources" sub="The master list FT-PM owns. A source with no items for 14 days is silent: is it still worth watching?" />
      <div className="bz-card flush">
        <div className="bz-bar">
          <div className="bz-filters">
            <Link className={!silentOnly ? "on" : ""} href="/admin/sources">All<i>{s.sources.length}</i></Link>
            <Link className={silentOnly ? "on" : ""} href="/admin/sources?show=silent">Silent 14 days<i>{silent}</i></Link>
          </div>
          <span className="bz-sp" />
          <span className="bz-small">{kinds.map(([k, n]) => `${KINDS[k] ?? k} ${n}`).join(" · ")}</span>
        </div>
        <div className="bz-table">
          <table className="bz-t">
            <thead><tr><th>Source</th><th className="r">Items 14d</th><th className="r">All items</th><th className="r">Picks</th><th>Last item</th><th>Status</th></tr></thead>
            <tbody>
              {[...byKind].map(([kind, rows]) => [
                <tr className="grp" key={kind}><td colSpan={6}>{KINDS[kind] ?? kind}<span className="n">{rows.length}</span></td></tr>,
                ...rows.map((x) => (
                  <tr key={x.id} className={!x.active ? "off" : ""}>
                    <td><div className="ft-title"><b>{x.name}</b><a className="ft-url" href={x.url} target="_blank" rel="noreferrer">{x.url.replace(/^https?:\/\//, "")}</a></div></td>
                    <td className="r bz-num">{x.items_recent}</td>
                    <td className="r bz-num">{x.items_total}</td>
                    <td className="r bz-num">{x.picks_total}</td>
                    <td className="bz-small">{ago(x.last_item_at)}</td>
                    <td>{!x.active ? <Pill v="off" label="Off" /> : x.items_recent === 0 ? <Pill v="late" label="Silent" /> : <Pill v="done" label="Active" />}</td>
                  </tr>
                )),
              ])}
            </tbody>
          </table>
        </div>
      </div>
      <div className="bz-small">Items count only when the bot sends <span className="ft-code">source_url</span> matching a source here.</div>
    </>
  );
}
