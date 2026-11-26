# Daily workflow

Agreed on Nov 25, 2026 in Funded Tape HQ (pomo651, FT-PM, Drew). The newsletter and the Short are now daily. The timetable below is **proposed** until pomo651 confirms it.

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

## Daily schedule (proposed)

Each edition covers the **24 hours up to 5 AM ET**. Times below are Eastern. In winter, 7 AM ET is 6 AM Edmonton (America/Edmonton, MST / UTC-6).

| Time (ET) | Edmonton (winter) | Who | What |
|---|---|---|---|
| All day, final sweep by **5:00 AM** | 4:00 AM | FT-sources, FT-community | Post every collected item as status `new`. Final sweep by 5 AM ET. |
| By **6:00 AM** | 5:00 AM | FT-PM | Fact-check against the firm's own page and mark picks. About **3 picks** on a weekday (FT-PM's proposal). |
| By **6:30 AM** | 5:30 AM | FT-editor | Post the edition as status `draft`. |
| Around **7:00 AM** | 6:00 AM | pomo651 | Approve and publish. Bots never publish. |
| **7:15–8:00 AM** | 6:15–7:00 AM | FT-video | Build the daily Short from the published edition. Ready in this window once pomo651 has approved the edition. Nothing is uploaded without pomo651's approval. |

Open questions for pomo651 (still unsettled):

1. Do we skip weekends?
2. Does a weekly Beehiiv recap continue alongside the daily edition?

Do not treat the times above as final until pomo651 confirms them. The old weekly rhythm (collect Mon–Thu, draft Fri, approve Sat, send Sun) is retired. Historical windows are in `cutoffs.md` and `send-schedule.md`.

## Rules for marking picks

- **FT-PM** is the only bot that marks an item `picked`.
- Fact-check first, against the **firm's own page**. Mark `picked` only after that check.
- Picks appear on the **public home page immediately**, so an unchecked item must never be marked `picked`.
- Aim for about **3 picks per weekday** (proposed).
- Items categorized as `allegation` are never picked. They may be noted, not featured.
- Use `rejected` for items that were reviewed and dropped.

## Editorial rules

- **Official source first.** Prefer the firm's own page, help center, or announcement over a recap or a social post. Community chatter can surface a lead; it does not replace the official source.
- **No invented numbers.** If a figure is not in the source, leave it out.
- **Allegations are never picked**, only noted (for example in `notes`, or as context that did not make the edition).
- **Caveats go in `notes`**, such as "unaudited" or "not confirmed for forex".
- **Every item links its source.** The item `url` is required and must point at the collected page or post.

## Approval steps

1. **FT-editor** writes the edition (`editions/YYYY-MM-DD.md`, plus the Beehiiv/HTML package as needed) and posts it to the site as status `draft` (`POST /api/bot/editions`). Drafts are not public.
2. **pomo651** reviews the draft, approves it, and publishes it on the site (and sends on Beehiiv, if that day's send is in use). Until then, the edition stays a draft and is not public and not sent.
3. **Bots never set an edition to `published`.**
4. After the edition is published, **FT-video** builds the daily Short from that approved, published edition. The Short is ready around 7:15–8:00 AM ET, once pomo651 has approved the edition.
5. **Nothing is uploaded** (YouTube or elsewhere) without pomo651's approval.
