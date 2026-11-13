#!/usr/bin/env python3
"""Download official results of the Swiss popular votes that matter for the migration
chronology from BFS STAT-TAB table px-x-1703030000_100 (Volksabstimmungen, Ergebnisse Ebene
Kanton seit 1866) and write data/events_timeline/swiss_votes_results.csv.

Usage: python3 -I scripts/events_timeline_votes.py
"""
import csv
import json
import time
import urllib.request

TABLE = "px-x-1703030000_100"
URL = "https://www.pxweb.bfs.admin.ch/api/v1/de/%s/%s.px" % (TABLE, TABLE)
OUT = "/home/user/Diaspora/data/events_timeline/swiss_votes_results.csv"
RAW = "/home/user/Diaspora/data/events_timeline/raw/px_votes_data.json"
# vote dates of interest (all proposals of these dates are downloaded, then filtered by keyword)
KEYS = ["EWR", "sektoriellen Abkommen", "bilateralen Abkommen", "Schengen", "Personenfreizügigkeit",
        "Freizügigkeitsabkommen", "Osteuropas", "Masseneinwanderung", "Überbevölkerung",
        "Mindestlohn", "Begrenzungsinitiative", "Grenz- und Küstenwache", "10-Millionen",
        "Ausschaffung krimineller", "18 Prozent", "Regelung der Zuwanderung"]


def get(url, body=None):
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    meta = get(URL)
    time.sleep(1.5)
    var = {v["code"]: v for v in meta["variables"]}
    vcode = [c for c in var if c.startswith("Datum")][0]
    sel = [(c, t) for c, t in zip(var[vcode]["values"], var[vcode]["valueTexts"])
           if t[:4] >= "1992" and any(k.lower() in t.lower() for k in KEYS)]
    body = {"query": [
        {"code": "Kanton", "selection": {"filter": "all", "values": ["*"]}},
        {"code": vcode, "selection": {"filter": "item", "values": [c for c, _ in sel]}},
        {"code": "Ergebnis", "selection": {"filter": "all", "values": ["*"]}}],
        "response": {"format": "json-stat2"}}
    d = get(URL, json.dumps(body).encode("utf-8"))
    json.dump(d, open(RAW, "w", encoding="utf-8"))
    dims = d["id"]
    size = d["size"]
    cats = [list(d["dimension"][k]["category"]["index"].keys()) if isinstance(d["dimension"][k]["category"]["index"], dict)
            else d["dimension"][k]["category"]["index"] for k in dims]
    labels = [d["dimension"][k]["category"]["label"] for k in dims]
    vals = d["value"]

    def val(ci, vi, ri):
        idx = [ci, vi, ri]
        pos = 0
        for i, n in enumerate(size):
            pos = pos * n + idx[i]
        return vals[pos]

    ik, iv, ir = dims.index("Kanton"), dims.index(vcode), dims.index("Ergebnis")
    assert (ik, iv, ir) == (0, 1, 2), dims
    res_codes = cats[ir]
    rows = []
    for vi, vc in enumerate(cats[iv]):
        text = labels[iv][vc]
        date, title = text[:10], text[11:]
        ch = {rc: val(cats[ik].index("CH"), vi, ri) for ri, rc in enumerate(res_codes)}
        yes_ix = res_codes.index("7")
        cant_yes = sum(1 for ci, cc in enumerate(cats[ik]) if cc != "CH" and (val(ci, vi, yes_ix) or 0) > 50)
        rows.append({
            "vote_date": date, "bfs_vote_code": vc, "title_de": title,
            "eligible_voters": ch["1"], "votes_cast": ch["2"], "turnout_pct": ch["3"],
            "valid_ballots": ch["4"], "yes_votes": ch["5"], "no_votes": ch["6"], "yes_pct": ch["7"],
            "cantons_with_yes_majority_of_26": cant_yes,
            "outcome": "accepted_by_people" if (ch["7"] or 0) > 50 else "rejected_by_people",
            "source_table": TABLE, "source_url": URL})
    rows.sort(key=lambda r: (r["vote_date"], r["bfs_vote_code"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r["vote_date"], r["yes_pct"], r["turnout_pct"], r["cantons_with_yes_majority_of_26"], r["title_de"][:110])


if __name__ == "__main__":
    main()
