import html, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
URL = re.compile(r'(https?://[^\s<>"]+[^\s<>".,;:)])')
def t(s):
    s = E(s, quote=False)
    return URL.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
def p(s): return f"<p>{t(s)}</p>"
def ul(items): return "<ul>" + "".join(f"<li>{t(i)}</li>" for i in items) + "</ul>"
def ol(items): return "<ol>" + "".join(f"<li>{t(i)}</li>" for i in items) + "</ol>"
def table(cols, rows, num=()):
    h = "<table><thead><tr>" + "".join(f"<th>{E(c)}</th>" for c in cols) + "</tr></thead><tbody>"
    for r in rows:
        h += "<tr>" + "".join(f'<td{" class=num" if i in num else ""}>{t(c)}</td>' for i, c in enumerate(r)) + "</tr>"
    return h + "</tbody></table>"
def links(items): return "<ul class=links>" + "".join(f'<li><a href="{u}">{E(n)}</a> <span class=muted>{E(u)}</span></li>' for n, u in items) + "</ul>"
def callout(lead, body, cls=""): return f'<div class="callout {cls}"><strong>{E(lead)}.</strong> {t(body)}</div>'
def sec(id, h, body, lvl=2): return f'<section id="{id}"><h{lvl}>{E(h)}</h{lvl}>{body}</section>'

toc = [("tldr","The plan in one minute",0),("primer","Industry primer",0),("money","How firms make money",1),("events","Key events and regulation",1),("size","Market size",1),("audience","Audience size",0),("sources","Source map",0),("team","Bot team",0),("roadmap","Alpha to Beta roadmap",0),("demo","Demo edition (verified draft)",0),("factcheck","Fact-check log",0),("gaps","Still unverified",0)]
out = []
out.append(sec("tldr","The plan in one minute",
  callout("CEO take","The audience is real and big: about 2 million active prop traders (modeled), and single firms report millions of signups. Most of them pay for challenges, few get paid, and rules change every week. A trusted, independent weekly \"what changed and what it means for you\" email fills a gap. That gap got wider this week, when Prop Firm Match, the biggest comparison site, lost trust.") +
  ol(["Alpha (now): a free weekly text email, Top 5 things you can't miss, sent every Sunday.",
      "KFC (CEO) runs 5 watcher bots and 1 editor bot. The watchers collect Mon–Thu, the editor drafts Fri, you approve Sat, and it sends Sun.",
      "Beta (later): turn each issue into one weekly YouTube video plus 3–5 Shorts, cross-posted to TikTok, Instagram Reels and X.",
      "Our edge: we stay independent and quote sources, and we disclose any affiliate links. The PFM scandal shows why traders value this."])))

money = sec("money","How firms make money",
  p("Revenue comes mostly from challenge fees, resets and activation fees, not trading. Pass and payout rates are low, so fees from the many fund the payouts to the few. Only 4 of 10 big firms publish pass rates (PropDataLab, checked Oct 2, 2026).") +
  table(["Funnel stage","Topstep 2025","Tradeify (Aug 25–Jul 26)","FPFX Tech sample"],
   [["Evaluations passed","16.8%","17.2%","14%"],["People ever funded","51.8%","40.3%","—"],["Funded traders paid","33.3%","28.5%","45%"],["All participants paid","—","—","7%"],["Moved to live","0.71%","3.0%","—"]],num=(1,2,3)) +
  p("Goat Funded Trader's public dashboard (Oct 21, 2026) shows 594,997 people who bought a challenge and 22,279 who were paid. That is about 3.7% of buyers (our calculation), with $26.16M paid in total.") +
  links([("PropDataLab: prop firm pass rates","https://propdatalab.com/prop-firm-pass-rates/"),("Finance Magnates: Goat Funded Trader paid $26M to 22,279 of 1.2M traders","https://www.financemagnates.com/forex/prop-firm-goat-funded-trader-says-it-paid-26-million-to-22279-of-12-million-traders/")]),3)

events = sec("events","Key events and regulation",
  table(["When","Event","Notes"],[
   ["Aug 2023","CFTC sues My Forex Funds (Traders Global) for fraud; assets frozen","The firm stops operating, and it becomes the industry's big scare."],
   ["Feb 2024","MetaQuotes pulls MT4/MT5 access from prop firms serving US clients","FTMO halts US signups, and firms move to cTrader, DXtrade, Match-Trader and TradeLocker."],
   ["May 2025","Judge dismisses the MFF case with prejudice and sanctions the CFTC","The CFTC is ordered to pay more than $3M in fees."],
   ["Dec 1, 2025","FTMO completes its acquisition of broker OANDA from CVC","The biggest consolidation deal so far."],
   ["Aug 31, 2026","FTMO Futures goes live","CFD leaders are moving into futures."],
   ["Sep 28, 2026","FundedSeat announces it is closing","It blamed limited platform access."],
   ["Oct 1, 2026","CMC Markets launches CMC Funded (simulated)","A listed broker enters the space."],
   ["Oct 29–30, 2026","Major firms cut affiliate ties with Prop Firm Match","Over the affiliate-tracking allegations; PFM accepts responsibility."],
   ["Nov 23, 2026","My Forex Funds brand relaunches under a new owner","Announced Oct 21."]]) +
  callout("Regulation status","No country has a dedicated licensing regime for prop-firm evaluations as of late 2026. The US classification of simulated challenges is still unresolved, and some firms are registering voluntarily through IB/FCM structures. ESMA is not actively working on it, and ASIC's focus is CFD product rules.","warn") +
  links([("Finance Magnates: FTMO halts US client acquisition amid MetaQuotes crackdown","https://www.financemagnates.com/forex/exclusive-ftmo-halts-us-client-acquisition-amid-metaquotes-crackdown/"),
         ("Reuters: Judge sanctions CFTC in My Forex Funds case","https://www.reuters.com/legal/government/judge-sanctions-cftc-over-agencys-conduct-my-forex-funds-case-2025-05-14/"),
         ("FTMO completes acquisition of OANDA","https://ftmo.com/en/press-release/ftmo-completes-acquisition-of-oanda-from-cvc/"),
         ("Finance Magnates: FTMO founders discuss futures expansion","https://www.financemagnates.com/forex/weekly-recap-ftmo-founders-discuss-futures-expansion-plus500-pushes-guidance-higher/"),
         ("Finance Magnates: MyForexFunds assets sold; FundedSeat closes; CMC Funded","https://www.financemagnates.com/forex/weekly-review-myforexfunds-brand-assets-sold-igs-otc-revenue-retention-slips/"),
         ("Finance Magnates: MyForexFunds Evolution relaunch","https://www.financemagnates.com/forex/myforexfunds-unveils-evolution-hitting-2-drawdown-gets-you-demoted-to-intern/"),
         ("upme: Are prop firms regulated? A jurisdiction map","https://upme.com/learn/are-prop-firms-regulated/"),
         ("Finance Magnates: Prop trading slips down Paris' agenda","https://www.financemagnates.com/forex/prop-trading-slips-down-paris-agenda-as-the-us-steps-up/")]),3)

size = sec("size","Market size",
  p("All figures are third-party estimates, not audited. Do not add them together.") +
  table(["Estimate","Value","Source"],[
   ["Primary market (firm revenue), 2026","$4.0–4.5B","Octrado study, Jul 2026"],["Broader ecosystem value","$20B","Octrado study, Jul 2026"],
   ["Industry revenue incl. traditional prop, 2026","$19.4B","ProprietaryTrading.com"],["Active funded accounts, 2026","720,000","ProprietaryTrading.com"],
   ["Estimated active traders","2.15M","PropTradeCenter, Oct 2026"],["Estimated funded traders","193,000","PropTradeCenter, Oct 2026"],
   ["Monthly payout run-rate","$188.6M","PropTradeCenter, Oct 2026"],["Active firms tracked","419","PropTradeCenter, Oct 2026"]],num=(1,)) +
  links([("Octrado: Capital on Trial (PDF)","https://prop.octrado.com/documents/octrado-study-prop-trading.pdf"),("PropTradeCenter market size estimates","https://proptradecenter.com/industry-data/estimates/market-size"),("State of Prop Trading 2026","https://proprietarytrading.com/article/state-of-prop-trading-2026")]),3)

out.append(sec("primer","Industry primer",
  p("A retail prop firm, also called a funded-trader program, sells traders an evaluation, or \"challenge\". The trader pays a fee, trades a simulated account under strict rules (profit target, daily loss limit, max drawdown, sometimes a consistency rule), and if they pass, gets a \"funded\" account. They keep a share of the profits from it, usually 80–90%, sometimes 100%. Most funded accounts are still simulated. The firm pays rewards out of its own revenue, and only a few traders get moved to real live capital.") +
  ol(["Buy a challenge: one-time or monthly fee, often $50–$600 depending on size. Examples: Topstep 50K at $49/mo plus $149 activation, FTMO 1-Step $100K at €499.",
      "Pass the evaluation: 1-step or 2-step. Hit a profit target without breaking the daily or overall loss limit.",
      "Get funded (usually simulated): payout rules apply, such as buffers, minimum profitable days, consistency rules and payout caps.",
      "Request payouts: profit split of 80–100%. Some firms cap the number of payouts per account.",
      "Get called up to live (rare): in 2025, 0.71% of Topstep participants reached Live. Tradeify: 3.0%."]) +
  table(["","Futures firms","Forex / CFD firms"],[
   ["Examples","Topstep, Apex, Tradeify, MyFundedFutures, Lucid, Take Profit Trader","FTMO, FundedNext, FundingPips, The5ers, Goat Funded, Blue Guardian"],
   ["Platforms","Tradovate, NinjaTrader, Rithmic, TopstepX, TradingView","MT5 (limited), cTrader, DXtrade, Match-Trader, TradeLocker"],
   ["Typical drawdown","Dollar EOD or intraday trailing (e.g. $2,000 on 50K)","Percent of balance (e.g. 5% daily, 10% overall)"],
   ["US traders","Mostly US-focused (CME data)","Many stopped serving the US after the 2024 MetaQuotes pullback"]]) +
  p("Product lines are blurring. FTMO launched futures on Aug 31, 2026, and BrightFunded followed on Oct 26. Crypto and perpetuals firms are showing up (FFN Perps, Vest, MyFundedPerps). Brokers are entering too: CMC Markets launched CMC Funded on Oct 1, 2026.") +
  money + events + size))

bars = [("FundedNext",192807),("FundingPips",181355),("FTMO",166889),("Prop Firm Match",141076),("Goat Funded Trader",139445),("Blue Guardian",104141),("Alpha Capital",98532),("The5ers",91036),("MyFundedFutures",90057),("Topstep",89470),("Tradeify",83539),("Apex",52957)]
mx = bars[0][1]
barhtml = '<div class=bars>' + "".join(f'<div class=bar><span class=bl>{E(n)}</span><span class=bt><span class=bf style="width:{v/mx*100:.1f}%"></span></span><span class=bv>{v/1000:.1f}K</span></div>' for n,v in bars) + '</div>'
out.append(sec("audience","Audience size",
  p("Our best estimate of the reachable audience is about 2 million active prop traders worldwide. That is a modeled figure, and firm-reported signups are higher because people sign up at several firms.") +
  '<div class=metrics>' + "".join(f'<div class=metric><div class=mv>{a}</div><div class=ml>{b}</div><div class=md>{c}</div></div>' for a,b,c in [("2.15M","Active prop traders","PropTradeCenter model, Oct 2026"),("4.5M+","FTMO registered customers","Firm-reported"),("1.2M","Goat Funded signups","595K bought a challenge"),("3M","FundingPips traders","Firm X bio, self-reported")]) + '</div>' +
  table(["Firm-reported figure","Value","Source"],[
   ["FTMO cumulative rewards","$650M+","Finance Magnates, Sep 2026 figures"],["FTMO rewards in Sep 2026","$14.4M, about 7,100 payouts","Finance Magnates"],
   ["Topstep paid all-time","$1.5B+","https://www.topstep.com/"],["Topstep traders paid weekly","7,000+","https://www.topstep.com/"],
   ["FundedNext cumulative payouts","$350M+ (unaudited)","Finance Magnates"],["Tradeify payouts","$300M+","Tradeify X bio"],
   ["cTrader prop ecosystem","500,000+ traders, 40+ firms","Octrado, citing cTrader"],["Prop Firm Match reach","25M+ visits in 3 years, 370K+ members","PFM X post, Oct 30, 2026, self-reported"]]) +
  "<h3>Official firm X followers (checked Nov 1, 2026)</h3>" + barhtml +
  "<h3>Community sizes</h3>" +
  table(["Community","Members","As of / source"],[
   ["FundingPips Discord","254,616","Oct 4, 2026, BestProps"],["FundedNext CFD Discord","254,550","Oct 4, 2026, BestProps"],["Lucid Trading Discord","195,714","Oct 4, 2026, BestProps"],
   ["Topstep Discord","190,872","Oct 4, 2026, BestProps"],["Tradeify Discord","154,134","Oct 4, 2026, BestProps"],["FTMO Discord","136,384","Oct 4, 2026, BestProps"],
   ["MyFundedFutures Discord","132,663","Oct 4, 2026, BestProps"],["r/Daytrading (broad)","5.2M","GummySearch"],["r/Forex (broad)","556K","GummySearch"],
   ["r/FuturesTrading (broad)","205K","GummySearch"],["r/Forexstrategy","155K","GummySearch"],["r/propfirm","42K, +1,484% in 12 months","KissMyPost, Oct 2026"],
   ["r/ApexTraderFunding","about 4,750","Reddit post, Aug 2026"],["r/PropFirms","about 3,000","GummySearch, Oct 27, 2026"]],num=(1,)) +
  p("Discord member counts overlap heavily, since one trader is often in 5–10 servers. Treat them as reach per channel, not unique people.") +
  links([("Finance Magnates: FTMO monthly rewards near $15M","https://www.financemagnates.com/forex/ftmo-adds-200-million-to-lifetime-payouts-in-one-year-as-monthly-rewards-near-15-million/"),
         ("BestProps: prop firm Discord servers checked","https://bestprops.com/best-prop-firms-with-discord-trader-communities/"),
         ("KissMyPost: r/propfirm stats","https://kissmypost.com/subreddit/propfirm"),("GummySearch: r/Daytrading","https://gummysearch.com/r/Daytrading/")])))

def xl(h): return f"https://x.com/{h}"
src = (
 "<h3>Official firm X accounts (verified Nov 1, 2026)</h3>" +
 table(["Firm","Handle","Type"],[
  ["FTMO",xl("FTMO_com"),"CFD + futures"],["Topstep",xl("Topstep")+" · "+xl("AskTopstep")+" · "+xl("TopstepTV"),"Futures"],["Apex Trader Funding",xl("ApexTradeFund"),"Futures"],
  ["FundedNext",xl("FundedNext"),"CFD + futures"],["FundingPips",xl("fundingpips"),"CFD"],["The5ers",xl("the5erstrading"),"CFD"],
  ["Goat Funded Trader",xl("GoatFunded"),"CFD + futures"],["Tradeify",xl("Tradeify"),"Futures + FX"],["MyFundedFutures",xl("MyFundedFutures"),"Futures"],
  ["Alpha Capital Group",xl("AlphaCapitalUK"),"CFD"],["Blue Guardian",xl("BlueGuardiancom"),"CFD + futures"],["E8 Markets",xl("E8Markets"),"CFD + futures"],
  ["Earn2Trade",xl("earn2trade"),"Futures"],["Funded Futures Network",xl("FFNFunding")+" (CEO "+xl("EthanFFNCEO")+")","Futures + perps"]]) +
 p("Dropped as wrong or inactive: @The5ers (an unrelated radio account), @AlphaCapitalGrp, @AlphaCapGroup, @LucidTrading, @TradeDay, @TakeProfitTrdr, @TakeProfitTradr. Still to find: the official handles for Take Profit Trader, Lucid Trading and TradeDay.") +
 "<h3>Official update pages (firm-announcements watcher)</h3>" +
 links([("FTMO CFD trading updates","https://ftmo.com/en/blog/trading-updates/trading-update-8-oct-2026/"),("FTMO Futures trading updates","https://ftmo.com/en/futures/trading-updates/"),
        ("FundedNext help center (FNL:004)","https://help.fundednext.com/en/articles/17718088-cfds-fnl-004"),("BrightFunded Futures help center","https://futures-help.brightfunded.com/en/articles/17507286-what-is-brightfunded-futures"),
        ("Blue Guardian Futures Standard rules","https://helpfutures.blueguardian.com/en/articles/15654479-standard-account-rules"),("Alpha Futures posts","https://alpha-futures.com/posts/alpha-futures-no-consistency-add-on-2026"),("Topstep","https://www.topstep.com/")]) +
 "<h3>News, change logs and data</h3>" +
 links([("Finance Magnates (forex)","https://www.financemagnates.com/forex/"),("Funded Truth prop firm news","https://fundedtruth.com/prop-firm-news/"),("FundedYield change log, Oct 2026","https://fundedyield.com/en/changelog/2026-10"),
        ("PYE Markets weekly rule changes","https://proveyouredge.com/articles/prop-rules-weekly-2026-10-23"),("Prop Firm Loop updates","https://propfirmloop.com/updates/"),("PropTraderz October roundup","https://www.proptraderz.com/prop-firm-rule-changes-october-2026/"),
        ("TheGodFunded news","https://thegodfunded.com/en/news/brightfunded-launches-futures-brightplus-brightcore/"),("Payout Junction on X","https://x.com/payoutjunction"),("PropDataLab","https://propdatalab.com/prop-firm-pass-rates/"),
        ("PropTradeCenter","https://proptradecenter.com/industry-data/estimates/market-size"),("BestProps","https://bestprops.com/best-prop-firm-youtube-channels-and-reviewers/")]) +
 p("Also: the PropScorer change log (from KFC's notes; no URL recorded).") +
 "<h3>Review and comparison sites</h3>" +
 ul(["Prop Firm Match (https://propfirmmatch.com/): biggest site, 141K X followers. Under an affiliate-tracking cloud since Oct 29, so track it as news, not as a neutral source.",
     "Trustpilot firm pages: ratings move a lot, and several are hidden behind guideline-breach banners (Alpha Capital, Blue Guardian, Goat Funded, E8, For Traders).",
     "Prop Firm Bridge (https://x.com/PropFirm_Bridge), Trusted Prop Hub (https://x.com/TrustedPropHub), DamnPropFirms (https://x.com/DamnPropFirms), Prop Firm Loop: all affiliate-funded, so disclose that when we cite them."]) +
 "<h3>X creators and commentators</h3>" +
 table(["Handle","Followers","Why watch"],[[xl("DodgysDD"),"99.1K","Big trading account, prop content"],[xl("arjoio"),"79.3K","Prop firm commentary"],[xl("traderkane"),"62.3K","Broke the PFM story; bio says he is building @propfirm"],
  [xl("tradernickfx"),"45.2K","Macro/forex educator"],[xl("TradesByMatt"),"35.5K","Futures (NQ)"],[xl("TrustedPropHub"),"20.6K","Prop news aggregator"],[xl("TheH0n3stTrader"),"18.3K","Payout tactics"],
  [xl("NickDoesFutures"),"16.5K","Futures prop reviews (code NICK)"],[xl("LSPTrades"),"7.0K","Futures streamer"]],num=(1,)) +
 "<h3>YouTube creators</h3>" +
 table(["Channel","Subscribers","Focus"],[["JeaFx https://www.youtube.com/@JeaFxForexTrading","793K","Forex, prop funding"],["Oliver Velez https://www.youtube.com/@OliverVelezTrading","446K","Trader education"],
  ["Trades by Matt https://www.youtube.com/@TradesbyMatt","238K","Futures, prop accounts"],["Dan Cheung https://www.youtube.com/@DanCheung","123K","Forex prop challenges"],
  ["Mindfully Trading https://www.youtube.com/mindfullytrading","84.1K","Forex day trading"],["Forex Prop Reviews https://www.youtube.com/@ForexPropReviews","46.1K","Prop firm reviews"],
  ["Trade Connect VVS https://www.youtube.com/@TradeConnectVVS","38.9K","Interviews with prop firm owners"],["Prop Firm Checker (channel URL from Feedspot returned 404; find the current one)","17.9K","Prop firm reviews"],
  ["NickDoesFutures, Damn Good Trading","not checked","Top-rated reviewers in BestProps' audit"],["Official: TopstepTV, MyFundedTV, Tradeify TV, FTMO","Topstep 200K+","Rule explainers, live streams"]],num=(1,)) +
 p("Subscriber counts are from Feedspot (Jul 2026): https://videos.feedspot.com/prop_trading_youtube_channels/") +
 "<h3>Instagram and TikTok</h3>" +
 ul(["Dan Cheung: 256.7K Instagram (Feedspot).","Oliver Velez: 187.2K Instagram (Feedspot).","PJ Trades: 258K Instagram, 194K TikTok, 49.9K-member Discord (https://www.marketframework.com/traders/pj-trades).","Forex Prop Reviews: 46.8K Instagram (Feedspot).","Next step: the social watcher builds a hashtag list for #propfirm, #fundedtrader, #ftmo and #topstep on TikTok and Reels."]) +
 "<h3>Reddit, Discord and Telegram</h3>" +
 ul(["Reddit: https://www.reddit.com/r/propfirm, https://www.reddit.com/r/PropFirms, https://www.reddit.com/r/Daytrading, https://www.reddit.com/r/FuturesTrading, https://www.reddit.com/r/Forex, https://www.reddit.com/r/Forexstrategy, https://www.reddit.com/r/TopstepCommunity (official Topstep), https://www.reddit.com/r/ApexTraderFunding.",
     "Discord: official servers of FundingPips, FundedNext (CFD and futures), Topstep, Lucid, Tradeify, FTMO, MyFundedFutures, Goat Funded, Alpha Capital and Blue Guardian. Only use invites taken from each firm's own site.",
     "Telegram: https://t.me/FundedNextOfficialCommunity (61K), https://t.me/FXIFYCOM, https://t.me/blueguardiancapital."]) +
 "<h3>Competitor newsletters</h3>" +
 ul(["Prop Traders Weekly (https://www.proptraders.io/subscribe), by Kieran Gohil: free, Mondays, 131+ issues. Subscriber count not public.","Prop Weekly (https://propweekly.com/newsletter): payouts and firms entering or leaving.","Prop Traders Club (https://proptraders.club/): 1–3 updates a week."]) +
 "<h3>KFC's source notes from the first run</h3>" +
 ul(["Reddit returned 403 to automated reads, and propfirmmatch.com is behind Cloudflare. Both need an approved API or a browser-based watcher.",
     "Most useful sources: Finance Magnates, Funded Truth, the PropScorer and FundedYield change logs, firm help pages, and X.",
     "Watch out for stale aggregator entries. One listed True Forex Funds as closing Oct 29, 2026, but it actually closed in May 2024.",
     "Lesson from the fact-check: firm pages sometimes contradict each other. BrightFunded lists a $250 minimum payout in its help center and $500 on its marketing page, so cite the help center and flag any conflict."]))
out.append(sec("sources","Source map",src))

out.append(sec("team","Bot team",
  table(["Bot","Owns","Main sources"],[["KFC (CEO)","Plans, assigns, QA, final pick of the Top 5","All watcher logs"],["X Watcher","Firm and creator X accounts","Handles in the source map"],
   ["Firm Watcher","Help pages, rule pages, change logs","Firm help centers, FundedYield, PYE, Prop Firm Loop"],["News Watcher","Industry news and payouts","Finance Magnates, Funded Truth, Payout Junction"],
   ["Community Watcher","Reddit, Discord, Trustpilot sentiment","Subreddits, official Discords"],["Video/Social Watcher","YouTube, TikTok, Instagram","Creators in the source map"],["Editor/Writer","Top 5 draft and fact check","Watcher logs, primary sources"]]) +
  p("Reporting line: you (pomo651) approve and publish, KFC manages the 5 watchers, the watchers feed the editor, and the editor sends the draft back to KFC.") +
  table(["Day (PT)","Who","Output"],[["Mon–Thu","5 watchers","Daily log: date, firm, what changed, link, confidence"],["Thu PM","KFC","Shortlist of 8–10 items, ranked by trader impact"],
   ["Fri","Editor","Top 5 draft and subject lines; every claim gets a source link"],["Fri PM","KFC","Fact-check pass: confirm on the firm's own page, drop stale items"],
   ["Sat","You","Approve or edit (nothing sends without you)"],["Sun AM","Platform","Send; KFC logs opens and clicks"]]) +
  p("Editorial rules: confirm every rule change on the firm's own page, mark anything else as unconfirmed, date every item, and disclose any affiliate link.")))

out.append(sec("roadmap","Alpha to Beta roadmap",
  table(["Phase","When","Milestone","Metric"],[["Alpha 0","Nov 2026","Demo issue approved; name and platform picked","Issue shipped"],["Alpha 1","Nov–Dec 2026","4 weekly issues; X account plus a thread per issue","500 subscribers, 45%+ open rate"],
   ["Alpha 2","Jan–Feb 2027","Referral program, reader polls, firm changelog page","2,000 subs, 5%+ click rate"],["Beta","Mar 2027+","Weekly YouTube video plus 3–5 Shorts, cross-posted","1,000 YT subs, 10K Shorts views/wk"]]) +
  p("The subscriber and engagement targets are our own goals, not benchmarks.") +
  table(["Platform","Strengths","Watch-outs"],[["Beehiiv","Built for newsletter growth: referral program, ad network, web archive","Paid tiers for growth tools"],
   ["Substack","Free to start, built-in discovery network, easy paid subs","Takes a cut of paid subscriptions; less control over branding"],["Kit (ConvertKit)","Strong automations and tagging, creator commerce","Less built-in discovery"]]) +
  p("Recommendation: Beehiiv for Alpha, because of growth tools and referrals. Pricing was not checked in this session.")))

demo_txt = open(os.path.join(ROOT, "editions", "2026-10-26_11-01-demo.txt")).read()
out.append(sec("demo","Demo edition (verified draft)",
  callout("Draft, not yet approved or published","Nothing has been sent. Facts were checked against the sources on Nov 1, 2026 (PT). \"Funded Tape\" is a working name only [name TBD].","warn") +
  p("This is the plain-text version, exactly as saved in demo-edition-2026-10-26_11-01.txt.") +
  f'<pre class=email>{t(demo_txt)}</pre>'))

out.append(sec("factcheck","Fact-check log",
  p("Changes from KFC's draft after checking sources on Nov 1, 2026.") +
  table(["Item","What changed"],[
   ["1","The quote's source is now PFM's Oct 30 statement post (https://x.com/PropFirmMatch/status/2116352044495765821). The earlier link was its Oct 29 'looking into it' post."],
   ["1","Added @traderkane's original Oct 29 post as a source, plus a one-line disclosure of his @propfirm project."],
   ["2","Corrected: $800–$1,200 is the profit per payout before the 80% split, so the trader receives about $640–$960. Added the 5-per-person cap, the news-profit 40% rule, and no refunds or resets."],
   ["2","Dropped the comparepropfirms.com roundup; cited the firm's own help page only."],
   ["3","Confirmed on BrightFunded's own pages. Added the drawdown types, payout cadence and launch code. The TheGodFunded link was replaced with the firm's own pages."],
   ["4","FFN: 'on or after Oct 22' corrected to 'after 10/22', per the CEO's own X post. Added the 30% short-trade profit rule and the fact that old accounts are still enforced."],
   ["4","Alpha Futures: confirmed, with add-on prices added."],
   ["4","Blue Guardian: the $5,000 figure is now confirmed on the official help page, so it is no longer headline-only. The earlier $3,500 figure is attributed to Funded Truth."],
   ["5","Confirmed against Topstep's X post; added the XFA release detail."]])))

out.append(sec("gaps","Still unverified",
  ul(["FundedNext FNL:004: the help page doesn't give a launch date (it was last modified Oct 28), and I didn't check whether seats remain.",
      "Blue Guardian: the earlier $3,500 value on the $150K account comes from Funded Truth only. No archived copy of the official page was checked.",
      "FFN: the new 30% rule wording is from Funded Truth and PropTraderz. The firm's own rules page wasn't opened.",
      "BrightFunded: the minimum payout conflicts between its pages ($250 in the help center, $500 on the how-it-works page), so it is left out of the edition.",
      "Subreddit sizes come from third-party trackers (GummySearch, KissMyPost) because Reddit blocked direct reads. YouTube and Instagram counts are from Feedspot, Jul 2026.",
      "Firm payout and trader totals are self-reported and unaudited. FundingPips' '3M traders' is from its X bio only."])))

tochtml = '<nav class=toc><h2>Contents</h2><ol>' + "".join(f'<li class="d{d}"><a href="#{i}">{E(l)}</a></li>' for i,l,d in toc) + '</ol></nav>'
css = """
:root{--ink:#1d1d1f;--muted:#6b6b70;--line:#e3e3e6;--soft:#f6f6f8;--accent:#1f5fbf;--warn:#fff6e0;--warnline:#e0b84a}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:#fff;color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:820px;margin:0 auto;padding:32px 20px 80px}
header.top{border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:24px}
.ver{display:inline-block;font-size:13px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}
h1{font-size:32px;line-height:1.2;margin:6px 0 8px}h2{font-size:24px;margin:40px 0 12px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:18px;margin:28px 0 8px}p{margin:10px 0}.muted{color:var(--muted);font-size:13px;word-break:break-all}
a{color:var(--accent);word-break:break-word}table{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px}
th,td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}th{background:var(--soft);font-weight:600}
td.num{text-align:right;white-space:nowrap}.callout{background:var(--soft);border-left:4px solid var(--ink);padding:12px 14px;margin:14px 0;border-radius:4px}
.callout.warn{background:var(--warn);border-left-color:var(--warnline)}.toc{background:var(--soft);padding:12px 18px;border-radius:6px}
.toc h2{border:0;margin:4px 0 6px;font-size:18px;padding:0}.toc ol{margin:0;padding-left:20px}.toc li.d1{margin-left:18px;list-style:circle}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:14px 0}
.metric{border:1px solid var(--line);border-radius:6px;padding:10px 12px}.mv{font-size:24px;font-weight:700}.ml{font-weight:600}.md{color:var(--muted);font-size:13px}
.bars{margin:10px 0}.bar{display:flex;align-items:center;gap:8px;margin:4px 0;font-size:14px}.bl{flex:0 0 150px}.bt{flex:1;background:var(--soft);height:14px;border-radius:3px;overflow:hidden}
.bf{display:block;height:100%;background:var(--accent)}.bv{flex:0 0 60px;text-align:right}
ul.links{padding-left:20px}ul.links li{margin:4px 0}
pre.email{white-space:pre-wrap;word-wrap:break-word;background:#fbfbfc;border:1px solid var(--line);border-radius:6px;padding:16px;font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
footer{margin-top:48px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:12px}
@media print{body{font-size:11pt}main{max-width:none;padding:0}a{color:var(--ink);text-decoration:underline}
h2{break-after:avoid}h3{break-after:avoid}table,.callout,.metric,.bar{break-inside:avoid}tr{break-inside:avoid}.toc{background:none;border:1px solid var(--line)}
.bf{-webkit-print-color-adjust:exact;print-color-adjust:exact}pre.email{break-inside:auto}@page{margin:16mm}}
"""
doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prop Firm Newsletter: CEO Plan, Version 1 (Nov 1, 2026)</title><style>{css}</style></head>
<body><main>
<header class=top><span class=ver>Version 1 — Nov 1, 2026</span><h1>Prop Firm Newsletter: CEO Plan</h1>
<p>What the prop firm industry is, how many traders we can reach, where the news comes from, which bots watch which sources, and the fact-checked demo of the weekly Top 5 email. Prepared by Drew with KFC (project CEO bot). Times are Pacific (PT).</p></header>
{tochtml}
{''.join(out)}
<footer>Version 1 — Nov 1, 2026. A static snapshot; figures are as of the dates shown and are not live. Not financial advice.</footer>
</main></body></html>"""
open(os.path.join(ROOT, "plan", "prop-firm-ceo-plan-v1.html"), "w").write(doc)
print(len(doc))
