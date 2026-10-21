# VibeDeck Player: сайт и SEO

Последнее обновление: 21.10.2026

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
- Без длинных тире в текстах
- Ответы мне: коротко, по-русски

## Что дальше
- После апдейта плеера: обновить функции и скриншоты на всех языках
- Когда выйдет эффект караоке: обновить /karaoke-key-change/ и перевести
- Через неделю: проверить индексацию в Search Console и Bing
- Обновить описание на Product Hunt (текст в `_build/OUTREACH.md`)
