# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/1372755394-ai/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/1372755394-ai/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page summing up Friday 20 November 2026 in one 1024×1024 image: Anthropic's record IPO debut (+17% to $97.17 after opening at $111.50), the $1,101-point Dow rout that swallowed the celebration, Nvidia's sixth straight fall, a near-certain December Fed hike, the first-ever Trump–Xi–Putin trilateral in Shenzhen, and the wars in the Gulf, Ukraine and Gaza — with every headline and figure rendered as crisp text around an AI-generated illustration.

## Stories on the page

- **Lead — Anthropic up 17% on debut.** Opened at $111.50 (+34% on the $83 offer), intraday high $115.10, briefly over $2tn fully diluted; closed $97.17 (+17%), ~$1.76tn; 813m+ shares traded, a debut volume record. Sources: Reuters via TechDefused, New York Post, AsiaToday, The Fault Line.
- **Markets ticker — Dow −1,101.11 (−2.19%) to 49,097.06**, first close below 50,000 since June; S&P 500 −2.02% to 7,175.83, sixth straight loss; Nasdaq −2.25% to 23,879.20, lowest since April; gold ~$3,675, a 14-month low. Sources: CNBC via VIRA Broadcasting, Longbridge, TechFlowPost, Finnhub.
- **Nvidia — sixth straight fall to $145.98 (−3.30%)**, ~28% off November highs; H200 shipments to China halted; AMD −7.72% after short seller Hunterbrook disclosed a position. Sources: Longbridge, TechFlowPost, Swingfolio, The Apex Wire.
- **The Fed — December hike ~95% priced in.** CME FedWatch ~95% for a 25bp rise on Dec 8–9; Gov. Waller floated 50bp and speaks Friday 8:25am ET. Sources: Finwire, The Market Periodical, PropTraderz.
- **APEC · Shenzhen — Trump, Xi, Putin sign declaration.** First-ever trilateral, ~90 minutes at Kylin Villa; four-point "Declaration Toward Peace": nuclear war cannot be won, dialogue on nuclear risk, more refined petroleum output, UN reform, ICC must not abuse jurisdiction; Ukraine not mentioned. Sources: USA Today, Council on Foreign Relations, MarketFlux.
- **The Gulf — Iran drones hit Kuwait, Bahrain.** Tehran answers the US strike on an IRGC missile site on Qeshm Island; an ADNOC tanker hit in Hormuz, 11 crew hurt, one missing. Sources: Bloomberg via BusinessMirror, KhabarWire, The Curtain.
- **Ukraine — Kerch bridge hit a third time.** Neptune missiles hit the rail section overnight 19 Nov, train traffic halted, one track reopened ~4pm; Putin rejects a ceasefire as US envoys meet Zelenskyy in Berlin. Sources: Associated Press via WPTF/Bury Times, The Level Report.
- **Gaza — tanks cross the Yellow Line.** First publicly announced ground operation since the Oct 2025 truce; three killed; Board of Peace report warns the truce may collapse; 1,650+ killed since the ceasefire. Sources: Dawn via Kabul News, The Mary Sue, ReliefWeb.
- **Also — GTA VI: ~19m copies, $1.84bn by launch day** (Sensor Tower estimate, no official Take-Two figure); Bitcoin ~$62,000; 10-yr yield ~5.05%. Sources: USA Today, ItsBizKit, Finwire.

Every figure above was checked against live news on the morning of 20 November 2026 (Beijing time); nothing was invented.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, stdlib only) copies the committed `entry.png` to the output directory and verifies the copy is byte-identical, under 1 MiB, exactly 1024×1024, and a whole PNG. Rebuild the image itself with `python3 build_frontpage.py` (needs PIL and the hero illustration in `assets/`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=qajetvf4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
