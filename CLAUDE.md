# prop-firm-newsletter — rules for the local FT-team (Claude Code)

Two teams share this repo:

| Team | Who | Works where |
|---|---|---|
| **FT-grok** | Grok bots: FT-PM, FT-sources, FT-community, FT-editor, FT-video, Drew (see `plan/TEAM.md`) | Cloud |
| **local FT-team** | pomo651 (owner) + Claude Code | This machine (`~/@Pomo651/prop-firm-newsletter`) |

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
