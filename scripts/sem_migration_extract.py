#!/usr/bin/env python3
"""Extract the rows 'Rumänien', 'Bulgarien' and 'Gesamttotal' from SEM (ZEMIS) Ausländerstatistik
workbooks into one long CSV with the original German column headers.

Usage: python3 -I sem_migration_extract.py <out.csv> <dir1> [<dir2> ...]
"""
import csv, os, re, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl

CANT = "AG AI AR BE BL BS FR GE GL GR JU LU NE NW OW SG SH SO SZ TG TI UR VD VS ZG ZH".split()
WANT = {"Rumänien": "Romania", "Bulgarien": "Bulgaria", "Gesamttotal": "all_foreigners"}

def clean(s):
    return re.sub(r"\s+", " ", str(s).replace("-\n", "").replace("\n", " ")).strip()

def isnum(c):
    return isinstance(c, (int, float)) and not isinstance(c, bool)

def read_sheet(ws, maxrows=260):
    rows = []
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i >= maxrows:
            break
        rows.append(list(r))
    return rows

def labels_for(rows):
    """Multi-level header labels: rows between the title and the first numeric data row."""
    fd = None
    for i, r in enumerate(rows):
        if sum(1 for c in r if isnum(c)) >= 2 and any(isinstance(c, str) and c.strip() for c in r[:3]):
            fd = i
            break
    if fd is None:
        return None, None, []
    title_i = None
    for i in range(fd):
        if any(isinstance(c, str) and len(c.strip()) > 12 for c in rows[i]):
            title_i = i
            break
    title = clean(next(c for c in rows[title_i] if isinstance(c, str) and len(c.strip()) > 12)) if title_i is not None else ""
    hdr = [r for r in rows[(title_i + 1 if title_i is not None else 0):fd] if any(c is not None and str(c).strip() for c in r)]
    ncol = max(len(r) for r in rows[: fd + 1])
    upper = [""] * ncol
    for k, r in enumerate(hdr):
        r = r + [None] * (ncol - len(r))
        last = k == len(hdr) - 1
        cur = ""; prev_upper = None
        new = list(upper)
        for j in range(1, ncol):
            v = r[j]
            if upper[j] != prev_upper:
                cur = ""
            prev_upper = upper[j]
            if v is not None and str(v).strip():
                cur = clean(v)
                lab = cur
            else:
                lab = "" if (last and len(hdr) > 1) else cur
            if lab:
                new[j] = (upper[j] + " | " + lab) if upper[j] else lab
        upper = new
    return title, fd, upper

def main(out, dirs):
    w = csv.writer(open(out, "w", newline="", encoding="utf-8"))
    w.writerow(["period", "table", "file", "sheet", "row_label", "col_idx", "column_label", "value", "table_title"])
    for d in dirs:
        for fn in sorted(os.listdir(d)):
            m = re.match(r"^(\d-\d\d)-(.*?)-(\d{4})-(\d\d)(-d)?\.xlsx$", fn)
            if not m:
                continue
            table = m.group(1) + "-" + m.group(2); period = f"{m.group(3)}-{m.group(4)}"
            wb = openpyxl.load_workbook(os.path.join(d, fn), read_only=True, data_only=True)
            sheets = [s for s in wb.sheetnames if s not in CANT and re.search(r"nati", s, re.I)]
            if table.startswith("2-10") :
                sheets += [s for s in wb.sheetnames if s in CANT]
            if not sheets:
                print("NO NATI SHEET", fn, wb.sheetnames[:4])
            for sn in sheets:
                rows = read_sheet(wb[sn])
                title, fd, labs = labels_for(rows)
                if fd is None:
                    print("NO DATA", fn, sn); continue
                for r in rows[fd:]:
                    lab = next((clean(c) for c in r[:2] if isinstance(c, str) and c.strip()), None)
                    if lab in WANT:
                        if sn in CANT and lab != "Rumänien":
                            continue
                        for j, c in enumerate(r):
                            if isnum(c):
                                w.writerow([period, table, fn, sn, WANT[lab], j, labs[j] if j < len(labs) else "", c, title])
            wb.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
