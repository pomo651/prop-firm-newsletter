import "server-only";
import { NextResponse } from "next/server";
import { rpc } from "./db";

// Shared handler for /api/bot/*: bearer-token check, JSON body, one RPC call.
export async function botWrite(req: Request, fn: string, arg: string, shape: "array" | "object") {
  const token = process.env.BOT_TOKEN;
  if (!token || req.headers.get("authorization") !== `Bearer ${token}`) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "body must be JSON" }, { status: 400 });
  }
  if (shape === "array" ? !Array.isArray(body) : typeof body !== "object" || body === null || Array.isArray(body)) {
    return NextResponse.json({ error: `body must be a JSON ${shape}` }, { status: 400 });
  }
  try {
    const result = await rpc(fn, { [arg]: body });
    return NextResponse.json({ ok: true, result });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
