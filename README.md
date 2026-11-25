# Funded Tape

Funded Tape is a weekly newsletter for prop firm traders. Each issue is the top 5 things you can't miss in the prop firm world that week: what changed, why it matters, and the source.

## Roadmap

- **Alpha:** a free text email, "Top 5 things you can't miss in the prop firm world this week." Sent on [Beehiiv](https://www.beehiiv.com/)'s free plan.
- **Beta:** the same weekly issue, plus one YouTube video and Shorts.

## Weekly cadence

Watchers collect Monday through Thursday. The Editor drafts on Friday. The owner approves on Saturday. The issue sends on Sunday on Beehiiv.

## Bot team

- **KFC** is the CEO: plans the week, assigns work, and picks the Top 5.
- **Feed** covers official firm sources and trade press (help centers, rule pages, firm announcements, industry news).
- **Pulse** covers community sources: Reddit, X, YouTube, Discord, and reviews.
- **Editor** writes the weekly draft.

Nothing sends until the owner approves it.

## Layout

- `plan/` — static CEO plan. Version 1 (Nov 1, 2026) is `plan/prop-firm-ceo-plan-v1.html`. Rebuild it with `python3 scripts/build_html.py`.
- `editions/` — newsletter issues. `editions/2026-10-26_11-01-demo.txt` is a practice draft that was never sent.
- `research/` — background notes. `research/platform-pricing-2026-11-03.txt` is the platform check that chose Beehiiv's free plan.
- `scripts/` — helpers. `scripts/build_html.py` generates the plan HTML.
- `site/` — the Funded Tape website (Next.js on Vercel). See **Website** below.
- `supabase/migrations/` — database schema for the website.

Future editions use `editions/YYYY-MM-DD_MM-DD.md`, named for the week the issue covers.

## Website (added Nov 25, 2026)

Live: **https://prop-firm-newsletter.vercel.app** (Vercel project `prop-firm-newsletter`, root directory `site/`).

| Page | What it shows |
|---|---|
| `/` Home | How Funded Tape works: a live animation (many sources → a few picks → the newsletter), live counters (sources, items, picks, editions) and the latest picks. It refreshes every 30 seconds. |
| `/daily` Daily newsletter | Published editions, newest first. One page per edition at `/daily/YYYY-MM-DD`. |

The left sidebar has only these two pages for now.

**How bots feed it.** The site reads from a database. Bots write to it through `POST /api/bot/sources`, `/api/bot/items` and `/api/bot/editions` with a bearer token. Full guide: [`site/BOT_API.md`](site/BOT_API.md).

**Rules that change for the bot team**

1. Anything marked `picked` appears on the public home page right away. Pick only fact-checked items.
2. Editions are posted as `draft`. Only the owner publishes one, so "nothing goes out until the owner approves" still holds on the site.
3. The site has a **daily** newsletter section. The `editions/*.txt|md` files remain the working drafts. Post the final version to `/api/bot/editions` too.

**Database.** Supabase project `blackout-clock` (ref `fqgryxjuecjgelcjdvmq`), schema `funded_tape` (tables `sources`, `items`, `editions`). The site never touches blackout-clock's own tables. It reaches the data only through `public.ft_*` functions, which only the server key can call. Schema: `supabase/migrations/20261125000000_funded_tape_site.sql`.

**Seeded data.** 71 sources from the plan's source map, plus the 13 source links and 5 picks from the demo edition. The demo edition itself (dated 2026-11-01) is stored as a **draft**, because it was never approved.

**Env vars** (Vercel production + preview, and `site/.env.local` locally; names in `site/.env.example`): `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `BOT_TOKEN`, `PREVIEW_KEY`.

**Run locally:** `cd site && npm install && npm run dev`. **Deploy:** `cd site && vercel deploy --prod`.
