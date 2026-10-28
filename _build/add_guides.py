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
    '/sampler/': ('Sampler', 'Record any sound on your phone', 'Press Rec and record what plays on your phone: YouTube, SoundCloud, any app.'),
    '/dj-loop/': ('DJ · Loop', 'How to loop part of a song', 'Beat-snapped loops from half a bar to 8 bars, tuned to the grid.'),
    '/offline-music-player-iphone/': ('Offline · iPhone', 'Offline music player for iPhone', 'Your whole library on planes and in dead zones. No WiFi needed.'),
    '/offline-music-player-android/': ('Offline · Android', 'Offline music player for Android', 'MP3, FLAC and WAV with no internet, no ads and no account.'),
    '/mp3-player-no-ads/': ('MP3 · No ads', 'MP3 player with no ads', 'Your MP3 files offline, with no account and no ads.'),
    '/play-flac-on-iphone/': ('How-to · FLAC', 'How to play FLAC on iPhone', 'Copy, import, play. No conversion and no internet.'),
    '/put-music-on-iphone-without-itunes/': ('How-to · Import', 'Put music on iPhone without iTunes', 'AirDrop, iCloud Drive and the Files app, step by step.'),
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
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store.</li><li>Copy your FLAC files to the iPhone. From a Mac, select them and send them with AirDrop. From a Windows PC, upload them to iCloud Drive. Any place the Files app shows works too.</li><li>Open VibeDeck Player and import the files from Files, iCloud Drive or Downloads.</li><li>Press play. The music plays offline, with no internet.</li><li>Shape the sound with the EQ, or change pitch and tempo if you practice along.</li></ol><h2>Good to know</h2><ul><li><strong>Storage:</strong> FLAC files are bigger than MP3, so check free space before you copy a large collection.</li><li><strong>Mixed library:</strong> MP3 and WAV play in the same queue as your FLAC files.</li><li><strong>Streaming tracks:</strong> songs inside streaming apps cannot be opened by other apps. VibeDeck plays files you own.</li></ul><p>The core player is free with no ads. VibeDeck Premium unlocks the full sound engine.</p><p>Also see: <a href="/flac-player-iphone/">FLAC player for iPhone</a>, <a href="/audio-formats/">audio formats VibeDeck Player plays</a>.</p>',
  faq_title='Playing FLAC on iPhone: FAQ',
  faq=[('Can iPhone play FLAC files?', 'Yes. iPhone can open FLAC files, but the Music app does not add them to your library. VibeDeck Player imports FLAC files and plays them offline with an EQ, pitch and tempo control.'),
       ('Do I need to convert FLAC to play it on iPhone?', 'No. VibeDeck Player plays FLAC directly, so there is nothing to convert and no quality is lost.'),
       ('How do I get FLAC files onto my iPhone without a cable?', 'Use AirDrop from a Mac, or upload the files to iCloud Drive from any computer. Then import them into VibeDeck Player from the Files app or iCloud Drive.'),
       ('Does FLAC playback work offline?', 'Yes. Once imported, the files are on your iPhone and play without WiFi or mobile data.'),
       ('Is it free?', 'The core player is free and has no ads. VibeDeck Premium is optional and unlocks the full sound engine: pitch and filter, EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.')],
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
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store or Google Play.</li><li>Import the karaoke or instrumental version of the song from your files.</li><li>Play it and open <strong>Pitch</strong>.</li><li>Move it down if the song is too high, up if it is too low.</li><li>Sing a verse and the chorus, then adjust by one semitone until it feels easy.</li></ol><h2>How many semitones?</h2><ul><li><strong>Chorus a little too high:</strong> try −1 to −2.</li><li><strong>A song by a female singer, sung by a man:</strong> try −3 to −5.</li><li><strong>A song by a male singer, sung by a woman:</strong> try +3 to +5.</li><li><strong>Too low and breathy:</strong> try +1 to +2.</li></ul><p>VibeDeck changes the key of the whole track. It does not remove vocals, so use an instrumental or karaoke version of the song for the best result.</p><p>Changing the key (Pitch) is part of VibeDeck Premium. The download is free and has no ads.</p><p>Also see: <a href="/change-song-key-iphone/">change the key of a song on iPhone</a>, <a href="/slow-down-song/">slow down a song without changing pitch</a>.</p>',
  faq_title='Karaoke key change: FAQ',
  faq=[('Can I change the key of a karaoke track on my phone?', 'Yes. Open the track in VibeDeck Player and move Pitch by up to 8 semitones in either direction. The change happens in real time.'),
       ('Will the song get slower or faster?', 'No. Pitch and tempo are independent, so the speed stays the same unless you change the tempo yourself.'),
       ('Does VibeDeck remove the vocals?', 'No. It shifts the key of the whole track. For karaoke, import an instrumental or karaoke version of the song.'),
       ('Is the original file changed?', 'No. The key changes during playback and the file is never modified. Reset returns the track to its original key.'),
       ('Does it work with songs from streaming apps?', 'No. VibeDeck only opens audio files stored on your device, such as MP3, FLAC and WAV.'),
       ('Is key change free?', 'The download is free and has no ads. Changing the key is part of VibeDeck Premium.')],
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
  statement='Slowed + reverb is a simple recipe: the song sits lower and floats in a big room. VibeDeck has no one-tap preset for it. You build the sound yourself from the same tools DJs use, so you decide how dark and how wide it gets.',
  features_title='Build the sound',
  features=[('Lower the pitch', 'Drop the track one to three semitones for that heavier, darker feel.'),
            ('Add space', 'The space effect adds echo-like depth and a soft reverb tail.'),
            ('Record and share', 'Capture up to 2 minutes with fade in and fade out, then share the clip.')],
  prose='<h2>Step by step</h2><ol><li>Install <strong>VibeDeck Player</strong> on iPhone or iPad and import your song.</li><li>Open the track in <strong>VibeDeck Studio</strong>.</li><li>Lower the pitch by one to three semitones.</li><li>Turn up the space effect until the tail sounds right to you.</li><li>Optional: set a beat-snapped loop on your favorite part, from half a bar to 8 bars.</li><li>Press REC, record up to two minutes and share the clip.</li></ol><h2>Tips for the sound</h2><ul><li><strong>Start small:</strong> −2 semitones and a medium amount of space is a good first try.</li><li><strong>Soften the top:</strong> the Studio filter can take the edge off bright highs.</li><li><strong>Add warmth:</strong> a touch of saturation makes the low end feel thicker.</li><li><strong>Slower for listening:</strong> in the main player, tempo changes separately from pitch, so you can also hear the track slower.</li></ul><p>Studio is part of VibeDeck Player on iPhone and iPad. It works with your own files, such as MP3, FLAC and WAV.</p><p>Also see: <a href="/delay/">delay and space effect</a>, <a href="/saturation/">saturation effect</a>, <a href="/dj-loop/">loop part of a song</a>.</p>',
  faq_title='Slowed + reverb: FAQ',
  faq=[('Can I make slowed + reverb on iPhone?', 'Yes. In VibeDeck Studio, lower the pitch and add the space effect, which gives a soft reverb tail. Then record up to two minutes and share the clip.'),
       ('Is there a one-tap slowed + reverb preset?', 'No. You build the sound with pitch and the space effect. It takes a few seconds and you control how deep it goes.'),
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
       ('Does it have ads?', 'No. Neither the free version nor Premium shows ads, and you do not need an account.'),
       ('Is there an iPhone version?', 'Yes. On iPhone and iPad, import songs from the Files app, iCloud Drive or AirDrop.')],
  related=['/offline-music-player-android/', '/flac-player-android/', '/mp3-player-no-ads/'],
  cta='Your Drive music, offline on Android. No ads.',
  link_from=('offline-music-player-android/index.html', 'Related: <a href="/offline-music-player-iphone/">', 'music from Google Drive offline')),

dict(slug='sampler',
  title='Record Internal Audio on iPhone and Android | VibeDeck',
  desc='Record any sound playing on your phone: YouTube, SoundCloud, any app. Edit it on the waveform, then share it, save it as a track or open it in Studio.',
  crumb='VibeDeck Sampler', eyebrow=('Feature', 'Sampler'),
  h1='Record any sound playing on your phone.', h1sub='Press Rec. Play anything. Keep it',
  lede='The VibeDeck Sampler records the sound playing on your phone, straight from the system. Press Rec, switch to YouTube, SoundCloud or any app, and come back when you have what you need. No microphone, no room noise, no computer. On iPhone and Android.',
  alt='VibeDeck Sampler recording system audio on iPhone',
  statement='You hear something great in a video, a stream or a live set, and there is no download button. Holding another phone to the speaker sounds terrible. The Sampler records the sound straight from your phone, clean, while it plays.',
  features_title='Hear it, press Rec, keep it',
  features=[('Any app', 'YouTube, SoundCloud, a browser, a game, a voice message. If your phone plays it, the Sampler records it.'),
            ('Clean system audio', 'AAC 256 kbps, 44.1 kHz, straight from the phone. A live meter shows the sound coming in.'),
            ('Edit on the waveform', 'The recording turns into a waveform. Set the in and out points, add a fade in and out of 0.5, 1 or 2 seconds and preview it.')],
  prose='<h2>How to record sound from your phone</h2><ol><li>Install <strong>VibeDeck Player</strong> from the App Store or Google Play.</li><li>Open VibeDeck and go to <strong>Sampler</strong>.</li><li>Press <strong>Rec</strong>.</li><li>Play the sound in YouTube, SoundCloud or any other app.</li><li>Come back and press <strong>Stop</strong>. The sample appears in Recorded Samples.</li><li>Tap it to edit it on the waveform.</li></ol><h2>What to do with the recording</h2><ul><li><strong>Share:</strong> send it to any app.</li><li><strong>Save to Library:</strong> it becomes a track in All Tracks.</li><li><strong>Open in Studio:</strong> loop it, bend it with pitch, filter, saturation and space, record your version and share it.</li></ul><h2>What people record</h2><ul><li><strong>A moment from a video:</strong> a beat, a line, a sound effect.</li><li><strong>A live stream or DJ set:</strong> the part you want to hear again.</li><li><strong>Raw material for your own sound:</strong> record it, twist it in Studio and post the result.</li><li><strong>Practice material:</strong> a riff or a vocal line to learn, then slow it down or change the key.</li></ul><p>Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The Sampler, Studio, pitch and the other tools need VibeDeck PRO.</p><p>Record only what you have the right to use. Music and videos made by other people are usually protected by copyright.</p><p>Also see: <a href="/slow-down-song/">slow down a song without changing pitch</a>, <a href="/change-song-key-iphone/">change the key of a song on iPhone</a>.</p>',
  faq_title='VibeDeck Sampler: FAQ',
  faq=[('How do I record internal audio on my phone?', 'Open the VibeDeck Sampler, press Rec and play the sound in any app. VibeDeck records the system audio while it plays.'),
       ('Can I record sound from YouTube?', 'Yes. Start recording in VibeDeck, then play the video in YouTube. The sound playing on your phone is recorded.'),
       ('Does it use the microphone?', 'No. It records the system audio, so there is no room noise in the recording.'),
       ('What quality is the recording?', 'AAC, 256 kbps, 44.1 kHz.'),
       ('Does it work on Android?', 'Yes. The Sampler works the same way on iPhone and Android.'),
       ('Is it free?', 'Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays music, also in the background. The Sampler, Studio, pitch and the other tools need VibeDeck PRO.')],
  related=['/slow-down-song/', '/change-song-key-iphone/', '/offline-music-player-iphone/'],
  cta='Hear it. Press Rec. Keep it.',
  link_from=('dj-loop/index.html', 'Also see: <a href="/slow-down-song/">', 'VibeDeck Sampler')),
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
