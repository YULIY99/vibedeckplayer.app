#!/usr/bin/env python3
"""Rename the paid tier "Premium" to "PRO" (the name the app uses since 1.0.15).

Case-sensitive, so ids, classes and anchors such as #premium stay as they are.
Korean particles and Turkish suffixes follow the new vowel ending. Idempotent.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIRST = [  # must run before the plain replacement
    ('Premium으로', 'PRO로'), ('Premium은', 'PRO는'), ('Premium을', 'PRO를'), ('Premium이', 'PRO가'), ('Premium과', 'PRO와'),
    ('Premium’a', 'PRO’ya'), ('Premium’un', 'PRO’nun'), ('Premium’da', 'PRO’da'), ('Premium’dan', 'PRO’dan'),
]

changed = 0
for p in sorted(ROOT.rglob('*.html')):
    if p.relative_to(ROOT).parts[0] in ('_build', '.github'):
        continue
    s = p.read_text(encoding='utf-8'); new = s
    for a, b in FIRST:
        new = new.replace(a, b)
    new = new.replace('Premium', 'PRO')
    if new != s:
        p.write_text(new, encoding='utf-8'); changed += 1
print('updated', changed, 'pages')
