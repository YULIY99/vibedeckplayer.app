#!/usr/bin/env python3
"""Add English how-to guides built on the /dj-loop/ page layout.

    python3 _build/add_guides.py [slug ...]   (no slug = every guide)

Content lives in GUIDES below. Each guide gets its own page, JSON-LD (WebPage,
Article, BreadcrumbList, FAQPage generated from the visible FAQ), a sitemap
entry and one incoming link from a related existing page. Re-running rewrites
the guide pages and skips links and sitemap entries that already exist.
Requires beautifulsoup4.
"""
from pathlib import Path
import copy, datetime, json, re, sys
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://vibedeckplayer.app'
TODAY = datetime.date.today().isoformat()
TEMPLATE = ROOT / 'dj-loop/index.html'
ANDROID_HERO = ROOT / 'offline-music-player-android/index.html'

HOME = ('/', 'Home', 'VibeDeck Player home', 'Same track, new feeling: the full tour of the offline music player.')
CARDS = {
    '/flac-player-iphone/': ('FLAC · iPhone', 'FLAC player for iPhone', 'Lossless FLAC offline on iPhone and iPad, with EQ, pitch and tempo.'),
    '/flac-player-android/': ('FLAC · Android', 'FLAC player for Android', 'Lossless FLAC offline on Android, with EQ, pitch and tempo. No ads.'),
    '/audio-formats/': ('Formats', 'Audio formats VibeDeck Player plays', 'FLAC, WAV and MP3, played offline with no conversion.'),
    '/change-song-key-iphone/': ('Pitch · iPhone', 'Change the key of a song on iPhone', 'Transpose by semitones without touching the tempo.'),
    '/slow-down-song/': ('How-to · Tempo', 'Slow down a song without changing pitch', 'Learn fast parts, choreography and solos at your own speed, in the same key.'),
    '/music-player-pitch-tempo/': ('Pitch · Tempo', 'Music player with pitch and tempo control', 'Change the key by ±8 st and the speed independently, for practice and DJ prep.'),
    '/delay/': ('Studio · FX', 'Delay and space effect', 'Echo-like depth and a soft reverb tail for tracks and loops.'),
    '/saturation/': ('Studio · FX', 'Saturation effect', 'Add warmth and grit to your tracks with the Studio saturation effect.'),
    '/dj-equalizer/': ('DJ EQ · iPhone', '3-band DJ EQ and 8-band equalizer', 'Gain, bass, mid and high, or eight bands from 60 Hz to 16 kHz. One tap to switch.'),
    '/vocal-remover/': ('Stems · iPhone', 'Vocal remover and stem splitter', 'Split a song into vocals and instrumental on your iPhone. No upload.'),
    '/karaoke-key-change/': ('How-to · Karaoke', 'Change the key for karaoke', 'Sing in your range: move the key by up to 8 semitones, same tempo.'),
    '/sampler/': ('Sampler', 'Record any sound on your phone', 'Press Rec and record what plays on your phone: YouTube, SoundCloud, any app.'),
    '/dj-loop/': ('DJ · Loop', 'How to loop part of a song', 'Beat-snapped loops from half a bar to 8 bars, tuned to the grid.'),
    '/offline-music-player-iphone/': ('Offline · iPhone', 'Offline music player for iPhone', 'Your whole library on planes and in dead zones. No WiFi needed.'),
    '/offline-music-player-android/': ('Offline · Android', 'Offline music player for Android', 'MP3, FLAC and WAV with no internet, no ads and no account.'),
    '/mp3-player-no-ads/': ('MP3 · No ads', 'MP3 player with no ads', 'Your MP3 files offline, with no account and no ads.'),
    '/play-flac-on-iphone/': ('How-to · FLAC', 'How to play FLAC on iPhone', 'Copy, import, play. No conversion and no internet.'),
    '/put-music-on-iphone-without-itunes/': ('How-to · Import', 'Put music on iPhone without iTunes', 'AirDrop, iCloud Drive and the Files app, step by step.'),
    '/slowed-reverb/': ('Effects · Preset', 'Slowed + reverb on your phone', 'One tap for the slowed + reverb sound, then fine-tune speed and reverb.'),
    '/bass-booster/': ('Effects · Bass', 'Bass booster for iPhone and Android', 'More low end for your own tracks, with the limiter to keep it clean.'),
    '/nightcore/': ('Effects · Preset', 'Nightcore on your phone', 'One tap speeds your song up and lifts the pitch: the nightcore sound.'),
    '/bpm-detector/': ('BPM · Tempo', 'BPM of every song', 'See the BPM of each track and sort your queue by tempo.'),
    '/whats-new/': ('Updates', 'What is new in VibeDeck', 'Stems, iPad support, lock screen covers and more in the latest version.'),
}

GUIDES = [
dict(slug='play-flac-on-iphone',
  title='How to Play FLAC Files on iPhone | VibeDeck Player',
  desc='Play FLAC on iPhone in three steps: copy the files with AirDrop, iCloud Drive or Files, import them into VibeDeck Player and press play. Offline, no ads.',
  crumb='How to play FLAC on iPhone', eyebrow=('How-to', 'FLAC'),
  h1='How to play FLAC files on iPhone.', h1sub='Copy, import, play. No conversion',
  lede='To play FLAC on iPhone, copy the files to your phone with AirDrop, iCloud Drive or the Files app, import them into VibeDeck Player and press play. There is nothing to convert, no internet is needed and there are no ads. The same steps work on iPad.',
  alt='Playing a FLAC file offline in VibeDeck Player on iPhone',
  statement='The Music app on iPhone does not add FLAC files to your library, so many guides tell you to convert everything first. You do not have to. A player that opens FLAC directly keeps your lossless files exactly as they are and still gives you an EQ, pitch and tempo.',
  features_title='FLAC on iPhone, the easy way',
  features=[('No conversion', 'VibeDeck Player opens FLAC as it is. Your lossless files keep every detail, and you keep one copy instead of two.'),
            ('Any way to copy', 'AirDrop from a Mac, iCloud Drive from any computer, or any place the Files app can reach.'),
            ('Sound controls', 'EQ with gain, bass boost, filter, stereo balance and a limiter, plus pitch and tempo.')],
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store.</li><li>Copy your FLAC files to the iPhone. From a Mac, select them and send them with AirDrop. From a Windows PC, upload them to iCloud Drive. Any place the Files app shows works too.</li><li>Open VibeDeck Player and import the files from Files, iCloud Drive or Downloads.</li><li>Press play. The music plays offline, with no internet.</li><li>Shape the sound with the EQ, or change pitch and tempo if you practice along.</li></ol><h2>Good to know</h2><ul><li><strong>Storage:</strong> FLAC files are bigger than MP3, so check free space before you copy a large collection.</li><li><strong>Mixed library:</strong> MP3 and WAV play in the same queue as your FLAC files.</li><li><strong>Streaming tracks:</strong> songs inside streaming apps cannot be opened by other apps. VibeDeck plays files you own.</li></ul><p>The core player is free with no ads. VibeDeck PRO unlocks the full sound engine.</p><p>Also see: <a href="/flac-player-iphone/">FLAC player for iPhone</a>, <a href="/audio-formats/">audio formats VibeDeck Player plays</a>.</p>',
  faq_title='Playing FLAC on iPhone: FAQ',
  faq=[('Can iPhone play FLAC files?', 'Yes. iPhone can open FLAC files, but the Music app does not add them to your library. VibeDeck Player imports FLAC files and plays them offline with an EQ, pitch and tempo control.'),
       ('Do I need to convert FLAC to play it on iPhone?', 'No. VibeDeck Player plays FLAC directly, so there is nothing to convert and no quality is lost.'),
       ('How do I get FLAC files onto my iPhone without a cable?', 'Use AirDrop from a Mac, or upload the files to iCloud Drive from any computer. Then import them into VibeDeck Player from the Files app or iCloud Drive.'),
       ('Does FLAC playback work offline?', 'Yes. Once imported, the files are on your iPhone and play without WiFi or mobile data.'),
       ('Is it free?', 'The core player is free and has no ads. VibeDeck PRO is optional and unlocks the full sound engine: pitch and filter, EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.')],
  related=['/flac-player-iphone/', '/put-music-on-iphone-without-itunes/', '/audio-formats/'],
  cta='Your FLAC files on iPhone, as they are. Offline. No ads.',
  link_from=('flac-player-iphone/index.html', 'Also see: <a href="/offline-music-player-iphone/">', 'how to play FLAC on iPhone')),

dict(slug='karaoke-key-change',
  title='Change the Key of a Song for Karaoke | VibeDeck Player',
  desc='Sing karaoke in your range: lower or raise a song by up to 8 semitones without changing the tempo. Works offline with your own files on iPhone and Android.',
  crumb='Change the key for karaoke', eyebrow=('How-to', 'Karaoke'),
  h1='Change the key of a song for karaoke.', h1sub='Your range, the same tempo',
  lede='To sing karaoke in a comfortable key, open the backing track in VibeDeck Player and move Pitch down or up by up to 8 semitones. The tempo stays the same, so the groove does not change. It works offline on iPhone, iPad and Android with your own audio files.',
  alt='Changing the key of a karaoke track with Pitch in VibeDeck Player',
  statement='Most songs are recorded in the singer’s key, not yours. If the chorus is too high, you strain. If it is too low, you mumble. Moving the whole track a few semitones fixes that in seconds, and keeping the tempo means you still sing with the same feel.',
  features_title='Karaoke in your key',
  features=[('Semitone steps', 'Up to 8 semitones up or down, one step at a time. Small moves make a big difference for the voice.'),
            ('Tempo stays put', 'Pitch and tempo are independent. Change the key and the song keeps its speed.'),
            ('Offline, any room', 'Your backing tracks are on the phone. No WiFi needed at the party or the rehearsal.')],
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store or Google Play.</li><li>Import the karaoke or instrumental version of the song from your files.</li><li>Play it and open <strong>Pitch</strong>.</li><li>Move it down if the song is too high, up if it is too low.</li><li>Sing a verse and the chorus, then adjust by one semitone until it feels easy.</li></ol><h2>How many semitones?</h2><ul><li><strong>Chorus a little too high:</strong> try −1 to −2.</li><li><strong>A song by a female singer, sung by a man:</strong> try −3 to −5.</li><li><strong>A song by a male singer, sung by a woman:</strong> try +3 to +5.</li><li><strong>Too low and breathy:</strong> try +1 to +2.</li></ul><p>No instrumental version? On iPhone, <a href="/vocal-remover/">VibeDeck Stems</a> splits the song into vocals and instrumental. Play the instrumental and change its key the same way.</p><p>Changing the key (Pitch) is part of VibeDeck PRO. The download is free and has no ads.</p><p>Also see: <a href="/change-song-key-iphone/">change the key of a song on iPhone</a>, <a href="/slow-down-song/">slow down a song without changing pitch</a>.</p>',
  faq_title='Karaoke key change: FAQ',
  faq=[('Can I change the key of a karaoke track on my phone?', 'Yes. Open the track in VibeDeck Player and move Pitch by up to 8 semitones in either direction. The change happens in real time.'),
       ('Will the song get slower or faster?', 'No. Pitch and tempo are independent, so the speed stays the same unless you change the tempo yourself.'),
       ('Can VibeDeck remove the vocals?', 'Yes, on iPhone. Open the song in Studio, tap STEMS and choose Instrumental. Pitch shifts the key of whatever part is playing.'),
       ('Is the original file changed?', 'No. The key changes during playback and the file is never modified. Reset returns the track to its original key.'),
       ('Does it work with songs from streaming apps?', 'No. VibeDeck only opens audio files stored on your device, such as MP3, FLAC and WAV.'),
       ('Is key change free?', 'The download is free and has no ads. Changing the key is part of VibeDeck PRO.')],
  related=['/change-song-key-iphone/', '/slow-down-song/', '/music-player-pitch-tempo/'],
  cta='Every song in your key. Offline. No ads.',
  link_from=('change-song-key-iphone/index.html', 'Also see: <a href="/slow-down-song/">', 'change the key for karaoke')),

dict(slug='slowed-reverb',
  title='Slowed + Reverb on Your Phone | VibeDeck Player',
  desc='Make slowed + reverb versions of your own songs on iPhone and iPad: lower the pitch and add the space effect in VibeDeck Studio, then record a 2-minute clip.',
  crumb='Slowed + reverb', eyebrow=('Studio', 'Slowed + reverb'),
  h1='Slowed + reverb on your phone.', h1sub='Lower, darker, with a long tail',
  lede='For a slowed + reverb sound, open your track in VibeDeck Studio, lower the pitch a few semitones and turn up the space effect for a soft reverb tail. Record up to two minutes with fade in and fade out, and share the clip. Studio works offline on iPhone and iPad.',
  alt='Building a slowed + reverb sound in VibeDeck Studio on iPhone',
  statement='Slowed + reverb is a simple recipe: the song sits lower and floats in a big room. In VibeDeck it takes one tap: the SLOWED + REVERB preset. Then you can fine-tune it with the same tools DJs use, so you decide how dark and how wide it gets.',
  features_title='Build the sound',
  features=[('One-tap preset', 'Tap SLOWED + REVERB and the track drops lower and slower with a long reverb tail.'),
            ('Add space', 'The space effect adds echo-like depth and a soft reverb tail.'),
            ('Record and share', 'Capture up to 2 minutes with fade in and fade out, then share the clip.')],
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> on iPhone or iPad and import your song.</li><li>Open the track in <strong>VibeDeck Studio</strong> or open <strong>Effects</strong>.</li><li>Tap the <strong>SLOWED + REVERB</strong> preset.</li><li>Want it deeper? Lower the speed a little more and turn up the reverb until the tail sounds right to you.</li><li>Optional: set a beat-snapped loop on your favorite part, from half a bar to 8 bars.</li><li>Press REC, record up to two minutes and share the clip.</li></ol><h2>Tips for the sound</h2><ul><li><strong>Start small:</strong> −2 semitones and a medium amount of space is a good first try.</li><li><strong>Soften the top:</strong> the Studio filter can take the edge off bright highs.</li><li><strong>Add warmth:</strong> a touch of saturation makes the low end feel thicker.</li><li><strong>Slower for listening:</strong> in the main player, tempo changes separately from pitch, so you can also hear the track slower.</li></ul><p>Studio is part of VibeDeck Player on iPhone and iPad. It works with your own files, such as MP3, FLAC and WAV.</p><p>Also see: <a href="/nightcore/">nightcore on your phone</a>, <a href="/delay/">delay and space effect</a>, <a href="/saturation/">saturation effect</a>, <a href="/dj-loop/">loop part of a song</a>.</p>',
  faq_title='Slowed + reverb: FAQ',
  faq=[('Can I make slowed + reverb on iPhone?', 'Yes. Tap the SLOWED + REVERB preset in VibeDeck, fine-tune the speed and the reverb, then record up to two minutes and share the clip.'),
       ('Is there a one-tap slowed + reverb preset?', 'Yes. Tap SLOWED + REVERB in Effects or in Studio. Then adjust the speed and the reverb if you want it deeper.'),
       ('How long can the recording be?', 'Up to two minutes, with fade in and fade out.'),
       ('Does it work on Android?', 'Studio is available on iPhone and iPad for now. On Android you can change pitch and tempo in the player.'),
       ('Can I use songs from streaming apps?', 'No. VibeDeck only opens audio files stored on your device.')],
  related=['/delay/', '/saturation/', '/dj-loop/'],
  cta='Your own slowed + reverb, offline. No ads.',
  link_from=('delay/index.html', 'Also see: <a href="/saturation/">', 'slowed + reverb on your phone')),

dict(slug='put-music-on-iphone-without-itunes',
  title='Put Music on iPhone Without iTunes | VibeDeck Player',
  desc='Put your own MP3, FLAC and WAV files on iPhone without iTunes or a cable: AirDrop, iCloud Drive or the Files app, then play them offline in VibeDeck Player.',
  crumb='Put music on iPhone without iTunes', eyebrow=('How-to', 'Import'),
  h1='How to put music on iPhone without iTunes.', h1sub='AirDrop, iCloud Drive or Files',
  lede='To put music on iPhone without iTunes, send the files with AirDrop from a Mac or upload them to iCloud Drive from any computer. Then import them into VibeDeck Player from the Files app and play them offline. MP3, FLAC and WAV work, with no conversion.',
  alt='Music imported from the Files app playing offline in VibeDeck Player',
  statement='Syncing music through iTunes or Finder means cables, libraries and conversions. If you already have the files, there is a shorter way: move them like any other file and open them in a player that reads them directly.',
  features_title='Three ways in',
  features=[('AirDrop', 'From a Mac, select the songs and AirDrop them to your iPhone in seconds.'),
            ('iCloud Drive', 'From Windows or Mac, upload the files to iCloud Drive and pick them up on the phone.'),
            ('Files app', 'Anything the Files app can reach, including Downloads, can be imported into VibeDeck Player.')],
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store.</li><li>Copy your songs to the iPhone with AirDrop, iCloud Drive or the Files app.</li><li>In VibeDeck Player, import them from Files, iCloud Drive or Downloads. The share sheet works too.</li><li>The songs appear in your library. Press play, no internet needed.</li></ol><h2>Which way to choose</h2><ul><li><strong>You have a Mac:</strong> AirDrop is the fastest for a few albums.</li><li><strong>You have a Windows PC:</strong> upload to iCloud Drive at icloud.com, then import on the phone.</li><li><strong>Files came from the web:</strong> they are usually in Downloads in the Files app.</li></ul><p>MP3, FLAC and WAV play in the same queue. No account and no ads.</p><p>Also see: <a href="/offline-music-player-iphone/">offline music player for iPhone</a>, <a href="/play-flac-on-iphone/">how to play FLAC on iPhone</a>.</p>',
  faq_title='Music on iPhone without iTunes: FAQ',
  faq=[('Can I put music on my iPhone without iTunes?', 'Yes. Copy the files with AirDrop, iCloud Drive or the Files app, then import them into VibeDeck Player. No sync and no cable needed.'),
       ('Which formats can I add?', 'MP3, WAV and FLAC. VibeDeck Player plays them without conversion.'),
       ('Do the songs need internet after import?', 'No. Imported songs are stored on your iPhone and play offline.'),
       ('Will the songs show up in the Music app?', 'No. They live in VibeDeck Player, which has its own library, queue and search.'),
       ('Do I need an account?', 'No. There is no sign-up and no login at any step.')],
  related=['/offline-music-player-iphone/', '/play-flac-on-iphone/', '/mp3-player-no-ads/'],
  cta='Your music on iPhone, no iTunes. Offline. No ads.',
  link_from=('offline-music-player-iphone/index.html', 'Related: <a href="/flac-player-iphone/">', 'put music on iPhone without iTunes')),

dict(slug='wav-player-iphone',
  title='WAV Player for iPhone, Offline, No Ads | VibeDeck Player',
  desc='Play WAV files on iPhone and iPad offline: recordings, bounces and uncompressed rips, with EQ, waveform, pitch and tempo. FLAC and MP3 too. No ads.',
  crumb='WAV player for iPhone', eyebrow=('iPhone · iPad', 'WAV'),
  h1='WAV player for iPhone.', h1sub='Uncompressed audio, offline',
  lede='VibeDeck Player plays WAV files on iPhone and iPad without internet: your recordings, studio bounces and uncompressed rips. Import them from Files, iCloud Drive or AirDrop and play them with an EQ, waveform, pitch and tempo control. No ads, no account.',
  alt='Playing a WAV recording offline in VibeDeck Player on iPhone',
  statement='WAV is what you get from a studio, a recorder or a DAW export: uncompressed and big. It is great for listening back to your own work, but most phone players are built for a streaming library, not for a folder of bounces. A file player fits better.',
  features_title='Made for WAV files',
  features=[('Uncompressed playback', 'WAV plays as it is, with no conversion and no upload.'),
            ('See the waveform', 'Scrub through the track on the waveform to jump to the part you want to check.'),
            ('Practice tools', 'Change pitch up to ±8 st and tempo separately, or loop a section in Studio.')],
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store.</li><li>Send your WAV files to the iPhone with AirDrop, iCloud Drive or the Files app.</li><li>Import them into VibeDeck Player.</li><li>Play, scrub the waveform and shape the sound with the EQ.</li></ol><h2>Who plays WAV on iPhone</h2><ul><li><strong>Musicians</strong> listening back to demos and rehearsal recordings.</li><li><strong>Producers</strong> checking a mix bounce on phone speakers and earbuds.</li><li><strong>Singers</strong> practicing with a backing track in their key.</li><li><strong>Collectors</strong> with uncompressed CD rips.</li></ul><p>WAV files are large, so keep an eye on free space. FLAC keeps CD sound in smaller files, and VibeDeck plays both in the same queue.</p><p>Also see: <a href="/audio-formats/">audio formats VibeDeck Player plays</a>, <a href="/play-flac-on-iphone/">how to play FLAC on iPhone</a>.</p>',
  faq_title='WAV player for iPhone: FAQ',
  faq=[('Can iPhone play WAV files?', 'Yes. With VibeDeck Player you import WAV files and play them offline, with an EQ, waveform, pitch and tempo.'),
       ('Do I need to convert WAV to MP3?', 'No. VibeDeck Player plays WAV directly. Converting to MP3 makes the file smaller but loses detail.'),
       ('Can I mix WAV with FLAC and MP3?', 'Yes. All three formats play in the same queue.'),
       ('Does it work on iPad?', 'Yes. VibeDeck Player runs on iPhone and iPad with iOS 17 or later.'),
       ('Is there an Android version?', 'Yes. VibeDeck Player is on Google Play and plays WAV, FLAC and MP3 offline.')],
  related=['/audio-formats/', '/flac-player-iphone/', '/put-music-on-iphone-without-itunes/'],
  cta='Your WAV files, uncompressed. Offline. No ads.',
  link_from=('audio-formats/index.html', 'Also see: <a href="/flac-player-iphone/">', 'WAV player for iPhone')),

dict(slug='google-drive-music-player-android', android=True,
  title='Play Google Drive Music Offline on Android | VibeDeck Player',
  desc='Listen to MP3, FLAC and WAV files from Google Drive on Android without internet: download them once, import into VibeDeck Player and play offline. No ads.',
  crumb='Google Drive music on Android', eyebrow=('Android', 'Google Drive'),
  h1='Play music from Google Drive offline.', h1sub='Download once, listen anywhere',
  lede='To listen to music from Google Drive without internet on Android, download the files to your phone once, then import them into VibeDeck Player and press play. MP3, FLAC and WAV play offline, with an EQ, pitch and tempo. No ads and no account.',
  alt='Music from Google Drive playing offline in VibeDeck Player on Android',
  statement='Google Drive is a good place to keep a music collection, but streaming each song from the cloud eats data and stops in a tunnel. Keep the files in Drive as a backup, and keep a copy on the phone for listening.',
  features_title='From Drive to your pocket',
  features=[('Your own copy', 'Download the songs from Drive once. After that they play with no connection.'),
            ('Lossless welcome', 'FLAC and WAV play as they are, next to your MP3 library.'),
            ('Sound controls', 'EQ with gain, bass boost, filter and limiter, plus pitch and tempo.')],
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from Google Play.</li><li>Open the Google Drive app, select your songs and tap Download.</li><li>In VibeDeck Player, import the files from your phone storage, for example the Downloads folder.</li><li>Press play. The songs now play offline.</li></ol><h2>Tips</h2><ul><li><strong>Organize first:</strong> keep the songs in one Drive folder so they are easy to select.</li><li><strong>Mind the space:</strong> FLAC and WAV are bigger than MP3, so check free storage before a large download.</li><li><strong>Keep the backup:</strong> the files stay in Drive, so you can delete local copies and download them again later.</li></ul><p>Also see: <a href="/offline-music-player-android/">offline music player for Android</a>, <a href="/flac-player-android/">FLAC player for Android</a>.</p>',
  faq_title='Google Drive music on Android: FAQ',
  faq=[('Can I play music from Google Drive offline?', 'Yes. Download the files from Google Drive to your phone, import them into VibeDeck Player and they play without internet.'),
       ('Which formats work?', 'MP3, WAV and FLAC.'),
       ('Does VibeDeck stream from Google Drive?', 'No. VibeDeck plays files stored on your device. That is what makes it work offline.'),
       ('Does it have ads?', 'No. Neither the free version nor PRO shows ads, and you do not need an account.'),
       ('Is there an iPhone version?', 'Yes. On iPhone and iPad, import songs from the Files app, iCloud Drive or AirDrop.')],
  related=['/offline-music-player-android/', '/flac-player-android/', '/mp3-player-no-ads/'],
  cta='Your Drive music, offline on Android. No ads.',
  link_from=('offline-music-player-android/index.html', 'Related: <a href="/offline-music-player-iphone/">', 'music from Google Drive offline')),

dict(slug='sampler',
  title='Record Internal Audio on iPhone and Android | VibeDeck',
  desc='Record any sound playing on your phone: YouTube, SoundCloud, TikTok and more. Edit it on the waveform, then share it, save it as a track or open it in Studio.',
  crumb='VibeDeck Sampler', eyebrow=('Feature', 'Sampler'),
  h1='Record any sound playing on your phone.', h1sub='Press Rec. Play anything. Keep it',
  lede='The VibeDeck Sampler records the sound playing on your phone, straight from the system. Press Rec, switch to YouTube, SoundCloud, TikTok or most other apps, and come back when you have what you need. No microphone, no room noise, no computer. On iPhone and Android.',
  alt='VibeDeck Sampler recording system audio on iPhone',
  statement='You hear something great in a video, a stream or a live set, and there is no download button. Holding another phone to the speaker sounds terrible. The Sampler records the sound straight from your phone, clean, while it plays.',
  features_title='Hear it, press Rec, keep it',
  features=[('Any app', 'YouTube, SoundCloud, TikTok, a browser, a game, a voice message. Most apps that play sound on your phone can be recorded.'),
            ('Clean system audio', 'MP3, AAC or WAV up to 320 kbps, 44.1 kHz stereo, straight from the phone. A live meter shows the sound coming in.'),
            ('Edit on the waveform', 'The recording turns into a waveform. Set the in and out points, add a fade in and out of 0.5, 1 or 2 seconds and preview it.')],
  prose='<h2>How to record sound from your phone</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store or Google Play.</li><li>Open VibeDeck and go to <strong>Sampler</strong>.</li><li>Press <strong>Rec</strong>.</li><li>Play the sound in YouTube, SoundCloud or any other app.</li><li>Come back and press <strong>Stop</strong>. The sample appears in Recorded Samples.</li><li>Tap it to edit it on the waveform.</li></ol><h2>What to do with the recording</h2><ul><li><strong>Share:</strong> send it to any app.</li><li><strong>Save to Library:</strong> it becomes a track in All Tracks.</li><li><strong>Open in Studio:</strong> loop it, bend it with pitch, filter, saturation and space, record your version and share it.</li></ul><h2>What people record</h2><ul><li><strong>A moment from a video:</strong> a beat, a line, a sound effect.</li><li><strong>A live stream or DJ set:</strong> the part you want to hear again.</li><li><strong>Raw material for your own sound:</strong> record it, twist it in Studio and post the result.</li><li><strong>Practice material:</strong> a riff or a vocal line to learn, then slow it down or change the key.</li></ul><p>Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The Sampler, Studio, pitch and the other tools need VibeDeck PRO.</p><p>Record only what you have the right to use. Music and videos made by other people are usually protected by copyright.</p><p>Also see: <a href="/slow-down-song/">slow down a song without changing pitch</a>, <a href="/change-song-key-iphone/">change the key of a song on iPhone</a>.</p>',
  faq_title='VibeDeck Sampler: FAQ',
  faq=[('How do I record internal audio on my phone?', 'Open the VibeDeck Sampler, press Rec and play the sound in any app. VibeDeck records the system audio while it plays.'),
       ('Can I record sound from YouTube?', 'Yes. Start recording in VibeDeck, then play the video in YouTube. The sound playing on your phone is recorded.'),
       ('Does it use the microphone?', 'No. It records the system audio, so there is no room noise in the recording. Microphone and video are not saved.'),
       ('What quality is the recording?', 'Choose MP3 for any device, AAC for smaller files or WAV for uncompressed sound. Bitrate from 128 to 320 kbps, 44.1 kHz stereo.'),
       ('Does it work on Android?', 'Yes. The Sampler works the same way on iPhone and Android.'),
       ('Can I record Apple Music?', 'No. Music protected by streaming services such as Apple Music is blocked by the system and records as silence. YouTube, SoundCloud and TikTok record fine.'),
       ('Is it free?', 'Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The Sampler, Studio, pitch and the other tools need VibeDeck PRO.')],
  related=['/slow-down-song/', '/change-song-key-iphone/', '/offline-music-player-iphone/'],
  cta='Hear it. Press Rec. Keep it.',
  link_from=('dj-loop/index.html', 'Also see: <a href="/slow-down-song/">', 'VibeDeck Sampler')),
dict(slug='vocal-remover',
  title='Vocal Remover and Stem Splitter for iPhone | VibeDeck',
  desc='Split any song into vocals and instrumental on your iPhone. Switch parts while it plays, keep tempo and loops, export each one. Nothing is uploaded.',
  crumb='VibeDeck Stems', eyebrow=('Feature', 'Stems'),
  h1='Split any song into vocals and instrumental.', h1sub='On your iPhone. Nothing uploaded',
  lede='VibeDeck Stems separates a song from your library into two parts, the vocals and the instrumental, right on your iPhone. Switch between Original, Vocal and Instrumental while the track plays, without losing your place, then export the part you need. Your music never leaves the phone.',
  alt='VibeDeck Stems splitting a song into vocal and instrumental on iPhone',
  statement='You want the instrumental to sing over, or the vocals alone to learn the words, and the song is one single file. Online vocal removers make you upload it and wait in a queue. Stems does the split with an AI model on the phone and keeps the result for next time.',
  features_title='One song, three versions',
  features=[('Original, Vocal, Instrumental', 'Tap a part to hear it. Switching keeps your place in the track, so you can compare them in a second.'),
            ('Tempo, loops and effects stay', 'Slow the instrumental down, loop a hard line of the vocal, add echo or space. The Studio tools keep working on every part.'),
            ('Export each part', 'Share the vocal or the instrumental as its own file: for karaoke, practice, covers, remixes and DJ edits.')],
  prose='<h2>How to split a song into stems on iPhone</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store.</li><li>Open a song from your library and go to <strong>Studio</strong>.</li><li>Tap <strong>STEMS</strong>.</li><li>Wait while VibeDeck separates the song. On a recent iPhone Pro it takes about as long as the song itself.</li><li>When the screen says <strong>Stems ready</strong>, choose <strong>Original</strong>, <strong>Vocal</strong> or <strong>Instrumental</strong>.</li><li>To keep a part, tap the <strong>Vocal</strong> or <strong>Instrumental</strong> export button and send it to any app.</li></ol><h2>Good to know</h2><ul><li><strong>First use:</strong> VibeDeck downloads the separation engine once from the App Store. After that, stems work offline.</li><li><strong>Once per song:</strong> the parts are saved, so next time the song opens with its stems ready. A small mark in the library shows which songs have them.</li><li><strong>Leave the app any time:</strong> separation pauses and continues when you come back.</li><li><strong>Private by design:</strong> the split runs on the iPhone. Nothing is uploaded.</li></ul><h2>What people use stems for</h2><ul><li><strong>Karaoke:</strong> play the instrumental and <a href="/karaoke-key-change/">change the key</a> to fit your voice.</li><li><strong>Learning songs:</strong> the vocals alone, slowed down, to catch every word.</li><li><strong>Practice:</strong> play your instrument over the instrumental.</li><li><strong>Remixes and DJ edits:</strong> export an a cappella or an instrumental and build on it.</li></ul><p>Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. Stems, Studio, the Sampler, pitch and the other tools need VibeDeck PRO.</p><p>Make stems only of music you have the right to use. Songs by other artists are usually protected by copyright.</p><p>Also see: <a href="/slow-down-song/">slow down a song without changing pitch</a>, <a href="/change-song-key-iphone/">change the key of a song on iPhone</a>.</p>',
  faq_title='VibeDeck Stems: FAQ',
  faq=[('How do I remove vocals from a song on iPhone?', 'Open the song in VibeDeck Studio, tap STEMS and choose Instrumental when the stems are ready. You can also export the instrumental as its own file.'),
       ('Can I get only the vocals (a cappella)?', 'Yes. Choose Vocal to hear only the voice, or export it with the Vocal button.'),
       ('Is my music uploaded?', 'No. The separation runs on your iPhone. Only the separation engine is downloaded, once, the first time you use Stems.'),
       ('How long does it take?', 'On a recent iPhone Pro, about as long as the song. Older iPhones take longer. If you leave the app, the split pauses and continues when you return.'),
       ('Can I slow down or loop the instrumental?', 'Yes. Tempo, loops and effects stay available after you switch parts, and switching keeps your place in the track.'),
       ('Which files can I split?', 'Songs in your VibeDeck library: MP3, WAV, FLAC and the other formats VibeDeck plays.'),
       ('Is it free?', 'Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. Stems, Studio, the Sampler, pitch and the other tools need VibeDeck PRO.')],
  related=['/karaoke-key-change/', '/slow-down-song/', '/change-song-key-iphone/'],
  cta='One song. Vocal, instrumental, original.',
  link_from=('karaoke-key-change/index.html', 'Also see: <a href="/change-song-key-iphone/">', 'vocal remover for iPhone')),
dict(slug='dj-equalizer',
  title='3-Band DJ EQ and 8-Band Equalizer for iPhone | VibeDeck',
  desc='Switch between a 3-band DJ EQ (gain, bass, mid, high) and an 8-band equalizer from 60 Hz to 16 kHz on iPhone. With limiter, mono and balance. No ads.',
  crumb='VibeDeck DJ EQ', eyebrow=('Feature', 'DJ EQ'),
  h1='Switch between a 3-band DJ EQ and an 8-band equalizer.', h1sub='One tap. Same track. On iPhone',
  lede='VibeDeck Player has two equalizers on one screen. The 3-band DJ EQ gives you big faders for gain, bass, mid and high, the way a DJ mixer does. The 8-band EQ shapes the sound in detail at 60, 150 and 400 Hz and at 1, 2, 4, 8 and 16 kHz. Tap 3 BAND or 8 BAND to switch while the music plays.',
  alt='VibeDeck 8-band equalizer on iPhone: eight faders from 60 Hz to 16 kHz',
  statement='DJs think in three moves: low, mid, high. Sound lovers want finer control: a little more air at 16 kHz, a little less boom at 150 Hz. Most players give you one or the other. VibeDeck gives you both and switches between them in one tap.',
  features_title='Two equalizers, one tap apart',
  features=[('3-band DJ EQ', 'Gain, bass, mid and high on big vertical faders, from +12 down to -24 dB. Fast moves you can make without looking.'),
            ('8-band equalizer', 'Eight faders at 60, 150, 400, 1k, 2k, 4k, 8k and 16k, each from -12 to +12 dB, plus its own gain bar.'),
            ('VibeMod, limiter, mono', 'VibeMod adds dense, punchy processing. The limiter keeps loud peaks clean. Mono folds the mix to one channel, so producers can check that the kick and bass sit in the middle.')],
  prose='<figure style="margin:0 0 28px"><picture><source type="image/avif" srcset="/assets/img/vibedeck-dj-eq-3band-8band-800.avif 800w, /assets/img/vibedeck-dj-eq-3band-8band-1200.avif 1200w, /assets/img/vibedeck-dj-eq-3band-8band-1600.avif 1600w" sizes="(min-width: 1024px) 860px, 92vw"><source type="image/webp" srcset="/assets/img/vibedeck-dj-eq-3band-8band-800.webp 800w, /assets/img/vibedeck-dj-eq-3band-8band-1200.webp 1200w, /assets/img/vibedeck-dj-eq-3band-8band-1600.webp 1600w" sizes="(min-width: 1024px) 860px, 92vw"><img src="/assets/img/vibedeck-dj-eq-3band-8band-1200.webp" alt="Switch between the 3-band DJ EQ and the 8-band equalizer in VibeDeck on iPhone" width="1200" height="750" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:24px"></picture></figure><h2>How to switch between the 3-band and 8-band EQ</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store.</li><li>Play a track from your library and open the <strong>EQ</strong>.</li><li>Tap <strong>3 BAND</strong> for the DJ EQ and move <strong>GAIN</strong>, <strong>BASS</strong>, <strong>MID</strong> and <strong>HIGH</strong>.</li><li>Tap <strong>8 BAND</strong> for the 8-band equalizer and shape each band from 60 Hz to 16 kHz.</li><li>Pushing the sound hard? Switch on <strong>LIMITER</strong> to keep the peaks clean. Tap <strong>VIBEMOD</strong> for a denser, punchier sound.</li><li>Tap <strong>MONO</strong> to hear the mix in mono, and <strong>L/R</strong> to set the balance.</li><li>Tap <strong>RESET EQ</strong> to go back to flat.</li></ol><h2>Good to know</h2><ul><li><strong>Switch any time:</strong> the music keeps playing when you change from 3 bands to 8 and back.</li><li><strong>Two styles of control:</strong> the 3-band DJ EQ is for quick, big moves. The 8-band EQ is for fine tuning to your headphones, speaker or car.</li><li><strong>Your own files:</strong> MP3, FLAC, WAV and the other formats VibeDeck plays, offline.</li><li><strong>On iPhone:</strong> the 3 BAND / 8 BAND switch is in the iPhone app.</li></ul><h2>Who uses it</h2><ul><li><strong>Producers:</strong> play your own track in mono to check that the kick and bass sit in the center, hear phase problems and test how the mix sounds on a club system or a phone speaker. Then switch back to stereo and compare.</li><li><strong>DJs:</strong> prepare tracks with the DJ EQ: cut the bass before a drop, lift the highs, check the mix on headphones.</li><li><strong>Bass lovers:</strong> push 60 Hz for the sub and keep 150 Hz under control.</li><li><strong>Headphone listeners:</strong> tune the 8 bands to the sound of your headphones.</li><li><strong>FLAC collectors:</strong> fine EQ for lossless files.</li><li><strong>Drivers:</strong> match the sound to the car speakers.</li></ul><p>Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The EQ, the limiter and the other sound tools need VibeDeck PRO.</p><p>Also see: <a href="/bass-booster/">boost bass on iPhone</a>, <a href="/limiter/">the limiter</a>, <a href="/dj-app/">VibeDeck as a DJ app</a>.</p>',
  faq_title='VibeDeck DJ EQ: FAQ',
  faq=[('Does VibeDeck have a DJ EQ?', 'Yes. The 3-band DJ EQ has gain, bass, mid and high faders, like the EQ on a DJ mixer.'),
       ('Does VibeDeck have an 8-band equalizer?', 'Yes, on iPhone. It has bands at 60 Hz, 150 Hz, 400 Hz, 1 kHz, 2 kHz, 4 kHz, 8 kHz and 16 kHz, each from -12 to +12 dB, and a separate gain control.'),
       ('How do I switch between 3 bands and 8 bands?', 'Open the EQ and tap 3 BAND or 8 BAND at the top of the panel. The music keeps playing.'),
       ('Which one should I use?', 'The 3-band DJ EQ for quick, DJ-style moves on bass, mids and highs. The 8-band EQ when you want to tune the sound in detail to your headphones, speaker or car.'),
       ('Can I listen to a track in mono?', 'Yes. Tap MONO under the EQ. Producers use it to check that the kick and bass sit in the middle of the mix and that nothing disappears in mono.'),
       ('What does VibeMod do?', 'VibeMod is a special dense processing of the sound. It makes the track fuller and punchier. Switch it on and off under the EQ to compare.'),
       ('Will a big boost distort the sound?', 'A strong boost can make loud peaks clip. Switch on LIMITER to keep them clean.'),
       ('Does it work offline?', 'Yes. The EQ works on the music files in your VibeDeck library, with no internet.'),
       ('Is it free?', 'Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The EQ, the limiter and the other sound tools need VibeDeck PRO.')],
  related=['/dj-loop/', '/music-player-pitch-tempo/', '/vocal-remover/'],
  cta='Three bands for the mix. Eight for the detail.',
  link_from=('dj-app/index.html', 'Also see: <a href="/dj-loop/">', '3-band DJ EQ and 8-band equalizer')),

dict(slug='nightcore',
  title='Nightcore Maker for iPhone: One-Tap Preset | VibeDeck',
  desc='Make a nightcore version of your own songs on iPhone and iPad: tap the NIGHTCORE preset in VibeDeck to speed the track up and raise the pitch. Offline, no ads.',
  crumb='Nightcore', eyebrow=('Effects', 'Nightcore'),
  h1='Nightcore on your phone, in one tap.', h1sub='Faster, higher, brighter',
  lede='To make nightcore, play your song in VibeDeck Player, open Effects and tap NIGHTCORE. The track speeds up and the pitch goes up with it, the way nightcore sounds. Fine-tune the speed, add reverb or bass boost, then record a clip and share it. It works offline on iPhone and iPad, with your own MP3, FLAC and WAV files.',
  alt='VibeDeck Player main screen on iPhone',
  statement='Nightcore is the opposite of slowed + reverb: the song plays faster and higher, so it feels brighter and full of energy. Speed and pitch move together, like a record spun faster. VibeDeck does it in one tap with the NIGHTCORE preset, and you can still shape every part of the sound yourself.',
  features_title='Make it nightcore',
  features=[('One-tap preset', 'Tap NIGHTCORE and the track speeds up with a higher pitch, ready to play.'),
            ('Fine-tune it', 'Move SPEED / PITCH, add reverb, echo, a DJ filter, bass boost or warm saturation.'),
            ('Record and share', 'In Studio, press REC, capture up to 2 minutes with fade in and fade out, and share the clip.')],
  prose='<figure style="margin:0 auto 28px;max-width:320px"><picture><source type="image/avif" srcset="/assets/img/vibedeck-effects-bass-boost-reverb-iphone-360.avif 360w, /assets/img/vibedeck-effects-bass-boost-reverb-iphone-540.avif 540w, /assets/img/vibedeck-effects-bass-boost-reverb-iphone-720.avif 720w" sizes="320px"><source type="image/webp" srcset="/assets/img/vibedeck-effects-bass-boost-reverb-iphone-360.webp 360w, /assets/img/vibedeck-effects-bass-boost-reverb-iphone-540.webp 540w, /assets/img/vibedeck-effects-bass-boost-reverb-iphone-720.webp 720w" sizes="320px"><img src="/assets/img/vibedeck-effects-bass-boost-reverb-iphone-540.webp" alt="VibeDeck Effects panel with the NIGHTCORE, SLOWED + REVERB, DUB DELAY and VINYL DRIVE presets on iPhone" width="540" height="1170" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:24px"></picture></figure><h2>How to make nightcore on iPhone</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store and import your song.</li><li>Play the track and open <strong>Effects</strong>.</li><li>Tap the <strong>NIGHTCORE</strong> preset.</li><li>Want it faster or slower? Move <strong>SPEED / PITCH</strong>. Speed and pitch change together, like a record.</li><li>Add <strong>REVERB</strong>, <strong>BASS BOOST</strong> or <strong>WARM SATURATION</strong> to taste.</li><li>To share it, open the track in <strong>VibeDeck Studio</strong>, press <strong>REC</strong> and record up to two minutes.</li><li>Tap <strong>ORIGINAL</strong> to go back to the normal sound.</li></ol><h2>Other one-tap presets</h2><ul><li><strong>SLOWED + REVERB:</strong> slower, lower, with a long reverb tail.</li><li><strong>DUB DELAY:</strong> echoes that repeat in time with the music.</li><li><strong>VINYL DRIVE:</strong> warm, saturated sound like an old record.</li><li><strong>ORIGINAL:</strong> resets all effects.</li></ul><h2>Good to know</h2><ul><li><strong>Your own files:</strong> VibeDeck plays music files stored on your device, such as MP3, FLAC and WAV. Songs inside streaming apps cannot be opened.</li><li><strong>Offline:</strong> the presets work with no internet.</li><li><strong>Nightcore vs speed only:</strong> in Studio you can also lock the key and change only the tempo, if you want faster without the higher pitch.</li></ul><p>Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The effects, the EQ and the other sound tools need VibeDeck PRO.</p><p>Also see: <a href="/slowed-reverb/">slowed + reverb on your phone</a>, <a href="/bass-booster/">boost bass on iPhone</a>, <a href="/saturation/">saturation effect</a>.</p>',
  faq_title='Nightcore: FAQ',
  faq=[('How do I make a nightcore version of a song on iPhone?', 'Play the song in VibeDeck Player, open Effects and tap NIGHTCORE. The track speeds up and the pitch rises. You can fine-tune the speed and add reverb or bass boost.'),
       ('What is nightcore?', 'Nightcore is a version of a song played faster and at a higher pitch, so it sounds brighter and more energetic.'),
       ('Can I change only the speed, without the higher pitch?', 'Yes. In VibeDeck Studio you can lock the key and change only the tempo.'),
       ('Can I record and share my nightcore version?', 'Yes. In Studio, press REC, record up to two minutes with fade in and fade out, and share the clip.'),
       ('Does it work offline?', 'Yes. The presets work on the music files in your VibeDeck library, with no internet.'),
       ('Can I use songs from streaming apps?', 'No. VibeDeck only opens audio files stored on your device.'),
       ('Is it free?', 'Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The effects, the EQ and the other sound tools need VibeDeck PRO.')],
  related=['/slowed-reverb/', '/bass-booster/', '/saturation/'],
  cta='Faster, higher, brighter. One tap.',
  link_from=('saturation/index.html', 'Also see: <a href="/delay/">', 'nightcore on your phone')),

dict(slug='bpm-detector',
  title='BPM Detector: See the BPM of Every Song | VibeDeck',
  desc='See the BPM of every song in your library on iPhone: VibeDeck shows the exact BPM on the main screen and sorts your queue by tempo. Offline, no ads.',
  crumb='BPM of every song', eyebrow=('Feature', 'BPM'),
  h1='See the BPM of every song.', h1sub='And sort your queue by tempo',
  lede='VibeDeck Player shows the BPM of the track you are playing right on the main screen. In the queue you can sort by BPM: tracks are grouped by tempo range, with the exact BPM on every track. It works offline on iPhone and iPad, with your own MP3, FLAC and WAV files.',
  alt='VibeDeck Player main screen on iPhone with the BPM readout',
  statement='DJs, runners and dancers all ask the same question: how fast is this song? Tapping along or opening a separate BPM app takes time. VibeDeck shows the BPM of every track in your library and lets you line them up by tempo, so the next song always fits.',
  features_title='Tempo at a glance',
  features=[('BPM on the main screen', 'The tempo of the playing track sits next to the waveform.'),
            ('Sort by BPM', 'The queue groups tracks by tempo range, with the exact BPM on every track.'),
            ('Change the tempo', 'In Studio, move the tempo from -100% to +100% and keep the key with key-lock.')],
  prose='<figure style="margin:0 auto 28px;max-width:320px"><picture><source type="image/avif" srcset="/assets/img/vibedeck-studio-dj-pitch-master-tempo-iphone-360.avif 360w, /assets/img/vibedeck-studio-dj-pitch-master-tempo-iphone-540.avif 540w, /assets/img/vibedeck-studio-dj-pitch-master-tempo-iphone-720.avif 720w" sizes="320px"><source type="image/webp" srcset="/assets/img/vibedeck-studio-dj-pitch-master-tempo-iphone-360.webp 360w, /assets/img/vibedeck-studio-dj-pitch-master-tempo-iphone-540.webp 540w, /assets/img/vibedeck-studio-dj-pitch-master-tempo-iphone-720.webp 720w" sizes="320px"><img src="/assets/img/vibedeck-studio-dj-pitch-master-tempo-iphone-540.webp" alt="VibeDeck Studio on iPhone showing the track BPM, classic DJ pitch and master tempo" width="540" height="1170" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:24px"></picture></figure><h2>How to find the BPM of a song</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store and import your music.</li><li>Play a track. The <strong>BPM</strong> appears on the main screen.</li><li>Open the <strong>queue</strong> and sort by <strong>BPM</strong>. Tracks are grouped by tempo range, with the exact BPM on each one.</li><li>Need a different tempo? Open the track in <strong>VibeDeck Studio</strong> and move the tempo. Key-lock keeps the pitch the same.</li></ol><h2>Who uses it</h2><ul><li><strong>DJs:</strong> line up tracks with close tempos and plan smooth transitions.</li><li><strong>Producers:</strong> check the tempo of a reference track before you start.</li><li><strong>Runners and gym:</strong> build a queue that matches your pace.</li><li><strong>Dancers:</strong> find songs at the right speed for practice, then slow them down if needed.</li></ul><h2>Good to know</h2><ul><li><strong>Your own files:</strong> VibeDeck works with music files stored on your device, such as MP3, FLAC and WAV.</li><li><strong>Offline:</strong> no internet is needed.</li><li><strong>Loops on the beat:</strong> Studio loops from half a bar to 8 bars snap to the tempo grid.</li></ul><p>Every new user gets 48 hours with everything unlocked, with no card and no sign-up.</p><p>Also see: <a href="/slow-down-song/">slow down a song without changing pitch</a>, <a href="/dj-loop/">loop part of a song</a>, <a href="/dj-app/">VibeDeck as a DJ app</a>.</p>',
  faq_title='BPM: FAQ',
  faq=[('How do I find the BPM of a song on iPhone?', 'Import the song into VibeDeck Player and play it. The BPM is shown on the main screen.'),
       ('Can I sort my music by BPM?', 'Yes. Sort the queue by BPM: tracks are grouped by tempo range, with the exact BPM on every track.'),
       ('Can I change the BPM of a song?', 'Yes. In VibeDeck Studio, move the tempo from -100% to +100%. Key-lock keeps the pitch the same.'),
       ('Does it work offline?', 'Yes. VibeDeck works with the music files on your device, with no internet.'),
       ('Which files work?', 'Your own audio files, such as MP3, AAC, M4A, WAV, AIFF and FLAC. Songs inside streaming apps cannot be opened.')],
  related=['/slow-down-song/', '/dj-loop/', '/dj-equalizer/'],
  cta='Know the tempo of every track.',
  link_from=('dj-app/index.html', 'Also see: <a href="/dj-equalizer/">', 'BPM of every song')),

dict(slug='whats-new',
  title='What is New in VibeDeck Player: Stems, iPad, Covers',
  desc='What is new in VibeDeck Player 1.0.21: Stems splits any track into acapella and backing, VibeDeck now fits every iPad and iPhone, covers on the lock screen.',
  crumb='What is new', eyebrow=('Updates', '1.0.21'),
  h1='What is new in VibeDeck Player.', h1sub='Version 1.0.21',
  lede='VibeDeck Player 1.0.21 brings Stems: split any track into acapella and backing, mix them live, or open them in Studio and add any effects, then export. VibeDeck now fits every iPad and every iPhone, old and new. Found covers now show on the lock screen too, and you can search a cover for any track.',
  alt='VibeDeck Player main screen on iPhone',
  statement='Every update of VibeDeck comes from the same idea: same track, new feeling. Version 1.0.21 adds the biggest tool so far, Stems, and makes the app fit every screen, from the smallest iPhone to the biggest iPad.',
  features_title='New in 1.0.21',
  features=[('Stems', 'Split any track into acapella and backing. Mix them live, or switch to Studio and add any effects. Export.'),
            ('iPad', 'VibeDeck now fits every iPad and every iPhone, old and new.'),
            ('Covers', 'Found covers now show on the lock screen too. Search a cover for any track.')],
  prose='<figure style="margin:0 auto 28px;max-width:320px"><picture><source type="image/avif" srcset="/assets/img/vibedeck-stems-acapella-backing-iphone-360.avif 360w, /assets/img/vibedeck-stems-acapella-backing-iphone-540.avif 540w, /assets/img/vibedeck-stems-acapella-backing-iphone-720.avif 720w" sizes="320px"><source type="image/webp" srcset="/assets/img/vibedeck-stems-acapella-backing-iphone-360.webp 360w, /assets/img/vibedeck-stems-acapella-backing-iphone-540.webp 540w, /assets/img/vibedeck-stems-acapella-backing-iphone-720.webp 720w" sizes="320px"><img src="/assets/img/vibedeck-stems-acapella-backing-iphone-540.webp" alt="VibeDeck Stems splitting a song into acapella and backing on iPhone" width="540" height="1170" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:24px"></picture></figure><h2>Version 1.0.21</h2><ul><li><strong>Stems:</strong> split any track into acapella and backing, right on your phone. Mix them live, or switch to Studio and add any effects. Export the result.</li><li><strong>iPad:</strong> VibeDeck now fits every iPad and every iPhone, old and new.</li><li><strong>Covers:</strong> found covers now show on the lock screen too. Search a cover for any track.</li><li>Bug fixes and improvements.</li></ul><h2>Version 1.0.20</h2><ul><li><strong>Share many tracks at once:</strong> select a batch of your own tracks, share them to VibeDeck and keep going. They will be in your queue when you get back.</li><li><strong>Sort by BPM:</strong> the queue groups by tempo range, with the exact BPM on every track.</li><li><strong>Pick your waveform:</strong> choose how the now-playing track moves, Needles or Bars.</li><li><strong>Stems has its own home:</strong> find it in Library, under Tools.</li><li><strong>Share from the queue:</strong> send the track you are playing straight from its menu.</li><li><strong>Locked to the beat:</strong> NEXT and the EQ lamp move with your music.</li><li>A brighter Hub, a smoother queue, smoother Studio knobs, and bug fixes.</li></ul><h2>What VibeDeck can do</h2><ul><li><strong>Player:</strong> MP3, AAC, M4A, WAV, AIFF and FLAC offline, with pitch, filter and BPM on the main screen.</li><li><strong>Sound tools:</strong> 3-band DJ EQ or 8-band EQ from 60 Hz to 16 kHz, VibeMod, limiter and mono.</li><li><strong>Effects:</strong> one-tap presets Slowed + Reverb, Nightcore, Dub Delay and Vinyl Drive, plus bass boost, saturation, reverb and echo.</li><li><strong>Studio:</strong> classic DJ pitch, master tempo, beat-synced loops from half a bar to 8 bars, REC.</li><li><strong>Sampler:</strong> record any sound playing on your phone, trim it with fade in and fade out, share it.</li><li><strong>Queue:</strong> drag to reorder, change any cover, night mode.</li></ul><p>Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The effects, the EQ and the other sound tools need VibeDeck PRO.</p><p>Also see: <a href="/vocal-remover/">vocal remover and stem splitter</a>, <a href="/nightcore/">nightcore on your phone</a>, <a href="/bpm-detector/">BPM of every song</a>.</p>',
  faq_title='VibeDeck updates: FAQ',
  faq=[('What is new in VibeDeck Player 1.0.21?', 'Stems splits any track into acapella and backing, VibeDeck now fits every iPad and iPhone, and found covers show on the lock screen too.'),
       ('Does VibeDeck work on iPad?', 'Yes. VibeDeck fits every iPad and every iPhone, old and new.'),
       ('Can VibeDeck remove vocals from a song?', 'Yes. Stems splits a track into acapella and backing on your phone. You can mix them live, add effects in Studio and export.'),
       ('Can I change the cover of a track?', 'Yes. Search a cover for any track, pick one from Photos or keep the original. Found covers also show on the lock screen.'),
       ('How do I get the update?', 'Update VibeDeck Player in the App Store. New users can download it for free.')],
  related=['/vocal-remover/', '/dj-equalizer/', '/sampler/'],
  cta='Same track. New feeling. Update now.',
  link_from=('vocal-remover/index.html', 'Also see: <a href="/slow-down-song/">', 'what is new in VibeDeck')),
]

class Ordered(HTMLFormatter):
    def attributes(self, tag): return tag.attrs.items()


def frag(soup, markup):
    return BeautifulSoup(markup, 'html.parser')


def check(g):
    errors = []
    if len(g['title']) > 60: errors.append(f"title {len(g['title'])}")
    if len(g['desc']) > 160: errors.append(f"desc {len(g['desc'])}")
    text = json.dumps(g, ensure_ascii=False)
    if '—' in text or '–' in text: errors.append('em/en dash')
    for href in g['related']:
        if href not in CARDS: errors.append(f'no card for {href}')
    if errors: sys.exit(f"{g['slug']}: {errors}")


def build(g, template, android_soup):
    check(g)
    slug, url = g['slug'], f"{SITE}/{g['slug']}/"
    soup = copy.deepcopy(template)
    soup.title.string = g['title']
    for sel, val in [('meta[name="description"]', g['desc']), ('meta[property="og:description"]', g['desc']), ('meta[name="twitter:description"]', g['desc']),
                     ('meta[property="og:title"]', g['title']), ('meta[name="twitter:title"]', g['title']), ('meta[property="og:url"]', url)]:
        soup.select_one(sel)['content'] = val
    soup.select_one('link[rel="canonical"]')['href'] = url
    main = soup.find('main')
    main.select_one('.crumbs li[aria-current]').string = g['crumb']
    eyebrow = main.select_one('.hero .eyebrow'); eyebrow.clear()
    eyebrow.append(g['eyebrow'][0] + ' '); dim = soup.new_tag('span', attrs={'class': 'dim'}); dim.string = '/ ' + g['eyebrow'][1]; eyebrow.append(dim)
    main.select_one('#hero-title .h1-plain').string = g['h1']
    main.select_one('#hero-title .h1-sub').string = g['h1sub']
    main.select_one('.hero .lede').string = g['lede']
    if g.get('android'):
        visual = main.select_one('.hero-visual')
        visual.replace_with(copy.deepcopy(android_soup.select_one('.hero-visual')))
        old = soup.select_one('link[rel="preload"][as="image"]')
        old.replace_with(copy.deepcopy(android_soup.select_one('link[rel="preload"][as="image"]')))
    main.select_one('.hero-visual img')['alt'] = g['alt']
    main.select_one('.statement p').string = g['statement']
    main.select_one('#features-title').string = g['features_title']
    for li, (h3, p) in zip(main.select('.panels > li'), g['features']):
        li.h3.string = h3; li.p.string = p
    box = main.select_one('.box.prose'); box.clear(); box.append(frag(soup, g['prose']))
    main.select_one('#faq-title').string = g['faq_title']
    main.select_one('#faq .eyebrow .dim').string = f"/ {len(g['faq']):02d}"
    faq = main.select_one('#faq .faq'); faq.clear()
    for q, a in g['faq']:
        faq.append(frag(soup, f'<details><summary><h3>{q}</h3></summary><div class="a"><p>{a}</p></div></details>'))
    cards = main.select_one('#related .cards'); cards.clear()
    for i, href in enumerate(['/'] + g['related']):
        tag, h3, p = HOME[1:] if href == '/' else CARDS[href]
        cards.append(frag(soup, f'<li data-reveal style="--rd:{i * 90}ms"><a class="card glass" href="{href}"><span class="tag">{tag}</span><h3>{h3}</h3><p>{p}</p><span class="go mono"><span>Open guide</span><span aria-hidden="true">→</span></span></a></li>'))
    main.select_one('#download .lede').string = g['cta']
    for a in soup.select('a[href*="apps.apple.com"], a[href*="play.google.com"]'):
        a['href'] = a['href'].replace('ct=dj-loop', 'ct=' + slug).replace('campaign%3Ddj-loop', 'campaign%3D' + slug)

    script = soup.select_one('script[type="application/ld+json"]')
    graph = json.loads(script.string)
    keep = [n for n in graph['@graph'] if n['@type'] in ('Organization', 'WebSite', 'MobileApplication')]
    image = soup.select_one('meta[property="og:image"]')['content']
    dates = {'datePublished': TODAY, 'dateModified': TODAY}
    graph['@graph'] = [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': g['title'], 'description': g['desc'], 'inLanguage': 'en',
         'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#app'}, 'publisher': {'@id': SITE + '/#org'},
         'primaryImageOfPage': image, **dates},
        {'@type': 'Article', '@id': url + '#article', 'headline': g['h1'], 'description': g['desc'], 'inLanguage': 'en', 'image': image,
         'author': {'@id': SITE + '/#org'}, 'publisher': {'@id': SITE + '/#org'}, 'mainEntityOfPage': {'@id': url + '#webpage'},
         'about': {'@id': SITE + '/#app'}, **dates},
        *keep,
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': g['crumb'], 'item': url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in g['faq']]},
    ]
    script.string = '\n' + json.dumps(graph, ensure_ascii=False, indent=1) + '\n'
    out = ROOT / slug / 'index.html'; out.parent.mkdir(exist_ok=True)
    out.write_text(soup.decode(formatter=Ordered()) + '\n')


def link_in(g):
    rel, anchor, text = g['link_from']
    path = ROOT / rel; s = path.read_text()
    href = f"/{g['slug']}/"
    if f'href="{href}"' in s: return
    assert s.count(anchor) == 1, (rel, anchor)
    label = anchor.split(':')[0]
    s = s.replace(anchor, f'{label}: <a href="{href}">{text}</a>, ' + anchor[len(label) + 2:])
    path.write_text(s)


def extend_sitemap(slugs):
    path = ROOT / 'sitemap.xml'; s = path.read_text()
    add = ''.join(f'  <url>\n    <loc>{SITE}/{slug}/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>0.8</priority>\n  </url>\n'
                  for slug in slugs if f'<loc>{SITE}/{slug}/</loc>' not in s)
    path.write_text(s.replace('</urlset>', add + '</urlset>'))


def main():
    template = BeautifulSoup(TEMPLATE.read_text(), 'html.parser')
    android = BeautifulSoup(ANDROID_HERO.read_text(), 'html.parser')
    only = sys.argv[1:]
    guides = [g for g in GUIDES if not only or g['slug'] in only]
    for g in guides:
        build(g, template, android); link_in(g)
    extend_sitemap([g['slug'] for g in guides])
    print('generated', ', '.join('/' + g['slug'] + '/' for g in guides))


if __name__ == '__main__':
    main()
