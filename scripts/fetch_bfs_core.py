#!/usr/bin/env python3
"""Federal backbone of the report: every BFS STAT-TAB series that identifies
Romanian nationals (or Romania as country of birth / origin / destination).

Writes tidy CSVs to data/bfs_core/. Source: BFS STAT-TAB (PxWeb API), tables listed inline.
Run:  python3 scripts/fetch_bfs_core.py [step ...]   (no argument = all steps)
"""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from pxweb import meta, fetch, write_csv  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "bfs_core"
RO = "Rumänien"


def find(variables, var, *needles, exact=True):
    """codes of values in `var` whose label (stripped of leading '- ') matches any needle."""
    out = []
    for c, t in variables[var]["values"].items():
        lab = t.lstrip("- ").strip()
        for n in needles:
            if (lab == n) if exact else (n in lab):
                out.append(c)
    if not out:
        raise KeyError(f"{needles} not found in {var}")
    return out


def first(variables, var):
    return [next(iter(variables[var]["values"]))]


def step_balance():
    """Demographic balance by nationality 1981-2025 (table px-x-0103010000_151)."""
    t = "px-x-0103010000_151"
    _, v = meta(t)
    peers = [RO, "Bulgarien", "Polen", "Ungarn", "Kroatien", "Slowakei", "Portugal", "Deutschland",
             "Italien", "Frankreich", "Spanien", "Kosovo", "Schweiz"]
    nat = first(v, "Staatsangehörigkeit") + find(v, "Staatsangehörigkeit", *peers)
    h, r = fetch(t, {"Jahr": "*", "Staatsangehörigkeit": nat, "Geschlecht": "*",
                     "Demografische Komponente": "*"})
    write_csv(OUT / "demographic_balance_by_nationality_1981_2025.csv",
              ["year", "nationality", "sex", "component", "value"], r)


def step_stock_age():
    """Stock of Romanians by canton, population type, sex and 5-year age class 2010-2025."""
    t = "px-x-0103010000_101"
    _, v = meta(t)
    h, r = fetch(t, {"Jahr": "*", "Kanton": "*", "Bevölkerungstyp": "*",
                     "Anwesenheitsbewilligung": first(v, "Anwesenheitsbewilligung"),
                     "Geschlecht": "*", "Altersklasse": "*",
                     "Staatsangehörigkeit": find(v, "Staatsangehörigkeit", RO)})
    write_csv(OUT / "romanians_stock_canton_age_sex_2010_2025.csv",
              ["year", "canton", "population_type", "permit", "sex", "age_class", "nationality", "persons"], r)


def step_all_nationalities():
    """Permanent resident population by nationality (all ~200) for Switzerland, 2010-2025:
    lets us rank Romania among foreign nationalities each year."""
    t = "px-x-0103010000_101"
    _, v = meta(t)
    h, r = fetch(t, {"Jahr": "*", "Kanton": first(v, "Kanton"), "Bevölkerungstyp": ["1"],
                     "Anwesenheitsbewilligung": first(v, "Anwesenheitsbewilligung"),
                     "Geschlecht": first(v, "Geschlecht"), "Altersklasse": first(v, "Altersklasse"),
                     "Staatsangehörigkeit": "*"})
    write_csv(OUT / "switzerland_permanent_population_by_nationality_2010_2025.csv",
              ["year", "canton", "population_type", "permit", "sex", "age_class", "nationality", "persons"], r)
    # totals + Swiss by canton (for shares per 1 000 inhabitants)
    h, r = fetch(t, {"Jahr": "*", "Kanton": "*", "Bevölkerungstyp": ["1"],
                     "Anwesenheitsbewilligung": first(v, "Anwesenheitsbewilligung"),
                     "Geschlecht": first(v, "Geschlecht"), "Altersklasse": first(v, "Altersklasse"),
                     "Staatsangehörigkeit": first(v, "Staatsangehörigkeit") + find(v, "Staatsangehörigkeit", "Schweiz")})
    write_csv(OUT / "canton_total_and_swiss_population_2010_2025.csv",
              ["year", "canton", "population_type", "permit", "sex", "age_class", "nationality", "persons"], r)


def step_birth_country():
    """Nationality x country of birth (table px-x-0103010000_499), 2010-2025, by canton and sex."""
    t = "px-x-0103010000_499"
    _, v = meta(t)
    nat_ro = find(v, "Staatsangehörigkeit", RO)
    nat_tot = first(v, "Staatsangehörigkeit")
    nat_ch = find(v, "Staatsangehörigkeit", "Schweiz")
    born_ro = find(v, "Geburtsstaat", RO)
    born_tot = first(v, "Geburtsstaat")
    born_ch = find(v, "Geburtsstaat", "Schweiz")
    # (a) everybody born in Romania, by nationality total / Swiss / Romanian
    h, r = fetch(t, {"Jahr": "*", "Kanton": "*", "Bevölkerungstyp": "*", "Geschlecht": "*",
                     "Staatsangehörigkeit": nat_tot + nat_ch + nat_ro, "Geburtsstaat": born_ro})
    write_csv(OUT / "born_in_romania_by_nationality_canton_2010_2025.csv",
              ["year", "canton", "population_type", "nationality", "country_of_birth", "sex", "persons"], r)
    # (b) Romanian nationals by country of birth total / Switzerland / Romania
    h, r = fetch(t, {"Jahr": "*", "Kanton": "*", "Bevölkerungstyp": "*", "Geschlecht": "*",
                     "Staatsangehörigkeit": nat_ro, "Geburtsstaat": born_tot + born_ch + born_ro})
    write_csv(OUT / "romanian_nationals_by_country_of_birth_canton_2010_2025.csv",
              ["year", "canton", "population_type", "nationality", "country_of_birth", "sex", "persons"], r)
    # (c) Romanian-born by every nationality, Switzerland, permanent, latest years (who are they?)
    h, r = fetch(t, {"Jahr": ["2010", "2015", "2020", "2025"], "Kanton": first(v, "Kanton"),
                     "Bevölkerungstyp": ["1"], "Geschlecht": first(v, "Geschlecht"),
                     "Staatsangehörigkeit": "*", "Geburtsstaat": born_ro})
    r = [x for x in r if x[-1] not in (0, None)]
    write_csv(OUT / "born_in_romania_by_all_nationalities_switzerland.csv",
              ["year", "canton", "population_type", "nationality", "country_of_birth", "sex", "persons"], r)


def step_migration():
    """Immigration / emigration of the permanent resident population, Romanian nationals, 2011-2025."""
    for t, name in (("px-x-0103020200_102", "immigration"), ("px-x-0103020300_102", "emigration")):
        _, v = meta(t)
        h, r = fetch(t, {"Jahr": "*", "Kanton": "*", "Staatsangehörigkeit": find(v, "Staatsangehörigkeit", RO),
                         "Geschlecht": "*", "Altersklasse": "*"})
        write_csv(OUT / f"romanians_{name}_canton_sex_age_2011_2025.csv",
                  ["year", "canton", "nationality", "sex", "age_class", "persons"], r)
    # by country of origin / destination = Romania, all nationality categories
    for t, var, name in (("px-x-0103020200_104", "Herkunftsstaat", "immigration_from_romania"),
                         ("px-x-0103020300_104", "Zielstaat", "emigration_to_romania")):
        _, v = meta(t)
        natvar = [k for k in v if k.startswith("Staatsangehörigkeit")][0]
        sel = {"Jahr": "*", "Kanton": first(v, "Kanton"), natvar: "*", var: find(v, var, RO),
               "Geschlecht": "*", "Altersklasse": first(v, "Altersklasse")}
        h, r = fetch(t, sel)
        write_csv(OUT / f"{name}_by_nationality_category_2011_2025.csv",
                  ["year", "canton", "nationality_category", "country", "sex", "age_class", "persons"], r)


def step_naturalisation():
    """Acquisition of Swiss citizenship by former Romanian nationals, 2011-2025."""
    t = "px-x-0103030100_101"
    _, v = meta(t)
    ro = find(v, "Staatsangehörigkeit ehemalig", RO)
    h, r = fetch(t, {"Jahr": "*", "Kanton": "*", "Art des Erwerbs": "*", "Geschlecht": "*",
                     "Alter": first(v, "Alter"), "Staatsangehörigkeit ehemalig": ro})
    write_csv(OUT / "romanians_naturalisations_canton_type_sex_2011_2025.csv",
              ["year", "canton", "acquisition_type", "sex", "age", "former_nationality", "persons"], r)
    h, r = fetch(t, {"Jahr": "*", "Kanton": first(v, "Kanton"), "Art des Erwerbs": first(v, "Art des Erwerbs"),
                     "Geschlecht": first(v, "Geschlecht"), "Alter": "*", "Staatsangehörigkeit ehemalig": ro})
    write_csv(OUT / "romanians_naturalisations_by_single_age_2011_2025.csv",
              ["year", "canton", "acquisition_type", "sex", "age", "former_nationality", "persons"], r)
    # all former nationalities, Switzerland, for ranking
    h, r = fetch(t, {"Jahr": "*", "Kanton": first(v, "Kanton"), "Art des Erwerbs": first(v, "Art des Erwerbs"),
                     "Geschlecht": first(v, "Geschlecht"), "Alter": first(v, "Alter"),
                     "Staatsangehörigkeit ehemalig": "*"})
    write_csv(OUT / "naturalisations_by_former_nationality_switzerland_2011_2025.csv",
              ["year", "canton", "acquisition_type", "sex", "age", "former_nationality", "persons"], r)


def step_communes():
    """Romanian nationals by canton / district / commune 2010-2025 (table px-x-0102010000_104)."""
    t = "px-x-0102010000_104"
    _, v = meta(t)
    geo = [k for k in v if k.startswith("Kanton")][0]
    ro = find(v, "Staatsangehörigkeit", RO)
    rows = []
    years = list(v["Jahr"]["values"])
    for chunk in (years[:6], years[6:11], years[11:]):
        h, r = fetch(t, {"Jahr": chunk, geo: "*", "Bevölkerungstyp": ["1"], "Geburtsort": "*",
                         "Staatsangehörigkeit": ro})
        rows += r
    write_csv(OUT / "romanians_by_commune_birthplace_2010_2025.csv",
              ["year", "geo", "population_type", "birthplace", "nationality", "persons"], rows)
    # all-nationality totals per commune for 2025 (share of Romanians)
    h, r = fetch(t, {"Jahr": ["2025"], geo: "*", "Bevölkerungstyp": ["1"], "Geburtsort": first(v, "Geburtsort"),
                     "Staatsangehörigkeit": first(v, "Staatsangehörigkeit") + find(v, "Staatsangehörigkeit", "Schweiz")})
    write_csv(OUT / "commune_total_and_swiss_population_2025.csv",
              ["year", "geo", "population_type", "birthplace", "nationality", "persons"], r)


def step_civil_status():
    """Civil status of Romanian nationals, one table per year (px-x-0103010000_410 ... _425)."""
    rows = []
    for yy in range(10, 26):
        t = f"px-x-0103010000_4{yy}"
        _, v = meta(t)
        h, r = fetch(t, {"Jahr": "*", "Bevölkerungstyp": ["1"], "Kanton": first(v, "Kanton"),
                         "Geschlecht": "*", "Zivilstand": "*",
                         "Staatsangehörigkeit": find(v, "Staatsangehörigkeit", RO),
                         "Geburtsstaat": first(v, "Geburtsstaat")})
        rows += r
    write_csv(OUT / "romanians_civil_status_sex_2010_2025.csv",
              ["year", "population_type", "canton", "sex", "civil_status", "nationality", "country_of_birth", "persons"], rows)


def step_single_age():
    """Single-year age pyramid of Romanian nationals for selected years (tables _110 ... _125)."""
    rows = []
    for yy in (10, 15, 20, 25):
        t = f"px-x-0103010000_1{yy}"
        _, v = meta(t)
        agevar = [k for k in v if k.startswith("Alter")][0]
        sel = {"Jahr": "*", "Kanton": first(v, "Kanton"), "Bevölkerungstyp": ["1"],
               "Anwesenheitsbewilligung": first(v, "Anwesenheitsbewilligung"),
               "Staatsangehörigkeit": find(v, "Staatsangehörigkeit", RO), "Geschlecht": "*", agevar: "*"}
        h, r = fetch(t, sel)
        print(t, h)
        rows += [dict(zip(h, x)) for x in r]
    cols = ["Jahr", "Kanton", "Bevölkerungstyp", "Anwesenheitsbewilligung", "Staatsangehörigkeit", "Geschlecht"]
    agekey = [k for k in rows[0] if k.startswith("Alter")][0]
    out = [[x[c] for c in cols] + [x[agekey], x["value"]] for x in rows]
    write_csv(OUT / "romanians_single_age_sex_selected_years.csv",
              ["year", "canton", "population_type", "permit", "nationality", "sex", "age", "persons"], out)


def step_enterprises():
    """Enterprises in Switzerland controlled from Romania and their employees, by canton (2014-2024)."""
    t = "px-x-0606010000_103"
    _, v = meta(t)
    h, r = fetch(t, {"Beobachtungseinheit": "*", "Sitzland (Auswahl)": find(v, "Sitzland (Auswahl)", RO),
                     "Kanton": "*", "Jahr": "*"})
    write_csv(OUT / "enterprises_controlled_from_romania_by_canton_2014_2024.csv",
              ["unit", "seat_country", "canton", "year", "value"], r)


def step_social_assistance():
    """Recipients of economic social assistance by nationality and canton, 2006-2025 (px-x-1304030000_306)."""
    t = "px-x-1304030000_306"
    _, v = meta(t)
    # 27 cantons x 207 nationalities x 20 years exceeds the 100 000-cell limit -> select nationalities
    keep = [c for c, lab in v["Staatsangehörigkeit"]["values"].items()
            if not lab.startswith("-") or lab.lstrip("- ").strip() in
            ("Rumänien", "Bulgarien", "Polen", "Ungarn", "Kroatien", "Portugal", "Deutschland", "Italien",
             "Frankreich", "Spanien", "Kosovo", "Serbien", "Türkei")]
    h, r = fetch(t, {"Kanton": "*", "Staatsangehörigkeit": keep, "Jahr": "*"})
    write_csv(OUT / "social_assistance_recipients_by_nationality_canton_2006_2025.csv",
              ["canton", "nationality", "year", "recipients"], r)


STEPS = {k[5:]: f for k, f in list(globals().items()) if k.startswith("step_")}

if __name__ == "__main__":
    todo = sys.argv[1:] or list(STEPS)
    for s in todo:
        print("==", s)
        STEPS[s]()
