import { NextResponse } from "next/server";
import { ownerAction, type OwnerAction } from "@/lib/db";

const ACTIONS: OwnerAction[] = ["publish", "unpublish", "approve_video", "unapprove_video", "mark_uploaded"];

// Owner-only (pomo651): publish/unpublish an edition, approve a Short.
// Body: {date, action, video_url?}; header x-owner-key: <OWNER_KEY>.
export async function POST(req: Request) {
  const key = process.env.OWNER_KEY;
  if (!key || req.headers.get("x-owner-key") !== key) {
    return NextResponse.json({ error: "wrong owner key" }, { status: 401 });
  }
  const body = await req.json().catch(() => null);
  const date = body?.date;
  const action = body?.action;
  if (typeof date !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(date) || !ACTIONS.includes(action)) {
    return NextResponse.json({ error: "need date (YYYY-MM-DD) and a valid action" }, { status: 400 });
  }
  try {
    const edition = await ownerAction(date, action, typeof body.video_url === "string" ? body.video_url : undefined);
    return NextResponse.json({ ok: true, status: edition.status, video: edition.video });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
