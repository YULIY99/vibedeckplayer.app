#!/usr/bin/env python3
"""Add the GoatCounter visit counter to every page and a note to the privacy policy.

Idempotent. `--check` exits 1 if any page is missing the counter.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNIPPET = ('<script data-goatcounter="https://vibedeck.goatcounter.com/count" '
           'async src="https://gc.zgo.at/count.js"></script>\n')
MARK = "gc.zgo.at/count.js"

PRIVACY_OLD = """        <h2>Links</h2>"""
PRIVACY_NEW = """        <h2>Website Visits</h2>
        <p>
          This website (vibedeckplayer.app) counts anonymous visits with GoatCounter,
          a privacy-friendly service. It sets no cookies, does not track you across
          sites, and does not store your IP address or any personal profile. It records
          only the page visited, the referring site, country, browser and screen size.
          This applies to the website only; the VibeDeck app itself contains no analytics.
        </p>

        <h2>Links</h2>"""


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).parts
        if rel[0] in ("_build", ".github"):
            continue
        yield p


def main():
    check = "--check" in sys.argv
    missing = []
    changed = 0
    for p in pages():
        h = p.read_text(encoding="utf-8")
        if p.name == "privacy.html" and "Website Visits" not in h:
            h = h.replace(PRIVACY_OLD, PRIVACY_NEW, 1)
            h = h.replace("Last updated: August 14, 2026", "Last updated: October 24, 2026", 1)
        if MARK not in h:
            if "</body>" not in h:
                print("no </body>:", p)
                continue
            h = h.replace("</body>", SNIPPET + "</body>", 1)
        if h != p.read_text(encoding="utf-8"):
            if check:
                missing.append(p)
            else:
                p.write_text(h, encoding="utf-8")
                changed += 1
    if check:
        for p in missing:
            print("missing:", p.relative_to(ROOT))
        sys.exit(1 if missing else 0)
    print("updated", changed, "pages")


main()
