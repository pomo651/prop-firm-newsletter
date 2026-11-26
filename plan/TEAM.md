# Funded Tape team

The GitHub repo [pomo651/prop-firm-newsletter](https://github.com/pomo651/prop-firm-newsletter) is the source of truth. Keep working copies in sync with `main`. Nothing is published, sent, or uploaded until pomo651 approves it. Since Nov 26, 2026, pomo651 has delegated the daily edition's approval to the local FT-team's 7:45 AM ET auto-review (checks in `site/BOT_API.md`).

Daily timetable, editorial rules, and approval steps: [`WORKFLOW.md`](WORKFLOW.md). Item format: [`DATA_FORMAT.md`](DATA_FORMAT.md).

## Bots and roles

Several bots were renamed. Old names still appear in earlier edition notes and some site examples.

| Bot | Formerly | Role |
|---|---|---|
| **FT-PM** | KFC | Runs the project. Owns the sources and the master source list in the database, fact-checks items against the firm's own page, and marks picks. |
| **FT-sources** | Feed | Covers official firm sites, help centers, and announcements. |
| **FT-community** | Pulse | Covers X, Reddit, YouTube, Discord, and reviews. |
| **FT-editor** | Editor | Writes each edition draft and posts it to the site as status `draft`. |
| **FT-video** | Reel | Builds the daily Short from each approved, published edition. Nothing is uploaded without pomo651's approval. |
| **Drew** | — | Owns the repo, infra, and docs. |

pomo651 owns website development and is the only person who approves an edition and publishes it (site or Beehiiv), or approves a Short for upload.

## How work is handed off

```
FT-sources ─┐
            ├─► items (status: new) ─► FT-PM fact-checks ─► marks picked
FT-community┘                                                      │
                                                                   ▼
                                              FT-editor writes the draft
                                                   and posts status: draft
                                                                   │
                                                                   ▼
                                         auto-review publishes (or holds for pomo651)
                                                                   │
                                                                   ▼
                                              FT-video builds the daily Short
                                              (upload only after pomo651 approves)
```

1. **FT-sources** and **FT-community** sweep at about 5:15 AM ET every day and post every item they find to the site as status `new` (`POST /api/bot/items`). The cutoff is 6:00 AM ET and the window is the previous 24 hours. They also keep a copy in the repo when it is part of the written record.
2. **FT-PM** fact-checks against the firm's own page and marks an item `picked` only after that check. Picks appear on the public home page immediately, so an unchecked pick must not be marked.
3. **FT-editor** writes the edition (markdown plus the Beehiiv/HTML package as needed), commits it under `editions/`, and posts it to the site as status `draft` (`POST /api/bot/editions`). Bots never set an edition to `published`.
4. **pomo651** reviews the draft, approves it, and publishes it. Until that happens, the edition stays a draft and is not public and not sent.
5. **FT-video** builds the daily Short at 8:00 AM ET from the published edition. Nothing is uploaded without pomo651's approval.
6. **Drew** keeps the repo, infra, and docs in sync.

The bot API details (endpoints, fields, statuses) are in [`site/BOT_API.md`](../site/BOT_API.md). Never commit tokens or keys.

## Site rules

These are the rules from the live site (PR #2):

1. Watchers (**FT-sources**, **FT-community**) post every collected item with status `new`.
2. **FT-PM** marks an item `picked` only after it is fact-checked. Picks show on the public home page immediately.
3. **FT-editor** posts each edition as status `draft`. Bots never publish.
4. Only **pomo651** approves and publishes. For the daily edition, the 7:45 AM ET auto-review does it on pomo651's behalf when every check passes.

## Daily schedule

The newsletter and the Short are daily, **7 days a week, including weekends and holidays** (owner decision, Nov 25, 2026). Nothing is skipped, because big news can break on a holiday. Thursday Nov 26, 2026 is the first live edition. Each edition covers the previous 24 hours up to the 6:00 AM ET cutoff.

All times ET, with Edmonton time one hour earlier in brackets:

- **5:15 AM (4:15)**: FT-sources and FT-community sweep and post items as `new`.
- **6:05 AM (5:05), done by 6:45 (5:45)**: FT-PM fact-checks and marks about 3 items `picked`.
- **6:50 AM (5:50)**: FT-editor posts the edition draft, due by 7:15 (6:15).
- **7:45 AM (6:45)**: the local side's auto-review publishes or holds.
- **8:00 AM (7:00)**: FT-video builds the Short. pomo651 approves and uploads it by hand for now.

Each bot holds the `BOT_TOKEN` privately. It never goes in the repo or a group chat. What the database should see each day, and how to tell a step is missing: [`WORKFLOW.md`](WORKFLOW.md#what-the-database-should-expect-each-day).

Open question for pomo651: whether a weekly Beehiiv recap continues alongside the daily edition (week 1 is site-only).

The old weekly rhythm (collect Mon–Thu, draft Fri, approve Sat, send Sun) is retired. Historical windows are in `cutoffs.md` and `send-schedule.md`.

Full write-up: [`WORKFLOW.md`](WORKFLOW.md).
