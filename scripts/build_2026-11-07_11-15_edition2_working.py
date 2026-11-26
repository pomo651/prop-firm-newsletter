# Builds Funded Tape edition #2 EARLY WORKING DRAFT (Fri Nov 13) - markdown + HTML, design B.
import html, re

TITLE = "Funded Tape: Top 5 Things You Can't Miss This Week (Nov 7 – Nov 15, 2026)"
SUBJECT = "Funded Tape: GFF's new 1-minute rule, a TopstepX glitch, and Tradeify's $12K Miami cap"
ALTS = ["Funded Tape: A $20 same-day challenge, a Miami prop plan, and PFM's new ranking",
        "Funded Tape: 5 rule changes and launches from Nov 7 – Nov 15"]
PREVIEW = "Goat Funded Futures' 1-minute rule, the TopstepX outage, Tradeify's Miami Plan, Prop Firm Match's sales-based ranking, and FundedNext's $20 FNL:005."
HOOK = "A scalping rule got rewritten, a prop plan got a soccer-club partner, and the biggest ranking site says its list is now a sales chart."
GREETING = "Happy Monday, traders \U0001F44B"
INTRO = ("This week Goat Funded Futures rewrote its holding-time rule, TopstepX had a Thursday-night data glitch, Tradeify launched a plan with Inter Miami CF, "
         "Prop Firm Match changed how it ranks firms, and FundedNext dropped a same-day challenge from $20. Here are the 5 things you can't miss.")

LABELS = {"DRAMA": ("\U0001F6A8 DRAMA", "#FFE4EC"), "DEAL": ("\U0001F3AB DEAL WATCH", "#E0F2FE"),
          "LAUNCH": ("\U0001F680 NEW LAUNCH", "#FEF3C7"), "RULE": ("\U0001F4DD RULE BOOK", "#EDE9FE"),
          "HEADS": ("\U0001F3AF HEADS UP", "#DCFCE7")}

STORIES = [
 dict(label="RULE",
  headline="Goat Funded Futures swaps its 2-minute rule for a 70% \"1 minute rule\" on every plan",
  paras=[
   "Since Mon Nov 9, every Goat Funded Futures (GFF) plan, from EOD and Flex to Daily Payouts, the Instant plans and GOAT Access, runs one holding-time check when you pass an evaluation and at every payout request: at least 70% of your closed trades, and at least 70% of your net profit, must come from trades held longer than 1 minute. Miss either and the payout is declined and that cycle's under-1-minute profit is deducted, though GFF says the account stays open.",
   "It replaces the old per-trade 2-minute microscalping deduction, raises Flex's threshold from 50% to 70%, and applies to new and existing accounts; cycles through Sun Nov 8 stay on the old rules. Partial closes count as separate trades, and tick scalping is still banned on every account.",
  ],
  why="Scalpers: track your hold times per payout cycle. A cluster of sub-minute trades can now block a whole payout, even on an account you bought before Nov 9.",
  links=[("GFF holding-time rules","https://help.goatfundedfutures.com/en/articles/14130422-holding-time-rules-on-each-plan"),("GFF Flex rules","https://help.goatfundedfutures.com/en/articles/14888545-flex-challenge-specifications-rules-and-payouts"),("GFF on X","https://x.com/GFFutures/status/2121149304202985925")]),
 dict(label="HEADS",
  headline="TopstepX had a data glitch Thursday night. If you were hit, don't touch the account yet",
  paras=[
   "Topstep says TopstepX trading data had an issue on Thu Nov 12 from 7:26 to 9:59 PM CT (8:26 to 10:59 PM ET). If you think your account was affected, Topstep asked you not to place trades, reset or delete the account until it follows up, because that could stop it from offering a resolution, and said you don't need to open a ticket.",
   "On Friday Topstep told a trader on X it would email everyone affected \"later today with a resolution.\" It hasn't said what went wrong or how many accounts were affected.",
  ],
  why="If you traded TopstepX Thursday evening, leave the account as is until Topstep's email tells you it's OK, then check the fix against your own trade log.",
  links=[("Topstep on X (status)","https://x.com/Topstep/status/2121094791823855705"),("Topstep on X (first alert)","https://x.com/Topstep/status/2121075303682638015"),("Topstep reply on X","https://x.com/Topstep/status/2121283251142590670")]),
 dict(label="LAUNCH",
  headline="Tradeify's Inter Miami \"Miami Plan\": one-day pass, static drawdown, and a hard $12,000 ending",
  paras=[
   "Tradeify became Inter Miami CF's Official Trading Partner on Nov 12 and launched the Miami Plan, a limited micros-only drop (10K, 25K, 50K) with no minimum days, no consistency rule, and a static drawdown that doesn't move even after payouts. A day later V2 joined V1: each payout splits 80% to you, 10% to a \"live fund\" and 10% to Tradeify (V1 is 75/10/15), with higher micro limits and lower targets on the 10K and 25K.",
   "The catch is in Tradeify's FAQ: Miami payout requests cap at $12,000 in total, and any profit above that is forfeited. Hit the cap and you move to a separate $1,500 Miami live account (90/10, daily payouts), and every other Tradeify account you hold is paused until that live account breaches. KYC is required at purchase, and it's one buyer per household.",
  ],
  why="It's cheap and quick to pass, but it's designed to end at $12,000 in requests, about $9,600 in cash on V2 per Tradeify. Skip it if you need your other Tradeify accounts to keep running.",
  links=[("Tradeify Miami Plan FAQ","https://help.tradeify.co/en/articles/18370624-miami-plan-faq"),("Tradeify launch on X","https://x.com/Tradeify/status/2120933200679555146"),("Miami Plan 2.0 on X","https://x.com/Tradeify/status/2121276469582115029"),("Inter Miami partnership on X","https://x.com/Tradeify/status/2120885894538289588")]),
 dict(label="HEADS",
  headline="Prop Firm Match's homepage now ranks its best-selling partners",
  paras=[
   "In a Nov 9 update to its statement, Prop Firm Match (PFM) said that with several firms pausing or ending partnerships, it no longer gets the same sales data and can't apply its old ranking (sales, views, ratings and favourites) consistently. Its homepage will now \"prioritize our best-selling active partners,\" with a label, and PFM says a firm's position reflects its sales through PFM and partnership status and \"should not be interpreted as an independent assessment\" of the firm.",
   "PFM says it will still show factual information on non-partner firms, and its review of the referral-redirect issue we covered last week is ongoing.",
  ],
  why="By PFM's own description, its homepage order is now a sales chart, not a quality ranking. Compare rules and payout terms on the firms' own pages.",
  links=[("PFM statement (Nov 9 update)","https://propfirmmatch.com/perpetuals/statement")]),
 dict(label="LAUNCH",
  headline="FundedNext Labs FNL:005: pick a $20 to $200 stake, hit one target the same day",
  paras=[
   "FundedNext's new CFD Labs drop, FNL:005, has you pick a $20, $50, $100 or $200 stake and a 3x or 5x multiplier, then trade a $10,000 account. Hit the target ($200 at 3x, $245 at 5x) before server close on the day you place your first trade, without losing $90 (3x) or $70 (5x), and you can request the reward that day: a multiple of your stake, up to $1,000 after KYC, per FundedNext.",
   "There's no daily loss limit, but the Labs page lists a 50% best-trade rule, and it's capped at 5 accounts per user while slots last.",
  ],
  why="It's a one-day shot where the reward is a multiple of what you pay and the loss limit is tight. Read the best-trade rule before you try it.",
  links=[("FundedNext Labs page","https://fundednext.com/labs"),("FundedNext on X","https://x.com/FundedNext/status/2120857111215387075")]),
]

OUTRO = "That's a wrap on edition #2! \U0001F389 Rules and deals change constantly, so always check the firm's own page before you buy. Hit reply and tell us which firm we should dig into next."
SIGN = "See you next week,"
NFA = "Not financial advice. Prop firm accounts are mostly simulated, and trading involves risk."

# ---------- markdown ----------
md = []
md.append("# Funded Tape #2: EARLY WORKING DRAFT (Fri Nov 13) for KFC. Not final, not approved, do not send\n")
md.append("**Window:** after Sat Nov 7 5 PM ET to Sun Nov 15 5 PM ET (per cutoffs.md); this draft covers news through ~1 PM ET Fri Nov 13. **Final draft:** Sun Nov 15 after the 5 PM ET cutoff. **Send:** Mon Nov 16, 7 AM ET, only after pomo651 approves.\n")
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
  f"<b>EARLY WORKING DRAFT (Fri Nov 13) &mdash; NOT SENT.</b> Final comes Sun Nov 15. Remove this box before scheduling.<br><b>Subject:</b> {e(SUBJECT)}<br><b>Alt 1:</b> {e(ALTS[0])}<br><b>Alt 2:</b> {e(ALTS[1])}<br><b>Preview:</b> {e(PREVIEW)}</td></tr>", out, count=1, flags=re.S)
out = out.replace("OCT 26 &ndash; NOV 1, 2026 &nbsp;&#183;&nbsp; DEMO EDITION &nbsp;&#183;&nbsp; 5 MIN READ",
                  "NOV 7 &ndash; NOV 15, 2026 &nbsp;&#183;&nbsp; EDITION #2 &nbsp;&#183;&nbsp; 5 MIN READ")
# greeting + intro (+ hook)
out = re.sub(r'(<p style="margin:0 0 10px 0;[^"]*">)Happy Sunday, traders &#128075;</p>\s*<p style="([^"]*)">.*?</p>',
  lambda m: f'<p style="margin:0 0 8px 0;{F}font-size:13px;font-weight:bold;color:#FF5C8A;letter-spacing:.5px;">{e(TITLE)}</p>'
            f'<p style="margin:0 0 14px 0;{F}font-size:16px;font-style:italic;line-height:1.5;color:#1E1B4B;">{e(HOOK)}</p>'
            f'{m.group(1)}Happy Monday, traders &#128075;</p>\n <p style="{m.group(2)}">{e(INTRO)}</p>', out, count=1, flags=re.S)
# stories: replace everything from first story row to the outro row
start = out.index('<tr><td class="px" style="padding:0 28px 22px 28px;">')
end = out.index('<tr><td class="px" style="padding:4px 28px 18px 28px;')
out = out[:start] + "\n".join(story_html(i, s) for i, s in enumerate(STORIES, 1)) + "\n" + out[end:]
out = re.sub(r"That&rsquo;s a wrap! &#127881;.*?See you next Sunday,",
  e(OUTRO).replace("\U0001F389", "&#127881;") + " We&rsquo;re independent, and any affiliate link will be labeled.<br><br>" + SIGN, out, count=1, flags=re.S)
out = out.replace("&#9888;&#65039; Not financial advice. Prop firm accounts are mostly simulated, and most traders do not receive a payout.", "&#9888;&#65039; " + e(NFA))

clean = re.sub(r'<tr>\s*<td style="background:#FFFFFF;border:1px dashed #FF5C8A;.*?</td></tr>', '', out, count=1, flags=re.S)
assert 'WORKING DRAFT' not in clean and '<b>Alt 1:' not in clean

base = "2026-11-07_11-15-edition2-WORKING-DRAFT-fri"
dirs = ["/workspace/prop-firm-newsletter/editions", "/cursor/stores/store-96c964e7-e846-4a02-a0c0-a86cd3b1304f/newsletter"]
for d in dirs:
    open(f"{d}/{base}.md", "w", encoding="utf-8").write(MD)
    open(f"{d}/{base}.html", "w", encoding="utf-8").write(out)
    open(f"{d}/{base}-beehiiv-clean.html", "w", encoding="utf-8").write(clean)

# link check
mdl = set(re.findall(r"\]\((https?://[^)]+)\)", MD))
htl = set(u for u in re.findall(r'href="(https?://[^"]+)"', out))
print("md links", len(mdl), "html links", len(htl), "match", mdl == htl, mdl ^ htl)
for bad in ["DEMO", "Happy Sunday", "Happy Friday", "OCT 26", "OCT 31", "FINAL DRAFT"]:
    print(bad, bad in out)

assert mdl == htl == set(re.findall(r'href="(https?://[^"]+)"', clean))
