#!/usr/bin/env python3
"""Fetch ONE official page/PDF, store it under data/events_timeline/raw/, convert it to
plain text and print only the lines matching a regex (so that whole pages never have to be
read). Used to verify every row of events.csv against the page it cites.

Usage:
  python3 -I scripts/events_timeline_fetch.py URL NAME [REGEX] [--ctx 0] [--max 40] [--links REGEX]

NAME is the file stem inside raw/ (extension is added from the content type).
The fetch log (name, url, final url, status, bytes, date) is appended to raw/_fetch_log.tsv.
"""
import argparse
import datetime
import html
import os
import re
import sys
import time

RAW = "/home/user/Diaspora/data/events_timeline/raw"


def fetch(url, tries=5):
    """Download with the system curl and its DEFAULT user agent (www.admin.ch and
    www.eda.admin.ch answer 403 to a bare "Mozilla/5.0" agent but 200 to plain curl)."""
    import subprocess
    import tempfile
    last = ""
    for i in range(tries):
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tmp = tf.name
        try:
            r = subprocess.run(
                ["curl", "-sS", "-L", "-m", "90", "-H", "Accept-Language: de,en;q=0.8",
                 "-o", tmp, "-w", "%{http_code}\t%{url_effective}\t%{content_type}", url],
                capture_output=True, text=True, timeout=120)
            parts = (r.stdout or "").split("\t")
            code = int(parts[0]) if parts and parts[0].isdigit() else 0
            final = parts[1] if len(parts) > 1 else url
            ctype = parts[2] if len(parts) > 2 else ""
            with open(tmp, "rb") as f:
                body = f.read()
            last = r.stderr
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        if code in (429, 503):
            time.sleep(15 + 5 * i)
            continue
        if code == 0:
            return 0, url, "", last.encode()
        return code, final, ctype, body
    return 0, url, "", last.encode()


def nuxt_strings(s):
    """The new federal sites (admin.ch/de/nsb, sem.admin.ch, seco.admin.ch ...) are Nuxt apps:
    the article body sits in the JSON payload <script id="__NUXT_DATA__">, not in the markup.
    Return the long text strings of that payload as HTML fragments."""
    import json
    out = []
    for m in re.finditer(r'(?is)<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>', s):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        if isinstance(data, list):
            for x in data:
                if isinstance(x, str) and len(x) >= 60 and (" " in x) and not x.startswith(("http", "/", "{", "[")):
                    out.append("<p>" + x + "</p>")
    return "\n".join(out)


def html_to_text(raw):
    s = raw.decode("utf-8", "replace")
    s = s + "\n<p>=== NUXT PAYLOAD TEXT ===</p>\n" + nuxt_strings(s)
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</h[1-6]>|</tr>|</td>|</th>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("\xa0", " ").replace(" ", " ").replace(" ", " ")
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in s.split("\n")]
    return "\n".join(l for l in lines if l)


def pdf_to_text(path):
    import pdfplumber
    out = []
    with pdfplumber.open(path) as pdf:
        for i, p in enumerate(pdf.pages):
            out.append("[page %d]" % (i + 1))
            out.append(p.extract_text() or "")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("name")
    ap.add_argument("regex", nargs="?")
    ap.add_argument("--ctx", type=int, default=0)
    ap.add_argument("--max", type=int, default=40)
    ap.add_argument("--links", help="print hrefs matching this regex")
    ap.add_argument("--width", type=int, default=420)
    a = ap.parse_args()

    os.makedirs(RAW, exist_ok=True)
    status, final, ctype, body = fetch(a.url)
    time.sleep(1.2)
    is_pdf = body[:4] == b"%PDF"
    ext = ".pdf" if is_pdf else ".html"
    path = os.path.join(RAW, a.name + ext)
    if status == 200 and len(body) <= 8 * 1024 * 1024:
        with open(path, "wb") as f:
            f.write(body)
    with open(os.path.join(RAW, "_fetch_log.tsv"), "a", encoding="utf-8") as f:
        f.write("\t".join([a.name + ext, a.url, final, str(status), str(len(body)),
                           datetime.date.today().isoformat()]) + "\n")
    print("STATUS", status, "| bytes", len(body), "| final", final[:200])
    if status != 200:
        print(body[:200].decode("utf-8", "replace"))
        return 1
    text = pdf_to_text(path) if is_pdf else html_to_text(body)
    with open(os.path.join(RAW, a.name + ".txt"), "w", encoding="utf-8") as f:
        f.write(text)
    if not is_pdf:
        m = re.search(r"(?is)<title[^>]*>(.*?)</title>", body.decode("utf-8", "replace"))
        if m:
            print("TITLE", html.unescape(m.group(1)).strip()[:200])
    lines = text.split("\n")
    print("LINES", len(lines))
    if a.links and not is_pdf:
        hrefs = re.findall(r'href="([^"]+)"', body.decode("utf-8", "replace"))
        seen = []
        for h in hrefs:
            if re.search(a.links, h) and h not in seen:
                seen.append(h)
        for h in seen[: a.max]:
            print("LINK", html.unescape(h)[:300])
    if a.regex:
        rx = re.compile(a.regex, re.I)
        n = 0
        shown = set()
        for i, l in enumerate(lines):
            if rx.search(l):
                for j in range(max(0, i - a.ctx), min(len(lines), i + a.ctx + 1)):
                    if j not in shown:
                        shown.add(j)
                        print("%5d: %s" % (j, lines[j][: a.width]))
                n += 1
                if n >= a.max:
                    break
    return 0


if __name__ == "__main__":
    sys.exit(main())
