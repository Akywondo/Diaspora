#!/usr/bin/env python3
"""Harvest the list of downloadable files (www.sem.admin.ch/dam/...) from SEM statistics pages
and optionally download them. One request at a time, >=1.2 s pause.

Usage:
  python3 sem_migration_harvest.py manifest <page_url> <page_cache.html> <manifest.csv>
  python3 sem_migration_harvest.py download <manifest.csv> <outdir> [regex-on-filename]
"""
import csv, html, os, re, subprocess, sys, time

UA = "Mozilla/5.0"

def curl(url, out):
    for i in range(5):
        r = subprocess.run(["curl", "-sS", "-L", "-m", "180", "-A", UA, "-o", out,
                            "-w", "%{http_code}", url], capture_output=True, text=True)
        code = r.stdout.strip()
        time.sleep(1.2)
        if code in ("429", "503"):
            time.sleep(10 + 5 * i)
            continue
        return code
    return "FAILED"

def dam_links(path):
    h = html.unescape(open(path, encoding="utf-8", errors="replace").read())
    return sorted(set(re.findall(r'https://www\.sem\.admin\.ch/dam/[^"\s\\]+', h)))

def manifest(page_url, cache, man):
    if not os.path.exists(cache) or os.path.getsize(cache) < 1000:
        code = curl(page_url, cache)
    else:
        code = "cached"
    ls = dam_links(cache)
    new = not os.path.exists(man)
    with open(man, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["page_url", "file_url", "file_name"])
        for l in ls:
            w.writerow([page_url, l, l.rsplit("/", 1)[-1]])
    print(page_url, code, len(ls))

def download(man, outdir, pat=None):
    os.makedirs(outdir, exist_ok=True)
    seen = set()
    for row in csv.DictReader(open(man, encoding="utf-8")):
        fn = row["file_name"]
        if fn in seen or (pat and not re.search(pat, fn)):
            continue
        seen.add(fn)
        out = os.path.join(outdir, fn)
        if os.path.exists(out) and os.path.getsize(out) > 500:
            continue
        code = curl(row["file_url"], out)
        if code != "200":
            print("ERR", code, row["file_url"])
    print("done", len(seen), "files matched")

if __name__ == "__main__":
    if sys.argv[1] == "manifest":
        manifest(*sys.argv[2:5])
    else:
        download(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
