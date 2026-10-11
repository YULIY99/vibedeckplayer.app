# VibeDeck: multilingual SEO architecture (draft, not published)

Underscore folder: Jekyll does not publish this file.

## Rules
- English stays at the root. No existing URL changes, no redirects of English pages.
- New languages live in subfolders: `/ja/`, `/es/`, `/pt-br/`. Slugs are in the local language.
- A language goes live only after its App Store / Google Play listing is localized.
- Each language gets its own small page set built from local demand, not a 1:1 copy of the 19 English pages.
- No IP or browser-language redirects. Visible language switcher only.
- Every localized page is written or reviewed by a native speaker. No machine-only text.

## Tags per page (only between true equivalents)
```html
<html lang="ja">
<link rel="canonical" href="https://vibedeckplayer.app/ja/ongaku-key-henkou/">
<link rel="alternate" hreflang="ja" href="https://vibedeckplayer.app/ja/ongaku-key-henkou/">
<link rel="alternate" hreflang="en" href="https://vibedeckplayer.app/change-song-key-iphone/">
<link rel="alternate" hreflang="x-default" href="https://vibedeckplayer.app/change-song-key-iphone/">
<meta property="og:locale" content="ja_JP">
```
- Canonical always points to the page itself, never to another language.
- hreflang must be reciprocal; `_build/verify_site.py` fails the check otherwise.
- JSON-LD: `inLanguage` per page; store links point to local storefronts (`apps.apple.com/jp/...`, Play `&hl=ja`).
- Sitemap: add `xhtml:link rel="alternate"` entries for each pair (namespace `http://www.w3.org/1999/xhtml`).

## First page sets (hypotheses, confirm with Keyword Planner / Search Console)
| Lang | hreflang | Pages | English equivalent |
|---|---|---|---|
| Japanese | ja | Home; Change song key (karaoke, ear-copy); Change tempo; FLAC player iPhone | /, /change-song-key-iphone/, /slow-down-song/, /flac-player-iphone/ |
| Spanish | es | Home; FLAC player (iPhone/Android); Offline player without ads | /, /flac-player-iphone/, /mp3-player-no-ads/ |
| Portuguese (BR) | pt-BR | Home; Offline player without ads (Android); FLAC player Android | /, /offline-music-player-android/, /flac-player-android/ |

## Measurement
- Google Play referrer per page and language: `utm_campaign=<lang>-<slug>`.
- App Store campaign link `pt=<provider token>&ct=<lang>-<slug>` once the provider token is supplied.
- Search Console: one URL-prefix property per language folder in addition to the domain property.
