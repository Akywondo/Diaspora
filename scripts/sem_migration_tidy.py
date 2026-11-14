#!/usr/bin/env python3
"""Turn sem_zemis_romania_cells_long.csv into tidy CSVs (stock, flows, balance, reasons, G permits).
Usage: python3 -I sem_migration_tidy.py <data/sem_migration dir>"""
import csv, re, sys, os, collections
D = sys.argv[1]
rows = list(csv.DictReader(open(os.path.join(D, "sem_zemis_romania_cells_long.csv"), encoding="utf-8")))
SEX = {"Total": "total", "Frauen": "female", "Männer": "male"}

def per(p):
    y, m = p.split("-")
    return int(y), (f"{y}-12-31" if m == "12" else f"{y}-09-30"), ("calendar_year" if m == "12" else "year_to_date_jan_sep")

def num(v):
    f = float(v); return int(f) if f == int(f) else f

def wr(name, header, data):
    with open(os.path.join(D, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(data)
    print(name, len(data))

SRC = "SEM Auslaenderstatistik (ZEMIS) table %s, file %s"
# 1 stock ------------------------------------------------------------------
out = []
for r in rows:
    if r["table"] != "2-10-best-tot-kat":
        continue
    y, ref, _ = per(r["period"]); lab = r["column_label"]
    geo = "CH" if len(r["sheet"]) > 2 else r["sheet"]
    last = lab.split(" | ")[-1].strip()
    sex = SEX.get(last, "total")
    if lab.startswith("Gesamt"):
        pop, permit = "total", "total"
    elif lab.startswith("Nicht ständige"):
        pop, permit = "non_permanent", "total_short_stay_lt_12_months"
    elif "Total ständige" in lab:
        pop, permit = "permanent", "total"
    elif "Kurzaufenthalter" in lab:
        pop, permit = "permanent", "L_short_stay_ge_12_months"
    elif "Aufenthalter (B)" in lab:
        pop, permit = "permanent", "B_residence"
    elif "Niedergelassene (C)" in lab:
        pop, permit = "permanent", "C_settlement"
    else:
        continue
    out.append([ref, y, r["row_label"], geo, pop, permit, sex, num(r["value"]), "2-10", r["file"]])
wr("sem_stock_by_permit_sex_canton.csv", ["reference_date", "year", "nationality", "geography", "population_type", "permit", "sex", "persons", "sem_table", "source_file"], out)

# 2 flows (4-40 permanent, 4-41 non-permanent) ------------------------------
FL = [("Total Einwanderung (Zuzug)", "immigration_total"), ("Einwanderung (Zuzug) | Effektive Einwanderung", "immigration_effective"),
      ("Übertritt aus dem Asylprozess", "immigration_transfer_from_asylum_process"), ("Einwanderung (Zuzug) | Statuswechsel", "immigration_status_change"),
      ("Reaktivierung Aufenthalt", "reactivation_of_stay"), ("Total Auswanderung (Wegzug)", "emigration_total"),
      ("Auswanderung (Wegzug) | Effektive Auswanderung", "emigration_effective"), ("Auswanderung (Wegzug) | Statuswechsel", "emigration_status_change"),
      ("Total übriger Abgang", "other_exit_total"), ("Automatisierter Abgang", "other_exit_automated"), ("Löschung Bewilligung", "other_exit_permit_cancelled"),
      ("Wanderungssaldo", "net_migration"), ("Zunahme", "increase_total"), ("Abnahme", "decrease_total")]
out = []
for r in rows:
    if r["table"] not in ("4-40-bil-saldo-stae-j", "4-41-bil-saldo-nstae-j") or len(r["sheet"]) <= 2:
        continue
    y, ref, pt = per(r["period"]); lab = r["column_label"]
    m = next((k for s, k in FL if (lab == s if s in ("Zunahme", "Abnahme", "Wanderungssaldo", "Reaktivierung Aufenthalt") else s in lab)), None)
    if m is None:
        print("UNMAPPED", r["table"], lab); continue
    out.append([y, pt, r["row_label"], "permanent" if "4-40" in r["table"] else "non_permanent", m, num(r["value"]), r["table"][:4], r["file"]])
wr("sem_migration_flows_yearly.csv", ["year", "period_type", "nationality", "population_type", "measure", "persons", "sem_table", "source_file"], out)

# 3 balance of permanent population (4-30) ----------------------------------
BL = [("Bestand Ende Monat", "stock_end_of_period"), ("Bestand Ende Vorjahr", "stock_end_of_previous_year"), ("Total Zunahme", "increase_total"),
      ("Effektive Einwanderung", "immigration_effective"), ("Übertritt aus dem Asyl", "transfer_from_asylum_process"), ("Zunahme (ohne Binnenwanderung) | Statuswechsel", "status_change_in"),
      ("Re-aktivierungen", "reactivations"), ("Geburten", "births"), ("Verlust Schweizer", "loss_of_swiss_citizenship"), ("Total Abnahme", "decrease_total"),
      ("Effektive Auswanderung", "emigration_effective"), ("Abnahme (ohne Binnenwanderung) | Statuswechsel", "status_change_out"), ("Übriger Abgang", "other_exit"),
      ("Todesfälle", "deaths"), ("Erwerb Schweizer", "acquisition_of_swiss_citizenship"), ("Technischer Ausgleich", "technical_adjustment")]
out = []
for r in rows:
    if r["table"] != "4-30-bil-stae-det-j" or len(r["sheet"]) <= 2:
        continue
    y, ref, pt = per(r["period"]); lab = r["column_label"]
    m = next((k for s, k in BL if s in lab), None)
    if m is None:
        print("UNMAPPED 4-30", lab); continue
    out.append([y, pt, r["row_label"], "permanent", m, num(r["value"]), "4-30", r["file"]])
wr("sem_permanent_population_balance_yearly.csv", ["year", "period_type", "nationality", "population_type", "component", "persons", "sem_table", "source_file"], out)

# 4 immigration by reason (3-30 permanent, 3-31 non-permanent) ---------------
RS = [("totaleinwanderung", "total"), ("kontingentierteerwerbstätigkeit", "gainful_employment_subject_to_quota"), ("erwerbstätigkeitohnekontingentierung", "gainful_employment_not_subject_to_quota"),
      ("familiennachzug", "family_reunification"), ("ausundweiterbildung", "education_and_training"), ("aufenthaltsbewilligungohneerwerbstätigkeit", "residence_without_gainful_activity"),
      ("anerkannterflüchtling", "recognised_refugee_after_asylum_grant"), ("härtefallregelung", "hardship_case_after_asylum_process"),
      ("ausländerrechtlicheregelung", "aliens_law_regularisation_after_asylum_process"), ("übrigezugänge", "other_entries")]
out = []
for r in rows:
    if r["table"] not in ("3-30-bew-in-stae-j", "3-31-bew-in-nstae-j") or len(r["sheet"]) <= 2:
        continue
    y, ref, pt = per(r["period"]); k = re.sub(r"[-\s]", "", r["column_label"]).lower()
    m = next((v for s, v in RS if s in k), None)
    if m is None:
        print("UNMAPPED reason", r["column_label"]); continue
    out.append([y, pt, r["row_label"], "permanent" if "3-30" in r["table"] else "non_permanent", m, num(r["value"]), r["table"][:4], r["file"]])
wr("sem_immigration_by_reason_yearly.csv", ["year", "period_type", "nationality", "population_type", "immigration_reason", "persons", "sem_table", "source_file"], out)

# 5 cross-border commuter permits (5-10) -------------------------------------
out = []
for r in rows:
    if r["table"] != "5-10-gg-best" or len(r["sheet"]) <= 2:
        continue
    y, ref, _ = per(r["period"]); lab = r["column_label"]; parts = [p.strip() for p in lab.split(" | ")]
    dur = "total" if parts[0].startswith("Total") else ("lt_12_months" if "< 12" in parts[0] else "ge_12_months")
    basis = "FZA_free_movement" if "FZA" in lab else ("AIG_AuG_third_country_rules" if re.search(r"A[UI]G", lab) else "total")
    sex = next((SEX[p] for p in parts if p in ("Frauen", "Männer")), "total")
    out.append([ref, y, r["row_label"], dur, basis, sex, num(r["value"]), "5-10", r["file"]])
wr("sem_cross_border_g_permits_stock.csv", ["reference_date", "year", "nationality", "permit_duration", "legal_basis", "sex", "permits", "sem_table", "source_file"], out)
