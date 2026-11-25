import type { Metadata } from "next";
import Link from "next/link";
import { getEditions, isPreview } from "@/lib/db";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Daily newsletter" };

const fmt = (d: string) =>
  new Date(`${d}T12:00:00Z`).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric" });

export default async function Daily({ searchParams }: { searchParams: Promise<{ preview?: string }> }) {
  const { preview } = await searchParams;
  const drafts = isPreview(preview);
  const editions = await getEditions(drafts);
  const q = drafts ? `?preview=${encodeURIComponent(preview!)}` : "";
  return (
    <>
      <div className="page-head">
        <div className="eyebrow">Daily newsletter</div>
        <h1>The prop firm news you can&apos;t miss</h1>
        <p>What changed, why it matters for your next account, and the source. Every fact is checked against the firm&apos;s own page.</p>
      </div>
      {drafts && <div className="draft-banner">Preview mode: drafts are shown. Only published editions are public.</div>}
      {editions.length === 0 && <div className="empty">The first edition is on its way.</div>}
      {editions.map((e) => (
        <Link key={e.edition_date} className="edition-card" href={`/daily/${e.edition_date}${q}`}>
          <span className="date">{fmt(e.edition_date)}</span>
          {e.status === "draft" && <span className="badge">Draft</span>}
          <h2>{e.subject}</h2>
          {e.preview && <p>{e.preview}</p>}
          <ol>{e.headlines.map((h) => <li key={h}>{h}</li>)}</ol>
        </Link>
      ))}
    </>
  );
}
