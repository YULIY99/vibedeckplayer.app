#!/usr/bin/env python3
"""Render a portrait phone banner (headline + app screenshot in a phone frame), same look as the Sampler banners.

    python3 _build/make_phone_banner.py SCREENSHOT OUT_NAME "WHITE LINE" "BLUE LINE"
    needs Google Chrome and Pillow; serves the repo on 127.0.0.1:8781
Writes assets/img/OUT_NAME-{360,540,720}.{webp,avif}.
"""
import base64, functools, http.server, socketserver, subprocess, sys, threading
from pathlib import Path
from PIL import Image

socketserver.TCPServer.allow_reuse_address = True
ROOT = Path(__file__).resolve().parents[1]
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="/styles.css"><style>
html,body{{width:720px;height:1561px;overflow:hidden;margin:0;background:#05090e}}
.bg{{position:absolute;inset:0;background:radial-gradient(520px 420px at 50% 6%,rgba(120,160,170,.30),transparent 70%),linear-gradient(180deg,#39474b 0%,#26353a 18%,#10181e 48%,#05090e 78%)}}
h1{{position:absolute;left:0;right:0;top:62px;margin:0;text-align:center;font:800 56px/1.12 var(--sans);letter-spacing:-.01em;color:#fff;text-transform:uppercase}}
h1 span{{display:block;color:#7fd3f0}}
.ph{{position:absolute;left:67px;top:244px;width:586px;height:1247px;box-sizing:border-box;border-radius:76px;padding:10px;background:#04070b;border:3px solid rgba(165,178,188,.55);box-shadow:0 30px 90px rgba(0,0,0,.55)}}
.ph img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:64px;display:block}}
.isl{{position:absolute;left:50%;top:26px;width:150px;height:44px;margin-left:-75px;border-radius:22px;background:#000}}
</style></head><body><div class="bg"></div>
<h1>{a}<span>{b}</span></h1>
<div class="ph"><img src="{img}"><div class="isl"></div></div>
</body></html>'''


def main():
    shot, out, a, b = sys.argv[1:5]
    uri = 'data:image/webp;base64,' + base64.b64encode(Path(shot).read_bytes()).decode()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *x: None
    tmp, png = ROOT / '_pb.html', ROOT / '_pb.png'
    tmp.write_text(PAGE.format(a=a, b=b, img=uri), encoding='utf-8')
    with socketserver.TCPServer(('127.0.0.1', 8781), handler) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--user-data-dir=/tmp/vd-pb-chrome',
                        '--window-size=720,1561', '--force-device-scale-factor=2', '--virtual-time-budget=3000',
                        f'--screenshot={png}', 'http://127.0.0.1:8781/_pb.html'], capture_output=True)
        srv.shutdown()
    im = Image.open(png).convert('RGB')
    for w in (360, 540, 720):
        r = im.resize((w, round(w * 1561 / 720)), Image.LANCZOS)
        r.save(ROOT / f'assets/img/{out}-{w}.webp', quality=86, method=6)
        r.save(ROOT / f'assets/img/{out}-{w}.avif', quality=62)
    tmp.unlink(); png.unlink()
    print('banner', out)


if __name__ == '__main__':
    main()
