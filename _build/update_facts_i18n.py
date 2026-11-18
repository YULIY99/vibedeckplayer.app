#!/usr/bin/env python3
"""Localized pages: (1) add description + featureList to the MobileApplication schema (from schema_i18n.py),
(2) replace three-format lists (FLAC, MP3 and WAV ...) by the six supported formats, outside title-like fields.
Run: python3 _build/update_facts_i18n.py [--dry] [lang ...]
"""
import re, sys, json, glob
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from schema_i18n import S
ROOT = Path(__file__).resolve().parents[1]
LANGS = list(S)
CONJ = {'es':' y ','pt-br':' e ','de':' und ','fr':' et ','it':' e ','ru':' и ','tr':' ve ','id':' dan ','pl':' i ','nl':' en ','vi':' và ','th':' และ ','uk':' і '}
FM = ['MP3', 'AAC', 'M4A', 'WAV', 'AIFF', 'FLAC']
def six(lang, comma_only):
    if lang == 'ja': return '、'.join(FM)
    if lang.startswith('zh'): return '、'.join(FM[:-1]) + ('、' if comma_only else ' 和 ') + 'FLAC'
    if lang == 'ko' or comma_only: return ', '.join(FM)
    return ', '.join(FM[:-1]) + CONJ[lang] + 'FLAC'

SEP = r'(?:\s*[,、，/・]\s*(?:dan\s+)?|\s+[^\W\d_]{1,5}\s+|\s*[和与及]\s*|\s*と\s*|\s*및\s*)'
PAT = re.compile(r'(?<![A-Za-z0-9-])(?:FLAC|MP3|WAV)' + SEP + r'(?:FLAC|MP3|WAV)' + SEP + r'(?:FLAC|MP3|WAV)(?![A-Za-z0-9-])')
PROTECT = [re.compile(r'<title>.*?</title>', re.S), re.compile(r'<meta[^>]+(?:og|twitter):title[^>]*>', re.S),
           re.compile(r'<h1\b.*?</h1>', re.S), re.compile(r'"name": "[^"]*"')]

def protected_spans(s):
    sp = []
    for r in PROTECT:
        sp += [m.span() for m in r.finditer(s)]
    return sp

def fix_formats(s, lang):
    spans = protected_spans(s); n = 0
    def rep(m):
        nonlocal n
        if any(a <= m.start() < b for a, b in spans): return m.group(0)
        t = m.group(0)
        comma_only = not re.search(r'[^\W\d_]{1,5}\s+(?:FLAC|MP3|WAV)$|[和与及と및]', t) or lang == 'ko'
        n += 1
        if lang == 'ja' and '・' in t: return '・'.join(FM)
        return six(lang, comma_only)
    return PAT.sub(rep, s), n

def add_schema(s, lang):
    if '"featureList"' in s: return s, 0
    desc, feats = S[lang]
    ind = '   '
    block = ('"description": %s,\n%s"featureList": [\n%s\n%s],\n%s' % (
        json.dumps(desc, ensure_ascii=False), ind, ',\n'.join(ind + '  ' + json.dumps(f, ensure_ascii=False) for f in feats), ind, ind))
    k = '"operatingSystem": "iOS 17.0 or later, iPadOS, Android",\n' + ind
    cnt = s.count(k)
    if cnt == 0: return s, 0
    return s.replace(k, k + block), cnt

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    langs = [a for a in sys.argv[1:] if not a.startswith('--')] or LANGS
    for lang in langs:
        tf = ts = 0; files = 0
        for f in sorted(glob.glob(str(ROOT / lang / '**/*.html'), recursive=True)):
            s = o = Path(f).read_text(encoding='utf-8')
            s, a = fix_formats(s, lang); s, b = add_schema(s, lang)
            tf += a; ts += b
            if s != o:
                files += 1
                if not dry: Path(f).write_text(s, encoding='utf-8')
        print(lang, 'files', files, 'format lists', tf, 'schema', ts)
