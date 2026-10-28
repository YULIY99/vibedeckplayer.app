#!/usr/bin/env python3
"""Add the "Tell a friend" share block to the 17 home pages, after the download section.

    python3 _build/add_share.py

Texts: _build/share_i18n.json. Brand icons: _build/share_icons.json (Simple Icons 13.21.0, CC0).
Share links are plain links (no third-party scripts); clicks are counted as GoatCounter events
by assets/site.js. Re-running replaces the block.
"""
import html, json, re, sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://vibedeckplayer.app'
ICONS = json.loads((ROOT / '_build/share_icons.json').read_text())
COLORS = {'whatsapp': '#25D366', 'telegram': '#26A5E4', 'facebook': '#0866FF', 'x': 'var(--text)',
          'threads': 'var(--text)', 'line': '#06C755', 'vk': '#0077FF'}
NAMES = {'whatsapp': 'WhatsApp', 'telegram': 'Telegram', 'facebook': 'Facebook', 'x': 'X', 'threads': 'Threads',
         'line': 'LINE', 'vk': 'VK'}
BASE = ['whatsapp', 'telegram', 'facebook', 'x', 'threads']
MAIL = ('<svg viewBox="0 0 24 24" aria-hidden="true" style="color:var(--accent-2)"><path d="M3.5 5.5h17v13h-17z" '
        'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="m4 6.5 8 6 8-6" '
        'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>')
NATIVE = ('<svg viewBox="0 0 24 24" aria-hidden="true" style="color:var(--accent-2)"><path d="M12 3v12M8 7l4-4 4 4M5 12v7'
          'a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
          'stroke-linejoin="round"/></svg>')
LINK = ('<svg viewBox="0 0 24 24" aria-hidden="true" style="color:var(--accent-2)"><path d="M10 13a5 5 0 0 0 7.5.5l3-3'
        'a5 5 0 0 0-7-7l-1.7 1.7M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def href(net, url, msg):
    u, m = quote(url, safe=''), quote(msg, safe='')
    return {'whatsapp': f'https://wa.me/?text={m}%20{u}',
            'telegram': f'https://t.me/share/url?url={u}&text={m}',
            'facebook': f'https://www.facebook.com/sharer/sharer.php?u={u}',
            'x': f'https://x.com/intent/post?text={m}&url={u}',
            'threads': f'https://www.threads.com/intent/post?text={m}%20{u}',
            'line': f'https://social-plugins.line.me/lineit/share?url={u}',
            'vk': f'https://vk.com/share.php?url={u}'}[net]


def block(c):
    e = html.escape
    page = SITE + c['home']
    native_url = page + '?utm_source=native&utm_medium=share&utm_campaign=share'
    # Phones only (site.js unhides it): the system share sheet reaches Instagram, TikTok, Messenger, Viber and the rest
    items = [f'<li hidden><button class="share-pill" type="button" data-share-native data-url="{e(native_url)}" data-text="{e(c["msg"])}">{NATIVE}<span>{e(c["more"])}</span></button></li>']
    for net in BASE + c.get('extra', []):
        url = f'{page}?utm_source={net}&utm_medium=share&utm_campaign=share'
        svg = f'<svg viewBox="0 0 24 24" aria-hidden="true" style="color:{COLORS[net]}"><path fill="currentColor" d="{ICONS[net]}"/></svg>'
        items.append(f'<li><a class="share-pill" href="{e(href(net, url, c["msg"]))}" target="_blank" rel="noopener" data-share="{net}">{svg}{NAMES[net]}</a></li>')
    mail = f'mailto:?subject={quote("VibeDeck Player")}&body={quote(c["msg"] + " " + page + "?utm_source=email&utm_medium=share&utm_campaign=share")}'
    items.append(f'<li><a class="share-pill" href="{e(mail)}" data-share="email">{MAIL}{e(c["email"])}</a></li>')
    copy_url = page + '?utm_source=link&utm_medium=share&utm_campaign=share'
    items.append(f'<li><button class="share-pill" type="button" data-share-copy="{e(copy_url)}" data-copied="{e(c["copied"])}">{LINK}<span>{e(c["copy"])}</span></button></li>')
    return ('<section class="section" id="share" aria-labelledby="share-title">\n'
            '  <div class="wrap">\n'
            '    <div class="share glass" data-reveal>\n'
            f'      <p class="tag">{e(c["tag"])} <span class="dim">{e(c["dim"])}</span></p>\n'
            f'      <h2 class="share-title" id="share-title">{e(c["title"])}</h2>\n'
            f'      <p class="share-text">{e(c["text"])}</p>\n'
            f'      <ul class="share-list">{"".join(items)}</ul>\n'
            '    </div>\n'
            '  </div>\n'
            '</section>\n')


def main():
    data = {k: v for k, v in json.loads((ROOT / '_build/share_i18n.json').read_text(encoding='utf-8')).items() if not k.startswith('_')}
    for code, c in data.items():
        p = ROOT / (c['home'].strip('/') + '/index.html' if c['home'] != '/' else 'index.html')
        s = p.read_text(encoding='utf-8')
        s = re.sub(r'<section class="section" id="share".*?</section>\n', '', s, flags=re.S)
        i = s.index('<section class="section" id="download"')
        j = s.index('</section>', i) + len('</section>\n')
        s = s[:j] + block(c) + s[j:]
        p.write_text(s, encoding='utf-8')
    print('share block on', len(data), 'home pages')


if __name__ == '__main__':
    main()
