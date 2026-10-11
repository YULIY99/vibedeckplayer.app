#!/usr/bin/env python3
"""Independent READ-ONLY pre-deploy check. Never writes to the repo.
Usage: python3 _build/verify_site.py [--base main] [--live https://vibedeckplayer.app]
Fails (exit 1) on any error, including an unreachable live site."""
import re, json, os, sys, html, subprocess, datetime, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
LIVE, BASE, SITE = arg("--live", "https://vibedeckplayer.app"), arg("--base", "main"), "https://vibedeckplayer.app"
errors, info = [], []
def published(rel):  # GitHub Pages + Jekyll defaults: skip _* and .* paths
    return not any(seg.startswith(("_", ".")) for seg in rel.split("/") if seg)
def resolve(path):
    p = urllib.parse.unquote(path.split("#")[0].split("?")[0]) or "/"
    if not published(p): return None
    f = os.path.join(ROOT, p.lstrip("/"))
    for c in ([os.path.join(f, "index.html")] if p.endswith("/") else [f, f + ".html", os.path.join(f, "index.html")]):
        if os.path.isfile(c): return c
    return None
def live(path):
    try:
        with urllib.request.urlopen(urllib.request.Request(LIVE + path, headers={"User-Agent": "vibedeck-verify"}), timeout=20) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if path == "/404.html": return e.read().decode("utf-8", "replace")
        if e.code == 404:
            return NEW if is_new(path) else errors.append(f"{path}: live 404 but page is not new vs {BASE}")
        return errors.append(f"{path}: live HTTP {e.code}")
    except Exception as e:
        errors.append(f"{path}: live site unreachable ({e.__class__.__name__}); cannot compare"); return None
NEW = object()
def is_new(path):
    f = resolve(path)
    if not f: return False
    rel = os.path.relpath(f, ROOT)
    r = subprocess.run(["git", "-C", ROOT, "cat-file", "-e", f"{BASE}:{rel}"], capture_output=True)
    return r.returncode != 0
def meta(b):
    g = lambda p: (m.group(1).strip() if (m := re.search(p, b, re.S | re.I)) else None)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", b, re.S)
    return {"title": html.unescape(g(r"<title>(.*?)</title>") or ""), "canonical": g(r'<link rel="canonical" href="(.*?)"'),
            "robots": g(r'<meta name="robots" content="(.*?)"'), "h1count": len(h1),
            "h1": re.sub(r"\s+", " ", re.sub("<.*?>", " ", h1[0])).strip() if h1 else None,
            "hreflang": re.findall(r'<link rel="alternate" hreflang="(.*?)" href="(.*?)"', b)}
if os.path.exists(os.path.join(ROOT, ".nojekyll")): errors.append(".nojekyll present: _build/ and _design/ would be PUBLISHED")
# sitemap
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
for d in re.findall(r"<lastmod>(.*?)</lastmod>", sm):
    try: datetime.date.fromisoformat(d) if len(d) == 10 else datetime.datetime.fromisoformat(d.replace("Z", "+00:00"))
    except ValueError: errors.append(f"sitemap: invalid lastmod {d!r}")
sitemap = [u.replace(SITE, "") or "/" for u in re.findall(r"<loc>(.*?)</loc>", sm)]
# all published HTML files (includes 404.html and legacy aliases)
html_files = sorted(os.path.relpath(os.path.join(dp, f), ROOT) for dp, dn, fn in os.walk(ROOT)
                    for f in fn if f.endswith(".html") and published(os.path.relpath(os.path.join(dp, f), ROOT)))
url_of = lambda rel: "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel
urls = sorted(set(sitemap + [url_of(r) for r in html_files] + ["/support", "/privacy", "/terms"]))
self_abs = re.compile(r'(?:href|src|content)="(https://vibedeckplayer\.app/[^"]*)"|"(https://vibedeckplayer\.app/[^"]*)"')
for u in urls:
    f = resolve(u)
    if not f: errors.append(f"{u}: missing locally (would 404)"); continue
    b = open(f, encoding="utf-8").read(); m = meta(b)
    is404 = u == "/404.html"
    if is404:
        if not (m["robots"] and "noindex" in m["robots"]): errors.append("/404.html: must be noindex")
    elif u in sitemap:
        if m["canonical"] != SITE + u: errors.append(f"{u}: canonical {m['canonical']}")
        if m["robots"] and "noindex" in m["robots"]: errors.append(f"{u}: noindex")
    if m["h1count"] != 1: errors.append(f"{u}: {m['h1count']} H1")
    hd = b[b.find("<head>") + 6:b.find("</head>")]
    stray = re.sub(r"<[^>]*>", "", re.sub(r"<script.*?</script>|<style.*?</style>|<title>.*?</title>", "", hd, flags=re.S)).strip()
    if stray: errors.append(f"{u}: stray text in <head> ({stray[:20]!r}) - browsers close <head> early, canonical/meta end up in <body>")
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', b, re.S):
        try: json.loads(j)
        except Exception as e: errors.append(f"{u}: invalid JSON-LD {e}")
    lb = live(u)
    if lb is NEW:
        info.append(f"{u}: new page (not live yet)")
    elif lb:
        lm = meta(lb)
        for k in ("title", "canonical", "robots", "h1"):
            if lm[k] != m[k]: errors.append(f"{u}: {k} changed vs live: {lm[k]!r} -> {m[k]!r}")
    if m["hreflang"]:
        langs = {l for l, _ in m["hreflang"]}
        selfl = [l for l, h in m["hreflang"] if h == SITE + u]
        htmllang = (re.search(r'<html[^>]*lang="([^"]+)"', b) or [None, None])[1]
        if "x-default" not in langs: errors.append(f"{u}: hreflang without x-default")
        if u in sitemap and not selfl: errors.append(f"{u}: hreflang set lacks self-reference")
        if selfl and htmllang and not any(l.lower() == htmllang.lower() for l in selfl if l != "x-default"): errors.append(f"{u}: html lang {htmllang} != hreflang {selfl}")
        if len(m["hreflang"]) != len({l for l, _ in m["hreflang"]}): errors.append(f"{u}: duplicate hreflang codes")
    for lang, href in m["hreflang"]:
        tf = resolve(href.replace(SITE, ""))
        if not tf: errors.append(f"{u}: hreflang {lang} -> {href} missing")
        elif not any(h == SITE + u for _, h in meta(open(tf, encoding="utf-8").read())["hreflang"]): errors.append(f"{u}: hreflang {lang} not reciprocal")
    refs = re.findall(r'(?:href|src)="(/[^/"][^"]*|/)"', b) + [s.strip().split()[0] for ss in re.findall(r'(?:srcset|imagesrcset)="([^"]*)"', b) for s in ss.split(",") if s.strip()]
    refs += [(a or c).replace(SITE, "") or "/" for a, c in self_abs.findall(b)]
    for r in refs:
        if r.startswith("/") and not resolve(r): errors.append(f"{u}: broken internal link {r}")
    for a in re.findall(r'href="(https://(?:apps\.apple\.com|play\.google\.com)[^"]*)"', b):
        a = html.unescape(a); q = urllib.parse.parse_qs(urllib.parse.urlparse(a).query)
        if "play.google.com" in a:
            if q.get("id") != ["com.vibedeck.player"]: errors.append(f"{u}: bad Play link {a}")
            rq = urllib.parse.parse_qs(q.get("referrer", [""])[0])
            if not all(k in rq for k in ("utm_source", "utm_medium", "utm_campaign")): errors.append(f"{u}: Play link without full referrer {a}")
        elif not re.search(r"/id6784724920(\?|$)|/developer/|stdeula", a): errors.append(f"{u}: bad App Store link {a}")
# CSS / manifest / llms references
for rel in ["styles.css", "site.webmanifest", "llms.txt", "llms-full.txt", "robots.txt"]:
    p = os.path.join(ROOT, rel)
    if os.path.exists(p):
        t = open(p, encoding="utf-8").read()
        for r in re.findall(r'url\((/[^)]+)\)|"src":\s*"(/[^"]+)"|https://vibedeckplayer\.app(/[^\s)"\]>]*)', t):
            r = next(x for x in r if x)
            if not resolve(r): errors.append(f"{rel}: broken reference {r}")
# public files removed/renamed vs base
try:
    diff = subprocess.run(["git", "-C", ROOT, "diff", "--name-status", "-M", BASE, "--"], capture_output=True, text=True, check=True).stdout
    removed = [l.split("\t")[1] for l in diff.splitlines() if l[:1] in "DR" and published(l.split("\t")[1])]
    alltext = "\n".join(open(os.path.join(ROOT, r), encoding="utf-8", errors="ignore").read() for r in html_files + ["styles.css", "assets/site.js", "site.webmanifest", "llms.txt", "llms-full.txt"] if os.path.exists(os.path.join(ROOT, r)))
    for r in removed:
        if SITE + "/" + r in sm or "/" + r in alltext or os.path.basename(r) in alltext: errors.append(f"removed public file still referenced or in sitemap: /{r}")
    info.append(f"{len(removed)} public files removed/renamed vs {BASE} (will 404 after deploy), none referenced" if removed else f"no public files removed vs {BASE}")
except Exception as e: errors.append(f"git diff vs {BASE} failed: {e}")
print(f"checked {len(urls)} URLs ({len(html_files)} HTML files) against {LIVE}")
for i in info: print("INFO ", i)
for e in errors: print("ERROR", e)
print("RESULT", "FAIL" if errors else "PASS"); sys.exit(1 if errors else 0)
