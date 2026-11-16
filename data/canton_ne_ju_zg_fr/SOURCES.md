# Sources (accessed 2026-11-15)

## romanians_nuechatel_zug_canton_stats.csv
- Zug: Kanton Zug, Statistik, "Ausländische Wohnbevölkerung nach Nationalität" (columns jahr, land, anzahl), https://data.zg.ch/store/1/resource/204 (raw: raw/c12f7f49). Romania ("Rumänien") 2010-2025. Universe/definition as given in the brief: STATPOP-based foreign resident population, 31 Dec. The file itself carries no definition text, so this is NOT confirmed from the file; it was inferred from the exact match with the BFS permanent-resident figure in all 16 years. Resource /store/2/resource/258 was not opened (budget).
- Neuchâtel: Service de statistique NE, Portail statistique, "Population étrangère" https://stat.ne.ch/1f.html (raw: raw/62d8e509). Source line on page: "Service de statistique - RCP" (registre cantonal de la population). Only the 2025 edition is published for Romania: total 549 (women 333, men 216); by permit: Établis 191, Permis de séjour 353, Courte durée 5. Values were read from the page's embedded chart/table (HTML), not a downloadable file. Evolution chart "depuis 2010" lists only the main nationalities; Romania is absent there.
## cantonal_crosscheck.csv
- Cantonal values above vs `/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv` (BFS STATPOP, Ständige Wohnbevölkerung, all permits, both sexes, all ages, 31 Dec).
## Checked, no Romania figure published
- Jura: https://stat.jura.ch/fr/STATISTIQUES/Population/1-Population/11-etat-et-structure-de-la-population.html ; XLSX JU-T.01.01.01 to .04 downloaded (raw/JU-T.01.01.0*.xlsx). Permanent resident population 31 Dec 2010-2025 by sex, age, commune and nationality, but nationality is only Total / Suisses / Étrangers. No Romania.
- Fribourg: https://opendata.fr.ch (Opendatasoft v2.1). Datasets 01_02_pop_res_perm_sex_natio (permanent residents by sex, commune, since 1981), 01_02_age_5_sex_natio, 01_03_naissance_sex_natio_class_age_mere: nationality is a two-value category (Suisse/Étranger). Dataset 01_03_bilan_demo_sex_natio and 01_03_mariages_natio: metadata not retrieved (connection resets), presumably same category. No Romania.
## Script
- /home/user/Diaspora/scripts/canton_ne_ju_zg_fr_build.py (parses raw files, builds both CSVs). Raw downloads were made with curl.
