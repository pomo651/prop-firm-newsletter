# Funded Tape team

The GitHub repo [pomo651/prop-firm-newsletter](https://github.com/pomo651/prop-firm-newsletter) is the source of truth. Keep working copies in sync with `main`. Nothing is published or sent until pomo651 approves it.

## Bots and roles

Several bots were renamed. Old names still appear in earlier edition notes and some site examples.

| Bot | Formerly | Role |
|---|---|---|
| **FT-PM** | KFC | Runs the project. Plans the day, assigns work, fact-checks items, and marks picks. |
| **FT-sources** | Feed | Covers official firm sites and announcements: help centers, rule pages, firm posts, and trade press. |
| **FT-community** | Pulse | Covers community sources: Reddit, X, and other community discussion. |
| **FT-editor** | Editor | Writes each edition draft and posts it to the site as status `draft`. |
| **FT-video** | Reel | Makes the YouTube Shorts (Beta). |
| **Drew** | — | Owns the repo, Beehiiv, and plan upkeep. |

pomo651 is the owner. Only pomo651 approves an edition and publishes it (site or Beehiiv).

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
                                              pomo651 approves and publishes
                                                                   │
                                                                   ▼
                                              Drew keeps the repo, Beehiiv,
                                              and plan files in sync
                                                                   │
                                                                   ▼
                                              FT-video makes the Short (Beta)
```

1. **FT-sources** and **FT-community** collect during the day's window and post every item they find to the site as status `new` (`POST /api/bot/items`). They also keep a copy in the repo when it is part of the written record.
2. **FT-PM** reviews those items, fact-checks anything that might make the edition, and marks an item `picked` only after that fact-check. Picks appear on the public home page immediately, so an unchecked pick must not be marked.
3. **FT-editor** writes the edition (markdown plus the Beehiiv/HTML package as needed), commits it under `editions/`, and posts it to the site as status `draft` (`POST /api/bot/editions`). Bots never set an edition to `published`.
4. **pomo651** reviews the draft, approves it, and publishes it. Until that happens, the edition stays a draft and is not public and not sent.
5. **Drew** syncs approved files to this repo, handles Beehiiv, and keeps the plan and this team doc current.
6. **FT-video** turns a published edition into a Short once the Beta video work is in motion.

The bot API details (endpoints, fields, statuses) are in [`site/BOT_API.md`](../site/BOT_API.md). Never commit tokens or keys.

## Site rules

These are the rules from the live site (PR #2):

1. Watchers (**FT-sources**, **FT-community**) post every collected item with status `new`.
2. **FT-PM** marks an item `picked` only after it is fact-checked. Picks show on the public home page immediately.
3. **FT-editor** posts each edition as status `draft`. Bots never publish.
4. **pomo651** alone approves and publishes.

## Daily cadence (not decided yet)

The newsletter is daily (owner decision, Nov 25, 2026). The exact times are still being planned.

**FT-PM's proposal** (not yet approved by pomo651):

- **5:00 AM ET** — source sweep (FT-sources and FT-community)
- **6:00 AM ET** — FT-PM's picks due
- **6:30 AM ET** — FT-editor's draft due (posted as `draft`)
- **around 7:00 AM ET** — publish, after pomo651 approves

Do not treat these times as the schedule until pomo651 decides. The old weekly rhythm (collect Mon–Thu, draft Fri, approve Sat, send Sun) is retired. Historical windows are in `cutoffs.md` and `send-schedule.md`.
