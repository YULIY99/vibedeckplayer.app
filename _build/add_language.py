#!/usr/bin/env python3
"""Add a language from the French page set, the same way add_italian.py built /it/.

    python3 _build/add_language.py --dump        # print numbered French source strings
    python3 _build/add_language.py ru ko tr      # generate pages, hreflang, footer links, sitemap

Translations live in _build/translations/<code>.json as {index: text}. Indices are
guarded by _build/translations/source.sha256: if the French text changes, the run
stops so the translations can be reviewed. Untranslated indices keep the French
text only when listed in "same" (brand names, units); anything else is an error.
Requires beautifulsoup4.
"""
from pathlib import Path
import copy, datetime, hashlib, json, re, sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, NavigableString, Doctype
from bs4.formatter import HTMLFormatter

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://vibedeckplayer.app'
TODAY = datetime.date.today().isoformat()
SOURCE = ['/fr/', '/fr/changer-tonalite/', '/fr/lecteur-flac/', '/fr/lecteur-mp3-sans-pub/']
LANGS = {
    'ru': dict(name='Русский', locale='ru_RU', routes=['/ru/', '/ru/smenit-tonalnost/', '/ru/flac-pleer/', '/ru/mp3-pleer-bez-reklamy/'],
               plans=['Ежемесячно', 'Ежегодно', 'Навсегда'],
               app_store='В App Store (iOS): $2.99 в месяц, $19.99 в год или $49.99 навсегда (USD).'),
    'ko': dict(name='한국어', locale='ko_KR', routes=['/ko/', '/ko/key-byeongyeong/', '/ko/flac-player/', '/ko/mp3-player/'],
               plans=['월간', '연간', '평생'],
               app_store='App Store(iOS): 월 $2.99, 연 $19.99, 평생 $49.99 (USD).'),
    'tr': dict(name='Türkçe', locale='tr_TR', routes=['/tr/', '/tr/sarki-tonu-degistirme/', '/tr/flac-calar/', '/tr/reklamsiz-mp3-calar/'],
               plans=['Aylık', 'Yıllık', 'Ömür boyu'],
               app_store='App Store’da (iOS): aylık $2.99, yıllık $19.99 veya ömür boyu $49.99 (USD).'),
    'id': dict(name='Bahasa Indonesia', locale='id_ID', routes=['/id/', '/id/ubah-nada-lagu/', '/id/pemutar-flac/', '/id/pemutar-mp3-tanpa-iklan/'],
               plans=['Bulanan', 'Tahunan', 'Seumur hidup'],
               app_store='Di App Store (iOS): $2.99 per bulan, $19.99 per tahun, atau $49.99 seumur hidup (USD).'),
    'pl': dict(name='Polski', locale='pl_PL', routes=['/pl/', '/pl/zmiana-tonacji/', '/pl/odtwarzacz-flac/', '/pl/odtwarzacz-mp3-bez-reklam/'],
               plans=['Miesięcznie', 'Rocznie', 'Dożywotnio'],
               app_store='W App Store (iOS): $2.99 miesięcznie, $19.99 rocznie lub $49.99 dożywotnio (USD).'),
    'nl': dict(name='Nederlands', locale='nl_NL', routes=['/nl/', '/nl/toonsoort-veranderen/', '/nl/flac-speler/', '/nl/mp3-speler-zonder-advertenties/'],
               plans=['Maandelijks', 'Jaarlijks', 'Levenslang'],
               app_store='In de App Store (iOS): $2.99 per maand, $19.99 per jaar of $49.99 levenslang (USD).'),
    'vi': dict(name='Tiếng Việt', locale='vi_VN', routes=['/vi/', '/vi/doi-tone-bai-hat/', '/vi/trinh-phat-flac/', '/vi/trinh-phat-mp3-khong-quang-cao/'],
               plans=['Hàng tháng', 'Hàng năm', 'Trọn đời'],
               app_store='Trên App Store (iOS): $2.99 mỗi tháng, $19.99 mỗi năm hoặc $49.99 trọn đời (USD).'),
    'zh-Hant': dict(name='繁體中文', locale='zh_TW', routes=['/zh-hant/', '/zh-hant/sheng-jiang-diao/', '/zh-hant/flac-player/', '/zh-hant/mp3-player/'],
               plans=['每月', '每年', '終身'],
               app_store='App Store（iOS）：每月 $2.99、每年 $19.99 或終身 $49.99（USD）。'),
}
TDIR = ROOT / '_build' / 'translations'


def path(url): return ROOT / (url.strip('/') + '/index.html')


def source_soups():
    result = []
    for url in SOURCE:
        soup = BeautifulSoup(path(url).read_text(), 'html.parser')
        for code in LANGS:  # strip links to the languages this script adds, so the source text is stable
            for tag in soup.select(f'[hreflang="{code}"], a[lang="{code}"]'):
                if tag.name == 'link' and tag.next_sibling == '\n': tag.next_sibling.extract()
                if tag.parent and tag.parent.name == 'li': tag.parent.decompose()
                else: tag.decompose()
        result.append((url, soup))
    return result


def text_items(soups):
    items = []
    def add(text):
        if text and text not in items: items.append(text)
    for _, soup in soups:
        for node in soup.find_all(string=True):
            if node.parent.name not in ['script', 'style'] and not isinstance(node, Doctype): add(node.strip())
        for tag in soup.find_all():
            for key in ['alt', 'aria-label']: add(tag.get(key))
        for tag in soup.find_all('meta'):
            if tag.get('name') in ['description', 'twitter:title', 'twitter:description'] or tag.get('property') in ['og:title', 'og:description', 'og:image:alt']:
                add(tag.get('content'))
    return items


class Ordered(HTMLFormatter):
    def attributes(self, tag): return tag.attrs.items()


def build(code, soups, items):
    cfg = LANGS[code]
    routes = dict(zip(SOURCE, cfg['routes']))
    data = json.loads((TDIR / f'{code}.json').read_text())
    same = set(data.get('same', []))
    T = {}
    for i, text in enumerate(items):
        if str(i) in data['t']: T[text] = data['t'][str(i)]
        elif str(i) not in same: sys.exit(f'{code}: index {i} not translated: {text[:80]!r}')
    dashes = [i for i, t in data['t'].items() if '—' in t]
    if dashes: sys.exit(f'{code}: em dash in translations {dashes}')

    def moved(text):
        for old, new in sorted(routes.items(), key=lambda p: -len(p[0])): text = text.replace(old, new)
        return text

    clusters = {}
    for old, source in soups:
        soup = copy.deepcopy(source); new = routes[old]
        clusters[soup.select_one('link[rel="alternate"][hreflang="en"]')['href'].replace(SITE, '')] = new
        for node in list(soup.find_all(string=True)):
            if node.parent.name in ['script', 'style'] or isinstance(node, Doctype): continue
            key = node.strip()
            if key in T:
                raw = str(node); lead = raw[:len(raw) - len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
                node.replace_with(NavigableString(lead + T[key] + trail))
        for tag in soup.find_all():
            for key in ['alt', 'aria-label', 'content']:
                if tag.get(key) in T: tag[key] = T[tag[key]]
            for key in ['href', 'src']:
                if key not in tag.attrs: continue
                if tag.name == 'link' and tag.get('rel') == ['alternate']: continue
                if tag.name == 'a' and tag.get('hreflang'): continue
                tag[key] = moved(tag[key])
            if tag.name == 'img':
                tag['src'] = tag['src'].replace('/badges/app-store-fr.svg', '/badges/app-store-en.svg').replace('/badges/google-play-fr.svg', '/badges/google-play-en.svg')
                if '/badges/app-store-en.svg' in tag['src']: tag['width'] = '144'
            if tag.name == 'a' and 'href' in tag.attrs and ('apps.apple.com' in tag['href'] or 'play.google.com' in tag['href']):
                tag['href'] = tag['href'].replace('hl=fr', 'hl=' + code).replace('ct=fr-', f'ct={code}-').replace('campaign%3Dfr-', f'campaign%3D{code}-')
        soup.html['lang'] = code
        if code == 'tr':  # Turkish uppercase turns i into İ: keep untranslated brand labels (iPhone, iOS, Android) English
            for node in soup.find_all(string=True):
                parent = node.parent
                if (node.strip() in items and node.strip() not in T and 'i' in node and parent.name not in ['script', 'style', 'title']
                        and len(parent.contents) == 1 and not parent.get('lang')):
                    parent['lang'] = 'en'
        soup.select_one('meta[property="og:locale"]')['content'] = cfg['locale']
        soup.select_one('link[rel="canonical"]')['href'] = SITE + new
        soup.select_one('meta[property="og:url"]')['content'] = SITE + new
        for nav in soup.find_all('nav'):
            if nav.find('a', hreflang='fr') and nav.find('ul'):
                li = soup.new_tag('li'); a = soup.new_tag('a', href=new, hreflang=code, lang=code)
                a.string = cfg['name']; a['aria-current'] = 'page'; li.append(a); nav.ul.append(li)
        if new == cfg['routes'][0]:  # home: show App Store prices next to Google Play, as /it/ does
            for plan, price in zip(soup.select('.plans > li'), ['2.99', '19.99', '49.99']):
                row = copy.deepcopy(plan.select_one('.prices > div'))
                row.dt.string = 'App Store · iOS'; row.dt['lang'] = 'en'; small = copy.deepcopy(row.dd.small)
                row.dd.clear(); row.dd.append('$' + price); row.dd.append(small); plan.select_one('.prices').insert(0, row)
            price_cell = soup.find('th', string=T['Prix']).find_next_sibling('td')
            price_cell.append(soup.new_tag('br')); price_cell.append(cfg['app_store'])
        script = soup.select_one('script[type="application/ld+json"]')
        graph = json.loads(script.string)
        def translate(obj):
            if isinstance(obj, dict): return {k: translate(v) for k, v in obj.items()}
            if isinstance(obj, list): return [translate(v) for v in obj]
            if isinstance(obj, str): return moved(T.get(obj, obj))
            return obj
        graph = translate(graph)
        for obj in graph['@graph']:
            if 'dateModified' in obj: obj.update(datePublished=TODAY, dateModified=TODAY)
            if obj.get('inLanguage') == 'fr': obj['inLanguage'] = code
            if obj['@type'] == 'WebPage':
                obj.update(name=soup.title.get_text(), description=soup.select_one('meta[name="description"]')['content'], inLanguage=code, url=SITE + new)
            if obj['@type'] == 'FAQPage':
                obj['inLanguage'] = code
                obj['mainEntity'] = [{'@type': 'Question', 'name': x.summary.get_text(' ', strip=True), 'acceptedAnswer': {'@type': 'Answer', 'text': x.select_one('.a').get_text(' ', strip=True)}} for x in soup.select('.faq > details')]
            if obj['@type'] == 'MobileApplication':
                obj['offers'] = [{'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}]
                for store, prices, url in [('Google Play', ['1.99', '14.99', '19.99'], f'https://play.google.com/store/apps/details?id=com.vibedeck.player&hl={code}'),
                                           ('App Store', ['2.99', '19.99', '49.99'], 'https://apps.apple.com/app/vibedeck-player/id6784724920')]:
                    obj['offers'] += [{'@type': 'Offer', 'name': f'VibeDeck Premium {name} ({store})', 'price': price, 'priceCurrency': 'USD', 'url': url} for name, price in zip(cfg['plans'], prices)]
        script.string = '\n' + json.dumps(graph, ensure_ascii=False, indent=1) + '\n'
        faq_count = soup.select_one('#faq .tag .dim')
        if faq_count:
            faq_count['data-section-count'] = '.faq > details'
            faq_count.string = '/ ' + str(len(soup.select('.faq > details')))
        out = path(new); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(soup.decode(formatter=Ordered()) + '\n')
    return clusters


def link_everywhere(code, clusters):
    """Reciprocal hreflang and footer language links on every page of the four clusters."""
    name = LANGS[code]['name']
    for f in ROOT.rglob('*.html'):
        if any(part.startswith(('_', '.')) for part in f.relative_to(ROOT).parts): continue
        s = f.read_text(); m = re.search(r'<link[^>]*hreflang="en"[^>]*href="' + re.escape(SITE) + r'([^"]+)"', s)
        if not m or m.group(1) not in clusters: continue
        url = clusters[m.group(1)]
        if f'hreflang="{code}"' not in s.split('</head>')[0]:
            s = s.replace('<link rel="alternate" hreflang="x-default"', f'<link rel="alternate" hreflang="{code}" href="{SITE}{url}">\n<link rel="alternate" hreflang="x-default"', 1)
        if '<footer' in s:
            i = s.index('<footer'); before, foot = s[:i], s[i:]
            def nav(n):
                text = n.group(0)
                if (not re.search(r'\slang="en"', text) and 'class="lang-switch"' not in text) or f'hreflang="{code}"' in text: return text
                a = f'<a href="{url}" hreflang="{code}" lang="{code}">{name}</a>'
                return text.replace('</ul>', f'<li>{a}</li></ul>') if '</ul>' in text else text.replace('</nav>', ' · ' + a + '</nav>')
            s = before + re.sub(r'<nav\b.*?</nav>', nav, foot, flags=re.S)
        f.write_text(s)


def extend_sitemap(code, clusters):
    NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'; X = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('', NS); ET.register_namespace('xhtml', X)
    sitemap = ROOT / 'sitemap.xml'; tree = ET.parse(sitemap); root = tree.getroot()
    by_url = {e.find('{' + NS + '}loc').text: e for e in root}
    home = LANGS[code]['routes'][0]
    for en, url in clusters.items():
        group = by_url[SITE + en]
        members = [group.find('{' + NS + '}loc').text] + [e.get('href') for e in group.findall('{' + X + '}link')]
        for member in set(members):
            el = by_url.get(member)
            if el is not None and not any(x.get('hreflang') == code for x in el.findall('{' + X + '}link')):
                ET.SubElement(el, '{' + X + '}link', {'rel': 'alternate', 'hreflang': code, 'href': SITE + url})
        if SITE + url not in by_url:
            el = ET.SubElement(root, '{' + NS + '}url'); ET.SubElement(el, '{' + NS + '}loc').text = SITE + url
            for alternate in group.findall('{' + X + '}link'): el.append(copy.deepcopy(alternate))
            ET.SubElement(el, '{' + NS + '}lastmod').text = TODAY
            ET.SubElement(el, '{' + NS + '}priority').text = '1.0' if url == home else '0.8'
            by_url[SITE + url] = el
    ET.indent(tree, space='  ')
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n')


def main():
    soups = source_soups(); items = text_items(soups)
    digest = hashlib.sha256(json.dumps(items, ensure_ascii=False).encode()).hexdigest()
    if '--dump' in sys.argv:
        print('SHA', digest)
        for i, t in enumerate(items): print(f'### {i}\n{t}')
        return
    expected = (TDIR / 'source.sha256').read_text().strip()
    if digest != expected: sys.exit('French source text changed; review translations, then update source.sha256')
    codes = [a for a in sys.argv[1:] if a in LANGS] or sys.exit(__doc__)
    for code in codes: build(code, soups, items)
    # Link every added language everywhere, so new pages also get the languages added before them
    for code in LANGS:
        if not path(LANGS[code]['routes'][0]).exists(): continue
        clusters = {soup.select_one('link[rel="alternate"][hreflang="en"]')['href'].replace(SITE, ''): route
                    for (_, soup), route in zip(soups, LANGS[code]['routes'])}
        link_everywhere(code, clusters); extend_sitemap(code, clusters)
    print('generated', ', '.join(f'{c}: {", ".join(LANGS[c]["routes"])}' for c in codes))


if __name__ == '__main__':
    main()
