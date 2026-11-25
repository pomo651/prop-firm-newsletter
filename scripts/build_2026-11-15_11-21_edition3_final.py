# Builds Funded Tape edition #3 FINAL DRAFT (Sat Nov 21) - markdown + HTML, design B.
# Derived from build_2026-11-15_11-21_edition3_working.py. Nothing is sent or scheduled.
import html, re

TITLE = "Funded Tape: Top 5 Things You Can't Miss This Week (Nov 15 – Nov 21)"
SUBJECT = "Funded Tape: Topstep's 13-country cutoff, Blue Guardian's $8K-a-day catch, and Alpha's 200-account drop"
ALTS = ["Funded Tape: Faster BrightFunded payouts, E8 Classic is back, and Topstep drops Wise",
        "Funded Tape: The 5 prop firm stories from Nov 15 – Nov 21 you can't miss"]
PREVIEW = "Topstep's 13-country closure and Wise exit, Blue Guardian's Futures Zero, BrightFunded's faster payouts, E8 Classic's static drawdown, and Alpha Futures' OPS 001."
HOOK = "One firm drew a border, two rewrote their payout clocks, and one is selling just 200 accounts with no consistency rule."
GREETING = "Happy Sunday, traders \U0001F44B"
INTRO = ("This week Topstep closed new accounts in 13 countries and quietly dropped Wise payouts, Blue Guardian swapped Express for an uncapped (mostly) futures plan, BrightFunded sped up payouts on new accounts, "
         "E8 brought back its Classic one-step, and Alpha Futures opened a limited no-consistency drop. Here are the 5 things you can't miss.")

LABELS = {"DRAMA": ("\U0001F6A8 DRAMA", "#FFE4EC"), "DEAL": ("\U0001F3AB DEAL WATCH", "#E0F2FE"),
          "LAUNCH": ("\U0001F680 NEW LAUNCH", "#FEF3C7"), "RULE": ("\U0001F4DD RULE BOOK", "#EDE9FE"),
          "HEADS": ("\U0001F3AF HEADS UP", "#DCFCE7")}

STORIES = [
 dict(label="RULE",
  headline="Topstep shuts new accounts in 13 countries (funded accounts keep getting paid) and drops Wise payouts",
  paras=[
   "Since Tue Nov 17, Topstep no longer sells new accounts or products to residents of Andorra, Cambodia, Ethiopia, Guinea, Kyrgyzstan, Laos, Macao, Mozambique, Namibia, Senegal, Serbia, Uzbekistan and Zimbabwe. Topstep says it affects fewer than 1,000 active traders and blames a rise in coordinated activity from those countries: ID documents that didn't belong to the applicant, purchases with other people's cards, and groups of accounts trading opposite sides of the same position.",
   "Topstep says funded accounts (Express Funded, Live Funded, and Challenges or Labs drops that reached the funded stage) keep trading and taking payouts before and after Dec 31, but Back2Funded is off the table and a funded account that closes can't be replaced. Trading Combine subscriptions are cancelled, non-funded accounts run until their paid-through date or Dec 31 at 5 PM CT (6 PM ET), whichever comes first, and anything still open then is refunded around Jan 4, along with unused banked Resets.",
   "Separately, and for every trader outside the US: Topstep's payout policy page (last updated Nov 19) now says Wise is no longer available for payouts. International traders are told to pick Wire, which the page lists at $30 and 5 to 10 business days.",
  ],
  why="If you live in one of the 13, the clock is Dec 31, 6 PM ET: pass and activate your Express Funded Account before then, use banked Resets now, and trade funded accounts like they're irreplaceable, because they are. Everyone else outside the US: budget $30 and an extra week or so per payout now that Wise is gone.",
  links=[("Topstep on X (Nov 17 details)","https://x.com/Topstep/status/2122838087453540518"),("Topstep on X (Nov 16)","https://x.com/Topstep/status/2122378475495457105"),("Topstep eligibility FAQ","https://help.topstep.com/en/articles/8284116-am-i-eligible-to-trade-with-topstep"),("Topstep payout policy","https://help.topstep.com/en/articles/8284233-topstep-payout-policy")]),
 dict(label="LAUNCH",
  headline="Blue Guardian's Futures Zero pays daily with no payout cap, but an $8,000 day ends the account",
  paras=[
   "Blue Guardian stopped selling Express on Nov 16 (existing Express accounts keep their rules) and rolled out Zero in its place. Zero is a one-phase futures evaluation on NinjaTrader in 25K to 150K: hit a 6% target with no time limit, and pick at checkout between end-of-day or intraday drawdown, with or without a daily loss limit, and a 30%, 40% or 50% consistency rule for the evaluation. Funded, you can withdraw profit above your buffer every day, $500 minimum, at a 90% split.",
   "The fine print is on the help page: funded Zero accounts always use an intraday trailing drawdown, news trading isn't allowed once funded, and any funded Zero account that makes $8,000 net profit in one trading day is closed. You then take $3,600 per account that hit it (all your funded Zero accounts close, plus a 30-day cooldown) or merge into one Live account, and profit above $8,000 that day isn't kept. Funded positions also close automatically at 4:10 PM New York time, so there's no holding overnight.",
  ],
  why="\"No payout cap\" isn't \"no ceiling.\" Size so no single day can get near $8,000, and remember the funded drawdown follows your open profit, unlike an end-of-day evaluation.",
  links=[("Blue Guardian Zero rules","https://help.blueguardian.com/en/articles/18446026-zero-account-rules"),("Express rules (no longer sold)","https://help.blueguardian.com/en/articles/18426764-express-account-rules"),("Blue Guardian on X","https://x.com/BlueGuardiancom/status/2122738659971486154")]),
 dict(label="RULE",
  headline="BrightFunded speeds up payouts on new accounts and adds no-challenge Instant Funding",
  paras=[
   "For accounts bought from Mon Nov 16, BrightFunded's 1-Step is now 1-Step Daily: no minimum trading days (was 5), first payout any day (was after 30 days) and daily payouts (was every 14 days). 2-Step Bright now needs 3 profitable days per phase instead of 5 trading days, and the first payout comes after 14 days instead of 30; targets, loss limits, split and the 14-day cycle stay the same.",
   "BrightFunded also launched Instant Funding for CFDs: no challenge, no profit target, on-demand payouts and up to a 90% split. Its page lists a 15% consistency rule (your best day can't be more than 15% of total net profit) and a 1% max open risk across all open trades.",
  ],
  why="Accounts bought before Nov 16 keep the old minimum days and payout timers, so check your purchase date before planning a withdrawal. On Instant, the 15% best-day rule is the real gate: one big day can stall your payout.",
  links=[("BrightFunded on X (rule changes)","https://x.com/BrightFunded/status/2122364882091696392"),("Existing accounts on X","https://x.com/BrightFunded/status/2122364894200639493"),("BrightFunded Instant page","https://brightfunded.com/cfds/instant")]),
 dict(label="LAUNCH",
  headline="E8 Classic is back: one step, an 8% target, and a 4% drawdown that never moves",
  paras=[
   "E8 Markets relaunched E8 Classic on Nov 17 and said E8 Classic Forex was live on Nov 18: one phase, an 8% profit target, a static 4% max drawdown, and a choice of a 2% daily loss limit or no daily limit. E8 says the drawdown \"never moves, not even after payout,\" with no consistency rule, no buffer, and payouts from $100.",
   "E8's Classic page also says, in its FAQ, that only 40% of profit made around high-impact news is credited in the funded (performance) stage, and that you're capped at $100K across Classic accounts (for example, two $50K). That FAQ is general, and we haven't confirmed these two points apply specifically to forex.",
  ],
  why="A static floor means payouts never eat into your cushion, but 4% is still tight. If you trade news, check the current terms for your market with E8 before you buy.",
  links=[("E8 Classic page","https://e8markets.com/e8-classic"),("E8 on X (terms)","https://x.com/E8Markets/status/2122605567734919438"),("E8 on X (Classic V2)","https://x.com/E8Markets/status/2122738411421479018"),("E8 on X (forex live, Nov 18)","https://x.com/E8Markets/status/2123031668810518800")]),
 dict(label="HEADS",
  headline="Alpha Futures' OPS 001: 200 no-evaluation futures accounts with no consistency rule",
  paras=[
   "Alpha Futures launched a new dashboard on Nov 19 with \"Alpha OPS,\" limited releases sold through the dashboard. The first drop, OPS 001, is a Direct account: no evaluation, qualified from day one, and no consistency rule (the public Direct plan has 20%). The OPS 001 page lists 25K for $349 and 50K for $519, a 90% split, a 1-day minimum, and only 200 accounts in total, up to 5 per person.",
   "On the 25K, the first payout request needs $1,500 profit and later ones $1,000, each capped at $1,000, with a $1,000 end-of-day trailing max loss and a $500 daily loss limit (the 50K doubles those). There's no scaling plan, and you can't place orders within 2 minutes before or after high-impact news.",
  ],
  why="No consistency rule removes the most common payout blocker, but $1,000 of max loss against a $1,500 first target is thin room. Alpha's X post mentions sizes up to 150K while the OPS page shows only 25K and 50K, so check what your dashboard actually offers before you buy. It's gone once all 200 sell.",
  links=[("Alpha OPS 001 page","https://alpha-futures.com/ops-001"),("Alpha Futures on X (Nov 19)","https://x.com/Alpha_Futures_/status/2123362389357674986"),("Alpha Futures on X (Nov 20)","https://x.com/Alpha_Futures_/status/2123797183505784993")]),
]

OUTRO = "That's a wrap on edition #3! \U0001F389 Rules and deals change constantly, so always check the firm's own page before you buy. Hit reply and tell us which firm we should dig into next."
SIGN = "See you next week,"
NFA = "Not financial advice. Prop firm accounts are mostly simulated, and trading involves risk."

# ---------- markdown ----------
md = []
md.append("# Funded Tape #3: FINAL DRAFT (Sat Nov 21) for KFC. Not approved, do not send\n")
md.append("**Window:** after Sun Nov 15 5 PM ET to Sat Nov 21 5 PM ET (per cutoffs.md); this final draft covers news through the 5 PM ET cutoff (Feed final sweep ~3:15 PM ET, Pulse final ~2:35 PM ET, my own official-X check for 3–5 PM ET plus primary-page rechecks ~5:10–5:30 PM ET). **Send:** Sun Nov 22, 9 AM ET, only after pomo651 approves.\n")
md.append("## Beehiiv package\n")
md.append(f"**Subject:** {SUBJECT}  ")
md.append(f"**Alt 1:** {ALTS[0]}  ")
md.append(f"**Alt 2:** {ALTS[1]}  ")
md.append(f"**Preview text:** {PREVIEW}\n")
md.append("---\n")
md.append(f"# {TITLE}\n")
md.append(f"*{HOOK}*\n")
md.append(f"**{GREETING}**\n")
md.append(INTRO + "\n")
for i, s in enumerate(STORIES, 1):
    md.append(f"### {i}. {LABELS[s['label']][0]}\n")
    md.append(f"**{s['headline']}**\n")
    for p in s["paras"]:
        md.append(p + "\n")
    md.append(f"> \U0001F4A1 **Why it matters:** *{s['why']}*\n")
    md.append("Sources: " + " · ".join(f"[{t}]({u})" for t, u in s["links"]) + "\n")
md.append("---\n")
md.append(OUTRO + "\n")
md.append(f"{SIGN}  \n**The Funded Tape crew**\n")
md.append(f"*\u26A0\uFE0F {NFA}*\n")
MD = "\n".join(md)

# ---------- html (design B template) ----------
tpl = open("/workspace/prop-firm-newsletter/funded-tape-template.html", encoding="utf-8").read()
e = lambda t: html.escape(t, quote=False)
F = "font-family:'Trebuchet MS',Helvetica,Arial,sans-serif;"

def story_html(i, s):
    lab, bg = LABELS[s["label"]]
    paras = "".join(f'<p style="margin:0 0 12px 0;{F}font-size:15px;line-height:1.6;color:#333;">{e(p)}</p>' for p in s["paras"])
    links = " &middot; ".join(f'<a href="{u}" style="color:#3B5BFD;text-decoration:underline;{F}">{e(t)}</a>' for t, u in s["links"])
    return f'''<tr><td class="px" style="padding:0 28px 22px 28px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border:2px solid #1E1B4B;border-radius:14px;">
<tr><td style="padding:16px 20px 0 20px;"><span style="display:inline-block;background:{bg};border-radius:20px;padding:4px 12px;{F}font-size:12px;font-weight:bold;color:#1E1B4B;letter-spacing:1px;">{e(lab)}</span></td></tr>
<tr><td style="padding:10px 20px 8px 20px;"><h2 style="margin:0;{F}font-size:20px;line-height:1.3;color:#1E1B4B;">{i}. {e(s["headline"])}</h2></td></tr>
<tr><td style="padding:4px 20px 0 20px;">{paras}</td></tr>
<tr><td style="padding:0 20px 14px 20px;"><div style="background:#FFD23F;border-radius:10px;padding:10px 14px;{F}font-size:14px;line-height:1.5;color:#1E1B4B;"><b>&#128161; Why it matters:</b> {e(s["why"])}</div></td></tr>
<tr><td style="padding:0 20px 18px 20px;{F}font-size:13px;color:#666;">&#128279; {links}</td></tr>
</table></td></tr>'''

out = tpl
out = re.sub(r"<title>.*?</title>", f"<title>{e(SUBJECT)}</title>", out, flags=re.S)
out = out.replace("5 prop firm moves from this week, and what each one means for your next account.&#847;", e(PREVIEW) + "&#847;")
out = re.sub(r"<b>DEMO &mdash; NOT SENT.</b>.*?</td></tr>",
  f"<b>FINAL DRAFT (Sat Nov 21) &mdash; NOT SENT, needs pomo651 approval.</b> Remove this box before scheduling.<br><b>Subject:</b> {e(SUBJECT)}<br><b>Alt 1:</b> {e(ALTS[0])}<br><b>Alt 2:</b> {e(ALTS[1])}<br><b>Preview:</b> {e(PREVIEW)}</td></tr>", out, count=1, flags=re.S)
out = out.replace("OCT 26 &ndash; NOV 1, 2026 &nbsp;&#183;&nbsp; DEMO EDITION &nbsp;&#183;&nbsp; 5 MIN READ",
                  "NOV 15 &ndash; NOV 21, 2026 &nbsp;&#183;&nbsp; EDITION #3 &nbsp;&#183;&nbsp; 5 MIN READ")
# greeting + intro (+ hook)
out = re.sub(r'(<p style="margin:0 0 10px 0;[^"]*">)Happy Sunday, traders &#128075;</p>\s*<p style="([^"]*)">.*?</p>',
  lambda m: f'<p style="margin:0 0 8px 0;{F}font-size:13px;font-weight:bold;color:#FF5C8A;letter-spacing:.5px;">{e(TITLE)}</p>'
            f'<p style="margin:0 0 14px 0;{F}font-size:16px;font-style:italic;line-height:1.5;color:#1E1B4B;">{e(HOOK)}</p>'
            f'{m.group(1)}Happy Sunday, traders &#128075;</p>\n <p style="{m.group(2)}">{e(INTRO)}</p>', out, count=1, flags=re.S)
# stories: replace everything from first story row to the outro row
start = out.index('<tr><td class="px" style="padding:0 28px 22px 28px;">')
end = out.index('<tr><td class="px" style="padding:4px 28px 18px 28px;')
out = out[:start] + "\n".join(story_html(i, s) for i, s in enumerate(STORIES, 1)) + "\n" + out[end:]
out = re.sub(r"That&rsquo;s a wrap! &#127881;.*?See you next Sunday,",
  e(OUTRO).replace("\U0001F389", "&#127881;") + " We&rsquo;re independent, and any affiliate link will be labeled.<br><br>" + SIGN, out, count=1, flags=re.S)
out = out.replace("&#9888;&#65039; Not financial advice. Prop firm accounts are mostly simulated, and most traders do not receive a payout.", "&#9888;&#65039; " + e(NFA))

clean = re.sub(r'<tr>\s*<td style="background:#FFFFFF;border:1px dashed #FF5C8A;.*?</td></tr>', '', out, count=1, flags=re.S)
assert 'FINAL DRAFT' not in clean and '<b>Alt 1:' not in clean

base = "2026-11-15_11-21-edition3-FINAL"
dirs = ["/workspace/prop-firm-newsletter/editions", "/cursor/stores/store-96c964e7-e846-4a02-a0c0-a86cd3b1304f/newsletter"]
for d in dirs:
    open(f"{d}/{base}.md", "w", encoding="utf-8").write(MD)
    open(f"{d}/{base}.html", "w", encoding="utf-8").write(out)
    open(f"{d}/{base}-beehiiv-clean.html", "w", encoding="utf-8").write(clean)

# link check
mdl = set(re.findall(r"\]\((https?://[^)]+)\)", MD))
htl = set(u for u in re.findall(r'href="(https?://[^"]+)"', out))
print("md links", len(mdl), "html links", len(htl), "match", mdl == htl, mdl ^ htl)
for bad in ["DEMO", "Happy Monday", "Happy Friday", "OCT 26", "NOV 7 &ndash;", "WORKING DRAFT", "MyForexFunds"]:
    print(bad, bad in out)

assert mdl == htl == set(re.findall(r'href="(https?://[^"]+)"', clean))
