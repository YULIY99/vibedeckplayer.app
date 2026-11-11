"""Localized homes, same idea as the English home (11.11.2026):
banners first (Sampler, Stems, DJ EQ), long text lower, no small labels/numbering/share block,
and on phones every banner block reads title -> banner -> text.
SEO: title, meta, H1, canonical, hreflang, JSON-LD and internal links stay identical (checked).
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["ja", "es", "pt-br", "de", "fr", "it", "ru", "ko", "tr", "id", "pl", "nl", "vi", "zh-hant", "zh-hans", "th"]
MOBILE = ('<style>.studio-points li{grid-template-columns:1fr}.panel{min-height:0}'
          '@media (max-width:899px){.feat-block .studio-feature-grid{gap:0}.feat-block .studio-copy{display:contents}'
          '.feat-block .studio-copy>.h2{order:1;margin-bottom:20px}.feat-block .studio-art{order:2;padding:0 0 28px}'
          '.feat-block .studio-copy>.lede,.feat-block .studio-copy>.studio-points,.feat-block .studio-copy>.studio-link{order:3}}</style>')


def cut(s, start_pat):
    i = s.index(start_pat)
    j = s.index("</section>", i) + len("</section>")
    return s[:i] + s[j:].lstrip("\n"), s[i:j]


def snapshot(s):
    head = s[: s.index("</head>")]
    internal = sorted(u for u in re.findall(r'href="([^"]+)"', s) if not u.startswith(("http", "mailto")))
    return head, internal, re.search(r"<h1.*?</h1>", s, re.S).group(0)


def run(lang):
    p = ROOT / lang / "index.html"
    s = p.read_text()
    if "feat-block" in s:
        return "already done"
    before = snapshot(s)
    # the wide-column style sits right before the DJ EQ section; keep it with the blocks
    wide = re.search(r'<style>@media \(min-width:900px\)\{#sampler[^<]*</style>\n?', s)
    wide_css = wide.group(0).strip() if wide else ""
    if wide:
        s = s.replace(wide.group(0), "", 1)
    s, sampler = cut(s, '<section class="section studio-feature" id="sampler"')
    s, stems = cut(s, '<section class="section studio-feature" id="stems"')
    s, djeq = cut(s, '<section class="section studio-feature" id="dj-eq"')
    s, studio = cut(s, '<section class="section" id="studio"')
    blocks = [b.replace('class="section studio-feature"', 'class="section studio-feature feat-block"', 1)
              for b in (sampler, stems, djeq)]
    h = s.index('<section class="hero')
    he = s.index("</section>", h) + len("</section>")
    s = s[:he] + "\n" + MOBILE + wide_css + "\n" + "\n".join(blocks + [studio]) + "\n" + s[he:].lstrip("\n")
    # de-slop inside <main>
    a, b = s.index("<main"), s.index("</main>")
    m = s[a:b]
    m = re.sub(r'\s*<p class="tag eyebrow">.*?</p>', "", m, flags=re.S)
    m = re.sub(r'<span class="studio-index mono">\d+</span>', "", m)
    m = re.sub(r'<span class="num" aria-hidden="true">\d+</span>', "", m)
    i = m.find('<section class="section" id="share"')
    if i >= 0:
        j = m.index("</section>", i) + len("</section>")
        m = m[:i] + m[j:].lstrip("\n")
    s = s[:a] + m + s[b:]
    assert snapshot(s) == before, f"{lang}: SEO snapshot changed"
    p.write_text(s)
    return "ok"


if __name__ == "__main__":
    for lang in (sys.argv[1:] or LANGS):
        print(lang, run(lang))
