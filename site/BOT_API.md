# Funded Tape site — bot API

Live site: https://prop-firm-newsletter.vercel.app
Every write goes through three endpoints. All are `POST`, take JSON, and need the header:

```
Authorization: Bearer <BOT_TOKEN>
```

The owner (pomo651) holds `BOT_TOKEN` and hands it to FT-PM. Never commit it.
Re-sending the same `url` / `edition_date` updates the row, so every call is safe to retry.

## 1. Sources: what the watchers look at

`POST /api/bot/sources` with a JSON **array**:

```json
[{ "name": "Topstep", "kind": "x", "url": "https://x.com/Topstep" }]
```

`kind` is one of `official`, `x`, `press`, `community`, `youtube`, `review`, `other`.
Send `"active": false` to stop counting a source. Home page counter = active sources.

## 2. Items: everything a watcher collects, and the picks

`POST /api/bot/items` with a JSON **array**:

```json
[{
  "url": "https://help.fundednext.com/en/articles/17718088-cfds-fnl-004",
  "title": "FundedNext sells a $50K CFD account with no challenge for $149.99",
  "source_name": "help.fundednext.com",
  "source_url": "https://help.fundednext.com/",
  "firm": "FundedNext",
  "collected_by": "FT-sources",
  "status": "new"
}]
```

- Required: `url`, `title`, `source_name`. Optional: `summary`, `source_url` (must match a source already sent), `firm`, `collected_by` (FT-sources / FT-community / FT-PM), `collected_at` (ISO time, default now).
- `status`: `new` when collected, `picked` when FT-PM picks it (after fact-checking), `rejected` when dropped.
- **Picks show on the public home page right away** (Latest picks + the live animation). Only mark `picked` once the item is fact-checked.

## 3. Editions: the daily newsletter

`POST /api/bot/editions` with a JSON **object**:

```json
{
  "edition_date": "2026-11-26",
  "subject": "…",
  "preview": "…",
  "intro": "…",
  "sections": [
    { "headline": "…", "body": "…", "why": "…", "sources": ["https://…"] }
  ],
  "outro": "…",
  "status": "draft"
}
```

- `status` defaults to `draft`. Drafts are **not public**. The owner reviews them at `/daily?preview=<PREVIEW_KEY>`.
- Only the owner flips an edition to `"published"`. Bots always send `draft`.
- The page adds its own "Not financial advice" footer, so leave it out of `outro`.

## Responses

`200 {"ok":true,"result":…}` · `401` bad or missing token · `400` bad JSON or a DB error (message included).

## Working example

`site/scripts/seed-demo.mjs` loads the plan's source map and the demo edition through these three endpoints:

```
SITE_URL=https://prop-firm-newsletter.vercel.app BOT_TOKEN=… node site/scripts/seed-demo.mjs
```
