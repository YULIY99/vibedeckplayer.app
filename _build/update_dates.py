"""Keep page dates honest: JSON-LD dateModified and sitemap <lastmod>.

A page's date is the last commit that touched it, ignoring markup-only commits
listed in _build/markup_only_commits.txt. Files with uncommitted changes get
today's date, so run this right before committing a content change.

    python3 _build/update_dates.py          # rewrite dates
    python3 _build/update_dates.py --check  # exit 1 if any date is stale
"""
import datetime, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vibedeckplayer.app"


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout


def markup_only():
    with open(os.path.join(ROOT, "_build", "markup_only_commits.txt"), encoding="utf-8") as f:
        return [git("rev-parse", line.split()[0]).strip() for line in f if line.strip() and not line.startswith("#")]


def content_dirty():
    """Uncommitted files, not counting edits this script makes to dates."""
    dirty = set()
    for rel in git("diff", "--name-only", "HEAD").split():
        lines = [l for l in git("diff", "-U0", "HEAD", "--", rel).splitlines()
                 if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        if any(not re.search(r'"dateModified": "|<lastmod>', l) for l in lines):
            dirty.add(rel)
    return dirty


def modified(rel, ignore, dirty):
    if rel in dirty:
        return datetime.date.today().isoformat()
    for line in git("log", "--follow", "--format=%H %ad", "--date=short", "--", rel).splitlines():
        sha, date = line.split()
        if sha not in ignore:
            return date
    return datetime.date.today().isoformat()


def file_for(url):
    path = url[len(SITE):].lstrip("/")
    return path + "index.html" if path.endswith("/") or not path else path


def main():
    check = "--check" in sys.argv
    ignore = set(markup_only())
    dirty = content_dirty()
    sm_path = os.path.join(ROOT, "sitemap.xml")
    sitemap = open(sm_path, encoding="utf-8").read()
    stale = []

    def fix_lastmod(m):
        date = modified(file_for(m.group(1)), ignore, dirty)
        if m.group(3) != date:
            stale.append(f"sitemap {m.group(1)}: {m.group(3)} -> {date}")
        return f"<loc>{m.group(1)}{m.group(2)}{date}"

    new_sitemap = re.sub(r"<loc>([^<]+)(</loc>(?:(?!</url>).)*?<lastmod>)([^<]+)", fix_lastmod, sitemap, flags=re.S)
    for url in re.findall(r"<loc>([^<]+)</loc>", sitemap):
        rel = file_for(url)
        path = os.path.join(ROOT, rel)
        s = open(path, encoding="utf-8").read()
        if '"dateModified"' not in s:
            continue
        date = modified(rel, ignore, dirty)
        new = re.sub(r'("dateModified": ")[^"]+(")', rf"\g<1>{date}\g<2>", s)
        if new != s:
            stale.append(f"{rel}: dateModified -> {date}")
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    if not check and new_sitemap != sitemap:
        open(sm_path, "w", encoding="utf-8").write(new_sitemap)
    for line in stale:
        print(("STALE " if check else "updated ") + line)
    if check and stale:
        print("run python3 _build/update_dates.py")
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()
