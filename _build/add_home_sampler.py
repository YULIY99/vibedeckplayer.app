#!/usr/bin/env python3
"""Add the Sampler block to the 17 home pages, right before the Studio section.

    python3 _build/add_home_sampler.py

Texts: _build/home_sampler_i18n.json. Reuses the Studio block styles (studio-feature), so the
design stays the same. Re-running replaces the block.
"""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = '/assets/img/vibedeck-sampler-iphone'
SIZES = '(min-width: 1024px) 344px, 72vw'


def block(c):
    e = html.escape
    srcset = lambda ext: ', '.join(f'{IMG}-{w}.{ext} {w}w' for w in (400, 600, 800))
    points = ''.join(f'<li><span class="studio-index mono">{i:02d}</span><span><strong>{e(t)}</strong><small>{e(s)}</small></span></li>'
                     for i, (t, s) in enumerate(c['points'], 1))
    return ('<section class="section studio-feature" id="sampler" aria-labelledby="sampler-title">\n'
            '  <div class="wrap studio-feature-grid">\n'
            '    <div class="studio-art" data-reveal>\n'
            '      <div class="studio-glow" aria-hidden="true"></div>\n'
            f'      <figure class="phone phone--lg"><picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{SIZES}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{SIZES}">'
            f'<img src="{IMG}-600.webp" alt="{e(c["alt"])}" width="600" height="1300" loading="lazy" decoding="async"></picture></figure>\n'
            '    </div>\n'
            '    <div class="studio-copy" data-reveal>\n'
            f'      <p class="tag eyebrow">{e(c["new"])} <span class="dim">/ VibeDeck Sampler</span></p>\n'
            f'      <h2 class="h2" id="sampler-title">{e(c["h2"])}<br><span class="soft">{e(c["soft"])}</span></h2>\n'
            f'      <p class="lede">{e(c["lede"])}</p>\n'
            f'      <ul class="studio-points" aria-label="VibeDeck Sampler">{points}</ul>\n'
            f'      <a class="studio-link mono" href="{c["page"]}">{e(c["link"])} <span aria-hidden="true">↗</span></a>\n'
            '    </div>\n'
            '  </div>\n'
            '</section>\n')


def main():
    data = {k: v for k, v in json.loads((ROOT / '_build/home_sampler_i18n.json').read_text(encoding='utf-8')).items() if not k.startswith('_')}
    for code, c in data.items():
        p = ROOT / ('index.html' if c['home'] == '/' else c['home'].strip('/') + '/index.html')
        s = p.read_text(encoding='utf-8')
        s = re.sub(r'<section class="section studio-feature" id="sampler".*?</section>\n', '', s, flags=re.S)
        m = re.search(r'<section class="section[^"]*" id="studio"', s)
        s = s[:m.start()] + block(c) + s[m.start():]
        p.write_text(s, encoding='utf-8')
    print('sampler block on', len(data), 'home pages')


if __name__ == '__main__':
    main()
