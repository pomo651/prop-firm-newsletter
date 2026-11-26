# Funded Tape site — bot API

Live site: https://prop-firm-newsletter.vercel.app
Every write goes through four endpoints. All are `POST`, take JSON, and need the header:

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

- Required: `url`, `title`, `source_name`. Optional: `summary`, `category` (`rule_change` | `launch` | `payout` | `pricing` | `promo` | `allegation`), `source_published_at` (ISO time the firm/source posted it), `evidence` (`official` | `firm_x_post` | `community`), `evidence_url`, `notes`, `source_url` (must match a source already sent), `firm`, `collected_by` (FT-sources / FT-community / FT-PM), `collected_at` (ISO time, default now).
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

- Always saved as `draft`; any `status` you send is ignored. Drafts are **not public**. The owner reviews them at `/daily?preview=<PREVIEW_KEY>` and publishes with the Publish button.
- **Auto-review at 7:45 AM ET (from Nov 26, 2026).** The local FT-team publishes on pomo651's behalf, but only if every check below passes. Otherwise the draft is **held** and pomo651 is emailed the reasons.

1. A draft exists whose `edition_date` is that day's date in New York.
2. It has a subject and at least one section.
3. Every section has a `headline`, a `body`, a `why`, and at least one `sources` link.
4. Every section's `sources` include at least one item that FT-PM marked `picked` (send the exact same `url`).
5. A picked item with `category: "allegation"` needs `evidence` of `official` or `firm_x_post` (a firm response or a documented policy).
6. No placeholder text anywhere: `TBD`, `TODO`, `XXX`, `lorem ipsum`, `[name…]`.

  Post the draft by 7:15 AM ET. A draft that arrives later isn't published until pomo651 does it by hand.
- Once an edition is published it is **locked**. A bot update returns `400 … already published`. Ask pomo651 to unpublish it if a fix is needed.
- The page adds its own "Not financial advice" footer, so leave it out of `outro`.

## 4. Videos: the daily Short

`POST /api/bot/videos` with a JSON **object**:

```json
{ "edition_date": "2026-11-27", "video_url": "https://…/short.mp4", "title": "Today's prop firm news in 60s" }
```

- One Short per edition. The edition must already exist (post it first).
- Always saved as `draft`. pomo651 approves it with the **Approve Short for upload** button. After approval the Short shows on the edition page and is **locked** for bots. Upload only after approval.
- `video_url` can point at the rendered file before upload; pomo651 can replace it with the public URL when marking it uploaded.

## Responses

`200 {"ok":true,"result":…}` · `401` bad or missing token · `400` bad JSON or a DB error (message included).

## Working example

`site/scripts/seed-demo.mjs` loads the plan's source map and the demo edition through these three endpoints:

```
SITE_URL=https://prop-firm-newsletter.vercel.app BOT_TOKEN=… node site/scripts/seed-demo.mjs
```
