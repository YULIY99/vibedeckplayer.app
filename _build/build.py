#!/usr/bin/env python3
"""Static page generator for vibedeckplayer.app.
Output is plain HTML committed to the repo (GitHub Pages). Run: python3 _build/build.py
Underscore folders are not published by GitHub Pages/Jekyll."""
import json, html, os, re, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vibedeckplayer.app"
APPSTORE = "https://apps.apple.com/app/vibedeck-player/id6784724920"
PLAY = "https://play.google.com/store/apps/details?id=com.vibedeck.player"
E = html.escape

# ---------------------------------------------------------------- images
IMG = {
  # live screenshots (shown inside a CSS phone frame)
  "now-playing": ("vibedeck-offline-music-player-iphone-now-playing", (400,600,800), (1290,2796)),
  "aura-live":   ("vibedeck-flac-player-iphone-aura", (400,600,800), (1290,2796)),
  "pitch-live":  ("vibedeck-pitch-filter-iphone", (400,600,800), (1290,2796)),
  # App Store banners
  "b-pitch":   ("vibedeck-pitch-control-iphone", (360,540,720), (1290,2796)),
  "b-eq":      ("vibedeck-equalizer-iphone", (360,540,720), (1290,2796)),
  "b-tone":    ("vibedeck-tone-control-iphone", (360,540,720), (1290,2796)),
  "b-vibemod": ("vibedeck-vibemod-visualizer-iphone", (360,540,720), (1290,2796)),
  "b-aura":    ("vibedeck-aura-visualizer-iphone", (360,540,720), (1290,2796)),
  "b-queue":   ("vibedeck-queue-reorder-iphone", (360,540,720), (1290,2796)),
  # Android banners
  "a-main": ("vibedeck-offline-music-player-android", (360,540,720), (941,1672)),
  "a-tone": ("vibedeck-android-tone-control", (360,540,720), (941,1672)),
}
SIZES_PHONE = "(min-width: 1024px) 326px, 66vw"
SIZES_CARD = "(min-width: 1024px) 288px, 76vw"
SIZES_PAIR = "(min-width: 1024px) 320px, 44vw"

def srcset(key, ext):
    base, ws, _ = IMG[key]
    return ", ".join(f"/assets/img/{base}-{w}.{ext} {w}w" for w in ws)

def pic(key, alt, sizes, lazy=True, cls=""):
    base, ws, (W, H) = IMG[key]
    mid = ws[1]
    w = mid; h = round(H * mid / W)
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{srcset(key,"avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset(key,"webp")}" sizes="{sizes}">'
            f'<img src="/assets/img/{base}-{mid}.webp" alt="{E(alt)}" width="{w}" height="{h}" {load}{(" class=%s" % cls) if cls else ""}></picture>')

def preload(key, sizes):
    return (f'<link rel="preload" as="image" type="image/avif" imagesrcset="{srcset(key,"avif")}" '
            f'imagesizes="{sizes}" fetchpriority="high">')

def phone(key, alt, lazy=True, size="", parallax=None, badges=None):
    p = f' data-parallax="{parallax}"' if parallax else ""
    b = ""
    if badges:
        b = "".join(f'<span class="float-badge glass mono {c}" aria-hidden="true">{t}</span>' for c, t in badges)
    return f'<div class="phone {size}"{p}>{pic(key, alt, SIZES_PHONE, lazy)}{b}</div>'

def wave(n=56, seed=7):
    r = random.Random(seed); bars = []
    for i in range(n):
        h = 18 + int(80 * abs(r.random() * 0.6 + 0.4 * (1 if i % 9 < 5 else 0.35)))
        bars.append(f'<i style="--h:{h}px;--d:-{r.random()*3.6:.2f}s"></i>')
    return '<div class="wave" aria-hidden="true">' + "".join(bars) + "</div>"

APPLE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25C11.88 5.02 13.69 3.18 15.8 3c.29 2.58-2.34 4.5-3.77 4.25z"/></svg>'
PLAY_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34a853" d="M2.4 3.2c-.25.32-.4.74-.4 1.25v15.1c0 .51.15.93.4 1.25L13.2 10.1z"/><path fill="#4285f4" d="m16.65 13.55-3.45-3.45L2.4 20.8c.4.5 1.07.56 1.72.2z"/><path fill="#fbbc04" d="m20.45 10.25-3.8-2.2L13.2 10.1l3.45 3.45 3.8-2.2c.72-.4.72-.7 0-1.1z"/><path fill="#ea4335" d="M4.12 3c-.65-.36-1.32-.3-1.72.2l10.8 10.35 3.45-3.45z"/></svg>'

def stores(ios=True, android=True):
    out = []
    if ios:
        out.append(f'<a class="store store--primary" href="{APPSTORE}" aria-label="Download VibeDeck Player on the App Store for iPhone and iPad">{APPLE_SVG}<span><small>Download on the</small><strong>App Store</strong></span></a>')
    if android:
        out.append(f'<a class="store" href="{PLAY}" aria-label="Get VibeDeck Player on Google Play for Android">{PLAY_SVG}<span><small>Get it on</small><strong>Google Play</strong></span></a>')
    return '<div class="stores">' + "".join(out) + "</div>"

# ---------------------------------------------------------------- shared data
GUIDES = [
  ("/flac-player-iphone/", "FLAC · iPhone", "FLAC player for iPhone", "Play lossless FLAC offline on iPhone and iPad, with a real EQ, pitch and tempo."),
  ("/offline-music-player-iphone/", "Offline · iPhone", "Offline music player for iPhone", "Your whole library on planes and in dead zones. No WiFi, no subscription."),
  ("/offline-music-player-android/", "Offline · Android", "Offline music player for Android", "MP3, FLAC, WAV, AAC and more from your phone, with zero mobile data spent on music."),
  ("/mp3-player-no-ads/", "MP3 · No ads", "MP3 player with no ads", "No banners, no video breaks, no account. Press play and hear your MP3s."),
  ("/music-player-pitch-tempo/", "Pitch · Tempo", "Music player with pitch and tempo control", "Change the key by ±8 semitones and the speed independently, for practice and DJ prep."),
  ("/vibedeck-vs-vox/", "Compare", "VibeDeck Player vs VOX", "An honest look at the VOX alternative with pitch tools and Android support."),
]
PRICE_NOTE = "Prices may vary by region; the App Store and Google Play listings always show the current local price."

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "VibeDeck", "url": SITE + "/",
       "logo": SITE + "/assets/img/icon-512.png", "email": "hello@vibedeckplayer.app",
       "founder": {"@type": "Person", "name": "Yuliy Metelskiy"}}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "name": "VibeDeck Player", "alternateName": "VibeDeck",
           "url": SITE + "/", "inLanguage": "en", "publisher": {"@id": SITE + "/#org"}}
def offer(name, price, desc, url):
    return {"@type": "Offer", "name": name, "price": price, "priceCurrency": "USD", "description": desc, "url": url}
APP = {"@type": "MobileApplication", "@id": SITE + "/#app", "name": "VibeDeck Player", "alternateName": "VibeDeck",
       "applicationCategory": "MusicApplication", "operatingSystem": "iOS 17.0 or later, iPadOS, Android",
       "description": "Offline music player for local FLAC, MP3, WAV, AAC, M4A and more files with 3-band EQ and gain, bass boost, filter, limiter, real-time pitch and tempo control, waveform and the AURA visualizer. No ads, account or tracking.",
       "url": SITE + "/", "image": SITE + "/assets/img/icon-512.png",
       "screenshot": [SITE + "/assets/img/vibedeck-offline-music-player-iphone-now-playing-800.webp",
                      SITE + "/assets/img/vibedeck-equalizer-iphone-720.webp",
                      SITE + "/assets/img/vibedeck-offline-music-player-android-720.webp"],
       "downloadUrl": [APPSTORE, PLAY], "installUrl": [APPSTORE, PLAY],
       "featureList": ["Offline playback for FLAC, MP3, WAV, AAC, M4A and more", "3-band equalizer with gain, bass boost, filter and limiter",
                       "Real-time pitch shifting up to plus or minus 8 semitones", "Independent tempo control",
                       "Waveform scrubbing and BPM readout", "Queue with drag to reorder", "Audio-reactive AURA visualizer, VibeMod and TONE"],
       "offers": [offer("VibeDeck Player", "0", "Free download. Core player with no ads.", APPSTORE),
                  offer("VibeDeck Player", "0", "Free download. Core player with no ads.", PLAY),
                  offer("VibeDeck Premium Monthly (App Store)", "2.99", "Full sound engine, billed monthly on iPhone and iPad.", APPSTORE),
                  offer("VibeDeck Premium Yearly (App Store)", "19.99", "Full sound engine, billed yearly on iPhone and iPad.", APPSTORE),
                  offer("VibeDeck Premium Lifetime (App Store)", "49.99", "Full sound engine, one-time purchase on iPhone and iPad.", APPSTORE),
                  offer("VibeDeck Premium Monthly (Google Play)", "1.99", "Full sound engine, billed monthly on Android.", PLAY),
                  offer("VibeDeck Premium Yearly (Google Play)", "9.99", "Full sound engine, billed yearly on Android.", PLAY),
                  offer("VibeDeck Premium Lifetime (Google Play)", "14.99", "Full sound engine, one-time purchase on Android.", PLAY)],
       "publisher": {"@id": SITE + "/#org"}, "author": {"@id": SITE + "/#org"}, "inLanguage": "en"}

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}

# ---------------------------------------------------------------- layout
def head(p):
    ld = json.dumps({"@context": "https://schema.org", "@graph": p["ld"]}, ensure_ascii=False, indent=1)
    og_img = SITE + "/assets/img/vibedeck-og-1200x630.jpg"
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else '<meta name="robots" content="index, follow, max-image-preview:large">'
    verify = '<meta name="google-site-verification" content="lARXSnM8CfbmGAwtuJDpwYdSgbqJIEOF87h83HUaXYc">\n' if p["path"] == "/" else ""
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{verify}<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["desc"])}">
{robots}
<link rel="canonical" href="{SITE}{p["path"]}">
<meta name="theme-color" content="#04070d">
<meta name="color-scheme" content="dark">
<meta name="apple-itunes-app" content="app-id=6784724920">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VibeDeck Player">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{E(p.get("og_title", p["title"]))}">
<meta property="og:description" content="{E(p.get("og_desc", p["desc"]))}">
<meta property="og:url" content="{SITE}{p["path"]}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="VibeDeck offline music player on iPhone">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(p.get("og_title", p["title"]))}">
<meta name="twitter:description" content="{E(p.get("og_desc", p["desc"]))}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/jetbrains-mono-latin-var.woff2" as="font" type="font/woff2" crossorigin>
{p.get("preload", "")}
<link rel="stylesheet" href="/styles.css?v=2">
<script>document.documentElement.className="js"</script>
<script src="/assets/site.js?v=2" defer></script>
<script type="application/ld+json">
{ld}
</script>
</head>'''

def header(active=None, dl="#download"):
    links = [("/#player", "Player"), ("/#workflow", "Workflow"), ("/support.html", "Support"), ("/privacy.html", "Privacy")]
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if active == t else ""}>{t}</a>' for u, t in links)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-wrap">
    <a class="brand" href="/" aria-label="VibeDeck Player home"><img src="/assets/vibedeck-logo-header.webp" alt="VibeDeck Player logo" width="32" height="32"><span class="brand-name">VibeDeck</span></a>
    <nav class="nav mono" aria-label="Main navigation">{nav}</nav>
    <a class="btn-dl" href="{dl}">Download</a>
  </div>
</header>'''

def footer():
    g = "".join(f'<li><a href="{u}">{E(t)}</a></li>' for u, _, t, _ in GUIDES)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="/" aria-label="VibeDeck Player home"><img src="/assets/vibedeck-logo-header.webp" alt="VibeDeck Player logo" width="32" height="32" loading="lazy"><span class="brand-name">VibeDeck</span></a>
        <p>Same Track. New Feeling. Offline music player for FLAC, MP3 &amp; WAV on iPhone, iPad and Android.</p>
      </div>
      <nav aria-label="Guides"><h2>Guides</h2><ul>{g}</ul></nav>
      <nav aria-label="Player"><h2>Player</h2><ul>
        <li><a href="/#player">Player</a></li><li><a href="/#workflow">Workflow</a></li><li><a href="/#premium">Premium</a></li><li><a href="/#faq">FAQ</a></li>
        <li><a href="{APPSTORE}">App Store</a></li><li><a href="{PLAY}">Google Play</a></li></ul></nav>
      <nav aria-label="Company"><h2>Company</h2><ul>
        <li><a href="/support.html">Support</a></li><li><a href="/privacy.html">Privacy</a></li><li><a href="/terms.html">Terms</a></li>
        <li><a href="mailto:hello@vibedeckplayer.app">hello@vibedeckplayer.app</a></li></ul></nav>
    </div>
    <div class="foot-base mono"><span>© 2026 VibeDeck</span><span>No ads · No account · No tracking</span></div>
  </div>
</footer>
</body>
</html>
'''

def faq_html(items, title="FAQ", tag="FAQ", lede=""):
    rows = "".join(f'<details><summary><h3>{E(q)}</h3></summary><div class="a"><p>{E(a)}</p></div></details>' for q, a in items)
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'''<section class="section" id="faq" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">{tag}</p><h2 class="h2" id="faq-title">{title}</h2></div>{l}</div>
    <div class="faq" data-reveal>{rows}</div>
  </div>
</section>'''

def cards_html(items, h2, tag, lede="", sid="guides", cls=""):
    c = "".join(f'<li data-reveal style="--rd:{(i%3)*90}ms"><a class="card glass" href="{u}"><span class="tag">{E(t)}</span><h3>{E(h)}</h3><p>{E(d)}</p><span class="go mono"><span>Open guide</span><span aria-hidden="true">→</span></span></a></li>' for i, (u, t, h, d) in enumerate(items))
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'''<section class="section" id="{sid}" aria-labelledby="{sid}-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">{tag}</p><h2 class="h2" id="{sid}-title">{h2}</h2></div>{l}</div>
    <ul class="cards {cls}">{c}</ul>
  </div>
</section>'''

def plans_html(h2_tag="h2", head_html=None):
    plans = [("Monthly", "$2.99", "$1.99", "/ mo", "Full sound engine, billed monthly through the store.", False),
             ("Yearly", "$19.99", "$9.99", "/ yr", "Full sound engine for twelve months.", False),
             ("Lifetime", "$49.99", "$14.99", "once", "Pay once. The full sound engine is yours for good.", True)]
    li = "".join(f'<li class="plan glass{" plan--hi" if hi else ""}" data-reveal style="--rd:{i*90}ms">{"<span class=\"badge mono\">Pay once</span>" if hi else ""}<h3>{n}</h3><dl class="prices"><div><dt class="mono">App Store · iPhone</dt><dd class="price">{ios}<small>{per}</small></dd></div><div><dt class="mono">Google Play · Android</dt><dd class="price price--sm">{andr}<small>{per}</small></dd></div></dl><p>{d}</p></li>' for i, (n, ios, andr, per, d, hi) in enumerate(plans))
    return f'<ul class="plans">{li}</ul><p class="note">{PRICE_NOTE}</p>'

def cta_html(text, ios=True, android=True, heading="Download VibeDeck Player", key="aura-live", alt="VibeDeck FLAC player for iPhone playing a track with AURA and waveform"):
    return f'''<section class="section" id="download" aria-labelledby="download-title">
  <div class="wrap">
    <div class="cta" data-reveal>
      <div class="cta-grid">
        <div class="cta-copy">
          <p class="tag">Download <span class="dim">/ iOS · Android</span></p>
          <h2 class="h2" id="download-title">{heading}</h2>
          <p class="lede">{text}</p>
          {stores(ios, android)}
        </div>
        <div class="cta-media">{phone(key, alt, True, "phone--sm", "0.05")}</div>
      </div>
    </div>
  </div>
</section>'''

def crumbs_html(trail):
    li = "".join((f'<li><a href="{u}">{E(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{E(n)}</li>') for i, (n, u) in enumerate(trail))
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs mono">{li}</ol></nav>'

def write(path, content):
    fp = os.path.join(ROOT, path.lstrip("/"))
    if fp.endswith("/"): fp += "index.html"
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(content)

# ---------------------------------------------------------------- HOME
HOME_FAQ = [
 ("Is VibeDeck Player free?", "The core player is free with no ads. VibeDeck Premium unlocks the full sound engine: pitch and filter, 3-band EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata. On the App Store Premium costs $2.99 per month, $19.99 per year or $49.99 for a lifetime license; on Google Play it costs $1.99 per month, $9.99 per year or $14.99 for a lifetime license."),
 ("Which audio formats does VibeDeck Player play?", "VibeDeck Player plays all popular audio formats stored on your device: FLAC, MP3, WAV, AAC, M4A, ALAC, AIFF and more. No conversion and no cloud upload needed."),
 ("Can iPhone play FLAC files?", "Yes. iPhone can play FLAC files, but the built-in options give you no equalizer, no pitch control and no real library for your own files. VibeDeck Player is a dedicated FLAC player for iPhone and iPad that plays your lossless files offline with a 3-band EQ, pitch and tempo control."),
 ("Does VibeDeck Player work offline?", "Yes. It is a fully offline music player: your files stay on the device and play with no WiFi, no account and no tracking."),
 ("Can I use VibeDeck Player offline without an account?", "Yes. There is no sign-up, no login and no cloud library. You import your own files once, and playback, EQ, pitch and tempo all run on the device, even in airplane mode."),
 ("How do I change the pitch of a song on iPhone?", "Open the track in VibeDeck Player and drag the Pitch / Filter slider on the main player screen. Pitch moves in real time up to plus or minus 8 semitones, tempo can be changed independently, and Reset returns the song to its original key. The file itself is never modified. Pitch and filter are part of VibeDeck Premium."),
 ("What is the best ad-free offline music player?", "It depends on what you need. If you want an offline music player with no ads that also changes pitch and tempo, runs on both iPhone and Android, and offers a one-time lifetime license, VibeDeck Player is built for exactly that. The core player is free with no ads; Premium is optional."),
 ("Is VibeDeck Player available for iPhone and Android?", "Yes. VibeDeck Player is on the App Store for iPhone and iPad (iOS 17.0 and later) and on Google Play for Android."),
 ("Is VibeDeck Player a good alternative to VOX?", "If you want real-time pitch and tempo control, Android support, or a one-time lifetime license, yes. VOX remains a strong pick if you live entirely inside the Apple ecosystem and do not need pitch tools."),
 ("What makes VibeDeck Player different?", "Real-time pitch shifting up to plus or minus 8 semitones, independent tempo control, 3-band EQ with gain, waveform scrubbing with BPM readout, and the audio-reactive AURA visualizer, all offline on your own files."),
]
SHOTS = [
 ("b-pitch", "Playback", "Pitch control on the main screen", "Same track, new feeling. Pitch, VibeMod and TONE sit right under the artwork.", "VibeDeck offline music player with pitch control on iPhone"),
 ("b-eq", "Sound", "3-band EQ with gain and limiter", "Gain, low, mid, high, plus limiter and stereo balance, applied in real time.", "VibeDeck music player equalizer for iPhone with gain, limiter and balance"),
 ("b-tone", "Tone", "Change the vibe", "One track. Two moods. Switch to TONE and hear the same song in a different colour.", "VibeDeck tone control for an offline music player on iPhone"),
 ("b-vibemod", "VibeMod", "Music that reacts", "Visuals that move with every beat, driven by the track that is playing.", "VibeDeck music-reactive visualizer for an offline music player"),
 ("b-aura", "Aura", "Same track. New universe.", "The AURA visual reacts to your music: an ambient world for low-light listening.", "VibeDeck AURA waveform visualizer for offline music playback"),
 ("b-queue", "Queue", "Touch and drag to reorder", "Rearrange tracks the way you like, search the library and see what is up next.", "VibeDeck queue for local music files with drag to reorder"),
]

def home():
    p = {"path": "/", "title": "VibeDeck Player – Offline Music Player for FLAC, MP3 & WAV",
         "desc": "Offline music player for iPhone & Android. Play FLAC, MP3, WAV, AAC, M4A and more with EQ, pitch and tempo control. No ads, no account. Download free.",
         "og_title": "VibeDeck Player – Same Track. New Feeling.",
         "og_desc": "Shape FLAC, MP3, WAV, AAC, M4A and more in real time with 3-band EQ, pitch, tempo, waveform and AURA on iOS and Android. No ads, account or tracking.",
         "preload": preload("now-playing", SIZES_PHONE),
         "ld": [ORG, WEBSITE, APP, faq_ld(HOME_FAQ)]}
    tabs = "".join(f'<a href="#shot-{i+1}" class="mono{" is-active" if i == 0 else ""}">{t}</a>' for i, (_, t, _, _, _) in enumerate(SHOTS))
    rail = "".join(f'<li class="shot" id="shot-{i+1}"><figure>{pic(k, alt, SIZES_CARD)}</figure><div><p class="tag"><b>{i+1:02d}</b> / {t}</p><h3>{h}</h3><p>{d}</p></div></li>' for i, (k, t, h, d, alt) in enumerate(SHOTS))
    body = f'''{header("Player")}
<main id="main">
<section class="hero" id="player" aria-labelledby="hero-title">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="tag eyebrow">iPhone · iPad · Android <span class="dim">/ Offline</span></p>
      <h1 id="hero-title"><span class="h1-big">Same Track. <em>New Feeling.</em></span><span class="h1-sub">Offline music player for FLAC, MP3 &amp; WAV</span></h1>
      <p class="lede">Offline music player for iPhone, iPad and Android that plays MP3, FLAC, WAV, AAC and more from your local files, with equalizer, pitch and tempo control. No WiFi needed.</p>
      {stores()}
      <ul class="hero-meta mono" aria-label="Highlights"><li>No ads</li><li>No account</li><li>No tracking</li><li>iOS 17+ · Android</li></ul>
      <div class="slider" aria-hidden="true"><div class="slider-top mono"><span><b>Pitch</b> / Filter</span><span>0.00</span></div><div class="slider-track"><span class="slider-thumb"></span></div><div class="slider-top mono"><span>0:02</span><span>BPM 124</span></div></div>
    </div>
    <div class="hero-visual">
      <div class="halo" aria-hidden="true"></div>
      {wave()}
      {phone("now-playing", "VibeDeck offline music player for iPhone with pitch control and equalizer", False, "phone--lg", "0.04", [])}
    </div>
  </div>
</section>

<section class="section statement" aria-label="About VibeDeck Player">
  <div class="wrap" data-reveal>
    <p class="tag">Same track <span class="dim">/ New feeling</span></p>
    <p>VibeDeck is a premium music player for iOS and Android, <strong>for people who own their music and want to feel it again.</strong> Import your audio files and shape the sound in real time with a 3-band EQ and gain, bass boost, filter, limiter, pitch, tempo, and DJ tools, all on one dark, distraction-free screen.</p>
  </div>
</section>

<section class="section" id="features" aria-labelledby="features-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Features <span class="dim">/ 06</span></p><h2 class="h2" id="features-title">Pitch, EQ, AURA, TONE. <span class="soft">One dark screen.</span></h2></div><p class="lede">Every sound tool lives one move from the track: a music player with pitch and tempo control, a real equalizer for iPhone and Android, and visuals that react to the beat.</p></div>
    <nav class="tabs" aria-label="Feature screens">{tabs}</nav>
    <ol class="rail" aria-label="VibeDeck feature screens">{rail}</ol>
    <div class="rail-ctrl mono"><span>Swipe to explore · 6 screens</span><div class="rail-btns"><button type="button" data-rail="prev" aria-label="Previous screen">←</button><button type="button" data-rail="next" aria-label="Next screen">→</button></div></div>
  </div>
</section>

<section class="section" id="workflow" aria-labelledby="workflow-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Workflow</p><h2 class="h2" id="workflow-title">Player first. <span class="soft">Controls close.</span></h2></div><p class="lede">VibeDeck keeps the current track readable while the queue and EQ stay one move away. This offline music player is built for low light, fast scanning, and deliberate sound shaping from your local files.</p></div>
    <ul class="panels">
      <li class="panel glass" data-reveal><span class="num" aria-hidden="true">01</span><h3>Playback</h3><p>Full transport controls, waveform with scrubbing, BPM readout, and pitch/filter on the main screen. Same track. New feeling.</p><span class="tag dim">Transport · Waveform · BPM</span></li>
      <li class="panel glass" data-reveal style="--rd:90ms"><span class="num" aria-hidden="true">02</span><h3>Queue</h3><p>See what's playing, search your library, and line up what's next without leaving the player. Night Mode strips the artwork for a calmer, distraction-free list.</p><span class="tag dim">Search · Up next · Night mode</span></li>
      <li class="panel glass" data-reveal style="--rd:180ms"><span class="num" aria-hidden="true">03</span><h3>Sound</h3><p>3-band EQ + Gain, bass boost, filter, VibeMod audio-reactive processing, stereo balance, and real-time pitch shifting up to ±8 semitones. Built-in limiter: clean, punchy sound on any headphones.</p><span class="tag dim">EQ · Pitch ±8 · Limiter</span></li>
    </ul>
  </div>
</section>

<section class="section" id="android" aria-labelledby="android-title">
  <div class="wrap duo">
    <div class="duo-copy" data-reveal>
      <p class="tag eyebrow">Android <span class="dim">/ Google Play</span></p>
      <h2 class="h2" id="android-title">VibeDeck for Android.</h2>
      <p class="lede">An offline music player for your own files, with pitch, waveform, tone and sound controls on one focused screen.</p>
      {stores(False, True)}
      <p class="mono" style="margin-top:24px"><a class="link" href="/offline-music-player-android/">Offline music player for Android →</a></p>
    </div>
    <div class="duo-media pair">
      <figure data-parallax="0.03">{pic("a-main", "VibeDeck for Android with pitch control and waveform", SIZES_PAIR)}</figure>
      <figure data-parallax="0.07">{pic("a-tone", "VibeDeck for Android with tone controls and playback tools", SIZES_PAIR)}</figure>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="specs-title">
  <div class="wrap specs" data-reveal>
    <h2 id="specs-title">Specs</h2>
    <ul class="chips"><li>All popular formats</li><li>FLAC</li><li>MP3</li><li>WAV</li><li>AAC</li><li>M4A</li><li>ALAC</li><li>AIFF</li><li>±8 semitones</li><li>Tempo</li><li>3-band EQ</li><li>Limiter</li><li>Offline</li><li>No ads</li><li>No account</li><li>No tracking</li></ul>
  </div>
</section>

{cards_html(GUIDES, 'Built for <span class="soft">the way you listen.</span>', 'Built for <span class="dim">/ 06</span>', "Six ways people use VibeDeck Player, each with its own guide.")}

<section class="section" id="why" aria-labelledby="why-title">
  <div class="wrap duo duo--rev">
    <div class="duo-copy prose" data-reveal>
      <p class="tag eyebrow">Why VibeDeck</p>
      <h2 id="why-title">Why VibeDeck Player?</h2>
      <p>VibeDeck Player is a premium <strong>offline music player for iPhone, iPad and Android</strong>, made for people who own their music. It plays the FLAC, MP3, WAV, AAC, M4A and more files already on your phone, with no WiFi, no account, no ads and no tracking. Your files stay on your device.</p>
      <p>Where most players stop at play and pause, VibeDeck treats every track as material. Shift pitch up to ±8 semitones and change tempo independently to practise, sing in your range or prep a DJ set. Shape the sound with a 3-band equalizer with gain, bass boost, filter, stereo balance and a built-in limiter. Scrub the waveform, read the BPM, and line up what's next in a queue you reorder by touch. AURA adds an ambient visual world that breathes with your music, and TONE and VibeMod give one track a second mood.</p>
      <p>Looking for a <a href="/flac-player-iphone/">FLAC player for iPhone</a>, an <a href="/mp3-player-no-ads/">MP3 player with no ads</a>, or a <a href="/vibedeck-vs-vox/">VOX alternative</a> that also runs on Android? VibeDeck Player covers all three on one dark, distraction-free screen. Same track. New feeling.</p>
    </div>
    <div class="duo-media media-solo">
      <div class="halo" aria-hidden="true"></div>
      {phone("pitch-live", "VibeDeck music player with pitch and filter slider and waveform on iPhone", True, "", "0.05")}
    </div>
  </div>
</section>

<section class="section" id="premium" aria-labelledby="premium-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Premium <span class="dim">/ Optional</span></p><h2 class="h2" id="premium-title">VibeDeck Premium</h2></div><p class="lede">The core player is free with no ads. VibeDeck Premium unlocks the full sound engine: pitch and filter, 3-band EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.</p></div>
    {plans_html()}
  </div>
</section>

{faq_html(HOME_FAQ, "Questions, answered.", 'FAQ <span class="dim">/ 10</span>')}

{cta_html("VibeDeck is now available for iPhone, iPad and Android. Work with local audio files, shape the sound in real time, and keep your music offline. No account. No ads. No tracking.")}
</main>
{footer()}'''
    write("/", head(p) + "\n" + body)
    return p

# ---------------------------------------------------------------- LANDING PAGES
def landing(d):
    trail = [("Home", "/"), (d["crumb"], d["path"])]
    p = {"path": d["path"], "title": d["title"], "desc": d["desc"], "og_desc": d.get("og_desc", d["desc"]),
         "preload": preload(d["visual"][0], SIZES_PHONE if d["visual"][2] == "phone" else SIZES_CARD),
         "ld": [ORG, WEBSITE, APP, crumbs_ld(trail), faq_ld(d["faq"])]}
    k, alt, kind = d["visual"]
    if kind == "phone":
        vis = phone(k, alt, False, "phone--lg", "0.04")
    else:
        sz = SIZES_CARD
        vis = f'<figure class="poster" data-parallax="0.04">{pic(k, alt, sz, False)}</figure>'
    feats = "".join(f'<li class="panel glass" data-reveal style="--rd:{i*90}ms"><span class="num" aria-hidden="true">{i+1:02d}</span><h3>{h}</h3><p>{t}</p></li>' for i, (h, t) in enumerate(d["features"]))
    extra = d.get("extra", "")
    related = [g for g in GUIDES if g[0] != d["path"] and g[0] in d["related"]]
    related = [("/", "Home", "VibeDeck Player home", "Same track, new feeling: the full tour of the offline music player.")] + related
    body = f'''{header()}
<main id="main">
<section class="hero hero--sub" aria-labelledby="hero-title">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      {crumbs_html(trail)}
      <p class="tag eyebrow">{d["tag"]}</p>
      <h1 id="hero-title"><span class="h1-plain">{d["h1"]}</span><span class="h1-sub">{d["h1_sub"]}</span></h1>
      <p class="lede">{d["lede"]}</p>
      {stores(d["ios"], d["android"])}
    </div>
    <div class="hero-visual">
      <div class="halo" aria-hidden="true"></div>
      {wave(48, len(d["path"]))}
      {vis}
    </div>
  </div>
</section>

<section class="section statement statement--small" aria-label="Overview">
  <div class="wrap" data-reveal><p>{d["statement"]}</p></div>
</section>

<section class="section" aria-labelledby="features-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Features <span class="dim">/ 03</span></p><h2 class="h2" id="features-title">{d["features_h2"]}</h2></div></div>
    <ul class="panels">{feats}</ul>
  </div>
</section>
{extra}
{faq_html(d["faq"], d["faq_h2"], 'FAQ <span class="dim">/ ' + f'{len(d["faq"]):02d}' + '</span>')}

{cards_html(related, 'Keep <span class="soft">exploring.</span>', "Related", "", "related", "cards--4")}

{cta_html(d["cta"], d["ios"], d["android"], "Download VibeDeck Player")}
</main>
{footer()}'''
    write(d["path"], head(p) + "\n" + body)
    return p

def prose_section(inner, sid=None):
    i = f' id="{sid}"' if sid else ""
    return f'''
<section class="section"{i}>
  <div class="wrap"><div class="glass box prose" data-reveal>{inner}</div></div>
</section>'''

FREE_A = "The core player is free with no ads. Premium unlocks the full sound engine including pitch and filter, 3-band EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata."
FILES_Q = ("Where do the music files come from?", "Your own collection: downloads, rips, Bandcamp purchases, DJ pools. If you own the file, it plays.")

PAGES = [
 dict(path="/flac-player-iphone/", crumb="FLAC player for iPhone",
  title="FLAC Player for iPhone – Lossless & Offline | VibeDeck",
  desc="Play lossless FLAC files offline on iPhone and iPad with 3-band EQ, pitch and tempo control. No ads, no account, no tracking. Download VibeDeck free.",
  og_desc="Play your FLAC collection offline on iPhone and iPad. Lossless audio with EQ, pitch, tempo and DJ tools. No ads or account.",
  tag="iPhone · iPad <span class=\"dim\">/ Lossless</span>", h1="Your FLAC collection, finally at home on iPhone.", h1_sub="FLAC player for iPhone &amp; iPad",
  lede="VibeDeck Player plays lossless FLAC files offline on iPhone and iPad, with a 3-band EQ and gain, pitch and tempo control, waveform scrubbing and DJ tools. No ads. No account. No tracking.",
  visual=("aura-live", "VibeDeck Player FLAC player for iPhone with pitch control", "phone"), ios=True, android=False,
  statement="iPhone plays FLAC, but the built-in options treat your lossless library as an afterthought: no equalizer, no pitch control, no waveform, no DJ tools. VibeDeck Player is built for people who own their music in FLAC and want to hear every detail of it, shaped exactly the way they like.",
  features_h2="FLAC player features",
  features=[("Lossless playback", "FLAC, WAV, MP3, AAC, M4A and more from your local files. Your audio stays on the device, with no streaming and no conversion."),
            ("Real EQ", "3-band EQ with gain, bass boost, filter, stereo balance and a limiter. Shape lossless sound in real time instead of accepting a flat default."),
            ("Pitch and tempo", "Shift pitch up to 8 semitones and change tempo independently. Practice, DJ prep, or just hear a track differently.")],
  extra=prose_section('<h2>Formats VibeDeck Player plays</h2><p>Drop your files in and press play. No conversion, no cloud upload.</p><ul><li><strong>FLAC</strong>: lossless, your main archive format</li><li><strong>WAV</strong>: uncompressed studio files</li><li><strong>MP3</strong>: your existing library and downloads</li></ul><p>Also see: <a href="/offline-music-player-iphone/">offline music player for iPhone</a>, <a href="/music-player-pitch-tempo/">pitch and tempo control</a>.</p>'),
  faq_h2="FLAC player FAQ",
  faq=[("Can iPhone play FLAC files?", "Yes. iPhone can play FLAC files, but the built-in options give you no equalizer, no pitch control and no real library for your own files. VibeDeck Player is a dedicated FLAC player for iPhone and iPad that plays your lossless files offline with full sound controls."),
       ("Does VibeDeck Player work without internet?", "Yes. VibeDeck Player is an offline music player. Your FLAC, MP3, WAV, AAC, M4A and more files stay on your device and play with no WiFi, no account and no ads."),
       ("Does it have an equalizer for FLAC playback?", "Yes. VibeDeck Player includes a 3-band EQ with gain, bass boost, filter, stereo balance and a built-in limiter, all applied in real time to your FLAC files."),
       ("Can I change pitch and tempo of FLAC tracks?", "Yes. VibeDeck Player offers real-time pitch shifting up to plus or minus 8 semitones and independent tempo control, which is rare among iPhone FLAC players."),
       ("Is VibeDeck Player free?", "The core player is free with no ads. VibeDeck Premium unlocks the full sound engine: pitch and filter, 3-band EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.")],
  related=["/offline-music-player-iphone/", "/music-player-pitch-tempo/", "/vibedeck-vs-vox/"],
  cta="Play your FLAC files offline on iPhone and iPad. No account. No ads. No tracking."),
 dict(path="/offline-music-player-iphone/", crumb="Offline music player for iPhone",
  title="Offline Music Player for iPhone – No WiFi | VibeDeck",
  desc="Offline music player for iPhone and iPad. Play MP3, FLAC, WAV, AAC and more with no internet, no ads, no account. EQ, pitch and tempo. Download free.",
  og_desc="Your music, on your iPhone, with no internet. Offline player for MP3, FLAC, WAV, AAC and more with EQ, pitch and DJ tools.",
  tag="iPhone · iPad <span class=\"dim\">/ No WiFi</span>", h1="Music that plays when the internet does not.", h1_sub="Offline music player for iPhone &amp; iPad",
  lede="Plane mode, dead zones, roaming bills. VibeDeck Player keeps your MP3, FLAC, WAV, AAC and more on the device and playing, with EQ, pitch, tempo and DJ tools. No WiFi needed, ever.",
  visual=("b-queue", "VibeDeck Player offline music player queue on iPhone", "card"), ios=True, android=False,
  statement="Streaming apps rent you music and take it away the moment you stop paying or lose signal. VibeDeck Player is the opposite: an offline music player for the files you own. Import once, listen anywhere, shape the sound in real time.",
  features_h2="Offline features",
  features=[("True offline", "No streaming, no buffering, no login. Your library lives on your iPhone and plays in airplane mode."),
            ("Your formats", "MP3, FLAC, WAV, AAC and more. Mix lossy and lossless in one queue without thinking about it."),
            ("Pro sound", "3-band EQ with gain, bass boost, pitch and tempo, waveform scrubbing and BPM readout, all on one dark screen.")],
  extra=prose_section('<h2>Why go offline on iPhone</h2><ul><li><strong>Flights and travel</strong>: your whole library, no WiFi required</li><li><strong>No subscription</strong>: the music you own stays yours</li><li><strong>Battery</strong>: local playback sips power compared to streaming</li><li><strong>Privacy</strong>: no account, no tracking, files never leave the device</li></ul><p>Related: <a href="/flac-player-iphone/">FLAC player for iPhone</a>, <a href="/mp3-player-no-ads/">MP3 player with no ads</a>.</p>'),
  faq_h2="Offline player FAQ",
  faq=[("What is the best offline music player for iPhone?", "VibeDeck Player is built for offline listening on iPhone and iPad: your MP3, FLAC, WAV, AAC and more files play with no internet, no ads and no account, plus EQ, pitch, tempo and DJ tools you will not find in stock apps."),
       ("Can I play music on iPhone without internet?", "Yes. With VibeDeck Player your files are stored on the device, so music keeps playing on planes, in the subway, or anywhere with no signal."),
       ("Does Apple Music work offline?", "Apple Music needs a paid subscription for offline downloads and locks you into its ecosystem. VibeDeck Player plays files you already own, with no subscription and no lock-in."),
       FILES_Q,
       ("Is VibeDeck Player free?", FREE_A.replace("The core player", "The core offline player"))],
  related=["/flac-player-iphone/", "/mp3-player-no-ads/", "/offline-music-player-android/"],
  cta="Offline music player for iPhone and iPad. No account. No ads. No tracking."),
 dict(path="/offline-music-player-android/", crumb="Offline music player for Android",
  title="Offline Music Player for Android – No Ads | VibeDeck",
  desc="Offline music player for Android. Play MP3, FLAC, WAV, AAC and more with no internet, no ads, no account. 3-band EQ, pitch and tempo. On Google Play.",
  og_desc="Your music, on your Android phone, with no internet. Offline player for MP3, FLAC, WAV, AAC and more with EQ, pitch and DJ tools.",
  tag="Android <span class=\"dim\">/ Google Play</span>", h1="Your files. Your phone. No internet required.", h1_sub="Offline music player for Android",
  lede="VibeDeck Player is an offline music player for Android that plays the MP3, FLAC, WAV, AAC and more files you already own, with a 3-band EQ and gain, pitch and tempo control, and DJ tools. No streaming, no ads, no account.",
  visual=("a-main", "VibeDeck Player offline music player for Android with pitch control", "card"), ios=False, android=True,
  statement="Most Android music apps push you toward streaming: subscriptions, data usage, downloads that expire. VibeDeck Player goes the other way. It is an offline music player for the files sitting on your phone right now, with pro sound tools on one dark screen.",
  features_h2="Android player features",
  features=[("True offline", "No streaming, no buffering, no login. Your library lives on your Android phone and plays in airplane mode."),
            ("Every format", "MP3, FLAC, WAV, AAC and more in one queue. Your rips, downloads and DJ pool tracks, all playable without conversion."),
            ("Pro sound", "3-band EQ with gain, bass boost, pitch and tempo, waveform scrubbing and BPM readout, made for headphones.")],
  extra=prose_section('<h2>Why go offline on Android</h2><ul><li><strong>Travel</strong>: your whole library on flights and road trips, no WiFi needed</li><li><strong>Data</strong>: zero streaming means zero mobile data burned on music</li><li><strong>Ownership</strong>: the files you bought or ripped stay yours, nothing expires</li><li><strong>Privacy</strong>: no account, no tracking, files never leave the device</li></ul><p>Related: <a href="/offline-music-player-iphone/">offline music player for iPhone</a>, <a href="/mp3-player-no-ads/">MP3 player with no ads</a>.</p>'),
  faq_h2="Android player FAQ",
  faq=[("What is the best offline music player for Android?", "VibeDeck Player is built for offline listening on Android: your MP3, FLAC, WAV, AAC and more files play with no internet, no ads and no account, plus EQ, pitch, tempo and DJ tools you will not find in the stock player."),
       ("Can I play music on Android without internet?", "Yes. With VibeDeck Player your files are stored on the phone, so music keeps playing on planes, in the subway, or anywhere with no signal."),
       ("Does VibeDeck Player play FLAC on Android?", "Yes. VibeDeck Player plays FLAC, WAV, MP3, AAC, M4A and more from your local files on Android, with a 3-band EQ and gain, pitch shifting and tempo control applied in real time."),
       ("Where do the music files come from?", "Your own collection: downloads, rips, purchases, DJ pools. If you own the file, it plays."),
       ("Is VibeDeck Player free on Android?", FREE_A.replace("The core player", "The core offline player"))],
  related=["/offline-music-player-iphone/", "/mp3-player-no-ads/", "/music-player-pitch-tempo/"],
  cta="Offline music player for Android. No account. No ads. No tracking."),
 dict(path="/mp3-player-no-ads/", crumb="MP3 player with no ads",
  title="MP3 Player With No Ads – Offline, No Account | VibeDeck",
  desc="An MP3 player with no ads, no account and no tracking. Play your MP3 files offline on iPhone and Android with EQ, pitch and tempo. Download free.",
  og_desc="An MP3 player with zero ads. Play your own MP3 files offline on iPhone and Android, with EQ, pitch and DJ tools.",
  tag="iPhone · Android <span class=\"dim\">/ Zero ads</span>", h1="Your MP3s. Zero ads. Nothing in the way.", h1_sub="MP3 player with no ads",
  lede="VibeDeck Player is an MP3 player with no ads, no account and no tracking. Your MP3 files play offline on iPhone and Android, with a 3-band EQ and gain, pitch and tempo control, and DJ tools.",
  visual=("now-playing", "VibeDeck Player MP3 player with no ads, now playing view", "phone"), ios=True, android=True,
  statement="Free music apps usually mean one thing: ads between your songs, or a paywall to remove them. VibeDeck Player is free and still shows nothing. No banners, no videos, no popups. The business model is an optional Premium upgrade for the sound engine, not your attention.",
  features_h2="MP3 player features",
  features=[("No ads, ever", "No banners, no video breaks, no sponsored popups. Press play and hear music, not marketing."),
            ("Offline MP3", "Your MP3 files live on the device and play with no internet. Planes, subways, dead zones: all fine."),
            ("Pro sound", "3-band EQ with gain, bass boost, pitch and tempo, waveform scrubbing and BPM readout on one dark screen.")],
  extra=prose_section('<h2>Why an MP3 player with no ads matters</h2><ul><li><strong>Flow</strong>: nothing interrupts the song, the mix, or the workout</li><li><strong>Battery and data</strong>: no ad SDKs means less drain and zero ad traffic</li><li><strong>Privacy</strong>: ad-free also means no ad tracking; there is no account at all</li><li><strong>Kids and focus</strong>: hand the phone over without random video ads popping up</li></ul><p>Related: <a href="/offline-music-player-iphone/">offline music player for iPhone</a>, <a href="/offline-music-player-android/">offline music player for Android</a>.</p>'),
  faq_h2="MP3 player FAQ",
  faq=[("Is there really no ads in VibeDeck Player?", "Correct. VibeDeck Player shows no banner ads, no video ads and no popups. The free version is supported by an optional Premium upgrade, not by advertising."),
       ("Can I play my own MP3 files offline?", "Yes. VibeDeck Player plays MP3 files stored on your device with no internet connection. Your files are never uploaded anywhere."),
       ("How do I add MP3 files to VibeDeck Player?", "Import your MP3 files from local storage or file sharing, and they appear in your library. No account or sign-in is needed at any step."),
       ("Does it play anything besides MP3?", "Yes. VibeDeck Player also plays FLAC and WAV, so you can mix formats in one offline queue."),
       ("Is VibeDeck Player free?", FREE_A)],
  related=["/offline-music-player-iphone/", "/offline-music-player-android/", "/flac-player-iphone/"],
  cta="MP3 player with no ads for iPhone and Android. No account. No tracking."),
 dict(path="/music-player-pitch-tempo/", crumb="Pitch and tempo control",
  title="Music Player With Pitch & Tempo Control | VibeDeck",
  desc="Change a song's key by ±8 semitones and its tempo independently, offline on iPhone and Android. For singers, musicians, dancers and DJs. Download free.",
  og_desc="Shift pitch up to 8 semitones and change tempo independently, offline. A music player built for practice, rehearsal and DJ prep.",
  tag="iPhone · Android <span class=\"dim\">/ ±8 semitones</span>", h1="Change the key. Change the speed. Keep the song.", h1_sub="Music player with pitch &amp; tempo control",
  lede="VibeDeck Player is a music player with real-time pitch and tempo control. Shift pitch up to plus or minus 8 semitones, change tempo independently, and shape the sound with a filter, all offline on iPhone and Android.",
  visual=("b-pitch", "VibeDeck Player pitch and filter controls on iPhone", "card"), ios=True, android=True,
  statement="Most music players treat a song as fixed: press play, accept the key and the speed. VibeDeck Player treats it as material. Singers move tracks into their range, guitarists match odd tunings, dancers slow a routine down to learn it, DJs sketch transitions. All on the device, with no internet and no account.",
  features_h2="Pitch and tempo features",
  features=[("Pitch shifting", "Real-time pitch control up to plus or minus 8 semitones, right on the main screen next to the LP/HP filter."),
            ("Tempo control", "Slow down or speed up independently of pitch. Learn solos note by note, or push the energy up."),
            ("DJ toolkit", "Waveform scrubbing, BPM readout, 3-band EQ with gain and a limiter. Practice and prep without decks.")],
  extra=prose_section('<h2>Who uses pitch and tempo control</h2><ul><li><strong>Singers</strong>: move any song into a comfortable vocal range in seconds</li><li><strong>Guitarists and instrumentalists</strong>: match the track to your tuning, then slow the hard parts down</li><li><strong>Dancers</strong>: rehearse at half speed, perform at full speed, same key</li><li><strong>DJs</strong>: test how a track feels pitched up or down before it goes into a set</li><li><strong>Curious listeners</strong>: hear a familiar track in a new key just because you can</li></ul><p>Related: <a href="/flac-player-iphone/">FLAC player for iPhone</a>, <a href="/offline-music-player-android/">offline music player for Android</a>.</p>'),
  faq_h2="Pitch and tempo FAQ",
  faq=[("Can I change the key of a song with VibeDeck Player?", "Yes. VibeDeck Player shifts pitch in real time up to plus or minus 8 semitones, so you can move any track into your vocal range or match an instrument tuning without changing the file."),
       ("Can I slow down music without changing the pitch?", "Yes. Tempo and pitch are independent in VibeDeck Player. Slow a track down to learn a solo or speed it up for a workout while the key stays exactly where it was."),
       ("Is VibeDeck Player good for musicians and DJs?", "It is built for that use: pitch and filter on the main screen, waveform scrubbing, BPM readout, 3-band EQ with gain and a limiter, all working offline on your own files."),
       ("Does pitch shifting work offline?", "Yes. All processing happens on the device. Pitch, tempo, EQ and filter work in airplane mode with no account and no internet."),
       ("Is VibeDeck Player free?", FREE_A)],
  related=["/flac-player-iphone/", "/vibedeck-vs-vox/", "/offline-music-player-android/"],
  cta="Pitch and tempo control for your own music files. iPhone and Android. No ads."),
]

VOX_TABLE = '''<h2>Feature comparison</h2><p>Based on publicly listed features as of September 2026. Details can change; check the current App Store listings for both apps.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Feature</th><th scope="col">VOX</th><th scope="col">VibeDeck Player</th></tr></thead><tbody>
<tr><td>Platforms</td><td>iOS, iPadOS, macOS</td><td>iOS, iPadOS, Android</td></tr>
<tr><td>Local FLAC, MP3, WAV playback</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Fully offline, no account needed</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Ads</td><td>None</td><td>None</td></tr>
<tr><td>Equalizer</td><td>Yes</td><td>Yes, 3-band EQ + Gain</td></tr>
<tr><td>Real-time pitch shifting</td><td>No</td><td>Yes, up to +8 / -8 semitones</td></tr>
<tr><td>Tempo control</td><td>No</td><td>Yes, independent of pitch</td></tr>
<tr><td>Waveform scrubbing and BPM readout</td><td>No</td><td>Yes</td></tr>
</tbody></table></div>'''

PAGES.append(dict(path="/vibedeck-vs-vox/", crumb="VibeDeck Player vs VOX",
  title="VibeDeck vs VOX – Offline Music Player Comparison",
  desc="VibeDeck Player vs VOX: an honest comparison of two offline music players. Pitch and tempo, Android support, pricing and when to pick which.",
  og_desc="VOX vs VibeDeck Player: which offline music player fits you? Honest comparison of features, platforms and pricing.",
  tag="Compare <span class=\"dim\">/ VOX alternative</span>", h1="Two offline players. Different strengths.", h1_sub="VibeDeck Player vs VOX: an honest comparison",
  lede="VOX by Coppertino is the established offline music player on iPhone: polished, reliable, Apple-only. VibeDeck Player is the newer alternative built around one thing VOX does not do: real-time pitch and tempo control. Here is the honest breakdown.",
  visual=("b-eq", "VibeDeck Player sound controls compared with VOX", "card"), ios=True, android=True,
  statement="This is not a hit piece. VOX is a good player, and if your whole life is inside the Apple ecosystem and you never touch pitch controls, it will serve you well. VibeDeck Player exists for the listeners VOX leaves out: people who want to change the key and speed of their music, people on Android, and people who prefer paying once instead of subscribing forever.",
  features_h2="When to choose which",
  features=[("Pick VOX if", "You are all-in on Apple devices, want a mature player with years of polish, and never need to change a song's key or speed."),
            ("Pick VibeDeck Player if", "You sing, play, dance or DJ and want pitch and tempo tools; you use Android; or you want a lifetime license instead of a subscription."),
            ("Try both", "Both are free to start. Install each, load the same tracks, and keep the one that fits how you listen.")],
  extra=prose_section(VOX_TABLE, "comparison") + f'''
<section class="section" id="premium" aria-labelledby="premium-title">
  <div class="wrap">
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Pricing</p><h2 class="h2" id="premium-title">VibeDeck Premium pricing</h2></div><p class="lede">The core player is free with no ads. Premium unlocks the full sound engine: pitch and filter, 3-band EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.</p></div>
    {plans_html()}
  </div>
</section>''',
  faq_h2="VOX alternative FAQ",
  faq=[("Is VibeDeck Player a good alternative to VOX?", "If you want real-time pitch and tempo control, Android support, or a one-time lifetime license, yes. VOX remains a strong pick if you live entirely inside the Apple ecosystem and do not need pitch tools."),
       ("What does VibeDeck Player do that VOX does not?", "VibeDeck Player shifts pitch up to plus or minus 8 semitones and changes tempo independently in real time, runs on Android as well as iPhone, and offers a lifetime Premium license. VOX does not include built-in pitch or tempo control."),
       ("Do both players work offline without an account?", "Yes. Both VOX and VibeDeck Player play your local files offline with no account required and no ads interrupting playback."),
       ("Can I switch from VOX to VibeDeck Player?", "Yes. Both play the same local files, so your library moves over as-is. No conversion, no re-buying anything."),
       ("Does VibeDeck Player work on Android?", "Yes, unlike VOX it runs on Android as well as iPhone and iPad."),
       ("How much does VibeDeck Premium cost?", "On the App Store VibeDeck Premium costs $2.99 per month, $19.99 per year or $49.99 once for a lifetime license. On Google Play it costs $1.99 per month, $9.99 per year or $14.99 once. Prices may vary by region; the App Store and Google Play listings show the current local price."),
       ("Is there a free version?", "Yes, the core player is free with no ads on both platforms.")],
  related=["/music-player-pitch-tempo/", "/offline-music-player-iphone/", "/offline-music-player-android/"],
  cta="Try the VOX alternative with pitch and tempo control. Free, no ads, no account."))

# ---------------------------------------------------------------- LEGAL / SUPPORT
LEGAL = [
 ("support", "/support.html", "Support", "VibeDeck Support – Offline Music Player Help",
  "Get help with VibeDeck Player, the offline music player for MP3, FLAC, WAV, AAC and M4A: importing tracks, queue, EQ, pitch and tempo."),
 ("privacy", "/privacy.html", "Privacy", "VibeDeck Privacy Policy – Offline Music Player",
  "How VibeDeck Player handles your audio files, optional cover-art lookup and privacy. No account, no ads, no tracking, no data sold."),
 ("terms", "/terms.html", "Terms", "VibeDeck Terms of Use – Offline Music Player",
  "Terms of Use for VibeDeck Player, the offline music player for local MP3, FLAC, WAV, AAC and M4A files on iPhone, iPad and Android."),
]
def legal(slug, path, crumb, title, desc):
    src = open(os.path.join(ROOT, "_build", "content", slug + ".html")).read()
    hero = re.search(r'<section class="page-hero">(.*?)</section>', src, re.S).group(1)
    rest = src[src.index("</section>", src.index('class="page-hero"')) + len("</section>"):]
    hero = hero.replace('<p class="eyebrow">', '<p class="tag eyebrow">')
    hero = re.sub(r'<h1>(.*?)</h1>', r'<h1 class="h1-plain" id="hero-title">\1</h1>', hero, flags=re.S)
    hero = re.sub(r'</h1>\s*<p>', '</h1>\n<p class="lede" style="margin-top:24px">', hero)
    rest = re.sub(r'<section class="content">', '<section class="section"><div class="wrap"><div class="glass box prose">', rest)
    rest = rest.replace("</section>", "</div></div></section>")
    trail = [("Home", "/"), (crumb, path)]
    p = {"path": path, "title": title, "desc": desc, "ld": [ORG, WEBSITE, crumbs_ld(trail)]}
    body = f'''{header(crumb if crumb in ("Support", "Privacy") else None, "/#download")}
<main id="main">
<section class="hero hero--page" aria-labelledby="hero-title"><div class="wrap">{crumbs_html(trail)}{hero}</div></section>
{rest}
</main>
{footer()}'''
    write(path, head(p) + "\n" + body)
    return p

def notfound():
    p = {"path": "/404.html", "title": "Page not found – VibeDeck Player", "desc": "This page does not exist. Go back to VibeDeck Player, the offline music player for FLAC, MP3, WAV, AAC, M4A and more.", "noindex": True, "ld": [WEBSITE]}
    body = f'''{header(None, "/#download")}
<main id="main"><section class="hero hero--page"><div class="wrap"><p class="tag eyebrow">404 <span class="dim">/ Signal lost</span></p><h1 class="h1-plain">This track is not in the queue.</h1><p class="lede" style="margin-top:24px">The page you are looking for does not exist. Try the <a class="link" href="/">VibeDeck Player home page</a> or one of the guides below.</p></div></section>
{cards_html(GUIDES, "Guides", "Explore", "", "guides")}
</main>
{footer()}'''
    write("/404.html", head(p) + "\n" + body)
    return p

if __name__ == "__main__":
    out = [home()] + [landing(d) for d in PAGES] + [legal(*l) for l in LEGAL] + [notfound()]
    for p in out:
        print(f'{p["path"]:34} title {len(p["title"]):3}  desc {len(p["desc"]):3}')
