#!/usr/bin/env python3
"""Parse table 17 'Arbeitslosenquote seit 2004' (monthly values + annual average) from the text
of SECO's bulletin 'Die Lage auf dem Arbeitsmarkt, Januar 2026' and write context_series.csv.
The text file is produced by:
  python3 -I scripts/events_timeline_fetch.py <URL> seco_lage_arbeitsmarkt_2026-01
Usage: python3 -I scripts/events_timeline_unemployment.py
"""
import csv
import re

URL = "https://www.seco.admin.ch/dam/de/sd-web/3dmYe3hl-IiX/2026-01_Die_Lage_auf_dem_Arbeitsmarkt_DE.pdf"
TXT = "/home/user/Diaspora/data/events_timeline/raw/seco_lage_arbeitsmarkt_2026-01.txt"
OUT = "/home/user/Diaspora/data/events_timeline/context_series.csv"
ROW = re.compile(r"^(\d{4})((?:\s+\d+,\d){13})\s*$")
CAP = re.compile(r"^Tabelle\s*(\d+):\s*(.+)$")


def main():
    cap, blocks = None, {}
    for line in open(TXT, encoding="utf-8"):
        line = line.strip()
        m = CAP.match(line)
        if m:
            cap = (m.group(1), m.group(2))
            continue
        m = ROW.match(line)
        if m and cap:
            blocks.setdefault(cap, []).append((int(m.group(1)), [float(x.replace(",", ".")) for x in m.group(2).split()]))
    for c in blocks:
        print("caption:", c, "rows:", len(blocks[c]))
    key = [c for c in blocks if c[0] == "17" and c[1].startswith("Arbeitslosenquote")][0]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["series", "year", "period", "value", "unit", "source_publisher", "source_table", "source_url"])
        for y, v in blocks[key]:
            for i, x in enumerate(v):
                per = "annual_average" if i == 12 else "M%02d" % (i + 1)
                w.writerow(["ch_registered_unemployment_rate", y, per, x, "percent", "SECO",
                            "Die Lage auf dem Arbeitsmarkt, Januar 2026, Tabelle 17 Arbeitslosenquote seit 2004", URL])
    print("annual:", " ".join("%d=%.1f" % (y, v[12]) for y, v in blocks[key]))


if __name__ == "__main__":
    main()
