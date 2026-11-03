#!/usr/bin/env python3
"""Put the real app screen in the hero of every page of a feature (English + 16 languages).

    python3 _build/set_sampler_hero.py [sampler|stems|eq]   (default: sampler)

The guide builders copy the hero image of their template page, so re-run this after
add_guides.py sampler or add_local_guides.py sampler. Idempotent.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES = {'sampler': ('/assets/img/vibedeck-sampler-iphone', '/sampler/', 'sampler.json'),
            'stems': ('/assets/img/vibedeck-stems-iphone', '/vocal-remover/', 'stems.json'),
            'eq': ('/assets/img/vibedeck-eq-8band-iphone', '/dj-equalizer/', 'eq.json')}
IMG = ''
SIZES = '(min-width: 1024px) 326px, 66vw'


def picture(alt):
    srcset = lambda ext: ', '.join(f'{IMG}-{w}.{ext} {w}w' for w in (400, 600, 800))
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{SIZES}"/>'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{SIZES}"/>'
            f'<img src="{IMG}-600.webp" alt="{alt}" width="600" height="1300" fetchpriority="high" decoding="async"/></picture>')


def main():
    global IMG
    IMG, en, data = FEATURES[sys.argv[1] if len(sys.argv) > 1 else 'sampler']
    src = ROOT / '_build/guides_i18n' / data
    slugs = [en] + ([c['slug'] for k, c in json.loads(src.read_text(encoding='utf-8')).items() if not k.startswith('_')] if src.exists() else [])
    for slug in slugs:
        p = ROOT / slug.strip('/') / 'index.html'
        s = p.read_text(encoding='utf-8')
        i = s.index('class="hero-visual"'); j = s.index('<picture', i); k = s.index('</picture>', j) + len('</picture>')
        alt = re.search(r'alt="([^"]*)"', s[j:k]).group(1)
        s = s[:j] + picture(alt) + s[k:]
        preload = (f'<link rel="preload" as="image" type="image/avif" imagesrcset="{", ".join(f"{IMG}-{w}.avif {w}w" for w in (400, 600, 800))}" '
                   f'imagesizes="{SIZES}" fetchpriority="high"/>')
        s = re.sub(r'<link rel="preload" as="image"[^>]*>', preload, s, count=1)
        p.write_text(s, encoding='utf-8')
    print('hero set on', len(slugs), 'pages')


if __name__ == '__main__':
    main()
