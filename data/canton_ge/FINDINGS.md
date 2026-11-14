# FINDINGS - Canton Geneva, Romanian nationals (OCSTAT)
Source for all: OCSTAT tables at https://statistique.ge.ch/statistique/tel/domaines/01/ (see SOURCES.md), 31 Dec, "population résidante".
- Stock of Romanian nationals: 767 (1989), 474 (1998, low point), 502 (2000), 680 (2007), 796 (2009), 1 235 (2013), 1 893 (2019), 2 022 (2020), 2 389 (2025). Table T 01.01.8.05.
- Growth 2013-2025: 1 235 -> 2 389 (+93 %); 2007-2025: 680 -> 2 389 (x3.5).
- Romanians are about 1.07 % of the foreign resident population of GE in 2025 (2 389 of 224 158; T 01.01.8.06) and 0.44 % of total resident population (537 191).
- Age 2025 (T 01.01.8.06): 0-19 = 475; 20-39 = 930; 40-64 = 913; 65+ = 71; total 2 389.
- Permit 2025 (T 01.01.8.07): B = 1 518; C = 675; international officials (CI/EX) = 119; L and asylum suppressed ("( )"); S = 0 ("-"). Total 2 389.
- Permit 2019: L 148, B 1 294, C 348, international officials 103, asylum 0; total 1 893. Permit 2014: L 142, B 860, C 238 (CI and asylum suppressed); total 1 360.
- International officials (Romanians): 91 (1995), 101 (2005), 109 (2013, old scheme), 105 (2013 new scheme), 103 (2019), 119 (2025). This is the only Geneva figure for "International Geneva" Romanians; it covers staff and family members of international organisations and missions (permit CI/EX), about 5 % of Romanians in GE.
- Share with permit C rose from 238/1 360 (17.5 %, 2014) to 675/2 389 (28 %, 2025).
- External migration (T 01.02.1.08/1.10): immigrants from abroad 214 (2014), 252 (2016), 331 (2017, peak), 263 (2018), 259 (2020), 209 (2022), 241 (2025). Net external migration: +122 (2014), +31 (2015), +217 (2017), +134 (2019), +109 (2021), +80 (2022), +106 (2025). Emigrants in ge_romanians_external_migration_by_year.csv.
- Naturalisations of former Romanians (T 01.02.9.02): 23 (2002), 6 (2010), 4 (2014), 33 (2015), 65 (2017), 37 (2019), 21 (2020), 42 (2022), 56 (2023), 70 (2024), 38 (2025).
- 2022-2025 resident stock growth slowed (2 178 -> 2 389, +9.7 % in 3 years) vs 2017-2019 (+16 %).

## Cross-checks done
cantonal_crosscheck.csv compares OCSTAT stock with BFS STATPOP permanent resident population, canton Genève, Romanian, 2010-2025. OCSTAT is higher in every year but 2023 (-12): +61 (7.2 %) 2010, +97 (7.7 %) 2014, +117 (7.1 %) 2018, +61 (3.1 %) 2020, +8 (0.4 %) 2022, -12 (-0.5 %) 2023, +13 (0.6 %) 2024, +23 (1.0 %) 2025 (OCSTAT 2 389 vs BFS 2 366). Explanation (from definitions, not a reconciliation by OCSTAT): OCSTAT counts all residents incl. asylum domain and short-stay/other non-permanent categories and uses the cantonal register, while BFS "ständige Wohnbevölkerung" excludes some non-permanent categories (short stays < 12 months, asylum) and BFS's definition changed with the 2010-2011 register-based STATPOP and the 2020 methodology revision; the shrinking gap after 2020 is consistent with this, but the exact cause per year was not published and is not verified. Both are 31 Dec. The BFS permanent-resident definition does include international officials, so the 119 CI persons are probably in both.

## Not published / not available
- No Romanian breakdown by sex, by commune (communal tables give only origin Swiss/foreign: T 01.01.12.01/12.02), by marital status, by household type, or by detailed age year in the OCSTAT tables found; permit table has no sex split.
- No births, deaths or natural balance by nationality Romania found; no pupils by nationality Romania found (not searched in education domain, budget); no wages by nationality/origin group, no EU-2 analysis and no cross-border commuter (permis G) counts for Romania found in the Population domain tables downloaded.
- Small permit cells (L, asylum, CI before 2019) are suppressed.
- Total foreign-born or Romanian-origin (country of birth) not published for Romania; T 01.02.5.x (migration status) groups by region only.

## Unverified leads
- OCSTAT "Informations statistiques" population publications (e.g. is_population_09_2026.pdf) and domain 03 (labour/cross-border workers, permit G), domain 15 (education) may carry Romania-specific data; not opened.

## Blocked hosts I would need
None. Several statistique.ge.ch downloads intermittently returned "Empty reply" and were retried; T_01_01_12_01 and T_01_01_1_0x were not downloaded.
