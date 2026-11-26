# Admin theme: bustem (same look as the VHealth and Kids Map admins)

The `/admin` pages use the FDE **bustem** theme: a calm, data-dense SaaS admin. The public site (`/`, `/daily`) keeps its own green look in `app/globals.css`; the two never mix.

## Files

| File | What it is | Edit it? |
|---|---|---|
| `app/admin/bustem.css` | The theme: tokens + every component, all scoped to `.bz`. Copied unchanged from the FDE theme. | **No.** Keep it identical to the source so the admins stay in step. Override in `admin.css`. |
| `app/admin/admin.css` | Funded Tape additions, prefixed `ft-` (pipeline step dots, 14-day strip, bar rows, workflow chain, sign-in). Also points the theme's font tokens at `next/font` Geist. | Yes. |
| `app/admin/layout.tsx` | Wraps every admin page in `<div class="bz ft-adm">`, loads Geist + Geist Mono, checks sign-in. | Rarely. |
| `components/admin/AdminNav.tsx` | Sidebar (`bz-side`, groups `bz-gl`, rows `bz-ni`). Add new pages to `GROUPS`. | When adding a page. |
| `components/admin/ui.tsx` | `Pill`, `Cat`, `Head`, `Bars`, `PartialNote`. Use these instead of hand-writing pills. | Yes. |

## The look in 8 rules

1. **Ink and warm greys only.** Ink `#0B0C0E`, text `#3A3A40`, muted `#6B6B73`, faint `#9A9994`, page `#F7F8FA` with a soft blue glow at the top.
2. **Colour means status, nothing else.** Green = done / OK, amber = needs attention, red = broken. No brand colour in the admin (the public site's green stays on the public site).
3. **Pill buttons.** One black primary per area, on the right. Everything else is a white ghost pill on its left. At most 2 buttons per row.
4. **Hairlines, not borders.** Cards use an inset 1px shadow (`--hair`). Radius 14px cards, 12px fields, 9px nav rows, 999px pills.
5. **Geist, weights 500 / 600.** h1 1.85rem, h2 1.1rem, table text .88rem, tiny uppercase group labels. Numbers use `tabular-nums`; codes use Geist Mono on a sand chip (`ft-code`).
6. **One line per thing.** Lists are tables (`bz-t`), grouped by a grey row (`tr.grp`): `Wed, Nov 25 · 4 items · 2 picked`.
7. **Status pills with a dot** (`bz-pill` + `g` / `o` / `r` / `b`). Counts go inside filter pills (`Picked 4`).
8. **Few words.** Title + one muted line. Long help folds into `details.bz-help`. Alert bars (`bz-alert`) only when something is wrong.

## Funded Tape status → colour

Always go through `<Pill v="…" />` so these stay consistent.

| Value | Pill | Meaning |
|---|---|---|
| item `new` | blue `b` | Collected, not reviewed yet |
| item `picked` | green `g` | Fact-checked, public on the home page |
| item `rejected` | grey | Reviewed and dropped (row is greyed) |
| edition `draft` | amber `o` | Not public |
| edition `published` | green `g` | Public |
| auto-review `held` | red `r` | Failed a check; needs pomo651 |
| Short `draft` | amber `o` ("Needs approval") | Waiting for pomo651 |
| Short `approved` / `uploaded` | green `g` | OK to upload / live |
| pipeline `done` / `wait` / `late` / `fail` | green / grey / amber / red | Today's step state |
| category `allegation` | red, no dot | Always labelled; picked only with official evidence |

A table row that breaks a rule gets a red left edge (`tr.bad`); one that needs a look gets amber (`tr.warn`).

## Page patterns used here

- **Monitoring (Today):** `bz-alert` (only when behind) → 4 `bz-kpi` tiles, each a link → pipeline table → "Needs you" list + 14-day strip → 3 small bar cards.
- **List (Items, Sources):** `Head` → optional alert → one `bz-card flush` with a `bz-bar` (filter pills left, count right) and a grouped `bz-t` table.
- **List with actions (Editions):** same, plus max 2 row buttons: ghost "Public page" left, black "Review" right. The right button turns ghost once nothing is waiting.
- **Reference (Workflows):** numbered cards in `ft-2` pairs, lists as `ft-list`, timetable as a `bz-t` table.

## Adding an admin page

1. Create `app/admin/<name>/page.tsx`. Start with `if (!(await isAdmin())) return null;` and read data with `getSnapshot()` from `lib/admin.ts`.
2. Use `Head`, `Pill`, `bz-card`, `bz-t`. Reuse a `bz-*` class before writing CSS. New CSS goes in `admin.css` with the `ft-` prefix, using the theme tokens (`var(--ink)`, `var(--ok)`…), never new hex values.
3. Add the page to `GROUPS` in `components/admin/AdminNav.tsx`.
4. Check it at 1440px and 390px wide (tables scroll inside their card).

## Don't

- No coloured primary buttons, no gradients on buttons or cards, no solid borders, no heavy shadows.
- No serif, no italics, no ALL CAPS except group labels.
- No stacked cards for something that could be a table rows list. No more than 2 buttons in a row.
- Don't edit `bustem.css`; don't import admin CSS into public pages.
