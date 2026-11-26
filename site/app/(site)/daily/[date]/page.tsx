import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getEdition, isPreview } from "@/lib/db";
import { OwnerPanel } from "@/components/OwnerPanel";

export const dynamic = "force-dynamic";

type Props = { params: Promise<{ date: string }>; searchParams: Promise<{ preview?: string }> };

const valid = (d: string) => /^\d{4}-\d{2}-\d{2}$/.test(d);

export async function generateMetadata({ params, searchParams }: Props): Promise<Metadata> {
  const { date } = await params;
  const { preview } = await searchParams;
  const e = valid(date) ? await getEdition(date, isPreview(preview)) : null;
  return { title: e ? e.subject : "Newsletter", description: e?.preview ?? undefined };
}

export default async function EditionPage({ params, searchParams }: Props) {
  const { date } = await params;
  const { preview } = await searchParams;
  if (!valid(date)) notFound();
  const drafts = isPreview(preview);
  const e = await getEdition(date, drafts);
  if (!e) notFound();
  const day = new Date(`${date}T12:00:00Z`).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric" });
  return (
    <article className="article">
      <Link className="back" href={drafts ? `/daily?preview=${encodeURIComponent(preview!)}` : "/daily"}>← All editions</Link>
      {e.status === "draft" && <div className="draft-banner" style={{ marginTop: 14 }}>Draft, not approved or sent. Visible only with the preview key.</div>}
      {drafts && <OwnerPanel date={date} status={e.status} video={e.video} review={e.review} />}
      <div className="eyebrow" style={{ marginTop: 18 }}>{day}</div>
      <h1>{e.subject}</h1>
      {e.intro && <p className="lede">{e.intro}</p>}
      {e.video?.video_url && (
        <p className="video-link">
          ▶ <a href={e.video.video_url} target="_blank" rel="noreferrer">{e.video.title ?? "Watch today's Short"}</a>
          {e.video.status === "draft" && <span className="badge">Short not approved</span>}
        </p>
      )}
      {e.sections.map((s, i) => (
        <section key={i}>
          <h2><small>{String(i + 1).padStart(2, "0")}</small>{s.headline}</h2>
          <p>{s.body}</p>
          {s.why && <p className="why"><b>Why it matters: </b>{s.why}</p>}
          {s.sources && s.sources.length > 0 && (
            <ul className="sources">
              {s.sources.map((u) => <li key={u}><a href={u} target="_blank" rel="noreferrer">{u}</a></li>)}
            </ul>
          )}
        </section>
      ))}
      {e.outro && <p style={{ whiteSpace: "pre-line" }}>{e.outro}</p>}
      <p className="disclaimer">Not financial advice. Prop firm accounts are mostly simulated, and most traders do not receive a payout.</p>
    </article>
  );
}
