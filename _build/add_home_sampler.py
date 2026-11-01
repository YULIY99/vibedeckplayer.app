#!/usr/bin/env python3
"""Add a feature block to the 17 home pages: Sampler before the Studio section, Stems before the Sampler.

    python3 _build/add_home_sampler.py [sampler|stems]   (default: sampler)

Texts: _build/home_<feature>_i18n.json. Reuses the Studio block styles (studio-feature), so the
design stays the same. Re-running replaces the block.
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# feature: (image, section id, label, json, the section it goes before)
FEATURES = {'sampler': ('/assets/img/vibedeck-sampler-iphone', 'sampler', 'VibeDeck Sampler', 'home_sampler_i18n.json', 'studio'),
            'stems': ('/assets/img/vibedeck-stems-iphone', 'stems', 'VibeDeck Stems', 'home_stems_i18n.json', 'sampler')}
IMG, SID, LABEL, DATA, BEFORE = FEATURES['sampler']
SIZES = '(min-width: 1024px) 344px, 72vw'


def block(c):
    e = html.escape
    srcset = lambda ext: ', '.join(f'{IMG}-{w}.{ext} {w}w' for w in (400, 600, 800))
    points = ''.join(f'<li><span class="studio-index mono">{i:02d}</span><span><strong>{e(t)}</strong><small>{e(s)}</small></span></li>'
                     for i, (t, s) in enumerate(c['points'], 1))
    return (f'<section class="section studio-feature" id="{SID}" aria-labelledby="{SID}-title">\n'
            '  <div class="wrap studio-feature-grid">\n'
            '    <div class="studio-art" data-reveal>\n'
            '      <div class="studio-glow" aria-hidden="true"></div>\n'
            f'      <figure class="phone phone--lg"><picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{SIZES}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{SIZES}">'
            f'<img src="{IMG}-600.webp" alt="{e(c["alt"])}" width="600" height="1300" loading="lazy" decoding="async"></picture></figure>\n'
            '    </div>\n'
            '    <div class="studio-copy" data-reveal>\n'
            f'      <p class="tag eyebrow">{e(c["new"])} <span class="dim">/ {LABEL}</span></p>\n'
            f'      <h2 class="h2" id="{SID}-title">{e(c["h2"])}<br><span class="soft">{e(c["soft"])}</span></h2>\n'
            f'      <p class="lede">{e(c["lede"])}</p>\n'
            f'      <ul class="studio-points" aria-label="{LABEL}">{points}</ul>\n'
            f'      <a class="studio-link mono" href="{c["page"]}">{e(c["link"])} <span aria-hidden="true">↗</span></a>\n'
            '    </div>\n'
            '  </div>\n'
            '</section>\n')


def main():
    global IMG, SID, LABEL, DATA, BEFORE
    IMG, SID, LABEL, DATA, BEFORE = FEATURES[sys.argv[1] if len(sys.argv) > 1 else 'sampler']
    data = {k: v for k, v in json.loads((ROOT / '_build' / DATA).read_text(encoding='utf-8')).items() if not k.startswith('_')}
    for code, c in data.items():
        p = ROOT / ('index.html' if c['home'] == '/' else c['home'].strip('/') + '/index.html')
        s = p.read_text(encoding='utf-8')
        s = re.sub(rf'<section class="section studio-feature" id="{SID}".*?</section>\n', '', s, flags=re.S)
        m = re.search(rf'<section class="section[^"]*" id="{BEFORE}"', s)
        s = s[:m.start()] + block(c) + s[m.start():]
        p.write_text(s, encoding='utf-8')
    print(SID, 'block on', len(data), 'home pages')


if __name__ == '__main__':
    main()
