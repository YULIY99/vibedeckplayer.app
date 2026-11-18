#!/usr/bin/env python3
"""Bring the 17 translated home pages to section parity with the English home.

Adds: pitch demo in the hero, Colour-from-cover, Queue, iPhone Duo, Cover, Android, Workflow and Guides sections,
replaces the 6-card features block with the 10-card one, and puts the sections in the English order.
Texts: _build/home_parity_{a,b,c}.py (66 strings per language, order = KEYS below).
Guides: built from the localized guide pages that exist (hreflang en -> group), links stay inside the language folder.
Run:  python3 _build/home_parity.py [lang ...]
"""
import re, sys, glob, html
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from home_parity_a import T as TA
from home_parity_b import T as TB
from home_parity_c import T as TC
T = {**TA, **TB, **TC}
ROOT = Path(__file__).resolve().parents[1]
LANGS = ['ja','es','pt-br','de','fr','it','ru','ko','tr','id','pl','nl','vi','zh-hant','zh-hans','th','uk']
N = 66
GROUPS = {
 'play': ['flac-player-iphone','flac-player-android','offline-music-player-iphone','offline-music-player-android','mp3-player-no-ads','audio-formats','best-offline-music-player','play-flac-on-iphone','wav-player-iphone','put-music-on-iphone-without-itunes','google-drive-music-player-android'],
 'key': ['music-player-pitch-tempo','change-song-key-iphone','slow-down-song','karaoke-key-change','bpm-detector','nightcore','slowed-reverb'],
 'tune': ['bass-booster','dj-filter','saturation','limiter','delay','dj-equalizer'],
 'dj': ['vocal-remover','sampler','dj-loop','dj-app'],
}
EN = open(ROOT / 'index.html', encoding='utf-8').read()

def sec(src, sid):
    return re.search(r'<section[^>]*\bid="%s".*?</section>' % sid, src, re.S).group(0)

def rep(s, a, b, count=1):
    assert a in s, a[:60]
    return s.replace(a, b)

def esc(t):
    return html.escape(t, quote=False)

def guides_html(lang, t):
    pages = {}
    for f in sorted(glob.glob(str(ROOT / lang / '*' / 'index.html'))):
        s = open(f, encoding='utf-8').read()
        m = re.search(r'<link rel="alternate" hreflang="en" href="https://vibedeckplayer.app/([^"]+?)/?"', s)
        h = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        if not m or not h: continue
        slug = m.group(1)
        sp = re.search(r'<span class="h1-(?:plain|big)">(.*?)</span>', h.group(1), re.S)
        title = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', (sp or h).group(1 if sp else 1))).strip().rstrip('.。')
        pages[slug] = (f'/{lang}/{Path(f).parent.name}/', title)
    cols = []
    for key, name in zip(('play','key','tune','dj'), t[62:66]):
        items = [pages[sl] for sl in GROUPS[key] if sl in pages]
        if items:
            cols.append('<div><h3>%s</h3><ul>%s</ul></div>' % (esc(name), ''.join('<li><a href="%s">%s</a></li>' % (u, ttl) for u, ttl in items)))
    base = sec(EN, 'guides')
    head = re.search(r'<style>.*?</style>', base, re.S).group(0)
    out = ('<section class="section" id="guides" aria-labelledby="guides-title">\n  <div class="wrap">\n    <div class="sec-head" data-reveal><div><h2 class="h2" id="guides-title">%s <span class="soft">%s</span></h2></div><p class="lede">%s</p></div>\n    %s<div class="guide-index">%s</div>\n  </div>\n</section>'
           % (esc(t[59]), esc(t[60]), esc(t[61]), head, ''.join(cols)))
    return out, sorted(pages), [len(c) for c in cols]

def build(lang, src):
    t = T[lang]
    assert len(t) == N, (lang, len(t))
    # --- queue
    q = sec(EN, 'queue')
    q = rep(q, 'Drag to reorder.<br><span class="soft">Change cover. Night mode.</span>', f'{esc(t[4])}<br><span class="soft">{esc(t[5])}</span>')
    q = rep(q, 'Rearrange tracks the way you like, change any cover and switch on night mode.', esc(t[6]))
    q = rep(q, 'VibeDeck queue on iPhone: drag to reorder, change cover, night mode', esc(t[4] + ' ' + t[5]))
    # --- colour
    c = sec(EN, 'colour')
    c = rep(c, 'The player takes its color from the cover.', esc(t[7]))
    c = rep(c, 'The matte panels and the glow change with every track. White theme coming soon.', esc(t[8]))
    c = rep(c, 'VibeDeck player with matte panels and glow in the colours of the album cover', esc(t[7]))
    c = rep(c, 'VibeDeck player on the same track with the panels tinted by the cover', esc(t[8]))
    # --- cover
    cv = sec(EN, 'cover')
    cv = rep(cv, 'Change any cover.<br><span class="soft">Search. Photos. Original.</span>', f'{esc(t[9])}<br><span class="soft">{esc(t[10])}</span>')
    cv = rep(cv, 'Search a cover for any track, pick one from Photos or keep the original.', esc(t[11]))
    cv = rep(cv, 'VibeDeck on iPhone: change any cover, search, Photos or original', esc(t[9] + ' ' + t[10]))
    # --- duo
    d = sec(EN, 'duo')
    d = rep(d, 'iPhone Duo.<br><span class="soft">Update next week.</span>', f'{esc(t[12])}<br><span class="soft">{esc(t[13])}</span>')
    d = rep(d, 'The player and the queue side by side on the big screen. Coming in the next update.', esc(t[14]))
    d = rep(d, 'VibeDeck on iPhone Duo: the player and the queue side by side', esc(t[12] + ' ' + t[14]))
    # --- android
    a = sec(EN, 'android')
    name = t[15].rstrip('.。')
    a = rep(a, 'VibeDeck for Android.', esc(t[15]))
    a = rep(a, 'An offline music player for your own files, with pitch, waveform, tone and sound controls on one screen.', esc(t[16]))
    a = re.sub(r'\s*<p class="mono" style="margin-top:24px"><a class="link" href="/offline-music-player-android/">.*?</a></p>', '', a, flags=re.S)
    badge = re.search(r'<a class="store-badge" href="https://play\.google\.com[^>]*>.*?</a>', src, re.S).group(0)
    a = re.sub(r'<a class="store-badge" href="https://play\.google\.com[^>]*>.*?</a>', lambda m: badge.replace('utm_campaign=%s-home' % lang, 'utm_campaign=%s-home' % lang), a, count=1, flags=re.S)
    eyebrows = [t[29 + 3 * i] for i in range(10)]
    alts = [m for m in re.finditer(r'alt="(VibeDeck for Android[^"]*)"', a)]
    assert len(alts) == 10, len(alts)
    it = iter(eyebrows)
    a = re.sub(r'alt="VibeDeck for Android[^"]*"', lambda m: 'alt="%s"' % esc(name + ': ' + next(it)), a)
    a = rep(a, 'aria-label="VibeDeck for Android screenshots"', 'aria-label="%s"' % esc(name))
    # --- workflow
    w = sec(EN, 'workflow')
    w = rep(w, 'Player first. <span class="soft">Controls close.</span>', f'{esc(t[17])} <span class="soft">{esc(t[18])}</span>')
    w = rep(w, 'VibeDeck keeps the current track readable while the queue and EQ stay one move away. This offline music player for your local files is easy to read in the dark, with sound controls close.', esc(t[19]))
    for k, (h, p) in enumerate((('Playback', "Full transport controls, waveform with scrubbing, BPM readout, and pitch/filter on the main screen. Same track. New feeling."),
                                ('Queue', "See what's playing, search your library, and line up what's next without leaving the player. Night Mode strips the artwork and leaves only the list."),
                                ('Sound', "EQ + Gain, bass boost, filter, VibeMod audio-reactive processing, stereo balance, and real-time pitch shifting up to ±8 st. Built-in limiter: clean, punchy sound on any headphones."))):
        w = rep(w, f'<h3>{h}</h3><p>{p}</p>', f'<h3>{esc(t[20 + 2 * k])}</h3><p>{esc(t[21 + 2 * k])}</p>')
    # --- features (10 cards)
    f = sec(EN, 'features')
    f = rep(f, 'Pitch, EQ, AURA, TONE. <span class="soft">One dark screen.</span>', f'{esc(t[26])} <span class="soft">{esc(t[27])}</span>')
    f = re.sub(r'(<p class="lede">)PRO sound tools live.*?(</p>)', lambda m: m.group(1) + esc(t[28]) + m.group(2), f, count=1, flags=re.S)
    cards = re.findall(r'<li><span class="k mono">(.*?)</span><div><h3>(.*?)</h3><p>(.*?)</p></div></li>', f, re.S)
    assert len(cards) == 10, len(cards)
    for k, (e, h, p) in enumerate(cards):
        f = rep(f, f'<span class="k mono">{e}</span><div><h3>{h}</h3><p>{p}</p></div>', f'<span class="k mono">{esc(t[29 + 3 * k])}</span><div><h3>{esc(t[30 + 3 * k])}</h3><p>{esc(t[31 + 3 * k])}</p></div>')
    f = f.replace('id="features-title"', 'id="more-title"').replace('aria-labelledby="features-title"', 'aria-labelledby="more-title"')
    g, gp, gl = guides_html(lang, t)
    # hero pitch demo
    demo = re.search(r'<div class="slider" data-pitch-demo.*?</div></div>\s*(?=\n)', sec_hero(EN), re.S)
    return dict(queue=q, colour=c, cover=cv, duo=d, android=a, workflow=w, features=f, guides=g), (gp, gl)

def sec_hero(src):
    return re.search(r'<section class="hero".*?</section>', src, re.S).group(0)

def demo_html(t):
    m = re.search(r'<div class="slider" data-pitch-demo.*?</output></div></div>', sec_hero(EN), re.S).group(0)
    m = rep(m, '<b>Pitch</b> / PRO demo', f'<b>{esc(t[0])}</b> / {esc(t[1])}')
    m = rep(m, '>RESET<', f'>{esc(t[2])}<')
    m = rep(m, 'aria-label="Pitch in semitones"', f'aria-label="{esc(t[3])}"')
    return m

def classify(part, seen_premium):
    head = re.match(r'<section[^>]*>', part).group(0)
    if 'class="hero' in head: return 'hero'
    if 'statement statement--small' in head: return 'statement'
    m = re.search(r'\bid="([^"]+)"', head)
    if m: return m.group(1)
    if 'aria-labelledby="features-title"' in head: return 'what'
    if 'aria-labelledby="specs-title"' in head: return 'specs'
    return 'glance' if seen_premium else 'howto'

ORDER = ['hero','statement','studio','sampler','stems','effects','colour','dj-eq','queue','duo','cover','android','specs','workflow','features','what','guides','why','howto','premium','glance','faq','related','download','share']

def process(lang):
    p = ROOT / lang / 'index.html'
    src = p.read_text(encoding='utf-8')
    if 'id="queue"' in src:
        print(lang, 'already done'); return
    parts = re.split(r'(?=<section\b)', src)
    pre, parts = parts[0], parts[1:]
    new, info = build(lang, src)
    named = {}
    seen = False
    for part in parts:
        k = classify(part, seen)
        if k == 'premium': seen = True
        named[k] = part
    assert 'share' in named and set(named) - set(ORDER) == set(), (lang, sorted(set(named) - set(ORDER)))
    named.update({k: v + '\n' for k, v in new.items() if k != 'features'})
    named['features'] = new['features'] + '\n'
    # hero demo after the dim note
    t = T[lang]
    h = named['hero']
    note = re.search(r'<p class="dim" style="margin-top:16px">.*?</p>', h, re.S)
    assert note, lang
    h = h[:note.end()] + '\n' + demo_html(t) + h[note.end():]
    named['hero'] = h
    # last section keeps the footer: it must stay last
    out = pre + ''.join(named[k] if named[k].endswith('\n') else named[k] for k in ORDER if k in named)
    p.write_text(out, encoding='utf-8')
    print(lang, 'ok; guide pages:', len(info[0]), 'cols', info[1])

if __name__ == '__main__':
    for l in (sys.argv[1:] or LANGS):
        process(l)
