#!/usr/bin/env python3
"""Build a catalogue of all BFS STAT-TAB (PxWeb) tables and flag those that
carry a nationality / country dimension containing Romania ("Rumänien").

Output: data/_catalog/pxweb_catalog.csv
Source: https://www.pxweb.bfs.admin.ch/api/v1/de/
"""
import csv, json, sys, time, urllib.request, pathlib

BASE = "https://www.pxweb.bfs.admin.ch/api/v1/de/"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "_catalog" / "pxweb_catalog.csv"


def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode("utf-8-sig"))
        except Exception as e:  # rate limit or transient error
            time.sleep(2 + 3 * i)
    return None


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    dbs = get(BASE + "?query=*&filter=*") or []
    ids = sorted({d["dbid"] for d in dbs})
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["table_id", "title", "updated", "has_romania", "romania_variable",
                    "romania_code", "variables", "years"])
        for n, dbid in enumerate(ids, 1):
            listing = get(BASE + dbid)
            time.sleep(0.25)
            if not listing:
                w.writerow([dbid, "", "", "", "", "", "", ""])
                continue
            for t in listing:
                meta = get(f"{BASE}{dbid}/{t['id']}")
                time.sleep(0.25)
                has, var, code, years = "no", "", "", ""
                names = []
                if meta:
                    for v in meta.get("variables", []):
                        names.append(f"{v['text']}[{len(v['values'])}]")
                        for c, txt in zip(v["values"], v["valueTexts"]):
                            if txt.strip() in ("Rumänien", "Rumaenien"):
                                has, var, code = "yes", v["code"], c
                        if v["code"].lower() in ("jahr", "year") or v["text"].lower() == "jahr":
                            years = f"{v['valueTexts'][0]}-{v['valueTexts'][-1]}"
                w.writerow([dbid, t.get("text", ""), t.get("updated", "")[:10], has, var, code,
                            "; ".join(names), years])
            f.flush()
            if n % 50 == 0:
                print(n, "/", len(ids), file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
