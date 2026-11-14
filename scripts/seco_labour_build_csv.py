#!/usr/bin/env python3
"""Build tidy CSVs from the SECO "Observatoriumsbericht zum FZA Schweiz-EU" (editions 2009-2026).

Values were transcribed from the pdftotext output produced by seco_labour_fetch_observatory.py.
Every row carries verification tokens (strings exactly as printed); this script re-checks that the
tokens occur on the cited PDF page (whitespace/apostrophes normalised) and writes `verified_on_page`.
If no page is given, the page is located automatically from the tokens.

Usage: python3 -I seco_labour_build_csv.py <raw_dir> <out_dir>
"""
import csv
import os
import re
import sys

RAW, OUT = sys.argv[1], sys.argv[2]
YEAR = {5: 2009, 6: 2010, 7: 2011, 8: 2012, 9: 2013, 10: 2014, 11: 2015, 12: 2016, 13: 2017,
        14: 2018, 15: 2019, 16: 2020, 17: 2021, 18: 2022, 19: 2023, 20: 2024, 21: 2025, 22: 2026}
_pages = {}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("′", "'").replace("`", "'")
    return re.sub(r"\s+", " ", s)


def pages(ed):
    if ed not in _pages:
        fn = os.path.join(RAW, "obs_txt", "obs%02d_%d.txt" % (ed, YEAR[ed]))
        with open(fn, encoding="utf-8", errors="replace") as f:
            _pages[ed] = [norm(p) for p in f.read().split("\f")]
    return _pages[ed]


def num(s):
    s = s.replace("%", "").replace("'", "").replace("’", "").replace(" ", "").replace(",", ".")
    return float(s)


ROWS = []
FAIL = []


def R(theme, ed, page, fig, indicator, group, scope, printed, unit, period, universe, source,
      note="", tokens=None, value=None):
    toks = [norm(t) for t in (tokens if tokens is not None else [printed])]
    pp = pages(ed)
    ok = False
    if page is None:
        cand = [i + 1 for i, p in enumerate(pp) if all(t in p for t in toks)]
        if cand:
            page, ok = cand[0], True
    else:
        ok = all(t in pp[page - 1] for t in toks)
    if not ok:
        FAIL.append((ed, page, indicator, group, period, toks))
    v = num(printed) if value is None else value
    if v == int(v) and "." not in printed and "," not in printed:
        v = int(v)
    ROWS.append(dict(theme=theme, indicator=indicator, group_label=group, scope=scope, value=v,
                     unit=unit, reference_period=period, universe=universe, data_source_cited=source,
                     report_edition=ed, report_year=YEAR[ed], pdf_page=page if page else "",
                     table_or_figure=fig, verified_on_page="yes" if ok else "no", note=note))


def SER(theme, ed, page, fig, indicator, group, scope, years, values, unit, universe, source,
        note="", ntok=3, extra=None):
    vals = values.split()
    assert len(vals) == len(years), (group, len(vals), len(years))
    tok = group + " " + " ".join(vals[:ntok])
    for y, v in zip(years, vals):
        R(theme, ed, page, fig, indicator, group, scope, v, unit, str(y), universe, source,
          note=(extra or {}).get(y, note), tokens=[tok])


# ------------------------------------------------------------------ A. net migration
T = "net_migration"
Y0215 = list(range(2002, 2016))
U_ALL = "total foreign resident population (permanent + non-permanent)"
C1 = "Tabelle C.1: Nettozuwanderung nach Staatsangehoerigkeit, gesamte auslaendische Wohnbevoelkerung, 2002-2015 (in 1'000)"
bad = "SOURCE INCONSISTENT: in this annex table the Romania row is 0.0 for 2002-2008 and -0.9 for 2009 while the Bulgaria row equals the EU-2 total of earlier editions; RO+BG do not add up to EU-2 in 2009 and 2011. Use the EU-2 row; treat RO/BG rows before 2010 as unreliable."
SER(T, 12, 107, C1, "net_migration", "EU-2", "EU2", Y0215,
    "0.3 0.2 0.1 0.1 0.2 0.1 0.2 1.7 2.2 2.5 2.4 2.7 1.8 1.5", "thousand persons", U_ALL, "SEM (ZEMIS)",
    note="EU-2 = Bulgaria + Romania; series revised vs editions 2010-2014 (2009: 0.5, 2010: 0.7, 2011: 2.4)")
SER(T, 12, 107, C1, "net_migration", "Rumänien", "RO", Y0215,
    "0.0 0.0 0.0 0.0 0.0 0.0 0.0 -0.9 1.5 2.2 1.7 1.7 1.1 0.9", "thousand persons", U_ALL, "SEM (ZEMIS)",
    note="Romania alone", extra={y: bad for y in range(2002, 2010)})
SER(T, 12, 107, C1, "net_migration", "Bulgarien", "BG", Y0215,
    "0.3 0.2 0.1 0.1 0.2 0.1 0.2 0.5 0.7 0.7 0.7 0.9 0.7 0.5", "thousand persons", U_ALL, "SEM (ZEMIS)",
    note="Bulgaria alone", extra={y: bad for y in range(2002, 2009)})
SER(T, 12, 107, C1, "net_migration", "EU-8", "EU8", Y0215,
    "1.9 0.9 1.2 1.7 4.2 3.8 4.4 3.5 4.0 7.0 8.3 8.7 8.7 9.0", "thousand persons", U_ALL, "SEM (ZEMIS)")
SER(T, 6, None, "Tabelle 2.2: Wanderungssaldo der auslaendischen Wohnbevoelkerung nach Staatsangehoerigkeit (in 1'000)",
    "net_migration", "EU2", "EU2", list(range(2002, 2010)), "0.3 0.2 0.1 0.1 0.2 0.1 0.2 0.5",
    "thousand persons", "foreign resident population", "as cited in report (BFM/ZEMIS)",
    note="older vintage (edition 2010); EU-2 = Bulgaria + Romania", ntok=8)
SER(T, 10, None, "table 'Wanderungssaldo nach Staatsangehoerigkeit' (rows EU8 / EU2 / uebrige EU8+2), chapter 2",
    "net_migration", "EU2", "EU2", list(range(2002, 2014)),
    "0.3 0.2 0.1 0.1 0.2 0.1 0.2 0.5 0.7 2.4 2.4 2.6", "thousand persons", "foreign resident population",
    "BFM/ZEMIS", note="older vintage (edition 2014); EU-2 = Bulgaria + Romania", ntok=12)
Z = "SEM (ZEMIS)"
R(T, 13, 6, "summary text", "net_migration", "EU2", "EU2", "3400", "persons", "2016", U_ALL, Z,
  note="EU-2; +126% vs 2015; SECO: 'voruebergehender Oeffnungseffekt' after quotas ended 1 June 2016", tokens=["EU2 (3400, +126%)"])
R(T, 13, 25, "text ch. 3.1.4", "net_migration_change_vs_previous_year", "EU2", "EU2", "1900", "persons", "2016", U_ALL, Z,
  note="EU-2; change 2015->2016 (+126%)", tokens=["(+1900; +126%)"])
R(T, 13, 25, "text ch. 3.1.4", "net_migration", "EU8", "EU8", "6'600", "persons", "2016", U_ALL, Z, tokens=["6'600 Personen"])
R(T, 13, 21, "text ch. 3.1", "net_migration", "Osteuropa (inkl. Kroatien)", "EU_EAST", "10'000", "persons", "2016", U_ALL, Z,
  note="EU8+EU2+Croatia; about 30% of the EU net migration", tokens=["10'000 Personen"])
t17 = ["4'200 Personen aus Rumänien (2'600) und Bulgarien (1'600)"]
R(T, 14, 18, "Kasten / Abb. 2.6 text", "net_migration", "Rumänien", "RO", "2'600", "persons", "2017", U_ALL, Z, note="Romania alone (rounded)", tokens=t17)
R(T, 14, 18, "Kasten / Abb. 2.6 text", "net_migration", "Bulgarien", "BG", "1'600", "persons", "2017", U_ALL, Z, tokens=t17)
R(T, 14, 18, "Kasten / Abb. 2.6 text", "net_migration", "Rumänien + Bulgarien", "EU2", "4'200", "persons", "2017", U_ALL, Z,
  note="EU-2; about 40% of net migration from Eastern Europe", tokens=t17)
t18 = ["3354 Personen aus Rumänien (2118) und Bulgarien (1236)"]
R(T, 15, 20, "Kasten 2.1 / Abb. 2.5 text", "net_migration", "Rumänien", "RO", "2118", "persons", "2018", U_ALL, Z, note="Romania alone", tokens=t18)
R(T, 15, 20, "Kasten 2.1 / Abb. 2.5 text", "net_migration", "Bulgarien", "BG", "1236", "persons", "2018", U_ALL, Z, tokens=t18)
R(T, 15, 20, "Kasten 2.1 / Abb. 2.5 text", "net_migration", "Rumänien + Bulgarien", "EU2", "3354", "persons", "2018", U_ALL, Z,
  note="EU-2; about 32% of net migration from Eastern Europe", tokens=t18)
t19 = ["3 926 Personen aus Rumänien (2 625) und Bulgarien (1 301)"]
R(T, 16, 22, "Kasten 2.1 / Abb. 2.5", "net_migration", "Rumänien", "RO", "2 625", "persons", "2019", U_ALL, Z, note="Romania alone", tokens=t19)
R(T, 16, 22, "Kasten 2.1 / Abb. 2.5", "net_migration", "Bulgarien", "BG", "1 301", "persons", "2019", U_ALL, Z, tokens=t19)
R(T, 16, 22, "Kasten 2.1 / Abb. 2.5", "net_migration", "Rumänien + Bulgarien", "EU2", "3 926", "persons", "2019", U_ALL, Z,
  note="EU-2; about 43% of net migration from Eastern Europe", tokens=t19)
R(T, 16, 5, "summary", "net_migration", "Osteuropa (EU8, EU2 und Kroatien)", "EU_EAST", "9 518", "persons", "2019", U_ALL, Z, tokens=["9 518 aus Osteuropa"])
t20 = ["7'400 Personen zu (davon mit 3'800 gut die Hälfte aus Rumänien und Bulgarien)"]
R(T, 17, 25, "text ch. 2", "net_migration", "Rumänien + Bulgarien", "EU2", "3'800", "persons", "2020", U_ALL, Z, note="EU-2 (rounded)", tokens=t20)
R(T, 17, 25, "text ch. 2", "net_migration", "Osteuropa", "EU_EAST", "7'400", "persons", "2020", U_ALL, Z, tokens=t20)
R(T, 18, 30, "Abb. 2.9 text", "net_migration", "Rumänien", "RO", "3'200", "persons", "2021", U_ALL, Z,
  note="Romania alone (rounded); 4th largest contributor to the EU/EFTA balance in 2021",
  tokens=["Mit je 3'200 resp. 3'100 Personen ist die Nettozuwanderung aus Rumänien und Spanien"])
U_P = "permanent foreign resident population"
f19 = "Abb. 1.2: Nettozuwanderung aus der EU/EFTA kumuliert ueber die Jahre 2002-2021, nach Nationalitaet (in Tsd.)"
s19 = "2002-2010 ESPOP & PETRA; from 2011 STATPOP (BFS)"
for g, sc, v in (("Rumänien", "RO", "26.1"), ("Bulgarien", "BG", "14.0"), ("Polen", "PL", "35.0"), ("Ungarn", "HU", "23.3")):
    R(T, 19, 14, f19, "net_migration_cumulative", g, sc, v, "thousand persons", "2002-2021", U_P, s19, tokens=[g + " " + v])
R(T, 19, 14, f19, "share_of_cumulative_eu_efta_net_migration", "Rumänien", "RO", "3%", "percent", "2002-2021", U_P, s19, tokens=["Rumänien 26.1 (3%)"])
f20 = "Abb. 1.2: Nettozuwanderung aus der EU/EFTA, nach Staatsangehoerigkeit (in 1 000)"
for g, sc, v, sh in (("Rumänien", "RO", "4.6", "7%"), ("Bulgarien", "BG", "1.8", "3%"), ("Polen", "PL", "4.6", "7%"),
                     ("Ungarn", "HU", "2.4", "3%"), ("Deutschland", "DE", "14.5", "21%")):
    R(T, 20, 15, f20, "net_migration", g, sc, v, "thousand persons", "2023", U_P, "ZEMIS (SEM)", tokens=["%s %s (%s)" % (g, v, sh)])
    R(T, 20, 15, f20, "share_of_eu_efta_net_migration", g, sc, sh, "percent", "2023", U_P, "ZEMIS (SEM)", tokens=["%s %s (%s)" % (g, v, sh)])
R(T, 20, 15, f20, "net_migration", "EU/EFTA Total", "EU_EFTA", "68'000", "persons", "2023", U_P, "ZEMIS (SEM)", tokens=["Total 68'000"])
f21 = "Abb. 1.2: Nettozuwanderung aus der EU/EFTA, nach Staatsangehoerigkeit"
s21 = "ESPOP, from 2011 STATPOP (BFS), 2024 ZEMIS (SEM)"
R(T, 21, 11, f21, "share_of_eu_efta_net_migration", "ROU", "RO", "6%", "percent", "2024", U_P, s21, note="Romania alone", tokens=["ROU", "9% 5% 6%"])
R(T, 21, 11, f21, "share_of_eu_efta_net_migration", "POL", "PL", "5%", "percent", "2024", U_P, s21, tokens=["POL", "9% 5% 6%"])
R(T, 21, 11, f21, "share_of_eu_efta_net_migration", "ROU", "RO", "4%", "percent", "average 2002-2024", U_P, s21, tokens=["ROU", "4% 5% 4%"])
R(T, 21, 12, "text to Abb. 1.2", "net_migration_annual_average", "Rumänien", "RO", "1 700", "persons per year", "average 2002-2024", U_P, s21,
  note="Romania alone; 4% of EU/EFTA net migration", tokens=["1 700 (4 Prozent) aus Rumänien"])
R(T, 21, 12, "text to Abb. 1.2", "net_migration_annual_average", "Polen", "PL", "2 000", "persons per year", "average 2002-2024", U_P, s21,
  tokens=["2 000 Personen (5 Prozent) aus Polen"])
f22 = "A 1.2 Anteil einzelner Herkunftsstaaten an der Nettozuwanderung aus dem EU/EFTA-Raum"
s22 = "ESPOP, from 2011 STATPOP (BFS); 2025 ZEMIS (SEM)"
n22 = "treemap label; value/label pairing checked with pdfplumber word coordinates"
R(T, 22, 9, f22, "share_of_eu_efta_net_migration", "ROU", "RO", "5%", "percent", "2025", U_P, s22, note="Romania alone; " + n22, tokens=["ROU", "4% (5%)"])
R(T, 22, 9, f22, "share_of_eu_efta_net_migration", "ROU", "RO", "4%", "percent", "average 2002-2025", U_P, s22, note="Romania alone; " + n22, tokens=["ROU", "4% (5%)"])
R(T, 22, 9, f22, "share_of_eu_efta_net_migration", "BGR", "BG", "1%", "percent", "2025", U_P, s22, note=n22, tokens=["BGR", "2% (1%)"])
R(T, 22, 9, f22, "share_of_eu_efta_net_migration", "BGR", "BG", "2%", "percent", "average 2002-2025", U_P, s22, note=n22, tokens=["BGR", "2% (1%)"])
R(T, 22, 9, "text", "net_migration", "Osteuropa (vorwiegend Polen, Rumänien und Ungarn)", "EU_EAST", "7 400", "persons", "2025", U_P, s22, tokens=["(2025: 7 400)"])
R(T, 22, 9, "text", "net_migration_annual_average", "Osteuropa (vorwiegend Polen, Rumänien und Ungarn)", "EU_EAST", "7 900", "persons per year",
  "average 2002-2025", U_P, s22, tokens=["7 900 Personen (2025: 7 400)"])

# ------------------------------------------------------------------ B. stocks
T = "population_stock"
D2 = "Tabelle D.2: Bestand der staendigen und nicht staendigen auslaendischen Wohnbevoelkerung nach Herkunftslaendern 2002-2015, Ende Dezember (in 1'000)"
U_ST = "permanent + non-permanent foreign resident population, end of December"
for g, sc, vals in (
        ("Rumänien", "RO", "3.6 3.7 3.9 4.0 4.1 4.2 4.6 5.7 7.1 8.8 10.4 12.0 13.0 13.8"),
        ("Bulgarien", "BG", "2.1 2.2 2.2 2.3 2.3 2.3 2.4 2.9 3.5 4.2 4.9 5.7 6.4 6.9"),
        ("EU-2", "EU2", "5.7 5.9 6.1 6.3 6.4 6.6 7.1 8.6 10.6 13.0 15.3 17.7 19.4 20.6"),
        ("EU-8", "EU8", "25.0 25.4 26.3 27.8 31.5 35.7 40.1 44.8 50.7 47.0 55.2 64.1 72.9 82.0"),
        ("EU27/EFTA", "EU_EFTA", "882 906 927 951 979 1013 1070 1105 1143 1192 1239 1301 1344 1380"),
        ("Gesamttotal", "TOTAL", "1495 1529 1554 1577 1598 1632 1692 1728 1771 1827 1879 1949 2004 2050")):
    SER(T, 12, 108, D2, "foreign_population_stock", g, sc, Y0215, vals, "thousand persons", U_ST, "SEM (ZEMIS)")
T29 = "Tabelle 2.9: Auslaendische Wohnbevoelkerung und Grenzgaenger, Bestand Dezember 2009"
for g, sc, a, b, c, tok in (
        ("Rumänien", "RO", "4'925", "808", "5'733", "Rumänien 4'925 0.3% 808 1.5% 5'733 0.3%"),
        ("Bulgarien", "BG", "2'473", "403", "2'876", "Bulgarien 2'473 0.2% 403 0.8% 2'876 0.1%"),
        ("Total EU2", "EU2", "7'398", "1'211", "8'609", "7'398 0.5% 1'211 2.3% 8'609 0.4%")):
    n = "caption says 'in 1'000' but values are printed in persons"
    R(T, 6, None, T29, "foreign_population_stock_permanent", g, sc, a, "persons", "2009-12", "permanent foreign resident population", "as cited in report (BFM/ZEMIS)", note=n, tokens=[tok])
    R(T, 6, None, T29, "foreign_population_stock_non_permanent", g, sc, b, "persons", "2009-12", "non-permanent foreign resident population", "as cited in report (BFM/ZEMIS)", note=n, tokens=[tok])
    R(T, 6, None, T29, "foreign_population_stock", g, sc, c, "persons", "2009-12", U_ST, "as cited in report (BFM/ZEMIS)", note=n, tokens=[tok])
T24 = "Tabelle 2.4: Bestand der staendigen und nicht staendigen auslaendischen Wohnbevoelkerung nach Staatsangehoerigkeit, 1991-2012, Ende Dezember (in 1'000)"
SER(T, 9, None, T24, "foreign_population_stock", "EU2", "EU2", list(range(1991, 2002)), "3 3 3 3 3 3 3 4 4 4 5",
    "thousand persons", U_ST, "as cited in report (BFM/ZEMIS)", note="EU-2 = Bulgaria + Romania; rounded to thousands", ntok=11)
SER(T, 9, None, T24, "foreign_population_stock", "EU2", "EU2", list(range(2002, 2013)), "6 6 6 6 6 7 7 9 11 13 15",
    "thousand persons", U_ST, "as cited in report (BFM/ZEMIS)", note="EU-2 = Bulgaria + Romania; rounded to thousands", ntok=11)
T21 = "Tabelle 2.1: Auslaendische Wohnbevoelkerung nach Staatsangehoerigkeit und Zuwanderungszeitpunkt"
U21 = "permanent + non-permanent foreign resident population aged 18-63/64, end of December 2016"
for g, sc, a, b, c in (("EU2, Kroatien", "EU2_HR", "20'000", "23'000", "43'000"), ("EU8", "EU8", "67'000", "8'000", "75'000"),
                       ("Total", "EU_EFTA", "727'000", "335'000", "1'062'000")):
    tok = ["%s %s %s %s" % (g, a, b, c)]
    R(T, 14, 53, T21, "stock_immigrated_under_fza", g, sc, a, "persons", "2016-12", U21, "ZEMIS", tokens=tok,
      note="EU2 counted as FZA immigrants if arrived after 2009" if sc == "EU2_HR" else "")
    R(T, 14, 53, T21, "stock_immigrated_before_fza", g, sc, b, "persons", "2016-12", U21, "ZEMIS", tokens=tok)
    R(T, 14, 53, T21, "stock_total", g, sc, c, "persons", "2016-12", U21, "ZEMIS", tokens=tok)
A21 = "Abb. 2.1: Personen aus der EU/EFTA in der Schweiz - Bestaende am 31.12.2020 nach Staatsangehoerigkeit und Zuwanderungszeitpunkt"
U20 = "persons with permits B, C and L aged 18-63/64, immigrated under the FZA, 31.12.2020"
R(T, 19, 37, A21, "stock_immigrated_under_fza", "OSTEUROPA", "EU_EAST", "120'600", "persons", "2020-12", U20, "STATPOP; Auswertung BSV/SECO",
  note="EU8+EU2 (+Croatia); the EU-2 sub-value is drawn but NOT labelled in the figure", tokens=["120'600 Pers."])
R(T, 19, 37, A21, "stock_immigrated_under_fza", "EU8", "EU8", "86'600", "persons", "2020-12", U20, "STATPOP; Auswertung BSV/SECO", tokens=["53'000 86'600"])
R(T, 19, 37, A21, "stock_immigrated_under_fza", "EU/EFTA total", "EU_EFTA", "836'500", "persons", "2020-12", U20, "STATPOP; Auswertung BSV/SECO", tokens=["836'500 Personen"])

# ------------------------------------------------------------------ C. unemployment insurance balance
T = "unemployment_insurance_balance"
ALV = {
    2010: (9, None, "Tabelle 4.6", "net of retrocessions", {"CH": ("71.7%", "59.2%", "1.21"), "EU_EFTA": ("22.8%", "23.2%", "0.98"),
           "THIRD": ("5.6%", "17.6%", "0.32"), "PT": ("2.9%", "5.3%", "0.54"), "EU8_EU2": ("0.6%", "0.9%", "0.63")}),
    2012: (10, 91, "Tabelle 5.4", "net of retrocessions", {"CH": ("70.2%", "56.9%", "1.23"), "EU_EFTA": ("24.4%", "26.6%", "0.91"),
           "THIRD": ("5.4%", "16.5%", "0.33"), "PT": ("3.0%", "6.8%", "0.44"), "EU8_EU2": ("0.9%", "1.2%", "0.73")}),
    2013: (11, 100, "Tabelle 6.4", "incl. retrocessions and reimbursements", {"CH": ("69.9%", "53.7%", "1.30"), "EU_EFTA": ("25.0%", "31.1%", "0.80"),
           "THIRD": ("5.4%", "15.1%", "0.36"), "PT": ("3.1%", "7.0%", "0.45"), "EU8_EU2": ("1.0%", "1.6%", "0.67")}),
    2014: (12, 87, "Tabelle 6.6", "incl. retrocessions and reimbursements", {"CH": ("71.2%", "55.7%", "1.28"), "EU_EFTA": ("23.2%", "29.2%", "0.79"),
           "THIRD": ("5.6%", "15.1%", "0.37"), "PT": ("3.2%", "7.5%", "0.45"), "EU8_EU2": ("1.2%", "1.8%", "0.68")}),
    2015: (13, None, "Tabelle 5.6", "incl. retrocessions and reimbursements", {"CH": ("70.4%", "54.9%", "1.28"), "EU_EFTA": ("24.0%", "30.1%", "0.80"),
           "THIRD": ("5.6%", "14.9%", "0.37"), "PT": ("3.2%", "7.5%", "0.43"), "EU8_EU2": ("1.3%", "2.2%", "0.61")}),
    2016: (14, 35, "Tabelle 4.7", "incl. retrocessions and reimbursements", {"CH": ("70.4%", "55.0%", "1.28"), "EU_EFTA": ("24.4%", "31.0%", "0.79"),
           "THIRD": ("5.2%", "14.0%", "0.37"), "PT": ("3.2%", "7.1%", "0.45"), "EU8_EU2": ("1.5%", "2.6%", "0.56")}),
    2017: (15, 37, "Tabelle 4.7", "incl. retrocessions and reimbursements", {"CH": ("70,4 %", "55,3 %", "1,27"), "EU_EFTA": ("24,4 %", "31,1 %", "0,78"),
           "THIRD": ("5,3 %", "13,6 %", "0,39"), "PT": ("3,2 %", "6,6 %", "0,48"), "EU8_EU2": ("1,6 %", "2,9 %", "0,56")}),
    2018: (16, 44, "Tabelle 4-7", "incl. retrocessions and reimbursements", {"CH": ("69,4%", "55,4%", "1.25", "89"), "EU_EFTA": ("25,0%", "31,0%", "0.81", "88"),
           "THIRD": ("5,3%", "13,1%", "0.40", "97"), "PT": ("3,2%", "6,2%", "0.51", "75"), "EU8_EU2": ("1,8%", "3,2%", "0.56", "87")}),
    2019: (17, 39, "Tabelle 4.7", "incl. retrocessions and reimbursements", {"CH": ("69.5%", "54.7%", "1.27", "88"), "EU_EFTA": ("24.7%", "31.4%", "0.79", "88"),
           "THIRD": ("5.5%", "13.4%", "0.41", "97"), "PT": ("3.1%", "5.8%", "0.54", "73"), "EU8_EU2": ("1.9%", "3.5%", "0.56", "89")}),
    2020: (18, 63, "Tabelle 4.8", "incl. retrocessions and reimbursements", {"CH": ("69.0%", "52.7%", "1.31", "102"), "EU_EFTA": ("25.5%", "32.8%", "0.78", "101"),
           "THIRD": ("5.5%", "14.5%", "0.38", "116"), "PT": ("3.1%", "5.9%", "0.52", "91"), "EU8_EU2": ("2.0%", "4.0%", "0.52", "104")}),
    2021: (19, 81, "Tabelle 3.7", "incl. retrocessions and reimbursements", {"CH": ("69.7%", "52.6%", "1.33", "105"), "EU_EFTA": ("23.7%", "31.2%", "0.76", "102"),
           "THIRD": ("6.7%", "16.3%", "0.41", "117"), "PT": ("3.1%", "5.4%", "0.57", "89"), "EU8_EU2": ("2.2%", "4.2%", "0.53", "104")}),
    2022: (20, 40, "Tabelle 3.7", "incl. retrocessions and reimbursements", {"CH": ("67.3%", "52.9%", "1.27", "89"), "EU_EFTA": ("25.9%", "30.8%", "0.84", "84"),
           "THIRD": ("6.8%", "16.3%", "0.42", "94"), "PT": ("3.1%", "5.3%", "0.58", "75"), "EU8_EU2": ("2.4%", "4.4%", "0.56", "87")}),
    2023: (21, 72, "Tabelle 3.7", "incl. retrocessions and reimbursements", {"CH": ("67.3%", "50.9%", "1.32", "86"), "EU_EFTA": ("26.7%", "33.0%", "0.81", "84"),
           "THIRD": ("6.0%", "16.2%", "0.37", "91"), "PT": ("3.2%", "5.3%", "0.60", "75"), "EU8_EU2": ("2.6%", "4.8%", "0.55", "71")}),
}
LAB = {"CH": "Schweiz", "EU_EFTA": "EU/EFTA (EU27/EFTA or EU28/EFTA depending on edition)", "THIRD": "Drittstaaten", "PT": "Portugal", "EU8_EU2": "EU8+2"}
SRC_ALV = "BSV (Individuelle Konten der AHV), SECO"
for yr, (ed, pg, tab, kind, d) in ALV.items():
    anchor = [d["EU8_EU2"][0], d["EU8_EU2"][1], d["EU8_EU2"][2], "Verhältnis Beiträge/ALE"]
    if pg is None:
        pg_found = [i + 1 for i, p in enumerate(pages(ed)) if all(norm(t) in p for t in anchor)]
        pg = pg_found[0] if pg_found else None
    for sc, vals in d.items():
        nt = "EU8+2 = EU-8 + Bulgaria + Romania (no separate EU-2 or Romania value published); " + kind if sc == "EU8_EU2" else kind
        fig = tab + ": Anteile an Einnahmen der ALV und Ausgaben fuer ALE nach Nationalitaetengruppen, %d" % yr
        R(T, ed, pg, fig, "share_of_alv_contributions", LAB[sc], sc, vals[0], "percent", str(yr), "all contributors to unemployment insurance (wage contributions)", SRC_ALV, note=nt)
        R(T, ed, pg, fig, "share_of_ale_benefits", LAB[sc], sc, vals[1], "percent", str(yr), "all unemployment benefit (ALE) expenditure", SRC_ALV, note=nt)
        R(T, ed, pg, fig, "ratio_contribution_share_to_benefit_share", LAB[sc], sc, vals[2], "ratio", str(yr), "ALV", SRC_ALV, note=nt + "; <1 = net recipient")
        if len(vals) > 3:
            R(T, ed, pg, fig, "ale_benefit_duration", LAB[sc], sc, vals[3], "daily allowances (days)", str(yr), "ALE recipients", SRC_ALV, note=nt,
              tokens=["Dauer ALE Bezug in Tagen", vals[3]])
T57 = "Tabelle 5.7: Verhaeltnis der Anteile an den Einnahmen der ALV und der Ausgaben fuer ALE nach Nationalitaetengruppen, 2006-2015"
k57 = {**{y: "with retrocessions for cross-border commuters (2006-2008)" for y in (2006, 2007, 2008)},
       **{y: "without retrocessions (2009-2012)" for y in (2009, 2010, 2011, 2012)},
       **{y: "with reimbursements for cross-border commuters (2013-2015)" for y in (2013, 2014, 2015)}}
for g, sc, vals, tok in (("EU8+2", "EU8_EU2", "0.76 0.82 0.81 0.77 0.72 0.75 0.73 0.66 0.69 0.61", "EU8+2 0.76 0.82 0.81 0.80 0.77"),
                         ("CH", "CH", "1.24 1.25 1.28 1.25 1.21 1.20 1.23 1.28 1.28 1.28", "CH 1.24 1.25 1.28 1.26 1.25"),
                         ("EU27/EFTA", "EU_EFTA", "0.87 0.87 0.86 0.93 0.98 0.97 0.92 0.81 0.80 0.80", "EU27/EFTA 0.87 0.87 0.86 0.87 0.93")):
    for y, v in zip(range(2006, 2016), vals.split()):
        R(T, 13, None, T57, "ratio_contribution_share_to_benefit_share_series", g, sc, v, "ratio", str(y), "ALV", SRC_ALV,
          note=k57[y] + ("; EU8+2 = EU-8 + Bulgaria + Romania" if sc == "EU8_EU2" else ""), tokens=[tok, "Tabelle 5.7"])

# ------------------------------------------------------------------ D. social assistance
T = "social_assistance_rate"
SH = "Sozialhilfestatistik BFS"
U_SH = "permanent resident population; persons with at least one social assistance benefit in the year"
R(T, 15, 40, "text to Abb. 4.4", "social_assistance_rate", "EU2 (Bulgarien und Rumänien)", "EU2", "4,6 %", "percent", "2017", U_SH, SH,
  note="EU-2 only", tokens=["4,6 % bei Personen aus der EU2"])
R(T, 15, 40, "text to Abb. 4.4", "social_assistance_rate", "EU8 (and Italy)", "EU8", "3,4 %", "percent", "2017", U_SH, SH,
  tokens=["3,4 % bei Personen aus Italien oder aus den Ländern der EU8"])
R(T, 16, 47, "text to Abb. 4.4", "social_assistance_rate", "EU2 (Bulgarien und Rumänien)", "EU2", "4,2 %", "percent", "2018", U_SH, SH,
  note="EU-2 only; same level as Spain/Greece", tokens=["4,2 % bei Personen aus der EU2"])
R(T, 16, 47, "text to Abb. 4.4", "social_assistance_rate", "EU8", "EU8", "2,9 %", "percent", "2018", U_SH, SH, tokens=["2,9 % bei Personen aus den Ländern der EU8"])
f41 = "Abb. 4.4: Sozialhilfequoten nach Nationalitaet, right panel 'Sozialhilfequote im Jahr 2019' (nur wirtschaftliche Sozialhilfe)"
n41 = "rates for single nationalities are SECO's own calculations; only nationalities with more than 600 cases in 2019 shown"
for g, sc, v in (("Rumänien", "RO", "4.0"), ("TOTAL", "TOTAL", "3.2"), ("Schweizer/innen", "CH", "2.2"), ("Ausländer/innen", "FOREIGN", "6.1"),
                 ("EU/EFTA", "EU_EFTA", "2.7"), ("Deutschland", "DE", "1.6"), ("Österreich", "AT", "1.8"), ("Polen", "PL", "1.9"),
                 ("Frankreich", "FR", "2.7"), ("Ungarn", "HU", "2.8"), ("Italien", "IT", "3.2"), ("Portugal", "PT", "3.5"),
                 ("Spanien", "ES", "4.6"), ("Drittstaaten", "THIRD", "12.6")):
    R(T, 17, 41, f41, "social_assistance_rate", g, sc, v, "percent", "2019", U_SH + " (economic social assistance only)", SH,
      note=("ROMANIA ALONE; " if sc == "RO" else "") + n41, tokens=[g + " " + v])
R(T, 19, 82, "Abb. 3.6: Sozialhilfequote nach Nationalitaet (2021, right panel)", "social_assistance_rate", "EU8, EU2, Kroatien", "EU_EAST", "2.7",
  "percent", "2021", U_SH, SH, note="EU8+EU2+Croatia; no separate EU-2/Romania value", tokens=["EU8, EU2, Kroatien 2.7"])
for g, sc, v, tok in (("EU8, EU2, Kroatien", "EU_EAST", "2.4", None), ("Schweizer/innen", "CH", "1.9", None), ("EU/EFTA", "EU_EFTA", "2.3", None),
                      ("Deutschland", "DE", "1.4", None), ("Portugal", "PT", "3.0", None), ("Spanien", "ES", "4.0", None),
                      ("Ausländer/innen", "FOREIGN", "6.0", "Ausländer/innen *) 6.0")):
    R(T, 20, 42, "Abb. 3.5: Sozialhilfequote fuer ausgewaehlte Nationalitaeten, im Jahr 2022", "social_assistance_rate", g, sc, v, "percent", "2022",
      U_SH, "Sozialhilfestatistik (BFS), Auswertung SECO", note="EU8+EU2+Croatia; no separate EU-2/Romania value" if sc == "EU_EAST" else "",
      tokens=[tok or (g + " " + v)])
for g, sc, v in (("EU8, EU2, Kroatien", "EU_EAST", "2.3"), ("EU/EFTA", "EU_EFTA", "2.2"), ("Deutschland", "DE", "1.4"), ("Portugal", "PT", "2.9")):
    R(T, 21, 74, "Abb. 3.5: Sozialhilfequote fuer ausgewaehlte Nationalitaeten (2023)", "social_assistance_rate", g, sc, v, "percent", "2023",
      U_SH, "Sozialhilfestatistik (BFS), Auswertung SECO", note="EU8+EU2+Croatia; no separate EU-2/Romania value" if sc == "EU_EAST" else "",
      tokens=[g + " " + v])
f210 = "Abb. 2.10: Anteil Personen mit Sozialhilfebezug nach Nationalitaet und Zuwanderungszeitpunkt, im Jahr 2016"
U210 = "permanent + non-permanent resident population aged 18-63/64; persons immigrated under the FZA (linked data)"
for g, sc, v in (("EU2+1 (FZA)", "EU2_HR", "1.9%"), ("EU8+Zypern und Malta (FZA)", "EU8", "1.6%"), ("Deutschland (FZA)", "DE", "1.4%"),
                 ("Portugal (FZA)", "PT", "3.3%"), ("EU28/EFTA, zugewandert vor FZA", "EU_EFTA_PRE_FZA", "4.5%"), ("DRITTSTAATEN", "THIRD", "9.0%")):
    R(T, 14, 67, f210, "social_assistance_receipt_rate_fza_immigrants", g, sc, v, "percent", "2016", U210,
      "Sozialhilfestatistik linked with ZEMIS", note="EU2+1 = Bulgaria, Romania + Croatia" if sc == "EU2_HR" else "", tokens=[g + " " + v])
f28 = "Abb. 2.8: Sozialhilfebezugsquote nach Nationalitaet und Zuwanderungszeitpunkt, im Jahr 2021"
U28 = "Swiss and foreigners with permits B, C, L aged 18-63/64; EU/EFTA groups = persons immigrated under the FZA (linked data)"
S28 = "SH-Statistik, STATPOP (verknuepft); Auswertung BSV/SECO"
R(T, 19, 48, "text to Abb. 2.8", "social_assistance_receipt_rate_fza_immigrants", "Rumänien und Bulgarien (EU2)", "EU2", "1.9%", "percent", "2021",
  U28, S28, note="EU-2 only (immigrated after 2009)", tokens=["(EU2) zugewanderten Personen kommt mit 1.9%"])
for g, sc, v in (("EU2 und Kroatien", "EU2_HR", "1.8"), ("EU8", "EU8", "1.3"), ("OST", "EU_EAST", "1.5"), ("Deutschland", "DE", "1.2"),
                 ("Portugal", "PT", "2.5"), ("EU/EFTA, zugewandert vor FZA", "EU_EFTA_PRE_FZA", "4.3"),
                 ("DRITTSTAATEN EUROPA", "THIRD_EUROPE", "7.1"), ("SCHWEIZER/INNEN", "CH", "2.4"), ("TOTAL", "TOTAL", "2.6")):
    R(T, 19, 49, f28, "social_assistance_receipt_rate_fza_immigrants", g, sc, v, "percent", "2021", U28, S28, tokens=[g + " " + v])

# ------------------------------------------------------------------ E. labour market integration
T = "labour_market_integration"
f22b = "Abb. 2.2: Arbeitnehmendenquoten nach Staatsangehoerigkeit und Zuwanderungszeitraum, im Jahr 2020"
U22 = "Swiss and foreigners with permits B, C, L aged 18-63/64; EU/EFTA groups = immigrated under the FZA; share with AHV-registered employment income"
S22 = "AHV-IK, STATPOP (verknuepft); Auswertung BSV/SECO"
for g, sc, v in (("Bulgarien und Rumänien", "EU2", "80.0"), ("Staaten der EU8", "EU8", "85.7"), ("Kroatien", "HR", "66.3"), ("OST", "EU_EAST", "83.8"),
                 ("EU/EFTA, zugewandert unter FZA", "EU_EFTA", "84.0"), ("Portugal", "PT", "91.1"), ("Deutschland", "DE", "85.1"),
                 ("Frankreich", "FR", "80.5"), ("EU/EFTA, zugewandert vor FZA", "EU_EFTA_PRE_FZA", "80.6"),
                 ("DRITTSTAATEN EUROPA", "THIRD_EUROPE", "71.6"), ("SCHWEIZER/INNEN", "CH", "83.7"), ("TOTAL", "TOTAL", "83.0")):
    R(T, 19, 40, f22b, "employee_rate_arbeitnehmendenquote", g, sc, v, "percent", "2020", U22, S22,
      note="EU-2 only; proxy for an activity/employment rate (NOT the SAKE Erwerbstaetigenquote)" if sc == "EU2" else "", tokens=[g + " " + v])
f22a = "Abb. 2.2: Arbeitnehmerquoten nach Nationalitaet und Zuwanderungszeitpunkt, im Jahr 2016"
U16 = "permanent + non-permanent resident population aged 18-63/64; EU groups = immigrated under the FZA"
for g, sc, v in (("EU2 und Kroatien", "EU2_HR", "77%"), ("EU8", "EU8", "86%"), ("Deutschland", "DE", "87%"),
                 ("EU28/EFTA, zugewandert vor FZA", "EU_EFTA_PRE_FZA", "80%"), ("DRITTSTAATEN", "THIRD", "69%")):
    R(T, 14, 55, f22a, "employee_rate_arbeitnehmerquote", g, sc, v, "percent", "2016", U16, "AHV-IK linked with ZEMIS (see report)",
      note="EU-2 + Croatia" if sc == "EU2_HR" else "", tokens=[g + " " + v])
R(T, 14, 55, "text to Abb. 2.2", "employee_rate_arbeitnehmerquote", "FZA-Zuwanderer total", "EU_EFTA", "85%", "percent", "2016", U16,
  "AHV-IK linked with ZEMIS (see report)", tokens=["mit 85% eine sehr hohe Erwerbsbeteiligung"])
f25b = "Abb. 2.5: Arbeitslosentaggeldbezugsquote nach Staatsangehoerigkeit und Zuwanderungszeitpunkt, im Jahr 2020"
U25 = "Swiss and foreigners with permits B, C, L aged 18-63/64; share receiving unemployment daily allowances during the year"
S25 = "AVAM/ASAL, IK-AHV, STATPOP (verknuepft); Auswertung BSV/SECO"
for g, sc, v in (("Bulgarien und Rumänien", "EU2", "6.9"), ("Staaten der EU8", "EU8", "6.7"), ("Kroatien", "HR", "3.4"), ("OST", "EU_EAST", "6.7"),
                 ("EU/EFTA, zugewandert unter FZA", "EU_EFTA", "5.7"), ("Portugal", "PT", "6.8"), ("Deutschland", "DE", "3.8"),
                 ("EU/EFTA, zugewandert vor FZA", "EU_EFTA_PRE_FZA", "4.5"), ("DRITTSTAATEN EUROPA", "THIRD_EUROPE", "8.3"),
                 ("SCHWEIZER/INNEN", "CH", "2.6"), ("TOTAL", "TOTAL", "3.4")):
    R(T, 19, 44, f25b, "unemployment_benefit_receipt_rate", g, sc, v, "percent", "2020", U25, S25,
      note="EU-2 only; annual receipt rate, NOT the registered unemployment rate (Covid year)" if sc == "EU2" else "", tokens=[g + " " + v])
f25a = "Abb. 2.5: Arbeitslosentaggeldbezugsquote nach Nationalitaet und Zuwanderungszeitpunkt, im Jahr 2016"
for g, sc, v in (("EU2 und Kroatien", "EU2_HR", "5.4%"), ("EU8", "EU8", "5.9%"), ("EU-Ost", "EU_EAST", "5.8%"), ("Portugal", "PT", "7.7%"),
                 ("Deutschland", "DE", "3.6%"), ("EU28/EFTA, zugewandert vor FZA", "EU_EFTA_PRE_FZA", "4.4%"), ("DRITTSTAATEN", "THIRD", "8.0%")):
    R(T, 14, 59, f25a, "unemployment_benefit_receipt_rate", g, sc, v, "percent", "2016",
      "permanent + non-permanent resident population aged 18-64; EU groups = immigrated under the FZA",
      "AVAM/ASAL linked with ZEMIS", note="EU-2 + Croatia" if sc == "EU2_HR" else "", tokens=[g + " " + v])
R(T, 14, 59, "text to Abb. 2.5", "unemployment_benefit_receipt_rate", "FZA-Zuwanderer total", "EU_EFTA", "5.5%", "percent", "2016",
  "permanent + non-permanent resident population aged 18-64", "AVAM/ASAL linked with ZEMIS", tokens=["lag im Jahr 2016 bei 5.5%"])
R(T, 14, 59, "text to Abb. 2.5", "unemployment_benefit_receipt_rate", "Schweiz total", "TOTAL", "3.3%", "percent", "2016",
  "permanent + non-permanent resident population aged 18-64", "AVAM/ASAL linked with ZEMIS", tokens=["gesamtschweizerischen Quote von 3.3%"])
# immigration reason
f23a = "Abb. 2.3: In ZEMIS erfasster Einwanderungsgrund bei Einreise, nach Nationalitaet, 2009-2016 (Mittelwert)"
REAS = ("work", "family_reunification", "education", "other")
for g, sc, vals in (("EU2", "EU2", "51% 29% 13% 8%"), ("EU8", "EU8", "67% 22% 5% 5%"), ("Kroatien", "HR", "12% 69% 10% 8%")):
    for r, v in zip(REAS, vals.split()):
        R(T, 14, 56, f23a, "immigration_reason_share_" + r, g, sc, v, "percent", "average 2009-2016", "immigration into the permanent resident population",
          "ZEMIS", note="EU-2 only; column order work/family/education/other inferred from legend and text" if sc == "EU2" else "", tokens=[g + " " + vals])
f23b = "Abb. 2.3: Einwanderungsgrund bei Einreise, nach Staatsangehoerigkeit, Einwanderungsjahrgaenge 2010-2020 (Mittelwert)"
for g, sc, vals in (("Bulgarien und Rumänien", "EU2", "84% 7% 3% 5%"), ("EU/EFTA", "EU_EFTA", "83% 7% 6% 5%")):
    for r, v in zip(REAS, vals.split()):
        R(T, 19, 40, f23b, "immigration_reason_share_" + r, g, sc, v, "percent", "average 2010-2020", "persons with permits B, C, L aged 18-63/64",
          "ZEMIS", note="EU-2 only; asylum share not printed (too small); column assignment inferred from legend order" if sc == "EU2" else "",
          tokens=[g + " " + vals])
f13 = "Abb. 1.3: Einwanderungsgrund bei Bewilligungserteilung, nach Staatsangehoerigkeit, im Jahr 2023"
for g, sc, vals in (("Rumänien", "RO", "76% 19%"), ("Bulgarien", "BG", "77% 16%"), ("Polen", "PL", "80% 15%"), ("EU/EFTA TOTAL", "EU_EFTA", "71% 18%")):
    for r, v in zip(REAS[:2], vals.split()):
        R(T, 20, 16, f13, "immigration_reason_share_" + r, g, sc, v, "percent", "2023", "immigration into the permanent resident population",
          "ZEMIS (SEM)", note="ROMANIA ALONE" if sc == "RO" else "", tokens=[g + " " + vals])
# wages + education (SAKE regressions sample)
WCOL = (("mean_hourly_wage", "CHF per hour (nominal)"), ("mean_age", "years"), ("mean_job_tenure", "years"), ("share_women", "percent"),
        ("share_education_sek1_no_post_compulsory", "percent"), ("share_education_sek2", "percent"), ("share_education_tertiary", "percent"))
for ed, fig, per, src, rows in (
        (14, "Tabelle 1.1: Deskriptive Statistik Erwerbstaetige 2010-2017 nach Migrationsstatus", "2010-2017 (pooled)", "BFS/SAKE 2010-2017, SECO calculations", (
            ("- Osteuropa", "EU_EAST", "36.1 35.7 3.3 54.0 7.2 37.7 55.1"), ("Ansässige Bevölkerung", "RESIDENT_REFERENCE", "40.9 42.9 10.1 46.9 10.4 53.2 36.4"),
            ("EU28/EFTA", "EU_EFTA", "41.2 37.6 4.1 41.1 15.5 31.2 53.2"), ("- Nordwesteuropa", "EU_NW", "46.2 38.2 4.3 41.4 4.5 31.9 63.6"),
            ("- Südeuropa", "EU_SOUTH", "33.2 37.0 4.0 36.9 38.9 28.4 32.7"))),
        (15, "Tabelle 2.2: Strukturmerkmale der Erwerbstaetigen 2010-2018 nach Migrationskohorte und Herkunftsregion", "2010-2018 (pooled)", "BFS/SAKE 2010-2018, SECO calculations", (
            ("- Osteuropa", "EU_EAST", "36,7 36,0 3,2 52,4 6,4 34,9 58,7"), ("Ansässige Bevölkerung", "RESIDENT_REFERENCE", "40,9 43,0 10,0 47,0 10,2 52,7 37,1"),
            ("EU28/EFTA", "EU_EFTA", "41,4 37,8 4,1 40,2 15,5 30,5 54,0"), ("- Nord-/Westeuropa", "EU_NW", "46,9 38,3 4,2 40,1 2,9 31,3 65,8"),
            ("- Südeuropa", "EU_SOUTH", "33,3 37,4 4,1 37,3 38,3 28,1 33,6")))):
    for g, sc, vals in rows:
        for (ind, unit), v in zip(WCOL, vals.split()):
            R(T, ed, None, fig, ind, g, sc, v, unit, per,
              "employed persons (SAKE), immigrated since June 2002; reference = Swiss + foreigners immigrated before 2002; apprentices excluded",
              src, note="Osteuropa = EU8 + EU2 + Croatia; no separate EU-2/Romania value" if sc == "EU_EAST" else "", tokens=[g + " " + vals])
f18 = "Abb. 1.8: Qualifikationsstruktur auslaendischer Arbeitskraefte, nach Nationalitaet und Zuwanderungszeitpunkt, im Jahr 2024"
EDU = ("share_education_tertiary", "share_education_sek2", "share_education_sek1_no_post_compulsory")
for g, sc, vals in (("EU Ost", "EU_EAST", "52% 36% 12%"), ("EU Nord", "EU_NW", "67% 27% 5%"), ("EU Süd", "EU_SOUTH", "40% 21% 38%"),
                    ("Schweizer/innen", "CH", "45% 46% 9%"), ("EU/EFTA, im Rahmen des FZA zugewandert", "EU_EFTA", "55% 26% 19%"), ("TOTAL", "TOTAL", "45% 41% 14%")):
    for ind, v in zip(EDU, vals.split()):
        R(T, 21, 17, f18, ind, g, sc, v, "percent", "2024", "employed persons aged 15+; EU groups = immigrated after 2002 under the FZA",
          "SAKE (BFS), Auswertung SECO", note="EU Ost = Eastern EU member states (EU8, EU2, Croatia); no separate Romania value" if sc == "EU_EAST" else "",
          tokens=[g + " " + vals])
f19b = "Abb. 1.9: Ausgeuebte Taetigkeit auslaendischer Arbeitskraefte (Berufshauptgruppen CH-ISCO), im Jahr 2024"
OCC = ("managers", "professionals_academic", "technicians", "clerical", "service_and_sales", "craft_trades", "plant_machine_operators", "elementary_occupations")
for g, sc, vals in (("EU Ost", "EU_EAST", "6% 27% 11% 8% 12% 14% 9% 13%"), ("Schweizer/innen", "CH", "9% 29% 19% 14% 13% 9% 3% 4%"),
                    ("EU/EFTA, im Rahmen des FZA zugewandert", "EU_EFTA", "10% 32% 14% 7% 12% 11% 5% 10%"), ("EU Süd", "EU_SOUTH", "7% 21% 11% 7% 15% 15% 7% 17%")):
    for o, v in zip(OCC, vals.split()):
        R(T, 21, 18, f19b, "occupation_share_" + o, g, sc, v, "percent", "2024", "employed persons aged 15+; EU groups = immigrated after 2002 under the FZA",
          "SAKE (BFS), Auswertung SECO", note="EU Ost = EU8, EU2, Croatia; 8 groups printed (agriculture not shown separately)" if sc == "EU_EAST" else "",
          tokens=[g + " " + vals])
f12 = "Tab. 1.2: Vertretung verschiedener Nationalitaetengruppen der staendigen Wohnbevoelkerung in ausgewaehlten Branchen, Durchschnitt 2018-2020"
BR = (("Beherbergung (55)", "accommodation_noga55", "0.8% 2.3% 1.9% 2.5% 2.8% 1.9%"), ("Restauration (56)", "restaurants_noga56", "2.2% 4.0% 2.7% 5.0% 4.3% 7.1%"),
      ("Detailhandel non-food (474-478, 4799)", "retail_non_food", "3.6% 2.4% 2.2% 2.6% 2.4% 2.8%"),
      ("Kunst, Unterh.& Erholung (90, 93)", "arts_entertainment_recreation", "1.8% 1.4% 1.6% 1.0% 2.4% 1.1%"),
      ("Persönliche Dienstleistungen (96)", "personal_services_noga96", "1.1% 1.0% 0.6% 1.5% 0.6% 1.6%"),
      ("Baugewerbe (41-43)", "construction_noga41_43", "5.4% 8.6% 4.1% 13.3% 6.3% 8.5%"), ("Übrige Branchen", "all_other_branches", "84.3% 79.6% 86.0% 73.4% 80.8% 76.2%"))
for lab, key, vals in BR:
    v = vals.split()
    for g, sc, i in (("Schweizer/innen", "CH", 0), ("EU/EFTA Total", "EU_EFTA", 1), ("EU-Süd", "EU_SOUTH", 3), ("EU-Ost", "EU_EAST", 4), ("Drittstaaten", "THIRD", 5)):
        R(T, 17, 49, f12, "share_of_employed_in_branch_" + key, g, sc, v[i], "percent", "average 2018-2020", "employed persons of the permanent resident population",
          "BFS/SAKE, SECO calculations", note="EU-Ost = EU8, EU2, Croatia; no separate Romania value" if sc == "EU_EAST" else "", tokens=[lab + " " + vals])

# ------------------------------------------------------------------ F. quotas / safeguard clause
T = "eu2_quotas_safeguard"
B3 = "Tabelle B.3: Kontingente fuer erstmalige Aufenthaltsbewilligungen fuer Erwerbstaetige der EU2 (in 1'000)"
PER = ["2009-06/2010-05", "2010-06/2011-05", "2011-06/2012-05", "2012-06/2013-05", "2013-06/2014-05", "2014-06/2015-05", "2015-06/2016-05"]
nq = "EU-2 (Bulgaria + Romania); as printed; the last two periods show lower values than the preceding one - verify against SEM before use"
for ind, vals, unit in (("quota_b_permits", "0.362 0.523 0.684 0.885 1.046 1.056 0.922", "thousand permits"),
                        ("quota_b_permits_exhaustion", "100% 100% 100% 100% 82% 93% 76%", "percent"),
                        ("quota_l_permits", "3.620 4.987 6.355 7.722 9.090 7.505 7.279", "thousand permits"),
                        ("quota_l_permits_exhaustion", "87% 100% 95% 92% 88% 72% 62%", "percent")):
    lab = "Ausschöpfung" if "exhaustion" in ind else "Kontingente"
    for p, v in zip(PER, vals.split()):
        R(T, 13, 97, B3, ind, "EU2", "EU2", v, unit, p, "first-time permits for gainfully employed EU-2 nationals", "SEM", note=nq, tokens=[lab + " " + vals])
R(T, 13, 14, "text ch. 2.2", "safeguard_clause_b_permit_ceiling", "EU2", "EU2", "996", "B permits per 12 months", "2017-06/2018-05",
  "B permits (EU/EFTA) for gainfully employed EU-2 nationals", "Federal Council decision of May 2017 (as reported by SECO)",
  note="Ventilklausel invoked May 2017; L permits not capped (threshold not reached)", tokens=["996 Einheiten"])
R(T, 14, 9, "ch. 1.2 Weiterfuehrung der Ventilklausel EU2", "safeguard_clause_b_permit_ceiling", "EU2", "EU2", "996", "B permits per 12 months", "2018-06/2019-05",
  "B permits (EU/EFTA) for gainfully employed EU-2 nationals", "Federal Council decision of 18 April 2018 (as reported by SECO)",
  note="extended one year; full free movement for BG/RO since 1 June 2019", tokens=["bis zum 31. Mai 2019 auf 996 Einheiten"])
R(T, 13, 82, "text ch. 5 (ALV)", "alv_retrocessions_short_term_residents_eu2", "EU2", "EU2", "0,6", "million CHF", "2016-01/2016-05",
  "retrocession of ALV contributions of EU-2 short-term residents (L) to home states", "SECO (extrapolation)",
  note="last retrocessions; totalisation of insurance periods applies to BG/RO since 1 June 2016", tokens=["0,6 Mio. Franken"])

# ------------------------------------------------------------------ write
COLS = ["theme", "indicator", "group_label", "scope", "value", "unit", "reference_period", "universe", "data_source_cited",
        "report_edition", "report_year", "pdf_page", "table_or_figure", "verified_on_page", "note"]
FILES = {"net_migration": "seco_obs_net_migration_eu2_romania.csv", "population_stock": "seco_obs_population_stock_eu2_romania.csv",
         "unemployment_insurance_balance": "seco_obs_unemployment_insurance_balance.csv",
         "social_assistance_rate": "seco_obs_social_assistance_rate.csv",
         "labour_market_integration": "seco_obs_labour_market_integration.csv",
         "eu2_quotas_safeguard": "seco_obs_eu2_quotas_safeguard.csv"}
for th, fn in FILES.items():
    rows = [r for r in ROWS if r["theme"] == th]
    with open(os.path.join(OUT, fn), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(fn, len(rows), "rows; unverified:", sum(r["verified_on_page"] == "no" for r in rows))
ed_src = os.path.join(RAW, "obs_editions.csv")
if os.path.exists(ed_src):
    with open(ed_src, encoding="utf-8") as f, open(os.path.join(OUT, "seco_observatory_report_editions.csv"), "w", encoding="utf-8") as g:
        g.write(f.read())
print("TOTAL", len(ROWS), "FAIL", len(FAIL))
seen = set()
for x in FAIL:
    k = (x[0], x[1], tuple(x[5]))
    if k in seen:
        continue
    seen.add(k)
    print("  FAIL ed%s p%s %s | %s | %s | %s" % (x[0], x[1], x[2], x[3], x[4], x[5]))
