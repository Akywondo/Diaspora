# Findings - Canton Vaud (Statistique Vaud, www.vd.ch)
All URLs: https://www.vd.ch/fileadmin/user_upload/organisation/dfin/statvd/Dom_01/Tableaux/<table>.xlsx
- Romanians, permanent resident, 31 Dec, Vaud (T01.02.18): 525 (2000), 723 (2007), 1 056 (2010), 2 304 (2017), 2 648 (2019), 2 956 (2020), 3 793 (2025).
- Growth 2010->2025: x3.6; 2019->2025: +1 145 (+43%). Romania is the largest EU-2/EU-East nationality in Vaud and 1st in group "Autres UE-27" listing 2025 (T01.02.18 Annuaire): Romania 3 793 = 1.28% of foreign pop (296 446); Poland 3 206; Bulgaria 2 070.
- Total foreign permanent residents Vaud 2025: 296 446 (T01.02.18).
- Annual change: 2016->17 +238, 2019->20 +308, 2021->22 +301, 2022->23 +209, 2023->24 +64, 2024->25 +127 (computed from series).
- Naturalisations of Romanians (T01.03.05, SEM SYMIC): 34 (2000), 18 (2007), 72 (2016), 131 (2023), 78 (2024), 64 (2025); rate 1.75% of Romanians in 2025 vs 3.86% in 2023, 6.73% in 2000. Cumulative 2000-2025 in vd_romanians_naturalisations.csv.
- New asylum applications by Romanians in Vaud: peak 177 (2002), 75 (2003), 45 (2007), 0-2 since 2008 (T01.02.23).
- Cross-check: Vaud vs BFS STATPOP Romanians permanent residents agree within -1.4% to +1.45% for 2010-2025; 2025: 3 793 vs 3 765 (+28, +0.74%). See cantonal_crosscheck.csv.

## Cross-checks done
Vaud T01.02.18 vs BFS reference extract: no exact match; differences -22 (2013, -1.4%) to +33 (2017, +1.45%). Likely causes: different register snapshot/cut-off, Vaud's 2017+ definition (asylum >=1y, international officials; BFS also counts these in the permanent population since 2010/2011 revision, but Vaud's own cantonal register RCPers differs in timing), and pre-2014 Vaud used SEM data (2012-2013 lower than BFS by ~1.4%). Explanation of causes is inference, not stated in a source.

## Not published / not available
Vaud does NOT publish for Romania (in files accessible on www.vd.ch): sex, age, permit, district/commune breakdown of Romanians; arrivals/departures; births; pupils by nationality; unemployment by nationality; wages by nationality; seasonal-worker/agri/health-staff series; a Numerus/press publication on Romanian or EU-2 immigration (none found in the 6 population Numerus PDFs read). SEM-based permit tables (Pop_etrangere_SEM_*) only split EU/EFTA (ES, FR, IT, PT) vs third states. Salary tables (Dom_03) are by characteristic/profession, not by nationality group (not examined cell by cell; no "Roumanie").
Lausanne: city statistics (Lausanne statistique, www.lausanne.ch) not in reachable host list; district Lausanne foreign total only (no Romania).

## Unverified leads
None used.

## Blocked hosts I would need
- https://mstrpub.vd.ch/MicroStrategy/servlet/mstrWeb (Statistique Vaud MicroStrategy cubes "BEVNAT" population projects; connection failed, code 000) - likely holds nationality x commune x age cubes.
- https://www.lausanne.ch/ (Lausanne city statistics, population by nationality incl. Roumanie).
- statistique.vd.ch / Statistique Vaud open data portal not tried (not reachable list).
