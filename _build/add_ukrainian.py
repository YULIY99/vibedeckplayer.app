#!/usr/bin/env python3
"""Build the Ukrainian (/uk/) pages from the finished Russian pages and add `uk` hreflang everywhere.

    _build/add_ukrainian.py --dump     write _build/translations/uk-source.json (Russian strings to translate)
    _build/add_ukrainian.py --build    build the uk pages that are listed as BUILT, then update every page
    _build/add_ukrainian.py --check    verify hreflang / switcher / sitemap

Translations live in _build/translations/uk.json as {russian string: ukrainian string}.
A Russian string without a translation stops the build. Pages are cloned from /ru/ because
that is the newest localized template (banners, share block, store links already per language).
Requires beautifulsoup4.
"""
from pathlib import Path
import json, re, sys, copy
from bs4 import BeautifulSoup, Comment
from bs4.formatter import HTMLFormatter


class Ordered(HTMLFormatter):
    def attributes(self, tag):
        return list(tag.attrs.items())  # keep the attribute order of the source page

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://vibedeckplayer.app'
TDIR = ROOT / '_build' / 'translations'
CYR = re.compile('[А-Яа-яЁёІіЇїЄє]')

# ru route -> uk route. Only routes listed in BUILT are generated now; links to the others
# point to the English equivalent until they are built (rerun after adding them to BUILT).
ROUTES = {
    '/ru/': '/uk/',
    '/ru/otdelit-golos-ot-muzyki/': '/uk/vidokremyty-holos-vid-muzyky/',
    '/ru/zamedlit-pesnyu/': '/uk/spovilnyty-pisnyu/',
    '/ru/smenit-tonalnost/': '/uk/zminyty-tonalnist/',
    '/ru/zapis-zvuka-s-telefona/': '/uk/zapys-zvuku-z-telefonu/',
    '/ru/bpm/': '/uk/bpm/',
    '/ru/chto-novogo/': '/uk/shcho-nove/',
    '/ru/dj-ekvalaizer/': '/uk/dj-ekvalaizer/',
    '/ru/flac-pleer/': '/uk/flac-pleyer/',
    '/ru/mp3-pleer-bez-reklamy/': '/uk/mp3-pleyer-bez-reklamy/',
    '/ru/nightcore/': '/uk/nightcore/',
}
BUILT = [
    '/ru/', '/ru/otdelit-golos-ot-muzyki/', '/ru/zamedlit-pesnyu/',
    '/ru/smenit-tonalnost/', '/ru/zapis-zvuka-s-telefona/',
]
SKIP_ATTRS = {'href', 'src', 'srcset', 'hreflang', 'lang', 'class', 'id', 'style', 'sizes', 'data-url', 'type', 'rel'}
LD_KEYS = {'name', 'description', 'text', 'headline', 'alternateName', 'caption', 'abstract', 'articleBody'}
UK_NAME = 'Українська'


def page_path(route): return ROOT / (route.strip('/') + '/index.html') if route != '/' else ROOT / 'index.html'


def read(p): return p.read_text(encoding='utf-8')


def collect(soup):
    """Ordered Cyrillic strings of a Russian page: text nodes, attributes, JSON-LD, inline scripts."""
    out = []
    def add(s):
        s = s.strip()
        if s and CYR.search(s) and s not in out: out.append(s)
    for t in soup.find_all(string=True):
        if isinstance(t, Comment): continue
        par = t.parent
        if par.name == 'style': continue
        if par.name == 'script':
            if par.get('type') == 'application/ld+json':
                try: walk_ld(json.loads(t), add)
                except Exception: pass
            else:
                for m in re.finditer(r'(["\'])((?:(?!\1).)*[А-Яа-яЁё](?:(?!\1).)*)\1', str(t)):
                    add(m.group(2))
            continue
        if par.name == 'a' and par.has_attr('hreflang') and par.has_attr('lang'): continue  # language names stay as they are
        add(str(t))
    for el in soup.find_all(True):
        for k, v in el.attrs.items():
            if k in SKIP_ATTRS or not isinstance(v, str): continue
            add(v)
    return out


def walk_ld(o, add, key=None):
    if isinstance(o, dict):
        for k, v in o.items(): walk_ld(v, add, k)
    elif isinstance(o, list):
        for v in o: walk_ld(v, add, key)
    elif isinstance(o, str) and key in LD_KEYS: add(o)


def translate_ld(o, tr, key=None):
    if isinstance(o, dict): return {k: translate_ld(v, tr, k) for k, v in o.items()}
    if isinstance(o, list): return [translate_ld(v, tr, key) for v in o]
    if isinstance(o, str) and key in LD_KEYS and CYR.search(o): return tr[o.strip()]
    return o


def load_tr():
    p = TDIR / 'uk.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def dump():
    TDIR.mkdir(exist_ok=True)
    seen = []
    for r in BUILT:
        soup = BeautifulSoup(read(page_path(r)), 'html.parser')
        for s in collect(soup):
            if s not in seen: seen.append(s)
    tr = load_tr()
    todo = [s for s in seen if s not in tr]
    (TDIR / 'uk-source.json').write_text(json.dumps(todo, ensure_ascii=False, indent=1), encoding='utf-8')
    print('strings', len(seen), 'untranslated', len(todo))


def uk_href(href, en_of):
    """Rewrite an internal ru link to uk (built) or to its English equivalent (not built yet)."""
    m = re.match(r'^(/ru/[^?#"]*|/ru)(.*)$', href)
    if not m: return href
    route, rest = m.group(1), m.group(2)
    if route == '/ru': route = '/ru/'
    if route in ROUTES and route in BUILT: return ROUTES[route] + rest
    if route in en_of: return en_of[route] + rest
    return href


def english_map():
    out = {}
    for r in ROUTES:
        s = read(page_path(r))
        m = re.search(r'hreflang="en" href="([^"]+)"', s)
        if m: out[r] = m.group(1).replace(SITE, '') or '/'
    return out


def build_page(ru_route, tr, en_of):
    src = read(page_path(ru_route))
    soup = BeautifulSoup(src, 'html.parser')
    uk_route = ROUTES[ru_route]
    uk_url = SITE + uk_route

    def T(s):
        k = s.strip()
        if k not in tr: raise SystemExit('missing translation: ' + k[:90])
        return s.replace(k, tr[k])

    for t in list(soup.find_all(string=True)):
        if isinstance(t, Comment): continue
        par = t.parent
        if par.name == 'style': continue
        if par.name == 'script':
            if par.get('type') == 'application/ld+json':
                data = translate_ld(json.loads(t), tr)
                s = json.dumps(data, ensure_ascii=False, indent=1)
                s = s.replace('"inLanguage": "ru"', '"inLanguage": "uk"')
                s = re.sub(r'(https://vibedeckplayer\.app)(/ru/[^"]*|/ru)', lambda m: SITE + uk_href(m.group(2), en_of), s)
                t.replace_with(type(t)(s))
            else:
                def sub(m):
                    q, body = m.group(1), m.group(2)
                    return q + tr[body.strip()] + q if CYR.search(body) else m.group(0)
                t.replace_with(type(t)(re.sub(r'(["\'])((?:(?!\1).)*[А-Яа-яЁё](?:(?!\1).)*)\1', sub, str(t))))
            continue
        if par.name == 'a' and par.has_attr('hreflang') and par.has_attr('lang'): continue
        if CYR.search(str(t)): t.replace_with(T(str(t)))
    for el in soup.find_all(True):
        for k, v in list(el.attrs.items()):
            if not isinstance(v, str): continue
            if k in ('href', 'data-url') and el.has_attr('hreflang'):
                continue  # language links (switcher, alternates) keep their own targets
            if k in ('href', 'data-url'):
                v2 = uk_href(v, en_of)
                v2 = v2.replace('hl=ru', 'hl=uk').replace('ct=ru-', 'ct=uk-').replace('utm_campaign%3Dru-', 'utm_campaign%3Duk-').replace('utm_campaign=ru-', 'utm_campaign=uk-')
                el[k] = v2
            elif k in ('src', 'srcset', 'sizes', 'hreflang', 'lang', 'class', 'id', 'style', 'type', 'rel'):
                continue
            elif CYR.search(v):
                el[k] = T(v)
    # language bits
    soup.html['lang'] = 'uk'
    for m in soup.find_all('meta', attrs={'property': 'og:locale'}): m['content'] = 'uk_UA'
    for m in soup.find_all('meta', attrs={'property': 'og:url'}): m['content'] = uk_url
    for l in soup.find_all('link', attrs={'rel': 'canonical'}): l['href'] = uk_url
    # hreflang: keep ru's block, add uk for this page
    add_hreflang_uk(soup, uk_url)
    # footer switcher
    fix_switcher(soup, current_uk=True, self_route=uk_route)
    out = soup.decode(formatter=Ordered())
    out = localize_urls(out)
    dest = page_path(uk_route)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding='utf-8')
    return dest


def localize_urls(out):
    """Absolute and percent-encoded ru links (share buttons), hl=ru and campaign tokens -> uk."""
    en_of = english_map()
    def route(m):
        r = m.group(2)
        key = r if r.endswith('/') else r + '/'
        if key in ROUTES and key in BUILT: new = ROUTES[key]
        elif key in en_of: new = en_of[key]
        else: new = r
        return m.group(1) + new
    lines = []
    for line in out.split('\n'):
        if 'hreflang="ru"' not in line:
            line = re.sub(r'(https://vibedeckplayer\.app)(/ru/[^"&?#%\s]*)', route, line)
            line = re.sub(r'(https%3A//vibedeckplayer\.app)(/ru/[^"&?#%\s]*)', route, line)
            line = line.replace('hl=ru', 'hl=uk')
            line = re.sub(r'((?:utm_campaign|ct)(?:=|%3D))ru-', r'\1uk-', line)
        lines.append(line)
    return '\n'.join(lines)


def add_hreflang_uk(soup, uk_url):
    if soup.find('link', attrs={'rel': 'alternate', 'hreflang': 'uk'}): return
    xdef = soup.find('link', attrs={'rel': 'alternate', 'hreflang': 'x-default'})
    new = soup.new_tag('link', rel='alternate', hreflang='uk', href=uk_url)
    if xdef is not None: xdef.insert_before(new)
    else:
        last = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
        if last: last[-1].insert_after(new)


def fix_switcher(soup, current_uk=False, self_route='/uk/'):
    """Footer language switcher: add Українська after Русский. On the uk page, mark it current."""
    # list-style switcher (<ul><li><a hreflang=...>)
    # the ru source may already carry an uk entry from an earlier run: drop it, add exactly one
    for old in soup.find_all('a', attrs={'hreflang': 'uk'}):
        if old.parent is not None and old.parent.name == 'li': old.parent.decompose()
        else: old.decompose()
    ru_a = soup.find('a', attrs={'hreflang': 'ru'})
    if ru_a is None: return
    if soup.find('a', attrs={'hreflang': 'uk'}) is not None and not current_uk: return
    if current_uk:
        if 'aria-current' in ru_a.attrs: del ru_a['aria-current']
    parent_li = ru_a.parent if ru_a.parent.name == 'li' else None
    new_a = soup.new_tag('a', href=self_route, hreflang='uk', lang='uk')
    new_a.string = UK_NAME
    if current_uk: new_a['aria-current'] = 'page'
    if parent_li is not None:
        li = soup.new_tag('li'); li.append(new_a); parent_li.insert_after(li)
    else:  # dot-separated variant used on English pages: <a> · <a> · ...
        from bs4 import NavigableString
        sep = NavigableString(' · ')
        ru_a.insert_after(sep); sep.insert_after(new_a)


UK_LI = '<li><a href="/uk/" hreflang="uk" lang="uk">' + UK_NAME + '</a></li>'
UK_A = '<a href="/uk/" hreflang="uk" lang="uk">' + UK_NAME + '</a>'
X_DEFAULT = re.compile(r'<link rel="alternate" hreflang="x-default"[^>]*>')
RU_A = re.compile(r'<a [^>]*hreflang="ru"[^>]*>Русский</a>')


def route_of(url):
    r = url.replace(SITE, '') or '/'
    return r


def file_of(url):
    r = route_of(url)
    if r.endswith('.html'): return ROOT / r.lstrip('/')
    return ROOT / (r.strip('/') + '/index.html') if r != '/' else ROOT / 'index.html'


def add_uk_hreflang_to_group(ru_route):
    """Every page of the family gets an hreflang=uk line pointing to the new uk page."""
    ru_html = read(page_path(ru_route))
    members = re.findall(r'<link rel="alternate" hreflang="(?!x-default)[^"]+" href="([^"]+)"', ru_html)
    uk_url = SITE + ROUTES[ru_route]
    n = 0
    for m in members:
        f = file_of(m)
        if not f.exists():
            print('  member missing', m); continue
        t = read(f)
        if 'hreflang="uk"' in t: continue
        x = X_DEFAULT.search(t)
        if not x: print('  no x-default in', f.relative_to(ROOT)); continue
        t = t[:x.start()] + '<link rel="alternate" hreflang="uk" href="' + uk_url + '"/>\n' + t[x.start():]
        f.write_text(t, encoding='utf-8'); n += 1
    return n


def add_switcher_everywhere():
    """Footer language links: like every other language, a page lists Українська only when it has
    an uk equivalent (then it links straight to it). Utility pages without hreflang link to /uk/."""
    n = 0
    for f in ROOT.rglob('*.html'):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(('_build/', 'node_modules/', 'uk/')): continue
        t = read(f)
        if 'hreflang="uk" lang="uk"' in t: continue
        m = RU_A.search(t)
        if not m: continue
        has_block = 'rel="alternate" hreflang=' in t
        u = re.search(r'<link rel="alternate" hreflang="uk" href="([^"]+)"', t)
        if has_block and not u: continue
        href = route_of(u.group(1)) if u else '/uk/'
        a = '<a href="' + href + '" hreflang="uk" lang="uk">' + UK_NAME + '</a>'
        after = t[m.end():m.end() + 5]
        ins = '<li>' + a + '</li>' if after.startswith('</li>') else ' · ' + a
        pos = m.end() + 5 if after.startswith('</li>') else m.end()
        t = t[:pos] + ins + t[pos:]
        f.write_text(t, encoding='utf-8'); n += 1
    return n


def update_sitemap():
    sm = ROOT / 'sitemap.xml'
    t = read(sm)
    for r in BUILT:
        uk_url = SITE + ROUTES[r]
        ru_url = SITE + r
        ru_html = read(page_path(r))
        members = re.findall(r'<link rel="alternate" hreflang="(?!x-default)[^"]+" href="([^"]+)"', ru_html)
        link = '    <xhtml:link rel="alternate" hreflang="uk" href="' + uk_url + '" />\n'
        for m in members:
            blk = re.search(r'  <url>\n    <loc>' + re.escape(m) + r'</loc>.*?  </url>\n', t, re.S)
            if not blk or 'hreflang="uk"' in blk.group(0): continue
            b = blk.group(0)
            b2 = re.sub(r'(    <xhtml:link rel="alternate" hreflang="x-default"[^\n]*\n)', lambda mm: link + mm.group(1), b, count=1)
            t = t.replace(b, b2)
        # the new uk page itself
        if '<loc>' + uk_url + '</loc>' not in t:
            ru_blk = re.search(r'  <url>\n    <loc>' + re.escape(ru_url) + r'</loc>.*?  </url>\n', t, re.S).group(0)
            nb = ru_blk.replace('<loc>' + ru_url + '</loc>', '<loc>' + uk_url + '</loc>')
            t = t.replace('</urlset>', nb + '</urlset>')
    sm.write_text(t, encoding='utf-8')


def check():
    bad = 0
    uk_pages = [page_path(ROUTES[r]) for r in BUILT]
    for f in ROOT.rglob('*.html'):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(('_build/', 'node_modules/')): continue
        t = read(f)
        tags = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', t)
        if not tags: continue
        langs = [a for a, b in tags]
        if len(set(langs)) != len(langs): print('DUP', rel); bad += 1
        if 'x-default' not in langs: print('NO x-default', rel); bad += 1
        # reciprocity for uk
        d = dict(tags)
        if 'uk' in d:
            tgt = file_of(d['uk'])
            if not tgt.exists(): print('uk target missing', rel, d['uk']); bad += 1
            else:
                back = re.findall(r'<link rel="alternate" hreflang="[^"]+" href="([^"]+)"', read(tgt))
                me = SITE + ('/' + rel[:-10] if rel.endswith('index.html') else '/' + rel)
                me = me if me != SITE + '/' + '' else SITE + '/'
                if me.rstrip('/') != SITE and me not in back and me + '/' not in back:
                    print('NOT reciprocal', rel, '->', d['uk']); bad += 1
    for f in uk_pages:
        t = read(f)
        langs = re.findall(r'<link rel="alternate" hreflang="([^"]+)"', t)
        ru_t = read(page_path([k for k, v in ROUTES.items() if page_path(v) == f][0]))
        want = len(re.findall(r'<link rel="alternate" hreflang=', ru_t)) + (0 if 'hreflang="uk"' in ru_t else 1)
        if len(langs) != want: print('uk page lines', f.relative_to(ROOT), len(langs), 'want', want); bad += 1
        print('  ', f.relative_to(ROOT), len(langs), 'hreflang lines (incl. x-default)')
        if re.search('[ыэъёЫЭЪЁ]', re.sub(r'<a [^>]*hreflang="ru"[^>]*>Русский</a>', '', t)):
            print('Russian letters left in', f.relative_to(ROOT)); bad += 1
        if any('/ru/' in ln and 'hreflang="ru"' not in ln for ln in t.split('\n')):
            print('/ru/ link left in', f.relative_to(ROOT)); bad += 1
    print('check done, problems:', bad)
    return bad


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else '--dump'
    if mode == '--dump': dump()
    elif mode == '--build':
        tr = load_tr(); en_of = english_map()
        for r in BUILT:
            print('built', build_page(r, tr, en_of).relative_to(ROOT))
        for r in BUILT:
            print('hreflang uk added to', add_uk_hreflang_to_group(r), 'pages for', r)
        print('switcher added on', add_switcher_everywhere(), 'pages')
        update_sitemap()
    elif mode == '--check': sys.exit(1 if check() else 0)
    else: print(__doc__)


if __name__ == '__main__':
    main()
