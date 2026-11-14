# SOURCES (accessed 2026-11-14)
Publisher for all: Bundesamt fuer Statistik (BFS/FSO).

1. lse_median_wage_by_permit_sex_region.csv
 - STAT-TAB px-x-0304010000_203 "Monatlicher Bruttolohn nach Grossregion, Schweizer/innen und Auslaender/innen, beruflicher Stellung und Geschlecht" (updated 2026-04-29). URL: https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-0304010000_203/px-x-0304010000_203.px
 - Variable "Schweizer/innen und Auslaender/innen" holds permit groups (Total, Swiss, foreigners, L, B, C, G, Andere); median = "Zentralwert". Berufliche Stellung fixed to Total. Years 2012,2014,...,2024 (survey is biennial since 2012; LSE).
 - Universe: employees, private + public sector (LSE), standardised gross monthly wage (full-time 4 1/3 weeks x 40 h, incl. 13th month share, bonuses; CHF), median. Nationality/permit is NOT by individual country: Romania cannot be isolated. Cells with value suppressed are empty (5 cells).
2. lse_median_wage_by_division_permit.csv
 - STAT-TAB px-x-0304010000_206 (same title family, by Wirtschaftsabteilung, Dienstjahre = Total, Grossregion = Switzerland). URL: https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-0304010000_206/px-x-0304010000_206.px
 - NOGA 2008 divisions 05-96 only; agriculture (01-03) NOT covered. 965 of 4592 cells empty (too few observations / confidentiality).
3. silc_poverty_rate_by_nationality_group.csv
 - BFS asset 24205291, table je-d-20.03.02.01.01 "Armutsquote und Bevoelkerungsanteil, nach verschiedenen Merkmalen" 2007-2021, from SILC (excl. fictitious rent). URL: https://dam-api.bfs.admin.ch/hub/api/dam/assets/24205291/master . Armutsquote = ABSOLUTE poverty (SKOS-based poverty line), NOT the at-risk-of-poverty rate (60% of median). Groups: Swiss, foreigners, Nord-/Westeuropa, Suedeuropa, Uebrige Laender. Romania falls under "Uebrige Laender" (non-N/W/S Europe + rest of world) - a very heterogeneous proxy. Column meaning: poor persons (thousands), 95% CI, poverty rate %, CI, share of total population %, share of poor %. Latest in this file: 2021 (a newer vintage may exist, not located).
4. swiss_wage_and_price_index_2010_2022.csv
 - BFS asset 24745551, table je-i-03.04.03.02.01 (T39) "Evoluzione dei salari nominali, dei prezzi al consumo e dei salari reali", index base 1939=100, Swiss Wage Index (SSAINF-based) and CPI annual-average change. URL: https://dam-api.bfs.admin.ch/hub/api/dam/assets/24745551/master . Series ends 2022. CPI given only as annual % change (cpi_annual_avg_change_pct), not index level. Real wage index = nominal deflated by CPI.
Scripts: scripts/wages_income_fetch.py, wages_income_poverty.py, wages_income_index.py. Raw: data/wages_income/raw/.
