# SOURCES (professions_health)
Accessed 2026-11-14. Script: /home/user/Diaspora/scripts/professions_health_fetch.py (raw metadata in raw/).
## hospital_staff_by_nationality_group_ch.csv
- BFS Krankenhausstatistik (KS), STAT-TAB px-x-1404010100_103 "Personal der Krankenhäuser nach Funktion, Betriebstyp, Grossregion/Kanton, Geschlecht, Staatsangehörigkeit (Auswahl)". URL: https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-1404010100_103/px-x-1404010100_103.px
- Universe: internal staff (Internes Personal) headcount at year-end, all hospitals, Switzerland, both sexes, 2010-2024; functions: total, Ärzteschaft, Pflegepersonal. Nationality values: Schweiz, Deutschland, Frankreich, Italien, Andere, Unbekannt (Total). ROMANIA NOT SEPARATE (inside "Andere"). Some "Unbekannt" cells empty (suppressed/none).
## sociomedical_staff_by_diploma_origin_ch.csv
- BFS Statistik der sozialmedizinischen Institutionen (SOMED), px-x-1404010100_304. URL: https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-1404010100_304/px-x-1404010100_304.px
- Staff headcount at year-end, Switzerland, selected trainings (total, Arzt, dipl. Pflegefachperson (+Weiterbildung), FaBe, FaGe) by diploma origin (Schweiz/Ausland/Unbekannt), 2006-2024. No nationality variable. Caveat: diploma origin 'Unbekannt' = all in 2006-2007-ish (not collected then); series break.
## Checked, no Romania
- https://dam-api.bfs.admin.ch/hub/api/dam/assets/10767211/master (PDF chart, SAKE education by migration status 2011-2018, no country detail). dam-api `q=` search parameter is ignored by the API (returns same list).
