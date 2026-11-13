#!/usr/bin/env python3
"""Helper: list pages of each observatory report text file that mention EU-2 / Romania / Bulgaria.
Usage: python3 -I seco_labour_grep_pages.py <obs_txt_dir> [regex]"""
import glob, os, re, sys
d = sys.argv[1]
rx = re.compile(sys.argv[2] if len(sys.argv) > 2 else r"EU[- ]?2\b|EU2\b|Rumän|Bulgar|BG/RO|RO/BG", re.I)
for fn in sorted(glob.glob(os.path.join(d, "*.txt"))):
    pages = open(fn, encoding="utf-8", errors="replace").read().split("\f")
    hits = [(i + 1, len(rx.findall(p))) for i, p in enumerate(pages) if rx.search(p)]
    print(os.path.basename(fn), "pages=%d" % len(pages), " ".join("%d(%d)" % h for h in hits))
