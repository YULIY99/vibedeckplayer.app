# VibeDeck redesign — SEO checklist (2026-10-01)

## URLs & redirects
- All URLs unchanged: /, 6 landing pages, /support.html, /privacy.html, /terms.html. No redirects needed.
- Added /404.html (noindex). Canonical on every page = self, absolute https.

## Titles (<=60) & descriptions (<=155), unique per page
| Page | Title (chars) | Desc |
|---|---|---|
| / | VibeDeck Player – Offline Music Player for FLAC, MP3 & WAV (58) | 134 |
| /flac-player-iphone/ | FLAC Player for iPhone – Lossless & Offline \| VibeDeck (54) | 149 |
| /offline-music-player-iphone/ | Offline Music Player for iPhone – No WiFi \| VibeDeck (52) | 146 |
| /offline-music-player-android/ | Offline Music Player for Android – No Ads \| VibeDeck (52) | 153 |
| /mp3-player-no-ads/ | MP3 Player With No Ads – Offline, No Account \| VibeDeck (55) | 145 |
| /music-player-pitch-tempo/ | Music Player With Pitch & Tempo Control \| VibeDeck (50) | 151 |
| /vibedeck-vs-vox/ | VibeDeck vs VOX – Offline Music Player Comparison (49) | 140 |
| support / privacy / terms | 44–46 | 131–134 |

## Headings
- Exactly one H1 per page. Home H1 = "Same Track. New Feeling." + "Offline music player for FLAC, MP3 & WAV" inside the same H1.
- Landing H1s keep the original line plus a keyword line. No skipped heading levels (checked).

## Structured data (JSON-LD @graph)
- Organization, WebSite, MobileApplication (MusicApplication; iOS 17+, iPadOS, Android; downloadUrl; offers 0 / 1.99 / 9.99 / 14.99 USD), FAQPage, BreadcrumbList on sub-pages.
- FAQPage is generated from the same data as the visible details/summary FAQ, so the text matches 1:1 (checked). No ratings or reviews.

## Meta
- Kept: canonical, OG, Twitter cards, apple-itunes-app, theme-color (#04070d), google-site-verification, lang="en".
- New 1200x630 OG image. Favicon set: favicon.ico, favicon.svg, 32px PNG, apple-touch-icon 180, manifest 192/512.
- sitemap.xml lastmod updated; robots.txt unchanged.

## Content & internal links
- Home: "Built for…" section with 6 cards to the landing pages; "Why VibeDeck Player?" (~200 words with contextual links); FAQ expanded to 10.
- Each landing page: breadcrumbs + "Keep exploring" (Home + 3 sibling pages); existing inline related links kept.
- Download CTAs above the fold and in the final block on every page.

## Core Web Vitals
- Static HTML, all text in the first response. One deferred JS file (~3 KB), progressive enhancement only.
- Hero image preloaded (AVIF, imagesrcset, fetchpriority=high); everything below the fold is loading="lazy".
- AVIF + WebP via picture, srcset 360–800w, width/height on every img.
- Self-hosted Latin-subset fonts (Inter 25 KB, JetBrains Mono 13 KB), preloaded, font-display: swap.
- Only transform/opacity animations; prefers-reduced-motion disables motion.
- After deploy: verify with PageSpeed Insights and the Rich Results Test.

## Images
- New descriptive filenames in /assets/img/. Old /assets/screens files are kept so indexed image URLs still resolve.
