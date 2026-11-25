# Builds the Funded Tape demo email (email-safe HTML: tables + inline styles, no JS)
import html
OUT="/workspace/prop-firm-newsletter/demo-email-funded-tape.html"
F="font-family:Helvetica,Arial,sans-serif;"
NAVY="#0B1F33"; GREEN="#15803D"; INK="#1F2937"; MUTED="#6B7280"; LINE="#E5E7EB"

def e(s): return html.escape(s, quote=True)

def link(url, label=None):
    label = label or url.split("//",1)[1].split("/",1)[0].replace("www.","")
    return f'<a href="{e(url)}" style="color:{GREEN};text-decoration:underline;{F}font-size:13px;">{e(label)}</a>'

stories = [
 dict(h="Firms cut ties with Prop Firm Match over affiliate-tracking claims",
  body=["On Oct 29, trader @traderkane posted a video on X showing that clicking a firm profile or a \u201ccopy code\u201d button on Prop Firm Match (PFM) sent visitors through PFM\u2019s affiliate link. On Oct 30, Apex, Tradeify, Topstep and Goat Funded Trader said they were ending their affiliate ties with PFM.",
        "That evening PFM admitted the problem: \u201cThis should not have happened. We take full responsibility for it.\u201d It says it is working through the numbers with each partner."],
  why="Discount codes and \u201cbest firm\u201d rankings often come with affiliate money attached. Pick firms on their rules, not a comparison site\u2019s rank, and expect firms to tighten affiliate programs.",
  note="Disclosure: @traderkane\u2019s X bio says he is building @propfirm.",
  src=[("https://www.financemagnates.com/forex/prop-firm-match-faces-affiliate-tracking-allegations-topstep-apex-tradeify-and-goat-funded-cut-ties/","Finance Magnates"),
       ("https://x.com/PropFirmMatch/status/2116352044495765821","PFM statement on X"),
       ("https://x.com/traderkane/status/2115904959401140641","@traderkane on X")]),
 dict(h="FundedNext sells a $50K CFD account with no challenge for $149.99",
  body=["A limited Lab release (CFDs-FNL:004): 2,000 accounts in total, 5 per person. No daily loss limit, but the $2,000 max loss trails your highest balance in real time, and you must clear a fixed $2,100 buffer ($52,100) before withdrawing.",
        "Each payout needs at least $800 profit above the buffer and is capped at $1,200; you keep 80%, so about $640 to $960 per payout. A 20% perpetual consistency rule applies, news-window profits count at 40%, and the account closes after the 5th payout. No refunds or resets."],
  why="The entry price is low, but the ceiling is about $4,800 per account (5 payouts of up to $960) and the trailing drawdown is tight. Run the numbers before you buy.",
  src=[("https://help.fundednext.com/en/articles/17718088-cfds-fnl-004","FundedNext help center")]),
 dict(h="BrightFunded launches futures: BrightPlus and BrightCore",
  body=["On Oct 26, CFD firm BrightFunded opened futures evaluations. Both plans are one phase: $25K to $150K accounts, a 6% target, no daily loss limit, no time limit, a one-time fee and no activation fee.",
        "BrightPlus has an intraday drawdown and daily payouts; BrightCore has an end-of-day drawdown and pays every 5 trading days. Launch code BRIGHTFUTURES (50% off) puts the 25K at $60 (Plus) and $65 (Core)."],
  why="Another CFD brand moves into futures after FTMO did in August. More competition usually means cheaper evaluations, but check the drawdown type: intraday is much easier to breach than end-of-day.",
  src=[("https://futures-help.brightfunded.com/en/articles/17507286-what-is-brightfunded-futures","BrightFunded help center"),
       ("https://brightfunded.com/futures/how-it-works","BrightFunded: how it works")]),
 dict(h="Rule changes at Alpha Futures, Funded Futures Network and Blue Guardian",
  bullets=["<b>Alpha Futures:</b> new optional \u201cNo Consistency in Qualified\u201d add-on removes the 40% consistency rule on Standard funded accounts for +$70 / +$90 / +$110 a month (50K / 100K / 150K). The evaluation keeps its 50% rule.",
           "<b>Funded Futures Network:</b> the CEO says accounts bought after Oct 22 no longer get closed for HFT (short-trade) violations; only that day\u2019s short-trade profit is removed when those trades exceed 30% of the day\u2019s activity, per Funded Truth. Older accounts stay on the old terms.",
           "<b>Blue Guardian Futures:</b> the official rules page now lists a $5,000 end-of-day trailing max drawdown on the $150K Standard account, up from $3,500 per Funded Truth."],
  why="Almost every change applies only to accounts bought after the change date. Check your purchase date and the terms that came with it before you trade or request a payout.",
  src=[("https://alpha-futures.com/posts/alpha-futures-no-consistency-add-on-2026","Alpha Futures"),
       ("https://x.com/EthanFFNCEO/status/2115103266186862804","FFN CEO on X"),
       ("https://fundedtruth.com/prop-firm-news/funded-futures-network-softens-hft-rule-short-trades-no-longer-fail-the-account/","Funded Truth (FFN)"),
       ("https://helpfutures.blueguardian.com/en/articles/15654479-standard-account-rules","Blue Guardian rules"),
       ("https://fundedtruth.com/prop-firm-news/blue-guardian-futures-raises-standard-150k-max-drawdown-to-5000/","Funded Truth (Blue Guardian)")]),
 dict(h="Topstep: heavy account-buyers will be moved to Live",
  body=["On Oct 28, Topstep replied on X to a trader upset about being moved to Live just before a payout. It said he had taken four payouts in three weeks while buying accounts \u201cat a pace that annualizes to roughly 700 per year.\u201d",
        "\u201cIt isn\u2019t a SIM lottery. Everyone is welcome, but repeatedly cycling through accounts will eventually mean proving your strategy in Live.\u201d His XFA balances will be released into Live as he builds there. TopstepX also added Live performance stats."],
  why="Buying and cycling lots of accounts can trigger a Live call-up, which changes when and how you get paid. Read Topstep\u2019s Live transition rules before you scale up.",
  src=[("https://x.com/Topstep/status/2115501066145976393","Topstep on X"),
       ("https://fundedtruth.com/prop-firm-news/topstep-adds-live-performance-stats-on-topstepx-and-explains-calls-to-live/","Funded Truth")]),
]

quick = [
 "<b>Myth check:</b> one aggregator listed True Forex Funds as closing on Oct 29. It actually shut down in May 2024. Always check the date.",
 "<b>Futures land-grab:</b> BrightFunded joins FTMO (August) on the list of CFD-first firms now selling futures evaluations.",
 "<b>PFM fallout:</b> Prop Firm Match says it is settling the affected numbers partner by partner. We\u2019ll track who returns.",
]

def p(t, size=15, color=INK, extra=""):
    return f'<p style="margin:0 0 12px 0;{F}font-size:{size}px;line-height:1.55;color:{color};{extra}">{t}</p>'

def card(i, s):
    inner = ""
    for b in s.get("body", []): inner += p(e(b))
    if s.get("bullets"):
        inner += '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
        for b in s["bullets"]:
            inner += f'<tr><td valign="top" style="width:16px;padding:0 0 10px 0;{F}font-size:15px;line-height:1.55;color:{GREEN};">&#9656;</td><td style="padding:0 0 10px 0;{F}font-size:15px;line-height:1.55;color:{INK};">{b}</td></tr>'
        inner += '</table>'
    if s.get("note"): inner += p(e(s["note"]), 13, MUTED, "font-style:italic;")
    srcs = " &nbsp;&middot;&nbsp; ".join(link(u, l) for u, l in s["src"])
    return f'''
<tr><td class="px" style="padding:0 32px 20px 32px;">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {LINE};border-radius:8px;">
  <tr><td class="cp" style="padding:20px 22px 6px 22px;">
   <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
    <td valign="top" style="padding-right:12px;"><div style="{F}width:32px;height:32px;line-height:32px;border-radius:16px;background:{NAVY};color:#ffffff;text-align:center;font-size:15px;font-weight:bold;">{i}</div></td>
    <td valign="middle"><h2 style="margin:0;{F}font-size:18px;line-height:1.3;color:{NAVY};font-weight:bold;">{e(s["h"])}</h2></td>
   </tr></table>
  </td></tr>
  <tr><td class="cp" style="padding:12px 22px 0 22px;">{inner}</td></tr>
  <tr><td class="cp" style="padding:0 22px 14px 22px;">
   <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td style="background:#F0FDF4;border-left:4px solid {GREEN};padding:10px 14px;{F}font-size:14px;line-height:1.5;color:{INK};"><b style="color:{GREEN};">Why it matters:</b> {e(s["why"])}</td>
   </tr></table>
  </td></tr>
  <tr><td class="cp" style="padding:0 22px 18px 22px;{F}font-size:13px;line-height:1.6;color:{MUTED};"><b>Source{'s' if len(s['src'])>1 else ''}:</b> {srcs}</td></tr>
 </table>
</td></tr>'''

preview = "5 prop firm moves from this week, and what each one means for your next account."
subject = "Firms dump Prop Firm Match, a $149.99 no-challenge 50K, and Topstep\u2019s Live call-ups"

quick_html = "".join(f'<tr><td valign="top" style="width:18px;padding:0 0 10px 0;{F}font-size:15px;color:{GREEN};">&bull;</td><td style="padding:0 0 10px 0;{F}font-size:14px;line-height:1.55;color:{INK};">{q}</td></tr>' for q in quick)

doc = f'''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>{e(subject)}</title>
<style>
  @media only screen and (max-width:620px) {{
    .container {{ width:100% !important; }}
    .px {{ padding-left:16px !important; padding-right:16px !important; }}
    .cp {{ padding-left:16px !important; padding-right:16px !important; }}
    .mast-title {{ font-size:30px !important; }}
  }}
</style>
</head>
<body style="margin:0;padding:0;background:#EEF1F4;">
<!-- Hidden inbox preview text -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#EEF1F4;">{e(preview)}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#EEF1F4;">
<tr><td align="center" style="padding:16px 8px 32px 8px;">

 <!-- Demo banner / inbox preview mock -->
 <table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;">
  <tr><td style="background:#FEF3C7;border:1px dashed #D97706;border-radius:6px;padding:10px 14px;{F}font-size:12px;line-height:1.5;color:#78350F;">
   <b style="letter-spacing:1px;">DEMO &mdash; NOT SENT.</b> Preview of how Funded Tape will look. Not approved or published.<br>
   <b>Subject:</b> {e(subject)}<br>
   <b>Preview text:</b> {e(preview)}
  </td></tr>
  <tr><td style="height:12px;line-height:12px;font-size:0;">&nbsp;</td></tr>
 </table>

 <table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border-radius:10px;overflow:hidden;">

  <!-- Masthead -->
  <tr><td class="px" style="background:{NAVY};padding:28px 32px 22px 32px;">
   <div style="{F}font-size:11px;letter-spacing:2px;color:#86EFAC;text-transform:uppercase;font-weight:bold;">&#9650; Weekly prop firm briefing</div>
   <h1 class="mast-title" style="margin:6px 0 6px 0;{F}font-size:36px;line-height:1.1;color:#FFFFFF;font-weight:800;letter-spacing:-0.5px;">Funded <span style="color:#4ADE80;">Tape</span></h1>
   <div style="{F}font-size:15px;line-height:1.4;color:#CBD5E1;">The prop firm week, sourced. 5 things you can&rsquo;t miss.</div>
  </td></tr>
  <tr><td class="px" style="background:#12304D;padding:9px 32px;{F}font-size:12px;color:#CBD5E1;letter-spacing:0.5px;">
   Demo edition &nbsp;|&nbsp; Week of <b style="color:#FFFFFF;">Oct 26 &ndash; Nov 1, 2026</b> &nbsp;|&nbsp; 5 min read
  </td></tr>

  <!-- Intro -->
  <tr><td class="px" style="padding:26px 32px 8px 32px;">
   {p("Happy Sunday, traders.", 17, NAVY, "font-weight:bold;")}
   {p("It was a big week. The best-known prop firm comparison site lost a batch of partner firms, FundedNext opened a limited no-challenge 50K, BrightFunded moved into futures, and Topstep explained why heavy account-buyers get moved to Live. Here are the 5 things you can&rsquo;t miss.")}
  </td></tr>

  <tr><td class="px" style="padding:6px 32px 14px 32px;{F}font-size:12px;letter-spacing:2px;color:{MUTED};font-weight:bold;text-transform:uppercase;">This week&rsquo;s top 5</td></tr>
  {''.join(card(i+1, s) for i, s in enumerate(stories))}

  <!-- Quick hits -->
  <tr><td class="px" style="padding:4px 32px 18px 32px;">
   <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F8FAFC;border-radius:8px;">
    <tr><td style="padding:16px 20px 6px 20px;{F}font-size:12px;letter-spacing:2px;color:{NAVY};font-weight:bold;text-transform:uppercase;">&#9889; Quick hits</td></tr>
    <tr><td style="padding:6px 20px 8px 20px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{quick_html}</table></td></tr>
   </table>
  </td></tr>

  <!-- Outro -->
  <tr><td class="px" style="padding:8px 32px 8px 32px;border-top:1px solid {LINE};">
   <div style="height:18px;line-height:18px;font-size:0;">&nbsp;</div>
   {p("That&rsquo;s the week. Rules and deals change constantly, so always read the current terms on the firm&rsquo;s own page before you buy. <b>Hit reply</b> and tell us which firm we should dig into next.")}
   {p("We&rsquo;re independent. If we ever use an affiliate link, we&rsquo;ll label it.")}
   {p("See you next Sunday.<br><b style='color:"+NAVY+";'>&mdash; Funded Tape</b>")}
  </td></tr>
  <tr><td class="px" style="padding:4px 32px 26px 32px;">
   <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td style="background:#F3F4F6;border-radius:6px;padding:12px 14px;{F}font-size:12px;line-height:1.5;color:{MUTED};"><b>Not financial advice.</b> Funded Tape is for information only. Prop firm accounts are mostly simulated, and most traders do not receive a payout. Trade at your own risk.</td>
   </tr></table>
  </td></tr>

  <!-- Footer -->
  <tr><td class="px" align="center" style="background:{NAVY};padding:20px 32px;{F}font-size:12px;line-height:1.6;color:#94A3B8;">
   You&rsquo;re receiving this because you subscribed to Funded Tape.<br>
   <a href="#" style="color:#CBD5E1;text-decoration:underline;">Unsubscribe</a> &nbsp;&middot;&nbsp; <a href="#" style="color:#CBD5E1;text-decoration:underline;">Manage preferences</a> &nbsp;&middot;&nbsp; <a href="#" style="color:#CBD5E1;text-decoration:underline;">View in browser</a><br>
   [Mailing address placeholder]
  </td></tr>
 </table>

</td></tr>
</table>
</body>
</html>
'''
open(OUT, "w").write(doc)
print("wrote", OUT, len(doc))
