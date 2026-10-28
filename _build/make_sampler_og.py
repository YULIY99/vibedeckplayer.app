#!/usr/bin/env python3
"""Render 1200x630 link-preview images for the Sampler pages, one per language, and point
og:image / twitter:image at them.

    python3 _build/make_sampler_og.py      (needs Google Chrome and Pillow; serves the repo on 127.0.0.1:8766)
"""
import html, json, re, subprocess, threading, functools, http.server, socketserver
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://vibedeckplayer.app'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
OUT = ROOT / 'assets/img/og'
SHOT = '/assets/img/vibedeck-sampler-iphone-800.webp'

PAGE = '''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><link rel="stylesheet" href="/styles.css"><style>
html,body{{width:1200px;height:630px;overflow:hidden;margin:0;background:#04070d}}
body{{font-family:var(--sans),"Hiragino Sans","PingFang SC","PingFang TC","Apple SD Gothic Neo","Thonburi",sans-serif}}
.bg{{position:absolute;inset:0;background:radial-gradient(620px 520px at 82% 60%,rgba(30,159,214,.24),transparent 62%),radial-gradient(500px 360px at 5% 0%,rgba(143,211,240,.08),transparent 60%),linear-gradient(180deg,#05090f,#04070d 60%,#03060b)}}
.left{{position:absolute;left:72px;top:64px;width:700px;height:502px;display:flex;flex-direction:column}}
.t{{font:500 18px/1 var(--mono);letter-spacing:.32em;color:#8fd3f0;text-transform:uppercase}}
.t:after{{content:"";display:block;width:240px;height:2px;margin-top:16px;background:linear-gradient(90deg,#1e9fd6,transparent)}}
h1{{margin:34px 0 0;font-weight:800;font-size:64px;line-height:1.04;letter-spacing:-.035em;color:#eef6fb}}
.apps{{display:flex;gap:12px;margin-top:auto}}
.app{{display:inline-flex;align-items:center;gap:10px;height:46px;padding:0 20px;border-radius:999px;border:1.5px solid rgba(143,211,240,.28);background:rgba(30,159,214,.08);font:600 20px/1 var(--sans);color:#cfe9f7}}
.app i{{width:9px;height:9px;border-radius:50%;background:#ef5350;box-shadow:0 0 12px #ef5350}}
.foot{{margin-top:22px;font:500 16px/1.5 var(--mono);letter-spacing:.14em;color:#7a8f9e;text-transform:uppercase}}
.foot b{{color:#cfe9f7;font-weight:600}}
.ph{{position:absolute;right:70px;top:48px;width:262px;height:568px;border-radius:44px;padding:9px;background:#0a1118;border:2px solid rgba(143,211,240,.42);box-shadow:0 0 0 6px rgba(4,7,13,.9),0 30px 90px rgba(30,159,214,.3)}}
.ph img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:36px;display:block}}
</style></head><body><div class="bg"></div>
<div class="left"><div class="t">VibeDeck / Sampler</div><h1 id="h">{h1}</h1>
<div class="apps"><span class="app"><i></i>YouTube</span><span class="app"><i></i>TikTok</span><span class="app"><i></i>SoundCloud</span></div>
<div class="foot"><b>{free}</b> · MP3 · AAC · WAV · 320 kbps</div></div>
<div class="ph"><img src="{shot}"></div>
<script>var h=document.getElementById('h'),s=64;while(h.scrollHeight>230&&s>34){{s-=2;h.style.fontSize=s+'px';}}</script>
</body></html>'''


def main():
    share = json.loads((ROOT / '_build/share_i18n.json').read_text(encoding='utf-8'))
    pages = json.loads((ROOT / '_build/guides_i18n/sampler.json').read_text(encoding='utf-8'))
    langs = {'en': ('/sampler/', 'Record any sound playing on your phone.')}
    for code, c in pages.items():
        if not code.startswith('_'): langs[code] = (c['slug'], c['h1'])
    OUT.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a: None
    with socketserver.TCPServer(('127.0.0.1', 8766), handler) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        for code, (slug, h1) in langs.items():
            free = share[code]['dim'].lstrip('/ ').strip()
            tmp = ROOT / f'_og_{code}.html'
            tmp.write_text(PAGE.format(lang=code, h1=html.escape(h1), free=html.escape(free), shot=SHOT), encoding='utf-8')
            png = ROOT / f'_og_{code}.png'
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--user-data-dir=/tmp/vd-og-chrome',
                            '--window-size=1200,630', '--virtual-time-budget=3000', f'--screenshot={png}',
                            f'http://127.0.0.1:8766/_og_{code}.html'], capture_output=True)
            name = f'vibedeck-sampler-og-{code.lower()}.jpg'
            Image.open(png).convert('RGB').save(OUT / name, quality=86, optimize=True, progressive=True)
            tmp.unlink(); png.unlink()
            p = ROOT / slug.strip('/') / 'index.html'; s = p.read_text(encoding='utf-8')
            url = f'{SITE}/assets/img/og/{name}'
            s = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>' + url, s, count=1)
            s = re.sub(r'(<meta name="twitter:image" content=")[^"]*', r'\g<1>' + url, s, count=1)
            s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + html.escape(h1, quote=True), s, count=1)
            p.write_text(s, encoding='utf-8')
            print(code, name)
        srv.shutdown()


if __name__ == '__main__':
    main()
