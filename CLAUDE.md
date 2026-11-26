# prop-firm-newsletter — rules for the local FT-team (Claude Code)

Two teams share this repo:

| Team | Who | Works where |
|---|---|---|
| **FT-grok** | Grok bots: FT-PM, FT-sources, FT-community, FT-editor, FT-video, Drew (see `plan/TEAM.md`) | Cloud |
| **local FT-team** | pomo651 (owner) + Claude Code | This machine (`~/@Pomo651/prop-firm-newsletter`) |

## Who owns what

| Area | Owner | What that means |
|---|---|---|
| **Data, media, resources**: sources, collecting, fact-checking, picks, edition text, Shorts, Beehiiv | **FT-grok** | They write into the DB **only** through `POST /api/bot/*` and keep `plan/`, `editions/`, `video/` current |
| **Website**: `site/`, `supabase/migrations/`, the bot API itself, deploys | **local FT-team** | We read the DB and render it. Page features, layout and new pages are our call |

- The website never collects or writes content itself. It only renders what FT-grok put in the DB (plus owner actions such as publishing).
- If FT-grok needs a new field or table (e.g. the proposed columns in `plan/DATA_FORMAT.md`), the local FT-team writes the migration, updates the bot API and `site/BOT_API.md`, deploys, and tells FT-grok in the PR.
- If an FT-grok PR edits `site/` or `supabase/`, treat it as a request. Review it extra carefully, or re-implement it ourselves.

### Agreement and acknowledgement (Nov 25, 2026)

**Agreement (set by pomo651, the owner):** FT-grok collects the data and saves it to the DB, and focuses on the media and resources side. The local FT-team renders that data on the website and controls the website's features.

| Party | Acknowledged |
|---|---|
| pomo651 (owner) | Yes, Nov 25, 2026 (set the agreement) |
| local FT-team (Claude Code) | Yes, Nov 25, 2026 |
| FT-grok | Pending. Asked to confirm in PR #8 (or reply in Funded Tape HQ) |

## Every session in this repo: check FT-grok's open PRs first

FT-grok marks each PR it opens with: **"Done by FT-grok — needs local FT-team review."**

1. `git pull` and run `gh pr list --repo pomo651/prop-firm-newsletter --state open`.
2. Review each FT-grok PR: read the README / `plan/` changes, scan the diff for secrets (tokens, keys), and check whether it touches `site/` or `supabase/`. If it does, build `site/` and check the live behaviour before merging.
3. If it's clean, merge it, then `git pull` so the local copy is in sync. If something is risky or unclear, don't merge. Tell pomo651 what you found.
4. Follow through on what the PR changes. If it renames something or changes a rule, update `site/`, the DB rows and the docs that still use the old version (example: PR #3 renamed the bots → PR #4 fixed the site docs and DB rows).
5. Report to pomo651 what was merged and what changed (a short table).

## When the local FT-team opens a PR

- Work on a branch and open a PR. Don't push straight to `main`.
- Start the PR body with: **"Done by local FT-team (pomo651 + Claude Code)."** If FT-grok should know about or act on the change, add: **"FT-grok: please read before your next run."**
- Every change is explained in `README.md` (and `plan/TEAM.md` if it affects roles or handoffs), because FT-grok learns about changes from the repo.

## Facts worth knowing

- Live site: https://prop-firm-newsletter.vercel.app. It does not deploy from GitHub; deploy with `cd site && vercel deploy --prod`.
- DB: blackout-clock Supabase (`fqgryxjuecjgelcjdvmq`), schema `funded_tape`. Apply SQL from `~/@Pomo651/blackout-clock` with `supabase db query --linked -f <file>`.
- Secrets (`BOT_TOKEN`, `PREVIEW_KEY`, service key) live in `site/.env.local` and Vercel. Never commit them.
- Only pomo651 approves or publishes an edition. The newsletter is daily; the exact times are pomo651's call.
