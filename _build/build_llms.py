"""Build llms.txt and llms-full.txt from the published pages.

Facts live in _build/llms_header.md; page titles, descriptions and FAQs are read
from the HTML (FAQPage JSON-LD matches the visible FAQ 1:1), so the files cannot
drift from the site. Page list and order come from sitemap.xml.

    python3 _build/build_llms.py          # write both files
    python3 _build/build_llms.py --check  # exit 1 if they are out of date
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vibedeckplayer.app"
LANGS = [("en", "English"), ("de", "Deutsch"), ("fr", "Français"), ("it", "Italiano"),
         ("es", "Español"), ("pt-BR", "Português (Brasil)"), ("ja", "日本語"),
         ("ru", "Русский"), ("ko", "한국어"), ("tr", "Türkçe")]
SKIP = {"/support.html", "/privacy.html", "/terms.html"}  # listed under Links


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def page(url):
    path = url[len(SITE):]
    s = read(path.lstrip("/") + "index.html" if path.endswith("/") else path.lstrip("/"))
    meta = lambda r: html.unescape(re.search(r, s, re.S).group(1)).strip()
    faq = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        data = json.loads(block)
        for item in data.get("@graph", [data]) if isinstance(data, dict) else data:
            if item.get("@type") == "FAQPage":
                faq += [(q["name"], q["acceptedAnswer"]["text"]) for q in item["mainEntity"]]
    return dict(url=url, path=path, lang=meta(r'<html[^>]*\blang="([^"]+)"'),
                title=meta(r"<title>(.*?)</title>"),
                desc=meta(r'<meta name="description" content="([^"]*)"'), faq=faq)


def build():
    urls = re.findall(r"<loc>([^<]+)</loc>", read("sitemap.xml"))
    pages = [page(u) for u in urls if u[len(SITE):] not in SKIP]
    header = read("_build/llms_header.md").rstrip() + "\n"
    short, full = [header], [header]
    for code, name in LANGS:
        group = [p for p in pages if p["lang"] == code]
        if not group:
            continue
        heading = "Pages" if code == "en" else f"Pages in {name} ({code})"
        short.append(f"\n## {heading}\n\n" + "".join(f"- [{p['title']}]({p['url']}): {p['desc']}\n" for p in group))
        for p in group:
            body = f"\n## {p['title']}\n\nURL: {p['url']}\nLanguage: {code}\n\n{p['desc']}\n"
            body += "".join(f"\n**Q: {q}**\n\nA: {a}\n" for q, a in p["faq"])
            full.append(body)
    unknown = sorted({p["lang"] for p in pages} - {c for c, _ in LANGS})
    if unknown:
        sys.exit(f"build_llms: add these languages to LANGS: {unknown}")
    return {"llms.txt": "".join(short), "llms-full.txt": "".join(full)}


if __name__ == "__main__":
    out = build()
    stale = [n for n, t in out.items() if not os.path.exists(os.path.join(ROOT, n)) or read(n) != t]
    if "--check" in sys.argv:
        for n in stale:
            print(f"{n} is out of date: run python3 _build/build_llms.py")
        sys.exit(1 if stale else 0)
    for n, t in out.items():
        with open(os.path.join(ROOT, n), "w", encoding="utf-8") as f:
            f.write(t)
    print("wrote", ", ".join(f"{n} ({len(t)} chars)" for n, t in out.items()))
