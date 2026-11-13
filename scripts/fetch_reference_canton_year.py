#!/usr/bin/env python3
"""Reference extract: Romanian nationals in Switzerland by canton, year,
population type, permit and sex (BFS STATPOP, STAT-TAB table px-x-0103010000_101).

Output: data/_reference/bfs_romanians_canton_year_permit_sex.csv
"""
import csv, json, time, urllib.request, pathlib, itertools

URL = "https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-0103010000_101/px-x-0103010000_101.px"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "_reference"


def call(url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    for i in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8-sig"))
        except Exception as e:
            print("retry", i, e)
            time.sleep(5 + 5 * i)
    raise SystemExit("failed")


meta = call(URL)
var = {v["code"]: v for v in meta["variables"]}
ro = [c for c, t in zip(var["Staatsangehörigkeit"]["values"], var["Staatsangehörigkeit"]["valueTexts"]) if t == "Rumänien"]
tot_nat = var["Staatsangehörigkeit"]["values"][0]
for k, v in var.items():
    print(k, list(zip(v["values"], v["valueTexts"]))[:14])

q = {"query": [
    {"code": "Staatsangehörigkeit", "selection": {"filter": "item", "values": ro}},
    {"code": "Altersklasse", "selection": {"filter": "item", "values": [var["Altersklasse"]["values"][0]]}},
    # variables that are not selected explicitly are eliminated (summed), so list them all
    {"code": "Kanton", "selection": {"filter": "all", "values": ["*"]}},
    {"code": "Bevölkerungstyp", "selection": {"filter": "all", "values": ["*"]}},
    {"code": "Anwesenheitsbewilligung", "selection": {"filter": "all", "values": ["*"]}},
    {"code": "Geschlecht", "selection": {"filter": "all", "values": ["*"]}},
    {"code": "Jahr", "selection": {"filter": "all", "values": ["*"]}},
], "response": {"format": "json-stat2"}}
time.sleep(1)
d = call(URL, q)
dims = d["id"]
print("dims", dims, d["size"])
labels = {k: d["dimension"][k]["category"]["label"] for k in dims}
names = {k: d["dimension"][k].get("label", k) for k in dims}
index = {k: sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1]) for k in dims}
OUT.mkdir(parents=True, exist_ok=True)
COLS = {"Jahr": "year", "Kanton": "canton", "Bevölkerungstyp": "population_type",
        "Anwesenheitsbewilligung": "permit", "Geschlecht": "sex", "Altersklasse": "age_class",
        "Staatsangehörigkeit": "nationality"}
with (OUT / "bfs_romanians_canton_year_permit_sex.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([COLS.get(names[k], names[k]) for k in dims] + ["persons"])
    keys = [[c for c, _ in index[k]] for k in dims]
    for n, combo in enumerate(itertools.product(*keys)):
        w.writerow([labels[k][c] for k, c in zip(dims, combo)] + [d["value"][n]])
print("rows", len(d["value"]), "dims", dims)
