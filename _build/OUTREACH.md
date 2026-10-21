# VibeDeck Player: тексты для площадок и инструкции

Файл в папке `_build`, на сайт не публикуется. Тексты на английском готовы к копированию.

---

## 1. Автоотправка в Bing через GitHub (1 минута)

1. Открой https://github.com/YULIY99/vibedeckplayer.app
2. Нажми **Add file → Create new file**.
3. В поле имени файла впиши: `.github/workflows/indexnow.yml`
4. Вставь текст ниже целиком.
5. Нажми **Commit changes…** и ещё раз **Commit changes**.

```yaml
name: IndexNow
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: python3 _build/indexnow.py --wait ${{ github.event.before || 'all' }} ${{ github.sha }}
```

После этого каждое обновление сайта само уходит в Bing, Яндекс и другие поисковики IndexNow.

---

## 2. Product Hunt (обновить свою страницу)

**Name:** VibeDeck Player

**Tagline (60):** Offline FLAC & MP3 player with pitch, tempo and EQ

**Description:**
VibeDeck Player is an offline music player for the files you own: FLAC, WAV and MP3 on iPhone, iPad and Android. Change pitch up to ±8 semitones and tempo separately, shape the sound with EQ, filter and limiter, and watch AURA visuals react to the music. VibeDeck Studio turns any part of a track into a beat-snapped loop and records a 2-minute clip to share. No ads, no account, no tracking.

**First comment (from the maker):**
Hi, I'm Yuliy. I've been a DJ for 25 years, and I wanted one simple thing on my phone: play my own FLAC and MP3 files offline and change the key and the tempo on the fly, without ads or an account. Nothing did all of that, so I built VibeDeck Player. It now also has VibeDeck Studio for loops and short clips. I'm updating it all the time, so tell me what you'd like to see next.

---

## 3. AlternativeTo (alternativeto.net)

Зарегистрируйся, затем **Suggest new application**.

- **Name:** VibeDeck Player
- **Website:** https://vibedeckplayer.app/
- **Platforms:** iPhone, iPad, Android
- **License:** Freemium
- **Categories:** Audio & Music → Music Player
- **Alternative to (выбери в списке):** VLC Media Player, Poweramp, foobar2000, Musicolet, Flacbox, Doppler

> Сравнения на сайте мы не делаем, но здесь так устроена площадка: ты просто отмечаешь, на что VibeDeck похож. Это не текст о конкурентах.

**Short description:**
Offline music player for FLAC, WAV and MP3 with real-time pitch, tempo and EQ. No ads, no account.

**Long description:**
VibeDeck Player plays the music files you already own, offline, on iPhone, iPad and Android. It supports FLAC, WAV and MP3 with no conversion. You can change the key by up to ±8 semitones and the tempo separately, shape the sound with an EQ, bass boost, filter, stereo balance and limiter, and scrub through tracks on the waveform. VibeDeck Studio (iPhone and iPad) makes beat-snapped loops and records clips up to 2 minutes. No ads, no account, no tracking. The core player is free; Premium unlocks the full sound engine.

**Features (tags):** Offline, FLAC support, Equalizer, Pitch shifting, Tempo control, Ad-free, No registration required, Audio visualizer

---

## 4. Reddit

Правила: один пост в одно сообщество, не чаще раза в несколько недель. Отвечай на все комментарии сам. Перед постом прочитай правила сообщества (в r/iosapps и r/androidapps саморекламу разрешают в определённые дни).

### r/iosapps и r/androidapps

**Title:** I'm a DJ and built an offline FLAC/MP3 player with pitch and tempo control, no ads

**Text:**
Hi all. I've been DJing for 25 years and wanted a player for my own files that works offline and lets me change the key and the tempo separately. I couldn't find one without ads or an account, so I made VibeDeck Player.

What it does:
- plays FLAC, WAV and MP3 from your device, no streaming, no conversion
- pitch up to ±8 semitones, tempo separate (good for singing, practice, DJ prep)
- EQ with gain, bass boost, filter, limiter, waveform
- Studio on iPhone/iPad: beat-snapped loops and 2-minute clips
- no ads, no account, no tracking

The core player is free. I'd really like honest feedback: what's missing, what's confusing.

iOS: https://apps.apple.com/app/vibedeck-player/id6784724920
Android: https://play.google.com/store/apps/details?id=com.vibedeck.player

### r/flac (только если правила разрешают)

**Title:** Offline FLAC player for iPhone and Android with EQ and pitch, looking for feedback

**Text:**
I made a player for people who keep their library in FLAC. It plays FLAC, WAV and MP3 offline on iPhone, iPad and Android, no conversion, with an EQ and limiter. It also changes pitch and tempo separately, which I use for practice. No ads, no account. Would love feedback from people who care about lossless playback.

---

## 5. Письмо авторам обзоров «лучшие офлайн-плееры»

Найди в Google статьи вроде "best offline music player iPhone 2026", "best FLAC player Android" и напиши авторам (контакт обычно внизу статьи).

**Subject:** An offline FLAC player for your "best music players" list

Hi [name],

I read your article "[title]" and thought VibeDeck Player might be a good fit for it.

It's an offline music player for iPhone, iPad and Android that plays FLAC, WAV and MP3 with no conversion. Unlike most players, it changes pitch (±8 semitones) and tempo separately, and it has an EQ with a limiter. There are no ads and no account.

Website: https://vibedeckplayer.app/
App Store: https://apps.apple.com/app/vibedeck-player/id6784724920
Google Play: https://play.google.com/store/apps/details?id=com.vibedeck.player

I'm happy to send a Premium code if you'd like to test the full version.

Thanks,
Yuliy Metelskiy
hello@vibedeckplayer.app

---

## 6. Описание для App Store и Google Play на других языках

Сайт теперь на 15 языках. Когда захочешь перевести страницы приложения в магазинах, скажи, на какие языки: подготовлю название, подзаголовок, ключевые слова (App Store) и описание под ограничения каждого магазина.
