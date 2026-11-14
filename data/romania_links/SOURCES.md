# SOURCES - romania_links (accessed 2026-11-14)

## swiss_with_romanian_second_citizenship_2015_2020.csv
- Publisher: BFS (FSO), Strukturerhebung (SE). Table: "Doppelbürgerschaft im Jahr 2020", data file CSV (SDMX-like columns, CTRYOFSECCITIZ = 8232 = Romania), asset 20964155.
- URL: https://dam-api.bfs.admin.ch/hub/api/dam/assets/20964155/master ; landing page https://www.bfs.admin.ch/bfs/de/home/aktuell/neue-veroeffentlichungen.gnpdetail.2022-0436.html
- Universe: Swiss citizens (permanent resident population, aged 15+) who hold a second citizenship, by country of the second citizenship. Sample survey (rolling annual SE, pooled), so values are estimates with 95% CI half-width in % (column ci95_halfwidth_pct). bfs_status: A = reliable, U = use with caution (higher uncertainty), L = suppressed (too few observations; not in the CSV rows kept).
- Caveats: Romania is broken out only for 2015-2020 (2010-2014 file has only totals). Rows "total" and "with_second_citizenship" coincide because the country dimension already implies a second citizenship. Persons are rounded estimates. Men+women may differ from total by 1 (rounding). 2015 and 2017/2018 men values are flagged U.
- Other files opened from the same release (xlsx assets 20944863/64/66/67/68/71/91/99): searched for "Rumän" - no hit (they give only with/without second citizenship, no country).

## census2000_romanian_main_language_by_canton.csv
- Publisher: BFS, STAT-TAB table px-x-4003000000_123 "Wohnbevölkerung 2000 nach Wohnsitztyp, Kanton/Bezirk/Gemeinde, Staatsangehörigkeit (Kategorie) und Hauptsprache" (Volkszählung 2000).
- URL: https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-4003000000_123/px-x-4003000000_123.px ; script /home/user/Diaspora/scripts/romania_links_census2000_lang.py (+ romania_links_build.py).
- Universe: residents at census 2000, civil-law residence (Zivilrechtlicher Wohnsitz) and economic residence; main language "Rumänisch" (single main language, census 2000). Nationality only Swiss/foreign (no Romanian-nationality split).
- Caveat: census 2000 is a full census, not comparable with the sample-based SE (2010+). Language is not nationality.

## Documents opened but not converted to CSV
- BFS "Sprachenlandschaft in der Schweiz" 2022 (Strukturerhebung 2020): https://dam-api.bfs.admin.ch/hub/api/dam/assets/23164427/master (Rumänisch appears in charts G2.9-G2.12 only as graphic; no numbers extractable).
- BFS xls "Ständige Wohnbevölkerung nach Hauptsprachen und Kanton - 2015": https://dam-api.bfs.admin.ch/hub/api/dam/assets/2220392/master (columns only Deutsch, Französisch, Italienisch, Rätoromanisch, Englisch, Andere: Romanian not separate).
- BFS "Auslandschweizerinnen und Auslandschweizer im Jahr 2024": https://dam-api.bfs.admin.ch/hub/api/dam/assets/34447203/master (4 pp.; no Romania figure).
- BFS "Als Hauptsprachen genannte Sprachen 2016" PDF https://dam-api.bfs.admin.ch/hub/api/dam/assets/4542467/master (Romanian within "Andere Sprachen" 7.5%).
