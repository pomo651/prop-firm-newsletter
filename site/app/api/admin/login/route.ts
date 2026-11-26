import { NextResponse } from "next/server";
import { ADMIN_COOKIE, cookieValue, keyMatches } from "@/lib/admin";

// Admin sign-in: a plain form posts the key here. Same key as draft previews (PREVIEW_KEY).
export async function POST(req: Request) {
  const form = await req.formData().catch(() => null);
  const key = String(form?.get("key") ?? "");
  const to = new URL("/admin", req.url);
  if (!keyMatches(key)) {
    to.searchParams.set("e", "1");
    return NextResponse.redirect(to, 303);
  }
  const res = NextResponse.redirect(to, 303);
  res.cookies.set(ADMIN_COOKIE, cookieValue(), {
    httpOnly: true, secure: true, sameSite: "lax", path: "/", maxAge: 60 * 60 * 24 * 30,
  });
  return res;
}
