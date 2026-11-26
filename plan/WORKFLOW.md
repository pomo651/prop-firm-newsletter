# Daily workflow

Agreed on Nov 25, 2026 in Funded Tape HQ (pomo651, FT-PM, Drew). The newsletter and the Short are daily, **7 days a week, including weekends and holidays**. Nothing is skipped, because big news can break on a holiday (decision by pomo651, Nov 25, 2026). **Thursday Nov 26, 2026 (US Thanksgiving) is the first live edition.** An evening edition (cutoff around 5 PM ET) remains an option to test later, using open and click data.

Item format and how bots write to the database: [`DATA_FORMAT.md`](DATA_FORMAT.md). Roles at a glance: [`TEAM.md`](TEAM.md). Bot API: [`site/BOT_API.md`](../site/BOT_API.md).

## Roles

| Who | Owns |
|---|---|
| **FT-PM** | The sources and the master source list in the database. Fact-checks items against the firm's own page and marks picks. |
| **FT-sources** | Official firm sites, help centers, and announcements. |
| **FT-community** | X, Reddit, YouTube, Discord, and reviews. |
| **FT-editor** | The edition draft, posted as status `draft`. |
| **FT-video** | The daily Short, built from the approved, published edition. |
| **Drew** | The repo, infra, and docs. |
| **pomo651** | Website development, and the only person who publishes or uploads. |

## Daily schedule (every day, 7 days a week)

Each edition covers the **24 hours up to the 6:00 AM ET cutoff**: the window is the previous 24 hours. The schedule is the same on weekends and holidays. Times below are Eastern (ET), with Edmonton time one hour earlier in brackets (America/Edmonton, MST / UTC-6 in winter; ET is UTC-5).

| Time ET (Edmonton) | Who | What |
|---|---|---|
| About **5:15 AM** (4:15) | FT-sources, FT-community | Sweep their sources and post every collected item as status `new` (`POST /api/bot/items`). Cutoff is **6:00 AM ET**; the window is the previous 24 hours. |
| **6:05 AM** (5:05) | FT-PM | Fact-check against the firm's own page and mark about **3 items** `picked`. |
| **6:50 AM** (5:50), due by **7:15 AM** (6:15) | FT-editor | Post the edition for today's New York date as status `draft` (`POST /api/bot/editions`). |
| **7:45 AM** (6:45) | Auto-review (local FT-team, for pomo651) | Publishes the draft if it passes every check in `site/BOT_API.md`; otherwise holds it and emails pomo651. Bots never publish. |
| **8:00 AM** (7:00) | FT-video | Build the daily Short from the published edition. For now pomo651 approves and uploads it by hand. |

Edmonton times are for winter; they follow the clock change in spring (ET is always 2 hours ahead of Edmonton in the 6:00 AM sense only when both are on the same rule, so check the local hour when daylight saving starts).

Still open for pomo651: does a weekly Beehiiv recap continue alongside the daily edition? (Week 1 is site-only, no daily Beehiiv send.)

The old weekly rhythm (collect Mon–Thu, draft Fri, approve Sat, send Sun) is retired. Historical windows are in `cutoffs.md` and `send-schedule.md`.

### Grok-side status (Nov 25, 2026)

- All five bots (FT-PM, FT-sources, FT-community, FT-editor, FT-video) have saved scheduled runs.
- FT-PM received the `BOT_TOKEN` on Nov 25, 2026 and posted a successful test item.
- FT-PM is switching the schedules to 7 days a week.
- Each bot holds the `BOT_TOKEN` privately. It never goes in the repo or in a group chat.

## What the database should expect each day

Written for the **local FT-team** (the website side, run with Claude Code). Once the Grok-side schedules are on 7 days, this is what lands in the `funded_tape` schema (migrations in `supabase/migrations/`) every day, including weekends and holidays. Bots write only through `POST /api/bot/*` (the endpoints call the `public.ft_*` functions); they never touch the tables directly.

All times are ET. The day's New York date is the `edition_date`.

| By (ET) | Who | Table and endpoint | What should be there |
|---|---|---|---|
| From about **5:15 AM** | FT-sources, FT-community | `funded_tape.items` via `POST /api/bot/items` | New rows with `status = 'new'` and `collected_by` set to the bot name (`FT-sources` or `FT-community`). Required fields `url`, `title`, `source_name`; usually also `source_url`, `firm`, `category`, `source_published_at`, `evidence`, `evidence_url`, `notes`. `collected_at` is the collection time. Items are collected up to the 6:00 AM ET cutoff, covering the previous 24 hours. |
| By **6:05 AM** | FT-PM | `funded_tape.items` via `POST /api/bot/items` | About **3** of those items moved to `status = 'picked'` (same `url` re-sent; `picked_at` is set by the database the first time). Items reviewed and dropped become `rejected`. A re-send replaces `title` and `status`; omitted optional fields keep their old values. |
| By **7:15 AM** (FT-editor starts at 6:50) | FT-editor | `funded_tape.editions` via `POST /api/bot/editions` | **Exactly one** row for that New York date (`edition_date` is unique, so a re-send updates it) with `status = 'draft'`, a `subject`, and `sections` as a JSON array of `{headline, body, why, sources}`. Every section has a headline, body, why-it-matters, and `sources` that include the exact `url` of at least one `picked` item, plus its source link. No placeholder text. |
| **7:45 AM** | Local FT-team (auto-review) | `funded_tape.editions`, `funded_tape.publish_log` | The draft becomes `published` (with `published_at`) if it passes the checks, or stays `draft` and is held. Either way one `publish_log` row is written (`result` is `published`, `held`, or `skipped`; `reasons` lists the problems). |
| After publish (8:00 AM start) | FT-video | `funded_tape.videos` via `POST /api/bot/videos` | At most one `draft` Short per `edition_date` (the edition must exist first). It is outside the 7:45 check. pomo651 approves it (`approved`) and uploads it (`uploaded`) by hand for now. FT-video posts here only after pomo651 OKs it and chooses where the video file lives. |

Bots **never set `published`**: `POST /api/bot/editions` saves every edition as `draft` whatever status is sent, and a published edition is locked (`400 … already published`) until pomo651 unpublishes it.

### How to tell a step is missing

Use the admin page, or query the tables. Example checks for a given New York date `D`:

| Missing step | How it shows up | What it means |
|---|---|---|
| FT-sources / FT-community did not run | No `funded_tape.items` rows with `collected_by` in (`FT-sources`, `FT-community`) and `collected_at` since about 5:15 AM ET on `D` (the admin snapshot's `last_item_at` per source is stale). | Collection is late or failed. |
| FT-PM did not pick | No `items` with `status = 'picked'` and `picked_at` on `D` (or fewer than about 3). | Fact-check is late. The 7:45 check will fail on "cites a picked item". |
| FT-editor did not post | No `editions` row with `edition_date = D` by 7:15 AM. | At **7:45 AM no draft means the edition is held**: `publish_log` gets a `held` row and pomo651 gets an email saying there is no draft. |
| The draft failed a check | `editions.status` is still `draft` and the latest `publish_log.reasons` for `D` lists why. | Held until the draft is fixed or pomo651 publishes by hand. |
| FT-video did not run | No `videos` row for `D` by about 8:45 AM. | The Short is late. It does not affect the edition. |
| The auto-review did not run | No `publish_log` row for `D` after 7:45 AM. | Local-side problem (cron or job), not a Grok-side one. |

Example query for a quick daily health read (replace `D`):

```sql
select
  (select count(*) from funded_tape.items
    where collected_by in ('FT-sources','FT-community') and collected_at >= (date 'D' + time '05:00') at time zone 'America/New_York') as items_collected,
  (select count(*) from funded_tape.items where status = 'picked' and picked_at >= (date 'D' + time '00:00') at time zone 'America/New_York') as picks,
  (select status from funded_tape.editions where edition_date = date 'D') as edition_status,
  (select result from funded_tape.publish_log where edition_date = date 'D' order by ran_at desc limit 1) as review_result;
```

### Ask for the local FT-team

Please make sure the **7:45 AM ET auto-publish job and its emails run all 7 days**, including Saturday, Sunday and holidays, and do not go silent on weekends. The pg_cron schedule in `supabase/migrations/20261126010000_funded_tape_auto_publish.sql` is already daily (`45 11,12 * * *`); please confirm that nothing on the site side (the job route, the result email, the admin pages) skips Saturday or Sunday.

## Rules for marking picks

- **FT-PM** is the only bot that marks an item `picked`.
- Fact-check first, against the **firm's own page**. Mark `picked` only after that check.
- Picks appear on the **public home page immediately**, so an unchecked item must never be marked `picked`.
- Aim for about **3 picks a day** (proposed).
- Items categorized as `allegation` may be picked only when the firm has given a case-specific response or there is a documented policy. Otherwise they go in notes and are not picked. Allegations are always labelled as allegations.
- Use `rejected` for items that were reviewed and dropped.

## Editorial rules

- **Official source first.** Prefer the firm's own page, help center, or official account announcement over a recap or a social post. Community chatter can surface a lead; it does not replace the official source. A staff or CEO reply on X is not an official statement.
- **No invented numbers.** If a figure is not in the source, leave it out.
- **Allegations may be picked only** when the firm has given a case-specific response or there is a documented policy. Otherwise they go in notes and are not picked. Allegations are always labelled as allegations.
- **View and like counts** are not facts or quality signals. Do not present them as evidence.
- **Payout totals** are the firm's own unaudited figures unless independently verified, and are never a pick on their own. Label them as unaudited unless independently verified.
- **Disclose conflicts of interest**, such as affiliate links or sponsorships.
- **Caveats go in `notes`**, such as "unaudited" or "not confirmed for forex".
- **Every item links its source.** The item `url` is required and must point at the collected page or post.

## Approval steps

1. **FT-editor** writes the edition (`editions/YYYY-MM-DD.md`, plus the Beehiiv/HTML package as needed) and posts it to the site as status `draft` (`POST /api/bot/editions`). Drafts are not public.
2. At 7:45 AM ET the **auto-review** (local FT-team, on pomo651's behalf) publishes the draft on the site if it passes every check in `site/BOT_API.md`; otherwise it holds the draft and emails pomo651. Sending on Beehiiv (if that day's send is in use) is still done by hand. Until then, the edition stays a draft and is not public and not sent.
3. **Bots never set an edition to `published`.**
4. After the edition is published, **FT-video** builds the daily Short from that approved, published edition. The Short is ready around 8:00–8:45 AM ET, once pomo651 has approved the edition.
5. **Nothing is uploaded** (YouTube or elsewhere) without pomo651's approval.
