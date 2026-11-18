#!/usr/bin/env python3
"""Bring English pages in line with the current app (site home + App Store 1.0.22).

Rules, applied to every English page (root + subfolders that are not a language folder):
  - schema MobileApplication.description: formats and EQ wording
  - schema featureList: rebuilt from the current feature set (page-specific extra items kept)
  - FAQ answers that claim an exhaustive format list or an old EQ description (JSON-LD and visible text together)
Run: python3 _build/update_facts.py [--dry]
"""
import re, glob, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LANGS = 'ja es pt-br de fr it ru ko tr id pl nl vi zh-hant zh-hans th uk'.split()
SIX = 'MP3, AAC, M4A, WAV, AIFF and FLAC'

TEXT_RULES = [
 ('Offline music player for local FLAC, WAV and MP3 files with EQ and gain, ',
  'Offline music player and speed changer for local MP3, AAC, M4A, WAV, AIFF and FLAC files with a 3-band DJ EQ or 8-band equalizer, '),
 ('VibeDeck Player plays audio files stored on your device: MP3, WAV and FLAC.', f'VibeDeck Player plays audio files stored on your device: {SIX}.'),
 ('VibeDeck Player plays MP3, WAV and FLAC files stored on your device.', f'VibeDeck Player plays {SIX} files stored on your device.'),
 ('Any file VibeDeck Player plays: MP3, WAV and FLAC.', f'Any file VibeDeck Player plays: {SIX}.'),
 ('Import FLAC, WAV and MP3 files as they are.', f'Import {SIX} files as they are.'),
 ('The EQ shapes everything VibeDeck Player plays: MP3, WAV and FLAC.', f'The EQ works on everything VibeDeck Player plays: {SIX}.'),
 ('Yes. An EQ with gain, bass boost, filter, stereo balance and a limiter.',
  'Yes. Switch between a 3-band DJ EQ and an 8-band equalizer from 60 Hz to 16 kHz, with gain, bass boost, filter, stereo balance and a limiter.'),
 ('Yes. VibeDeck Player includes an EQ with gain, bass boost, filter, stereo balance and a built-in limiter, all applied in real time to your FLAC files.',
  'Yes. VibeDeck Player has a 3-band DJ EQ and an 8-band equalizer from 60 Hz to 16 kHz, plus bass boost, filter, stereo balance and a built-in limiter, all applied in real time to your FLAC files.'),
 ('Yes. VibeDeck Player plays FLAC, WAV and MP3 from your local files on Android, with an EQ and gain, ',
  f'Yes. VibeDeck Player plays {SIX} from your local files on Android, with a 3-band DJ EQ or 8-band equalizer, '),
 ('Yes, on iPhone. It has bands at 60 Hz', 'Yes, on iPhone and Android. It has bands at 60 Hz'),
 ('FLAC, WAV and MP3, played offline with no conversion', f'{SIX}, played offline with no conversion'),
 ('Offline music player for local FLAC, WAV and MP3 files with EQ and gain for real bass control,',
  'Offline music player and speed changer for local MP3, AAC, M4A, WAV, AIFF and FLAC files with a 3-band DJ EQ or 8-band equalizer for real bass control,'),
 ('<td>MP3, WAV and FLAC</td>', f'<td>{SIX}</td>'),
 ('Free offline music player for iPhone and Android. Play FLAC, WAV and MP3. Pitch,',
  'Free offline music player and speed changer for iPhone and Android. Plays MP3, FLAC, WAV, AAC and more. Pitch,'),
 ('It plays the FLAC, WAV and MP3 files already on your phone', f'It plays the {SIX} files already on your phone'),
 ('VibeDeck imports local MP3, WAV and FLAC files you choose', f'VibeDeck imports local {SIX} files you choose'),
 ('the offline music player for FLAC, WAV and MP3.', 'the offline music player for MP3, FLAC, WAV and more.'),
 ('FLAC, WAV and MP3 from your local files.', f'{SIX} from your local files.'),
 ('Offline music player for FLAC, WAV &amp; MP3 on iPhone, iPad and Android.', 'Offline music player for MP3, FLAC, WAV, M4A, AAC, AIFF &amp; more on iPhone, iPad and Android.'),
 ('Offline music player for FLAC, WAV & MP3 on iPhone, iPad and Android.', 'Offline music player for MP3, FLAC, WAV, M4A, AAC, AIFF & more on iPhone, iPad and Android.'),
]
REGEX_RULES = [
 (r'(">|"text": ")MP3, WAV and FLAC\.', r'\g<1>' + SIX + '.'),
 (r'(?<=<p>)MP3, WAV and FLAC\. VibeDeck Player plays them', SIX + '. VibeDeck Player plays them'),
 (r'(?<=<p>)MP3, WAV and FLAC\.(?=</p>)', SIX + '.'),
]
STD = [
 f'Offline playback for {SIX}',
 '3-band DJ EQ or 8-band equalizer from 60 Hz to 16 kHz, with gain, bass boost, filter, stereo balance and a built-in limiter',
 'Real-time pitch shifting up to ±8 st',
 'Independent tempo control',
 'Waveform scrubbing and BPM readout',
 'Queue with drag to reorder, cover change and Night Mode',
 'Audio-reactive AURA visualizer, VibeMod and TONE',
 'VibeDeck Studio: beat-snapped loops from 1/2 to 8 bars, speed and pitch with key lock, DJ filter, echo, space, presets such as Slowed + Reverb and Nightcore, reverse playback, session recording up to 2 minutes with fade in/out and clip sharing',
 'VibeDeck Sampler: record the sound playing on the phone from YouTube, TikTok and more, then trim, share or open it in Studio',
 'VibeDeck Stems: split a song into vocal and instrumental on the device, then mix them live',
 'Effects: bass boost, saturation, reverb and echo, plus presets such as Slowed + Reverb and Nightcore',
 'Import single tracks or whole folders, with duplicates skipped and artwork found automatically',
]
STD_PREFIX = ('3-band DJ EQ or 8-band', 'VibeDeck Sampler:', 'VibeDeck Stems:', 'Effects:', 'Import single tracks', 'Offline playback for')
GENERIC = re.compile(r'^(Offline playback for|equalizer with|Real-time pitch|Independent tempo|Waveform scrubbing|Queue with drag|Audio-reactive AURA|VibeDeck Studio:|Beat-snapped loops with fine grid)', re.I)

def en_files():
    out = []
    for f in glob.glob(str(ROOT / '**/*.html'), recursive=True):
        rel = Path(f).relative_to(ROOT)
        if rel.parts[0] == '_build' or rel.parts[0] in LANGS: continue
        out.append(Path(f))
    return sorted(out)

def fix_feature_lists(s):
    def one(m):
        items = json.loads(m.group(1))
        std = set(STD)
        extra = []
        for i in items:
            if GENERIC.match(i) or i in std or i.startswith(STD_PREFIX) or i in extra: continue
            extra.append(i)
        new = STD[:2] + extra + STD[2:]
        body = ',\n'.join('    ' + json.dumps(i, ensure_ascii=False) for i in new)
        return '"featureList": [\n' + body + '\n   ]'
    return re.subn(r'"featureList": (\[.*?\])', one, s, flags=re.S)

def process(path, dry):
    s = path.read_text(encoding='utf-8'); o = s; counts = {}
    for a, b in TEXT_RULES:
        n = s.count(a)
        if n: s = s.replace(a, b); counts[a[:40]] = n
    for a, b in REGEX_RULES:
        s, n = re.subn(a, b, s)
        if n: counts[a[:30]] = n
    s, n = fix_feature_lists(s)
    if n: counts['featureList'] = n
    if s != o and not dry: path.write_text(s, encoding='utf-8')
    return counts

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    tot = {}
    for p in en_files():
        c = process(p, dry)
        for k, v in c.items(): tot[k] = tot.get(k, 0) + v
        if c: print(p.relative_to(ROOT), sum(c.values()))
    print(tot)
