#!/usr/bin/env python3
"""Build data/events_timeline/events.csv from the hand-curated list below.

Every row with verified == "yes" was checked in this session against the official page in
`source_url` (saved copies: data/events_timeline/raw/, fetch log raw/_fetch_log.tsv; pages
were fetched with scripts/events_timeline_fetch.py, vote results with
scripts/events_timeline_votes.py). Rows with verified == "no" are general-knowledge leads
that could not be opened on a reachable official host; they carry NO numbers taken from
memory other than the date itself and must be treated as unverified.

Usage: python3 -I scripts/events_timeline_build.py
"""
import csv

OUT = "/home/user/Diaspora/data/events_timeline/events.csv"
COLS = ["date", "end_date", "date_precision", "title_en", "title_ro", "category",
        "description_en", "expected_effect", "source_url", "source_publisher", "verified"]
CATS = {"free_movement_law", "swiss_vote", "swiss_policy", "romania", "economy", "health",
        "schengen_eu", "bilateral"}

NSB = "https://www.admin.ch/de/nsb?id="
PX_VOTES = "https://www.pxweb.bfs.admin.ch/pxweb/de/px-x-1703030000_100/"

# (date, end_date, precision, title_en, title_ro, category, description_en, expected_effect,
#  source_url, source_publisher, verified)
EVENTS = [
    # EVENTS-BEGIN
    # EVENTS-END
]


def main():
    seen = set()
    rows = []
    for e in EVENTS:
        assert len(e) == len(COLS), e[:4]
        r = dict(zip(COLS, e))
        assert r["category"] in CATS, r
        assert r["verified"] in ("yes", "no"), r
        assert len(r["date"]) == 10 and r["date"][4] == "-" and r["date"][7] == "-", r
        assert r["date_precision"] in ("day", "month", "year"), r
        key = (r["date"], r["title_en"])
        assert key not in seen, key
        seen.add(key)
        rows.append(r)
    rows.sort(key=lambda r: (r["date"], r["title_en"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    n_yes = sum(1 for r in rows if r["verified"] == "yes")
    print("events:", len(rows), "| verified yes:", n_yes, "| no:", len(rows) - n_yes)
    cats = {}
    for r in rows:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    print(cats)


if __name__ == "__main__":
    main()
