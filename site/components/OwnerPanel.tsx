"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import type { Edition, OwnerAction, Video } from "@/lib/types";

const STORE = "ft-owner-key";

function readKey() {
  try {
    return localStorage.getItem(STORE) ?? "";
  } catch {
    return "";
  }
}

// Shown on an edition page in preview mode. The owner key stays in this browser only.
export function OwnerPanel({ date, status, video, review }: { date: string; status: "draft" | "published"; video: Video | null; review?: Edition["review"] }) {
  const router = useRouter();
  const [key, setKey] = useState("");
  // load after mount so server and client HTML match
  // eslint-disable-next-line react-hooks/set-state-in-effect
  useEffect(() => setKey(readKey()), []);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  async function run(action: OwnerAction, extra?: Record<string, string>) {
    if (action === "publish" && !confirm(`Publish the ${date} edition? It goes public right away.`)) return;
    setBusy(true);
    setMsg("");
    try {
      const res = await fetch("/api/owner", {
        method: "POST",
        headers: { "content-type": "application/json", "x-owner-key": key },
        body: JSON.stringify({ date, action, ...extra }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error);
      try {
        localStorage.setItem(STORE, key);
      } catch {
        /* private mode: key just isn't remembered */
      }
      setMsg("Done.");
      router.refresh();
    } catch (e) {
      setMsg((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="owner">
      <div className="owner-head">Owner controls</div>
      {review && (
        <div className={`review review-${review.result}`}>
          Auto-review {new Date(review.ran_at).toLocaleString("en-US", { timeZone: "America/New_York", dateStyle: "medium", timeStyle: "short" })} ET:{" "}
          <b>{review.result}</b>
          {review.reasons.length > 0 && <ul>{review.reasons.map((r) => <li key={r}>{r}</li>)}</ul>}
        </div>
      )}
      <label>
        Owner key{" "}
        <input type="password" value={key} onChange={(e) => setKey(e.target.value)} autoComplete="off" />
      </label>
      <div className="owner-row">
        <span>Edition: <b>{status}</b></span>
        {status === "draft" ? (
          <button className="btn primary" disabled={busy || !key} onClick={() => run("publish")}>Publish edition</button>
        ) : (
          <button className="btn" disabled={busy || !key} onClick={() => run("unpublish")}>Unpublish</button>
        )}
      </div>
      <div className="owner-row">
        <span>Short: <b>{video ? video.status : "none yet"}</b></span>
        {video?.status === "draft" && (
          <button className="btn primary" disabled={busy || !key} onClick={() => run("approve_video")}>Approve Short for upload</button>
        )}
        {video?.status === "approved" && (
          <>
            <button
              className="btn primary"
              disabled={busy || !key}
              onClick={() => {
                const url = prompt("Public URL of the uploaded Short (optional):") ?? undefined;
                run("mark_uploaded", url ? { video_url: url } : undefined);
              }}
            >
              Mark uploaded
            </button>
            <button className="btn" disabled={busy || !key} onClick={() => run("unapprove_video")}>Withdraw approval</button>
          </>
        )}
      </div>
      {msg && <div className="owner-msg">{msg}</div>}
    </div>
  );
}
