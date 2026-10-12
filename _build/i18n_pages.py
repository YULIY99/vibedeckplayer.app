#!/usr/bin/env python3
"""Generates localized landing pages (ja, es, pt-BR) from _build/i18n_content.py and wires
hreflang into their English equivalents + sitemap. Idempotent. Does NOT touch other pages.
Run: python3 _build/i18n_pages.py"""
import os, re, json, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from i18n_content import PAGES, APPLE
from i18n_extra import EXTRA
for _p in PAGES:
    _x = EXTRA.get(_p["path"])
    if _x:
        _p["prose"] = _p["prose"].split("<h2>VibeDeck Studio")[0]
        _p["faq"] = list(_p["faq"]) + _x["faq_more"]
        _p["related"] = list(_p["related"]) + _x["related_more"]
        _p.update({k: v for k, v in _x.items() if k not in ("faq_more", "related_more")})
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vibedeckplayer.app"
E = lambda s: html.escape(s, quote=True)
TPL = open(os.path.join(ROOT, "change-song-key-iphone/index.html"), encoding="utf-8").read()
# Official store badges (unmodified artwork), one pair per language. Widths at 48px height.
BADGE = {"ja": ("ja", 131, 162), "es": ("es", 144, 162), "pt-BR": ("pt-br", 144, 162), "de": ("de", 144, 162), "fr": ("fr", 152, 162)}
WAVE = re.search(r'<div class="wave" aria-hidden="true">.*?</div>', TPL, re.S).group(0)
IMG = {"now-playing": ("vibedeck-offline-music-player-iphone-now-playing", (400, 600, 800), 600, 1300, "(min-width: 1024px) 288px, 76vw"),
       "b-pitch": ("vibedeck-pitch-control-iphone", (360, 540, 720), 540, 1170, "(min-width: 1024px) 288px, 76vw"),
       "pitch-filter": ("vibedeck-pitch-filter-iphone", (400, 600, 800), 600, 1300, "(min-width: 1024px) 288px, 76vw"),
       "aura": ("vibedeck-flac-player-iphone-aura", (400, 600, 800), 600, 1300, "(min-width: 1024px) 288px, 76vw")}
UI = {"ja": {"logo": "VibeDeck Playerのロゴ", "overview": "概要", "company": "VibeDeckについて", "crumbs": "パンくずリスト", "en": "（英語）"},
      "es": {"logo": "Logotipo de VibeDeck Player", "overview": "Resumen", "company": "Información de VibeDeck", "crumbs": "Ruta de navegación", "en": " (en inglés)"},
      "pt-BR": {"logo": "Logotipo do VibeDeck Player", "overview": "Visão geral", "company": "Institucional", "crumbs": "Trilha de navegação", "en": " (em inglês)"},
      "de": {"logo": "Logo von VibeDeck Player", "overview": "Überblick", "company": "Über VibeDeck", "crumbs": "Brotkrumen-Navigation", "en": " (auf Englisch)"},
      "fr": {"logo": "Logo de VibeDeck Player", "overview": "Aperçu", "company": "À propos de VibeDeck", "crumbs": "Fil d’Ariane", "en": " (en anglais)"}}
LANG_NAMES = [("en", "English"), ("ja", "日本語"), ("es", "Español"), ("pt-BR", "Português"), ("de", "Deutsch"), ("fr", "Français")]
def W(x): return E(x).replace("|", "<wbr>")
def srcset(k, ext): n, ws, *_ = IMG[k]; return ", ".join(f"/assets/img/{n}-{w}.{ext} {w}w" for w in ws)
def pic(k, alt, lazy):
    n, ws, w, h, sizes = IMG[k]
    extra = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{srcset(k,"avif")}" sizes="{sizes}"><source type="image/webp" srcset="{srcset(k,"webp")}" sizes="{sizes}">'
            f'<img src="/assets/img/{n}-{w}.webp" alt="{E(alt)}" width="{w}" height="{h}" {extra}></picture>')
def play(p): return f'https://play.google.com/store/apps/details?id=com.vibedeck.player&amp;hl={p["play_hl"]}&amp;referrer=utm_source%3Dvibedeckplayer.app%26utm_medium%3Dwebsite%26utm_campaign%3D{p["campaign"]}'
def stores(p):
    k, wa, wg = BADGE[p["lang"]]
    sep = "" if p["lang"] == "ja" else " "
    def badge(href, aria, img, alt, w):
        return (f'<a class="store-badge" href="{href}" aria-label="{E(aria)}"><img src="/assets/badges/{img}-{k}.svg" '
                f'alt="{E(alt)}" width="{w}" height="48" decoding="async"></a>')
    b = [badge(f'{APPLE}?pt=129091862&amp;ct={p["campaign"]}&amp;mt=8', p["aria"][0], "app-store", p["store_small"][0] + sep + p["store_strong"][0], wa),
         badge(play(p), p["aria"][1], "google-play", p["store_small"][1] + sep + p["store_strong"][1], wg)]
    return '<div class="stores">' + "".join(b[::-1] if p.get("android") else b) + '</div>'  # own platform first
def clusters():
    """English URL -> {lang: url} for every localized page."""
    c = {}
    for p in PAGES: c.setdefault(p["en"], {"en": p["en"]})[p["lang"]] = p["path"]
    return c
def alt_links(group):
    out = [f'<link rel="alternate" hreflang="{l}" href="{SITE}{u}">' for l, u in sorted(group.items(), key=lambda x: [n for n, _ in LANG_NAMES].index(x[0]))]
    return "\n".join(out + [f'<link rel="alternate" hreflang="x-default" href="{SITE}{group["en"]}">'])
def switcher(group, current, label):
    items = []
    for l, name in LANG_NAMES:
        if l in group:
            items.append(f'<span aria-current="true" lang="{l}">{name}</span>' if l == current else f'<a href="{group[l]}" hreflang="{l}" lang="{l}">{name}</a>')
    return f'<nav class="lang-switch" aria-label="{E(label)}">' + " · ".join(items) + "</nav>"
def ld(p, home):
    url = SITE + p["path"]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "VibeDeck", "item": SITE + home}]
    if p["path"] != home: crumbs.append({"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url})
    g = [{"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": p["lang"],
          "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#app"}},
         {"@type": "MobileApplication", "@id": SITE + "/#app", "name": "VibeDeck Player", "applicationCategory": "MusicApplication",
          "operatingSystem": "iOS 17.0 or later, iPadOS, Android", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "downloadUrl": [APPLE, "https://play.google.com/store/apps/details?id=com.vibedeck.player"],
          "sameAs": [APPLE, "https://play.google.com/store/apps/details?id=com.vibedeck.player"]},
         {"@type": "BreadcrumbList", "itemListElement": crumbs},
         {"@type": "FAQPage", "inLanguage": p["lang"], "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]
    return json.dumps({"@context": "https://schema.org", "@graph": g}, indent=1, ensure_ascii=False)
def extra_top(p, hs):
    if "features" not in p: return ""
    f = "".join(f'<li class="panel glass" data-reveal style="--rd:{(i%3)*90}ms"><span class="num" aria-hidden="true">0{i+1}</span><p class="tag">{E(t)}</p><h3{hs}>{W(h)}</h3><p>{E(d)}</p></li>' for i, (t, h, d) in enumerate(p["features"]))
    st = "".join(f'<li class="panel glass" data-reveal style="--rd:{(i%3)*90}ms"><span class="num" aria-hidden="true">0{i+1}</span><h3{hs}>{W(h)}</h3><p>{E(d)}</p></li>' for i, (h, d) in enumerate(p["studio"]))
    why = "".join(f"<p>{x}</p>" for x in p["why"])
    chips = "".join(f"<li>{E(c)}</li>" for c in p["chips"])
    return f'''
<section class="section" id="features" aria-labelledby="more-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">VibeDeck <span class="dim">/ {len(p["features"]):02d}</span></p><h2 class="h2" id="more-title"{hs}>{W(p["features_h2"])}</h2></div></div>
    <ul class="panels">{f}</ul>
  </div>
</section>

<section class="section" id="studio" aria-labelledby="studio-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Studio <span class="dim">/ iPhone · iPad</span></p><h2 class="h2" id="studio-title"{hs}>{W(p["studio_h2"])}</h2></div><p class="lede">{E(p["studio_lede"])}</p></div>
    <ul class="panels">{st}</ul>
  </div>
</section>

<section class="section" id="why" aria-labelledby="why-title">
  <div class="wrap duo duo--rev">
    <div class="duo-copy prose" data-reveal>
      <p class="tag eyebrow">VibeDeck</p>
      <h2 id="why-title"{hs}>{W(p["why_h2"])}</h2>
      {why}
    </div>
    <div class="duo-media media-solo">
      <div class="halo" aria-hidden="true"></div>
      <div class="phone " data-parallax="0.05">{pic("b-pitch", p["alt"], True)}</div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="specs-title">
  <div class="wrap specs" data-reveal>
    <h2 id="specs-title">{E(p["specs_h2"])}</h2>
    <ul class="chips">{chips}</ul>
  </div>
</section>
'''
def extra_bottom(p, hs):
    if "plans" not in p: return ""
    n = len(p["plans"])
    plans = "".join(f'<li class="plan glass{" plan--hi" if i == n-1 else ""}" data-reveal style="--rd:{i*90}ms">' + (f'<span class="badge mono">{E(p["plan_badge"])}</span>' if i == n-1 else "") + f'<h3{hs}>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(p["plans"]))
    rows = "".join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in p["glance"])
    return f'''
<section class="section" id="premium" aria-labelledby="premium-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Premium</p><h2 class="h2" id="premium-title">VibeDeck Premium</h2></div><p class="lede">{E(p["premium_lede"])}</p></div>
    <ul class="plans">{plans}</ul><p class="note">{E(p["premium_note"])}</p>
  </div>
</section>

<section class="section">
  <div class="wrap"><div class="glass box prose" data-reveal><h2{hs}>{E(p["glance_h2"])}</h2><div class="table-wrap"><table><tbody>{rows}</tbody></table></div></div></div>
</section>
'''
def page(p):
    home = p.get("home", p["path"]); group = clusters()[p["en"]]; url = SITE + p["path"]
    n, ws, w, h, sizes = IMG[p["img"]]
    h1style = ' style="word-break:keep-all;overflow-wrap:anywhere"' if p["lang"] == "ja" else ""
    hs = h1style
    panels = "".join(f'<li class="panel glass" data-reveal style="--rd:{i*90}ms"><span class="num" aria-hidden="true">0{i+1}</span><h3{hs}>{W(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(p["panels"]))
    faq = "".join(f'<details><summary><h3{hs}>{W(q)}</h3></summary><div class="a"><p>{E(a)}</p></div></details>' for q, a in p["faq"])
    rel = "".join(f'<li data-reveal style="--rd:{i*90}ms"><a class="card glass" href="{u}"{" hreflang=\"en\" lang=\"en\"" if t=="English" else ""}><span class="tag">{E(t)}</span><h3>{E(h3)}</h3><p>{E(d)}</p><span class="go mono"><span aria-hidden="true">→</span></span></a></li>' for i, (u, t, h3, d) in enumerate(p["related"]))
    crumbs = f'<li><a href="{home}">{E("VibeDeck")}</a></li>' + (f'<li aria-current="page">{E(p["crumb"])}</li>' if p["path"] != home else "")
    fl = p["foot_links"]
    crumbs_nav = f'<nav aria-label="{E(UI[p["lang"]]["crumbs"])}"><ol class="crumbs mono">{crumbs}</ol></nav>\n' if p["path"] != home else ""
    h1 = E(p["h1"]).replace("|", "<wbr>")
    h1sub = E(p["h1sub"]).replace("|", "<wbr>")
    return f'''<!doctype html>
<html lang="{p["lang"]}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["desc"])}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
{alt_links(group)}
<meta name="theme-color" content="#04070d">
<meta name="color-scheme" content="dark">
<meta name="apple-itunes-app" content="app-id=6784724920">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VibeDeck Player">
<meta property="og:locale" content="{p["og"]}">
<meta property="og:title" content="{E(p["title"])}">
<meta property="og:description" content="{E(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/vibedeck-og-1200x630.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(p["alt"])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(p["title"])}">
<meta name="twitter:description" content="{E(p["desc"])}">
<meta name="twitter:image" content="{SITE}/assets/img/vibedeck-og-1200x630.jpg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" type="image/avif" imagesrcset="{srcset(p["img"],"avif")}" imagesizes="{sizes}" fetchpriority="high">
<link rel="stylesheet" href="/styles.css?v=12">
<script>document.documentElement.className="js"</script>
<script src="/assets/site.js?v=2" defer></script>
<script type="application/ld+json">
{ld(p, home)}
</script>
</head>

<body>
<a class="skip" href="#main">{E(p["skip"])}</a>
<header class="site-header">
  <div class="wrap header-wrap">
    <a class="brand" href="{home}" aria-label="{E(p["home_aria"])}"><img src="/assets/vibedeck-logo-header.webp" alt="{E(UI[p["lang"]]["logo"])}" width="32" height="32"><span class="brand-name">VibeDeck</span></a>
    <nav class="nav mono" aria-label="{E(p["foot_lang"])}"><a href="{p["en"]}" hreflang="en" lang="en">English</a></nav>
    <a class="btn-dl" href="#download">{E(p["dl"])}</a>
  </div>
</header>
<main id="main">
<section class="hero hero--sub" aria-labelledby="hero-title">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      {crumbs_nav}      <p class="tag eyebrow">{E(p["eyebrow"])}</p>
      <h1 id="hero-title"{h1style}><span class="h1-plain">{h1}</span> <span class="h1-sub">{h1sub}</span></h1>
      <p class="lede">{E(p["lede"])}</p>
      {stores(p)}
      <p class="dim" style="margin-top:16px">{E(p["note"])}</p>
    </div>
    <div class="hero-visual">
      <div class="halo" aria-hidden="true"></div>
      {WAVE}
      <figure class="poster" data-parallax="0.04">{pic(p["img"], p["alt"], False)}</figure>
    </div>
  </div>
</section>

<section class="section statement statement--small" aria-label="{E(UI[p["lang"]]["overview"])}">
  <div class="wrap" data-reveal><p>{E(p["statement"])}</p></div>
</section>

<section class="section" aria-labelledby="features-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">VibeDeck <span class="dim">/ 03</span></p><h2 class="h2" id="features-title"{hs}>{W(p["panels_h2"])}</h2></div></div>
    <ul class="panels">{panels}</ul>
  </div>
</section>

{extra_top(p, hs)}<section class="section">
  <div class="wrap"><div class="glass box prose" data-reveal>{p["prose"]}</div></div>
</section>{extra_bottom(p, hs)}
<section class="section" id="faq" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">FAQ <span class="dim">/ {len(p["faq"]):02d}</span></p><h2 class="h2" id="faq-title"{hs}>{W(p["faq_h2"])}</h2></div></div>
    <div class="faq" data-reveal>{faq}</div>
  </div>
</section>

<section class="section" id="related" aria-labelledby="related-title">
  <div class="wrap">
    <ul class="cards">{rel}</ul>
  </div>
</section>

<section class="section" id="download" aria-labelledby="download-title">
  <div class="wrap">
    <div class="cta" data-reveal>
      <div class="cta-grid">
        <div class="cta-copy">
          <p class="tag">{E(p["dl"])} <span class="dim">/ iOS · Android</span></p>
          <h2 class="h2" id="download-title"{hs}>{W(p["cta_h2"])}</h2>
          <p class="lede">{E(p["cta_lede"])}</p>
          {stores(p)}
        </div>
        <div class="cta-media"><div class="phone phone--sm" data-parallax="0.05">{pic(p["img2"], p["alt2"], True)}</div></div>
      </div>
    </div>
  </div>
</section>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="{home}" aria-label="{E(p["home_aria"])}"><img src="/assets/vibedeck-logo-header.webp" alt="{E(UI[p["lang"]]["logo"])}" width="32" height="32" loading="lazy"><span class="brand-name">VibeDeck</span></a>
        <p>{E(p["foot"])}</p>
      </div>
      <nav aria-label="{E(p["foot_lang"])}"><h2>{E(p["foot_lang"])}</h2><ul>{"".join(f'<li><a href="{u}" hreflang="{l}" lang="{l}">{dict(LANG_NAMES)[l]}</a></li>' for l, u in group.items())}</ul></nav>
      <nav aria-label="{E(UI[p["lang"]]["company"])}"><h2>VibeDeck</h2><ul>
        <li><a href="/support.html" hreflang="en">{E(fl[0])}{UI[p["lang"]]["en"]}</a></li><li><a href="/privacy.html" hreflang="en">{E(fl[1])}{UI[p["lang"]]["en"]}</a></li><li><a href="/terms.html" hreflang="en">{E(fl[2])}{UI[p["lang"]]["en"]}</a></li>
        <li><a href="mailto:hello@vibedeckplayer.app">hello@vibedeckplayer.app</a></li></ul></nav>
    </div>
    <div class="foot-base mono"><span>© 2026 VibeDeck</span><span>{E(p["foot_base"])}</span></div>
    <p class="foot-legal">Apple, the Apple logo, iPhone and iPad are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc. Google Play and the Google Play logo are trademarks of Google LLC.</p>
  </div>
</footer>
</body>
</html>
'''
def wire_english():
    for en, group in clusters().items():
        f = os.path.join(ROOT, en.lstrip("/"), "index.html")
        s = open(f, encoding="utf-8").read()
        s = re.sub(r'\n<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", s)
        s = re.sub(r'<nav class="lang-switch"[^>]*>.*?</nav>', "", s)
        canon = re.search(r'<link rel="canonical" href="[^"]*">', s).group(0)
        s = s.replace(canon, canon + "\n" + alt_links(group), 1)
        s = s.replace('<span>No ads · No account · No tracking</span></div>',
                      '<span>No ads · No account · No tracking</span>' + switcher(group, "en", "Language") + '</div>', 1)
        open(f, "w", encoding="utf-8").write(s)
def sitemap():
    f = os.path.join(ROOT, "sitemap.xml"); s = open(f, encoding="utf-8").read()
    s = s.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    s = re.sub(r'\n    <xhtml:link [^>]*/>', "", s)
    for p in PAGES:
        if f"<loc>{SITE}{p['path']}</loc>" not in s:
            s = s.replace("</urlset>", f"  <url>\n    <loc>{SITE}{p['path']}</loc>\n    <lastmod>2026-10-11</lastmod>\n    <priority>0.7</priority>\n  </url>\n</urlset>")
    for en, group in clusters().items():
        links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{u}"/>' for l, u in group.items()) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{en}"/>'
        for u in group.values():
            s = s.replace(f"<loc>{SITE}{u}</loc>", f"<loc>{SITE}{u}</loc>{links}", 1)
    open(f, "w", encoding="utf-8").write(s)
if __name__ == "__main__":
    for p in PAGES:
        d = os.path.join(ROOT, p["path"].strip("/")); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(p)); print("wrote", p["path"])
    wire_english(); sitemap(); print("wired hreflang + sitemap")
