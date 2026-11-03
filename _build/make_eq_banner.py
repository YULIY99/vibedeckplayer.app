#!/usr/bin/env python3
"""Render the 3-band DJ EQ / 8-band EQ banner (two real app screens side by side).

    python3 _build/make_eq_banner.py   (needs Google Chrome and Pillow; serves the repo on 127.0.0.1:8767)

Writes assets/img/vibedeck-dj-eq-3band-8band-{800,1200,1600}.{webp,avif}.
"""
import functools, http.server, socketserver, subprocess, threading
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
OUT = 'assets/img/vibedeck-dj-eq-3band-8band'

PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="/styles.css"><style>
html,body{width:1600px;height:1000px;overflow:hidden;margin:0;background:#04070d}
.bg{position:absolute;inset:0;background:radial-gradient(520px 520px at 27% 58%,rgba(30,159,214,.20),transparent 64%),radial-gradient(520px 520px at 73% 58%,rgba(30,159,214,.20),transparent 64%),linear-gradient(180deg,#05090f,#04070d 60%,#03060b)}
.col{position:absolute;top:48px;width:520px;display:flex;flex-direction:column;align-items:center}
.l{left:200px}.r{right:200px}
.t{font:600 22px/1 var(--mono);letter-spacing:.28em;color:#8fd3f0;text-transform:uppercase}
.s{margin-top:14px;font:500 16px/1 var(--mono);letter-spacing:.2em;color:#7a8f9e;text-transform:uppercase}
.ph{margin-top:30px;width:366px;height:793px;border-radius:52px;padding:10px;background:#0a1118;border:2px solid rgba(143,211,240,.42);box-shadow:0 0 0 7px rgba(4,7,13,.9),0 34px 100px rgba(30,159,214,.32)}
.ph img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:43px;display:block}
.sw{position:absolute;left:50%;top:500px;transform:translateX(-50%);display:flex;align-items:center;gap:0;padding:6px;border-radius:999px;background:#060b12;border:1.5px solid rgba(143,211,240,.3);box-shadow:0 20px 60px rgba(0,0,0,.6)}
.sw span{font:600 18px/1 var(--mono);letter-spacing:.2em;color:#7a8f9e;padding:14px 20px;border-radius:999px}
.sw .on{color:#8fd3f0;background:rgba(30,159,214,.16);box-shadow:inset 0 0 0 1.5px rgba(30,159,214,.7)}
.sw i{font-style:normal;color:#8fd3f0;font:600 22px/1 var(--mono);padding:0 6px}
</style></head><body><div class="bg"></div>
<div class="col l"><div class="t">3-Band DJ EQ</div><div class="s">Gain · Bass · Mid · High</div><div class="ph"><img src="/assets/img/vibedeck-eq-3band-iphone-800.webp"></div></div>
<div class="col r"><div class="t">8-Band EQ</div><div class="s">60 Hz to 16 kHz</div><div class="ph"><img src="/assets/img/vibedeck-eq-8band-iphone-800.webp"></div></div>
<div class="sw"><span class="on">3 BAND</span><i>&#8644;</i><span class="on">8 BAND</span></div>
</body></html>'''


def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a: None
    tmp, png = ROOT / '_eq_banner.html', ROOT / '_eq_banner.png'
    tmp.write_text(PAGE, encoding='utf-8')
    with socketserver.TCPServer(('127.0.0.1', 8767), handler) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--user-data-dir=/tmp/vd-og-chrome',
                        '--window-size=1600,1000', '--virtual-time-budget=3000', f'--screenshot={png}',
                        'http://127.0.0.1:8767/_eq_banner.html'], capture_output=True)
        srv.shutdown()
    im = Image.open(png).convert('RGB')
    for w in (800, 1200, 1600):
        r = im.resize((w, w * 1000 // 1600), Image.LANCZOS)
        r.save(ROOT / f'{OUT}-{w}.webp', quality=86, method=6)
        r.save(ROOT / f'{OUT}-{w}.avif', quality=62)
    tmp.unlink(); png.unlink()
    print('banner', OUT)


if __name__ == '__main__':
    main()
