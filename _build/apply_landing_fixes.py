#!/usr/bin/env python3
"""Targeted, idempotent landing fixes. Does not run the stale site generator."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent.parent
p = ROOT / 'index.html'
s = p.read_text()
s = s.replace('Offline music player for iPhone and Android. Play FLAC, WAV and MP3 with EQ, pitch and tempo control. Free. No ads, no account.', 'Free offline music player for iPhone and Android. Play FLAC, WAV and MP3. Pitch, filter, EQ, limiter, AURA and TONE require Premium. No ads, no account.')
s = s.replace('iPhone · iPad · Android <span class="dim">/ Offline', 'iPhone · iPad · Android <span class="dim">/ Free')
s = s.replace('with equalizer, pitch and tempo control. No WiFi needed.</p>', 'with free core playback and no WiFi needed. <a href="#premium">Premium</a> unlocks pitch, filter, EQ, limiter, AURA and TONE.</p>', 1)
old = '<div class="slider" aria-hidden="true"><div class="slider-top mono"><span><b>Pitch</b> / Filter</span><span>0.00</span></div><div class="slider-track"><span class="slider-thumb"></span></div><div class="slider-top mono"><span>0:02</span><span>BPM 124</span></div></div>'
new = '<div class="slider" data-pitch-demo data-base-bpm="124"><div class="slider-top mono"><label for="pitch-demo"><b>Pitch</b> / Premium demo</label><span><output data-pitch-value for="pitch-demo">+0.0 st</output> <button class="pitch-reset mono" type="button" data-pitch-reset>RESET</button></span></div><div class="slider-track"><input class="pitch-input" id="pitch-demo" type="range" min="-8" max="8" step="0.1" value="0" aria-label="Pitch in semitones" aria-valuetext="+0.0 st" aria-describedby="pitch-bpm"><span class="slider-thumb" aria-hidden="true"></span></div><div class="slider-top mono"><span>−8 st / +8 st</span><output id="pitch-bpm" data-pitch-bpm for="pitch-demo">BPM 124.0</output></div></div>'
s = s.replace(old, new)
if '/assets/landing-controls.css' not in s:
    s = s.replace('<link rel="stylesheet" href="/styles.css?v=13">', '<link rel="stylesheet" href="/styles.css?v=13">\n<link rel="stylesheet" href="/assets/landing-controls.css?v=1">')
s = s.replace('/assets/site.js?v=2', '/assets/site.js?v=3')
s = s.replace('VibeDeck is a premium music player for iOS and Android,', 'VibeDeck is a free music player with optional Premium for iOS and Android,')
s = s.replace('Import your audio files and shape the sound in real time with an EQ and gain, bass boost, filter, limiter, pitch, tempo, and DJ tools,', 'Import and play your audio files for free. Premium adds EQ and gain, bass boost, filter, limiter, pitch, AURA, TONE and more,')
s = s.replace('Every sound tool lives one move from the track:', 'Premium sound tools live one move from the track:')
for number, label in [('01', 'Playback'), ('02', 'Sound'), ('03', 'Tone'), ('04', 'VibeMod'), ('05', 'Aura')]:
    s = s.replace(f'<b>{number}</b> / {label}', f'<b>{number}</b> / Premium · {label}')
s = s.replace('<td>EQ with gain, bass boost, filter, stereo balance, limiter</td>', '<td>Premium: EQ with gain, bass boost, filter, stereo balance, limiter</td>')
s = s.replace('<td>Pitch up to', '<td>Premium pitch up to').replace('<td>AURA waveform, VibeMod and TONE,', '<td>Premium: AURA waveform, VibeMod and TONE,')
s = s.replace('Built for <span class="dim">/ 19</span>', 'Built for <span class="dim" data-section-count=".cards > li">/ 18</span>')
s = s.replace('FAQ <span class="dim">/ 10</span>', 'FAQ <span class="dim" data-section-count=".faq > details">/ 9</span>')
block = '<div><dt class="mono">Google Play · Android</dt><dd class="price price--sm"><small>see Google Play</small></dd></div>'
link = 'https://play.google.com/store/apps/details?id=com.vibedeck.player&amp;referrer=utm_source%3Dvibedeckplayer.app%26utm_medium%3Dwebsite%26utm_campaign%3Dhome-premium'
if block in s:
    assert s.count(block) == 3, 'Unexpected pricing layout; inspect before editing'
    s = s.replace(block, '', 2)
    s = s.replace(block, '<div><dt class="mono">Google Play · Android</dt><dd class="price price--sm"><small>One-time purchase, no subscription. <a href="' + link + '">Google Play ↗</a></small></dd></div>')
s = s.replace('on Google Play the current Premium price is shown in the store listing.', 'on Google Play Premium is a one-time purchase with no subscription. The store listing shows the current local price.')
s = s.replace('Free; Premium price shown in the Google Play listing', 'Free; Premium is a one-time purchase, no subscription. <a href="' + link + '">View on Google Play</a>')
p.write_text(s)
for p in ROOT.rglob('*.html'):
    if any(part.startswith(('_', '.')) for part in p.relative_to(ROOT).parts):
        continue
    s = p.read_text()
    t = re.sub(r'(?:plus or minus|plus ou moins|mais o menos|mais ou menos|más o menos)\s*8\s*(?:semitones|semitonos|semitons|demi-tons)', '±8 st', s, flags=re.I)
    t = re.sub(r'(±\s*8|[+−-]?\d+(?:[.,]\d+)?)\s*(?:semitones?|semitonos?|semitons?|demi-tons?|Halbtöne[n]?|Halbton|半音)(?![a-z])', r'\1 st', t, flags=re.I)
    t = t.replace('in semitones (up to ±8)', 'in semitones (st, up to ±8 st)').replace('Pitch ±8 ·', 'Pitch ±8 st ·')
    if t != s:
        p.write_text(t)
print('Landing fixes applied without rebuilding the site.')

# Keep Google Play pricing consistent with the current product plans.
import runpy
runpy.run_path(str(ROOT / "_build/update_android_pricing.py"), run_name="__main__")
