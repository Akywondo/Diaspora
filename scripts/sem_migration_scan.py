#!/usr/bin/env python3
"""Scan a directory of SEM xlsx files: one line per file (sheet count, non-canton sheet
names, title of the nationality sheet, whether a Rumänien row exists). Run with python3 -I."""
import sys, os, re, warnings
warnings.filterwarnings("ignore")
import openpyxl

CANT = set("AG AI AR BE BL BS FR GE GL GR JU LU NE NW OW SG SH SO SZ TG TI UR VD VS ZG ZH".split())

def scan(d, pat=None):
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".xlsx") or (pat and not re.search(pat, fn)):
            continue
        try:
            wb = openpyxl.load_workbook(os.path.join(d, fn), read_only=True, data_only=True)
        except Exception as e:
            print(fn, "ERR", e); continue
        names = wb.sheetnames
        other = [s for s in names if s not in CANT]
        info = []
        for sn in other[:4]:
            ws = wb[sn]
            title = None; ro = None; n = 0
            for r in ws.iter_rows(values_only=True):
                n += 1
                for c in r:
                    if isinstance(c, str):
                        if title is None and len(c.strip()) > 8:
                            title = re.sub(r"\s+", " ", c.strip())[:95]
                        if ro is None and re.search(r"Rum[äa]nien|Roumanie|Romania", c):
                            ro = n
            info.append(f"[{sn}: rows={n} RO={ro} '{title}']")
        print(f"{fn[:40]:40} sheets={len(names)} cant={len(names)-len(other)} " + " ".join(info))
        wb.close()

if __name__ == "__main__":
    scan(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
