# FINDINGS - romania_links (accessed 2026-11-14)

Verified (files opened in this session)
- Swiss citizens with a Romanian second citizenship (permanent resident pop. 15+, SE estimate): 2015 2 858; 2016 2 866; 2017 3 295; 2018 3 206; 2019 3 508; 2020 3 594 (95% CI half-width 15-18%). Source: https://dam-api.bfs.admin.ch/hub/api/dam/assets/20964155/master (CSV in folder).
- 2020 by sex: 1 490 men, 2 104 women (men 2020 CI +-24%). Women outnumber men every year 2015-2020 (e.g. 2017: 906 men vs 2 389 women, men flagged "use with caution").
- Romania is therefore listed in the BFS dual-citizenship dataset (code 8232) for 2015-2020; for 2010-2014 only the total of dual citizens is published (2010: 1 011 879; 2014: 1 119 144 Swiss with a second citizenship, all countries).
- Growth 2015->2020 of Romanian-second-citizenship Swiss: +736 (+26%, within wide confidence intervals).
- Census 2000: 3 394 residents (civil-law residence) named Romanian as main language in Switzerland: 741 Swiss citizens + 2 653 foreigners (1 495 589 foreigners and 7 287 357 total residents). Source px-x-4003000000_123 (CSV census2000_romanian_main_language_by_canton.csv, 26 cantons).
- The Strukturerhebung 2010-2020 publishes "Rumänisch" only graphically among the most frequent non-national languages (BFS Sprachenlandschaft 2022, charts G2.9-G2.12; text: in the Italian-speaking region Romanian rose by +0.2 pp 2010-2020). The canton xls 2015 has only DE/FR/IT/RM/EN/Other: no Romanian speaker count per year/canton is published in the files I could open.
- Swiss citizens in Romania: BFS file on Swiss Abroad 2024 contains no country detail. A search snippet (EDA country page) says 709 at end 2024: UNVERIFIED (see leads).
- EDA www.eda.admin.ch pages return HTTP 403 (Akamai "Access Denied") to curl for every URL tried (de/en, bilateral page, Swiss contribution); europa.eda.admin.ch and schweiz-rumaenien.eda.admin.ch blocked by proxy. So items 1, 2, 5 could NOT be verified.

## Not published / not available
- Dual nationals by Romania before 2015 and after 2020 (not in files found; newer SE releases not located).
- Romanian main-language speaker counts 2010+ (numbers) - only chart percentages.
- Swiss citizens in Romania per year (EDA/BFS Auslandschweizerstatistik) - not retrievable here.
- Votes of Romanians in Switzerland and polling-station counts - only on Romanian hosts (blocked).

## Unverified leads (search snippets, NOT in CSVs)
- EDA bilateral page (de): https://www.eda.admin.ch/countries/romania/de/home/bilaterale-beziehungen/in-kuerze.html (also .../eda/de/home/vertretungen-und-reisehinweise/rumaenien/bilatereale-beziehungenschweizrumaenien.html): reported 709 Swiss in Romania end 2024 (snippet).
- Second Swiss contribution to Romania: CHF 221.5 million, 11 thematic programmes until end 2029; framework agreement signed Dec 2022 in Bucharest, five implementation agreements 20 Feb 2025; focus energy efficiency, dual education, interior/justice, health, social inclusion (Roma), civic participation (snippet; URLs: https://www.eda.admin.ch/countries/romania/de/home/schweizer-beitrag/second-swiss-contribution/projekte.html and https://www.europa.eda.admin.ch/de/laender-zweiter-schweizer-beitrag). First (enlargement) contribution amount/projects not seen.
- EDA Auslandschweizerstatistik table "Zahl der Auslandschweizer nach Wohnsitzland" 2016-2025: https://www.eda.admin.ch/eda/de/home/leben-im-ausland/schweizerinnen-und-schweizer-im-ausland/die-fuenfte-schweiz/statistiken.html
- Media only (not official): Switzerland 1 336 voters (round unknown), 8 polling stations in Switzerland and 555 postal-vote requests for the Nov 2024 presidential round 1 (Forbes.ro / press; to be verified on https://prezenta.roaep.ro and https://www.roaep.ro ). May 2025: 965 polling stations abroad total; no Swiss figure.
- SEM figure quoted by Newsweek.ro: 43 942 Romanians at 31 Jul 2025, 39 654 permanent: not checked here (another agent covers SEM).
- BNR remittances from Switzerland: nothing found.

## Blocked hosts I would need (priority)
1. prezenta.roaep.ro / https://www.roaep.ro - polling-station level results abroad (Switzerland votes and number of sections) for presidential 2014, 2019, Nov 2024 (annulled), May 2025 (2 rounds), parliamentary 2020, 2024.
2. https://www.bec.ro (Biroul Electoral Central) - final results by country "Elveția" (2024 annulment round; 2025).
3. https://www.mae.ro - number of polling stations in Switzerland (Bern, Zürich, Geneva, Lausanne, Basel...), consular statistics/estimates of Romanian community in Switzerland, registered postal-vote requests.
4. https://www.bnr.ro - balance of payments / workers' remittances by country (Switzerland).
5. https://www.insse.ro and https://dprp.gov.ro - Romanian emigration statistics, Romanians abroad estimates.
6. Also (Swiss) www.eda.admin.ch is up at proxy level but 403 from Akamai: bilateral facts, Swiss contribution, Auslandschweizerstatistik.

## Cross-checks done
- Dual-citizen totals (Total row) 2010-2014 are consistent in order of magnitude with BFS statements (approx. 19% of Swiss 15+ in 2020 per search snippet; not verified in file).
- Men+women = total within 1 person for each year 2015-2020 (match).
- Census 2000: Swiss + foreign Romanian speakers = 741 + 2 653 = 3 394 (match with total).
- Not compared with the STATPOP reference extract (2010+ Romanian nationals) - different concept (nationality vs second citizenship of Swiss).
