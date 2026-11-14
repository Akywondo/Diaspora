# FINDINGS canton_zh
- Canton ZH Romanians (civil-law population, 31.12): 979 (2010), 2 512 (2016), 4 180 (2019), 5 039 (2020), 6 859 (2022), 7 983 (2024), 8 394 (2025 provisional). Source KTZH_00001143_00002169.xlsx.
- Canton annual growth: +1 047 (2019, +33.4%), +859 (2020), +827 (2021), +993 (2022), +690 (2023), +434 (2024), +411 (2025); 2025 vs 2015 +3 355; 5-year growth to 2025 +3 355 (+66.6%), 10-year +6 277 (+296.5%).
- Cross-check vs BFS permanent resident Romanians canton ZH: 2025 canton 8 394 vs BFS 8 429 (-35, -0.42%); 2024 7 983 vs 8 020 (-0.46%); 2022 -0.09%; 2023 -0.09%; 2010 -3.55%; 2018 -3.84%. Canton is always slightly lower than BFS (all 16 years).
- Explanation: canton counts civil-law residence (Hauptwohnsitz), own register survey; BFS STATPOP "ständige Wohnbevölkerung" is economic-residence-based, includes e.g. persons with permit L/F >= 12 months and some Nebenwohnsitz/Wochenaufenthalt rules; reference date both 31.12. 2025 canton value provisional (final after appeal period April 2026). Differences narrowed from ~3-4% (2010-2014) to <0.5% (2020-2025).
- SEM/ZEMIS-based canton series: 2017 2 985 vs BFS 2 988 (-0.1%); 2018 3 248 vs 3 258 (-0.3%). 2016 file 2 986 vs BFS 2 531 does not match (definition unclear; flagged).
- Municipalities 2018 (ZEMIS, 31.12.2018): Zürich 1 250 (note file also has a row "Zürich (ZH)" = canton 3 248), Winterthur 152, Dübendorf 120, Adliswil 105, Dietikon 81, Opfikon 68, Kloten 63. Only 2016-2018 municipal data by nationality found.
- City of Zürich Romanians (31.12): 171 (1993), 289 (2005), 362 (2007), 477 (2010), 882 (2015), 1 165 (2016), 1 725 (2019), 1 865 (2020), 2 254 (2022), 2 474 (2025). Share of canton 2025 about 29% (2 474 / 8 394, different register bases: city wirtschaftliche vs canton zivilrechtliche, indicative only).
- Historic city: 79 (1894), 249 (1920), 7 (1960), 132 (1980), 217 (1990).
- Sex 2025 city: 1 343 women, 1 131 men; 2010: 307 women, 170 men.
- Permit 2025 city: B 1 907, C 531, other 36; 2019: B 1 172, C 273, other 280.
- Biggest Quartiere 2025: Altstetten 245, Seebach 199, Oerlikon 158, Wollishofen 156, Alt-Wiedikon 152, Enge 149 (34 Quartiere, sum 2 474).
- City births to Romanian mothers/parents (dataset nationality of newborn): 5 (2010), 15 (2014), 19 (2019), 26 (2022), 30 (2024), 30 (2025).
- City naturalisations of Romanians: 14 (2010), 22 (2015), 23 (2019), 36 (2022), 43 (2024), 52 (2025).
- City marriages with at least one Romanian partner: 55 (2025), 49 (2024), 39 (2019); 842 summed over all years in file.
- Asylum sector (monthly): 1 Romanian each in Ausweis F 2018/19 and S 2023-25: negligible.
- Net international migration of Romanians into canton ZH (ZEMIS, statistik.info 2015/09): +57 (2002), +104 (2009), +213 (2014), +107 (Jan-Oct 2015). Publication also covers EU-2 as part of the group EU-8/EU-2/Kroatien and notes quota removal for RO/BG expected mid-2016.
- Zürich publications on the topic: statistik.info 2015/09 (Struktur der Einwanderung), statistik.info 2013/08 (Personenfreizügigkeit verändert Zuwanderung, 1999-2007; KTZH_00000549_00001463.pdf). No Romania-specific analysis found.
- Winterthur: dataset only distinguishes Schweiz/Ausland (KTZH_00002563_00005253, KTZH_00002605_00005330); 2025 foreign nationals 27 596 + 5 707 split by birth origin; no Romania.

## Not published / not available
- Canton: Romanian by age/sex/permit; municipality level after 2018; in/out-migration (flows) by nationality after 2015; births, naturalisations, pupils, wages, social assistance by nationality (cantonal datasets only distinguish Schweiz/Ausland; 1-year-age x Gemeinde dataset KTZH_00000254_00001282 has only Schweiz/Ausland).
- City Zürich: age structure by nationality; moves in/out by nationality (only Herkunft/Wegzugsort and Schweizer/Ausländer); pupils/wages/social assistance by nationality; Stadtkreis by sex/age for Romanians. Winterthur: no Romania.
## Unverified leads
- datenkatalog.statistik.zh.ch (blocked) may list further datasets (e.g. kantonale Einbürgerungen nach Staatsangehörigkeit). A search snippet suggested a nationality xlsx; confirmed and used.
## Blocked hosts I would need
- datenkatalog.statistik.zh.ch (https://datenkatalog.statistik.zh.ch), daten.statistik.zh.ch, ckan-prod.zurich.datopian.com (CSV download redirect target; datastore API on data.stadt-zuerich.ch worked instead), www.web.statistik.zh.ch/ogd/ directory listing (403).
## Cross-checks done
- See cantonal_crosscheck.csv: canton vs BFS reference for 2010-2025 (civil-law) and 2016-2018 (ZEMIS).
