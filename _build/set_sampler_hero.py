#!/usr/bin/env python3
"""Put the real Sampler screen in the hero of every Sampler page (English + 16 languages).

The guide builders copy the hero image of their template page, so re-run this after
add_guides.py sampler or add_local_guides.py sampler. Idempotent.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = '/assets/img/vibedeck-sampler-iphone'
SIZES = '(min-width: 1024px) 326px, 66vw'


def picture(alt):
    srcset = lambda ext: ', '.join(f'{IMG}-{w}.{ext} {w}w' for w in (400, 600, 800))
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{SIZES}"/>'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{SIZES}"/>'
            f'<img src="{IMG}-600.webp" alt="{alt}" width="600" height="1300" fetchpriority="high" decoding="async"/></picture>')


def main():
    slugs = ['/sampler/'] + [c['slug'] for k, c in json.loads((ROOT / '_build/guides_i18n/sampler.json').read_text(encoding='utf-8')).items() if not k.startswith('_')]
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
