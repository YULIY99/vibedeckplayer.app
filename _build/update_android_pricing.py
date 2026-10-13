#!/usr/bin/env python3
"""Update Google Play prices only; preserve iOS prices and existing page layout."""
from pathlib import Path
import html, json, re
ROOT = Path(__file__).resolve().parent.parent
PRICES = ('1.99', '14.99', '19.99')
COPY = {
 'en': (('Monthly','Yearly','Lifetime'), ('/ mo','/ yr','once'), 'Google Play (Android): $1.99/month, $14.99/year or $19.99 lifetime (USD).', 'Free; Premium $1.99/month, $14.99/year, $19.99 lifetime (USD).'),
 'ja': (('月額','年額','買い切り'), ('/ 月','/ 年','1回払い'), 'Google Play（Android）のPremiumは月額$1.99、年額$14.99、買い切り$19.99です（米ドル）。', ''),
 'es': (('Mensual','Anual','De por vida'), ('/ mes','/ año','pago único'), 'En Google Play (Android), Premium cuesta $1.99 al mes, $14.99 al año o $19.99 de por vida (USD).', ''),
 'pt-br': (('Mensal','Anual','Vitalício'), ('/ mês','/ ano','pagamento único'), 'No Google Play (Android), o Premium custa $1.99 por mês, $14.99 por ano ou $19.99 vitalício (USD).', ''),
 'de': (('Monatlich','Jährlich','Lebenslang'), ('/ Monat','/ Jahr','einmalig'), 'Bei Google Play (Android) kostet Premium $1.99 pro Monat, $14.99 pro Jahr oder $19.99 lebenslang (USD).', ''),
 'fr': (('Mensuel','Annuel','À vie'), ('/ mois','/ an','une fois'), 'Sur Google Play (Android), Premium coûte $1.99 par mois, $14.99 par an ou $19.99 à vie (USD).', ''),
}
OLD_EN = 'on Google Play Premium is a one-time purchase with no subscription. The store listing shows the current local price.'
NEW_EN = 'on Google Play Premium costs $1.99 per month, $14.99 per year or $19.99 for a lifetime license (USD).'
PRICE_WORDS = re.compile(r'price|cost|plans|prix|prix|formules|preço|preços|planos|precio|precios|planes|preis|preise|pläne|価格|料金|プラン', re.I)

def faq_text(text, question, lang, home):
    if OLD_EN in text:
        return text.replace(OLD_EN, NEW_EN)
    if COPY[lang][2] in text or NEW_EN in text:
        return text
    if 'Premium' in text and ((('Google Play' in text or 'ストア' in text) and PRICE_WORDS.search(text)) or (home and 'Premium' in question)):
        return text + ' ' + COPY[lang][2]
    return text

for p in ROOT.rglob('*.html'):
    if any(part.startswith(('_','.')) for part in p.relative_to(ROOT).parts):
        continue
    s = p.read_text()
    m = re.search(r'<html[^>]*lang="([^"]+)"', s)
    if not m:
        continue
    lang = m[1].lower()
    if lang not in COPY:
        continue
    rel = str(p.relative_to(ROOT))
    home = rel == 'index.html' or rel == lang + '/index.html'
    if home:
        # Replace/insert only Android price rows; leave every App Store row byte-for-byte.
        def plans(match):
            section = match[0]
            index = -1
            def plan(match):
                nonlocal index
                index += 1
                card = match[0]
                row = '<div><dt class="mono">Google Play · Android</dt><dd class="price">$' + PRICES[index] + '<small>' + html.escape(COPY[lang][1][index]) + ' · USD</small></dd></div>'
                old_row = r'<div><dt class="mono">(?:(?!</dt>).)*Google Play(?:(?!</dt>).)*</dt><dd.*?</dd></div>'
                previous = re.search(old_row, card, re.S)
                if previous:
                    anchor = re.search(r'<a\b[^>]*>Google Play[^<]*</a>', previous[0])
                    if anchor:
                        row = row.replace('Google Play · Android', anchor[0] + ' · Android')
                    card = re.sub(old_row, lambda _: row, card, count=1, flags=re.S)
                elif '</dl>' in card:
                    card = card.replace('</dl>', row + '</dl>', 1)
                else:
                    card = re.sub(r'(</h3>)', lambda m: m[0] + '<dl class="prices">' + row + '</dl>', card, count=1)
                return card
            section = re.sub(r'<li\b[^>]*class="plan [^"]*"[^>]*>.*?</li>', plan, section, flags=re.S)
            assert index == 2, (rel, 'Expected three pricing cards')
            return section
        s = re.sub(r'<ul class="plans">.*?</ul>', plans, s, count=1, flags=re.S)
        if lang == 'en':
            def english_specs(m):
                anchor = re.search(r'<a\b[^>]*>.*?</a>', m[2])
                return m[1] + COPY[lang][3] + (' ' + anchor[0] if anchor else '') + m[3]
            s = re.sub(r'(<tr><th scope="row">Price on Google Play</th><td>)(.*?)(</td></tr>)', english_specs, s, count=1, flags=re.S)
        else:
            labels = {'ja':'料金','es':'Precio','pt-br':'Preço','de':'Preis','fr':'Prix'}
            pattern = r'(<tr><th scope="row">' + labels[lang] + r'</th><td>)(.*?)(</td></tr>)'
            def specs(m):
                text = m[2]
                if COPY[lang][2] not in text:
                    text += '<br>' + html.escape(COPY[lang][2], quote=False)
                return m[1] + text + m[3]
            s, n = re.subn(pattern, specs, s, count=1, flags=re.S)
            assert n == 1, (rel, 'Missing price row')
    # Pricing-related FAQ answers, in HTML and JSON-LD, including localized guides.
    def answer(m):
        text = html.unescape(m[3])
        question = html.unescape(re.sub(r'<[^>]+>', '', m[1]))
        new = faq_text(text, question, lang, home)
        return m[0] if new == text else m[1] + m[2] + html.escape(new, quote=False) + m[4]
    s = re.sub(r'(<summary>.*?</summary>)(<div class="a"><p>)(.*?)(</p></div>)', answer, s, flags=re.S)
    def ld(m):
        source = m[2]
        data = json.loads(source)
        entities = data.get('@graph', [data])
        for entity in entities:
            if entity.get('@type') == 'FAQPage':
                for q in entity.get('mainEntity', []):
                    a = q.get('acceptedAnswer', {})
                    old = a.get('text', '')
                    new = faq_text(old, q.get('name',''), lang, home)
                    if new != old:
                        source = source.replace(json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False))
        # Append Android offers without reformatting or changing existing iOS offers.
        matches = list(re.finditer(r'"offers"\s*:\s*', source))
        for om in reversed(matches):
            start = om.end()
            offers, length = json.JSONDecoder().raw_decode(source[start:])
            array = offers if isinstance(offers, list) else [offers]
            existing = [o for o in array if 'Google Play' in o.get('name','') and 'Premium' in o.get('name','')]
            if existing:
                assert [o['price'] for o in existing] == list(PRICES), (rel, 'Unexpected Android prices')
                continue
            android = [{'@type':'Offer', 'name':'VibeDeck Premium ' + COPY[lang][0][i] + ' (Google Play)', 'price':price, 'priceCurrency':'USD', 'url':'https://play.google.com/store/apps/details?id=com.vibedeck.player' + ('' if lang=='en' else '&hl='+lang)} for i,price in enumerate(PRICES)]
            original = source[start:start+length]
            addition = ',\n' + ',\n'.join('    ' + json.dumps(o, ensure_ascii=False) for o in android)
            replacement = original[:-1] + addition + '\n   ]' if isinstance(offers,list) else '[' + original + addition + '\n   ]'
            source = source[:start] + replacement + source[start+length:]
        json.loads(source)
        return m[1] + source + m[3]
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, s, flags=re.S)
    if s != p.read_text():
        p.write_text(s)
print('Google Play prices updated; iOS prices preserved.')
