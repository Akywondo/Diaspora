# SOURCES (accessed 2026-11-12/14)
All CSVs built by /home/user/Diaspora/scripts/canton_east_tg_parse.py and canton_east_sg_crosscheck.py; raw files in raw/.

## tg_romanians_by_year_permit.csv
- Publisher: Kanton Thurgau, Amt fuer Daten und Statistik. Tables "Auslaendische Wohnbevoelkerung nach Staatsangehoerigkeit" 2015-2025 (BevKant_AuslStaatsangehoerigkeit.xlsx) and "... nach Staatsangehoerigkeit und Aufenthaltsbewilligung" (BevKant_AuslStaatsangehBew.xlsx, one sheet per year 2015-2025: C, B, L>=12 months).
- Page: https://statistik.tg.ch/themen-und-daten/bevoelkerung-und-haushalte/bevoelkerungsstand-und-struktur/auslaendische-bevoelkerung.html/7033
- Files: https://statistik.tg.ch/public/upload/assets/186079/2025_2015_BevKant_AuslStaatsangehoerigkeit.xlsx ; https://statistik.tg.ch/public/upload/assets/186078/2025_2015_BevKant_AuslStaatsangehBew.xlsx
- Definition: permanent foreign resident population, 31 Dec (STATPOP-based; nationalities shown if >=10 persons). Total foreign row included.
- Caveat: municipal table (BevGmd_Ausl_Staatsangeh.xlsx) shows only Germany, Italy, N. Macedonia, Portugal, "Sonstige": Romania NOT separable by municipality. Quarterly file 2026_06_BevNationalitaetBewilligung.xlsx has no nationality detail beyond Swiss/foreign.

## sg_romanians_permanent_foreign_resident_by_year.csv, sg_romanians_by_municipality_2024.csv
- Publisher: Kanton St. Gallen, Fachstelle/Amt fuer Daten und Statistik. Table I_78 "Staendige auslaendische Wohnbevoelkerung am Jahresende, nach haeufigsten Staatsangehoerigkeiten und Geburtsort" (B01_Ausl_002), canton 1991-2024; Wahlkreise and municipalities Dec 2024. Also B01_Ausl_003 (2015-2024, all nationalities; Romania 2024 = 2852 there vs 2851 in I_78: 1-person inconsistency between two cantonal files).
- URL: https://www.sg.ch/content/dam/sgch/kanton-stgallen/statistik/b01/B01_Ausl_002_staendigeAuslWB_Staatsangeh%C3%B6rigkeit_Kt_WK_Gem.pdf (+ .xlsx); overview page https://www.sg.ch/ueber-den-kanton-st-gallen/statistik/themen/B01/wohnbevoelkerung.html
- Definition: SOURCE IS SEM ZEMIS (not STATPOP): permanent foreign residents with B/C/Ci permit or L >= 12 months; 31 Dec. Nationalities shown if >1000 persons.
- Caveat: Wahlkreis/municipal values are shown only where table lists Romania (it does for all municipalities, 2024 only). Latest year is 2024 (2025 update not yet online in the files fetched).

## cantonal_crosscheck.csv
- Cantonal series above vs /home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv (BFS STATPOP, permanent resident population, 31 Dec, permit/sex/age totals).
