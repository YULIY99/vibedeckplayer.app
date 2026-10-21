"""Tell Bing, Yandex, Seznam, Naver and other IndexNow engines which pages changed.

    python3 _build/indexnow.py --all              # every URL in sitemap.xml
    python3 _build/indexnow.py BEFORE_SHA AFTER_SHA  # pages changed between two commits
    add --wait to send only once GitHub Pages serves the new version
    add --dry-run to print the URLs without sending

The key file /<key>.txt at the site root proves ownership. Only URLs listed in
sitemap.xml are sent, so _build files, assets and noindex pages are never pinged.
"""
import glob, json, os, re, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vibedeckplayer.app"
ENDPOINT = "https://api.indexnow.org/indexnow"


def key():
    for p in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(p)[:-4]
        if re.fullmatch(r"[0-9a-f]{32}", name) and open(p).read().strip() == name:
            return name
    sys.exit("indexnow: key file <32 hex>.txt not found at site root")


def sitemap_urls():
    return re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())


def url_for(rel):
    if rel == "index.html":
        return SITE + "/"
    return f"{SITE}/{rel[:-len('index.html')]}" if rel.endswith("/index.html") else f"{SITE}/{rel}"


def changed(before, after):
    # "all", the zero SHA of a first push, or a force-pushed-away commit: send everything
    diff = subprocess.run(["git", "-C", ROOT, "diff", "--name-only", before, after], capture_output=True, text=True)
    if before == "all" or set(before) == {"0"} or diff.returncode:
        return sitemap_urls()
    files = diff.stdout.split()
    known = set(sitemap_urls())
    urls = [u for u in map(url_for, files) if u in known]
    # llms files and sitemap carry no page of their own; a sitemap-only change re-sends nothing
    return urls


def wait_for_deploy(url, timeout=600):
    """Poll until GitHub Pages serves the committed version of url."""
    path = url[len(SITE):].lstrip("/")
    want = open(os.path.join(ROOT, path + "index.html" if path.endswith("/") or not path else path), "rb").read()
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}?deploy-check={int(time.time())}", timeout=20) as r:
                if r.read() == want:
                    print(f"indexnow: deploy is live ({url})")
                    return
        except Exception:
            pass
        time.sleep(20)
    print("indexnow: deploy not confirmed after 10 min, sending anyway")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    urls = sitemap_urls() if "--all" in sys.argv else changed(*args[:2]) if len(args) >= 2 else sys.exit(__doc__)
    if not urls:
        print("indexnow: no indexable pages changed")
        return
    if "--wait" in sys.argv:
        wait_for_deploy(urls[0])
    k = key()
    print(f"indexnow: {len(urls)} URL(s)\n  " + "\n  ".join(urls))
    if "--dry-run" in sys.argv:
        return
    body = json.dumps({"host": "vibedeckplayer.app", "key": k, "keyLocation": f"{SITE}/{k}.txt",
                       "urlList": urls}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"indexnow: HTTP {r.status} (200/202 = accepted)")
    except urllib.error.HTTPError as e:
        sys.exit(f"indexnow: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}")


if __name__ == "__main__":
    main()
