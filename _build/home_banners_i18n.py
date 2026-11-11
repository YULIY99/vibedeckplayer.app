"""Put the new iPhone banners on the 16 localized home pages.

Same layout as the English home: iPhone 18 Pro Max hero, EQ 3-band + 8-band,
Stems banner, Sampler Rec + Trim, Cover banner in "Why".
SEO: no change to title, meta, H1, hreflang, JSON-LD or links (checked below).
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["ja", "es", "pt-br", "de", "fr", "it", "ru", "ko", "tr", "id", "pl", "nl", "vi", "zh-hant", "zh-hans", "th"]

ALT_EQ3 = {
    "ja": "iPhoneのVibeDeck 3バンドDJ EQ: ゲイン、ベース、ミッド、ハイ",
    "es": "Ecualizador DJ de 3 bandas de VibeDeck en iPhone: gain, bass, mid y high",
    "pt-br": "Equalizador DJ de 3 bandas do VibeDeck no iPhone: gain, bass, mid e high",
    "de": "VibeDeck 3-Band-DJ-EQ auf dem iPhone: Gain, Bass, Mid und High",
    "fr": "Égaliseur DJ 3 bandes de VibeDeck sur iPhone : gain, bass, mid et high",
    "it": "Equalizzatore DJ a 3 bande di VibeDeck su iPhone: gain, bass, mid e high",
    "ru": "Трёхполосный DJ-эквалайзер VibeDeck на iPhone: gain, bass, mid и high",
    "ko": "iPhone의 VibeDeck 3밴드 DJ EQ: 게인, 베이스, 미드, 하이",
    "tr": "iPhone'da VibeDeck 3 bantlı DJ EQ: gain, bass, mid ve high",
    "id": "EQ DJ 3 band VibeDeck di iPhone: gain, bass, mid, dan high",
    "pl": "3-pasmowy korektor DJ VibeDeck na iPhonie: gain, bass, mid i high",
    "nl": "VibeDeck 3-bands DJ-EQ op iPhone: gain, bass, mid en high",
    "vi": "EQ DJ 3 dải của VibeDeck trên iPhone: gain, bass, mid và high",
    "zh-hant": "iPhone 上的 VibeDeck 三段 DJ 等化器：增益、低音、中音、高音",
    "zh-hans": "iPhone 上的 VibeDeck 三段 DJ 均衡器：增益、低音、中音、高音",
    "th": "อีควอไลเซอร์ DJ 3 แบนด์ของ VibeDeck บน iPhone: gain, bass, mid และ high",
}
ALT_TRIM = {
    "ja": "iPhoneのVibeDeck Sampler: 録音をトリミングしてフェードイン・フェードアウト",
    "es": "VibeDeck Sampler en iPhone: recorta una grabación con fundido de entrada y salida",
    "pt-br": "VibeDeck Sampler no iPhone: corte uma gravação com fade in e fade out",
    "de": "VibeDeck Sampler auf dem iPhone: Aufnahme kürzen mit Fade-in und Fade-out",
    "fr": "VibeDeck Sampler sur iPhone : couper un enregistrement avec fondu d'entrée et de sortie",
    "it": "VibeDeck Sampler su iPhone: taglia una registrazione con fade in e fade out",
    "ru": "VibeDeck Sampler на iPhone: обрезка записи с плавным началом и концом",
    "ko": "iPhone의 VibeDeck Sampler: 녹음 자르기, 페이드 인과 페이드 아웃",
    "tr": "iPhone'da VibeDeck Sampler: kaydı kırp, fade in ve fade out ekle",
    "id": "VibeDeck Sampler di iPhone: potong rekaman dengan fade in dan fade out",
    "pl": "VibeDeck Sampler na iPhonie: przycinanie nagrania z fade in i fade out",
    "nl": "VibeDeck Sampler op iPhone: opname inkorten met fade-in en fade-out",
    "vi": "VibeDeck Sampler trên iPhone: cắt bản ghi với fade in và fade out",
    "zh-hant": "iPhone 上的 VibeDeck Sampler：剪輯錄音，加入淡入淡出",
    "zh-hans": "iPhone 上的 VibeDeck Sampler：剪辑录音，加入淡入淡出",
    "th": "VibeDeck Sampler บน iPhone: ตัดเสียงที่บันทึกพร้อม fade in และ fade out",
}

BOX = "overflow:hidden;border-radius:var(--r-lg);border:1px solid var(--line);box-shadow:0 40px 100px -48px rgba(30,159,214,.55)"
WIDE = ('<style>@media (min-width:900px){#sampler .studio-feature-grid,#dj-eq .studio-feature-grid{grid-template-columns:1.2fr .8fr;'
        'gap:clamp(32px,5vw,72px)}#sampler .studio-art>div:not(.studio-glow),#dj-eq .studio-art>div:not(.studio-glow){width:100%!important;gap:18px!important}}</style>')
HERO = "vibedeck-iphone-18-pro-max-now-playing"


def pic(n, alt, sizes, widths=(360, 540, 720), main=540, attrs='loading="lazy"', w=540, h=1170):
    av = ", ".join(f"/assets/img/{n}-{x}.avif {x}w" for x in widths)
    wb = ", ".join(f"/assets/img/{n}-{x}.webp {x}w" for x in widths)
    return (f'<picture><source type="image/avif" srcset="{av}" sizes="{sizes}"><source type="image/webp" srcset="{wb}" sizes="{sizes}">'
            f'<img src="/assets/img/{n}-{main}.webp" alt="{alt}" width="{w}" height="{h}" {attrs} decoding="async" style="display:block;width:100%;height:auto"></picture>')


def fig(n, alt, margin="0", sizes="(min-width: 1024px) 320px, 45vw"):
    return f'<figure style="margin:{margin};{BOX}">{pic(n, alt, sizes)}</figure>'


def pair(a, b):
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start;width:min(100%,640px)">{a}{b}</div>'


def alt_of(block):
    return re.search(r'<img [^>]*alt="([^"]*)"', block).group(1)


def replace_in_section(s, sec_id, start_pat, end_pat, build):
    t = s.index(f'id="{sec_id}"')
    pats = [start_pat, start_pat.replace('class="phone "', 'class="phone"')]
    i = min(x for x in (s.find(p, t) for p in pats) if x >= 0)
    j = s.index(end_pat, i) + len(end_pat)
    return s[:i] + build(s[i:j]) + s[j:]


def seo_snapshot(s):
    head = s[: s.index("</head>")]
    head = re.sub(r'<link rel="preload" as="image"[^>]*>', "", head)
    return head, sorted(re.findall(r'href="([^"]+)"', s)), re.search(r"<h1.*?</h1>", s, re.S).group(0)


def run(lang):
    p = ROOT / lang / "index.html"
    s = p.read_text()
    before = seo_snapshot(s)
    if HERO in s:
        return "already done"
    # hero
    i = s.index('<figure class="poster"')
    j = s.index("</figure>", i) + 9
    alt = alt_of(s[i:j])
    s = s[:i] + (f'<div data-parallax="0.04" style="position:relative;z-index:1;width:clamp(250px,74vw,360px);filter:drop-shadow(0 40px 60px rgba(30,159,214,.28))">'
                 + pic(HERO, alt, "(min-width: 1024px) 360px, 74vw", (360, 540, 720, 1068), 720, 'fetchpriority="high"', 1068, 2206) + "</div>") + s[j:]
    s = re.sub(r'<link rel="preload" as="image" type="image/avif" imagesrcset="[^"]*now-playing[^>]*>',
               f'<link rel="preload" as="image" type="image/avif" imagesrcset="/assets/img/{HERO}-360.avif 360w, /assets/img/{HERO}-540.avif 540w, /assets/img/{HERO}-720.avif 720w, /assets/img/{HERO}-1068.avif 1068w" imagesizes="(min-width: 1024px) 360px, 74vw" fetchpriority="high">', s)
    # EQ: 3-band then 8-band
    s = replace_in_section(s, "dj-eq", '<figure class="phone phone--lg">', "</figure>",
                           lambda b: pair(fig("vibedeck-3-band-dj-eq-iphone", ALT_EQ3[lang]), fig("vibedeck-equalizer-iphone", alt_of(b), "48px 0 0")))
    # Stems
    s = replace_in_section(s, "stems", '<figure class="phone phone--lg">', "</figure>",
                           lambda b: f'<figure style="margin:0;width:clamp(260px,80vw,400px);{BOX}">{pic("vibedeck-stems-acapella-backing-iphone", alt_of(b), "(min-width: 1024px) 400px, 80vw")}</figure>')
    # Sampler: Rec then Trim
    s = replace_in_section(s, "sampler", '<figure class="phone phone--lg">', "</figure>",
                           lambda b: pair(fig("vibedeck-sampler-record-system-audio-iphone", alt_of(b)), fig("vibedeck-trim-fade-share-iphone", ALT_TRIM[lang], "48px 0 0")))
    # Why: cover banner
    s = replace_in_section(s, "why", '<div class="phone " data-parallax="0.05">', "</picture></div>",
                           lambda b: f'<figure data-parallax="0.05" style="margin:0;width:clamp(250px,74vw,340px);{BOX}">{pic("vibedeck-change-cover-iphone", alt_of(b), "(min-width: 1024px) 340px, 74vw")}</figure>')
    # wider media column for the two pairs
    t = s.index('id="dj-eq"')
    k = s.rindex("<section", 0, t)
    s = s[:k] + WIDE + "\n" + s[k:]
    after = seo_snapshot(s)
    assert before == after, f"{lang}: SEO snapshot changed"
    assert s.count("<img") == (p.read_text().count("<img") + 2), lang
    p.write_text(s)
    return "ok"


if __name__ == "__main__":
    for lang in (sys.argv[1:] or LANGS):
        print(lang, run(lang))
