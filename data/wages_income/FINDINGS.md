# FINDINGS - wages and income (BFS)
Key point: no BFS table gives wages/income/poverty for Romanian nationals. Closest proxies below. All values from files opened this session.

## Table: indicator | available for Romania? | closest official proxy | latest value | table ID / URL
| Indicator | Romania? | Closest proxy | Latest value | Source |
|---|---|---|---|---|
| Median gross monthly wage (standardised) | No | Foreigners with B permit (79% of Romanians hold B) | 2024: CHF 5 834 (B), 6 559 (C), 5 184 (L), 6 314 (G), 6 235 all foreigners, 7 480 Swiss, 7 024 total | STAT-TAB px-x-0304010000_203 |
| Wage by sector | No | B-permit holders by NOGA division | see table below | px-x-0304010000_206 |
| Poverty rate by nationality | No | "Uebrige Laender" group | 2021: 19.4% (+/-4.5) vs 13.2% foreigners, 7.2% Swiss | je-d-20.03.02.01.01 (asset 24205291) |
| At-risk-of-poverty rate / median equivalised income by nationality group | Not located (only total / foreign / Swiss seen elsewhere) | - | - | not found |
| Wage index, CPI | n/a (national) | Swiss wage index, CPI | 2022: nominal index 2468 (1939=100), +0.9%; CPI +2.8%; real -1.9% | asset 24745551 |

## Bullets
- Median 2024, all Switzerland, total sexes: Swiss 7 480; foreigners 6 235 (-16.6%); B 5 834 (-22.0% vs Swiss); C 6 559; L 5 184; G 6 314; Andere 5 003; overall 7 024 CHF. (px-x-0304010000_203)
- B-permit median 2012 -> 2024: 5 768 -> 5 834 (+1.1% nominal in 12 years); Swiss 6 720 -> 7 480 (+11.3%); foreigners 5 797 -> 6 235; C 5 788 -> 6 559. B/Swiss ratio fell from 0.86 (2012) to 0.78 (2024). Full B series: 2012 5768, 2014 5596, 2016 5641, 2018 5629, 2020 5769, 2022 5743, 2024 5834.
- B permit 2024 by sex (Switzerland): women 5 475, men 5 971. By region 2024 (women/men): Zuerich 5 935/6 449; Nordwestschweiz 5 953/6 032; Region lemanique 5 709/5 993; Zentralschweiz 5 890/6 076; Espace Mittelland 5 022/5 508; Ostschweiz 4 896/5 706; Ticino 4 771/5 517.
- Sector medians 2024, Switzerland, columns Swiss / all foreigners / B / C (CHF): Food manufacturing (div 10) 5 947/5 039/4 719/5 400; Secondary sector production total 7 236/6 414/6 054/6 638; Building construction (41) 7 221/6 416/6 044/6 699; Civil engineering (42) 7 413/6 879/6 521/7 065; Finishing trades (43) 6 862/6 174/5 769/6 520; Road transport (49) 7 092/5 804/5 284/6 384; Warehousing (52) 6 645/5 606/5 329/5 894; Post/courier (53) 6 398/5 344/5 004/5 685; Hotels (55) 5 228/4 571/4 542/4 911; Restaurants (56) 5 129/4 566/4 432/4 791; Retail (47) 5 350/5 013/4 860/5 123; Temp agencies (78) 6 260/5 843/5 764/6 174; Building services/gardening (81) 6 198/4 588/4 352/4 822; Health (86) 7 221/7 190/7 028/7 202; Residential care (87) 6 460/5 642/5 135/5 675; Social work (88) 7 014/5 910/5 312/5 929.
- Total in these divisions: Swiss 7 480, B 5 834. Agriculture (NOGA 01-03) not in LSE.
- Poverty (absolute, SILC): 2021 Swiss 7.2%, foreigners 13.2%, N/W Europe 7.6%, S Europe 10.1%, other countries 19.4% (95% CI +/-4.5pp); other countries = 10.3% of population but 22.9% of poor. 2012: 6.3/9.8/12.9% for N-W/S/other. Full 2007-2021 in CSV.
- Wage index: nominal 2010 2 284 -> 2022 2 468 (1939=100); CPI change 2010 0.7, 2011 0.2, 2012 -0.7, 2013 -0.2, 2014 0.0 (-0.0132 as stored), 2015 -1.1, 2016 -0.4, 2017 0.5, 2018 0.9, 2019 0.4, 2020 -0.7, 2021 0.6, 2022 2.8 %. Real wage index peaked 2020 (324) and fell to 315 in 2022 (-1.9%).

## Not published / not available
- Wage, income or poverty by individual nationality (Romania): not published in STAT-TAB or the files opened; LSE only Swiss/foreign/permit.
- LSE "Lohn nach Nationalitaetengruppe" (e.g. Osteuropa): not found in STAT-TAB (only 13 px-x-0304010000_* tables, none by nationality group).
- Wage index and CPI are NOT in STAT-TAB (catalogue of 633 tables has none); only the 1939-2022 xlsx was reached. Years 2023-2025 NOT done (CPI index level, SLI base 2020 not extracted). SILC at-risk-of-poverty rate and median equivalised income by nationality group: not found/not done; the poverty file is absolute poverty to 2021 only.

## Unverified leads (search snippets, not in CSVs)
- BFS press: Swiss Wage Index 2024 nominal +1.8% (104.2, base 2020=100), real +0.7% (97.6); 2025 nominal +1.8% (106.1), real +1.6% (99.2). Pages: https://www.bfs.admin.ch/bfs/rm/home.gnpdetail.2025-0075.html and https://www.bfs.admin.ch/bfs/de/home/aktuell/neue-veroeffentlichungen.assetdetail.36503586.html. verified=no (search snippet).
- Snippet: 2024 overall at-risk-of-poverty rate 16.4% (verified=no).

## Blocked hosts I would need
- None blocked. (www.pxweb.bfs.admin.ch / dam-api OK; dam-api "query" search parameter is ignored.)

## Cross-checks done
- CPI change 2022 (2.8%) and real wage change (-1.9%) match the BFS press snippet for 2022 (+0.9% nominal, -1.9% real): match. Median totals in 203 vs 206 for 2024 total (7 024) and Swiss (7 480): match.
