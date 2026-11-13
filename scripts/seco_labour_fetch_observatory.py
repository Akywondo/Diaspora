#!/usr/bin/env python3
"""Download the SECO "Observatoriumsbericht zum FZA Schweiz-EU" PDFs (editions 1-22)
listed on https://www.seco.admin.ch/de/observatorium-fza-schweiz-eu and convert each one to
per-page text files (pdftotext -layout), so that they can be grepped for EU-2 / Rumaenien.

Usage: python3 seco_labour_fetch_observatory.py <raw_dir> [min_edition]
Output: <raw_dir>/obs_pdf/obsNN_YYYY.pdf  and <raw_dir>/obs_txt/obsNN_YYYY.txt
        (form-feed separated pages) + <raw_dir>/obs_editions.csv (edition, year, url, pages)
"""
import csv
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

INDEX = "https://www.seco.admin.ch/de/observatorium-fza-schweiz-eu"
UA = {"User-Agent": "Mozilla/5.0"}


def get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # noqa
            code = getattr(e, "code", None)
            print("  retry", i, code, e, file=sys.stderr)
            time.sleep(15 if code in (429, 503) else 4)
    raise RuntimeError("failed " + url)


def main():
    raw = sys.argv[1]
    min_ed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    os.makedirs(os.path.join(raw, "obs_pdf"), exist_ok=True)
    os.makedirs(os.path.join(raw, "obs_txt"), exist_ok=True)
    html = get(INDEX).decode("utf-8", "replace")
    links = sorted(set(re.findall(
        r'https://www\.seco\.admin\.ch/dam/de/sd-web/[^"\\ ]*Observatoriumsbericht[^"\\ ]*?_SECO_\d{4}_DE\.pdf', html)))
    rows = []
    for url in links:
        name = urllib.parse.unquote(url.rsplit("/", 1)[1])
        m = re.match(r"(\d+)[._ ]", name)
        y = re.search(r"SECO_(\d{4})_DE", name)
        ed, year = int(m.group(1)), int(y.group(1))
        if ed < min_ed:
            continue
        pdf = os.path.join(raw, "obs_pdf", "obs%02d_%d.pdf" % (ed, year))
        txt = os.path.join(raw, "obs_txt", "obs%02d_%d.txt" % (ed, year))
        if not os.path.exists(pdf):
            data = get(url)
            with open(pdf, "wb") as f:
                f.write(data)
            time.sleep(1.5)
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
        with open(txt, encoding="utf-8", errors="replace") as f:
            pages = f.read().count("\f")
        rows.append((ed, year, url, pages, os.path.getsize(pdf)))
        print(ed, year, pages, os.path.getsize(pdf))
    rows.sort()
    with open(os.path.join(raw, "obs_editions.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["edition", "publication_year", "url", "pdf_pages", "pdf_bytes"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
