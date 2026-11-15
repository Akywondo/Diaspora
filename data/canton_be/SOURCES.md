# SOURCES - canton_be (accessed 2026-11-15)

Publisher for all: Finanzverwaltung des Kantons Bern (Abt. Finanzausgleich / Statistik), www.fin.be.ch. Underlying data: BFS PETRA (to 2009), STATPOP (from 2010). Pages used (HTML, list the downloads):
- https://www.fin.be.ch/de/start/themen/OeffentlicheStatistik/bevoelkerungsstatistik/bevoelkerungsstand-und--struktur.html
- https://www.fin.be.ch/de/start/themen/OeffentlicheStatistik/bevoelkerungsstatistik/migration.html

## be_foreign_resident_by_nationality_1990_2025.csv
- Table: "Staendige auslaendische Wohnbevoelkerung im Kanton Bern, nach detaillierter Staatsangehoerigkeit, 1990-2025" (xlsx, sheet Tabelle1; raw copy in raw/nat_1990_2025.xlsx).
- URL: https://www.fin.be.ch/content/dam/fin/dokumente/de/finanzverwaltung/statistik/bev%C3%B6lkerungsstatistik/bev%C3%B6lkerungsstand-und--struktur/2026/Staendige_ausl_WB_im_Kt_Bern_nach_detaill_Staatsangehoerigkeit_1990-2025_d.xlsx
- Definition: permanent resident foreign population, 31 Dec, by nationality; stock. All nationalities (incl. Romania = "Rumaenien", Bulgaria separately) plus continent aggregates. Romania row is in the same file; filter nationality_de == "Rumänien".
- Caveat: the file's own footnote: from 2010 change of production method and new definition of permanent resident population (incl. asylum seekers with stay >= 12 months). 2009->2010 (380 -> 475) is a series break. 1990-2009 PETRA, 2010+ STATPOP.
- Script: /home/user/Diaspora/scripts/canton_be_extract.py

## cantonal_crosscheck.csv
- Cantonal values above vs /home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv (canton Bern, permanent resident population, permit total, sex total, age total, Romania), 2010-2025.

## Other files inspected (not turned into CSV, no Romania content)
- Staendige_WB_der_Gemeinden_nach_Geschlecht_und_Staatsangehoer_1981-2025_d_f.xlsx (raw/gem_nat_1981_2025.xlsx): per municipality and Verwaltungskreis, only Swiss/foreign x sex. No nationality detail.
- Staendige_WB_im_Kt_Bern_nach_Alter_Geschlecht_und_Staatsangehoerigkeit_1981-2025_d.xlsx (raw/alter_sex_nat.xlsx): age/sex/Swiss-foreign only, no nationality detail.
- Erwerb_des_Schweizer_Buergerrechts_1999_2024_d.xlsx (raw/einb_1999_2024.xlsx): by canton of residence, not by nationality.
