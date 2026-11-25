import { NextResponse } from "next/server";
import { getStats } from "@/lib/db";

export const dynamic = "force-dynamic";

// Polled by the home page every 30s for live counters and latest picks.
export async function GET() {
  const stats = await getStats();
  return NextResponse.json(stats, { headers: { "cache-control": "no-store" } });
}
