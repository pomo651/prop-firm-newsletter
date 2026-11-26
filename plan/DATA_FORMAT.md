# Item and edition format

Stay on **Supabase** (Postgres). The website and the bots use the `funded_tape` schema from [`supabase/migrations/20261125000000_funded_tape_site.sql`](../supabase/migrations/20261125000000_funded_tape_site.sql): tables `sources`, `items`, and `editions`.

The website only reads. Bots **write only** through these endpoints, never straight into the database:

- `POST /api/bot/sources`
- `POST /api/bot/items`
- `POST /api/bot/editions`

Each call uses `Authorization: Bearer <BOT_TOKEN>`. The token is held by the owner and handed to FT-PM. **Never commit tokens or keys.** Full request shapes: [`site/BOT_API.md`](../site/BOT_API.md).

Writing through the API keeps the format in one place, so the database can change later without touching every bot.

## `items` — fields that exist today

These columns are in the database and accepted by `POST /api/bot/items` now.

| Field | Required | Notes |
|---|---|---|
| `url` | yes | Unique. The collected page or post. Re-sending the same `url` updates the row. |
| `title` | yes | Headline as collected. |
| `summary` | no | Short factual summary. No invented numbers. |
| `source_name` | yes | Display name of the source (for example `help.fundednext.com`). |
| `source_url` | no | Must already exist as a `sources` row (same `url`). |
| `firm` | no | Firm the item is about. |
| `collected_by` | no | Who posted it: `FT-sources`, `FT-community`, or `FT-PM`. |
| `collected_at` | no | When it was collected (ISO 8601). Defaults to now. |
| `status` | no | `new` (default, just collected), `picked` (fact-checked and selected), or `rejected`. |
| `picked_at` | — | Set by the API the first time `status` is `picked`. Do not invent it. |

Watchers always post items as `status: "new"`. Only FT-PM marks `picked`, and only after a fact-check against the firm's own page. Picks show on the public home page immediately.

## `items` — proposed columns (not in the database yet)

These were agreed in Funded Tape HQ on Nov 25, 2026. They **need a migration from pomo651**, and the bot API must be updated before bots can store them. Until then, treat them as a proposal: do not assume a POST will persist them.

| Field | Type / values | Purpose |
|---|---|---|
| `category` | one of `rule_change`, `launch`, `payout`, `pricing`, `promo`, `allegation` | How to sort the item. An `allegation` may be picked only when the firm has given a case-specific response or there is a documented policy; otherwise it is noted and not picked. Allegations are always labelled as allegations. |
| `source_published_at` | ISO 8601 timestamptz | When the firm (or source) posted it, not when we collected it. |
| `evidence` | one of `official`, `firm_x_post`, `community` | What kind of evidence backs the item. Prefer `official`. |
| `evidence_url` | URL | Link to that evidence (often the firm's own page). |
| `notes` | text | Caveats such as "unaudited" or "not confirmed for forex". |

## Example `POST /api/bot/items` payload

The payload below is **example data**, not a confirmed fact. The first block is valid today. The second block is proposed and will be stored only after the migration and API update.

```json
[
  {
    "url": "https://help.fundednext.com/en/articles/17718088-cfds-fnl-004",
    "title": "FundedNext sells a $50K CFD account with no challenge for $149.99",
    "summary": "FundedNext's help center lists a $50K CFD account with no challenge, priced at $149.99.",
    "source_name": "help.fundednext.com",
    "source_url": "https://help.fundednext.com/",
    "firm": "FundedNext",
    "collected_by": "FT-sources",
    "collected_at": "2026-11-25T10:15:00Z",
    "status": "new",

    "category": "pricing",
    "source_published_at": "2026-11-24T15:00:00Z",
    "evidence": "official",
    "evidence_url": "https://help.fundednext.com/en/articles/17718088-cfds-fnl-004",
    "notes": "Advertised price is for the CFD instant account; not confirmed for forex."
  }
]
```

## Other existing tables

**`sources`** (master list, owned by FT-PM): `name`, `kind` (`official`, `x`, `press`, `community`, `youtube`, `review`, `other`), `url` (unique), `active`. Posted with `POST /api/bot/sources`.

**`editions`**: `edition_date` (unique), `subject`, `preview`, `intro`, `outro`, `sections` (JSON array of `{headline, body, why, sources}`), `status` (`draft` or `published`), `published_at`. Posted with `POST /api/bot/editions`. Bots always send `status: "draft"`. Only pomo651 publishes.

## Proposed `videos` table (not in the database yet)

A small table linking each daily Short to its edition. Needs a migration from pomo651. No bot endpoint exists yet.

| Field | Purpose |
|---|---|
| `edition_date` | The edition this Short belongs to (same date as `editions.edition_date`). |
| `video_url` | Where the rendered (or uploaded) Short lives, once there is a URL. |
| `status` | Lifecycle of the Short (for example drafted vs approved). Exact values TBD with the migration. |
| `approved_at` | When pomo651 approved the upload. Nothing is uploaded without that approval. |
