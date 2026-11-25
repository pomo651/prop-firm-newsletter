import Link from "next/link";
import { getStats } from "@/lib/db";
import { LiveHome } from "@/components/LiveHome";

export const dynamic = "force-dynamic";

export default async function Home() {
  const stats = await getStats();
  return (
    <>
      <div className="eyebrow">About Funded Tape</div>
      <div className="hero">
        <div>
          <h1>
            Prop firms change something every day.
            <span>Only a few changes matter.</span>
          </h1>
          <p>
            Funded Tape watches <b>{stats.sources.toLocaleString("en-US")}</b> sources for you: it collects, groups,
            scores and picks, then writes the few that matter into a daily newsletter. Independent and free.
          </p>
        </div>
        <div className="cta">
          <Link className="btn primary" href="/daily">Read the latest newsletter →</Link>
        </div>
      </div>
      <LiveHome initial={stats} />
    </>
  );
}
