# FT-grok side: what runs by itself, and what the DB should expect

Written by FT-PM (FT-grok), Nov 25, 2026. Applies from the first live edition, **Thursday Nov 26, 2026**.

## Status: on autopilot, every day

Every FT-grok step now runs on its own schedule, **7 days a week, weekends and holidays included** (pomo651, Nov 25, 2026). There is no dry run and no skipped day. On thin days (weekends, holidays) expect fewer picks and a shorter edition, never padding.

| ET (Edmonton) | Bot | What it writes to the DB | Endpoint, status |
|---|---|---|---|
| ~5:15–6:00 AM (4:15–5:00) | FT-sources | Official-source items for the 24h up to 6:00 AM ET, plus any new sources | `POST /api/bot/items` `new`, `POST /api/bot/sources` |
| ~5:15–6:00 AM (4:15–5:00) | FT-community | Community items (X, Reddit, YouTube, review sites) for the same window | `POST /api/bot/items` `new` |
| ~6:05–6:45 AM (5:05–5:45) | FT-PM | About 3 fact-checked picks (re-sends the same `url` with `picked`), and duds as `rejected` | `POST /api/bot/items` `picked` / `rejected` |
| by 7:15 AM (6:15) | FT-editor | Today's edition, `edition_date` = New York date; every section cites a picked `url` | `POST /api/bot/editions` (always `draft`) |
| 7:45 AM (6:45) | local FT-team | Auto-review: publish or hold (unchanged) | n/a |
| ~8:00–8:45 AM (7:00–7:45) | FT-video | Renders the daily Short | **Not posted yet.** `POST /api/bot/videos` starts only after pomo651 confirms posting and where `video_url` is hosted. |

So each morning the DB should see, in order: a batch of `new` items (typically a few to a couple dozen), then about 1 to 3 items flipped to `picked` by 6:45, then one `draft` edition by 7:15. If the 7:45 check finds no draft, it holds as designed and FT-PM investigates.

## How the bots coordinate

The bot API is write-only, so the bots also share what they post through files on the FT-grok machine (not in this repo): one folder per New York date with `items-FT-sources.json`, `items-FT-community.json`, `picks.json` + `picks-notes.md`, `edition.json`, `short.json`. Each file is exactly what was POSTed. The bot token is stored privately on that machine; it is never committed, printed, or posted in chat.

## Test content (live now)

To verify the write path, FT-PM posted one real, fact-checked pick on Nov 25, 2026 (~11:25 PM ET), which shows in Latest picks on the home page:

- `url`: https://help.topstep.com/en/articles/8284116-am-i-eligible-to-trade-with-topstep
- title: "Topstep stops selling new accounts in 13 countries; funded accounts keep getting paid"
- `firm` Topstep, `category` rule_change, `evidence` official, `collected_by` FT-PM, `notes` marks it as a site test pick.

It was fact-checked for weekly edition #3 and the source page was rechecked live. If the local team wants it off the home page, FT-PM can re-send it as `rejected`.

## Still manual (pomo651)

- Approving and uploading the Short (no YouTube connection yet).
- Beehiiv: off; week 1 is site-only. A weekly recap is still undecided.

## For the local team to check

- The site admin still says "first live Fri Nov 27" and "Skip weekends?" (`site/app/admin/workflows/page.tsx`, `site/app/admin/page.tsx`). This PR doesn't touch site code; please update those strings to "7 days a week, first live Thu Nov 26".
- Weekend/holiday auto-review: with 7-day runs, a weekend draft should be expected, not treated as unusual.
