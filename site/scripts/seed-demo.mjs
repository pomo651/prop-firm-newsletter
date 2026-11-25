// Seeds the site from files already in this repo, through the same bot API the
// Grok bots use (so it doubles as a working client example):
//   1. sources  <- the "Source map" section of plan/prop-firm-ceo-plan-v1.html
//   2. items    <- every source URL cited in editions/2026-10-26_11-01-demo.txt
//                  (first URL of each story = picked, the rest = collected)
//   3. edition  <- the demo edition, as status "draft" (never approved, so not public)
//
// Usage: SITE_URL=https://<site> BOT_TOKEN=... node scripts/seed-demo.mjs
// Safe to re-run: everything upserts by url / edition_date.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const SITE = process.env.SITE_URL ?? "http://localhost:3000";
const TOKEN = process.env.BOT_TOKEN;
if (!TOKEN) throw new Error("BOT_TOKEN is required");

async function post(route, body) {
  const res = await fetch(`${SITE}/api/bot/${route}`, {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${TOKEN}` },
    body: JSON.stringify(body),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(`${route}: ${res.status} ${JSON.stringify(json)}`);
  console.log(route, json);
}

const host = (u) => new URL(u).hostname.replace(/^www\./, "");
const PRESS = ["financemagnates.com", "fundedtruth.com", "propweekly.com", "thegodfunded.com", "proptraderz.com",
  "fundedyield.com", "proveyouredge.com", "propfirmloop.com", "propdatalab.com", "proptradecenter.com", "marketframework.com"];
const REVIEW = ["propfirmmatch.com", "bestprops.com", "trustpilot.com", "proptraders.io", "proptraders.club", "videos.feedspot.com"];

function kindOf(u) {
  const h = host(u);
  if (h === "x.com") return "x";
  if (h.endsWith("youtube.com")) return "youtube";
  if (h.endsWith("reddit.com") || h === "t.me" || h.includes("discord")) return "community";
  if (PRESS.includes(h)) return "press";
  if (REVIEW.includes(h)) return "review";
  return "official";
}

function nameOf(u, text) {
  const t = text.replace(/<[^>]+>/g, "").trim();
  if (t && !t.startsWith("http")) return t;
  const h = host(u);
  const p = new URL(u).pathname.split("/").filter(Boolean);
  if (h === "x.com") return `@${p[0]}`;
  if (h.endsWith("reddit.com") && p[0] === "r") return `r/${p[1]}`;
  if (h.endsWith("youtube.com") && p[0]) return p[0];
  if (h === "t.me") return `Telegram ${p[0]}`;
  return h;
}

// 1. sources
const plan = readFileSync(path.join(ROOT, "plan/prop-firm-ceo-plan-v1.html"), "utf8");
const map = plan.slice(plan.indexOf('id="sources"'), plan.indexOf('id="team"'));
const sources = new Map();
for (const [, url, text] of map.matchAll(/<a href="(https?:\/\/[^"]+)"[^>]*>([\s\S]*?)<\/a>/g)) {
  if (!sources.has(url)) sources.set(url, { name: nameOf(url, text), kind: kindOf(url), url });
}

// 2 + 3. demo edition
const txt = readFileSync(path.join(ROOT, "editions/2026-10-26_11-01-demo.txt"), "utf8");
const parts = txt.split(/\n-{20,}\n/);
const head = parts[0];
const subject = head.match(/^SUBJECT: (.+)$/m)[1].trim();
const preview = head.match(/^PREVIEW TEXT: (.+)$/m)[1].trim();
const intro = head.split(/^PREVIEW TEXT: .+$/m)[1].trim().split(/\n\n/).slice(1).join("\n\n").trim();
// the site prints its own disclaimer footer, so drop the edition's copy
const outro = parts.at(-1).replace(/\n*Not financial advice\.[\s\S]*$/, "").trim();
const EDITION_DATE = "2026-11-01"; // demo covers Oct 26 - Nov 1
const PICKED_AT = "2026-11-01T12:00:00-07:00";

const sections = [];
const items = [];
for (const block of parts.slice(1, -1)) {
  const lines = block.trim().split("\n");
  const headline = lines[0].replace(/^\d+\)\s*/, "").trim();
  const rest = lines.slice(1).join("\n").trim();
  const urls = [...rest.matchAll(/https?:\/\/\S+/g)].map((m) => m[0]);
  const text = rest.replace(/\nSources?:[\s\S]*$/, "").trim();
  const [body, whyBlock = ""] = text.split(/\n\nWhy it matters:\s*/);
  const [why, ...notes] = whyBlock.split(/\n\n/);
  sections.push({ headline, body: [body, ...notes].join("\n\n").trim(), why: why.trim(), sources: urls });
  urls.forEach((url, i) => {
    if (!sources.has(url) && host(url) === "x.com") {
      // an X post: credit the account
      const acct = `https://x.com/${new URL(url).pathname.split("/")[1]}`;
      if (!sources.has(acct)) sources.set(acct, { name: `@${new URL(url).pathname.split("/")[1]}`, kind: "x", url: acct });
    }
    items.push({
      url,
      title: headline,
      source_name: host(url) === "x.com" ? `@${new URL(url).pathname.split("/")[1]} on X` : host(url),
      collected_by: kindOf(url) === "x" ? "Pulse" : "Feed",
      collected_at: PICKED_AT,
      status: i === 0 ? "picked" : "new",
      picked_at: i === 0 ? PICKED_AT : undefined,
    });
  });
}

await post("sources", [...sources.values()]);
await post("items", items);
await post("editions", { edition_date: EDITION_DATE, subject, preview, intro, outro, sections, status: "draft" });
