#!/usr/bin/env python3
"""Remove concrete PRO prices from FAQ answers, visible and FAQPage JSON-LD in sync.

    python3 _build/faq_remove_prices.py [--write]   (default: dry run, prints every changed answer)

Only FAQ answers that contain a $ amount change. The sentence with the amounts is removed;
when the answer no longer says where the price is shown, one neutral line in the page's
language is added. Questions, other sections and other JSON-LD nodes stay byte-for-byte.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICE = re.compile(r'\$\s?\d')
USD = re.compile(r'\$\s?\d|\bUSD\b|米ドル|美元')
NEUTRAL = {
    'en': 'PRO prices depend on your country and are shown in the App Store and Google Play.',
    'ru': 'Цена PRO зависит от страны и показана в App Store и Google Play.',
    'de': 'Der Preis für PRO hängt vom Land ab und wird im App Store und bei Google Play angezeigt.',
    'es': 'El precio de PRO depende del país y aparece en el App Store y Google Play.',
    'fr': 'Le prix de PRO dépend du pays et s’affiche dans l’App Store et sur Google Play.',
    'it': 'Il prezzo di PRO dipende dal paese ed è indicato su App Store e Google Play.',
    'ja': 'PROの価格は国によって異なり、App StoreとGoogle Playに表示されます。',
    'ko': 'PRO 가격은 국가에 따라 다르며 App Store와 Google Play에 표시됩니다.',
    'nl': 'De prijs van PRO hangt af van je land en staat in de App Store en Google Play.',
    'pl': 'Cena PRO zależy od kraju i jest podana w App Store i Google Play.',
    'pt-br': 'O preço do PRO depende do país e aparece na App Store e no Google Play.',
    'tr': 'PRO fiyatı ülkeye göre değişir ve App Store ile Google Play’de gösterilir.',
    'id': 'Harga PRO tergantung negara dan ditampilkan di App Store dan Google Play.',
    'vi': 'Giá PRO tùy theo quốc gia và được hiển thị trên App Store và Google Play.',
    'th': 'ราคา PRO ขึ้นอยู่กับประเทศและแสดงใน App Store และ Google Play',
    'zh-hans': 'PRO 价格因国家或地区而异，以 App Store 和 Google Play 显示为准。',
    'zh-hant': 'PRO 價格依國家或地區而異，以 App Store 和 Google Play 顯示為準。',
}
CJK = ('ja', 'zh-hans', 'zh-hant')
STORE = re.compile(r'App Store|Google Play|ストア|스토어|\bstores?\b', re.I)


def sentences(text, lang):
    if lang == 'th':  # Thai has no full stops: a price sentence starts at "ใน App Store" / "ใน Google Play"
        return [p for p in re.split(r'\s+(?=ใน (?:App Store|Google Play))', text) if p]
    if lang in CJK:
        return [p for p in re.split(r'(?<=[。！？])', text) if p]
    return [p for p in re.split(r'(?<=[.!?])\s+(?=[^\s\d])', text) if p]


def clean(text, lang):
    if not PRICE.search(text):
        return text
    keep = [s for s in sentences(text, lang) if not USD.search(s)]
    joiner = '' if lang in CJK else ' '
    out = joiner.join(s.strip() if lang not in CJK else s for s in keep).strip()
    if not STORE.search(out):
        out = (out + joiner + NEUTRAL[lang]).strip()
    assert not PRICE.search(out), out
    return out


def main(write):
    pages = answers = 0
    for p in sorted(ROOT.rglob('index.html')):
        if any(part.startswith(('_', '.')) for part in p.relative_to(ROOT).parts):
            continue
        s = p.read_text(encoding='utf-8')
        lang = re.search(r'<html[^>]*lang="([^"]+)"', s)[1].lower()
        lang = lang if lang in NEUTRAL else lang.split('-')[0]
        n = 0

        def visible(m):
            nonlocal n
            new = clean(m[2], lang)
            if new == m[2]:
                return m[0]
            n += 1
            if not write:
                print(f'{p.relative_to(ROOT)} [{lang}]\n  - {m[2]}\n  + {new}')
            return m[1] + new + m[3]
        s2 = re.sub(r'(<details><summary>.*?</summary><div class="a"><p>)(.*?)(</p></div></details>)', visible, s, flags=re.S)

        def ld(m):
            src = m[2]
            data = json.loads(src)
            for node in data.get('@graph', [data]):
                if node.get('@type') != 'FAQPage':
                    continue
                for q in node.get('mainEntity', []):
                    old = q['acceptedAnswer']['text']
                    new = clean(old, lang)
                    if new != old:
                        for dump in (json.dumps(old, ensure_ascii=False), json.dumps(old)):
                            if dump in src:
                                src = src.replace(dump, json.dumps(new, ensure_ascii=False), 1)
                                break
                        else:
                            sys.exit(f'{p}: LD text not found verbatim')
            json.loads(src)
            return m[1] + src + m[3]
        s2 = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, s2, flags=re.S)
        if s2 != s:
            pages += 1; answers += n
            if write:
                p.write_text(s2, encoding='utf-8')
    print(f'{"wrote" if write else "dry run"}: {answers} visible answers on {pages} pages')


if __name__ == '__main__':
    main('--write' in sys.argv)
