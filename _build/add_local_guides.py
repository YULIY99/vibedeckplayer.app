#!/usr/bin/env python3
"""Translate an English guide into other languages, using each language's own guide page as layout.

    python3 _build/add_local_guides.py slow-down

Content: _build/guides_i18n/<guide>.json, one entry per language. Each page keeps
the localized header, footer, related cards and store links of its template and
gets new text, JSON-LD (WebPage, Article, BreadcrumbList, FAQPage) and a full
hreflang cluster. The English page and existing equivalents (EXISTING) get the
new hreflang links and footer language links; sitemap alternates are rebuilt.
Requires beautifulsoup4.
"""
from pathlib import Path
import copy, datetime, html, json, re, sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://vibedeckplayer.app'
TODAY = datetime.date.today().isoformat()
ORDER = ['en', 'ja', 'es', 'pt-BR', 'de', 'fr', 'it', 'ru', 'ko', 'tr', 'id', 'pl', 'nl', 'vi', 'zh-Hant']
NAMES = {'en': 'English', 'ja': '日本語', 'es': 'Español', 'pt-BR': 'Português', 'de': 'Deutsch', 'fr': 'Français',
         'it': 'Italiano', 'ru': 'Русский', 'ko': '한국어', 'tr': 'Türkçe', 'id': 'Bahasa Indonesia', 'pl': 'Polski',
         'nl': 'Nederlands', 'vi': 'Tiếng Việt', 'zh-Hant': '繁體中文'}
# Layout template per language: a guide page with hero, features, prose, FAQ, related and download sections
TEMPLATES = {'ja': '/ja/tempo-henkou/', 'de': '/de/tonart-aendern/', 'fr': '/fr/changer-tonalite/', 'it': '/it/cambiare-tonalita/',
             'es': '/es/reproductor-flac/', 'pt-BR': '/pt-br/player-flac-android/', 'ru': '/ru/smenit-tonalnost/',
             'ko': '/ko/key-byeongyeong/', 'tr': '/tr/sarki-tonu-degistirme/', 'id': '/id/ubah-nada-lagu/',
             'pl': '/pl/zmiana-tonacji/', 'nl': '/nl/toonsoort-veranderen/', 'vi': '/vi/doi-tone-bai-hat/',
             'zh-Hant': '/zh-hant/sheng-jiang-diao/'}
KEY_PAGES = {'ja': '/ja/key-henkou-app/', 'de': '/de/tonart-aendern/', 'fr': '/fr/changer-tonalite/', 'it': '/it/cambiare-tonalita/',
             'es': '/change-song-key-iphone/', 'pt-BR': '/change-song-key-iphone/', 'ru': '/ru/smenit-tonalnost/',
             'ko': '/ko/key-byeongyeong/', 'tr': '/tr/sarki-tonu-degistirme/', 'id': '/id/ubah-nada-lagu/',
             'pl': '/pl/zmiana-tonacji/', 'nl': '/nl/toonsoort-veranderen/', 'vi': '/vi/doi-tone-bai-hat/',
             'zh-Hant': '/zh-hant/sheng-jiang-diao/'}
GUIDES = {'slow-down': {'en': '/slow-down-song/', 'existing': {'ja': '/ja/tempo-henkou/'}, 'campaign': 'slow-down'},
          'sampler': {'en': '/sampler/', 'existing': {}, 'campaign': 'sampler'}}


class Ordered(HTMLFormatter):
    def attributes(self, tag): return tag.attrs.items()


def path(url): return ROOT / (url.strip('/') + '/index.html')


def frag(markup): return BeautifulSoup(markup, 'html.parser')


def check(code, c):
    errors = []
    if len(c['title']) > 60: errors.append(f"title {len(c['title'])}")
    if len(c['desc']) > 160: errors.append(f"desc {len(c['desc'])}")
    if '—' in json.dumps(c, ensure_ascii=False): errors.append('em dash')
    if errors: sys.exit(f'{code}: {errors}')


def build(code, c, cluster, campaign):
    url = SITE + c['slug']
    soup = BeautifulSoup(path(TEMPLATES[code]).read_text(), 'html.parser')
    soup.title.string = c['title']
    for sel, val in [('meta[name="description"]', c['desc']), ('meta[property="og:description"]', c['desc']),
                     ('meta[name="twitter:description"]', c['desc']), ('meta[property="og:title"]', c['title']),
                     ('meta[name="twitter:title"]', c['title']), ('meta[property="og:url"]', url)]:
        tag = soup.select_one(sel)
        if tag: tag['content'] = val
    soup.select_one('link[rel="canonical"]')['href'] = url
    main = soup.find('main')
    main.select_one('.crumbs li[aria-current]').string = c['crumb']
    eyebrow = main.select_one('.hero .eyebrow'); eyebrow.clear()
    eyebrow.append(c['eyebrow'][0] + ' '); dim = soup.new_tag('span', attrs={'class': 'dim'}); dim.string = '/ ' + c['eyebrow'][1]; eyebrow.append(dim)
    main.select_one('#hero-title .h1-plain').string = c['h1']
    main.select_one('#hero-title .h1-sub').string = c['h1sub']
    main.select_one('.hero .lede').string = c['lede']
    for note in main.select('.hero .hero-copy > p'):  # template's 'app is in English' note names its own control
        if not set(note.get('class') or []) & {'lede', 'eyebrow', 'tag'}: note.string = c['note']
    main.select_one('.hero-visual img')['alt'] = c['alt']
    main.select_one('.statement p').string = c['statement']
    main.select_one('#features-title').string = c['features_title']
    for li, (h3, p) in zip(main.select('.panels > li'), c['features']):
        li.h3.string = h3; li.p.string = p
    box = main.select_one('.box.prose'); box.clear()
    box.append(frag(c['prose'].replace('{key}', KEY_PAGES[code])))
    main.select_one('#faq-title').string = c['faq_title']
    main.select_one('#faq .eyebrow .dim').string = f"/ {len(c['faq']):02d}"
    faq = main.select_one('#faq .faq'); faq.clear()
    for q, a in c['faq']:
        faq.append(frag(f'<details><summary><h3>{html.escape(q)}</h3></summary><div class="a"><p>{html.escape(a)}</p></div></details>'))
    main.select_one('#download .lede').string = c['cta']
    for a in soup.select('a[href*="apps.apple.com"], a[href*="play.google.com"]'):
        a['href'] = re.sub(r'ct=[^&]+', 'ct=' + campaign, a['href'])
        a['href'] = re.sub(r'campaign%3D[^&%]+', 'campaign%3D' + campaign, a['href'])
    # Language links: every nav with hreflang anchors points to this guide's cluster
    for nav in soup.find_all('nav'):
        # Language links carry lang == hreflang; support/privacy links only carry hreflang="en"
        anchors = [a for a in nav.find_all('a', attrs={'hreflang': True}) if a.get('lang') == a['hreflang']]
        if not anchors: continue
        for a in anchors:
            if a['hreflang'] in cluster: a['href'] = cluster[a['hreflang']]
        if nav.find('ul'):
            have = {a['hreflang'] for a in anchors}
            for lang in ORDER:
                if lang in cluster and lang not in have:
                    li = soup.new_tag('li'); a = soup.new_tag('a', href=cluster[lang], hreflang=lang, lang=lang); a.string = NAMES[lang]
                    if lang == code: a['aria-current'] = 'page'
                    li.append(a); nav.ul.append(li)
    head = soup.head
    for link in head.select('link[rel="alternate"][hreflang]'): link.decompose()
    canonical = head.select_one('link[rel="canonical"]')
    for lang in reversed(ORDER + ['x-default']):
        if lang == 'x-default' or lang in cluster:
            canonical.insert_after(soup.new_tag('link', rel='alternate', hreflang=lang, href=SITE + cluster['en' if lang == 'x-default' else lang]))
    script = soup.select_one('script[type="application/ld+json"]')
    graph = json.loads(script.string)
    image = soup.select_one('meta[property="og:image"]')['content']
    nodes = [n for n in graph['@graph'] if n['@type'] in ('Organization', 'WebSite', 'MobileApplication')]
    crumbs = [n for n in graph['@graph'] if n['@type'] == 'BreadcrumbList'][0]
    crumbs['itemListElement'][-1].update(name=c['crumb'], item=url)
    dates = {'datePublished': TODAY, 'dateModified': TODAY}
    graph['@graph'] = [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': c['title'], 'description': c['desc'], 'inLanguage': code,
         'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#app'}, 'publisher': {'@id': SITE + '/#org'}, **dates},
        {'@type': 'Article', '@id': url + '#article', 'headline': c['h1'], 'description': c['desc'], 'inLanguage': code, 'image': image,
         'author': {'@id': SITE + '/#org'}, 'publisher': {'@id': SITE + '/#org'}, 'mainEntityOfPage': {'@id': url + '#webpage'},
         'about': {'@id': SITE + '/#app'}, **dates},
        *nodes, crumbs,
        {'@type': 'FAQPage', 'inLanguage': code, 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]},
    ]
    script.string = '\n' + json.dumps(graph, ensure_ascii=False, indent=1) + '\n'
    out = path(c['slug']); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(soup.decode(formatter=Ordered()) + '\n')


def link_existing(rel_url, cluster):
    """Add missing hreflang links and footer language links to a hand-edited page, as text."""
    p = path(rel_url); s = p.read_text()
    head, body = s.split('</head>', 1)
    have = set(re.findall(r'<link rel="alternate" hreflang="([^"]+)"', head))
    add = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{cluster[l]}">\n' for l in ORDER if l in cluster and l not in have)
    if 'x-default' in have:
        head = head.replace('<link rel="alternate" hreflang="x-default"', add + '<link rel="alternate" hreflang="x-default"', 1)
    else:  # page had no hreflang cluster yet: add it, with x-default, right after the canonical link
        add += f'<link rel="alternate" hreflang="x-default" href="{SITE}{cluster["en"]}">\n'
        head = re.sub(r'(<link rel="canonical"[^>]*>\n?)', lambda m: m.group(1) + ('' if m.group(1).endswith('\n') else '\n') + add, head, count=1)
    if '<footer' in body:
        i = body.index('<footer'); before, foot = body[:i], body[i:]
        def nav(m):
            text = m.group(0)
            if not re.search(r'hreflang="([^"]+)" lang="\1"', text): return text
            for l in ORDER:
                if l in cluster and f'hreflang="{l}"' not in text and cluster[l] != rel_url:
                    a = f'<a href="{cluster[l]}" hreflang="{l}" lang="{l}">{NAMES[l]}</a>'
                    text = text.replace('</ul>', f'<li>{a}</li></ul>') if '</ul>' in text else text.replace('</nav>', ' · ' + a + '</nav>')
            return text
        body = before + re.sub(r'<nav\b.*?</nav>', nav, foot, flags=re.S)
    p.write_text(head + '</head>' + body)


def sitemap(cluster):
    NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'; X = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('', NS); ET.register_namespace('xhtml', X)
    sm = ROOT / 'sitemap.xml'; tree = ET.parse(sm); root = tree.getroot()
    by_url = {e.find('{' + NS + '}loc').text: e for e in root}
    for lang in ORDER:
        if lang not in cluster: continue
        url = SITE + cluster[lang]
        el = by_url.get(url)
        if el is None:
            el = ET.SubElement(root, '{' + NS + '}url'); ET.SubElement(el, '{' + NS + '}loc').text = url
            ET.SubElement(el, '{' + NS + '}lastmod').text = TODAY; ET.SubElement(el, '{' + NS + '}priority').text = '0.8'
        for old in el.findall('{' + X + '}link'): el.remove(old)
        loc = el.find('{' + NS + '}loc')
        links = [ET.Element('{' + X + '}link', {'rel': 'alternate', 'hreflang': l, 'href': SITE + cluster[l]}) for l in ORDER if l in cluster]
        links.append(ET.Element('{' + X + '}link', {'rel': 'alternate', 'hreflang': 'x-default', 'href': SITE + cluster['en']}))
        for i, link in enumerate(links): el.insert(list(el).index(loc) + 1 + i, link)
    ET.indent(tree, space='  ')
    sm.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n')


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    g = GUIDES[name]
    content = {k: v for k, v in json.loads((ROOT / '_build/guides_i18n' / f'{name}.json').read_text()).items() if not k.startswith('_')}
    for code, c in content.items(): check(code, c)
    cluster = {'en': g['en'], **g['existing'], **{code: c['slug'] for code, c in content.items()}}
    for code, c in content.items(): build(code, c, cluster, f"{code.lower()}-{g['campaign']}")
    for rel_url in [g['en'], *g['existing'].values()]: link_existing(rel_url, cluster)
    sitemap(cluster)
    print(f'{name}: {len(content)} pages, cluster of {len(cluster)} languages')


if __name__ == '__main__':
    main()
