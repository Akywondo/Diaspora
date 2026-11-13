#!/usr/bin/env python3
"""Small BFS STAT-TAB extracts used ONLY to cross-check / label the Eurostat series for Switzerland.

Usage: python3 -I scripts/eurostat_compare_bfs_crosscheck.py /home/user/Diaspora/data/eurostat_compare

1. px-x-0103010000_151  Demografische Bilanz nach Staatsangehoerigkeit (1981-2025), Romania (8232),
   all years x sex x all demographic components  -> bfs_crosscheck_demographic_balance_romania.csv
2. px-x-0103010000_499  Staendige und nichtstaendige Wohnbevoelkerung nach Kanton, Bevoelkerungstyp,
   Staatsangehoerigkeit, Geburtsstaat und Geschlecht (2010-2025), Switzerland, country of birth
   Romania (8232), nationality total / Swiss / Romanian -> bfs_crosscheck_romanian_born_ch.csv
"""
import csv
import json
import os
import sys
import time
import urllib.request

API = "https://www.pxweb.bfs.admin.ch/api/v1/de/%s/%s.px"

JOBS = [
    ("bfs_crosscheck_demographic_balance_romania", "px-x-0103010000_151", [
        ("Jahr", "all", ["*"]),
        ("Staatsangehörigkeit", "item", ["8232"]),
        ("Geschlecht", "item", ["0", "1", "2"]),
        ("Demografische Komponente", "all", ["*"]),
    ]),
    ("bfs_crosscheck_romanian_born_ch", "px-x-0103010000_499", [
        ("Jahr", "all", ["*"]),
        ("Kanton", "item", ["8100"]),
        ("Bevölkerungstyp", "item", ["1", "2"]),
        ("Staatsangehörigkeit", "item", ["-99999", "8100", "8232"]),
        ("Geburtsstaat", "item", ["8232"]),
        ("Geschlecht", "item", ["-99999", "1", "2"]),
    ]),
]

RENAME = {"Jahr": "year", "Staatsangehörigkeit": "nationality", "Geschlecht": "sex",
          "Demografische Komponente": "component", "Kanton": "canton", "Bevölkerungstyp": "population_type",
          "Geburtsstaat": "country_of_birth"}


def post(table, query):
    body = json.dumps({"query": [{"code": c, "selection": {"filter": f, "values": v}} for c, f, v in query],
                       "response": {"format": "json-stat2"}}).encode("utf-8")
    for attempt in range(6):
        req = urllib.request.Request(API % (table, table), data=body,
                                     headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # 429/503 -> back off
            print("retry", attempt, repr(e)[:120])
            time.sleep(15 + 5 * attempt)
    raise RuntimeError("giving up " + table)


def main():
    out = sys.argv[1]
    os.makedirs(os.path.join(out, "raw"), exist_ok=True)
    for name, table, query in JOBS:
        raw = post(table, query)
        with open(os.path.join(out, "raw", name + ".json"), "wb") as f:
            f.write(raw)
        js = json.loads(raw.decode("utf-8"))
        ids, sizes = js["id"], js["size"]
        cats = []
        for d in ids:
            c = js["dimension"][d]["category"]
            order = sorted(c["index"], key=lambda k: c["index"][k])
            cats.append([(k, c["label"][k]) for k in order])
        vals = js["value"]
        with open(os.path.join(out, name + ".csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            head = []
            for d in ids:
                lab = RENAME.get(js["dimension"][d].get("label", d), RENAME.get(d, d))
                head.append(lab)
            w.writerow(["bfs_table"] + head + ["persons"])
            for n, v in enumerate(vals):
                coord, m = [], n
                for s in reversed(sizes):
                    coord.append(m % s)
                    m //= s
                coord.reverse()
                w.writerow([table] + [cats[i][c][1] for i, c in enumerate(coord)] + ["" if v is None else v])
        print(name, table, "cells", len(vals), "updated", js.get("updated"))
        time.sleep(2)


if __name__ == "__main__":
    main()
