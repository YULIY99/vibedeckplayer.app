# VibeDeck Player: сайт и SEO

Последнее обновление: 28.10.2026

## Где что лежит
- Сайт: https://vibedeckplayer.app (GitHub Pages)
- Репозиторий: github.com/YULIY99/vibedeckplayer.app
- Папка на Mac: Documents/GITHUB(VIBEDECK)/vibedeck-site
- Публикация: push в main, сайт обновляется за 1–2 минуты
- Папка `_build` на сайт не попадает (там скрипты и заметки)

## Кабинеты
- Google Search Console: вход через Google, ресурс https://vibedeckplayer.app/
- Bing Webmaster Tools: тот же аккаунт, там же второй сайт (речь в текст)
- Product Hunt: producthunt.com/products/vibedeck-2 (описание устарело, обновить)
- Threads: @vibedeck.studio. Reddit и старый Threads заблокированы
- Пароли сюда не записывать, только в менеджер паролей

## Что сделано 21.10.2026
1. llms.txt и llms-full.txt (справка для ChatGPT и Claude) собираются из страниц автоматически
2. Скрытая разметка (JSON-LD): WebPage, Article, даты, связь с App Store, Google Play, Product Hunt, Threads
3. IndexNow: каждое обновление сайта само уходит в Bing и Яндекс (GitHub Action)
4. Языки: 17 (en, ja, es, pt-BR, de, fr, it, ru, ko, tr, id, pl, nl, vi, zh-Hant, zh-Hans, th), по 4 страницы + «замедлить песню» и Сэмплер
5. 6 английских гайдов: FLAC на iPhone, караоке (смена тональности), slowed + reverb, музыка без iTunes, WAV на iPhone, Google Drive на Android
6. Гайд «замедлить песню» на 14 языках
7. Search Console: запрос индексации, sitemap отправлен заново
8. Скорость: PageSpeed 99/100/100/100
9. Тексты для площадок: `_build/OUTREACH.md`

## Что сделано 24–28.10.2026
1. Счётчик посещений GoatCounter на всех страницах: vibedeck.goatcounter.com (вход у владельца). Скрипт `_build/add_counter.py`
2. Страница Сэмплера `/sampler/` и 14 переводов: запись любого звука с телефона (YouTube, SoundCloud, любое приложение), редактирование по волне, Share, Save to Library, Open in Studio. Источник переводов: `_build/guides_i18n/sampler_src.py`
3. Новая схема цены на всех языках: 48 часов всё открыто без карты, потом бесплатно только слушать музыку (в том числе в фоне, без перемотки по волне), остальное с VibeDeck PRO. Скрипт `_build/update_pricing_text.py`
4. «Premium» переименован в «PRO» везде (`_build/rename_premium.py`)
5. 28.10 добавлены упрощённый китайский (zh-Hans) и тайский (th). `source.sha256` обновлён под текущий французский текст; переводы zh-Hans и th ему соответствуют, старые языки в `translations/` описывают старую цену (для пересборки их не использовать)
6. Блок «Расскажите друзьям» внизу 17 главных страниц: WhatsApp, Telegram, Facebook, X, Threads (+ VK для ru, LINE для ja/th/zh-Hant), почта, «Скопировать ссылку», на телефонах кнопка «Ещё» (системное меню: Instagram, TikTok и т.д.). Нажатия и переходы видны в GoatCounter (share-*, utm_campaign=share). Скрипт `_build/add_share.py`, тексты `_build/share_i18n.json`
7. Сэмплер на сайте: экран Sampler вверху страниц, баннеры превью ссылок на 17 языках (`make_sampler_og.py`), форматы MP3/AAC/WAV до 320 kbps, TikTok, Apple Music не пишется (защита). Блок сэмплера на всех главных перед Studio (`add_home_sampler.py`). После пересборки страниц сэмплера запускать `set_sampler_hero.py` и `make_sampler_og.py`
8. Посты для Threads: шаблон и правила в папке `../threads-posts` (рядом с сайтом)

## Главные скрипты (в `_build`)
- `verify_site.py`: проверка всего сайта перед публикацией
- `add_language.py`: добавить язык (переводы в `translations/`)
- `add_guides.py`: новые английские гайды
- `add_local_guides.py`: перевод гайда на другие языки (`guides_i18n/`)
- `build_llms.py`: пересобрать llms.txt
- `update_dates.py`: даты в sitemap и разметке
- `indexnow.py`: отправить страницы в Bing вручную

## Правила
- Дизайн не менять
- Писать только правду о функциях. Сейчас нет: удаления голоса (караоке), OGG/Opus
- Про новую функцию сначала спросить владельца, как она работает, показать текст и только потом публиковать
- Без длинных тире в текстах
- Ответы мне: коротко, по-русски

## Что дальше
- После апдейта плеера: обновить функции и скриншоты на всех языках
- Когда выйдет эффект караоке: обновить /karaoke-key-change/ и перевести
- Через неделю: проверить индексацию в Search Console и Bing
- Обновить описание на Product Hunt (текст в `_build/OUTREACH.md`)
- 28.10 запрошена индексация в Google: /sampler/ и ru, es, ja, pt-br, de, fr, it, tr, pl. /zh-hans/ тоже отправлена 28.10. 29.10 запросить: /th/, сэмплер ko, id, nl, vi, zh-hant, zh-hans, th; 30.10 остальные подстраницы /zh-hans/ и /th/ (лимит около 11 в день) (лимит Google около 10 в день)
- Поставить баннеры (скриншоты Sampler и Trim) на страницы сэмплера, когда владелец пришлёт
