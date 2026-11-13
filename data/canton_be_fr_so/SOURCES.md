# SOURCES (accessed 2026-11-12)

## cantonal_romanians_series.csv
- Fribourg (Service de la statistique, SStat): Annuaire statistique du canton de Fribourg, table T01-11 "Population étrangère, par pays d'origine" (Dec stock, 1950-2021; permanent + non-permanent foreign resident population, source STATPOP 2010-2021 / BFS). 2010, 2019-2021 from edition 2023 https://www.fr.ch/sites/default/files/2023-05/annuaire-statistique-du-canton-de-fribourg--edition-2023_0.pdf (excerpt in raw/fr_annuaire2023_T01-11_excerpt.txt); 2015-2018 from edition 2020 https://www.fr.ch/sites/default/files/2020-03/Annuaire%20statistique%20du%20canton%20de%20Fribourg%20-%20Edition%202020.pdf (raw/fr_ann2020.txt, T01-11). Values 1950/1970/1990 (1, 2, 161) exist but are not in the CSV (census era).
- Solothurn (Amt für Finanzen, Statistik SO): "Wohnbevölkerung per 31.12.YYYY - Statistische Mitteilung" (2021, 2022, 2023) and "Solothurn zählt! Trends zur Bevölkerung" 2025 (data 31.12.2024) and 2026 (data 31.12.2025); URLs in the CSV. Tables "Die 15 häufigsten Herkunftsländer" / "Nationalitäten: die 50 grössten Bevölkerungsgruppen". Definition: cantonal GERES register, main residence, incl. B, C, L, F, N, S (RRB 2012/597, https://so.ch/fileadmin/internet/fd/fd-afin/stat/01/bevoelkerungszahlen/RRB_2012_597.pdf); differs from BFS STATPOP permanent population (stated by SO itself). Editions revise earlier years (the 2026 edition's +9.1 % growth implies a 2024 base of ~1 881, not 1 915; the 2025 edition's +10.5 % implies ~1 733 for 2023, not 1 762). Raw: raw/so_wb2020-2022.txt, raw/Solothurn_zaehlt_25.txt, raw/Solothurn_zaehlt_2026.txt (PDF files in raw/ too). 2020 edition: Romania not in top 15 (rank-15 = Österreich 1 021), so Romania < 1 021 (not in CSV).
- Sex (SO 2024: 1 041 m / 874 f; 2025: 1 176 m / 876 f) from the same tables.

## cantonal_crosscheck.csv
Cantonal values above vs BFS reference extract data/_reference/bfs_romanians_canton_year_permit_sex.csv (STATPOP 31 Dec; permanent = "Ständige Wohnbevölkerung", non-permanent = "Nichtständige Wohnbevölkerung"). Script scripts/canton_be_fr_so_build.py. Last row: SStat web text "Entre 2010 et 2025 ... Roumanie (+1105)" https://www.fr.ch/deef/ssd/statistiques-par-themes/migration-et-integration (raw/fr_mig.html) vs BFS 1343-238.

## bfs_so_fr_be_permit_sex_profile.csv
Derived (filter, no recalculation) from the BFS reference extract for BE, FR, SO: permit x sex x year x population type. Not a cantonal source.

## Bern
No cantonal Romania value obtained (host fin.be.ch blocked); nothing in the CSVs except BFS profile.
