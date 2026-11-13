#!/usr/bin/env python3
"""Small helper for the BFS STAT-TAB (PxWeb) API.

Usage from other scripts:  from pxweb import meta, fetch, write_csv
Source: https://www.pxweb.bfs.admin.ch/api/v1/de/<table>/<table>.px
"""
import csv, itertools, json, pathlib, time, urllib.request

BASE = "https://www.pxweb.bfs.admin.ch/api/v1/de/{t}/{t}.px"
_last = [0.0]


def _call(url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    for i in range(7):
        wait = 1.2 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode("utf-8-sig"))
        except Exception as e:  # 429 / transient
            print("  retry", i, type(e).__name__, str(e)[:120])
            time.sleep(8 + 6 * i)
    raise SystemExit(f"failed: {url}")


def meta(table):
    """Return {code: {'text':..., 'values': {code: label}}} preserving order."""
    m = _call(BASE.format(t=table))
    out = {}
    for v in m["variables"]:
        out[v["code"]] = {"text": v["text"], "values": dict(zip(v["values"], v["valueTexts"])),
                          "elimination": v.get("elimination", False)}
    return m["title"], out


def code_of(variables, var, label):
    for c, t in variables[var]["values"].items():
        if t == label:
            return c
    raise KeyError(f"{label!r} not in {var}")


def fetch(table, selection):
    """selection: {var_code: list_of_value_codes or '*'}; variables not listed are eliminated."""
    q = []
    for code, vals in selection.items():
        if vals == "*":
            q.append({"code": code, "selection": {"filter": "all", "values": ["*"]}})
        else:
            q.append({"code": code, "selection": {"filter": "item", "values": list(vals)}})
    d = _call(BASE.format(t=table), {"query": q, "response": {"format": "json-stat2"}})
    dims = d["id"]
    names = [d["dimension"][k].get("label", k) for k in dims]
    labels = [d["dimension"][k]["category"]["label"] for k in dims]
    order = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])]
             for k in dims]
    rows = []
    for n, combo in enumerate(itertools.product(*order)):
        rows.append([labels[i][c] for i, c in enumerate(combo)] + [d["value"][n]])
    return names + ["value"], rows


def write_csv(path, header, rows):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", path, len(rows), "rows")
