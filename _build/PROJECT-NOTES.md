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
4. Языки: 15 (en, ja, es, pt-BR, de, fr, it, ru, ko, tr, id, pl, nl, vi, zh-Hant), по 4 страницы
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
5. Внимание: `add_language.py` теперь остановится (изменился французский исходник). Перед новым языком обновить переводы в `translations/` под новую цену и только потом `source.sha256`

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
- 28.10 запрошена индексация в Google: /sampler/ и ru, es, ja, pt-br, de, fr, it, tr, pl. 29.10 запросить ko, id, nl, vi, zh-hant (лимит Google около 10 в день)
- Поставить баннеры (скриншоты Sampler и Trim) на страницы сэмплера, когда владелец пришлёт
