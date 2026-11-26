# Builds Funded Tape edition #1 FINAL (markdown + HTML, design B) from one content source.
import html, re, shutil, os

TITLE = "Funded Tape: Top 5 Things You Can't Miss This Week (Oct 31 – Nov 7, 2026)"
SUBJECT = "Funded Tape: Topstep tests daily payouts, FundingPips drops a $25K from $99, and Earn2Trade adds a 5-day payout rule"
ALTS = ["Funded Tape: Daily payouts, a $99 Labs account, and new rules at Earn2Trade",
        "Funded Tape: 5 payout and rule changes from Oct 31 – Nov 7"]
PREVIEW = "Topstep's Daily Payouts+, Prop Firm Match's Nov 2 statement, FundedNext's tiered Rapid caps, FundingPips EXP 004, and Earn2Trade's five-profitable-days rule."
HOOK = "Some firms made payouts faster this week, others made them harder to reach, and the biggest comparison site is still explaining itself."
GREETING = "Happy Sunday, traders \U0001F44B"
INTRO = ("Welcome to the very first Funded Tape. This week Topstep started testing daily payouts, FundingPips launched a cheap limited-run CFD account, "
         "and two firms changed how and when funded traders can withdraw. Here are the 5 things you can't miss.")

LABELS = {"DRAMA": ("\U0001F6A8 DRAMA", "#FFE4EC"), "DEAL": ("\U0001F3AB DEAL WATCH", "#E0F2FE"),
          "LAUNCH": ("\U0001F680 NEW LAUNCH", "#FEF3C7"), "RULE": ("\U0001F4DD RULE BOOK", "#EDE9FE"),
          "HEADS": ("\U0001F3AF HEADS UP", "#DCFCE7")}

STORIES = [
 dict(label="LAUNCH",
  headline="Topstep tests daily payouts with two limited Labs Combines",
  paras=[
   "On Nov 5 Topstep opened two limited $50K Labs Combines with \"Daily Payouts+\": #010 (EOD trailing, $119 one-time, $3,000 target) and #011 (static, $149, $4,000 target). Both have a $2,000 max loss, a mandatory $1,000 daily loss limit, a 55% consistency target, and a cap of 5 purchases per trader across both that doesn't refresh when accounts fail or close.",
   "Once funded, you pick a path at every payout: a daily payout of $250 to $1,500 (once per trading day, after a $2,000 profit buffer) or the 5 Winning Days path (up to $4,000 EOD or $8,000 static), both at 90/10. The catch, per Topstep's own help page: taking a daily payout sets your max loss limit to $0.",
  ],
  why="Understand the buffer, payout and max-loss rules before withdrawing.",
  links=[("Topstep blog","https://www.topstep.com/blog/daily-payouts"),("Topstep Labs help page","https://help.topstep.com/en/articles/15520357-topstep-labs"),("Topstep on X","https://x.com/Topstep/status/2118360434134634573")]),
 dict(label="DRAMA",
  headline="Prop Firm Match explains its referral-redirect problem",
  paras=[
   "In a statement last revised Nov 2, Prop Firm Match (PFM) said that from Oct 2025 its \"Copy Code\" and \"Buy\" buttons opened the firm you picked in a new tab while sending the original tab through that firm's affiliate link, and from Mar 2026 some firm-name and logo clicks did the same. PFM says it disabled this on Oct 29, removed it on Oct 31, and estimates the impact at a \"low single-digit percentage\" of commissions for most of 46 integrated partners. Its review is still in progress.",
   "Finance Magnates reported that about 21 brands, including Apex, Tradeify, Lucid, Goat Funded Trader, FundingPips and Blue Guardian, have ended partnerships. That count comes from the press, not PFM. Topstep never had a PFM affiliate code; per Finance Magnates, it paid for a listing and is dropping it.",
  ],
  why="PFM says prices and discounts weren't affected, but rankings and \"best deal\" lists are shifting as partners leave. Check a firm's own site for rules and codes rather than treating any comparison ranking as neutral.",
  links=[("PFM statement","https://propfirmmatch.com/futures/statement"),("PFM on X","https://x.com/PropFirmMatch/status/2117383581467054511"),("Finance Magnates","https://www.financemagnates.com/forex/2-dozen-brands-one-background-tab-how-prop-firm-matchs-affiliate-redirect-slipped-past-its-partners/")]),
 dict(label="RULE",
  headline="FundedNext Futures Rapid: help pages now show tiered early payout caps",
  paras=[
   "FundedNext's Rapid Daily and Rapid Pro help articles, both updated Nov 5, now list payout caps that rise by withdrawal: payouts 1 to 3 are capped at $600, $1,000 or $2,000 (25K, 50K, 100K), and payouts 4 and 5 at $850, $1,250 or $2,500. The minimum is $250, you need $500 profit in the cycle, the split is 90%, and the account concludes after the 5th reward.",
   "An older FundedNext help article still shows flat caps of $800, $1,200 and $2,500, so the firm's own pages don't fully agree yet. FundedNext hasn't said whether accounts bought before the update are affected.",
  ],
  why="If you're planning around Rapid's early withdrawals, use the Nov 5 tables, and ask support which caps apply to your account if you bought before Nov 5.",
  links=[("Rapid Daily rules","https://helpfutures.fundednext.com/en/articles/17229779-fundednext-futures-rapid-daily-fundednext-account-all-rules"),("Rapid Pro rules","https://helpfutures.fundednext.com/en/articles/17229713-fundednext-futures-rapid-pro-fundednext-account-all-rules"),("Older withdrawal help article","https://helpfutures.fundednext.com/en/articles/17242064-how-can-i-withdraw-my-performance-reward")]),
 dict(label="LAUNCH",
  headline="FundingPips drops EXP 004, a $25K one-step from $99",
  paras=[
   "FundingPips launched Labs EXP 004 on Nov 7: a limited-run $25K one-step CFD account with a 6% target and a 3% static max loss. It costs $99 with a 2% daily loss limit or $199 with none, max 3 per user. On the Master account you can request rewards from day one, as often as you like, from 1% ($250) at an 80% split. The fine print: on Master, profits from trades within 5 minutes of high-impact news are deducted, positions are closed automatically overnight, and weekend holding isn't allowed in either phase.",
   "Separately, a payout-terms dispute played out on X. Trader @Abdullahfxx alleged that FundingPips moved him onto On-Demand reward terms after he passed a challenge. On Nov 7, Avikk, an affiliated business-development team member, replied on X that those terms followed an individual risk review, were disclosed before the account was issued, and aren't applied to every trader. He later posted a screenshot of a trade he cited in his response; it has not been independently verified and covers only this case. Other traders' Device ID and account-closure allegations remain allegations with no public firm reply that we found.",
  ],
  why="EXP 004 is cheap, but the overnight close and news deductions on Master matter if you swing trade or trade news. And if a firm offers you different terms after you pass, read them before you accept the account.",
  links=[("EXP 004 help page","https://help.fundingpips.com/hc/en-us/articles/52395111530897-EXP-004"),("FundingPips on X","https://x.com/fundingpips/status/2118966842186489989"),("@Abdullahfxx on X","https://x.com/Abdullahfxx/status/2118313965755523243"),("@avikkfp reply on X","https://x.com/avikkfp/status/2119111176999313788"),("@avikkfp screenshot post on X","https://x.com/avikkfp/status/2119181752610767222")]),
 dict(label="RULE",
  headline="Earn2Trade swaps its Progression Ladder for fixed contract limits and a five-profitable-day payout rule",
  paras=[
   "For subscriptions bought on or after Nov 2, Earn2Trade replaced the Progression Ladder with fixed contract limits that the platform enforces by blocking oversize orders (for example, 4 contracts or 40 micros on a $50K, 8 on a $100K). Funded traders now need five profitable days, not necessarily in a row, before each withdrawal, with daily minimums from $100 (TCP25) to $350 (GAU200).",
   "Subscriptions bought before Nov 2 stay on the old rules, including their rebills, resets and any funded accounts that come from them. Earn2Trade says there's still no profit buffer or funded consistency rule, and the $100 minimum withdrawal is unchanged.",
  ],
  why="Your rules depend on when you bought. On a new subscription, plan for at least five qualifying days between payouts, and know you can't size past your limit as you grow.",
  links=[("Earn2Trade rule update","https://www.earn2trade.com/blog/earn2trade-rule-updates-november-2026/")]),
]

OUTRO = "That's a wrap on edition #1! \U0001F389 Rules and deals change constantly, so always check the firm's own page before you buy. Hit reply and tell us which firm we should dig into next."
SIGN = "See you next week,"
NFA = "Not financial advice. Prop firm accounts are mostly simulated, and trading involves risk."

# ---------- markdown ----------
md = []
md.append("# Funded Tape #1: FINAL draft for KFC (not approved, do not send)\n")
md.append("**Window:** after Sat Oct 31 5 PM ET to Sat Nov 7 5 PM ET (per cutoffs.md). **Send:** Sun Nov 8, 9 AM ET, after pomo651 approves.\n")
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
  f"<b>FINAL DRAFT &mdash; NOT SENT.</b> Awaiting pomo651's approval. Remove this box before scheduling.<br><b>Subject:</b> {e(SUBJECT)}<br><b>Alt 1:</b> {e(ALTS[0])}<br><b>Alt 2:</b> {e(ALTS[1])}<br><b>Preview:</b> {e(PREVIEW)}</td></tr>", out, count=1, flags=re.S)
out = out.replace("OCT 26 &ndash; NOV 1, 2026 &nbsp;&#183;&nbsp; DEMO EDITION &nbsp;&#183;&nbsp; 5 MIN READ",
                  "OCT 31 &ndash; NOV 7, 2026 &nbsp;&#183;&nbsp; EDITION #1 &nbsp;&#183;&nbsp; 5 MIN READ")
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

base = "2026-10-31_11-07-edition1-FINAL"
dirs = ["/workspace/prop-firm-newsletter/editions", "/cursor/stores/store-96c964e7-e846-4a02-a0c0-a86cd3b1304f/newsletter"]
for d in dirs:
    open(f"{d}/{base}.md", "w", encoding="utf-8").write(MD)
    open(f"{d}/{base}.html", "w", encoding="utf-8").write(out)
    open(f"{d}/{base}-beehiiv-clean.html", "w", encoding="utf-8").write(clean)

# link check
mdl = set(re.findall(r"\]\((https?://[^)]+)\)", MD))
htl = set(u for u in re.findall(r'href="(https?://[^"]+)"', out))
print("md links", len(mdl), "html links", len(htl), "match", mdl == htl, mdl ^ htl)
for bad in ["DEMO", "BrightFunded", "traderkane", "Happy Friday", "OCT 26"]:
    print(bad, bad in out)

assert mdl == htl == set(re.findall(r'href="(https?://[^"]+)"', clean))
