import { CATEGORY_LABEL, type Category } from "@/lib/types";

// Small presentational pieces shared by the admin pages (bustem classes only).

type Tone = "g" | "o" | "r" | "b" | "";
const TONE: Record<string, Tone> = {
  // items
  new: "b", picked: "g", rejected: "",
  // editions / reviews / shorts
  published: "g", draft: "o", held: "r", skipped: "", approved: "g", uploaded: "g",
  // pipeline steps
  done: "g", wait: "", late: "o", fail: "r",
};
const WORD: Record<string, string> = { done: "Done", wait: "Not due", late: "Late", fail: "Missing" };

export function Pill({ v, label }: { v: string; label?: string }) {
  return <span className={`bz-pill ${TONE[v] ?? ""}`}>{label ?? WORD[v] ?? v[0].toUpperCase() + v.slice(1)}</span>;
}

export function Cat({ c }: { c: Category | null }) {
  if (!c) return <span className="bz-small">—</span>;
  return <span className={`bz-pill nodot ${c === "allegation" ? "r" : ""}`}>{CATEGORY_LABEL[c]}</span>;
}

export const EVIDENCE: Record<string, string> = { official: "Official", firm_x_post: "Firm X post", community: "Community" };

export function Head({ title, sub, children }: { title: string; sub: string; children?: React.ReactNode }) {
  return (
    <div className="bz-hd">
      <div>
        <h1>{title}</h1>
        <div className="bz-sub">{sub}</div>
      </div>
      {children && <div className="bz-btns">{children}</div>}
    </div>
  );
}

export function PartialNote() {
  return (
    <div className="bz-alert o">
      <span>Partial data: apply <b>20261127000000_funded_tape_admin.sql</b> to see every item and source.</span>
      <a href="/admin/workflows#data">How</a>
    </div>
  );
}

export function Bars({ rows }: { rows: { label: string; n: number }[] }) {
  const max = Math.max(1, ...rows.map((r) => r.n));
  return (
    <div className="ft-bars">
      {rows.map((r) => (
        <div className="ft-bar" key={r.label}>
          <span>{r.label}</span>
          <div><i style={{ width: `${(r.n / max) * 100}%` }} /></div>
          <b>{r.n}</b>
        </div>
      ))}
    </div>
  );
}
