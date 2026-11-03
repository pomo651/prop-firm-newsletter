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

Future editions use `editions/YYYY-MM-DD_MM-DD.md`, named for the week the issue covers.
