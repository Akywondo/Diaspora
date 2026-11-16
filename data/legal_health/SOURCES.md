# SOURCES legal_health (accessed 2026-11-15)
## lex_koller_rules.csv
Publisher: Bundesamt fuer Justiz (BJ/FOJ).
- https://www.bj.admin.ch/de/grundstueckerwerb-durch-personen-im-ausland (page, news item on revision)
- https://www.bj.admin.ch/de/revision-lex-koller (dossier, consultation 15.4.-15.7.2026, statements 27.7.2026)
- https://www.bj.admin.ch/dam/de/sd-web/4c4DJ25jQFCr/faq-lex-koller-d.pdf (FAQ, "Stand 08.09.2026", 34 pp; link on the page did not move)
Raw copies: raw/bj_page.html, raw/revision-lex-koller.html, raw/faq.pdf, raw/faq.txt. Caveat: FAQ is administrative guidance, legal basis BewG (SR 211.412.41) / BewV; explanatory report of the 2026 consultation not opened.
## recognised_medical_diplomas_romania.csv
Publisher: Bundesamt fuer Gesundheit (BAG/FOPH), source Medizinalberufekommission (MEBEKO). Page: https://www.bag.admin.ch/de/statistiken-medizinalberufe ("Statistiken Medizinalberufe (2013-2024)").
- Physicians: https://www.bag.admin.ch/dam/de/sd-web/jYnK6E8zVJKV/uebersicht_diplome-med-2024.xlsx
- Dentists: https://www.bag.admin.ch/dam/de/sd-web/n9lxHqYrhk1j/uebersicht_diplome-dent-2024.xlsx
- Pharmacists: https://www.bag.admin.ch/dam/de/sd-web/JUvXggYewgJF/uebersicht_diplome-pharm-2024.xlsx
Cross-check: https://www.bag.admin.ch/dam/de/sd-web/hugICURwEKgK/BAG_TStatistik_MedBerufe-2025_de_(1).pdf (Top-5 tables p.2, p.5); also Aerztinnen_und_Aerzte_2024_d.pdf (hm0goj1U9sLs).
Definitions: counts = diplomas recognised per calendar year, by country of issue, 2002-2024; includes third-country diplomas recognised indirectly via a treaty state (the files say so). Counts diplomas, not persons; not a stock of practising doctors. Measures romania_share_pct and rank are derived by scripts/legal_health_parse_diplomas.py (rank = 1 + number of countries with a higher count, ties not split; empty when 0). Caveat: pharmacist sum of country rows is 298 vs file "Gesamtergebnis" 299 in 2024 (file inconsistency); other years/professions match. Other raw: raw/diplome_2024.xlsx (6.4 MB raw per-diploma file 2002-2024, downloaded, not parsed).
