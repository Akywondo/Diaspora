#!/usr/bin/env python3
"""Fetch Eurostat series on Romanian citizens / Romanian-born (Switzerland + European comparison)
and push/pull context series. Writes raw JSON-stat responses to <out>/raw/ and one tidy CSV per
query to <out>/.

Usage:  python3 -I scripts/eurostat_compare_fetch.py /home/user/Diaspora/data/eurostat_compare [name ...]

API: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<dataset>?format=JSON&...
Requests are strictly sequential with a pause >= 1.2 s and back-off on 429/503.
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
BROAD_AGE = ["TOTAL", "Y_LT15", "Y15-64", "Y_GE65", "UNK"]
SEX = ["T", "M", "F"]
CTX_GEO = ["RO", "CH", "EU27_2020"]

# name -> (dataset, params)   (a parameter that is not listed = all values kept)
QUERIES = {
    # 1. stock by citizenship = RO, Switzerland, full sex x age detail
    "pop_ro_citizens_ch_by_sex_age": ("migr_pop1ctz", {"geo": ["CH"], "citizen": ["RO"]}),
    # 2. same stock for every reporting country (broad ages)
    "pop_ro_citizens_by_country": ("migr_pop1ctz", {"citizen": ["RO"], "sex": SEX, "age": BROAD_AGE}),
    # what Switzerland reports at all (all citizenships, totals) -> shows which years/citizen groups exist
    "pop_ch_all_citizenships_total": ("migr_pop1ctz", {"geo": ["CH"], "sex": ["T"], "age": ["TOTAL"]}),
    # 3. stock by country of birth = RO
    "pop_ro_born_ch_by_sex_age": ("migr_pop3ctb", {"geo": ["CH"], "c_birth": ["RO"]}),
    "pop_ro_born_by_country": ("migr_pop3ctb", {"c_birth": ["RO"], "sex": SEX, "age": BROAD_AGE}),
    # 4. flows by citizenship = RO
    "imm_ro_citizens_by_country": ("migr_imm1ctz", {"citizen": ["RO"], "sex": SEX, "age": BROAD_AGE}),
    "emi_ro_citizens_by_country": ("migr_emi1ctz", {"citizen": ["RO"], "sex": SEX, "age": BROAD_AGE}),
    # Romania's own reported emigration by country of next usual residence (all partners)
    "emi_from_ro_by_next_residence": ("migr_emi3nxt", {"geo": ["RO"], "sex": ["T"], "age": ["TOTAL"]}),
    # Romania's own reported immigration by country of previous residence (returns)
    "imm_to_ro_by_prev_residence": ("migr_imm5prv", {"geo": ["RO"], "sex": ["T"], "age": ["TOTAL"]}),
    # Swiss-reported mirror flows with partner country = RO
    "imm_to_ch_from_prev_residence_ro": ("migr_imm5prv", {"geo": ["CH"], "partner": ["RO"], "sex": SEX, "age": BROAD_AGE}),
    "emi_from_ch_to_next_residence_ro": ("migr_emi3nxt", {"geo": ["CH"], "partner": ["RO"], "sex": SEX, "age": BROAD_AGE}),
    # 5. acquisition of citizenship, former citizenship = RO
    "acq_former_ro_citizens_by_country": ("migr_acq", {"citizen": ["RO"], "sex": SEX, "age": BROAD_AGE}),
    # 6. context
    "ctx_gdp_per_capita": ("nama_10_pc", {"geo": CTX_GEO, "na_item": ["B1GQ"],
                                           "unit": ["CP_PPS_EU27_2020_HAB", "CP_EUR_HAB", "PC_EU27_2020_HAB_MPPS_CP"],
                                           "sinceTimePeriod": ["2000"]}),
    "ctx_gdp_pps_index_tec00114": ("tec00114", {"geo": CTX_GEO}),
    "ctx_net_earnings": ("earn_nt_net", {"geo": CTX_GEO, "estruct": ["NET", "GRS"],
                                         "ecase": ["P1_NCH_AW100", "P1_NCH_AW67", "CPL_CH2_AW100_100"],
                                         "sinceTimePeriod": ["2000"]}),
    "ctx_unemployment_rate": ("une_rt_a", {"geo": CTX_GEO, "sex": SEX, "age": ["Y15-74", "Y15-24"],
                                           "unit": ["PC_ACT"], "sinceTimePeriod": ["2000"]}),
    "ctx_population_1jan": ("demo_gind", {"geo": CTX_GEO, "indic_de": ["JAN", "CNMIGRAT", "NATGROW"],
                                          "sinceTimePeriod": ["1990"]}),
    "ctx_median_equivalised_income": ("ilc_di03", {"geo": CTX_GEO, "sex": ["T"], "age": ["TOTAL"],
                                                   "statinfo": ["MED_EI", "MEAN_EI"], "sinceTimePeriod": ["2005"]}),
}


def build_url(dataset, params):
    parts = [("format", "JSON"), ("lang", "EN")]
    for k, vals in params.items():
        for v in vals:
            parts.append((k, v))
    return BASE + dataset + "?" + urllib.parse.urlencode(parts)


def http_get(url):
    last = None
    for attempt in range(6):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = "HTTP %s %s" % (e.code, e.read().decode("utf-8", "replace")[:200])
            if e.code in (429, 503, 502, 504):
                time.sleep(10 + 5 * attempt)
                continue
            raise RuntimeError(last + " :: " + url)
        except Exception as e:  # network hiccup
            last = repr(e)
            time.sleep(10 + 5 * attempt)
    raise RuntimeError("giving up: %s :: %s" % (last, url))


def tidy(js):
    """JSON-stat 2.0 -> list of dict rows (one per non-missing cell or flagged cell)."""
    ids, sizes = js["id"], js["size"]
    codes, labels = [], []
    for d in ids:
        cat = js["dimension"][d]["category"]
        idx = cat["index"]
        ordered = sorted(idx, key=lambda c: idx[c])
        codes.append(ordered)
        labels.append(cat.get("label", {}))
    values = js.get("value", {})
    status = js.get("status", {})
    if isinstance(values, list):
        values = {str(i): v for i, v in enumerate(values) if v is not None}
    keys = set(values) | set(status)
    rows = []
    for k in sorted(keys, key=int):
        n = int(k)
        coord = []
        for size in reversed(sizes):
            coord.append(n % size)
            n //= size
        coord.reverse()
        row = {}
        for d, c, cl, lb in zip(ids, coord, codes, labels):
            row[d] = cl[c]
            if d in ("geo", "partner", "citizen", "c_birth"):
                row[d + "_label"] = lb.get(cl[c], "")
        row["value"] = values.get(k, "")
        row["flag"] = status.get(k, "")
        rows.append(row)
    return rows


def main():
    out = sys.argv[1]
    only = sys.argv[2:]
    raw = os.path.join(out, "raw")
    os.makedirs(raw, exist_ok=True)
    log = []
    for name, (dataset, params) in QUERIES.items():
        if only and name not in only:
            continue
        url = build_url(dataset, params)
        body = http_get(url)
        js = json.loads(body.decode("utf-8"))
        rawpath = os.path.join(raw, name + ".json")
        if len(body) <= 8 * 1024 * 1024:
            with open(rawpath, "wb") as f:
                f.write(body)
        rows = tidy(js)
        cols = []
        for r in rows:
            for c in r:
                if c not in cols:
                    cols.append(c)
        with open(os.path.join(out, name + ".csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            head = [("year" if c == "time" else c) for c in cols if c not in ("value", "flag")]
            w.writerow(["dataset"] + head + ["value", "flag"])
            for r in rows:
                w.writerow([dataset] + [r.get(c, "") for c in cols if c not in ("value", "flag")]
                           + [r.get("value", ""), r.get("flag", "")])
        years = sorted({r["time"] for r in rows if r.get("value", "") != ""})
        log.append({"name": name, "dataset": dataset, "label": js.get("label"), "updated": js.get("updated"),
                    "url": url, "rows": len(rows), "bytes": len(body),
                    "first_year": years[0] if years else "", "last_year": years[-1] if years else ""})
        print("%-38s %-13s rows=%-6d %s..%s updated=%s" % (name, dataset, len(rows),
              years[0] if years else "-", years[-1] if years else "-", js.get("updated")))
        time.sleep(1.3)
    logpath = os.path.join(out, "raw", "_fetch_log.json")
    old = []
    if os.path.exists(logpath):
        with open(logpath, encoding="utf-8") as f:
            old = [x for x in json.load(f) if x["name"] not in {l["name"] for l in log}]
    with open(logpath, "w", encoding="utf-8") as f:
        json.dump(old + log, f, indent=1)


if __name__ == "__main__":
    main()
