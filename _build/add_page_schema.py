"""Add page-level JSON-LD: WebPage, Article (guides), dates, publisher, sameAs.

Inserts nodes as text at the top of the existing @graph so the rest of each
hand-edited block stays byte-for-byte unchanged. Dates come from git history.
Idempotent: pages that already carry "dateModified" are skipped.

    python3 _build/add_page_schema.py
"""
import html, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vibedeckplayer.app"
ORG, WEBSITE, APP = SITE + "/#org", SITE + "/#website", SITE + "/#app"
PLAY_DEV = "https://play.google.com/store/apps/developer?id=VibeDeck"
SKIP = {"404.html", "privacy.html", "support.html", "terms.html"}
GUIDES = {"audio-formats", "bass-booster", "best-offline-music-player", "change-song-key-iphone",
          "delay", "dj-filter", "dj-loop", "limiter", "saturation", "slow-down-song",
          "de/tonart-aendern", "fr/changer-tonalite", "it/cambiare-tonalita",
          "ja/key-henkou-app", "ja/tempo-henkou"}


def git_dates(rel):
    out = subprocess.run(["git", "-C", ROOT, "log", "--follow", "--format=%ad", "--date=short", "--", rel],
                         capture_output=True, text=True, check=True).stdout.split()
    return out[-1], out[0]


def node(obj):
    return "\n".join("  " + line for line in json.dumps(obj, indent=1, ensure_ascii=False).splitlines()) + ","


def main():
    files = subprocess.run(["git", "-C", ROOT, "ls-files", "*.html"], capture_output=True, text=True).stdout.split()
    changed = 0
    for rel in files:
        if rel.startswith("_build/") or rel in SKIP:
            continue
        path = os.path.join(ROOT, rel)
        s = open(path, encoding="utf-8").read()
        if '"dateModified"' in s:
            continue
        slug = rel[:-len("/index.html")] if rel.endswith("/index.html") else ""
        url = f"{SITE}/{slug}/" if slug else SITE + "/"
        lang = re.search(r'<html[^>]*\blang="([^"]+)"', s).group(1)
        title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).strip()
        desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
        image = re.search(r'<meta property="og:image" content="([^"]*)"', s).group(1)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1)
        h1 = (re.search(r'<span class="h1-plain">(.*?)</span>', h1, re.S) or re.search(r"(.*)", h1, re.S)).group(1)
        headline = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h1))).strip()[:110]
        published, modified = git_dates(rel)
        dates = {"datePublished": published, "dateModified": modified}
        new = []
        if lang == "en":
            new.append({"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
                        "description": desc, "inLanguage": "en", "isPartOf": {"@id": WEBSITE},
                        "about": {"@id": APP}, "publisher": {"@id": ORG},
                        "primaryImageOfPage": image, **dates})
            # Organization already present: add the Google Play developer page to sameAs
            s, n = re.subn(r'("sameAs": \[\s*"https://apps\.apple\.com/us/developer/yuliy-metelskiy/id6784724922")(\s*\])',
                           lambda m: f'{m.group(1)},\n    "{PLAY_DEV}"{m.group(2)}', s, count=1)
            assert n == 1, rel
        else:
            # Localized pages reference #website/#org without defining them
            new.append({"@type": "Organization", "@id": ORG, "name": "VibeDeck", "url": SITE + "/",
                        "logo": SITE + "/assets/img/icon-512.png", "email": "hello@vibedeckplayer.app",
                        "founder": {"@type": "Person", "name": "Yuliy Metelskiy"},
                        "sameAs": ["https://apps.apple.com/us/developer/yuliy-metelskiy/id6784724922", PLAY_DEV]})
            new.append({"@type": "WebSite", "@id": WEBSITE, "name": "VibeDeck Player", "url": SITE + "/",
                        "publisher": {"@id": ORG}})
            s, n = re.subn(r'(\n   "@type": "WebPage",\n)',
                           lambda m: m.group(1) + f'   "datePublished": "{published}",\n   "dateModified": "{modified}",\n'
                                                  f'   "publisher": {{"@id": "{ORG}"}},\n', s, count=1)
            assert n == 1, rel
        if slug in GUIDES:
            new.append({"@type": "Article", "@id": url + "#article", "headline": headline,
                        "description": desc, "inLanguage": lang, "image": image,
                        "author": {"@id": ORG}, "publisher": {"@id": ORG},
                        "mainEntityOfPage": {"@id": url + "#webpage"}, "about": {"@id": APP}, **dates})
        s, n = re.subn(r'("@graph": \[\n)', lambda m: m.group(1) + "\n".join(node(o) for o in new) + "\n", s, count=1)
        assert n == 1, rel
        open(path, "w", encoding="utf-8").write(s)
        changed += 1
    print(f"updated {changed} pages")


if __name__ == "__main__":
    main()
