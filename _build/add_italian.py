#!/usr/bin/env python3
"""Add Italian pages using existing layouts. Does not rebuild or replace other languages.
Run: python3 _build/add_italian.py (requires beautifulsoup4).
Translation indices are guarded by the source-text digest; changed source needs review.
"""
from pathlib import Path
import json, re, hashlib, copy
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, NavigableString, Doctype
from bs4.formatter import HTMLFormatter
ROOT=Path(__file__).resolve().parents[1]
SITE='https://vibedeckplayer.app'
ROUTES={'/fr/':'/it/','/fr/changer-tonalite/':'/it/cambiare-tonalita/','/fr/lecteur-flac/':'/it/lettore-flac/','/fr/lecteur-mp3-sans-pub/':'/it/lettore-mp3-senza-pub/'}
def path(url): return ROOT/(url.strip('/')+'/index.html')
def source_soups():
    result=[]
    for url in ROUTES:
        soup=BeautifulSoup(path(url).read_text(),'html.parser')
        for tag in soup.select('[hreflang="it"], a[lang="it"], span[lang="it"]'):
            if tag.name=='link' and tag.next_sibling=='\n':tag.next_sibling.extract()
            if tag.parent and tag.parent.name=='li':tag.parent.decompose()
            else:tag.decompose()
        result.append((url,soup))
    return result
def text_items(soups):
    items=[]
    def add(text):
        if text and text not in items:items.append(text)
    for _,soup in soups:
        for node in soup.find_all(string=True):
            if node.parent.name not in ['script','style']:add(node.strip())
        for tag in soup.find_all():
            for key in ['alt','aria-label']:add(tag.get(key))
        for tag in soup.find_all('meta'):
            if tag.get('name') in ['description','twitter:title','twitter:description'] or tag.get('property') in ['og:title','og:description','og:image:alt']:add(tag.get('content'))
    return items
class Ordered(HTMLFormatter):
    def attributes(self,tag):return tag.attrs.items()
def moved(text):
    for old,new in sorted(ROUTES.items(),key=lambda p:-len(p[0])):text=text.replace(old,new)
    return text
soups=source_soups();items=text_items(soups)
expected=(ROOT/'_build/italian_source.sha256').read_text().strip()
assert hashlib.sha256(json.dumps(items,ensure_ascii=False).encode()).hexdigest()==expected,'French source text changed; review Italian translations before generating'
translations=json.loads((ROOT/'_build/italian_translations.json').read_text())
T={items[int(i)]:text for i,text in translations.items()}
clusters={}
for old,source in soups:
    soup=copy.deepcopy(source);new=ROUTES[old]
    en=soup.select_one('link[rel="alternate"][hreflang="en"]')['href'].replace(SITE,'')
    clusters[en]=new
    for node in list(soup.find_all(string=True)):
        if node.parent.name in ['script','style'] or isinstance(node,Doctype):continue
        key=node.strip()
        if key in T:
            raw=str(node);lead=raw[:len(raw)-len(raw.lstrip())];trail=raw[len(raw.rstrip()):]
            node.replace_with(NavigableString(lead+T[key]+trail))
    for tag in soup.find_all():
        for key in ['alt','aria-label','content']:
            if tag.get(key) in T:tag[key]=T[tag[key]]
        for key in ['href','src']:
            if key not in tag.attrs:continue
            if tag.name=='link' and tag.get('rel')==['alternate']:continue
            if tag.name=='a' and tag.get('hreflang'):continue
            tag[key]=moved(tag[key])
        if tag.name=='img':
            tag['src']=tag['src'].replace('/badges/app-store-fr.svg','/badges/app-store-en.svg').replace('/badges/google-play-fr.svg','/badges/google-play-en.svg')
            if '/badges/app-store-en.svg' in tag['src']:tag['width']='144'
        if tag.name=='a' and 'store-badge' in tag.get('class',[]):
            tag['href']=tag['href'].replace('hl=fr','hl=it').replace('ct=fr-','ct=it-').replace('campaign%3Dfr-','campaign%3Dit-')
    soup.html['lang']='it'
    soup.select_one('meta[property="og:locale"]')['content']='it_IT'
    soup.select_one('link[rel="canonical"]')['href']=SITE+new
    soup.select_one('meta[property="og:url"]')['content']=SITE+new
    for nav in soup.select('nav[aria-label="Lingua"]'):
        if nav.find('ul'):
            li=soup.new_tag('li');a=soup.new_tag('a',href=new,hreflang='it',lang='it');a.string='Italiano';a['aria-current']='page';li.append(a);nav.ul.append(li)
    # Show unchanged iOS prices too, with explicit USD on the new Italian page only.
    if new=='/it/':
        for plan,price in zip(soup.select('.plans > li'),['2.99','19.99','49.99']):
            row=copy.deepcopy(plan.select_one('.prices > div'))
            row.dt.string='App Store · iOS';small=copy.deepcopy(row.dd.small)
            row.dd.clear();row.dd.append('$'+price);row.dd.append(small);plan.select_one('.prices').insert(0,row)
        price_cell=soup.find('th',string='Prezzo').find_next_sibling('td')
        price_cell.append(soup.new_tag('br'));price_cell.append('Su App Store (iOS): $2.99 al mese, $19.99 all’anno o $49.99 a vita (USD).')
    graph=json.loads(soup.select_one('script[type="application/ld+json"]').string)
    def translate(obj):
        if isinstance(obj,dict):return {k:translate(v) for k,v in obj.items()}
        if isinstance(obj,list):return [translate(v) for v in obj]
        if isinstance(obj,str):return moved(T.get(obj,obj))
        return obj
    graph=translate(graph)
    for obj in graph['@graph']:
        if obj['@type']=='WebPage':
            obj.update(name=soup.title.get_text(),description=soup.select_one('meta[name="description"]')['content'],inLanguage='it',url=SITE+new)
        if obj['@type']=='FAQPage':
            obj['inLanguage']='it';obj['mainEntity']=[{'@type':'Question','name':x.summary.get_text(' ',strip=True),'acceptedAnswer':{'@type':'Answer','text':x.select_one('.a').get_text(' ',strip=True)}} for x in soup.select('.faq > details')]
        if obj['@type']=='MobileApplication':
            obj['offers']=[{'@type':'Offer','price':'0','priceCurrency':'USD'}]
            for store,prices,url in [('Google Play',['1.99','14.99','19.99'],'https://play.google.com/store/apps/details?id=com.vibedeck.player&hl=it'),('App Store',['2.99','19.99','49.99'],'https://apps.apple.com/app/vibedeck-player/id6784724920')]:
                obj['offers'] += [{'@type':'Offer','name':'VibeDeck Premium '+name+' ('+store+')','price':price,'priceCurrency':'USD','url':url} for name,price in zip(['Mensile','Annuale','A vita'],prices)]
    soup.select_one('script[type="application/ld+json"]').string='\n'+json.dumps(graph,ensure_ascii=False,indent=1)+'\n'
    soup.select_one('script[src]')['src']='/assets/site.js?v=4'
    faq_count=soup.select_one('#faq .tag .dim')
    faq_count['data-section-count']='.faq > details'
    faq_count.string='/ '+str(len(soup.select('.faq > details')))
    output=path(new);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(soup.decode(formatter=Ordered())+'\n')
# Reciprocal alternates and visible footer links only. Preserve all existing page text.
for f in ROOT.rglob('*.html'):
    if any(part.startswith(('_','.')) for part in f.relative_to(ROOT).parts):continue
    s=f.read_text();match=re.search(r'<link[^>]*hreflang="en"[^>]*href="'+re.escape(SITE)+r'([^\"]+)"',s)
    if not match or match.group(1) not in clusters:continue
    it=clusters[match.group(1)]
    if 'hreflang="it"' not in s.split('</head>')[0]:
        s=s.replace('<link rel="alternate" hreflang="x-default"',f'<link rel="alternate" hreflang="it" href="{SITE}{it}">\n<link rel="alternate" hreflang="x-default"',1)
    if '<footer' in s:
        i=s.index('<footer');before,foot=s[:i],s[i:]
        def nav(m):
            text=m.group(0)
            if (not re.search(r'\slang="en"',text) and 'class="lang-switch"' not in text) or 'hreflang="it"' in text:return text
            a=f'<a href="{it}" hreflang="it" lang="it">Italiano</a>'
            return text.replace('</ul>',f'<li>{a}</li></ul>') if '</ul>' in text else text.replace('</nav>',' · '+a+'</nav>')
        s=before+re.sub(r'<nav\b.*?</nav>',nav,foot,flags=re.S)
    f.write_text(s)
# Extend the existing sitemap without removing URLs or other language relationships.
NS='http://www.sitemaps.org/schemas/sitemap/0.9';X='http://www.w3.org/1999/xhtml'
ET.register_namespace('',NS);ET.register_namespace('xhtml',X)
sitemap=ROOT/'sitemap.xml';tree=ET.parse(sitemap);root=tree.getroot()
by_url={e.find('{'+NS+'}loc').text:e for e in root}
for en,it in clusters.items():
    group=by_url[SITE+en]
    members=[group.find('{'+NS+'}loc').text]+[e.get('href') for e in group.findall('{'+X+'}link')]
    for url in set(members):
        if url not in by_url:continue
        el=by_url[url]
        if not any(x.get('hreflang')=='it' for x in el.findall('{'+X+'}link')):ET.SubElement(el,'{'+X+'}link',{'rel':'alternate','hreflang':'it','href':SITE+it})
        date=el.find('{'+NS+'}lastmod')
        if date is not None:date.text='2026-10-13'
    if SITE+it not in by_url:
        el=ET.SubElement(root,'{'+NS+'}url');ET.SubElement(el,'{'+NS+'}loc').text=SITE+it
        for alternate in group.findall('{'+X+'}link'):el.append(copy.deepcopy(alternate))
        ET.SubElement(el,'{'+NS+'}lastmod').text='2026-10-13';ET.SubElement(el,'{'+NS+'}priority').text='1.0' if it=='/it/' else '0.8'
ET.indent(tree,space='  ');sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n')
for name in ['llms.txt','llms-full.txt']:
    f=ROOT/name;s=f.read_text();marker='\n## Italiano\n'
    if marker in s:s=s.split(marker)[0]
    links='\n'.join(f'- [{BeautifulSoup(path(it).read_text(),"html.parser").title.get_text()}]({SITE}{it})' for it in ROUTES.values())
    f.write_text(s.rstrip()+marker+'\n'+links+'\n')
print('Italian home and three guides generated; reciprocal hreflang, switchers, sitemap and AI page links updated.')
