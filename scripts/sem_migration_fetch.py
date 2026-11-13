#!/usr/bin/env python3
"""Polite fetch helper for www.sem.admin.ch pages/files (one request at a time, >=1 s pause).

Usage:
  python3 sem_migration_fetch.py page <url> <outfile>      # save a page, print its links
  python3 sem_migration_fetch.py file <url> <outfile>      # save a binary file
"""
import re, subprocess, sys, time, os, html, json

UA = "Mozilla/5.0"

def fetch(url, out, tries=5):
    for i in range(tries):
        r = subprocess.run(["curl", "-sS", "-L", "-m", "120", "-A", UA, "-o", out,
                            "-w", "%{http_code} %{size_download} %{content_type}", url],
                           capture_output=True, text=True)
        code = r.stdout.split(" ")[0] if r.stdout else "000"
        time.sleep(1.2)
        if code in ("429", "503"):
            time.sleep(10 + 5 * i)
            continue
        return r.stdout.strip() + (" ERR " + r.stderr.strip() if r.stderr.strip() else "")
    return "FAILED"

def links(path, pat=None):
    h = open(path, encoding="utf-8", errors="replace").read()
    h = html.unescape(h)
    found = set(re.findall(r'href="([^"]+)"', h))
    # nuxt payload often holds urls as plain strings
    found |= set(re.findall(r'"(/(?:de|fr|en|it)/[^"\s]{3,200})"', h))
    found |= set(re.findall(r'"(https?://[^"\s]{5,300}\.(?:xlsx|xls|pdf|csv|zip)[^"\s]*)"', h))
    found |= set(re.findall(r'"(/dam/[^"\s]{5,300})"', h))
    found |= set(re.findall(r'"(/[^"\s]{5,300}\.(?:xlsx|xls|pdf|csv|zip))"', h))
    out = sorted(found)
    if pat:
        out = [l for l in out if re.search(pat, l, re.I)]
    return out

if __name__ == "__main__":
    mode, url, out = sys.argv[1:4]
    pat = sys.argv[4] if len(sys.argv) > 4 else None
    print(fetch(url, out))
    if mode == "page":
        ls = [l for l in links(out, pat) if not l.startswith("/_nuxt")]
        for l in ls[:150]:
            print(l)
        print("n_links", len(ls))
