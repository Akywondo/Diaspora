# Findings: NE / JU / ZG / FR own statistics (Romanian nationals)

- Zug: Romanian nationals 75 (2010), 100 (2011), 132, 145, 162, 181 (2015), 210, 236, 262, 310 (2019), 339 (2020), 394, 445, 504 (2023), 515 (2024), 538 (2025). Source https://data.zg.ch/store/1/resource/204.
- Zug growth 2010 -> 2025: 75 -> 538, about 7.2x; the 2019 free-movement year shows +48 (262 -> 310), but growth was steady before and after.
- Neuchâtel 2025 (Service de statistique, RCP): 549 Romanian nationals; women 333, men 216 (60.7% women). https://stat.ne.ch/1f.html
- Neuchâtel 2025 by permit: Établis (C) 191, Permis de séjour (B) 353, Courte durée 5. Same page. Romanians are 1.12% of the cantonal population per the page tooltip, and about 34.8% of them hold C.
- Cross-check: Zug matches BFS STATPOP exactly in all 16 years (diff 0).
- Cross-check: Neuchâtel 549 vs BFS 550 permanent residents 2025 (-1, -0.18%). BFS split: C 191, B 353, L 6 (sum 550). NE shows 191, 353, 5: the only gap is one L-permit holder.
- BFS reference 2025 (permanent resident, 31 Dec) for the other two cantons: Jura 173 (B 127, C 45, L 1), Fribourg 1 343 (B 929, C 384, L 27, international official without diplomatic status 3). Not verifiable against cantonal sources (see below).
- BFS also lists non-permanent Romanians 2025: Neuchâtel 22, Jura 9, Fribourg 87. No cantonal source counts these.
- NE definition note: the NE foreign population (C+B+short stay) is the cantonal register's resident foreign population. The Neuchâtel figures are consistent with the BFS permanent resident definition (diff 1 person). The page text on the annual recensement cantonal was not opened.

## Not published / not available
- Jura: no Romania; the cantonal XLSX series (2010-2025, by sex, age class, commune) only splits Suisses/Étrangers.
- Fribourg: no Romania in any opendata.fr.ch nationality dataset I found (stock, age, births by mother's age); nationality is only Suisse/Étranger. No flows by nationality published there.
- Neuchâtel: Romania only for 2025 (and the 2024 edition is not on the page). No commune breakdown for Romania found. No time series for Romania (the evolution chart covers only major nationalities).
- Zug: only the total per year; no sex/age/commune breakdown for Romania in resource 204.
- None of the four publishes Romanian births, naturalisations or migration flows in the sources opened.

## Unverified leads
- Zug resource https://data.zg.ch/store/2/resource/258 (not opened), and other Zug/Fribourg/Neuchâtel datasets (possible sex/commune breakdowns) were not checked.
- Fribourg datasets 01_03_bilan_demo_sex_natio, 01_03_mariages_natio, 01_03_deces_sex_natio_class_age: metadata fetch failed (connection resets from opendata.fr.ch on repeated requests); the Statistical Office of Fribourg (www.fr.ch/sstat) may hold PDF tables by nationality.
- Neuchâtel: other pages (e.g. 1g/1i) and the downloadable "Table et données" were not exhausted.

## Blocked hosts I would need
- None blocked. opendata.fr.ch intermittently reset connections (curl 35) for the `/records` and `/facets` endpoints; I did not work around it beyond simple retries.

## Cross-checks done
- Zug 16 years vs BFS: all equal. Neuchâtel 2025 vs BFS: 549 vs 550. Jura, Fribourg: no cantonal Romania figure to compare.
