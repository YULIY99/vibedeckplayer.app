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
  "studio-live": ("vibedeck-studio-loop-slicer-iphone", (400,600,800), (1290,2796)),
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
  ("/offline-music-player-android/", "Offline · Android", "Offline music player for Android", "MP3, FLAC, ALAC, AIFF, WAV and AAC from your phone, with zero mobile data spent on music."),
  ("/mp3-player-no-ads/", "MP3 · No ads", "MP3 player with no ads", "No banners, no video breaks, no account. Press play and hear your MP3s."),
  ("/music-player-pitch-tempo/", "Pitch · Tempo", "Music player with pitch and tempo control", "Change the key by ±8 semitones and the speed independently, for practice and DJ prep."),
  ("/audio-formats/", "Formats · Hi-Res", "Music player for all audio formats", "FLAC, ALAC, AIFF, WAV, MP3, AAC, M4A and CAF, played offline with no conversion."),
  ("/change-song-key-iphone/", "How-to · Key", "Change the key of a song on iPhone", "Transpose any track up or down by semitones to fit your voice or instrument."),
  ("/slow-down-song/", "How-to · Tempo", "Slow down a song without changing pitch", "Learn fast parts, choreography and solos at your own speed, in the same key."),
  ("/flac-player-android/", "FLAC · Android", "FLAC player for Android", "Lossless FLAC offline on Android, with EQ, pitch and tempo. No ads."),
  ("/best-offline-music-player/", "Guide · 2026", "Best offline music player", "What to look for in an offline player in 2026, and how VibeDeck compares."),
  ("/#studio", "Studio · New", "VibeDeck Studio: remix and record clips", "Beat-snapped loops, live effects and session recording you can share as a clip."),
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
       "description": "Offline music player for local FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A files with 3-band EQ and gain, bass boost, filter, limiter, real-time pitch and tempo control, waveform and the AURA visualizer. No ads, account or tracking.",
       "url": SITE + "/", "image": SITE + "/assets/img/icon-512.png",
       "screenshot": [SITE + "/assets/img/vibedeck-offline-music-player-iphone-now-playing-800.webp",
                      SITE + "/assets/img/vibedeck-equalizer-iphone-720.webp",
                      SITE + "/assets/img/vibedeck-offline-music-player-android-720.webp"],
       "downloadUrl": [APPSTORE, PLAY], "installUrl": [APPSTORE, PLAY],
       "featureList": ["Offline playback for FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A", "3-band equalizer with gain, bass boost, filter and limiter",
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
<link rel="stylesheet" href="/styles.css?v=7">
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
        <p>Same Track. New Feeling. Offline music player for FLAC, ALAC, WAV &amp; MP3 on iPhone, iPad and Android.</p>
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
 ("Which audio formats does VibeDeck Player play?", "VibeDeck Player plays all popular audio formats stored on your device: MP3, WAV, FLAC (Hi-Res Lossless), M4A including Apple Lossless (ALAC), AAC, AIFF/AIF and CAF. No conversion and no cloud upload needed."),
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
    p = {"path": "/", "title": "VibeDeck Player: Offline Music Player for FLAC, WAV, MP3",
         "desc": "Offline music player for iPhone & Android. Plays FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A with EQ, pitch and tempo. No ads, no account. Free.",
         "og_title": "VibeDeck Player: Same Track. New Feeling.",
         "og_desc": "Shape FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A in real time with 3-band EQ, pitch, tempo, waveform and AURA on iOS and Android. No ads, account or tracking.",
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
      <h1 id="hero-title"><span class="h1-big">Same Track. <em>New Feeling.</em></span><span class="h1-sub">Offline music player for FLAC, ALAC, WAV &amp; MP3</span></h1>
      <p class="lede">Offline music player for iPhone, iPad and Android that plays MP3, FLAC, ALAC, AIFF, WAV and AAC from your local files, with equalizer, pitch and tempo control. No WiFi needed.</p>
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
    <div class="sec-head" data-reveal><div><p class="tag eyebrow">Features <span class="dim">/ {len(GUIDES):02d}</span></p><h2 class="h2" id="features-title">Pitch, EQ, AURA, TONE. <span class="soft">One dark screen.</span></h2></div><p class="lede">Every sound tool lives one move from the track: a music player with pitch and tempo control, a real equalizer for iPhone and Android, and visuals that react to the beat.</p></div>
    <nav class="tabs" aria-label="Feature screens">{tabs}</nav>
    <ol class="rail" aria-label="VibeDeck feature screens">{rail}</ol>
    <div class="rail-ctrl mono"><span>Swipe to explore · 6 screens</span><div class="rail-btns"><button type="button" data-rail="prev" aria-label="Previous screen">←</button><button type="button" data-rail="next" aria-label="Next screen">→</button></div></div>
  </div>
</section>

<section class="section studio-feature" id="studio" aria-labelledby="studio-title">
  <div class="wrap studio-feature-grid">
    <div class="studio-art" data-reveal>
      <div class="studio-glow" aria-hidden="true"></div>
      <figure class="phone phone--lg"><img src="/assets/img/vibedeck-studio-real-screen.png" alt="VibeDeck Studio on iPhone: beat-grid loop slicer, pitch, filter, effects and recording controls" width="1290" height="2796" loading="lazy" decoding="async"></figure>
    </div>
    <div class="studio-copy" data-reveal>
      <p class="tag eyebrow">New <span class="dim">/ VibeDeck Studio</span></p>
      <h2 class="h2" id="studio-title">VibeDeck Studio.<br><span class="soft">Remix &amp; Clips.</span></h2>
      <p class="lede">Turn a moment in your track into a loop, shape its sound, then record and share the result—all in the same player.</p>
      <ul class="studio-points" aria-label="VibeDeck Studio features">
        <li><span class="studio-index mono">01</span><span><strong>Loop to the beat</strong><small>Choose ½ to 8 bars, snapped to the beat grid.</small></span></li>
        <li><span class="studio-index mono">02</span><span><strong>Fine-tune every cut</strong><small>Adjust the grid and loop start or end.</small></span></li>
        <li><span class="studio-index mono">03</span><span><strong>Shape the sound</strong><small>Pitch, filter, saturation, space and sound presets.</small></span></li>
        <li><span class="studio-index mono">04</span><span><strong>Record and share</strong><small>Capture a live session up to 2 minutes, add fade in/out, and share it as a clip.</small></span></li>
        <li><span class="studio-index mono">05</span><span><strong>Keep it playing</strong><small>Studio plays in the background.</small></span></li>
        <li><span class="studio-index mono">06</span><span><strong>Made smoother</strong><small>Faster track analysis, smoother reverb, refreshed design.</small></span></li>
      </ul>
      <a class="studio-link mono" href="#download">Explore VibeDeck <span aria-hidden="true">↗</span></a>
    </div>
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
    <ul class="chips"><li>All popular formats</li><li>FLAC</li><li>ALAC</li><li>AIFF</li><li>WAV</li><li>MP3</li><li>AAC</li><li>M4A</li><li>CAF</li><li>±8 semitones</li><li>Tempo</li><li>3-band EQ</li><li>Limiter</li><li>Offline</li><li>No ads</li><li>No account</li><li>No tracking</li></ul>
  </div>
</section>

{cards_html(GUIDES, 'Built for <span class="soft">the way you listen.</span>', 'Built for <span class="dim">/ {len(GUIDES):02d}</span>', "Guides for every way people use VibeDeck Player.")}

<section class="section" id="why" aria-labelledby="why-title">
  <div class="wrap duo duo--rev">
    <div class="duo-copy prose" data-reveal>
      <p class="tag eyebrow">Why VibeDeck</p>
      <h2 id="why-title">Why VibeDeck Player?</h2>
      <p>VibeDeck Player is a premium <strong>offline music player for iPhone, iPad and Android</strong>, made for people who own their music. It plays the FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A files already on your phone, with no WiFi, no account, no ads and no tracking. Your files stay on your device.</p>
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

{prose_section('<h2>VibeDeck Player at a glance</h2><div class="table-wrap"><table><tbody><tr><th scope="row">Platforms</th><td>iPhone and iPad (iOS 17+), Android</td></tr><tr><th scope="row">Audio formats</th><td>MP3, WAV, FLAC, M4A / ALAC, AAC, AIFF / AIF, CAF</td></tr><tr><th scope="row">Sound</th><td>3-band EQ with gain, bass boost, filter, stereo balance, limiter</td></tr><tr><th scope="row">Pitch and tempo</th><td>Pitch up to ±8 semitones, tempo independent from pitch</td></tr><tr><th scope="row">Visuals</th><td>AURA waveform, VibeMod and TONE, music-reactive starry sky with comets</td></tr><tr><th scope="row">Internet</th><td>Not needed: plays files stored on your device</td></tr><tr><th scope="row">Ads, account, tracking</th><td>None</td></tr><tr><th scope="row">Price on App Store</th><td>Free; Premium $2.99/month, $19.99/year, $49.99 lifetime</td></tr><tr><th scope="row">Price on Google Play</th><td>Free; Premium $1.99/month, $9.99/year, $14.99 lifetime</td></tr></tbody></table></div><p class="dim">Prices may vary by region.</p>')}
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
  title="FLAC Player for iPhone, Lossless | VibeDeck Player",
  desc="Play lossless FLAC files offline on iPhone and iPad with 3-band EQ, pitch and tempo control. No ads, no account, no tracking. Download VibeDeck free.",
  og_desc="Play your FLAC collection offline on iPhone and iPad. Lossless audio with EQ, pitch, tempo and DJ tools. No ads or account.",
  tag="iPhone · iPad <span class=\"dim\">/ Lossless</span>", h1="Your FLAC collection, finally at home on iPhone.", h1_sub="FLAC player for iPhone &amp; iPad",
  lede="VibeDeck Player plays lossless FLAC files offline on iPhone and iPad, with a 3-band EQ and gain, pitch and tempo control, waveform scrubbing and DJ tools. No ads. No account. No tracking.",
  visual=("aura-live", "VibeDeck Player FLAC player for iPhone with pitch control", "phone"), ios=True, android=False,
  statement="iPhone plays FLAC, but the built-in options treat your lossless library as an afterthought: no equalizer, no pitch control, no waveform, no DJ tools. VibeDeck Player is built for people who own their music in FLAC and want to hear every detail of it, shaped exactly the way they like.",
  features_h2="FLAC player features",
  features=[("Lossless playback", "FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A from your local files. Your audio stays on the device, with no streaming and no conversion."),
            ("Real EQ", "3-band EQ with gain, bass boost, filter, stereo balance and a limiter. Shape lossless sound in real time instead of accepting a flat default."),
            ("Pitch and tempo", "Shift pitch up to 8 semitones and change tempo independently. Practice, DJ prep, or just hear a track differently.")],
  extra=prose_section('<h2>Formats VibeDeck Player plays</h2><p>Drop your files in and press play. No conversion, no cloud upload.</p><ul><li><strong>FLAC</strong>: lossless, your main archive format</li><li><strong>WAV</strong>: uncompressed studio files</li><li><strong>MP3</strong>: your existing library and downloads</li><li><strong>ALAC / M4A</strong>: Apple Lossless from your Mac or iTunes library</li><li><strong>AIFF / AIF</strong>: studio masters</li><li><strong>AAC and CAF</strong>: compact and Apple Core Audio files</li></ul><p>Full list: <a href="/audio-formats/">audio formats VibeDeck Player supports</a>.</p><p>Also see: <a href="/offline-music-player-iphone/">offline music player for iPhone</a>, <a href="/music-player-pitch-tempo/">pitch and tempo control</a>.</p>'),
  faq_h2="FLAC player FAQ",
  faq=[("Can iPhone play FLAC files?", "Yes. iPhone can play FLAC files, but the built-in options give you no equalizer, no pitch control and no real library for your own files. VibeDeck Player is a dedicated FLAC player for iPhone and iPad that plays your lossless files offline with full sound controls."),
       ("Does VibeDeck Player work without internet?", "Yes. VibeDeck Player is an offline music player. Your FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A files stay on your device and play with no WiFi, no account and no ads."),
       ("Does it have an equalizer for FLAC playback?", "Yes. VibeDeck Player includes a 3-band EQ with gain, bass boost, filter, stereo balance and a built-in limiter, all applied in real time to your FLAC files."),
       ("Can I change pitch and tempo of FLAC tracks?", "Yes. VibeDeck Player offers real-time pitch shifting up to plus or minus 8 semitones and independent tempo control, which is rare among iPhone FLAC players."),
       ("Is VibeDeck Player free?", "The core player is free with no ads. VibeDeck Premium unlocks the full sound engine: pitch and filter, 3-band EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.")],
  related=["/offline-music-player-iphone/", "/music-player-pitch-tempo/", "/vibedeck-vs-vox/"],
  cta="Play your FLAC files offline on iPhone and iPad. No account. No ads. No tracking."),
 dict(path="/offline-music-player-iphone/", crumb="Offline music player for iPhone",
  title="Offline Music Player for iPhone | VibeDeck Player",
  desc="Offline music player for iPhone and iPad. Play MP3, FLAC, ALAC, AIFF, WAV and AAC with no internet, no ads, no account. EQ, pitch and tempo. Download free.",
  og_desc="Your music, on your iPhone, with no internet. Offline player for MP3, FLAC, ALAC, AIFF, WAV and AAC with EQ, pitch and DJ tools.",
  tag="iPhone · iPad <span class=\"dim\">/ No WiFi</span>", h1="Music that plays when the internet does not.", h1_sub="Offline music player for iPhone &amp; iPad",
  lede="Plane mode, dead zones, roaming bills. VibeDeck Player keeps your MP3, FLAC, ALAC, AIFF, WAV and AAC on the device and playing, with EQ, pitch, tempo and DJ tools. No WiFi needed, ever.",
  visual=("b-queue", "VibeDeck Player offline music player queue on iPhone", "card"), ios=True, android=False,
  statement="Streaming apps rent you music and take it away the moment you stop paying or lose signal. VibeDeck Player is the opposite: an offline music player for the files you own. Import once, listen anywhere, shape the sound in real time.",
  features_h2="Offline features",
  features=[("True offline", "No streaming, no buffering, no login. Your library lives on your iPhone and plays in airplane mode."),
            ("Your formats", "MP3, FLAC, ALAC, AIFF, WAV and AAC. Mix lossy and lossless in one queue without thinking about it."),
            ("Pro sound", "3-band EQ with gain, bass boost, pitch and tempo, waveform scrubbing and BPM readout, all on one dark screen.")],
  extra=prose_section('<h2>Why go offline on iPhone</h2><ul><li><strong>Flights and travel</strong>: your whole library, no WiFi required</li><li><strong>No subscription</strong>: the music you own stays yours</li><li><strong>Battery</strong>: local playback sips power compared to streaming</li><li><strong>Privacy</strong>: no account, no tracking, files never leave the device</li></ul><p>Related: <a href="/flac-player-iphone/">FLAC player for iPhone</a>, <a href="/mp3-player-no-ads/">MP3 player with no ads</a>.</p>'),
  faq_h2="Offline player FAQ",
  faq=[("What is the best offline music player for iPhone?", "VibeDeck Player is built for offline listening on iPhone and iPad: your MP3, FLAC, ALAC, AIFF, WAV, AAC and M4A files play with no internet, no ads and no account, plus EQ, pitch, tempo and DJ tools you will not find in stock apps."),
       ("Can I play music on iPhone without internet?", "Yes. With VibeDeck Player your files are stored on the device, so music keeps playing on planes, in the subway, or anywhere with no signal."),
       ("Does Apple Music work offline?", "Apple Music needs a paid subscription for offline downloads and locks you into its ecosystem. VibeDeck Player plays files you already own, with no subscription and no lock-in."),
       FILES_Q,
       ("Is VibeDeck Player free?", FREE_A.replace("The core player", "The core offline player"))],
  related=["/flac-player-iphone/", "/mp3-player-no-ads/", "/offline-music-player-android/"],
  cta="Offline music player for iPhone and iPad. No account. No ads. No tracking."),
 dict(path="/offline-music-player-android/", crumb="Offline music player for Android",
  title="Offline Music Player for Android | VibeDeck Player",
  desc="Offline music player for Android. Play MP3, FLAC, ALAC, AIFF, WAV and AAC with no internet, no ads, no account. 3-band EQ, pitch and tempo. On Google Play.",
  og_desc="Your music, on your Android phone, with no internet. Offline player for MP3, FLAC, ALAC, AIFF, WAV and AAC with EQ, pitch and DJ tools.",
  tag="Android <span class=\"dim\">/ Google Play</span>", h1="Your files. Your phone. No internet required.", h1_sub="Offline music player for Android",
  lede="VibeDeck Player is an offline music player for Android that plays the MP3, FLAC, ALAC, AIFF, WAV, AAC and M4A files you already own, with a 3-band EQ and gain, pitch and tempo control, and DJ tools. No streaming, no ads, no account.",
  visual=("a-main", "VibeDeck Player offline music player for Android with pitch control", "card"), ios=False, android=True,
  statement="Most Android music apps push you toward streaming: subscriptions, data usage, downloads that expire. VibeDeck Player goes the other way. It is an offline music player for the files sitting on your phone right now, with pro sound tools on one dark screen.",
  features_h2="Android player features",
  features=[("True offline", "No streaming, no buffering, no login. Your library lives on your Android phone and plays in airplane mode."),
            ("Every format", "MP3, FLAC, ALAC, AIFF, WAV and AAC in one queue. Your rips, downloads and DJ pool tracks, all playable without conversion."),
            ("Pro sound", "3-band EQ with gain, bass boost, pitch and tempo, waveform scrubbing and BPM readout, made for headphones.")],
  extra=prose_section('<h2>Why go offline on Android</h2><ul><li><strong>Travel</strong>: your whole library on flights and road trips, no WiFi needed</li><li><strong>Data</strong>: zero streaming means zero mobile data burned on music</li><li><strong>Ownership</strong>: the files you bought or ripped stay yours, nothing expires</li><li><strong>Privacy</strong>: no account, no tracking, files never leave the device</li></ul><p>Related: <a href="/offline-music-player-iphone/">offline music player for iPhone</a>, <a href="/mp3-player-no-ads/">MP3 player with no ads</a>.</p>'),
  faq_h2="Android player FAQ",
  faq=[("What is the best offline music player for Android?", "VibeDeck Player is built for offline listening on Android: your MP3, FLAC, ALAC, AIFF, WAV, AAC and M4A files play with no internet, no ads and no account, plus EQ, pitch, tempo and DJ tools you will not find in the stock player."),
       ("Can I play music on Android without internet?", "Yes. With VibeDeck Player your files are stored on the phone, so music keeps playing on planes, in the subway, or anywhere with no signal."),
       ("Does VibeDeck Player play FLAC on Android?", "Yes. VibeDeck Player plays FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A from your local files on Android, with a 3-band EQ and gain, pitch shifting and tempo control applied in real time."),
       ("Where do the music files come from?", "Your own collection: downloads, rips, purchases, DJ pools. If you own the file, it plays."),
       ("Is VibeDeck Player free on Android?", FREE_A.replace("The core player", "The core offline player"))],
  related=["/offline-music-player-iphone/", "/mp3-player-no-ads/", "/music-player-pitch-tempo/"],
  cta="Offline music player for Android. No account. No ads. No tracking."),
 dict(path="/mp3-player-no-ads/", crumb="MP3 player with no ads",
  title="MP3 Player With No Ads, Offline | VibeDeck Player",
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
  title="Music Player With Pitch & Tempo | VibeDeck Player",
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

PAGES.append(dict(path="/audio-formats/", crumb="Supported audio formats",
  title="FLAC, ALAC, AIFF and WAV Player | VibeDeck Player",
  desc="One offline player for FLAC, ALAC, AIFF, WAV, MP3, AAC, M4A and CAF on iPhone, iPad and Android. No conversion, no ads, with EQ, pitch and tempo.",
  og_desc="FLAC, ALAC, AIFF, WAV, MP3, AAC, M4A and CAF in one offline player. No conversion, no ads.",
  tag="Formats <span class=\"dim\">/ Hi-Res</span>", h1="Every format you own. One player.", h1_sub="FLAC, ALAC, AIFF &amp; WAV player",
  lede="VibeDeck Player plays the audio files you already have: hi-res FLAC, Apple Lossless (ALAC), AIFF studio masters, WAV, MP3, AAC, M4A and CAF. No conversion, no cloud upload, no internet.",
  visual=("aura-live", "VibeDeck Player playing a lossless track on iPhone", "phone"), ios=True, android=True,
  statement="Most music libraries are a mix: FLAC rips, ALAC from an old iTunes library, AIFF and WAV from the studio, MP3 from everywhere else. Built-in players handle some of them and hide the rest. VibeDeck Player opens them all in one library and plays them offline, with the same EQ, pitch and tempo controls for every file.",
  features_h2="Why one player for every format",
  features=[("No conversion", "Import files as they are. Lossless stays lossless: FLAC, ALAC, AIFF and WAV play from your device exactly as you imported them, with no conversion."),
            ("One sound engine", "3-band EQ with gain, limiter, pitch up to ±8 semitones and independent tempo work the same on MP3 and on a 24-bit master."),
            ("Fully offline", "Files live on your phone. No streaming, no account, no ads, no tracking.")],
  extra=prose_section('<h2>Supported audio formats</h2><ul><li><strong>FLAC</strong> (.flac): hi-res lossless, the standard archive format</li><li><strong>ALAC</strong> (.m4a): Apple Lossless from iTunes or Music on Mac</li><li><strong>AIFF / AIF</strong> (.aiff, .aif): uncompressed studio masters</li><li><strong>WAV</strong> (.wav): uncompressed audio from DAWs and recorders</li><li><strong>MP3</strong> (.mp3): the most common compressed format</li><li><strong>AAC / M4A</strong> (.aac, .m4a): compact files from stores and phones</li><li><strong>CAF</strong> (.caf): Apple Core Audio files</li></ul><p>OGG, WMA and Opus are not supported yet. Convert them to FLAC or AAC before importing.</p><h2>Lossless vs compressed: what to keep</h2><p>For your archive keep FLAC or ALAC: they are lossless and about half the size of WAV or AIFF. Use WAV or AIFF for files you still edit. MP3 and AAC are fine for everyday listening when space is tight. VibeDeck Player plays all of them side by side, so you never have to choose one format for the whole library.</p><p>Also see: <a href="/flac-player-iphone/">FLAC player for iPhone</a>, <a href="/offline-music-player-iphone/">offline music player for iPhone</a>, <a href="/offline-music-player-android/">offline music player for Android</a>.</p>'),
  faq_h2="Audio formats FAQ",
  faq=[("What audio formats does VibeDeck Player support?", "VibeDeck Player plays MP3, WAV, FLAC, M4A including Apple Lossless (ALAC), AAC, AIFF/AIF and CAF files stored on your device."),
       ("Can I play ALAC (Apple Lossless) files on iPhone?", "Yes. VibeDeck Player plays ALAC files in .m4a containers offline on iPhone and iPad, with EQ, pitch and tempo control."),
       ("Does VibeDeck Player play AIFF and WAV?", "Yes. AIFF, AIF and WAV files play without conversion, including 24-bit studio files."),
       ("Does VibeDeck Player support OGG, WMA or Opus?", "Not yet. Convert OGG, WMA or Opus files to FLAC or AAC and import them into VibeDeck Player."),
       ("Do I need to convert my files before importing?", "No. Import FLAC, ALAC, AIFF, WAV, MP3, AAC, M4A and CAF files as they are. Nothing is converted or uploaded.")],
  related=["/flac-player-iphone/", "/offline-music-player-iphone/", "/offline-music-player-android/"],
  cta="Play every file you own, offline. No conversion. No ads. No tracking."))
PAGES.append(dict(path="/change-song-key-iphone/", crumb="Change the key of a song on iPhone",
  title="Change the Key of a Song on iPhone | VibeDeck Player",
  desc="Change a song's key on iPhone in seconds: transpose up or down by up to 8 semitones, keep the tempo, work offline. Step-by-step guide with VibeDeck Player.",
  og_desc="Transpose any song on iPhone by up to ±8 semitones without changing tempo. Step-by-step guide.",
  tag="How-to <span class=\"dim\">/ Key</span>", h1="How to change the key of a song on iPhone.", h1_sub="Transpose any track by semitones",
  lede="To change the key of a song on iPhone, open the track in VibeDeck Player, go to Pitch and move it up or down in semitones (up to ±8). Tempo stays the same, the change is instant, and it works offline with your own MP3, FLAC, WAV, AAC and ALAC files.",
  visual=("b-pitch", "Changing the key of a song with VibeDeck Player pitch control on iPhone", "card"), ios=True, android=True,
  statement="The built-in Music app on iPhone cannot transpose a song. Singers, guitarists and sax players end up hunting for karaoke versions or re-recording backing tracks. A real-time pitch shifter fixes that in one move: the same recording, in the key that fits your voice or instrument.",
  features_h2="Why use VibeDeck Player to transpose",
  features=[("Semitone steps", "Move a song up or down by up to 8 semitones. One semitone is one piano key, so you always know exactly where you are."),
            ("Tempo stays", "Pitch and tempo are independent. Change the key and the song keeps its original speed, or slow it down as well."),
            ("Your own files, offline", "Works on local MP3, FLAC, WAV, AAC, ALAC and AIFF files. No upload, no internet, no account.")],
  extra=prose_section('<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store (it is also on Google Play for Android).</li><li>Import your track from Files, iCloud Drive, Downloads or AirDrop.</li><li>Start playback and open the <strong>Pitch</strong> control.</li><li>Move pitch down to make a song lower (for example −2 for a deeper voice) or up to make it higher.</li><li>Sing or play along. Tempo is not affected unless you change it.</li></ol><h2>How many semitones do I need?</h2><ul><li><strong>Too high to sing:</strong> try −1 to −3 semitones.</li><li><strong>Female vocal sung by a male voice:</strong> often −3 to −5.</li><li><strong>Eb-tuned guitar track, standard-tuned guitar:</strong> +1 semitone.</li><li><strong>Bb instrument (trumpet, tenor sax) reading concert pitch:</strong> −2 semitones.</li><li><strong>Eb instrument (alto sax):</strong> +3 semitones.</li></ul><p>Pitch control is part of VibeDeck Premium; the player itself is free with no ads.</p><p>Also see: <a href="/slow-down-song/">slow down a song without changing pitch</a>, <a href="/music-player-pitch-tempo/">music player with pitch and tempo control</a>.</p>'),
  faq_h2="Changing key on iPhone: FAQ",
  faq=[("Can you change the key of a song on iPhone?", "Yes. The built-in Music app cannot, but VibeDeck Player can: it shifts the pitch of any local song by up to plus or minus 8 semitones in real time, without changing tempo."),
       ("Does changing the key change the speed?", "No. In VibeDeck Player pitch and tempo are independent, so the song keeps its original speed when you transpose it."),
       ("Can I transpose Apple Music or Spotify songs?", "No. Streaming apps protect their tracks, so no third-party app can process them. VibeDeck Player works with audio files you own, such as MP3, FLAC, WAV, AAC and ALAC."),
       ("Does it work offline?", "Yes. Transposing happens on your iPhone, with no internet connection and no upload."),
       ("Is pitch control free?", "VibeDeck Player is free to download with no ads. Pitch and the full sound engine are part of VibeDeck Premium: monthly, yearly or a one-time lifetime purchase.")],
  related=["/slow-down-song/", "/music-player-pitch-tempo/", "/flac-player-iphone/"],
  cta="Put any song in your key. Offline, instantly, no ads."))
PAGES.append(dict(path="/slow-down-song/", crumb="Slow down a song without changing pitch",
  title="Slow Down a Song, Keep the Pitch | VibeDeck Player",
  desc="Slow down any song on iPhone or Android without changing its pitch. Practice solos, choreography and lyrics at your own speed, offline. Step-by-step guide.",
  og_desc="Change song speed without changing pitch on iPhone and Android. Practice at your own tempo.",
  tag="How-to <span class=\"dim\">/ Tempo</span>", h1="Slow down a song without changing its pitch.", h1_sub="Tempo control for practice",
  lede="To slow down a song without changing pitch, open it in VibeDeck Player and lower the Tempo control. The song plays slower but stays in the same key, so you can learn a solo, a dance routine or fast lyrics, then bring it back to full speed. Works offline on iPhone, iPad and Android.",
  visual=("now-playing", "Slowing down a song without changing pitch in VibeDeck Player", "phone"), ios=True, android=True,
  statement="Playing a track slower on a basic player makes it sound low and muddy, like a tape running down. Time-stretching keeps the key while the speed changes, which is how musicians and dancers actually practice: slow first, then faster, then full tempo.",
  features_h2="Built for practice",
  features=[("Same key, any speed", "Tempo is independent from pitch, so a slowed-down song stays in tune with your instrument."),
            ("Change key too", "Need it slower and lower? Combine tempo with pitch shifting of up to ±8 semitones."),
            ("Offline and private", "Your files stay on your device. No upload, no internet, no ads during practice.")],
  extra=prose_section('<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store or Google Play.</li><li>Import the song from your files.</li><li>Open the <strong>Tempo</strong> control and lower it until the hard part is comfortable.</li><li>Practice, then raise the tempo step by step until you reach the original speed.</li></ol><h2>Who uses it</h2><ul><li><strong>Guitarists and pianists</strong> learning solos and fast passages by ear.</li><li><strong>Dancers and coaches</strong> rehearsing choreography at a slower count.</li><li><strong>Singers</strong> catching fast lyrics and runs.</li><li><strong>DJs</strong> preparing transitions at matching tempo.</li><li><strong>Language learners</strong> listening to songs or recordings more slowly.</li></ul><p>Tempo and pitch are part of VibeDeck Premium; the player itself is free with no ads.</p><p>Also see: <a href="/change-song-key-iphone/">change the key of a song on iPhone</a>, <a href="/music-player-pitch-tempo/">pitch and tempo control</a>.</p>'),
  faq_h2="Slowing down songs: FAQ",
  faq=[("How do I slow down a song without changing the pitch?", "Use a player with independent tempo control, such as VibeDeck Player. Lower the tempo and the song plays slower in the same key."),
       ("Can I slow down music on iPhone?", "Yes. VibeDeck Player slows down local music files on iPhone and iPad without changing pitch, offline."),
       ("Does it work on Android?", "Yes. VibeDeck Player is available on Google Play with the same tempo and pitch controls."),
       ("Which files can I slow down?", "Any file VibeDeck Player plays: MP3, WAV, FLAC, M4A/ALAC, AAC, AIFF and CAF. Streaming tracks from Spotify or Apple Music cannot be processed by third-party apps."),
       ("Can I also change the key?", "Yes. Pitch and tempo are independent, so you can slow a song down and transpose it by up to plus or minus 8 semitones at the same time.")],
  related=["/change-song-key-iphone/", "/music-player-pitch-tempo/", "/offline-music-player-android/"],
  cta="Practice at your speed, in your key. Offline. No ads."))
PAGES.append(dict(path="/flac-player-android/", crumb="FLAC player for Android",
  title="FLAC Player for Android, No Ads | VibeDeck Player",
  desc="Play lossless FLAC on Android offline with a 3-band EQ, pitch and tempo control. Also WAV, MP3, AAC, M4A and AIFF. No ads, no account. Free on Google Play.",
  og_desc="Lossless FLAC on Android, offline, with EQ, pitch and tempo. No ads, no account.",
  tag="Android <span class=\"dim\">/ Lossless</span>", h1="A FLAC player for Android that respects your files.", h1_sub="FLAC player for Android",
  lede="VibeDeck Player plays lossless FLAC files offline on Android, with a 3-band EQ and gain, a limiter, pitch and tempo control, and a waveform you can scrub. It also plays WAV, MP3, AAC, M4A and AIFF. No ads. No account. No tracking.",
  visual=("a-main", "VibeDeck Player FLAC player for Android", "card"), ios=False, android=True,
  statement="Plenty of Android players open FLAC. Few of them do it without banner ads, account prompts or a dated interface. VibeDeck Player treats a lossless library the way it deserves: clean playback, real sound controls and nothing between you and the music.",
  features_h2="FLAC on Android, done right",
  features=[("Lossless, offline", "FLAC plays straight from your phone storage. No streaming, no mobile data, no conversion."),
            ("Real sound controls", "3-band EQ with gain, bass boost, filter, stereo balance and a limiter, in real time."),
            ("Pitch and tempo", "Shift pitch up to ±8 semitones and change tempo independently, for practice or DJ prep.")],
  extra=prose_section('<h2>Formats on Android</h2><ul><li><strong>FLAC</strong>: lossless archive format</li><li><strong>WAV</strong> and <strong>AIFF</strong>: uncompressed studio files</li><li><strong>MP3</strong>, <strong>AAC</strong> and <strong>M4A</strong>: everyday compressed files</li></ul><h2>How to start</h2><ol><li>Install VibeDeck Player from Google Play.</li><li>Copy FLAC files to your phone or download them to storage.</li><li>Import them into VibeDeck Player and press play. No internet needed.</li></ol><p>Also see: <a href="/offline-music-player-android/">offline music player for Android</a>, <a href="/audio-formats/">supported audio formats</a>.</p>'),
  faq_h2="FLAC on Android: FAQ",
  faq=[("Can Android play FLAC files?", "Yes. Android supports FLAC, and VibeDeck Player adds what basic players lack: a real EQ, pitch and tempo control, a waveform and no ads."),
       ("Is there a FLAC player for Android without ads?", "Yes. VibeDeck Player has no ads in the free version or in Premium, and needs no account."),
       ("Does it work offline?", "Yes. FLAC files play from your device with no internet and no mobile data."),
       ("Does it have an equalizer?", "Yes. A 3-band EQ with gain, bass boost, filter, stereo balance and a limiter."),
       ("How much does it cost on Android?", "Free to download. VibeDeck Premium on Google Play costs $1.99 per month, $9.99 per year or $14.99 once for lifetime access. Prices may vary by region.")],
  related=["/offline-music-player-android/", "/audio-formats/", "/music-player-pitch-tempo/"],
  cta="Your FLAC library on Android. Offline. No ads. No tracking."))
PAGES.append(dict(path="/best-offline-music-player/", crumb="Best offline music player",
  title="Best Offline Music Player in 2026 | VibeDeck Player",
  desc="How to choose the best offline music player in 2026: formats, EQ, pitch and tempo, ads, privacy, price. A clear checklist and how VibeDeck Player compares.",
  og_desc="The 2026 checklist for choosing an offline music player, and how VibeDeck Player compares.",
  tag="Guide <span class=\"dim\">/ 2026</span>", h1="The best offline music player in 2026: what actually matters.", h1_sub="Offline music player buying guide",
  lede="The best offline music player plays every file you own without conversion, works with no internet, has real sound controls and shows no ads. VibeDeck Player is built around exactly that checklist, on iPhone, iPad and Android.",
  visual=("b-queue", "VibeDeck Player offline music player library and queue", "card"), ios=True, android=True,
  statement="Streaming made music easy and made owning it feel old-fashioned. Then came flights, dead zones, roaming bills, removed albums and price rises. If you keep your own files, the player you choose decides how good they sound and how much they annoy you. Here is what to check.",
  features_h2="The 2026 checklist",
  features=[("Formats without conversion", "FLAC, ALAC, AIFF and WAV for lossless, MP3, AAC and M4A for everyday files. Anything that forces conversion loses quality and time."),
            ("Real controls", "A proper EQ with a limiter, plus pitch and tempo if you sing, play, dance or DJ. Most players stop at a basic preset list."),
            ("No ads, no account", "Ads and logins are the most common complaints in player reviews. Offline should mean private.")],
  extra=prose_section('<h2>How VibeDeck Player compares</h2><div class="table-wrap"><table><thead><tr><th>What to check</th><th>VibeDeck Player</th><th>Built-in iPhone Music app</th></tr></thead><tbody><tr><td>FLAC, ALAC, AIFF, WAV from Files</td><td>Yes</td><td>Limited</td></tr><tr><td>Works fully offline</td><td>Yes</td><td>Downloaded tracks only</td></tr><tr><td>3-band EQ with limiter</td><td>Yes</td><td>Presets only</td></tr><tr><td>Pitch shift ±8 semitones</td><td>Yes</td><td>No</td></tr><tr><td>Independent tempo</td><td>Yes</td><td>No</td></tr><tr><td>No ads, no account</td><td>Yes</td><td>Requires Apple ID</td></tr><tr><td>Android version</td><td>Yes</td><td>No</td></tr></tbody></table></div><h2>Pick by use case</h2><ul><li><strong>Lossless collectors:</strong> <a href="/flac-player-iphone/">FLAC player for iPhone</a>, <a href="/flac-player-android/">FLAC player for Android</a>.</li><li><strong>Travel and dead zones:</strong> <a href="/offline-music-player-iphone/">offline player for iPhone</a>, <a href="/offline-music-player-android/">for Android</a>.</li><li><strong>Singers and musicians:</strong> <a href="/change-song-key-iphone/">change key</a>, <a href="/slow-down-song/">slow down without changing pitch</a>.</li><li><strong>Leaving a cloud player:</strong> <a href="/vibedeck-vs-vox/">VibeDeck Player vs VOX</a>.</li></ul>'),
  faq_h2="Offline music players: FAQ",
  faq=[("What is the best offline music player for iPhone?", "Look for a player that imports FLAC, ALAC, AIFF and WAV without conversion, works with no internet, has a real EQ and shows no ads. VibeDeck Player covers all of these and adds pitch and tempo control."),
       ("What is the best offline music player for Android?", "The same checklist applies. VibeDeck Player is available on Google Play with FLAC support, a 3-band EQ, pitch and tempo, no ads and no account."),
       ("Can I listen to music without internet on my phone?", "Yes, if the files are stored on the phone. Copy or download your music, import it into an offline player like VibeDeck Player and it plays with WiFi and mobile data off."),
       ("Is there a free offline music player with no ads?", "Yes. VibeDeck Player is free to download and has no ads. Premium adds the full sound engine with pitch, EQ gain, limiter and visuals."),
       ("Which audio formats should an offline player support?", "At least MP3, AAC and M4A for everyday files and FLAC, ALAC, WAV and AIFF for lossless. VibeDeck Player supports all of them plus CAF.")],
  related=["/offline-music-player-iphone/", "/flac-player-android/", "/vibedeck-vs-vox/"],
  cta="The offline player built around the checklist. Free, no ads."))
PAGES.append(dict(path="/studio/", crumb="VibeDeck Studio",
  title="Slowed + Reverb, Nightcore & Loop Maker | VibeDeck Player",
  desc="VibeDeck Studio, coming in the next update: cut loops by beats and bars, add slowed + reverb, nightcore or dub delay in one tap, export clips for TikTok.",
  og_desc="Loop slicer, one-tap slowed + reverb and nightcore, export to WAV, M4A and MP4 for TikTok. Coming soon.",
  tag="Studio <span class=\"dim\">/ Coming soon</span>", h1="VibeDeck Studio: remix and clip your music.", h1_sub="Slowed + reverb, nightcore and loop maker",
  lede="VibeDeck Studio is coming to VibeDeck Player in the next update. Slice any track into loops from one beat to 16 bars, apply one-tap effects like Slowed + Reverb, Nightcore, Underwater and Dub Delay, fine-tune pitch, filter and limiter, then export a clip for TikTok, Reels or Shorts.",
  visual=("studio-live", "VibeDeck Studio loop slicer and quick FX presets on iPhone", "phone"), ios=True, android=True,
  statement="Sped-up, slowed + reverb and nightcore edits drive half the sounds on TikTok, and making one usually means a laptop, a DAW and an hour. VibeDeck Studio does it on your phone with the songs you already own: pick a section, tap an effect, export.",
  features_h2="What VibeDeck Studio does",
  features=[("Loop Slicer", "Tempo-aware loops of 1 beat, 1, 2, 4, 8 or 16 bars, with bar-by-bar nudging and millisecond timing on the waveform."),
            ("One-tap FX", "Original, Viral, Analog, Slowed + Reverb, Nightcore, Underwater and Dub Delay presets, plus Tweak FX for custom settings."),
            ("Export for social", "Save as 24-bit WAV, M4A (AAC) or MP4 video with the music visualizer, ready for TikTok, Instagram Reels and YouTube Shorts.")],
  extra=prose_section('<h2>How it will work</h2><ol><li>Open a track from your library in <strong>VibeDeck Studio</strong>.</li><li>Choose a loop length or keep the full track.</li><li>Tap a Quick FX preset such as <strong>Slowed + Reverb</strong> or <strong>Nightcore</strong>, or shape your own with Tweak FX, pitch and filter.</li><li>Press <strong>Play</strong> to preview, then <strong>Export</strong> to WAV, M4A or MP4.</li></ol><h2>Made for</h2><ul><li><strong>Creators</strong> making sped-up, slowed and nightcore sounds for TikTok and Reels.</li><li><strong>DJs</strong> preparing loops and edits on the go.</li><li><strong>Dancers</strong> cutting the exact section they rehearse.</li><li><strong>Producers</strong> sketching ideas from reference tracks.</li></ul><p>VibeDeck Studio arrives as a free update to VibeDeck Player. Install the app now to get it as soon as it ships. Use only music you own or have the rights to share.</p><p>Also see: <a href="/music-player-pitch-tempo/">pitch and tempo control</a>, <a href="/slow-down-song/">slow down a song without changing pitch</a>.</p>'),
  faq_h2="VibeDeck Studio FAQ",
  faq=[("What is VibeDeck Studio?", "VibeDeck Studio is the remix and clip section of VibeDeck Player: a loop slicer, one-tap effects like Slowed + Reverb and Nightcore, and export to WAV, M4A and MP4 video."),
       ("How do I make a slowed + reverb version of a song on my phone?", "Open the song in VibeDeck Studio and tap the Slowed + Reverb preset. Preview it, adjust with Tweak FX if you like, then export the result."),
       ("Can I make nightcore on iPhone?", "Yes. VibeDeck Studio has a one-tap Nightcore preset that speeds up and raises a track, and you can export it as audio or video."),
       ("Which export formats are supported?", "24-bit WAV without compression, M4A (AAC) and MP4 video with the VibeDeck music visualizer."),
       ("When is VibeDeck Studio available?", "It is coming in the next update of VibeDeck Player for iPhone. Install VibeDeck Player now and the update will add Studio automatically.")],
  related=["/music-player-pitch-tempo/", "/slow-down-song/", "/change-song-key-iphone/"],
  cta="Get VibeDeck Player now and Studio lands in your next update."))
PAGES.append(dict(path="/vibedeck-vs-vox/", crumb="VibeDeck Player vs VOX",
  title="VibeDeck Player vs VOX: Offline Player Comparison",
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
 ("support", "/support.html", "Support", "Support and Help | VibeDeck Player",
  "Get help with VibeDeck Player, the offline music player for MP3, FLAC, ALAC, AIFF, WAV, AAC and M4A: importing tracks, queue, EQ, pitch and tempo."),
 ("privacy", "/privacy.html", "Privacy", "Privacy Policy | VibeDeck Player",
  "How VibeDeck Player handles your audio files, optional cover-art lookup and privacy. No account, no ads, no tracking, no data sold."),
 ("terms", "/terms.html", "Terms", "Terms of Use | VibeDeck Player",
  "Terms of Use for VibeDeck Player, the offline music player for local MP3, FLAC, ALAC, AIFF, WAV, AAC and M4A files on iPhone, iPad and Android."),
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
    p = {"path": "/404.html", "title": "Page not found | VibeDeck Player", "desc": "This page does not exist. Go back to VibeDeck Player, the offline music player for FLAC, ALAC, AIFF, WAV, MP3, AAC and M4A.", "noindex": True, "ld": [WEBSITE]}
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
