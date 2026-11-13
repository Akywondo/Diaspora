#!/usr/bin/env python3
"""Helper: print lines (with context) of given pages / regex from an observatory text file.
Usage: python3 -I seco_labour_show.py <txt> <regex|-> <ctx> [page,page-page ...]"""
import re, sys
fn, rxs, ctx = sys.argv[1], sys.argv[2], int(sys.argv[3])
sel = set()
for a in sys.argv[4:]:
    for part in a.split(","):
        if "-" in part:
            x, y = part.split("-"); sel.update(range(int(x), int(y) + 1))
        elif part:
            sel.add(int(part))
pages = open(fn, encoding="utf-8", errors="replace").read().split("\f")
rx = None if rxs == "-" else re.compile(rxs, re.I)
for i, p in enumerate(pages, 1):
    if sel and i not in sel:
        continue
    lines = [l.rstrip() for l in p.split("\n")]
    if rx is None:
        print("=== p%d ===" % i)
        print("\n".join(l[:230] for l in lines if l.strip()))
        continue
    keep = set()
    for j, l in enumerate(lines):
        if rx.search(l):
            keep.update(range(max(0, j - ctx), min(len(lines), j + ctx + 1)))
    if keep:
        print("=== p%d ===" % i)
        for j in sorted(keep):
            if lines[j].strip():
                print(lines[j][:230])
