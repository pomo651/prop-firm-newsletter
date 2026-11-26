# Funded Tape

Funded Tape is a daily newsletter for prop firm traders. Each issue is the things you can't miss in the prop firm world that day: what changed, why it matters, and the source.

## Roadmap

- **Alpha:** a free daily issue of "the things you can't miss in the prop firm world today," published at https://prop-firm-newsletter.vercel.app/daily. Sent on [Beehiiv](https://www.beehiiv.com/)'s free plan.
- **Beta:** the same daily issue, plus one YouTube video and Shorts.

## Daily workflow

The newsletter and the Short are daily, **7 days a week, including weekends and holidays**. Each edition covers the previous 24 hours up to the 6:00 AM ET cutoff. Full write-up: [`plan/WORKFLOW.md`](plan/WORKFLOW.md). Item format: [`plan/DATA_FORMAT.md`](plan/DATA_FORMAT.md).

```mermaid
flowchart TD
  A[FT-sources and FT-community sweep at about 5:15 AM ET and post items as new] --> B[Cutoff 6:00 AM ET]
  B --> C[FT-PM fact-checks and marks about 3 picks, 6:05 start, done by 6:45 AM ET]
  C --> D[FT-editor posts the edition as draft at 6:50, due by 7:15 AM ET]
  D --> E[Auto-review at 7:45 AM ET publishes it, or holds it for pomo651]
  E --> F[FT-video builds the daily Short at 8:00 AM ET]
```

All times ET, with Edmonton time one hour earlier in brackets:

1. About **5:15 AM** (4:15): FT-sources and FT-community sweep and post every item as `new`. The cutoff is 6:00 AM ET and the window is the previous 24 hours.
2. From **6:05 AM** (5:05), done by **6:45 AM** (5:45): FT-PM fact-checks against the firm's own page and marks about 3 items `picked`. Picks show on the public home page immediately, so only mark one after the check.
3. **6:50 AM** (5:50), due by **7:15 AM** (6:15): FT-editor posts the edition as status `draft`.
4. **7:45 AM** (6:45): the local FT-team's **auto-review** publishes the draft on pomo651's behalf if it passes every check (list in `site/BOT_API.md`). Otherwise it holds the draft and emails pomo651. Bots never publish.
5. **8:00 AM** (7:00): FT-video builds the daily Short from the published edition. For now pomo651 approves and uploads it by hand.

This runs every day, including weekends and holidays, because big news can break on a holiday (pomo651, Nov 25, 2026). Thursday Nov 26, 2026 is the first live edition. An evening edition (cutoff around 5 PM ET) remains an option to test later, using open and click data. Still open: whether a weekly Beehiiv recap continues (week 1 is site-only).

What the database should see each day, and how the local team can tell a step is missing: [`plan/WORKFLOW.md`](plan/WORKFLOW.md#what-the-database-should-expect-each-day). Each bot holds the `BOT_TOKEN` privately; it never goes in the repo or a group chat.

## Bot team

Roles, handoffs, and site rules are in [`plan/TEAM.md`](plan/TEAM.md). In short:

- **FT-PM** (formerly KFC) runs the project, owns the source list, fact-checks items, and marks picks.
- **FT-sources** (formerly Feed) covers official firm sites, help centers, and announcements.
- **FT-community** (formerly Pulse) covers X, Reddit, YouTube, Discord, and reviews.
- **FT-editor** (formerly Editor) writes the daily draft and posts it as status `draft`.
- **FT-video** (formerly Reel) builds the daily Short from the published edition.
- **Drew** owns the repo, infra, and docs.
- **pomo651** owns website development and is the only one who publishes or uploads.

The GitHub repo is the source of truth. Nothing sends or uploads until it is approved: by pomo651, or for the daily edition by the auto-review pomo651 delegated to the local FT-team.

## Pull requests: FT-grok and the local FT-team

Two teams work in this repo: **FT-grok** (the Grok bots above) and the **local FT-team** (pomo651 + Claude Code, on pomo651's machine).

- **Who owns what.** FT-grok owns the data, media and resources: collecting, fact-checking, picks, edition text, Shorts, Beehiiv. It writes to the DB only through `POST /api/bot/*`. The local FT-team owns the website (`site/`, `supabase/migrations/`, the bot API, deploys), which reads the DB and renders it. Need a new field or table? Ask in a PR or issue; the local FT-team adds the migration and API support.
- **FT-grok PRs** start the PR body with: *"Done by FT-grok — needs local FT-team review."* FT-grok never merges its own PRs. The local FT-team reviews, merges, and syncs.
- **Local FT-team PRs** start with: *"Done by local FT-team (pomo651 + Claude Code)."* FT-grok should read these before its next run.
- Every change is explained in this README (and in `plan/TEAM.md` if roles or handoffs change).

## Layout

- `plan/` — static CEO plan and team docs. Version 1 (Nov 1, 2026) is `plan/prop-firm-ceo-plan-v1.html`. Rebuild it with `python3 scripts/build_html.py`. Daily workflow: [`plan/WORKFLOW.md`](plan/WORKFLOW.md). Item format: [`plan/DATA_FORMAT.md`](plan/DATA_FORMAT.md). Roles and handoffs: [`plan/TEAM.md`](plan/TEAM.md).
- `editions/` — newsletter issues. `editions/2026-10-26_11-01-demo.txt` is a practice draft that was never sent. FINAL drafts of weekly editions #1–#3 are here too (no confirmed send on record; see [`cutoffs.md`](cutoffs.md)); see **Archive / newsletter files**.
- `research/` — background notes. `research/platform-pricing-2026-11-03.txt` is the platform check that chose Beehiiv's free plan.
- `scripts/` — helpers. `scripts/build_html.py` generates the plan HTML. Edition and screenshot builders live here too.
- `site/` — the Funded Tape website (Next.js on Vercel). See **Website** and **Admin** below.
- `supabase/migrations/` — database schema for the website.
- `designs/`, `video/`, `proposals/`, `reports/` — template explorations, the Shorts pipeline, strategy proposals, and status reports. See **Archive / newsletter files**.
- `funded-tape-template.html`, `cutoffs.md`, `send-schedule.md` — the Design B email template and the old weekly window/send schedule.

Future editions use `editions/YYYY-MM-DD.md`, named for the day the issue covers (the demo file keeps its old weekly name).

## Website (added Nov 25, 2026)

Live: **https://prop-firm-newsletter.vercel.app** (Vercel project `prop-firm-newsletter`, root directory `site/`).

| Page | What it shows |
|---|---|
| `/` Home | How Funded Tape works: a live animation (many sources → a few picks → the newsletter), live counters (sources, items, picks, editions) and the latest picks. It refreshes every 30 seconds. |
| `/daily` Daily newsletter | Published editions, newest first. One page per edition at `/daily/YYYY-MM-DD`. |

The left sidebar has only these two pages for now. The admin (below) is separate and not linked from the public site.

## Admin (added Nov 26, 2026)

**https://prop-firm-newsletter.vercel.app/admin** is for pomo651 and the local FT-team. Sign in with the `PREVIEW_KEY` (the same key that opens drafts). The admin only reads. Publishing and approving Shorts still happen on the draft page with the `OWNER_KEY`, as before.

| Page | What to watch |
|---|---|
| **Today** | Today's pipeline against the timetable (sweep 6:00, picks 6:45, draft 7:15, auto-review 7:45, Short 8:00–8:45 ET, with Edmonton times), each step Done / Not due / Late / Missing. KPIs: items in 24h, picks vs ~3, published in the last 14 days, active and silent sources. "Needs you" (held drafts, Shorts to approve, risky picks), a 14-day edition strip, picks by category and evidence, items by collector, and the audience metrics not connected yet (Beehiiv, YouTube, page views). |
| **Items & picks** | Every item, grouped by day, filtered by status. A red edge marks a pick with no category, no evidence link, or an allegation without official evidence. |
| **Editions & Shorts** | Every edition with its status, latest auto-review result and Short status, plus the auto-review log. Buttons open the owner view. |
| **Sources** | The master list by kind, with item counts. A source with no items for 14 days is marked silent. |
| **Workflows** | The whole operating manual on one page: daily run, morning checklist, who owns what, pick and editorial rules, the 6 auto-review checks, what to do when something breaks, PR rules, and how data changes. Keep it in step with `plan/WORKFLOW.md` and `plan/TEAM.md`. |

**Theme.** The admin uses the FDE "bustem" theme, the same look as the VHealth and Kids Map admins. Rules, files, status colours and how to add a page: [`site/app/admin/THEME.md`](site/app/admin/THEME.md).

**Database.** The admin reads one new function, `public.ft_admin_snapshot` (migration `supabase/migrations/20261127000000_funded_tape_admin.sql`). It only reads and is granted to `service_role` only. **Until it is applied, the admin runs in partial mode**: Today and Editions work from the existing functions, but the item list and source list are missing. Apply it from `~/@Pomo651/blackout-clock` with `supabase db query --linked -f <file>`.

**Code.** Public pages moved into the route group `site/app/(site)/` (URLs unchanged). Admin pages are in `site/app/admin/`, data and time helpers in `site/lib/admin.ts`, sign-in at `site/app/api/admin/login` (httpOnly cookie, 30 days).

**How bots feed it.** The site reads from a database. Bots write to it through `POST /api/bot/sources`, `/api/bot/items` and `/api/bot/editions` with a bearer token. Full guide: [`site/BOT_API.md`](site/BOT_API.md).

**Rules that change for the bot team**

1. Anything marked `picked` appears on the public home page right away. Pick only fact-checked items.
2. Editions are posted as `draft`. Only the owner publishes one, so "nothing goes out until the owner approves" still holds on the site.
3. The newsletter is **daily** (owner confirmed Nov 25, 2026). The `editions/*.txt|md` files remain the working drafts. Post the final version to `/api/bot/editions` too.

**Database.** Supabase project `blackout-clock` (ref `fqgryxjuecjgelcjdvmq`), schema `funded_tape` (tables `sources`, `items`, `editions`). The site never touches blackout-clock's own tables. It reaches the data only through `public.ft_*` functions, which only the server key can call. Schema: `supabase/migrations/20261125000000_funded_tape_site.sql`.

**Seeded data.** 71 sources from the plan's source map, plus the 13 source links and 5 picks from the demo edition. The demo edition itself (dated 2026-11-01) is stored as a **draft**, because it was never approved.

**Env vars** (Vercel production + preview, and `site/.env.local` locally; names in `site/.env.example`): `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `BOT_TOKEN`, `PREVIEW_KEY`, `OWNER_KEY`, `FT_JOB_SECRET`, `RESEND_API_KEY`, `NOTIFY_EMAIL`.

**Run locally:** `cd site && npm install && npm run dev`. **Deploy:** merging to `main` deploys to production automatically. Vercel's root directory is `site`; every PR gets a preview deploy.

**Auto-review + publish (from Nov 26, 2026, delegated by pomo651).** A pg_cron job calls `/api/jobs/auto-publish` daily at 7:45 AM ET (DST-safe). It runs `ft_review_edition`, publishes if every check passes, otherwise holds the draft, and emails pomo651 either way. Each run is logged in `funded_tape.publish_log` and shown on the draft page. The checks are listed in `site/BOT_API.md`.

**Monitoring + alerts (from Nov 26, 2026).** `/admin/monitor` grades every step of every day: collect by 6:00, picks by 6:45, draft by 7:15, publish at 7:45, and (once FT-video starts posting) Short by 8:45 and its approval. Each step is green, amber (late / needs pomo651), red (missing / held), or grey (not due / off). pg_cron runs two checkpoints: **7:20 AM ET** emails pomo651 about any red collect / picks / draft step before the 7:45 publish, and **8:55 AM ET** emails about anything red, late or waiting on pomo651. Each problem is emailed once per day (`funded_tape.monitor_alerts`). If the DB can't be read, that's emailed too. The page and the emails both read `ft_monitor`, so they always agree.

**Publishing by hand (owner only).** pomo651 opens `/daily?preview=<PREVIEW_KEY>`, opens the draft, enters the owner key, and clicks **Publish edition**. **Approve Short for upload** works the same way. Bots can't publish, can't change a published edition, and can't change an approved Short.

**New data fields (Nov 26, 2026).** Items accept `category`, `source_published_at`, `evidence`, `evidence_url` and `notes`. Shorts are posted with `POST /api/bot/videos`. Details: `site/BOT_API.md` and `plan/DATA_FORMAT.md`. On the home page, picks now show their category tag.

## Archive / newsletter files

Synced from the team's local working copy on Nov 25, 2026. These files had not been committed after the initial repo layout.

- `editions/` also holds the FINAL drafts of editions #1 (Nov 8), #2 (Nov 16), and #3 (Nov 22): markdown, HTML, Beehiiv-clean HTML, a desktop preview PNG, and notes to FT-PM (filenames still say KFC), plus the Nov 6–7 verify-for-kfc notes. **Editions #1–#3 were drafted for the old weekly cadence. There is no confirmed send on record; see [`cutoffs.md`](cutoffs.md).**
- `funded-tape-template.html` and `designs/` — the Design B email template and the A–D design explorations (HTML + desktop/mobile previews).
- `video/` — Shorts pipeline code and small assets (`build.sh`, `render.py`, `make_audio.py`, template, cover, script, metadata). Large rendered MP4s are not stored in the repo.
- `proposals/` and `reports/` — the video/newsletter content-strategy proposal and the Nov 25 status report.
- `cutoffs.md` and `send-schedule.md` — the weekly edition windows and test-send schedule (historical; the newsletter is now daily).
- `scripts/build_*.py` and `scripts/shoot.py` — builders that produced the edition HTML and screenshots. They were moved here from the local working copy; `scripts/build_html.py` (the plan builder already in the repo) was left unchanged.
