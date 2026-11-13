#!/usr/bin/env python3
"""Shared helpers to read SEM (ZEMIS) Ausländerstatistik workbooks. Import with python3 -I
after inserting the scripts dir into sys.path."""
import re, warnings
warnings.filterwarnings("ignore")
import openpyxl

RO = re.compile(r"^\s*(Rum[äa]nien|Roumanie|Romania)\s*$")
CANTONS = "AG AI AR BE BL BS FR GE GL GR JU LU NE NW OW SG SH SO SZ TG TI UR VD VS ZG ZH".split()

def clean(s):
    return re.sub(r"\s+", " ", str(s)).strip()

def sheet_rows(ws, max_rows=400):
    """All rows as lists, merged header cells filled in (not read-only mode)."""
    rows = []
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i >= max_rows:
            break
        rows.append(list(r))
    # fill merged ranges (header only) so that multi-level headers can be combined
    try:
        for mr in ws.merged_cells.ranges:
            if mr.min_row > 15:
                continue
            v = ws.cell(mr.min_row, mr.min_col).value
            for rr in range(mr.min_row, min(mr.max_row, len(rows)) + 1):
                for cc in range(mr.min_col, mr.max_col + 1):
                    if cc - 1 < len(rows[rr - 1]):
                        rows[rr - 1][cc - 1] = v
    except Exception:
        pass
    return rows

def find_row(rows, regex=RO):
    for i, r in enumerate(rows):
        for c in r[:4]:
            if isinstance(c, str) and regex.search(c):
                return i
    return None

def header_labels(rows, first_data_row):
    """Combine the text cells of the header rows above the first numeric data row."""
    # header block = rows between the title (row 0..) and first_data_row that contain strings
    ncol = max(len(r) for r in rows[: first_data_row + 1])
    labels = [""] * ncol
    # find first header row: first row (after row 0) with >=2 non-empty string cells
    start = None
    for i in range(1, first_data_row):
        n = sum(1 for c in rows[i] if isinstance(c, str) and c.strip())
        if n >= 2:
            start = i
            break
    if start is None:
        start = max(0, first_data_row - 3)
    for i in range(start, first_data_row):
        for j, c in enumerate(rows[i]):
            if c is None or (isinstance(c, str) and not c.strip()):
                continue
            # stop header collection when the row is already a data row (numbers)
            if isinstance(c, (int, float)):
                continue
            t = clean(c)
            if labels[j] and labels[j].split(" | ")[-1] == t:
                continue
            labels[j] = (labels[j] + " | " + t) if labels[j] else t
    return labels

def first_data_row(rows):
    """Index of first row that has a string label in col 0..2 and >=2 numeric cells."""
    for i, r in enumerate(rows):
        nums = sum(1 for c in r if isinstance(c, (int, float)) and not isinstance(c, bool))
        strs = [c for c in r[:3] if isinstance(c, str) and c.strip()]
        if nums >= 2 and strs:
            return i
    return None

def extract(path, sheet, regex=RO):
    """Return (title, [(header_label, value), ...]) for the row matching regex in sheet."""
    wb = openpyxl.load_workbook(path, data_only=True)
    if sheet not in wb.sheetnames:
        wb.close()
        return None, None
    ws = wb[sheet]
    rows = sheet_rows(ws)
    wb.close()
    title = None
    for r in rows[:6]:
        for c in r:
            if isinstance(c, str) and len(c.strip()) > 8:
                title = clean(c); break
        if title:
            break
    i = find_row(rows, regex)
    if i is None:
        return title, []
    fd = first_data_row(rows)
    labels = header_labels(rows, fd if fd is not None else i)
    out = []
    for j, c in enumerate(rows[i]):
        if isinstance(c, (int, float)) and not isinstance(c, bool):
            out.append((labels[j] if j < len(labels) else f"col{j}", c))
    return title, out
