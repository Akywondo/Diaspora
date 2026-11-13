#!/usr/bin/env python3
"""Helper: list table/figure captions on pages that mention EU-2/Romania/Osteuropa.
Usage: python3 -I seco_labour_captions.py <txt> ..."""
import re, sys, os
rx = re.compile(r"EU[- ]?2\b|EU2\b|Rumän|Bulgar|Osteurop|EU8\+2|EU-?10|EU-?17", re.I)
cap = re.compile(r"(Tabelle|Tab\.|Abb\.|Abbildung|Grafik|Kasten)\s*[A-Z]?\d+(\.\d+)?[a-z]?\s*:")
for fn in sys.argv[1:]:
    pages = open(fn, encoding="utf-8", errors="replace").read().split("\f")
    print("#####", os.path.basename(fn))
    for i, p in enumerate(pages, 1):
        if not rx.search(p):
            continue
        for l in p.split("\n"):
            m = cap.search(l)
            if m:
                print("p%d: %s" % (i, l[m.start():m.start() + 150].strip()))
