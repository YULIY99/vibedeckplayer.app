#!/usr/bin/env python3
"""Source of nightcore.json, bpm.json and whats-new.json (localized /nightcore/, /bpm-detector/, /whats-new/).

    python3 _build/guides_i18n/updates_src.py
    python3 _build/add_local_guides.py nightcore && python3 _build/add_local_guides.py bpm && python3 _build/add_local_guides.py whats-new

App labels (Effects, NIGHTCORE, SLOWED + REVERB, DUB DELAY, VINYL DRIVE, ORIGINAL, SPEED / PITCH,
REVERB, BASS BOOST, REC, BPM, Studio, Stems) stay in English because the app is in English.
The price line is the language's line from eq.json. Links go to the same language's pages.
"""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
EQ = {k: v for k, v in json.loads((HERE / 'eq.json').read_text()).items() if not k.startswith('_')}
STEMS = {'ja': '/ja/vocal-bunri/', 'es': '/es/separar-voz-de-cancion/', 'pt-BR': '/pt-br/separar-voz-da-musica/', 'de': '/de/gesang-entfernen/',
         'fr': '/fr/supprimer-voix/', 'it': '/it/rimuovere-voce/', 'ru': '/ru/otdelit-golos-ot-muzyki/', 'ko': '/ko/vocal-bunri/',
         'tr': '/tr/vokal-ayirma/', 'id': '/id/pisahkan-vokal/', 'pl': '/pl/usuwanie-wokalu/', 'nl': '/nl/zang-verwijderen/',
         'vi': '/vi/tach-giong-hat/', 'zh-Hant': '/zh-hant/ren-sheng-fen-li/', 'zh-Hans': '/zh-hans/ren-sheng-fen-li/', 'th': '/th/yaek-siang-rong/'}
ORDER = ['ja', 'es', 'pt-BR', 'de', 'fr', 'it', 'ru', 'ko', 'tr', 'id', 'pl', 'nl', 'vi', 'zh-Hant', 'zh-Hans', 'th']
PRE = {c: '/' + c.lower() + '/' for c in ORDER}
WN = {'ja': 'whats-new', 'es': 'novedades', 'pt-BR': 'novidades', 'de': 'neuigkeiten', 'fr': 'nouveautes', 'it': 'novita',
      'ru': 'chto-novogo', 'ko': 'whats-new', 'tr': 'yenilikler', 'id': 'yang-baru', 'pl': 'nowosci', 'nl': 'nieuw',
      'vi': 'co-gi-moi', 'zh-Hant': 'whats-new', 'zh-Hans': 'whats-new', 'th': 'whats-new'}
SLUG = {'nightcore': lambda c: PRE[c] + 'nightcore/', 'bpm': lambda c: PRE[c] + 'bpm/', 'whats-new': lambda c: PRE[c] + WN[c] + '/'}
BANNER = {'nightcore': 'vibedeck-effects-bass-boost-reverb-iphone', 'bpm': 'vibedeck-studio-dj-pitch-master-tempo-iphone',
          'whats-new': 'vibedeck-stems-acapella-backing-iphone'}
B = lambda t: f'<strong>{t}</strong>'


def price(code):
    return re.search(r'<p>(.*?)</p>', EQ[code]['prose']).group(1)


def figure(kind, alt):
    b = BANNER[kind]; ss = lambda e: ', '.join(f'/assets/img/{b}-{w}.{e} {w}w' for w in (360, 540, 720))
    return (f'<figure style="margin:0 auto 28px;max-width:320px"><picture><source type="image/avif" srcset="{ss("avif")}" sizes="320px">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="320px"><img src="/assets/img/{b}-540.webp" alt="{alt}" width="540" height="1170" '
            'loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:24px"></picture></figure>')


def links(code, text):
    return (text.replace('{eq}', EQ[code]['slug']).replace('{stems}', STEMS[code])
                .replace('{nc}', SLUG['nightcore'](code)).replace('{bpm}', SLUG['bpm'](code)))


def page(kind, code, d):
    prose = figure(kind, d['banner_alt'])
    for h2, tag, items in d['blocks']:
        prose += f'<h2>{h2}</h2><{tag}>' + ''.join(f'<li>{i}</li>' for i in items) + f'</{tag}>'
    prose += f'<p>{price(code)}</p><p>{links(code, d["also"])}</p>'
    return dict(slug=SLUG[kind](code), title=d['title'], desc=d['desc'], crumb=d['crumb'], eyebrow=d['eyebrow'], h1=d['h1'], h1sub=d['h1sub'],
                lede=d['lede'], alt=d['alt'], statement=d['statement'], features_title=d['ft'], features=d['features'],
                prose=prose, faq_title=d['faq_title'], faq=d['faq'] + [[d['free_q'], price(code)]], cta=d['cta'], note=d['note'])


NC, BPM, NEW = {}, {}, {}

# ------------------------------------------------------------------ Russian
NC['ru'] = dict(
    title='Nightcore на iPhone: пресет в одно касание | VibeDeck',
    desc='Сделайте nightcore-версию своей песни на iPhone и iPad: нажмите пресет NIGHTCORE в VibeDeck, трек станет быстрее и выше. Офлайн, без рекламы.',
    crumb='Nightcore', eyebrow=['Эффекты', 'Nightcore'], h1='Nightcore на телефоне в одно касание.', h1sub='Быстрее, выше, ярче',
    lede='Чтобы сделать nightcore, включите песню в VibeDeck Player, откройте Effects и нажмите NIGHTCORE. Трек ускорится, и тон поднимется вместе с ним. Подстройте скорость, добавьте реверб или бас, запишите клип и поделитесь. Работает офлайн на iPhone и iPad с вашими MP3, FLAC и WAV.',
    alt='Главный экран VibeDeck Player на iPhone', banner_alt='Панель Effects в VibeDeck с пресетами NIGHTCORE, SLOWED + REVERB, DUB DELAY и VINYL DRIVE на iPhone',
    statement='Nightcore противоположен slowed + reverb: песня играет быстрее и выше, поэтому звучит ярче и энергичнее. Скорость и тон меняются вместе, как у пластинки на большей скорости. В VibeDeck это одно касание пресета NIGHTCORE, а дальше вы сами настраиваете звук.',
    ft='Сделайте nightcore', features=[['Пресет в одно касание', 'Нажмите NIGHTCORE, и трек ускорится с более высоким тоном.'],
                                       ['Тонкая настройка', 'SPEED / PITCH, реверб, эхо, DJ-фильтр, BASS BOOST и теплая сатурация.'],
                                       ['Запись и шеринг', 'В Studio нажмите REC, запишите до 2 минут с fade in и fade out и поделитесь.']],
    blocks=[('Как сделать nightcore на iPhone', 'ol', ['Установите ' + B('VibeDeck Player') + ' из App Store и добавьте песню.', 'Включите трек и откройте ' + B('Effects') + '.',
             'Нажмите пресет ' + B('NIGHTCORE') + '.', 'Нужно быстрее или медленнее? Двигайте ' + B('SPEED / PITCH') + ': скорость и тон меняются вместе.',
             'Добавьте ' + B('REVERB') + ' или ' + B('BASS BOOST') + ' по вкусу.', 'Чтобы поделиться, откройте трек в ' + B('VibeDeck Studio') + ', нажмите ' + B('REC') + ' и запишите до двух минут.',
             B('ORIGINAL') + ' возвращает обычный звук.']),
            ('Другие пресеты в одно касание', 'ul', [B('SLOWED + REVERB:') + ' медленнее, ниже, с длинным хвостом реверба.', B('DUB DELAY:') + ' эхо в такт музыке.',
             B('VINYL DRIVE:') + ' теплый насыщенный звук, как у старой пластинки.'])],
    also='Также: <a href="{eq}">DJ эквалайзер: 3 и 8 полос</a>, <a href="{stems}">как отделить голос от музыки</a>.',
    faq_title='Nightcore: вопросы и ответы',
    faq=[['Как сделать nightcore-версию песни на iPhone?', 'Включите песню в VibeDeck Player, откройте Effects и нажмите NIGHTCORE. Трек ускорится, тон поднимется. Скорость можно подстроить и добавить реверб или бас.'],
         ['Что такое nightcore?', 'Это версия песни, которая играет быстрее и выше, поэтому звучит ярче и энергичнее.'],
         ['Можно ускорить без повышения тона?', 'Да. В VibeDeck Studio можно зафиксировать тональность и менять только темп.'],
         ['Можно записать и отправить свою версию?', 'Да. В Studio нажмите REC, запишите до двух минут с fade in и fade out и поделитесь клипом.'],
         ['Работает без интернета?', 'Да. Пресеты работают с файлами в вашей библиотеке VibeDeck без интернета.']],
    free_q='Это бесплатно?', cta='Быстрее, выше, ярче. В одно касание.', note='Приложение на английском: откройте Effects и нажмите «NIGHTCORE».')

BPM['ru'] = dict(
    title='BPM каждой песни и сортировка по темпу | VibeDeck',
    desc='Узнайте BPM каждой песни на iPhone: VibeDeck показывает точный BPM на главном экране и сортирует очередь по темпу. Офлайн, без рекламы.',
    crumb='BPM каждой песни', eyebrow=['Функция', 'BPM'], h1='BPM каждой песни.', h1sub='И очередь по темпу',
    lede='VibeDeck Player показывает BPM трека прямо на главном экране. В очереди можно сортировать по BPM: треки группируются по диапазону темпа, у каждого точный BPM. Работает офлайн на iPhone и iPad с вашими MP3, FLAC и WAV.',
    alt='Главный экран VibeDeck Player на iPhone с BPM', banner_alt='VibeDeck Studio на iPhone: BPM трека, классический DJ-питч и master tempo',
    statement='Диджеи, бегуны и танцоры спрашивают одно: какой темп у этой песни? Отстукивать вручную или открывать отдельное приложение долго. VibeDeck показывает BPM каждого трека в библиотеке и выстраивает их по темпу, чтобы следующая песня подходила.',
    ft='Темп сразу видно', features=[['BPM на главном экране', 'Темп играющего трека рядом с волной.'], ['Сортировка по BPM', 'Очередь группирует треки по диапазону темпа, у каждого точный BPM.'],
                                      ['Смена темпа', 'В Studio темп от -100% до +100%, тональность держит key-lock.']],
    blocks=[('Как узнать BPM песни', 'ol', ['Установите ' + B('VibeDeck Player') + ' из App Store и добавьте музыку.', 'Включите трек. ' + B('BPM') + ' появится на главном экране.',
             'Откройте ' + B('очередь') + ' и отсортируйте по ' + B('BPM') + '. Треки группируются по диапазону темпа, у каждого точный BPM.',
             'Нужен другой темп? Откройте трек в ' + B('VibeDeck Studio') + ' и измените темп. Key-lock сохраняет тональность.']),
            ('Кому это нужно', 'ul', [B('Диджеям:') + ' подбирать треки с близким темпом и планировать переходы.', B('Продюсерам:') + ' узнать темп референса перед работой.',
             B('Для бега и зала:') + ' собрать очередь под свой темп.', B('Танцорам:') + ' найти песни нужной скорости для тренировки.'])],
    also='Также: <a href="{nc}">nightcore на телефоне</a>, <a href="{eq}">DJ эквалайзер: 3 и 8 полос</a>.',
    faq_title='BPM: вопросы и ответы',
    faq=[['Как узнать BPM песни на iPhone?', 'Добавьте песню в VibeDeck Player и включите ее. BPM показан на главном экране.'],
         ['Можно отсортировать музыку по BPM?', 'Да. Отсортируйте очередь по BPM: треки группируются по диапазону темпа, у каждого точный BPM.'],
         ['Можно изменить BPM песни?', 'Да. В VibeDeck Studio темп меняется от -100% до +100%. Key-lock сохраняет тональность.'],
         ['Работает без интернета?', 'Да. VibeDeck работает с музыкальными файлами на вашем устройстве без интернета.']],
    free_q='Это бесплатно?', cta='Знайте темп каждого трека.', note='Приложение на английском: темп показан как «BPM».')

NEW['ru'] = dict(
    title='Что нового в VibeDeck Player: Stems, iPad, обложки',
    desc='Что нового в VibeDeck Player 1.0.21: Stems делит любой трек на акапеллу и минус, приложение подходит для любого iPad и iPhone, обложки на экране блокировки.',
    crumb='Что нового', eyebrow=['Обновления', '1.0.21'], h1='Что нового в VibeDeck Player.', h1sub='Версия 1.0.21',
    lede='В VibeDeck Player 1.0.21 появился Stems: любой трек делится на акапеллу и минус, их можно сводить вживую или открыть в Studio, добавить эффекты и экспортировать. VibeDeck теперь подходит для любого iPad и iPhone, старого и нового. Найденные обложки показываются и на экране блокировки, а обложку можно найти для любого трека.',
    alt='Главный экран VibeDeck Player на iPhone', banner_alt='VibeDeck Stems делит песню на акапеллу и минус на iPhone',
    statement='Каждое обновление VibeDeck про одну идею: тот же трек, новое ощущение. Версия 1.0.21 добавляет самый большой инструмент, Stems, и подгоняет приложение под любой экран, от маленького iPhone до большого iPad.',
    ft='Новое в 1.0.21', features=[['Stems', 'Любой трек делится на акапеллу и минус. Сводите вживую или добавьте эффекты в Studio. Экспорт.'],
                                   ['iPad', 'VibeDeck подходит для любого iPad и любого iPhone, старого и нового.'],
                                   ['Обложки', 'Найденные обложки видны и на экране блокировки. Поиск обложки для любого трека.']],
    blocks=[('Версия 1.0.21', 'ul', [B('Stems:') + ' делите любой трек на акапеллу и минус прямо на телефоне, сводите вживую или добавьте эффекты в Studio и экспортируйте.',
             B('iPad:') + ' VibeDeck подходит для любого iPad и iPhone, старого и нового.', B('Обложки:') + ' найденные обложки видны на экране блокировки. Поиск обложки для любого трека.',
             'Исправления и улучшения.']),
            ('Версия 1.0.20', 'ul', [B('Много треков сразу:') + ' выберите пачку своих треков, отправьте их в VibeDeck, и они будут в очереди.',
             B('Сортировка по BPM:') + ' очередь группируется по темпу, у каждого трека точный BPM.', B('Вид волны:') + ' Needles или Bars.',
             B('Stems в библиотеке:') + ' в разделе Tools.', B('Шеринг из очереди:') + ' отправьте играющий трек из его меню.', 'Ярче Hub, плавнее очередь и ручки Studio, исправления.'])],
    also='Также: <a href="{stems}">как отделить голос от музыки</a>, <a href="{nc}">nightcore на телефоне</a>, <a href="{bpm}">BPM каждой песни</a>.',
    faq_title='Обновления VibeDeck: вопросы и ответы',
    faq=[['Что нового в VibeDeck Player 1.0.21?', 'Stems делит любой трек на акапеллу и минус, приложение подходит для любого iPad и iPhone, найденные обложки видны на экране блокировки.'],
         ['VibeDeck работает на iPad?', 'Да. VibeDeck подходит для любого iPad и любого iPhone, старого и нового.'],
         ['VibeDeck может убрать голос из песни?', 'Да. Stems делит трек на акапеллу и минус на телефоне. Их можно свести вживую, добавить эффекты в Studio и экспортировать.'],
         ['Как получить обновление?', 'Обновите VibeDeck Player в App Store. Новые пользователи скачивают его бесплатно.']],
    free_q='Это бесплатно?', cta='Тот же трек. Новое ощущение. Обновитесь.', note='Приложение на английском: Stems находится в Library, раздел Tools.')

# ------------------------------------------------------------------ Japanese
NC['ja'] = dict(
    title='iPhoneでナイトコア: ワンタップのプリセット | VibeDeck',
    desc='iPhoneとiPadで自分の曲をナイトコアに。VibeDeckのNIGHTCOREプリセットをタップするだけで、曲が速く高くなります。オフライン、広告なし。',
    crumb='ナイトコア', eyebrow=['エフェクト', 'Nightcore'], h1='ナイトコアをワンタップで。', h1sub='速く、高く、明るく',
    lede='ナイトコアを作るには、VibeDeck Playerで曲を再生し、Effectsを開いてNIGHTCOREをタップします。曲が速くなり、ピッチも一緒に上がります。スピードを調整し、リバーブや低音を足して、クリップを録音して共有できます。iPhoneとiPadで、手持ちのMP3、FLAC、WAVをオフラインで使えます。',
    alt='iPhoneのVibeDeck Playerメイン画面', banner_alt='iPhoneのVibeDeck Effectsパネル: NIGHTCORE、SLOWED + REVERB、DUB DELAY、VINYL DRIVEのプリセット',
    statement='ナイトコアはslowed + reverbの反対です。曲が速く高く鳴るので、明るくエネルギッシュに聞こえます。レコードを速く回したように、スピードとピッチが一緒に変わります。VibeDeckならNIGHTCOREプリセットをワンタップ。そのあと音は自由に作り込めます。',
    ft='ナイトコアにする', features=[['ワンタップのプリセット', 'NIGHTCOREをタップすると、曲が速く高くなります。'], ['細かく調整', 'SPEED / PITCH、リバーブ、エコー、DJフィルター、BASS BOOST、ウォームサチュレーション。'],
                                    ['録音して共有', 'StudioでRECを押し、フェードイン・アウト付きで最大2分録音して共有。']],
    blocks=[('iPhoneでナイトコアを作る方法', 'ol', ['App Storeから' + B('VibeDeck Player') + 'を入れて曲を取り込みます。', '曲を再生して' + B('Effects') + 'を開きます。', B('NIGHTCORE') + 'プリセットをタップします。',
             '速さを変えたいときは' + B('SPEED / PITCH') + 'を動かします。スピードとピッチは一緒に変わります。', B('REVERB') + 'や' + B('BASS BOOST') + 'をお好みで。',
             '共有するには' + B('VibeDeck Studio') + 'で曲を開き、' + B('REC') + 'で最大2分録音します。', B('ORIGINAL') + 'で元の音に戻ります。']),
            ('ほかのワンタッププリセット', 'ul', [B('SLOWED + REVERB:') + 'ゆっくり低く、長いリバーブ。', B('DUB DELAY:') + '曲のテンポに合ったエコー。', B('VINYL DRIVE:') + '古いレコードのような温かい音。'])],
    also='あわせて読む: <a href="{eq}">3バンドDJ EQと8バンドイコライザー</a>、<a href="{stems}">ボーカルを分離する方法</a>',
    faq_title='ナイトコア: よくある質問',
    faq=[['iPhoneで曲をナイトコアにするには？', 'VibeDeck Playerで曲を再生し、Effectsを開いてNIGHTCOREをタップします。曲が速くなりピッチが上がります。スピードの調整やリバーブ、低音の追加もできます。'],
         ['ナイトコアとは？', '曲を速く、高いピッチで再生したバージョンです。明るくエネルギッシュに聞こえます。'],
         ['ピッチを上げずに速くできますか？', 'はい。VibeDeck Studioではキーを固定してテンポだけ変えられます。'],
         ['録音して共有できますか？', 'はい。StudioでRECを押し、フェードイン・アウト付きで最大2分録音して共有できます。'],
         ['オフラインで使えますか？', 'はい。プリセットはVibeDeckライブラリの音楽ファイルでインターネットなしに使えます。']],
    free_q='無料ですか？', cta='速く、高く、明るく。ワンタップで。', note='アプリの表示は英語です: Effectsを開いて「NIGHTCORE」をタップしてください。')

BPM['ja'] = dict(
    title='曲のBPMを表示、テンポで並べ替え | VibeDeck',
    desc='iPhoneでライブラリの曲のBPMがわかります。VibeDeckはメイン画面に正確なBPMを表示し、キューをテンポで並べ替えます。オフライン、広告なし。',
    crumb='曲のBPM', eyebrow=['機能', 'BPM'], h1='すべての曲のBPMがわかる。', h1sub='キューをテンポ順に',
    lede='VibeDeck Playerはメイン画面に再生中の曲のBPMを表示します。キューはBPMで並べ替えでき、テンポの範囲ごとにまとまり、各曲に正確なBPMが付きます。iPhoneとiPadで、手持ちのMP3、FLAC、WAVをオフラインで使えます。',
    alt='BPM表示のあるiPhoneのVibeDeck Playerメイン画面', banner_alt='iPhoneのVibeDeck Studio: 曲のBPM、クラシックDJピッチ、マスターテンポ',
    statement='DJもランナーもダンサーも同じことを知りたい。この曲のテンポは？ 手でタップしたり別アプリを開いたりは手間です。VibeDeckはライブラリの全曲のBPMを表示し、テンポ順に並べるので、次の曲がぴったり合います。',
    ft='テンポがひと目でわかる', features=[['メイン画面にBPM', '再生中の曲のテンポが波形の横に。'], ['BPMで並べ替え', 'キューがテンポの範囲ごとにまとまり、各曲に正確なBPM。'], ['テンポを変える', 'Studioでテンポを-100%から+100%。key-lockでキーはそのまま。']],
    blocks=[('曲のBPMを調べる方法', 'ol', ['App Storeから' + B('VibeDeck Player') + 'を入れて音楽を取り込みます。', '曲を再生すると、メイン画面に' + B('BPM') + 'が出ます。',
             B('キュー') + 'を開いて' + B('BPM') + 'で並べ替えます。テンポの範囲ごとにまとまり、各曲に正確なBPMが付きます。', 'テンポを変えたいときは' + B('VibeDeck Studio') + 'で曲を開きます。key-lockでキーは変わりません。']),
            ('こんな人に', 'ul', [B('DJ:') + 'テンポの近い曲を並べてつなぎを考える。', B('プロデューサー:') + '制作前にリファレンス曲のテンポを確認。', B('ランニング・ジム:') + 'ペースに合ったキューを作る。', B('ダンサー:') + '練習に合う速さの曲を探す。'])],
    also='あわせて読む: <a href="{nc}">ナイトコアをワンタップで</a>、<a href="{eq}">3バンドDJ EQと8バンドイコライザー</a>',
    faq_title='BPM: よくある質問',
    faq=[['iPhoneで曲のBPMを調べるには？', '曲をVibeDeck Playerに取り込んで再生します。BPMはメイン画面に表示されます。'],
         ['音楽をBPMで並べ替えられますか？', 'はい。キューをBPMで並べ替えると、テンポの範囲ごとにまとまり、各曲に正確なBPMが付きます。'],
         ['曲のBPMを変えられますか？', 'はい。VibeDeck Studioでテンポを-100%から+100%まで変えられます。key-lockでキーはそのままです。'],
         ['オフラインで使えますか？', 'はい。端末の音楽ファイルでインターネットなしに使えます。']],
    free_q='無料ですか？', cta='すべての曲のテンポがわかる。', note='アプリの表示は英語です: テンポは「BPM」と表示されます。')

NEW['ja'] = dict(
    title='VibeDeck Playerの新機能: Stems、iPad、カバー',
    desc='VibeDeck Player 1.0.21の新機能: Stemsで曲をアカペラと伴奏に分離、すべてのiPadとiPhoneに対応、見つけたカバーをロック画面にも表示。',
    crumb='新機能', eyebrow=['アップデート', '1.0.21'], h1='VibeDeck Playerの新機能。', h1sub='バージョン1.0.21',
    lede='VibeDeck Player 1.0.21ではStemsが登場。どんな曲もアカペラと伴奏に分けて、ライブでミックスしたり、Studioでエフェクトをかけて書き出せます。VibeDeckは新旧すべてのiPadとiPhoneに対応しました。見つけたカバーはロック画面にも表示され、どの曲でもカバーを検索できます。',
    alt='iPhoneのVibeDeck Playerメイン画面', banner_alt='iPhoneで曲をアカペラと伴奏に分けるVibeDeck Stems',
    statement='VibeDeckのアップデートはいつも同じ考えから。同じ曲、新しい感覚。1.0.21は最大のツールStemsを加え、小さなiPhoneから大きなiPadまで、どの画面にも合うようになりました。',
    ft='1.0.21の新機能', features=[['Stems', 'どんな曲もアカペラと伴奏に。ライブでミックス、またはStudioでエフェクト。書き出し。'], ['iPad', '新旧すべてのiPadとiPhoneに対応。'], ['カバー', '見つけたカバーをロック画面にも表示。どの曲でもカバーを検索。']],
    blocks=[('バージョン1.0.21', 'ul', [B('Stems:') + 'どんな曲もスマホでアカペラと伴奏に分けて、ライブでミックスするかStudioでエフェクトをかけて書き出せます。', B('iPad:') + '新旧すべてのiPadとiPhoneに対応。',
             B('カバー:') + '見つけたカバーをロック画面にも表示。どの曲でもカバーを検索できます。', '不具合の修正と改善。']),
            ('バージョン1.0.20', 'ul', [B('まとめて共有:') + '自分の曲をまとめて選び、VibeDeckに共有するとキューに入ります。', B('BPMで並べ替え:') + 'キューがテンポごとにまとまり、各曲に正確なBPM。',
             B('波形の選択:') + 'NeedlesかBars。', B('Stemsの場所:') + 'LibraryのToolsの中。', B('キューから共有:') + '再生中の曲をメニューから送れます。', 'Hubがより明るく、キューとStudioのノブがよりなめらかに、不具合の修正。'])],
    also='あわせて読む: <a href="{stems}">ボーカルを分離する方法</a>、<a href="{nc}">ナイトコアをワンタップで</a>、<a href="{bpm}">曲のBPM</a>',
    faq_title='VibeDeckのアップデート: よくある質問',
    faq=[['VibeDeck Player 1.0.21の新機能は？', 'Stemsで曲をアカペラと伴奏に分離、すべてのiPadとiPhoneに対応、見つけたカバーをロック画面にも表示。'],
         ['VibeDeckはiPadで使えますか？', 'はい。新旧すべてのiPadとiPhoneに対応しています。'],
         ['曲からボーカルを消せますか？', 'はい。Stemsでスマホ上で曲をアカペラと伴奏に分けられます。ライブでミックス、Studioでエフェクト、書き出しができます。'],
         ['アップデートの方法は？', 'App StoreでVibeDeck Playerをアップデートしてください。新しく使う人は無料でダウンロードできます。']],
    free_q='無料ですか？', cta='同じ曲、新しい感覚。今すぐアップデート。', note='アプリの表示は英語です: StemsはLibraryのToolsにあります。')

# ------------------------------------------------------------------ Spanish
NC['es'] = dict(
    title='Nightcore en iPhone: preset de un toque | VibeDeck',
    desc='Haz la versión nightcore de tus canciones en iPhone y iPad: toca el preset NIGHTCORE en VibeDeck y la pista sonará más rápida y aguda. Sin anuncios.',
    crumb='Nightcore', eyebrow=['Efectos', 'Nightcore'], h1='Nightcore en tu teléfono, con un toque.', h1sub='Más rápido, más agudo, más brillante',
    lede='Para hacer nightcore, reproduce tu canción en VibeDeck Player, abre Effects y toca NIGHTCORE. La pista se acelera y el tono sube con ella. Ajusta la velocidad, añade reverb o graves, graba un clip y compártelo. Funciona sin conexión en iPhone y iPad con tus MP3, FLAC y WAV.',
    alt='Pantalla principal de VibeDeck Player en iPhone', banner_alt='Panel Effects de VibeDeck con los presets NIGHTCORE, SLOWED + REVERB, DUB DELAY y VINYL DRIVE en iPhone',
    statement='El nightcore es lo contrario del slowed + reverb: la canción suena más rápida y aguda, con más brillo y energía. Velocidad y tono cambian juntos, como un disco girando más rápido. En VibeDeck es un toque en el preset NIGHTCORE, y después ajustas el sonido a tu gusto.',
    ft='Hazlo nightcore', features=[['Preset de un toque', 'Toca NIGHTCORE y la pista se acelera con un tono más agudo.'], ['Ajuste fino', 'SPEED / PITCH, reverb, eco, filtro DJ, BASS BOOST y saturación cálida.'],
                                    ['Graba y comparte', 'En Studio pulsa REC, graba hasta 2 minutos con fade in y fade out y compártelo.']],
    blocks=[('Cómo hacer nightcore en iPhone', 'ol', ['Instala ' + B('VibeDeck Player') + ' desde el App Store e importa tu canción.', 'Reproduce la pista y abre ' + B('Effects') + '.', 'Toca el preset ' + B('NIGHTCORE') + '.',
             '¿Más rápido o más lento? Mueve ' + B('SPEED / PITCH') + ': velocidad y tono cambian juntos.', 'Añade ' + B('REVERB') + ' o ' + B('BASS BOOST') + ' a tu gusto.',
             'Para compartir, abre la pista en ' + B('VibeDeck Studio') + ', pulsa ' + B('REC') + ' y graba hasta dos minutos.', B('ORIGINAL') + ' vuelve al sonido normal.']),
            ('Otros presets de un toque', 'ul', [B('SLOWED + REVERB:') + ' más lento, más grave, con una larga cola de reverb.', B('DUB DELAY:') + ' ecos al ritmo de la música.', B('VINYL DRIVE:') + ' sonido cálido y saturado, como un disco antiguo.'])],
    also='Ver también: <a href="{eq}">ecualizador DJ de 3 y 8 bandas</a>, <a href="{stems}">cómo separar la voz de una canción</a>.',
    faq_title='Nightcore: preguntas frecuentes',
    faq=[['¿Cómo hago una versión nightcore de una canción en iPhone?', 'Reproduce la canción en VibeDeck Player, abre Effects y toca NIGHTCORE. La pista se acelera y el tono sube. Puedes ajustar la velocidad y añadir reverb o graves.'],
         ['¿Qué es el nightcore?', 'Es una versión de una canción más rápida y aguda, que suena más brillante y con más energía.'],
         ['¿Puedo acelerar sin subir el tono?', 'Sí. En VibeDeck Studio puedes fijar la tonalidad y cambiar solo el tempo.'],
         ['¿Puedo grabar y compartir mi versión?', 'Sí. En Studio pulsa REC, graba hasta dos minutos con fade in y fade out y comparte el clip.'],
         ['¿Funciona sin conexión?', 'Sí. Los presets funcionan con los archivos de tu biblioteca de VibeDeck, sin internet.']],
    free_q='¿Es gratis?', cta='Más rápido, más agudo, más brillante. Con un toque.', note='La app está en inglés: abre Effects y toca «NIGHTCORE».')

BPM['es'] = dict(
    title='BPM de cada canción y orden por tempo | VibeDeck',
    desc='Conoce el BPM de cada canción en iPhone: VibeDeck muestra el BPM exacto en la pantalla principal y ordena tu cola por tempo. Sin conexión, sin anuncios.',
    crumb='BPM de cada canción', eyebrow=['Función', 'BPM'], h1='El BPM de cada canción.', h1sub='Y tu cola ordenada por tempo',
    lede='VibeDeck Player muestra el BPM de la pista que suena en la pantalla principal. En la cola puedes ordenar por BPM: las pistas se agrupan por rango de tempo, con el BPM exacto en cada una. Funciona sin conexión en iPhone y iPad con tus MP3, FLAC y WAV.',
    alt='Pantalla principal de VibeDeck Player en iPhone con el BPM', banner_alt='VibeDeck Studio en iPhone con el BPM de la pista, pitch DJ clásico y master tempo',
    statement='DJs, corredores y bailarines se preguntan lo mismo: ¿qué tempo tiene esta canción? Contar a mano o abrir otra app lleva tiempo. VibeDeck muestra el BPM de cada pista de tu biblioteca y las ordena por tempo, para que la siguiente encaje.',
    ft='El tempo de un vistazo', features=[['BPM en la pantalla principal', 'El tempo de la pista que suena, junto a la forma de onda.'], ['Ordenar por BPM', 'La cola agrupa las pistas por rango de tempo, con el BPM exacto en cada una.'],
                                            ['Cambia el tempo', 'En Studio, tempo de -100% a +100% y key-lock para mantener la tonalidad.']],
    blocks=[('Cómo saber el BPM de una canción', 'ol', ['Instala ' + B('VibeDeck Player') + ' desde el App Store e importa tu música.', 'Reproduce una pista. El ' + B('BPM') + ' aparece en la pantalla principal.',
             'Abre la ' + B('cola') + ' y ordena por ' + B('BPM') + '. Las pistas se agrupan por rango de tempo, con el BPM exacto.', '¿Otro tempo? Abre la pista en ' + B('VibeDeck Studio') + ' y cambia el tempo. Key-lock mantiene la tonalidad.']),
            ('Para quién', 'ul', [B('DJs:') + ' juntar pistas con tempos cercanos y planear transiciones.', B('Productores:') + ' conocer el tempo de una referencia antes de empezar.',
             B('Correr y gimnasio:') + ' una cola a tu ritmo.', B('Bailarines:') + ' canciones a la velocidad justa para ensayar.'])],
    also='Ver también: <a href="{nc}">nightcore en tu teléfono</a>, <a href="{eq}">ecualizador DJ de 3 y 8 bandas</a>.',
    faq_title='BPM: preguntas frecuentes',
    faq=[['¿Cómo sé el BPM de una canción en iPhone?', 'Importa la canción en VibeDeck Player y reprodúcela. El BPM aparece en la pantalla principal.'],
         ['¿Puedo ordenar mi música por BPM?', 'Sí. Ordena la cola por BPM: las pistas se agrupan por rango de tempo, con el BPM exacto en cada una.'],
         ['¿Puedo cambiar el BPM de una canción?', 'Sí. En VibeDeck Studio el tempo va de -100% a +100%. Key-lock mantiene la tonalidad.'],
         ['¿Funciona sin conexión?', 'Sí. VibeDeck usa los archivos de música de tu dispositivo, sin internet.']],
    free_q='¿Es gratis?', cta='Conoce el tempo de cada pista.', note='La app está en inglés: el tempo aparece como «BPM».')

NEW['es'] = dict(
    title='Novedades de VibeDeck Player: Stems, iPad, portadas',
    desc='VibeDeck Player 1.0.21: Stems separa cualquier pista en acapella y base, la app se adapta a todo iPad y iPhone y las portadas salen en la pantalla de bloqueo.',
    crumb='Novedades', eyebrow=['Actualizaciones', '1.0.21'], h1='Novedades de VibeDeck Player.', h1sub='Versión 1.0.21',
    lede='VibeDeck Player 1.0.21 trae Stems: separa cualquier pista en acapella y base, mézclalas en vivo o ábrelas en Studio, añade efectos y exporta. VibeDeck ahora se adapta a todo iPad y todo iPhone, viejo y nuevo. Las portadas encontradas también salen en la pantalla de bloqueo, y puedes buscar una portada para cualquier pista.',
    alt='Pantalla principal de VibeDeck Player en iPhone', banner_alt='VibeDeck Stems separa una canción en acapella y base en iPhone',
    statement='Cada actualización de VibeDeck nace de la misma idea: la misma canción, una nueva sensación. La versión 1.0.21 suma la herramienta más grande hasta ahora, Stems, y adapta la app a cualquier pantalla, del iPhone más pequeño al iPad más grande.',
    ft='Nuevo en 1.0.21', features=[['Stems', 'Separa cualquier pista en acapella y base. Mezcla en vivo o añade efectos en Studio. Exporta.'], ['iPad', 'VibeDeck se adapta a todo iPad y todo iPhone, viejo y nuevo.'],
                                    ['Portadas', 'Las portadas encontradas salen también en la pantalla de bloqueo. Busca una portada para cualquier pista.']],
    blocks=[('Versión 1.0.21', 'ul', [B('Stems:') + ' separa cualquier pista en acapella y base en tu teléfono, mézclalas en vivo o añade efectos en Studio y exporta.', B('iPad:') + ' VibeDeck se adapta a todo iPad y iPhone, viejo y nuevo.',
             B('Portadas:') + ' las portadas encontradas salen en la pantalla de bloqueo. Busca una portada para cualquier pista.', 'Correcciones y mejoras.']),
            ('Versión 1.0.20', 'ul', [B('Muchas pistas a la vez:') + ' elige un lote de tus pistas, compártelo con VibeDeck y estará en tu cola.', B('Ordenar por BPM:') + ' la cola se agrupa por tempo, con el BPM exacto en cada pista.',
             B('Forma de onda:') + ' Needles o Bars.', B('Stems en la biblioteca:') + ' en Library, dentro de Tools.', B('Compartir desde la cola:') + ' envía la pista que suena desde su menú.', 'Un Hub más brillante, una cola y perillas de Studio más suaves, y correcciones.'])],
    also='Ver también: <a href="{stems}">cómo separar la voz de una canción</a>, <a href="{nc}">nightcore en tu teléfono</a>, <a href="{bpm}">BPM de cada canción</a>.',
    faq_title='Actualizaciones de VibeDeck: preguntas frecuentes',
    faq=[['¿Qué hay de nuevo en VibeDeck Player 1.0.21?', 'Stems separa cualquier pista en acapella y base, la app se adapta a todo iPad y iPhone y las portadas encontradas salen en la pantalla de bloqueo.'],
         ['¿VibeDeck funciona en iPad?', 'Sí. VibeDeck se adapta a todo iPad y todo iPhone, viejo y nuevo.'],
         ['¿VibeDeck puede quitar la voz de una canción?', 'Sí. Stems separa una pista en acapella y base en tu teléfono. Puedes mezclarlas en vivo, añadir efectos en Studio y exportar.'],
         ['¿Cómo consigo la actualización?', 'Actualiza VibeDeck Player en el App Store. Los nuevos usuarios lo descargan gratis.']],
    free_q='¿Es gratis?', cta='La misma canción. Una nueva sensación. Actualiza.', note='La app está en inglés: Stems está en Library, dentro de Tools.')

# ------------------------------------------------------------------ Portuguese (Brazil)
NC['pt-BR'] = dict(
    title='Nightcore no iPhone: preset de um toque | VibeDeck',
    desc='Faça a versão nightcore das suas músicas no iPhone e iPad: toque no preset NIGHTCORE do VibeDeck e a faixa fica mais rápida e aguda. Offline, sem anúncios.',
    crumb='Nightcore', eyebrow=['Efeitos', 'Nightcore'], h1='Nightcore no seu celular, com um toque.', h1sub='Mais rápido, mais agudo, mais brilhante',
    lede='Para fazer nightcore, toque sua música no VibeDeck Player, abra Effects e toque em NIGHTCORE. A faixa acelera e o tom sobe junto. Ajuste a velocidade, adicione reverb ou graves, grave um clipe e compartilhe. Funciona offline no iPhone e iPad com seus MP3, FLAC e WAV.',
    alt='Tela principal do VibeDeck Player no iPhone', banner_alt='Painel Effects do VibeDeck com os presets NIGHTCORE, SLOWED + REVERB, DUB DELAY e VINYL DRIVE no iPhone',
    statement='Nightcore é o oposto de slowed + reverb: a música toca mais rápida e aguda, com mais brilho e energia. Velocidade e tom mudam juntos, como um disco girando mais rápido. No VibeDeck é um toque no preset NIGHTCORE, e depois você ajusta o som do seu jeito.',
    ft='Deixe nightcore', features=[['Preset de um toque', 'Toque em NIGHTCORE e a faixa acelera com o tom mais agudo.'], ['Ajuste fino', 'SPEED / PITCH, reverb, eco, filtro DJ, BASS BOOST e saturação quente.'],
                                    ['Grave e compartilhe', 'No Studio toque em REC, grave até 2 minutos com fade in e fade out e compartilhe.']],
    blocks=[('Como fazer nightcore no iPhone', 'ol', ['Instale o ' + B('VibeDeck Player') + ' pela App Store e importe sua música.', 'Toque a faixa e abra ' + B('Effects') + '.', 'Toque no preset ' + B('NIGHTCORE') + '.',
             'Mais rápido ou mais lento? Mova ' + B('SPEED / PITCH') + ': velocidade e tom mudam juntos.', 'Adicione ' + B('REVERB') + ' ou ' + B('BASS BOOST') + ' a gosto.',
             'Para compartilhar, abra a faixa no ' + B('VibeDeck Studio') + ', toque em ' + B('REC') + ' e grave até dois minutos.', B('ORIGINAL') + ' volta ao som normal.']),
            ('Outros presets de um toque', 'ul', [B('SLOWED + REVERB:') + ' mais lento, mais grave, com uma longa cauda de reverb.', B('DUB DELAY:') + ' ecos no ritmo da música.', B('VINYL DRIVE:') + ' som quente e saturado, como um disco antigo.'])],
    also='Veja também: <a href="{eq}">equalizador DJ de 3 e 8 bandas</a>, <a href="{stems}">como separar a voz da música</a>.',
    faq_title='Nightcore: perguntas frequentes',
    faq=[['Como faço uma versão nightcore de uma música no iPhone?', 'Toque a música no VibeDeck Player, abra Effects e toque em NIGHTCORE. A faixa acelera e o tom sobe. Dá para ajustar a velocidade e adicionar reverb ou graves.'],
         ['O que é nightcore?', 'É uma versão da música mais rápida e aguda, que soa mais brilhante e com mais energia.'],
         ['Posso acelerar sem subir o tom?', 'Sim. No VibeDeck Studio você pode travar o tom e mudar só o andamento.'],
         ['Posso gravar e compartilhar minha versão?', 'Sim. No Studio toque em REC, grave até dois minutos com fade in e fade out e compartilhe o clipe.'],
         ['Funciona offline?', 'Sim. Os presets funcionam com os arquivos da sua biblioteca do VibeDeck, sem internet.']],
    free_q='É grátis?', cta='Mais rápido, mais agudo, mais brilhante. Com um toque.', note='O app está em inglês: abra Effects e toque em «NIGHTCORE».')

BPM['pt-BR'] = dict(
    title='BPM de cada música e ordem por andamento | VibeDeck',
    desc='Veja o BPM de cada música no iPhone: o VibeDeck mostra o BPM exato na tela principal e ordena sua fila por andamento. Offline, sem anúncios.',
    crumb='BPM de cada música', eyebrow=['Recurso', 'BPM'], h1='O BPM de cada música.', h1sub='E a fila por andamento',
    lede='O VibeDeck Player mostra o BPM da faixa que está tocando na tela principal. Na fila você pode ordenar por BPM: as faixas são agrupadas por faixa de andamento, com o BPM exato em cada uma. Funciona offline no iPhone e iPad com seus MP3, FLAC e WAV.',
    alt='Tela principal do VibeDeck Player no iPhone com o BPM', banner_alt='VibeDeck Studio no iPhone com o BPM da faixa, pitch DJ clássico e master tempo',
    statement='DJs, corredores e dançarinos querem saber a mesma coisa: qual o andamento desta música? Contar na mão ou abrir outro app toma tempo. O VibeDeck mostra o BPM de cada faixa da sua biblioteca e ordena por andamento, para a próxima música encaixar.',
    ft='Andamento num relance', features=[['BPM na tela principal', 'O andamento da faixa que toca, ao lado da forma de onda.'], ['Ordenar por BPM', 'A fila agrupa as faixas por andamento, com o BPM exato em cada uma.'],
                                          ['Mude o andamento', 'No Studio, andamento de -100% a +100% e key-lock para manter o tom.']],
    blocks=[('Como saber o BPM de uma música', 'ol', ['Instale o ' + B('VibeDeck Player') + ' pela App Store e importe suas músicas.', 'Toque uma faixa. O ' + B('BPM') + ' aparece na tela principal.',
             'Abra a ' + B('fila') + ' e ordene por ' + B('BPM') + '. As faixas são agrupadas por andamento, com o BPM exato.', 'Outro andamento? Abra a faixa no ' + B('VibeDeck Studio') + ' e mude. O key-lock mantém o tom.']),
            ('Para quem', 'ul', [B('DJs:') + ' juntar faixas com andamentos próximos e planejar transições.', B('Produtores:') + ' saber o andamento de uma referência antes de começar.',
             B('Corrida e academia:') + ' uma fila no seu ritmo.', B('Dançarinos:') + ' músicas na velocidade certa para ensaiar.'])],
    also='Veja também: <a href="{nc}">nightcore no seu celular</a>, <a href="{eq}">equalizador DJ de 3 e 8 bandas</a>.',
    faq_title='BPM: perguntas frequentes',
    faq=[['Como sei o BPM de uma música no iPhone?', 'Importe a música no VibeDeck Player e toque. O BPM aparece na tela principal.'],
         ['Posso ordenar minhas músicas por BPM?', 'Sim. Ordene a fila por BPM: as faixas são agrupadas por andamento, com o BPM exato em cada uma.'],
         ['Posso mudar o BPM de uma música?', 'Sim. No VibeDeck Studio o andamento vai de -100% a +100%. O key-lock mantém o tom.'],
         ['Funciona offline?', 'Sim. O VibeDeck usa os arquivos de música do seu aparelho, sem internet.']],
    free_q='É grátis?', cta='Saiba o andamento de cada faixa.', note='O app está em inglês: o andamento aparece como «BPM».')

NEW['pt-BR'] = dict(
    title='Novidades do VibeDeck Player: Stems, iPad, capas',
    desc='Novidades do VibeDeck Player 1.0.21: Stems separa qualquer faixa em acapella e base, o app cabe em todo iPad e iPhone e as capas aparecem na tela de bloqueio.',
    crumb='Novidades', eyebrow=['Atualizações', '1.0.21'], h1='Novidades do VibeDeck Player.', h1sub='Versão 1.0.21',
    lede='O VibeDeck Player 1.0.21 traz o Stems: separe qualquer faixa em acapella e base, mixe ao vivo ou abra no Studio, adicione efeitos e exporte. O VibeDeck agora cabe em todo iPad e todo iPhone, antigo e novo. As capas encontradas também aparecem na tela de bloqueio, e você pode buscar uma capa para qualquer faixa.',
    alt='Tela principal do VibeDeck Player no iPhone', banner_alt='VibeDeck Stems separando uma música em acapella e base no iPhone',
    statement='Toda atualização do VibeDeck vem da mesma ideia: a mesma música, uma nova sensação. A versão 1.0.21 traz a maior ferramenta até agora, o Stems, e ajusta o app a qualquer tela, do menor iPhone ao maior iPad.',
    ft='Novo na 1.0.21', features=[['Stems', 'Separe qualquer faixa em acapella e base. Mixe ao vivo ou adicione efeitos no Studio. Exporte.'], ['iPad', 'O VibeDeck cabe em todo iPad e todo iPhone, antigo e novo.'],
                                   ['Capas', 'As capas encontradas aparecem também na tela de bloqueio. Busque uma capa para qualquer faixa.']],
    blocks=[('Versão 1.0.21', 'ul', [B('Stems:') + ' separe qualquer faixa em acapella e base no celular, mixe ao vivo ou adicione efeitos no Studio e exporte.', B('iPad:') + ' o VibeDeck cabe em todo iPad e iPhone, antigo e novo.',
             B('Capas:') + ' as capas encontradas aparecem na tela de bloqueio. Busque uma capa para qualquer faixa.', 'Correções e melhorias.']),
            ('Versão 1.0.20', 'ul', [B('Várias faixas de uma vez:') + ' escolha um lote das suas faixas, compartilhe com o VibeDeck e elas estarão na fila.', B('Ordenar por BPM:') + ' a fila agrupa por andamento, com o BPM exato em cada faixa.',
             B('Forma de onda:') + ' Needles ou Bars.', B('Stems na biblioteca:') + ' em Library, dentro de Tools.', B('Compartilhar da fila:') + ' envie a faixa que toca pelo menu dela.', 'Um Hub mais brilhante, fila e botões do Studio mais suaves, e correções.'])],
    also='Veja também: <a href="{stems}">como separar a voz da música</a>, <a href="{nc}">nightcore no seu celular</a>, <a href="{bpm}">BPM de cada música</a>.',
    faq_title='Atualizações do VibeDeck: perguntas frequentes',
    faq=[['O que há de novo no VibeDeck Player 1.0.21?', 'O Stems separa qualquer faixa em acapella e base, o app cabe em todo iPad e iPhone e as capas encontradas aparecem na tela de bloqueio.'],
         ['O VibeDeck funciona no iPad?', 'Sim. O VibeDeck cabe em todo iPad e todo iPhone, antigo e novo.'],
         ['O VibeDeck tira a voz de uma música?', 'Sim. O Stems separa uma faixa em acapella e base no celular. Dá para mixar ao vivo, adicionar efeitos no Studio e exportar.'],
         ['Como pego a atualização?', 'Atualize o VibeDeck Player na App Store. Novos usuários baixam grátis.']],
    free_q='É grátis?', cta='A mesma música. Uma nova sensação. Atualize.', note='O app está em inglês: o Stems fica em Library, dentro de Tools.')

# ------------------------------------------------------------------ German
NC['de'] = dict(
    title='Nightcore auf dem iPhone: Preset mit einem Tipp | VibeDeck',
    desc='Mach Nightcore aus deinen Songs auf iPhone und iPad: Tippe in VibeDeck auf das Preset NIGHTCORE, der Track wird schneller und höher. Offline, ohne Werbung.',
    crumb='Nightcore', eyebrow=['Effekte', 'Nightcore'], h1='Nightcore auf dem Handy, mit einem Tipp.', h1sub='Schneller, höher, heller',
    lede='Für Nightcore spielst du deinen Song in VibeDeck Player ab, öffnest Effects und tippst auf NIGHTCORE. Der Track wird schneller und die Tonhöhe steigt mit. Passe das Tempo an, füge Hall oder Bass hinzu, nimm einen Clip auf und teile ihn. Funktioniert offline auf iPhone und iPad mit deinen MP3, FLAC und WAV.',
    alt='Hauptbildschirm von VibeDeck Player auf dem iPhone', banner_alt='VibeDeck Effects auf dem iPhone mit den Presets NIGHTCORE, SLOWED + REVERB, DUB DELAY und VINYL DRIVE',
    statement='Nightcore ist das Gegenteil von Slowed + Reverb: Der Song läuft schneller und höher und klingt heller und energiegeladener. Tempo und Tonhöhe ändern sich zusammen, wie bei einer schneller gedrehten Platte. In VibeDeck ist das ein Tipp auf NIGHTCORE, danach formst du den Sound selbst.',
    ft='Mach es Nightcore', features=[['Preset mit einem Tipp', 'Tippe auf NIGHTCORE, und der Track wird schneller und höher.'], ['Feinschliff', 'SPEED / PITCH, Hall, Echo, DJ-Filter, BASS BOOST und warme Sättigung.'],
                                      ['Aufnehmen und teilen', 'Im Studio REC drücken, bis zu 2 Minuten mit Fade-in und Fade-out aufnehmen und teilen.']],
    blocks=[('So machst du Nightcore auf dem iPhone', 'ol', ['Installiere ' + B('VibeDeck Player') + ' aus dem App Store und importiere deinen Song.', 'Spiele den Track ab und öffne ' + B('Effects') + '.', 'Tippe auf das Preset ' + B('NIGHTCORE') + '.',
             'Schneller oder langsamer? Verschiebe ' + B('SPEED / PITCH') + ': Tempo und Tonhöhe ändern sich zusammen.', 'Füge nach Geschmack ' + B('REVERB') + ' oder ' + B('BASS BOOST') + ' hinzu.',
             'Zum Teilen öffne den Track im ' + B('VibeDeck Studio') + ', drücke ' + B('REC') + ' und nimm bis zu zwei Minuten auf.', B('ORIGINAL') + ' setzt alle Effekte zurück.']),
            ('Weitere Presets mit einem Tipp', 'ul', [B('SLOWED + REVERB:') + ' langsamer, tiefer, mit langer Hallfahne.', B('DUB DELAY:') + ' Echos im Takt der Musik.', B('VINYL DRIVE:') + ' warmer, gesättigter Klang wie eine alte Platte.'])],
    also='Siehe auch: <a href="{eq}">DJ-Equalizer mit 3 und 8 Bändern</a>, <a href="{stems}">Gesang aus einem Song entfernen</a>.',
    faq_title='Nightcore: häufige Fragen',
    faq=[['Wie mache ich eine Nightcore-Version eines Songs auf dem iPhone?', 'Spiele den Song in VibeDeck Player ab, öffne Effects und tippe auf NIGHTCORE. Der Track wird schneller und höher. Du kannst das Tempo anpassen und Hall oder Bass hinzufügen.'],
         ['Was ist Nightcore?', 'Eine schnellere und höhere Version eines Songs, die heller und energiegeladener klingt.'],
         ['Kann ich schneller machen, ohne dass es höher klingt?', 'Ja. Im VibeDeck Studio kannst du die Tonart festhalten und nur das Tempo ändern.'],
         ['Kann ich meine Version aufnehmen und teilen?', 'Ja. Im Studio REC drücken, bis zu zwei Minuten mit Fade-in und Fade-out aufnehmen und den Clip teilen.'],
         ['Funktioniert es offline?', 'Ja. Die Presets funktionieren mit den Dateien in deiner VibeDeck-Bibliothek, ohne Internet.']],
    free_q='Ist es kostenlos?', cta='Schneller, höher, heller. Mit einem Tipp.', note='Die App ist auf Englisch: öffne Effects und tippe auf «NIGHTCORE».')

BPM['de'] = dict(
    title='BPM jedes Songs und Sortierung nach Tempo | VibeDeck',
    desc='Sieh die BPM jedes Songs auf dem iPhone: VibeDeck zeigt die genauen BPM auf dem Hauptbildschirm und sortiert die Warteschlange nach Tempo. Ohne Werbung.',
    crumb='BPM jedes Songs', eyebrow=['Funktion', 'BPM'], h1='Die BPM jedes Songs.', h1sub='Und die Warteschlange nach Tempo',
    lede='VibeDeck Player zeigt die BPM des laufenden Tracks direkt auf dem Hauptbildschirm. In der Warteschlange sortierst du nach BPM: Die Tracks werden nach Tempobereich gruppiert, jeder mit seinen genauen BPM. Funktioniert offline auf iPhone und iPad mit deinen MP3, FLAC und WAV.',
    alt='Hauptbildschirm von VibeDeck Player auf dem iPhone mit BPM-Anzeige', banner_alt='VibeDeck Studio auf dem iPhone mit Track-BPM, klassischem DJ-Pitch und Master Tempo',
    statement='DJs, Läufer und Tänzer fragen dasselbe: Wie schnell ist dieser Song? Mitklopfen oder eine eigene BPM-App kostet Zeit. VibeDeck zeigt die BPM jedes Tracks deiner Bibliothek und ordnet sie nach Tempo, damit der nächste Song passt.',
    ft='Tempo auf einen Blick', features=[['BPM auf dem Hauptbildschirm', 'Das Tempo des laufenden Tracks neben der Wellenform.'], ['Nach BPM sortieren', 'Die Warteschlange gruppiert nach Tempobereich, mit genauen BPM für jeden Track.'],
                                          ['Tempo ändern', 'Im Studio Tempo von -100% bis +100%, Key-Lock hält die Tonart.']],
    blocks=[('So findest du die BPM eines Songs', 'ol', ['Installiere ' + B('VibeDeck Player') + ' aus dem App Store und importiere deine Musik.', 'Spiele einen Track ab. Die ' + B('BPM') + ' erscheinen auf dem Hauptbildschirm.',
             'Öffne die ' + B('Warteschlange') + ' und sortiere nach ' + B('BPM') + '. Die Tracks werden nach Tempobereich gruppiert, mit genauen BPM.', 'Anderes Tempo? Öffne den Track im ' + B('VibeDeck Studio') + ' und ändere es. Key-Lock hält die Tonart.']),
            ('Für wen', 'ul', [B('DJs:') + ' Tracks mit ähnlichem Tempo zusammenstellen und Übergänge planen.', B('Produzenten:') + ' das Tempo eines Referenztracks prüfen.',
             B('Laufen und Gym:') + ' eine Warteschlange in deinem Tempo.', B('Tänzer:') + ' Songs in der richtigen Geschwindigkeit zum Üben.'])],
    also='Siehe auch: <a href="{nc}">Nightcore auf dem Handy</a>, <a href="{eq}">DJ-Equalizer mit 3 und 8 Bändern</a>.',
    faq_title='BPM: häufige Fragen',
    faq=[['Wie finde ich die BPM eines Songs auf dem iPhone?', 'Importiere den Song in VibeDeck Player und spiele ihn ab. Die BPM stehen auf dem Hauptbildschirm.'],
         ['Kann ich meine Musik nach BPM sortieren?', 'Ja. Sortiere die Warteschlange nach BPM: Die Tracks werden nach Tempobereich gruppiert, mit genauen BPM für jeden Track.'],
         ['Kann ich die BPM eines Songs ändern?', 'Ja. Im VibeDeck Studio geht das Tempo von -100% bis +100%. Key-Lock hält die Tonart.'],
         ['Funktioniert es offline?', 'Ja. VibeDeck nutzt die Musikdateien auf deinem Gerät, ohne Internet.']],
    free_q='Ist es kostenlos?', cta='Kenne das Tempo jedes Tracks.', note='Die App ist auf Englisch: das Tempo steht als «BPM».')

NEW['de'] = dict(
    title='Neu in VibeDeck Player: Stems, iPad, Cover',
    desc='VibeDeck Player 1.0.21: Stems trennt jeden Track in Acapella und Begleitung, die App passt auf jedes iPad und iPhone, Cover auf dem Sperrbildschirm.',
    crumb='Neuigkeiten', eyebrow=['Updates', '1.0.21'], h1='Neu in VibeDeck Player.', h1sub='Version 1.0.21',
    lede='VibeDeck Player 1.0.21 bringt Stems: Trenne jeden Track in Acapella und Begleitung, mische sie live oder öffne sie im Studio, füge Effekte hinzu und exportiere. VibeDeck passt jetzt auf jedes iPad und jedes iPhone, alt und neu. Gefundene Cover erscheinen auch auf dem Sperrbildschirm, und du kannst für jeden Track ein Cover suchen.',
    alt='Hauptbildschirm von VibeDeck Player auf dem iPhone', banner_alt='VibeDeck Stems trennt einen Song in Acapella und Begleitung auf dem iPhone',
    statement='Jedes VibeDeck-Update folgt derselben Idee: derselbe Track, ein neues Gefühl. Version 1.0.21 bringt das bisher größte Werkzeug, Stems, und passt die App an jeden Bildschirm an, vom kleinsten iPhone bis zum größten iPad.',
    ft='Neu in 1.0.21', features=[['Stems', 'Trenne jeden Track in Acapella und Begleitung. Live mischen oder im Studio Effekte hinzufügen. Exportieren.'], ['iPad', 'VibeDeck passt auf jedes iPad und jedes iPhone, alt und neu.'],
                                  ['Cover', 'Gefundene Cover erscheinen auch auf dem Sperrbildschirm. Cover-Suche für jeden Track.']],
    blocks=[('Version 1.0.21', 'ul', [B('Stems:') + ' trenne jeden Track auf dem Handy in Acapella und Begleitung, mische live oder füge im Studio Effekte hinzu und exportiere.', B('iPad:') + ' VibeDeck passt auf jedes iPad und iPhone, alt und neu.',
             B('Cover:') + ' gefundene Cover erscheinen auf dem Sperrbildschirm. Cover-Suche für jeden Track.', 'Fehlerbehebungen und Verbesserungen.']),
            ('Version 1.0.20', 'ul', [B('Viele Tracks auf einmal:') + ' wähle einen Stapel deiner Tracks, teile ihn mit VibeDeck, und sie sind in deiner Warteschlange.', B('Nach BPM sortieren:') + ' die Warteschlange gruppiert nach Tempo, mit genauen BPM.',
             B('Wellenform wählen:') + ' Needles oder Bars.', B('Stems in der Bibliothek:') + ' in Library unter Tools.', B('Teilen aus der Warteschlange:') + ' sende den laufenden Track aus seinem Menü.', 'Ein hellerer Hub, flüssigere Warteschlange und Studio-Regler, Fehlerbehebungen.'])],
    also='Siehe auch: <a href="{stems}">Gesang aus einem Song entfernen</a>, <a href="{nc}">Nightcore auf dem Handy</a>, <a href="{bpm}">BPM jedes Songs</a>.',
    faq_title='VibeDeck-Updates: häufige Fragen',
    faq=[['Was ist neu in VibeDeck Player 1.0.21?', 'Stems trennt jeden Track in Acapella und Begleitung, die App passt auf jedes iPad und iPhone, und gefundene Cover erscheinen auf dem Sperrbildschirm.'],
         ['Funktioniert VibeDeck auf dem iPad?', 'Ja. VibeDeck passt auf jedes iPad und jedes iPhone, alt und neu.'],
         ['Kann VibeDeck den Gesang aus einem Song entfernen?', 'Ja. Stems trennt einen Track auf dem Handy in Acapella und Begleitung. Du kannst live mischen, im Studio Effekte hinzufügen und exportieren.'],
         ['Wie bekomme ich das Update?', 'Aktualisiere VibeDeck Player im App Store. Neue Nutzer laden es kostenlos.']],
    free_q='Ist es kostenlos?', cta='Derselbe Track. Ein neues Gefühl. Jetzt aktualisieren.', note='Die App ist auf Englisch: Stems findest du in Library unter Tools.')

# ------------------------------------------------------------------ French
NC['fr'] = dict(
    title='Nightcore sur iPhone : preset en un geste | VibeDeck',
    desc='Nightcore sur iPhone et iPad : touchez le preset NIGHTCORE dans VibeDeck, votre morceau devient plus rapide et plus aigu. Hors ligne, sans pub.',
    crumb='Nightcore', eyebrow=['Effets', 'Nightcore'], h1='Le nightcore sur votre téléphone, en un geste.', h1sub='Plus rapide, plus aigu, plus brillant',
    lede='Pour faire du nightcore, lancez votre morceau dans VibeDeck Player, ouvrez Effects et touchez NIGHTCORE. Le titre accélère et la hauteur monte avec lui. Ajustez la vitesse, ajoutez de la réverb ou des basses, enregistrez un extrait et partagez-le. Fonctionne hors ligne sur iPhone et iPad avec vos MP3, FLAC et WAV.',
    alt='Écran principal de VibeDeck Player sur iPhone', banner_alt='Panneau Effects de VibeDeck avec les presets NIGHTCORE, SLOWED + REVERB, DUB DELAY et VINYL DRIVE sur iPhone',
    statement='Le nightcore est l’inverse du slowed + reverb : le morceau joue plus vite et plus aigu, il sonne plus brillant et plus énergique. Vitesse et hauteur changent ensemble, comme un vinyle qui tourne plus vite. Dans VibeDeck, c’est un geste sur le preset NIGHTCORE, puis vous façonnez le son à votre goût.',
    ft='Passez en nightcore', features=[['Preset en un geste', 'Touchez NIGHTCORE et le titre accélère avec une hauteur plus aiguë.'], ['Réglage fin', 'SPEED / PITCH, réverb, écho, filtre DJ, BASS BOOST et saturation chaude.'],
                                        ['Enregistrez et partagez', 'Dans Studio, touchez REC, enregistrez jusqu’à 2 minutes avec fondu d’entrée et de sortie, puis partagez.']],
    blocks=[('Comment faire du nightcore sur iPhone', 'ol', ['Installez ' + B('VibeDeck Player') + ' depuis l’App Store et importez votre morceau.', 'Lancez le titre et ouvrez ' + B('Effects') + '.', 'Touchez le preset ' + B('NIGHTCORE') + '.',
             'Plus vite ou plus lent ? Déplacez ' + B('SPEED / PITCH') + ' : vitesse et hauteur changent ensemble.', 'Ajoutez ' + B('REVERB') + ' ou ' + B('BASS BOOST') + ' selon vos goûts.',
             'Pour partager, ouvrez le titre dans ' + B('VibeDeck Studio') + ', touchez ' + B('REC') + ' et enregistrez jusqu’à deux minutes.', B('ORIGINAL') + ' revient au son normal.']),
            ('Autres presets en un geste', 'ul', [B('SLOWED + REVERB :') + ' plus lent, plus grave, avec une longue queue de réverb.', B('DUB DELAY :') + ' des échos en rythme avec la musique.', B('VINYL DRIVE :') + ' un son chaud et saturé, comme un vieux vinyle.'])],
    also='À voir aussi : <a href="{eq}">égaliseur DJ 3 et 8 bandes</a>, <a href="{stems}">supprimer la voix d’une chanson</a>.',
    faq_title='Nightcore : questions fréquentes',
    faq=[['Comment faire une version nightcore d’une chanson sur iPhone ?', 'Lancez la chanson dans VibeDeck Player, ouvrez Effects et touchez NIGHTCORE. Le titre accélère et la hauteur monte. Vous pouvez ajuster la vitesse et ajouter de la réverb ou des basses.'],
         ['Qu’est-ce que le nightcore ?', 'C’est une version d’une chanson plus rapide et plus aiguë, qui sonne plus brillante et plus énergique.'],
         ['Puis-je accélérer sans monter la hauteur ?', 'Oui. Dans VibeDeck Studio, vous pouvez bloquer la tonalité et changer seulement le tempo.'],
         ['Puis-je enregistrer et partager ma version ?', 'Oui. Dans Studio, touchez REC, enregistrez jusqu’à deux minutes avec fondus et partagez l’extrait.'],
         ['Cela fonctionne hors ligne ?', 'Oui. Les presets fonctionnent avec les fichiers de votre bibliothèque VibeDeck, sans internet.']],
    free_q='Est-ce gratuit ?', cta='Plus rapide, plus aigu, plus brillant. En un geste.', note='L’app est en anglais : ouvrez Effects et touchez « NIGHTCORE ».')

BPM['fr'] = dict(
    title='BPM de chaque morceau et tri par tempo | VibeDeck',
    desc='Voyez le BPM de chaque morceau sur iPhone : VibeDeck affiche le BPM exact sur l’écran principal et trie votre file d’attente par tempo. Hors ligne, sans pub.',
    crumb='BPM de chaque morceau', eyebrow=['Fonction', 'BPM'], h1='Le BPM de chaque morceau.', h1sub='Et la file triée par tempo',
    lede='VibeDeck Player affiche le BPM du titre en cours directement sur l’écran principal. Dans la file d’attente, vous pouvez trier par BPM : les titres sont regroupés par plage de tempo, avec le BPM exact sur chacun. Fonctionne hors ligne sur iPhone et iPad avec vos MP3, FLAC et WAV.',
    alt='Écran principal de VibeDeck Player sur iPhone avec le BPM', banner_alt='VibeDeck Studio sur iPhone avec le BPM du titre, le pitch DJ classique et le master tempo',
    statement='DJ, coureurs et danseurs se posent la même question : quel est le tempo de ce morceau ? Taper le rythme ou ouvrir une autre app prend du temps. VibeDeck affiche le BPM de chaque titre de votre bibliothèque et les classe par tempo, pour que le suivant s’enchaîne bien.',
    ft='Le tempo d’un coup d’œil', features=[['BPM sur l’écran principal', 'Le tempo du titre en cours, à côté de la forme d’onde.'], ['Trier par BPM', 'La file regroupe les titres par plage de tempo, avec le BPM exact de chacun.'],
                                            ['Changer le tempo', 'Dans Studio, tempo de -100 % à +100 %, et key-lock garde la tonalité.']],
    blocks=[('Comment connaître le BPM d’un morceau', 'ol', ['Installez ' + B('VibeDeck Player') + ' depuis l’App Store et importez votre musique.', 'Lancez un titre. Le ' + B('BPM') + ' apparaît sur l’écran principal.',
             'Ouvrez la ' + B('file d’attente') + ' et triez par ' + B('BPM') + '. Les titres sont regroupés par plage de tempo, avec le BPM exact.', 'Un autre tempo ? Ouvrez le titre dans ' + B('VibeDeck Studio') + ' et changez-le. Key-lock garde la tonalité.']),
            ('Pour qui', 'ul', [B('DJ :') + ' rapprocher des titres au tempo proche et préparer les transitions.', B('Producteurs :') + ' vérifier le tempo d’une référence avant de commencer.',
             B('Course et salle :') + ' une file à votre rythme.', B('Danseurs :') + ' des morceaux à la bonne vitesse pour répéter.'])],
    also='À voir aussi : <a href="{nc}">le nightcore sur votre téléphone</a>, <a href="{eq}">égaliseur DJ 3 et 8 bandes</a>.',
    faq_title='BPM : questions fréquentes',
    faq=[['Comment connaître le BPM d’une chanson sur iPhone ?', 'Importez la chanson dans VibeDeck Player et lancez-la. Le BPM s’affiche sur l’écran principal.'],
         ['Puis-je trier ma musique par BPM ?', 'Oui. Triez la file par BPM : les titres sont regroupés par plage de tempo, avec le BPM exact de chacun.'],
         ['Puis-je changer le BPM d’une chanson ?', 'Oui. Dans VibeDeck Studio, le tempo va de -100 % à +100 %. Key-lock garde la tonalité.'],
         ['Cela fonctionne hors ligne ?', 'Oui. VibeDeck utilise les fichiers musicaux de votre appareil, sans internet.']],
    free_q='Est-ce gratuit ?', cta='Connaissez le tempo de chaque titre.', note='L’app est en anglais : le tempo s’affiche « BPM ».')

NEW['fr'] = dict(
    title='Nouveautés de VibeDeck Player : Stems, iPad, pochettes',
    desc='VibeDeck Player 1.0.21 : Stems sépare tout titre en acapella et instrumental, l’app s’adapte à chaque iPad et iPhone, pochettes sur l’écran verrouillé.',
    crumb='Nouveautés', eyebrow=['Mises à jour', '1.0.21'], h1='Les nouveautés de VibeDeck Player.', h1sub='Version 1.0.21',
    lede='VibeDeck Player 1.0.21 apporte Stems : séparez n’importe quel titre en acapella et instrumental, mixez-les en direct ou ouvrez-les dans Studio, ajoutez des effets et exportez. VibeDeck s’adapte maintenant à chaque iPad et chaque iPhone, anciens et récents. Les pochettes trouvées s’affichent aussi sur l’écran verrouillé, et vous pouvez chercher une pochette pour n’importe quel titre.',
    alt='Écran principal de VibeDeck Player sur iPhone', banner_alt='VibeDeck Stems sépare une chanson en acapella et instrumental sur iPhone',
    statement='Chaque mise à jour de VibeDeck part de la même idée : le même morceau, une nouvelle sensation. La version 1.0.21 ajoute l’outil le plus important à ce jour, Stems, et adapte l’app à tous les écrans, du plus petit iPhone au plus grand iPad.',
    ft='Nouveau dans la 1.0.21', features=[['Stems', 'Séparez tout titre en acapella et instrumental. Mixez en direct ou ajoutez des effets dans Studio. Exportez.'], ['iPad', 'VibeDeck s’adapte à chaque iPad et chaque iPhone, anciens et récents.'],
                                          ['Pochettes', 'Les pochettes trouvées s’affichent aussi sur l’écran verrouillé. Recherche de pochette pour tout titre.']],
    blocks=[('Version 1.0.21', 'ul', [B('Stems :') + ' séparez tout titre en acapella et instrumental sur votre téléphone, mixez en direct ou ajoutez des effets dans Studio et exportez.', B('iPad :') + ' VibeDeck s’adapte à chaque iPad et iPhone, anciens et récents.',
             B('Pochettes :') + ' les pochettes trouvées s’affichent sur l’écran verrouillé. Recherche de pochette pour tout titre.', 'Corrections et améliorations.']),
            ('Version 1.0.20', 'ul', [B('Plusieurs titres d’un coup :') + ' choisissez un lot de vos titres, partagez-le avec VibeDeck, et ils seront dans votre file.', B('Tri par BPM :') + ' la file se regroupe par tempo, avec le BPM exact de chaque titre.',
             B('Forme d’onde :') + ' Needles ou Bars.', B('Stems dans la bibliothèque :') + ' dans Library, sous Tools.', B('Partage depuis la file :') + ' envoyez le titre en cours depuis son menu.', 'Un Hub plus lumineux, une file et des boutons Studio plus fluides, et des corrections.'])],
    also='À voir aussi : <a href="{stems}">supprimer la voix d’une chanson</a>, <a href="{nc}">le nightcore sur votre téléphone</a>, <a href="{bpm}">BPM de chaque morceau</a>.',
    faq_title='Mises à jour de VibeDeck : questions fréquentes',
    faq=[['Quoi de neuf dans VibeDeck Player 1.0.21 ?', 'Stems sépare tout titre en acapella et instrumental, l’app s’adapte à chaque iPad et iPhone, et les pochettes trouvées s’affichent sur l’écran verrouillé.'],
         ['VibeDeck fonctionne-t-il sur iPad ?', 'Oui. VibeDeck s’adapte à chaque iPad et chaque iPhone, anciens et récents.'],
         ['VibeDeck peut-il supprimer la voix d’une chanson ?', 'Oui. Stems sépare un titre en acapella et instrumental sur votre téléphone. Vous pouvez mixer en direct, ajouter des effets dans Studio et exporter.'],
         ['Comment obtenir la mise à jour ?', 'Mettez à jour VibeDeck Player dans l’App Store. Les nouveaux utilisateurs le téléchargent gratuitement.']],
    free_q='Est-ce gratuit ?', cta='Le même morceau. Une nouvelle sensation. Mettez à jour.', note='L’app est en anglais : Stems se trouve dans Library, sous Tools.')

# ------------------------------------------------------------------ Italian
NC['it'] = dict(
    title='Nightcore su iPhone: preset con un tocco | VibeDeck',
    desc='Nightcore su iPhone e iPad: tocca il preset NIGHTCORE in VibeDeck e il tuo brano diventa più veloce e più acuto. Offline, senza pubblicità.',
    crumb='Nightcore', eyebrow=['Effetti', 'Nightcore'], h1='Nightcore sul telefono, con un tocco.', h1sub='Più veloce, più acuto, più brillante',
    lede='Per fare nightcore, riproduci la tua canzone in VibeDeck Player, apri Effects e tocca NIGHTCORE. Il brano accelera e l’intonazione sale insieme. Regola la velocità, aggiungi riverbero o bassi, registra una clip e condividila. Funziona offline su iPhone e iPad con i tuoi MP3, FLAC e WAV.',
    alt='Schermata principale di VibeDeck Player su iPhone', banner_alt='Pannello Effects di VibeDeck con i preset NIGHTCORE, SLOWED + REVERB, DUB DELAY e VINYL DRIVE su iPhone',
    statement='Il nightcore è l’opposto dello slowed + reverb: la canzone suona più veloce e più acuta, più brillante e piena di energia. Velocità e intonazione cambiano insieme, come un vinile che gira più veloce. In VibeDeck basta un tocco sul preset NIGHTCORE, poi il suono lo modelli tu.',
    ft='Rendilo nightcore', features=[['Preset con un tocco', 'Tocca NIGHTCORE e il brano accelera con un’intonazione più alta.'], ['Regolazione fine', 'SPEED / PITCH, riverbero, eco, filtro DJ, BASS BOOST e saturazione calda.'],
                                      ['Registra e condividi', 'In Studio premi REC, registra fino a 2 minuti con fade in e fade out e condividi.']],
    blocks=[('Come fare nightcore su iPhone', 'ol', ['Installa ' + B('VibeDeck Player') + ' dall’App Store e importa la canzone.', 'Riproduci il brano e apri ' + B('Effects') + '.', 'Tocca il preset ' + B('NIGHTCORE') + '.',
             'Più veloce o più lento? Muovi ' + B('SPEED / PITCH') + ': velocità e intonazione cambiano insieme.', 'Aggiungi ' + B('REVERB') + ' o ' + B('BASS BOOST') + ' a piacere.',
             'Per condividere, apri il brano in ' + B('VibeDeck Studio') + ', premi ' + B('REC') + ' e registra fino a due minuti.', B('ORIGINAL') + ' torna al suono normale.']),
            ('Altri preset con un tocco', 'ul', [B('SLOWED + REVERB:') + ' più lento, più basso, con una lunga coda di riverbero.', B('DUB DELAY:') + ' eco a tempo con la musica.', B('VINYL DRIVE:') + ' suono caldo e saturo, come un vecchio vinile.'])],
    also='Vedi anche: <a href="{eq}">equalizzatore DJ a 3 e 8 bande</a>, <a href="{stems}">come rimuovere la voce da una canzone</a>.',
    faq_title='Nightcore: domande frequenti',
    faq=[['Come faccio una versione nightcore di una canzone su iPhone?', 'Riproduci la canzone in VibeDeck Player, apri Effects e tocca NIGHTCORE. Il brano accelera e l’intonazione sale. Puoi regolare la velocità e aggiungere riverbero o bassi.'],
         ['Che cos’è il nightcore?', 'È una versione di una canzone più veloce e più acuta, che suona più brillante ed energica.'],
         ['Posso accelerare senza alzare l’intonazione?', 'Sì. In VibeDeck Studio puoi bloccare la tonalità e cambiare solo il tempo.'],
         ['Posso registrare e condividere la mia versione?', 'Sì. In Studio premi REC, registra fino a due minuti con fade in e fade out e condividi la clip.'],
         ['Funziona offline?', 'Sì. I preset funzionano con i file della tua libreria VibeDeck, senza internet.']],
    free_q='È gratis?', cta='Più veloce, più acuto, più brillante. Con un tocco.', note='L’app è in inglese: apri Effects e tocca «NIGHTCORE».')

BPM['it'] = dict(
    title='BPM di ogni canzone e ordine per tempo | VibeDeck',
    desc='Scopri i BPM di ogni canzone su iPhone: VibeDeck mostra i BPM esatti nella schermata principale e ordina la coda per tempo. Offline, senza pubblicità.',
    crumb='BPM di ogni canzone', eyebrow=['Funzione', 'BPM'], h1='I BPM di ogni canzone.', h1sub='E la coda per tempo',
    lede='VibeDeck Player mostra i BPM del brano in riproduzione direttamente nella schermata principale. Nella coda puoi ordinare per BPM: i brani sono raggruppati per fascia di tempo, con i BPM esatti su ognuno. Funziona offline su iPhone e iPad con i tuoi MP3, FLAC e WAV.',
    alt='Schermata principale di VibeDeck Player su iPhone con i BPM', banner_alt='VibeDeck Studio su iPhone con i BPM del brano, pitch DJ classico e master tempo',
    statement='DJ, runner e ballerini si chiedono la stessa cosa: che tempo ha questa canzone? Battere il ritmo a mano o aprire un’altra app richiede tempo. VibeDeck mostra i BPM di ogni brano della libreria e li ordina per tempo, così il successivo si incastra bene.',
    ft='Il tempo a colpo d’occhio', features=[['BPM nella schermata principale', 'Il tempo del brano in riproduzione accanto alla forma d’onda.'], ['Ordina per BPM', 'La coda raggruppa i brani per fascia di tempo, con i BPM esatti di ognuno.'],
                                              ['Cambia il tempo', 'In Studio, tempo da -100% a +100%, il key-lock mantiene la tonalità.']],
    blocks=[('Come scoprire i BPM di una canzone', 'ol', ['Installa ' + B('VibeDeck Player') + ' dall’App Store e importa la tua musica.', 'Riproduci un brano. I ' + B('BPM') + ' appaiono nella schermata principale.',
             'Apri la ' + B('coda') + ' e ordina per ' + B('BPM') + '. I brani sono raggruppati per fascia di tempo, con i BPM esatti.', 'Serve un altro tempo? Apri il brano in ' + B('VibeDeck Studio') + ' e cambialo. Il key-lock mantiene la tonalità.']),
            ('Per chi', 'ul', [B('DJ:') + ' avvicinare brani con tempi simili e preparare i passaggi.', B('Produttori:') + ' controllare il tempo di una reference prima di iniziare.',
             B('Corsa e palestra:') + ' una coda al tuo ritmo.', B('Ballerini:') + ' canzoni alla velocità giusta per provare.'])],
    also='Vedi anche: <a href="{nc}">nightcore sul telefono</a>, <a href="{eq}">equalizzatore DJ a 3 e 8 bande</a>.',
    faq_title='BPM: domande frequenti',
    faq=[['Come scopro i BPM di una canzone su iPhone?', 'Importa la canzone in VibeDeck Player e riproducila. I BPM sono nella schermata principale.'],
         ['Posso ordinare la musica per BPM?', 'Sì. Ordina la coda per BPM: i brani sono raggruppati per fascia di tempo, con i BPM esatti di ognuno.'],
         ['Posso cambiare i BPM di una canzone?', 'Sì. In VibeDeck Studio il tempo va da -100% a +100%. Il key-lock mantiene la tonalità.'],
         ['Funziona offline?', 'Sì. VibeDeck usa i file musicali sul tuo dispositivo, senza internet.']],
    free_q='È gratis?', cta='Conosci il tempo di ogni brano.', note='L’app è in inglese: il tempo è indicato come «BPM».')

NEW['it'] = dict(
    title='Novità di VibeDeck Player: Stems, iPad, copertine',
    desc='VibeDeck Player 1.0.21: Stems divide ogni brano in acapella e base, l’app si adatta a ogni iPad e iPhone, copertine nella schermata di blocco.',
    crumb='Novità', eyebrow=['Aggiornamenti', '1.0.21'], h1='Le novità di VibeDeck Player.', h1sub='Versione 1.0.21',
    lede='VibeDeck Player 1.0.21 porta Stems: dividi qualsiasi brano in acapella e base, mixali dal vivo o aprili in Studio, aggiungi effetti ed esporta. VibeDeck ora si adatta a ogni iPad e a ogni iPhone, vecchio e nuovo. Le copertine trovate compaiono anche nella schermata di blocco, e puoi cercare una copertina per qualsiasi brano.',
    alt='Schermata principale di VibeDeck Player su iPhone', banner_alt='VibeDeck Stems divide una canzone in acapella e base su iPhone',
    statement='Ogni aggiornamento di VibeDeck nasce dalla stessa idea: lo stesso brano, una nuova sensazione. La versione 1.0.21 aggiunge lo strumento più grande finora, Stems, e adatta l’app a ogni schermo, dal più piccolo iPhone al più grande iPad.',
    ft='Novità della 1.0.21', features=[['Stems', 'Dividi qualsiasi brano in acapella e base. Mixa dal vivo o aggiungi effetti in Studio. Esporta.'], ['iPad', 'VibeDeck si adatta a ogni iPad e a ogni iPhone, vecchio e nuovo.'],
                                        ['Copertine', 'Le copertine trovate compaiono anche nella schermata di blocco. Cerca una copertina per qualsiasi brano.']],
    blocks=[('Versione 1.0.21', 'ul', [B('Stems:') + ' dividi qualsiasi brano in acapella e base sul telefono, mixa dal vivo o aggiungi effetti in Studio ed esporta.', B('iPad:') + ' VibeDeck si adatta a ogni iPad e iPhone, vecchio e nuovo.',
             B('Copertine:') + ' le copertine trovate compaiono nella schermata di blocco. Cerca una copertina per qualsiasi brano.', 'Correzioni e miglioramenti.']),
            ('Versione 1.0.20', 'ul', [B('Tanti brani insieme:') + ' scegli un gruppo dei tuoi brani, condividilo con VibeDeck e li troverai in coda.', B('Ordina per BPM:') + ' la coda si raggruppa per tempo, con i BPM esatti di ogni brano.',
             B('Forma d’onda:') + ' Needles o Bars.', B('Stems nella libreria:') + ' in Library, sotto Tools.', B('Condividi dalla coda:') + ' invia il brano in riproduzione dal suo menu.', 'Un Hub più luminoso, coda e manopole di Studio più fluide, correzioni.'])],
    also='Vedi anche: <a href="{stems}">come rimuovere la voce da una canzone</a>, <a href="{nc}">nightcore sul telefono</a>, <a href="{bpm}">BPM di ogni canzone</a>.',
    faq_title='Aggiornamenti di VibeDeck: domande frequenti',
    faq=[['Cosa c’è di nuovo in VibeDeck Player 1.0.21?', 'Stems divide ogni brano in acapella e base, l’app si adatta a ogni iPad e iPhone e le copertine trovate compaiono nella schermata di blocco.'],
         ['VibeDeck funziona su iPad?', 'Sì. VibeDeck si adatta a ogni iPad e a ogni iPhone, vecchio e nuovo.'],
         ['VibeDeck può togliere la voce da una canzone?', 'Sì. Stems divide un brano in acapella e base sul telefono. Puoi mixarli dal vivo, aggiungere effetti in Studio ed esportare.'],
         ['Come ottengo l’aggiornamento?', 'Aggiorna VibeDeck Player dall’App Store. I nuovi utenti lo scaricano gratis.']],
    free_q='È gratis?', cta='Lo stesso brano. Una nuova sensazione. Aggiorna.', note='L’app è in inglese: Stems si trova in Library, sotto Tools.')

# ------------------------------------------------------------------ Korean
NC['ko'] = dict(
    title='iPhone에서 나이트코어: 원탭 프리셋 | VibeDeck',
    desc='iPhone과 iPad에서 내 노래를 나이트코어로. VibeDeck의 NIGHTCORE 프리셋을 탭하면 곡이 더 빠르고 높아집니다. 오프라인, 광고 없음.',
    crumb='나이트코어', eyebrow=['이펙트', 'Nightcore'], h1='나이트코어를 한 번의 탭으로.', h1sub='더 빠르게, 더 높게, 더 밝게',
    lede='나이트코어를 만들려면 VibeDeck Player에서 노래를 재생하고 Effects를 열어 NIGHTCORE를 탭하세요. 곡이 빨라지고 음정도 함께 올라갑니다. 속도를 조절하고 리버브나 베이스를 더한 뒤 클립을 녹음해 공유하세요. iPhone과 iPad에서 내 MP3, FLAC, WAV로 오프라인에서 작동합니다.',
    alt='iPhone의 VibeDeck Player 메인 화면', banner_alt='iPhone의 VibeDeck Effects 패널: NIGHTCORE, SLOWED + REVERB, DUB DELAY, VINYL DRIVE 프리셋',
    statement='나이트코어는 slowed + reverb의 반대입니다. 노래가 더 빠르고 높게 재생되어 더 밝고 에너지 넘치게 들립니다. 레코드를 빠르게 돌린 것처럼 속도와 음정이 함께 바뀝니다. VibeDeck에서는 NIGHTCORE 프리셋을 한 번 탭하고, 그다음 소리를 원하는 대로 다듬으면 됩니다.',
    ft='나이트코어로 만들기', features=[['원탭 프리셋', 'NIGHTCORE를 탭하면 곡이 더 빠르고 높아집니다.'], ['세밀한 조정', 'SPEED / PITCH, 리버브, 에코, DJ 필터, BASS BOOST, 따뜻한 새추레이션.'],
                                      ['녹음하고 공유', 'Studio에서 REC를 눌러 페이드 인·아웃과 함께 최대 2분 녹음하고 공유.']],
    blocks=[('iPhone에서 나이트코어 만드는 방법', 'ol', ['App Store에서 ' + B('VibeDeck Player') + '를 설치하고 노래를 가져옵니다.', '곡을 재생하고 ' + B('Effects') + '를 엽니다.', B('NIGHTCORE') + ' 프리셋을 탭합니다.',
             '더 빠르게 또는 느리게? ' + B('SPEED / PITCH') + '를 움직이세요. 속도와 음정이 함께 바뀝니다.', '취향에 따라 ' + B('REVERB') + ' 또는 ' + B('BASS BOOST') + '를 더합니다.',
             '공유하려면 ' + B('VibeDeck Studio') + '에서 곡을 열고 ' + B('REC') + '를 눌러 최대 2분 녹음합니다.', B('ORIGINAL') + '로 원래 소리로 돌아갑니다.']),
            ('다른 원탭 프리셋', 'ul', [B('SLOWED + REVERB:') + ' 더 느리고 낮게, 긴 리버브 꼬리.', B('DUB DELAY:') + ' 음악 박자에 맞춘 에코.', B('VINYL DRIVE:') + ' 오래된 레코드 같은 따뜻하고 진한 소리.'])],
    also='함께 보기: <a href="{eq}">3밴드 DJ EQ와 8밴드 이퀄라이저</a>, <a href="{stems}">노래에서 보컬 분리하기</a>',
    faq_title='나이트코어: 자주 묻는 질문',
    faq=[['iPhone에서 노래를 나이트코어로 만들려면?', 'VibeDeck Player에서 노래를 재생하고 Effects를 열어 NIGHTCORE를 탭하세요. 곡이 빨라지고 음정이 올라갑니다. 속도를 조절하고 리버브나 베이스를 더할 수 있습니다.'],
         ['나이트코어란?', '노래를 더 빠르고 높은 음정으로 재생한 버전으로, 더 밝고 에너지 넘치게 들립니다.'],
         ['음정을 올리지 않고 빠르게만 할 수 있나요?', '네. VibeDeck Studio에서 키를 고정하고 템포만 바꿀 수 있습니다.'],
         ['내 버전을 녹음해서 공유할 수 있나요?', '네. Studio에서 REC를 눌러 페이드 인·아웃과 함께 최대 2분 녹음하고 클립을 공유하세요.'],
         ['오프라인에서 작동하나요?', '네. 프리셋은 VibeDeck 라이브러리의 음악 파일로 인터넷 없이 작동합니다.']],
    free_q='무료인가요?', cta='더 빠르게, 더 높게, 더 밝게. 한 번의 탭으로.', note='앱은 영어로 표시됩니다: Effects를 열고 «NIGHTCORE»를 탭하세요.')

BPM['ko'] = dict(
    title='모든 노래의 BPM과 템포별 정렬 | VibeDeck',
    desc='iPhone에서 모든 노래의 BPM을 확인하세요. VibeDeck은 메인 화면에 정확한 BPM을 보여주고 대기열을 템포별로 정렬합니다. 오프라인, 광고 없음.',
    crumb='노래의 BPM', eyebrow=['기능', 'BPM'], h1='모든 노래의 BPM.', h1sub='그리고 템포별 대기열',
    lede='VibeDeck Player는 재생 중인 곡의 BPM을 메인 화면에 바로 보여줍니다. 대기열은 BPM으로 정렬할 수 있으며, 곡이 템포 범위별로 묶이고 각 곡에 정확한 BPM이 표시됩니다. iPhone과 iPad에서 내 MP3, FLAC, WAV로 오프라인에서 작동합니다.',
    alt='BPM이 표시된 iPhone의 VibeDeck Player 메인 화면', banner_alt='iPhone의 VibeDeck Studio: 곡의 BPM, 클래식 DJ 피치, 마스터 템포',
    statement='DJ, 러너, 댄서 모두 같은 걸 묻습니다. 이 노래 템포가 얼마지? 손으로 박자를 세거나 다른 앱을 여는 건 번거롭습니다. VibeDeck은 라이브러리의 모든 곡 BPM을 보여주고 템포순으로 정렬해 다음 곡이 딱 맞게 해 줍니다.',
    ft='템포를 한눈에', features=[['메인 화면에 BPM', '재생 중인 곡의 템포가 파형 옆에.'], ['BPM으로 정렬', '대기열이 템포 범위별로 묶이고 각 곡에 정확한 BPM.'], ['템포 변경', 'Studio에서 템포 -100%~+100%, key-lock으로 키 유지.']],
    blocks=[('노래의 BPM을 확인하는 방법', 'ol', ['App Store에서 ' + B('VibeDeck Player') + '를 설치하고 음악을 가져옵니다.', '곡을 재생하면 메인 화면에 ' + B('BPM') + '이 나타납니다.',
             B('대기열') + '을 열고 ' + B('BPM') + '으로 정렬합니다. 곡이 템포 범위별로 묶이고 정확한 BPM이 표시됩니다.', '다른 템포가 필요하면 ' + B('VibeDeck Studio') + '에서 곡을 열고 템포를 바꾸세요. key-lock이 키를 유지합니다.']),
            ('이런 분께', 'ul', [B('DJ:') + ' 템포가 비슷한 곡을 모아 전환을 계획.', B('프로듀서:') + ' 작업 전에 레퍼런스 곡의 템포 확인.', B('러닝과 헬스:') + ' 내 페이스에 맞는 대기열.', B('댄서:') + ' 연습에 맞는 속도의 노래 찾기.'])],
    also='함께 보기: <a href="{nc}">나이트코어를 한 번의 탭으로</a>, <a href="{eq}">3밴드 DJ EQ와 8밴드 이퀄라이저</a>',
    faq_title='BPM: 자주 묻는 질문',
    faq=[['iPhone에서 노래의 BPM을 확인하려면?', '노래를 VibeDeck Player로 가져와 재생하세요. BPM이 메인 화면에 표시됩니다.'],
         ['음악을 BPM으로 정렬할 수 있나요?', '네. 대기열을 BPM으로 정렬하면 곡이 템포 범위별로 묶이고 각 곡에 정확한 BPM이 표시됩니다.'],
         ['노래의 BPM을 바꿀 수 있나요?', '네. VibeDeck Studio에서 템포를 -100%에서 +100%까지 바꿀 수 있습니다. key-lock이 키를 유지합니다.'],
         ['오프라인에서 작동하나요?', '네. 기기의 음악 파일로 인터넷 없이 작동합니다.']],
    free_q='무료인가요?', cta='모든 곡의 템포를 알아보세요.', note='앱은 영어로 표시됩니다: 템포는 «BPM»으로 표시됩니다.')

NEW['ko'] = dict(
    title='VibeDeck Player 새 기능: Stems, iPad, 커버',
    desc='VibeDeck Player 1.0.21 새 기능: Stems로 곡을 아카펠라와 반주로 분리, 모든 iPad와 iPhone 지원, 찾은 커버를 잠금 화면에도 표시.',
    crumb='새 기능', eyebrow=['업데이트', '1.0.21'], h1='VibeDeck Player의 새 기능.', h1sub='버전 1.0.21',
    lede='VibeDeck Player 1.0.21에 Stems가 추가되었습니다. 어떤 곡이든 아카펠라와 반주로 나누어 라이브로 믹스하거나 Studio에서 이펙트를 더해 내보낼 수 있습니다. VibeDeck은 이제 오래된 기기부터 최신 기기까지 모든 iPad와 iPhone에 맞습니다. 찾은 커버는 잠금 화면에도 표시되고, 어떤 곡이든 커버를 검색할 수 있습니다.',
    alt='iPhone의 VibeDeck Player 메인 화면', banner_alt='iPhone에서 노래를 아카펠라와 반주로 나누는 VibeDeck Stems',
    statement='VibeDeck의 모든 업데이트는 같은 생각에서 시작합니다. 같은 곡, 새로운 느낌. 버전 1.0.21은 지금까지 가장 큰 도구인 Stems를 더하고, 가장 작은 iPhone부터 가장 큰 iPad까지 모든 화면에 맞게 바뀌었습니다.',
    ft='1.0.21 새 기능', features=[['Stems', '어떤 곡이든 아카펠라와 반주로. 라이브 믹스 또는 Studio에서 이펙트. 내보내기.'], ['iPad', '오래된 기기부터 최신 기기까지 모든 iPad와 iPhone 지원.'], ['커버', '찾은 커버를 잠금 화면에도 표시. 어떤 곡이든 커버 검색.']],
    blocks=[('버전 1.0.21', 'ul', [B('Stems:') + ' 휴대폰에서 어떤 곡이든 아카펠라와 반주로 나누고, 라이브로 믹스하거나 Studio에서 이펙트를 더해 내보내세요.', B('iPad:') + ' 모든 iPad와 iPhone 지원.',
             B('커버:') + ' 찾은 커버를 잠금 화면에도 표시. 어떤 곡이든 커버 검색.', '버그 수정 및 개선.']),
            ('버전 1.0.20', 'ul', [B('여러 곡 한 번에:') + ' 내 곡을 여러 개 골라 VibeDeck으로 공유하면 대기열에 들어갑니다.', B('BPM으로 정렬:') + ' 대기열이 템포별로 묶이고 각 곡에 정확한 BPM.',
             B('파형 선택:') + ' Needles 또는 Bars.', B('라이브러리의 Stems:') + ' Library의 Tools 안.', B('대기열에서 공유:') + ' 재생 중인 곡을 메뉴에서 바로 보내기.', '더 밝은 Hub, 더 부드러운 대기열과 Studio 노브, 버그 수정.'])],
    also='함께 보기: <a href="{stems}">노래에서 보컬 분리하기</a>, <a href="{nc}">나이트코어를 한 번의 탭으로</a>, <a href="{bpm}">모든 노래의 BPM</a>',
    faq_title='VibeDeck 업데이트: 자주 묻는 질문',
    faq=[['VibeDeck Player 1.0.21의 새 기능은?', 'Stems로 곡을 아카펠라와 반주로 분리, 모든 iPad와 iPhone 지원, 찾은 커버를 잠금 화면에도 표시.'],
         ['VibeDeck은 iPad에서 작동하나요?', '네. 오래된 기기부터 최신 기기까지 모든 iPad와 iPhone에 맞습니다.'],
         ['노래에서 보컬을 지울 수 있나요?', '네. Stems가 휴대폰에서 곡을 아카펠라와 반주로 나눕니다. 라이브 믹스, Studio 이펙트, 내보내기가 가능합니다.'],
         ['업데이트는 어떻게 받나요?', 'App Store에서 VibeDeck Player를 업데이트하세요. 새 사용자는 무료로 다운로드할 수 있습니다.']],
    free_q='무료인가요?', cta='같은 곡, 새로운 느낌. 지금 업데이트하세요.', note='앱은 영어로 표시됩니다: Stems는 Library의 Tools에 있습니다.')

# ------------------------------------------------------------------ Turkish
NC['tr'] = dict(
    title='iPhone’da Nightcore: tek dokunuşla preset | VibeDeck',
    desc='Şarkılarının nightcore versiyonunu iPhone ve iPad’de yap: VibeDeck’te NIGHTCORE preset’ine dokun, parça hızlanır ve incelir. Çevrimdışı, reklamsız.',
    crumb='Nightcore', eyebrow=['Efektler', 'Nightcore'], h1='Telefonunda nightcore, tek dokunuşla.', h1sub='Daha hızlı, daha ince, daha parlak',
    lede='Nightcore yapmak için şarkını VibeDeck Player’da çal, Effects’i aç ve NIGHTCORE’a dokun. Parça hızlanır ve ton da onunla yükselir. Hızı ayarla, reverb ya da bas ekle, bir klip kaydet ve paylaş. iPhone ve iPad’de kendi MP3, FLAC ve WAV dosyalarınla çevrimdışı çalışır.',
    alt='iPhone’da VibeDeck Player ana ekranı', banner_alt='iPhone’da VibeDeck Effects paneli: NIGHTCORE, SLOWED + REVERB, DUB DELAY ve VINYL DRIVE preset’leri',
    statement='Nightcore, slowed + reverb’ün tersidir: şarkı daha hızlı ve daha ince çalar, daha parlak ve enerjik duyulur. Hız ve ton birlikte değişir, hızlı dönen bir plak gibi. VibeDeck’te bu, NIGHTCORE preset’ine tek dokunuş; sonra sesi istediğin gibi şekillendirirsin.',
    ft='Nightcore yap', features=[['Tek dokunuşla preset', 'NIGHTCORE’a dokun, parça daha yüksek tonla hızlansın.'], ['İnce ayar', 'SPEED / PITCH, reverb, eko, DJ filtresi, BASS BOOST ve sıcak satürasyon.'],
                                  ['Kaydet ve paylaş', 'Studio’da REC’e bas, fade in ve fade out ile 2 dakikaya kadar kaydet ve paylaş.']],
    blocks=[('iPhone’da nightcore nasıl yapılır', 'ol', [B('VibeDeck Player') + '’ı App Store’dan yükle ve şarkını ekle.', 'Parçayı çal ve ' + B('Effects') + '’i aç.', B('NIGHTCORE') + ' preset’ine dokun.',
             'Daha hızlı mı, daha yavaş mı? ' + B('SPEED / PITCH') + '’i kaydır: hız ve ton birlikte değişir.', 'İstersen ' + B('REVERB') + ' ya da ' + B('BASS BOOST') + ' ekle.',
             'Paylaşmak için parçayı ' + B('VibeDeck Studio') + '’da aç, ' + B('REC') + '’e bas ve iki dakikaya kadar kaydet.', B('ORIGINAL') + ' normal sese döner.']),
            ('Diğer tek dokunuşluk preset’ler', 'ul', [B('SLOWED + REVERB:') + ' daha yavaş, daha kalın, uzun reverb kuyruğuyla.', B('DUB DELAY:') + ' müziğin temposunda ekolar.', B('VINYL DRIVE:') + ' eski bir plak gibi sıcak, doygun ses.'])],
    also='Ayrıca bak: <a href="{eq}">3 ve 8 bantlı DJ ekolayzer</a>, <a href="{stems}">şarkıdan vokal ayırma</a>.',
    faq_title='Nightcore: sık sorulan sorular',
    faq=[['iPhone’da bir şarkının nightcore versiyonunu nasıl yaparım?', 'Şarkıyı VibeDeck Player’da çal, Effects’i aç ve NIGHTCORE’a dokun. Parça hızlanır ve ton yükselir. Hızı ayarlayabilir, reverb ya da bas ekleyebilirsin.'],
         ['Nightcore nedir?', 'Bir şarkının daha hızlı ve daha ince çalınan, daha parlak ve enerjik duyulan versiyonudur.'],
         ['Tonu yükseltmeden sadece hızlandırabilir miyim?', 'Evet. VibeDeck Studio’da tonu sabitleyip yalnızca tempoyu değiştirebilirsin.'],
         ['Versiyonumu kaydedip paylaşabilir miyim?', 'Evet. Studio’da REC’e bas, fade in ve fade out ile iki dakikaya kadar kaydet ve klibi paylaş.'],
         ['Çevrimdışı çalışır mı?', 'Evet. Preset’ler VibeDeck kitaplığındaki dosyalarla internetsiz çalışır.']],
    free_q='Ücretsiz mi?', cta='Daha hızlı, daha ince, daha parlak. Tek dokunuşla.', note='Uygulama İngilizce: Effects’i aç ve «NIGHTCORE»’a dokun.')

BPM['tr'] = dict(
    title='Her şarkının BPM’i ve tempoya göre sıralama | VibeDeck',
    desc='iPhone’da her şarkının BPM’ini gör: VibeDeck ana ekranda kesin BPM’i gösterir ve sıranı tempoya göre dizer. Çevrimdışı, reklamsız.',
    crumb='Her şarkının BPM’i', eyebrow=['Özellik', 'BPM'], h1='Her şarkının BPM’i.', h1sub='Ve tempoya göre sıra',
    lede='VibeDeck Player çalan parçanın BPM’ini doğrudan ana ekranda gösterir. Sırada BPM’e göre sıralayabilirsin: parçalar tempo aralığına göre gruplanır, her birinde kesin BPM yazar. iPhone ve iPad’de kendi MP3, FLAC ve WAV dosyalarınla çevrimdışı çalışır.',
    alt='iPhone’da BPM gösteren VibeDeck Player ana ekranı', banner_alt='iPhone’da VibeDeck Studio: parçanın BPM’i, klasik DJ pitch ve master tempo',
    statement='DJ’ler, koşucular ve dansçılar aynı şeyi sorar: bu şarkının temposu ne? Elle saymak ya da ayrı bir uygulama açmak zaman alır. VibeDeck kitaplığındaki her parçanın BPM’ini gösterir ve onları tempoya göre dizer, böylece sıradaki şarkı tam oturur.',
    ft='Tempo bir bakışta', features=[['Ana ekranda BPM', 'Çalan parçanın temposu dalga formunun yanında.'], ['BPM’e göre sırala', 'Sıra parçaları tempo aralığına göre gruplar, her birinde kesin BPM.'], ['Tempoyu değiştir', 'Studio’da tempo -%100 ile +%100 arası, key-lock tonu korur.']],
    blocks=[('Bir şarkının BPM’i nasıl bulunur', 'ol', [B('VibeDeck Player') + '’ı App Store’dan yükle ve müziğini ekle.', 'Bir parça çal. ' + B('BPM') + ' ana ekranda görünür.',
             B('Sırayı') + ' aç ve ' + B('BPM') + '’e göre sırala. Parçalar tempo aralığına göre gruplanır, kesin BPM ile.', 'Başka bir tempo mu lazım? Parçayı ' + B('VibeDeck Studio') + '’da aç ve tempoyu değiştir. Key-lock tonu korur.']),
            ('Kimler için', 'ul', [B('DJ’ler:') + ' yakın tempolu parçaları bir araya getirip geçişleri planla.', B('Prodüktörler:') + ' başlamadan önce referans parçanın temposunu öğren.',
             B('Koşu ve spor salonu:') + ' temponuza uygun bir sıra.', B('Dansçılar:') + ' çalışmak için doğru hızda şarkılar.'])],
    also='Ayrıca bak: <a href="{nc}">telefonunda nightcore</a>, <a href="{eq}">3 ve 8 bantlı DJ ekolayzer</a>.',
    faq_title='BPM: sık sorulan sorular',
    faq=[['iPhone’da bir şarkının BPM’ini nasıl bulurum?', 'Şarkıyı VibeDeck Player’a ekle ve çal. BPM ana ekranda görünür.'],
         ['Müziğimi BPM’e göre sıralayabilir miyim?', 'Evet. Sırayı BPM’e göre sırala: parçalar tempo aralığına göre gruplanır, her birinde kesin BPM.'],
         ['Bir şarkının BPM’ini değiştirebilir miyim?', 'Evet. VibeDeck Studio’da tempo -%100 ile +%100 arasında değişir. Key-lock tonu korur.'],
         ['Çevrimdışı çalışır mı?', 'Evet. VibeDeck cihazındaki müzik dosyalarıyla internetsiz çalışır.']],
    free_q='Ücretsiz mi?', cta='Her parçanın temposunu bil.', note='Uygulama İngilizce: tempo «BPM» olarak görünür.')

NEW['tr'] = dict(
    title='VibeDeck Player yenilikleri: Stems, iPad, kapaklar',
    desc='VibeDeck Player 1.0.21 yenilikleri: Stems her parçayı akapella ve altyapıya ayırır, uygulama her iPad ve iPhone’a uyar, kapaklar kilit ekranında görünür.',
    crumb='Yenilikler', eyebrow=['Güncellemeler', '1.0.21'], h1='VibeDeck Player’daki yenilikler.', h1sub='Sürüm 1.0.21',
    lede='VibeDeck Player 1.0.21 Stems’i getiriyor: her parçayı akapella ve altyapıya ayır, canlı miksle ya da Studio’da açıp efekt ekle ve dışa aktar. VibeDeck artık eski ve yeni her iPad ve her iPhone’a uyuyor. Bulunan kapaklar kilit ekranında da görünüyor ve her parça için kapak arayabilirsin.',
    alt='iPhone’da VibeDeck Player ana ekranı', banner_alt='iPhone’da bir şarkıyı akapella ve altyapıya ayıran VibeDeck Stems',
    statement='Her VibeDeck güncellemesi aynı fikirden doğar: aynı parça, yeni bir his. 1.0.21 sürümü şimdiye kadarki en büyük aracı, Stems’i ekliyor ve uygulamayı en küçük iPhone’dan en büyük iPad’e kadar her ekrana uyduruyor.',
    ft='1.0.21’de yeni', features=[['Stems', 'Her parçayı akapella ve altyapıya ayır. Canlı miksle ya da Studio’da efekt ekle. Dışa aktar.'], ['iPad', 'VibeDeck eski ve yeni her iPad ve iPhone’a uyar.'], ['Kapaklar', 'Bulunan kapaklar kilit ekranında da görünür. Her parça için kapak ara.']],
    blocks=[('Sürüm 1.0.21', 'ul', [B('Stems:') + ' telefonunda her parçayı akapella ve altyapıya ayır, canlı miksle ya da Studio’da efekt ekle ve dışa aktar.', B('iPad:') + ' VibeDeck eski ve yeni her iPad ve iPhone’a uyar.',
             B('Kapaklar:') + ' bulunan kapaklar kilit ekranında görünür. Her parça için kapak ara.', 'Hata düzeltmeleri ve iyileştirmeler.']),
            ('Sürüm 1.0.20', 'ul', [B('Birçok parça birden:') + ' parçalarından bir grup seç, VibeDeck’e paylaş, sırada olsunlar.', B('BPM’e göre sırala:') + ' sıra tempoya göre gruplanır, her parçada kesin BPM.',
             B('Dalga formu:') + ' Needles ya da Bars.', B('Kitaplıkta Stems:') + ' Library içinde Tools altında.', B('Sıradan paylaş:') + ' çalan parçayı menüsünden gönder.', 'Daha parlak Hub, daha akıcı sıra ve Studio düğmeleri, hata düzeltmeleri.'])],
    also='Ayrıca bak: <a href="{stems}">şarkıdan vokal ayırma</a>, <a href="{nc}">telefonunda nightcore</a>, <a href="{bpm}">her şarkının BPM’i</a>.',
    faq_title='VibeDeck güncellemeleri: sık sorulan sorular',
    faq=[['VibeDeck Player 1.0.21’de ne yeni?', 'Stems her parçayı akapella ve altyapıya ayırır, uygulama her iPad ve iPhone’a uyar ve bulunan kapaklar kilit ekranında görünür.'],
         ['VibeDeck iPad’de çalışır mı?', 'Evet. VibeDeck eski ve yeni her iPad ve iPhone’a uyar.'],
         ['VibeDeck bir şarkıdan vokali çıkarabilir mi?', 'Evet. Stems telefonunda bir parçayı akapella ve altyapıya ayırır. Canlı miksleyebilir, Studio’da efekt ekleyebilir ve dışa aktarabilirsin.'],
         ['Güncellemeyi nasıl alırım?', 'VibeDeck Player’ı App Store’dan güncelle. Yeni kullanıcılar ücretsiz indirir.']],
    free_q='Ücretsiz mi?', cta='Aynı parça. Yeni bir his. Şimdi güncelle.', note='Uygulama İngilizce: Stems, Library içinde Tools altında.')

# ------------------------------------------------------------------ Indonesian
NC['id'] = dict(
    title='Nightcore di iPhone: preset satu ketukan | VibeDeck',
    desc='Buat versi nightcore lagumu sendiri di iPhone dan iPad: ketuk preset NIGHTCORE di VibeDeck, lagu jadi lebih cepat dan lebih tinggi. Offline, tanpa iklan.',
    crumb='Nightcore', eyebrow=['Efek', 'Nightcore'], h1='Nightcore di ponselmu, satu ketukan.', h1sub='Lebih cepat, lebih tinggi, lebih cerah',
    lede='Untuk membuat nightcore, putar lagumu di VibeDeck Player, buka Effects dan ketuk NIGHTCORE. Lagu jadi lebih cepat dan nadanya ikut naik. Atur kecepatan, tambahkan reverb atau bass, rekam klip lalu bagikan. Berjalan offline di iPhone dan iPad dengan file MP3, FLAC dan WAV milikmu.',
    alt='Layar utama VibeDeck Player di iPhone', banner_alt='Panel Effects VibeDeck dengan preset NIGHTCORE, SLOWED + REVERB, DUB DELAY dan VINYL DRIVE di iPhone',
    statement='Nightcore adalah kebalikan dari slowed + reverb: lagu diputar lebih cepat dan lebih tinggi, jadi terdengar lebih cerah dan penuh energi. Kecepatan dan nada berubah bersama, seperti piringan hitam yang diputar lebih cepat. Di VibeDeck cukup satu ketukan pada preset NIGHTCORE, lalu kamu atur suaranya sendiri.',
    ft='Jadikan nightcore', features=[['Preset satu ketukan', 'Ketuk NIGHTCORE dan lagu jadi lebih cepat dengan nada lebih tinggi.'], ['Atur detail', 'SPEED / PITCH, reverb, echo, filter DJ, BASS BOOST dan saturasi hangat.'],
                                      ['Rekam dan bagikan', 'Di Studio tekan REC, rekam hingga 2 menit dengan fade in dan fade out, lalu bagikan.']],
    blocks=[('Cara membuat nightcore di iPhone', 'ol', ['Pasang ' + B('VibeDeck Player') + ' dari App Store dan impor lagumu.', 'Putar lagu dan buka ' + B('Effects') + '.', 'Ketuk preset ' + B('NIGHTCORE') + '.',
             'Mau lebih cepat atau lebih lambat? Geser ' + B('SPEED / PITCH') + ': kecepatan dan nada berubah bersama.', 'Tambahkan ' + B('REVERB') + ' atau ' + B('BASS BOOST') + ' sesuai selera.',
             'Untuk membagikan, buka lagu di ' + B('VibeDeck Studio') + ', tekan ' + B('REC') + ' dan rekam hingga dua menit.', B('ORIGINAL') + ' kembali ke suara normal.']),
            ('Preset satu ketukan lainnya', 'ul', [B('SLOWED + REVERB:') + ' lebih lambat, lebih rendah, dengan ekor reverb panjang.', B('DUB DELAY:') + ' gema yang mengikuti tempo musik.', B('VINYL DRIVE:') + ' suara hangat dan tebal seperti piringan hitam lama.'])],
    also='Lihat juga: <a href="{eq}">equalizer DJ 3 dan 8 band</a>, <a href="{stems}">cara memisahkan vokal dari lagu</a>.',
    faq_title='Nightcore: pertanyaan umum',
    faq=[['Bagaimana membuat versi nightcore lagu di iPhone?', 'Putar lagu di VibeDeck Player, buka Effects dan ketuk NIGHTCORE. Lagu jadi lebih cepat dan nadanya naik. Kamu bisa mengatur kecepatan dan menambahkan reverb atau bass.'],
         ['Apa itu nightcore?', 'Versi lagu yang diputar lebih cepat dan dengan nada lebih tinggi, sehingga terdengar lebih cerah dan bersemangat.'],
         ['Bisakah mempercepat tanpa menaikkan nada?', 'Bisa. Di VibeDeck Studio kamu bisa mengunci kunci nada dan mengubah tempo saja.'],
         ['Bisakah merekam dan membagikan versiku?', 'Bisa. Di Studio tekan REC, rekam hingga dua menit dengan fade in dan fade out, lalu bagikan klipnya.'],
         ['Apakah berjalan offline?', 'Ya. Preset bekerja dengan file musik di perpustakaan VibeDeck tanpa internet.']],
    free_q='Apakah gratis?', cta='Lebih cepat, lebih tinggi, lebih cerah. Satu ketukan.', note='Aplikasi dalam bahasa Inggris: buka Effects lalu ketuk «NIGHTCORE».')

BPM['id'] = dict(
    title='BPM setiap lagu dan urutkan menurut tempo | VibeDeck',
    desc='Lihat BPM setiap lagu di iPhone: VibeDeck menampilkan BPM yang tepat di layar utama dan mengurutkan antrean menurut tempo. Offline, tanpa iklan.',
    crumb='BPM setiap lagu', eyebrow=['Fitur', 'BPM'], h1='BPM setiap lagu.', h1sub='Dan antrean menurut tempo',
    lede='VibeDeck Player menampilkan BPM lagu yang sedang diputar langsung di layar utama. Di antrean kamu bisa mengurutkan menurut BPM: lagu dikelompokkan menurut rentang tempo, dengan BPM tepat di setiap lagu. Berjalan offline di iPhone dan iPad dengan file MP3, FLAC dan WAV milikmu.',
    alt='Layar utama VibeDeck Player di iPhone dengan BPM', banner_alt='VibeDeck Studio di iPhone dengan BPM lagu, pitch DJ klasik dan master tempo',
    statement='DJ, pelari dan penari bertanya hal yang sama: berapa tempo lagu ini? Menghitung manual atau membuka aplikasi lain memakan waktu. VibeDeck menampilkan BPM setiap lagu di perpustakaanmu dan mengurutkannya menurut tempo, agar lagu berikutnya pas.',
    ft='Tempo sekilas', features=[['BPM di layar utama', 'Tempo lagu yang diputar ada di samping gelombang suara.'], ['Urutkan menurut BPM', 'Antrean mengelompokkan lagu menurut rentang tempo, dengan BPM tepat di setiap lagu.'], ['Ubah tempo', 'Di Studio, tempo -100% sampai +100%, key-lock menjaga kunci nada.']],
    blocks=[('Cara mengetahui BPM lagu', 'ol', ['Pasang ' + B('VibeDeck Player') + ' dari App Store dan impor musikmu.', 'Putar lagu. ' + B('BPM') + ' muncul di layar utama.',
             'Buka ' + B('antrean') + ' dan urutkan menurut ' + B('BPM') + '. Lagu dikelompokkan menurut rentang tempo, dengan BPM tepat.', 'Perlu tempo lain? Buka lagu di ' + B('VibeDeck Studio') + ' dan ubah temponya. Key-lock menjaga kunci nada.']),
            ('Untuk siapa', 'ul', [B('DJ:') + ' menyusun lagu dengan tempo mirip dan merencanakan transisi.', B('Produser:') + ' cek tempo lagu referensi sebelum mulai.', B('Lari dan gym:') + ' antrean sesuai ritmemu.', B('Penari:') + ' lagu dengan kecepatan pas untuk latihan.'])],
    also='Lihat juga: <a href="{nc}">nightcore di ponselmu</a>, <a href="{eq}">equalizer DJ 3 dan 8 band</a>.',
    faq_title='BPM: pertanyaan umum',
    faq=[['Bagaimana mengetahui BPM lagu di iPhone?', 'Impor lagu ke VibeDeck Player dan putar. BPM tampil di layar utama.'],
         ['Bisakah mengurutkan musik menurut BPM?', 'Bisa. Urutkan antrean menurut BPM: lagu dikelompokkan menurut rentang tempo, dengan BPM tepat di setiap lagu.'],
         ['Bisakah mengubah BPM lagu?', 'Bisa. Di VibeDeck Studio tempo bisa diubah dari -100% sampai +100%. Key-lock menjaga kunci nada.'],
         ['Apakah berjalan offline?', 'Ya. VibeDeck memakai file musik di perangkatmu tanpa internet.']],
    free_q='Apakah gratis?', cta='Ketahui tempo setiap lagu.', note='Aplikasi dalam bahasa Inggris: tempo tampil sebagai «BPM».')

NEW['id'] = dict(
    title='Yang baru di VibeDeck Player: Stems, iPad, sampul',
    desc='Yang baru di VibeDeck Player 1.0.21: Stems memisahkan lagu jadi acapella dan iringan, aplikasi pas di setiap iPad dan iPhone, sampul tampil di layar kunci.',
    crumb='Yang baru', eyebrow=['Pembaruan', '1.0.21'], h1='Yang baru di VibeDeck Player.', h1sub='Versi 1.0.21',
    lede='VibeDeck Player 1.0.21 menghadirkan Stems: pisahkan lagu apa pun jadi acapella dan iringan, mix langsung atau buka di Studio, tambahkan efek dan ekspor. VibeDeck kini pas di setiap iPad dan setiap iPhone, lama maupun baru. Sampul yang ditemukan juga tampil di layar kunci, dan kamu bisa mencari sampul untuk lagu apa pun.',
    alt='Layar utama VibeDeck Player di iPhone', banner_alt='VibeDeck Stems memisahkan lagu jadi acapella dan iringan di iPhone',
    statement='Setiap pembaruan VibeDeck lahir dari ide yang sama: lagu yang sama, rasa yang baru. Versi 1.0.21 menambahkan alat terbesar sejauh ini, Stems, dan menyesuaikan aplikasi dengan setiap layar, dari iPhone terkecil sampai iPad terbesar.',
    ft='Baru di 1.0.21', features=[['Stems', 'Pisahkan lagu apa pun jadi acapella dan iringan. Mix langsung atau tambah efek di Studio. Ekspor.'], ['iPad', 'VibeDeck pas di setiap iPad dan iPhone, lama maupun baru.'], ['Sampul', 'Sampul yang ditemukan juga tampil di layar kunci. Cari sampul untuk lagu apa pun.']],
    blocks=[('Versi 1.0.21', 'ul', [B('Stems:') + ' pisahkan lagu apa pun jadi acapella dan iringan di ponselmu, mix langsung atau tambah efek di Studio lalu ekspor.', B('iPad:') + ' VibeDeck pas di setiap iPad dan iPhone, lama maupun baru.',
             B('Sampul:') + ' sampul yang ditemukan tampil di layar kunci. Cari sampul untuk lagu apa pun.', 'Perbaikan bug dan peningkatan.']),
            ('Versi 1.0.20', 'ul', [B('Banyak lagu sekaligus:') + ' pilih sekumpulan lagumu, bagikan ke VibeDeck, dan semuanya masuk antrean.', B('Urutkan menurut BPM:') + ' antrean dikelompokkan menurut tempo, dengan BPM tepat di setiap lagu.',
             B('Pilih gelombang:') + ' Needles atau Bars.', B('Stems di perpustakaan:') + ' di Library, bagian Tools.', B('Bagikan dari antrean:') + ' kirim lagu yang diputar dari menunya.', 'Hub lebih cerah, antrean dan kenop Studio lebih halus, perbaikan bug.'])],
    also='Lihat juga: <a href="{stems}">cara memisahkan vokal dari lagu</a>, <a href="{nc}">nightcore di ponselmu</a>, <a href="{bpm}">BPM setiap lagu</a>.',
    faq_title='Pembaruan VibeDeck: pertanyaan umum',
    faq=[['Apa yang baru di VibeDeck Player 1.0.21?', 'Stems memisahkan lagu jadi acapella dan iringan, aplikasi pas di setiap iPad dan iPhone, dan sampul yang ditemukan tampil di layar kunci.'],
         ['Apakah VibeDeck berjalan di iPad?', 'Ya. VibeDeck pas di setiap iPad dan setiap iPhone, lama maupun baru.'],
         ['Bisakah VibeDeck menghapus vokal dari lagu?', 'Bisa. Stems memisahkan lagu jadi acapella dan iringan di ponselmu. Kamu bisa mix langsung, menambah efek di Studio dan mengekspor.'],
         ['Bagaimana mendapatkan pembaruan?', 'Perbarui VibeDeck Player di App Store. Pengguna baru bisa mengunduhnya gratis.']],
    free_q='Apakah gratis?', cta='Lagu yang sama. Rasa yang baru. Perbarui sekarang.', note='Aplikasi dalam bahasa Inggris: Stems ada di Library, bagian Tools.')

# ------------------------------------------------------------------ Polish
NC['pl'] = dict(
    title='Nightcore na iPhonie: preset jednym dotknięciem | VibeDeck',
    desc='Zrób wersję nightcore swoich piosenek na iPhonie i iPadzie: dotknij presetu NIGHTCORE w VibeDeck, a utwór przyspieszy i zabrzmi wyżej. Offline, bez reklam.',
    crumb='Nightcore', eyebrow=['Efekty', 'Nightcore'], h1='Nightcore na telefonie, jednym dotknięciem.', h1sub='Szybciej, wyżej, jaśniej',
    lede='Aby zrobić nightcore, odtwórz piosenkę w VibeDeck Player, otwórz Effects i dotknij NIGHTCORE. Utwór przyspiesza, a wysokość dźwięku rośnie razem z nim. Dopasuj tempo, dodaj pogłos albo bas, nagraj klip i udostępnij go. Działa offline na iPhonie i iPadzie z twoimi plikami MP3, FLAC i WAV.',
    alt='Ekran główny VibeDeck Player na iPhonie', banner_alt='Panel Effects w VibeDeck z presetami NIGHTCORE, SLOWED + REVERB, DUB DELAY i VINYL DRIVE na iPhonie',
    statement='Nightcore to przeciwieństwo slowed + reverb: piosenka gra szybciej i wyżej, więc brzmi jaśniej i z większą energią. Tempo i wysokość zmieniają się razem, jak płyta kręcona szybciej. W VibeDeck to jedno dotknięcie presetu NIGHTCORE, a potem sam kształtujesz brzmienie.',
    ft='Zrób z tego nightcore', features=[['Preset jednym dotknięciem', 'Dotknij NIGHTCORE, a utwór przyspieszy z wyższym dźwiękiem.'], ['Dokładne ustawienia', 'SPEED / PITCH, pogłos, echo, filtr DJ, BASS BOOST i ciepła saturacja.'],
                                          ['Nagraj i udostępnij', 'W Studio naciśnij REC, nagraj do 2 minut z fade in i fade out i udostępnij.']],
    blocks=[('Jak zrobić nightcore na iPhonie', 'ol', ['Zainstaluj ' + B('VibeDeck Player') + ' z App Store i zaimportuj piosenkę.', 'Odtwórz utwór i otwórz ' + B('Effects') + '.', 'Dotknij presetu ' + B('NIGHTCORE') + '.',
             'Szybciej czy wolniej? Przesuń ' + B('SPEED / PITCH') + ': tempo i wysokość zmieniają się razem.', 'Dodaj ' + B('REVERB') + ' albo ' + B('BASS BOOST') + ' według uznania.',
             'Aby udostępnić, otwórz utwór w ' + B('VibeDeck Studio') + ', naciśnij ' + B('REC') + ' i nagraj do dwóch minut.', B('ORIGINAL') + ' przywraca zwykłe brzmienie.']),
            ('Inne presety jednym dotknięciem', 'ul', [B('SLOWED + REVERB:') + ' wolniej, niżej, z długim ogonem pogłosu.', B('DUB DELAY:') + ' echo w rytm muzyki.', B('VINYL DRIVE:') + ' ciepłe, nasycone brzmienie jak ze starej płyty.'])],
    also='Zobacz też: <a href="{eq}">korektor DJ 3 i 8 pasm</a>, <a href="{stems}">jak usunąć wokal z piosenki</a>.',
    faq_title='Nightcore: często zadawane pytania',
    faq=[['Jak zrobić wersję nightcore piosenki na iPhonie?', 'Odtwórz piosenkę w VibeDeck Player, otwórz Effects i dotknij NIGHTCORE. Utwór przyspiesza i brzmi wyżej. Możesz dopasować tempo i dodać pogłos albo bas.'],
         ['Czym jest nightcore?', 'To wersja piosenki odtwarzana szybciej i wyżej, przez co brzmi jaśniej i energiczniej.'],
         ['Czy mogę przyspieszyć bez podnoszenia tonacji?', 'Tak. W VibeDeck Studio możesz zablokować tonację i zmieniać tylko tempo.'],
         ['Czy mogę nagrać i udostępnić swoją wersję?', 'Tak. W Studio naciśnij REC, nagraj do dwóch minut z fade in i fade out i udostępnij klip.'],
         ['Czy działa offline?', 'Tak. Presety działają z plikami w twojej bibliotece VibeDeck, bez internetu.']],
    free_q='Czy to jest darmowe?', cta='Szybciej, wyżej, jaśniej. Jednym dotknięciem.', note='Aplikacja jest po angielsku: otwórz Effects i dotknij «NIGHTCORE».')

BPM['pl'] = dict(
    title='BPM każdej piosenki i sortowanie po tempie | VibeDeck',
    desc='Sprawdź BPM każdej piosenki na iPhonie: VibeDeck pokazuje dokładne BPM na ekranie głównym i sortuje kolejkę według tempa. Offline, bez reklam.',
    crumb='BPM każdej piosenki', eyebrow=['Funkcja', 'BPM'], h1='BPM każdej piosenki.', h1sub='I kolejka według tempa',
    lede='VibeDeck Player pokazuje BPM odtwarzanego utworu bezpośrednio na ekranie głównym. W kolejce możesz sortować według BPM: utwory są grupowane według zakresu tempa, każdy z dokładnym BPM. Działa offline na iPhonie i iPadzie z twoimi plikami MP3, FLAC i WAV.',
    alt='Ekran główny VibeDeck Player na iPhonie z BPM', banner_alt='VibeDeck Studio na iPhonie z BPM utworu, klasycznym pitchem DJ i master tempo',
    statement='DJ-e, biegacze i tancerze pytają o to samo: jakie tempo ma ta piosenka? Wystukiwanie albo osobna aplikacja zabiera czas. VibeDeck pokazuje BPM każdego utworu w bibliotece i układa je według tempa, żeby następna piosenka pasowała.',
    ft='Tempo na pierwszy rzut oka', features=[['BPM na ekranie głównym', 'Tempo odtwarzanego utworu obok fali dźwięku.'], ['Sortuj według BPM', 'Kolejka grupuje utwory według zakresu tempa, każdy z dokładnym BPM.'], ['Zmień tempo', 'W Studio tempo od -100% do +100%, key-lock trzyma tonację.']],
    blocks=[('Jak sprawdzić BPM piosenki', 'ol', ['Zainstaluj ' + B('VibeDeck Player') + ' z App Store i zaimportuj muzykę.', 'Odtwórz utwór. ' + B('BPM') + ' pojawi się na ekranie głównym.',
             'Otwórz ' + B('kolejkę') + ' i posortuj według ' + B('BPM') + '. Utwory są grupowane według zakresu tempa, z dokładnym BPM.', 'Potrzebujesz innego tempa? Otwórz utwór w ' + B('VibeDeck Studio') + ' i zmień je. Key-lock trzyma tonację.']),
            ('Dla kogo', 'ul', [B('DJ-e:') + ' łączyć utwory o podobnym tempie i planować przejścia.', B('Producenci:') + ' sprawdzić tempo utworu referencyjnego przed pracą.', B('Bieganie i siłownia:') + ' kolejka w twoim rytmie.', B('Tancerze:') + ' piosenki w odpowiednim tempie do ćwiczeń.'])],
    also='Zobacz też: <a href="{nc}">nightcore na telefonie</a>, <a href="{eq}">korektor DJ 3 i 8 pasm</a>.',
    faq_title='BPM: często zadawane pytania',
    faq=[['Jak sprawdzić BPM piosenki na iPhonie?', 'Zaimportuj piosenkę do VibeDeck Player i odtwórz ją. BPM jest na ekranie głównym.'],
         ['Czy mogę posortować muzykę według BPM?', 'Tak. Posortuj kolejkę według BPM: utwory są grupowane według zakresu tempa, każdy z dokładnym BPM.'],
         ['Czy mogę zmienić BPM piosenki?', 'Tak. W VibeDeck Studio tempo zmienia się od -100% do +100%. Key-lock trzyma tonację.'],
         ['Czy działa offline?', 'Tak. VibeDeck korzysta z plików muzycznych na twoim urządzeniu, bez internetu.']],
    free_q='Czy to jest darmowe?', cta='Znaj tempo każdego utworu.', note='Aplikacja jest po angielsku: tempo widać jako «BPM».')

NEW['pl'] = dict(
    title='Nowości w VibeDeck Player: Stems, iPad, okładki',
    desc='Nowości w VibeDeck Player 1.0.21: Stems dzieli każdy utwór na acapellę i podkład, aplikacja pasuje do każdego iPada i iPhone’a, okładki na ekranie blokady.',
    crumb='Nowości', eyebrow=['Aktualizacje', '1.0.21'], h1='Nowości w VibeDeck Player.', h1sub='Wersja 1.0.21',
    lede='VibeDeck Player 1.0.21 przynosi Stems: podziel dowolny utwór na acapellę i podkład, miksuj na żywo albo otwórz w Studio, dodaj efekty i eksportuj. VibeDeck pasuje teraz do każdego iPada i każdego iPhone’a, starego i nowego. Znalezione okładki widać też na ekranie blokady, a okładkę możesz wyszukać dla każdego utworu.',
    alt='Ekran główny VibeDeck Player na iPhonie', banner_alt='VibeDeck Stems dzieli piosenkę na acapellę i podkład na iPhonie',
    statement='Każda aktualizacja VibeDeck wychodzi z tej samej myśli: ten sam utwór, nowe odczucie. Wersja 1.0.21 dodaje największe jak dotąd narzędzie, Stems, i dopasowuje aplikację do każdego ekranu, od najmniejszego iPhone’a po największego iPada.',
    ft='Nowe w 1.0.21', features=[['Stems', 'Podziel dowolny utwór na acapellę i podkład. Miksuj na żywo albo dodaj efekty w Studio. Eksport.'], ['iPad', 'VibeDeck pasuje do każdego iPada i iPhone’a, starego i nowego.'], ['Okładki', 'Znalezione okładki widać też na ekranie blokady. Wyszukaj okładkę dla każdego utworu.']],
    blocks=[('Wersja 1.0.21', 'ul', [B('Stems:') + ' podziel dowolny utwór na acapellę i podkład na telefonie, miksuj na żywo albo dodaj efekty w Studio i eksportuj.', B('iPad:') + ' VibeDeck pasuje do każdego iPada i iPhone’a, starego i nowego.',
             B('Okładki:') + ' znalezione okładki widać na ekranie blokady. Wyszukaj okładkę dla każdego utworu.', 'Poprawki i ulepszenia.']),
            ('Wersja 1.0.20', 'ul', [B('Wiele utworów naraz:') + ' wybierz paczkę swoich utworów, udostępnij je do VibeDeck, a trafią do kolejki.', B('Sortowanie według BPM:') + ' kolejka grupuje według tempa, każdy utwór z dokładnym BPM.',
             B('Wygląd fali:') + ' Needles albo Bars.', B('Stems w bibliotece:') + ' w Library, w sekcji Tools.', B('Udostępnianie z kolejki:') + ' wyślij odtwarzany utwór z jego menu.', 'Jaśniejszy Hub, płynniejsza kolejka i pokrętła Studio, poprawki.'])],
    also='Zobacz też: <a href="{stems}">jak usunąć wokal z piosenki</a>, <a href="{nc}">nightcore na telefonie</a>, <a href="{bpm}">BPM każdej piosenki</a>.',
    faq_title='Aktualizacje VibeDeck: często zadawane pytania',
    faq=[['Co nowego w VibeDeck Player 1.0.21?', 'Stems dzieli każdy utwór na acapellę i podkład, aplikacja pasuje do każdego iPada i iPhone’a, a znalezione okładki widać na ekranie blokady.'],
         ['Czy VibeDeck działa na iPadzie?', 'Tak. VibeDeck pasuje do każdego iPada i każdego iPhone’a, starego i nowego.'],
         ['Czy VibeDeck usunie wokal z piosenki?', 'Tak. Stems dzieli utwór na acapellę i podkład na telefonie. Możesz miksować na żywo, dodać efekty w Studio i eksportować.'],
         ['Jak dostać aktualizację?', 'Zaktualizuj VibeDeck Player w App Store. Nowi użytkownicy pobierają go za darmo.']],
    free_q='Czy to jest darmowe?', cta='Ten sam utwór. Nowe odczucie. Zaktualizuj.', note='Aplikacja jest po angielsku: Stems jest w Library, w sekcji Tools.')

# ------------------------------------------------------------------ Dutch
NC['nl'] = dict(
    title='Nightcore op iPhone: preset met één tik | VibeDeck',
    desc='Nightcore op iPhone en iPad: tik op de preset NIGHTCORE in VibeDeck en je nummer wordt sneller en hoger. Offline, zonder reclame.',
    crumb='Nightcore', eyebrow=['Effecten', 'Nightcore'], h1='Nightcore op je telefoon, met één tik.', h1sub='Sneller, hoger, helderder',
    lede='Voor nightcore speel je je nummer af in VibeDeck Player, open je Effects en tik je op NIGHTCORE. Het nummer versnelt en de toonhoogte gaat mee omhoog. Stel de snelheid bij, voeg galm of bas toe, neem een clip op en deel hem. Werkt offline op iPhone en iPad met je eigen MP3, FLAC en WAV.',
    alt='Hoofdscherm van VibeDeck Player op iPhone', banner_alt='VibeDeck Effects op iPhone met de presets NIGHTCORE, SLOWED + REVERB, DUB DELAY en VINYL DRIVE',
    statement='Nightcore is het tegenovergestelde van slowed + reverb: het nummer speelt sneller en hoger en klinkt helderder en energieker. Snelheid en toonhoogte veranderen samen, zoals een plaat die sneller draait. In VibeDeck is dat één tik op NIGHTCORE, daarna vorm je het geluid zelf.',
    ft='Maak het nightcore', features=[['Preset met één tik', 'Tik op NIGHTCORE en het nummer versnelt met een hogere toon.'], ['Fijn afstellen', 'SPEED / PITCH, galm, echo, DJ-filter, BASS BOOST en warme saturatie.'],
                                       ['Opnemen en delen', 'Druk in Studio op REC, neem tot 2 minuten op met fade-in en fade-out en deel.']],
    blocks=[('Zo maak je nightcore op iPhone', 'ol', ['Installeer ' + B('VibeDeck Player') + ' uit de App Store en importeer je nummer.', 'Speel het nummer af en open ' + B('Effects') + '.', 'Tik op de preset ' + B('NIGHTCORE') + '.',
             'Sneller of langzamer? Schuif ' + B('SPEED / PITCH') + ': snelheid en toonhoogte veranderen samen.', 'Voeg naar smaak ' + B('REVERB') + ' of ' + B('BASS BOOST') + ' toe.',
             'Om te delen open je het nummer in ' + B('VibeDeck Studio') + ', druk je op ' + B('REC') + ' en neem je tot twee minuten op.', B('ORIGINAL') + ' zet alle effecten terug.']),
            ('Andere presets met één tik', 'ul', [B('SLOWED + REVERB:') + ' langzamer, lager, met een lange galmstaart.', B('DUB DELAY:') + ' echo’s op de maat van de muziek.', B('VINYL DRIVE:') + ' warm, verzadigd geluid zoals een oude plaat.'])],
    also='Zie ook: <a href="{eq}">DJ-equalizer met 3 en 8 banden</a>, <a href="{stems}">zang uit een nummer verwijderen</a>.',
    faq_title='Nightcore: veelgestelde vragen',
    faq=[['Hoe maak ik een nightcore-versie van een nummer op iPhone?', 'Speel het nummer af in VibeDeck Player, open Effects en tik op NIGHTCORE. Het nummer versnelt en klinkt hoger. Je kunt de snelheid bijstellen en galm of bas toevoegen.'],
         ['Wat is nightcore?', 'Een versie van een nummer die sneller en hoger speelt, waardoor het helderder en energieker klinkt.'],
         ['Kan ik sneller zonder hoger te klinken?', 'Ja. In VibeDeck Studio kun je de toonsoort vastzetten en alleen het tempo veranderen.'],
         ['Kan ik mijn versie opnemen en delen?', 'Ja. Druk in Studio op REC, neem tot twee minuten op met fade-in en fade-out en deel de clip.'],
         ['Werkt het offline?', 'Ja. De presets werken met de bestanden in je VibeDeck-bibliotheek, zonder internet.']],
    free_q='Is het gratis?', cta='Sneller, hoger, helderder. Met één tik.', note='De app is in het Engels: open Effects en tik op «NIGHTCORE».')

BPM['nl'] = dict(
    title='BPM van elk nummer en sorteren op tempo | VibeDeck',
    desc='Zie de BPM van elk nummer op iPhone: VibeDeck toont de exacte BPM op het hoofdscherm en sorteert je wachtrij op tempo. Offline, zonder reclame.',
    crumb='BPM van elk nummer', eyebrow=['Functie', 'BPM'], h1='De BPM van elk nummer.', h1sub='En je wachtrij op tempo',
    lede='VibeDeck Player toont de BPM van het nummer dat speelt direct op het hoofdscherm. In de wachtrij kun je sorteren op BPM: nummers worden gegroepeerd per tempobereik, elk met de exacte BPM. Werkt offline op iPhone en iPad met je eigen MP3, FLAC en WAV.',
    alt='Hoofdscherm van VibeDeck Player op iPhone met BPM', banner_alt='VibeDeck Studio op iPhone met de BPM van het nummer, klassieke DJ-pitch en master tempo',
    statement='DJ’s, hardlopers en dansers vragen hetzelfde: welk tempo heeft dit nummer? Meetikken of een aparte app openen kost tijd. VibeDeck toont de BPM van elk nummer in je bibliotheek en zet ze op tempo, zodat het volgende nummer past.',
    ft='Tempo in één oogopslag', features=[['BPM op het hoofdscherm', 'Het tempo van het nummer dat speelt, naast de golfvorm.'], ['Sorteren op BPM', 'De wachtrij groepeert per tempobereik, elk nummer met de exacte BPM.'], ['Tempo aanpassen', 'In Studio tempo van -100% tot +100%, key-lock houdt de toonsoort.']],
    blocks=[('Zo vind je de BPM van een nummer', 'ol', ['Installeer ' + B('VibeDeck Player') + ' uit de App Store en importeer je muziek.', 'Speel een nummer af. De ' + B('BPM') + ' verschijnt op het hoofdscherm.',
             'Open de ' + B('wachtrij') + ' en sorteer op ' + B('BPM') + '. Nummers worden gegroepeerd per tempobereik, met de exacte BPM.', 'Ander tempo nodig? Open het nummer in ' + B('VibeDeck Studio') + ' en pas het aan. Key-lock houdt de toonsoort.']),
            ('Voor wie', 'ul', [B('DJ’s:') + ' nummers met een vergelijkbaar tempo bij elkaar zetten en overgangen plannen.', B('Producers:') + ' het tempo van een referentienummer checken.', B('Hardlopen en sportschool:') + ' een wachtrij op jouw tempo.', B('Dansers:') + ' nummers op de juiste snelheid om te oefenen.'])],
    also='Zie ook: <a href="{nc}">nightcore op je telefoon</a>, <a href="{eq}">DJ-equalizer met 3 en 8 banden</a>.',
    faq_title='BPM: veelgestelde vragen',
    faq=[['Hoe vind ik de BPM van een nummer op iPhone?', 'Importeer het nummer in VibeDeck Player en speel het af. De BPM staat op het hoofdscherm.'],
         ['Kan ik mijn muziek sorteren op BPM?', 'Ja. Sorteer de wachtrij op BPM: nummers worden gegroepeerd per tempobereik, elk met de exacte BPM.'],
         ['Kan ik de BPM van een nummer veranderen?', 'Ja. In VibeDeck Studio gaat het tempo van -100% tot +100%. Key-lock houdt de toonsoort.'],
         ['Werkt het offline?', 'Ja. VibeDeck gebruikt de muziekbestanden op je apparaat, zonder internet.']],
    free_q='Is het gratis?', cta='Ken het tempo van elk nummer.', note='De app is in het Engels: het tempo staat als «BPM».')

NEW['nl'] = dict(
    title='Nieuw in VibeDeck Player: Stems, iPad, hoesjes',
    desc='Nieuw in VibeDeck Player 1.0.21: Stems splitst elk nummer in acapella en begeleiding, de app past op elke iPad en iPhone, hoesjes op het vergrendelscherm.',
    crumb='Nieuw', eyebrow=['Updates', '1.0.21'], h1='Nieuw in VibeDeck Player.', h1sub='Versie 1.0.21',
    lede='VibeDeck Player 1.0.21 brengt Stems: splits elk nummer in acapella en begeleiding, mix ze live of open ze in Studio, voeg effecten toe en exporteer. VibeDeck past nu op elke iPad en elke iPhone, oud en nieuw. Gevonden hoesjes verschijnen ook op het vergrendelscherm, en je kunt voor elk nummer een hoesje zoeken.',
    alt='Hoofdscherm van VibeDeck Player op iPhone', banner_alt='VibeDeck Stems splitst een nummer in acapella en begeleiding op iPhone',
    statement='Elke VibeDeck-update komt uit hetzelfde idee: hetzelfde nummer, een nieuw gevoel. Versie 1.0.21 voegt het grootste gereedschap tot nu toe toe, Stems, en past de app aan elk scherm aan, van de kleinste iPhone tot de grootste iPad.',
    ft='Nieuw in 1.0.21', features=[['Stems', 'Splits elk nummer in acapella en begeleiding. Mix live of voeg effecten toe in Studio. Exporteer.'], ['iPad', 'VibeDeck past op elke iPad en iPhone, oud en nieuw.'], ['Hoesjes', 'Gevonden hoesjes verschijnen ook op het vergrendelscherm. Zoek een hoesje voor elk nummer.']],
    blocks=[('Versie 1.0.21', 'ul', [B('Stems:') + ' splits elk nummer op je telefoon in acapella en begeleiding, mix live of voeg effecten toe in Studio en exporteer.', B('iPad:') + ' VibeDeck past op elke iPad en iPhone, oud en nieuw.',
             B('Hoesjes:') + ' gevonden hoesjes verschijnen op het vergrendelscherm. Zoek een hoesje voor elk nummer.', 'Bugfixes en verbeteringen.']),
            ('Versie 1.0.20', 'ul', [B('Veel nummers tegelijk:') + ' kies een stapel van je nummers, deel ze met VibeDeck en ze staan in je wachtrij.', B('Sorteren op BPM:') + ' de wachtrij groepeert op tempo, elk nummer met de exacte BPM.',
             B('Golfvorm kiezen:') + ' Needles of Bars.', B('Stems in de bibliotheek:') + ' in Library, onder Tools.', B('Delen vanuit de wachtrij:') + ' stuur het nummer dat speelt vanuit het menu.', 'Een helderdere Hub, een soepelere wachtrij en Studio-knoppen, bugfixes.'])],
    also='Zie ook: <a href="{stems}">zang uit een nummer verwijderen</a>, <a href="{nc}">nightcore op je telefoon</a>, <a href="{bpm}">BPM van elk nummer</a>.',
    faq_title='VibeDeck-updates: veelgestelde vragen',
    faq=[['Wat is nieuw in VibeDeck Player 1.0.21?', 'Stems splitst elk nummer in acapella en begeleiding, de app past op elke iPad en iPhone en gevonden hoesjes verschijnen op het vergrendelscherm.'],
         ['Werkt VibeDeck op iPad?', 'Ja. VibeDeck past op elke iPad en elke iPhone, oud en nieuw.'],
         ['Kan VibeDeck de zang uit een nummer halen?', 'Ja. Stems splitst een nummer op je telefoon in acapella en begeleiding. Je kunt live mixen, effecten toevoegen in Studio en exporteren.'],
         ['Hoe krijg ik de update?', 'Werk VibeDeck Player bij in de App Store. Nieuwe gebruikers downloaden hem gratis.']],
    free_q='Is het gratis?', cta='Hetzelfde nummer. Een nieuw gevoel. Update nu.', note='De app is in het Engels: Stems staat in Library, onder Tools.')

# ------------------------------------------------------------------ Vietnamese
NC['vi'] = dict(
    title='Nightcore trên iPhone: preset một chạm | VibeDeck',
    desc='Tạo bản nightcore cho bài hát của bạn trên iPhone và iPad: chạm preset NIGHTCORE trong VibeDeck, bài hát nhanh hơn và cao hơn. Ngoại tuyến, không quảng cáo.',
    crumb='Nightcore', eyebrow=['Hiệu ứng', 'Nightcore'], h1='Nightcore trên điện thoại, chỉ một chạm.', h1sub='Nhanh hơn, cao hơn, sáng hơn',
    lede='Để làm nightcore, phát bài hát trong VibeDeck Player, mở Effects và chạm NIGHTCORE. Bài hát tăng tốc và cao độ cũng tăng theo. Chỉnh tốc độ, thêm reverb hoặc bass, ghi một đoạn và chia sẻ. Hoạt động ngoại tuyến trên iPhone và iPad với file MP3, FLAC và WAV của bạn.',
    alt='Màn hình chính VibeDeck Player trên iPhone', banner_alt='Bảng Effects của VibeDeck với các preset NIGHTCORE, SLOWED + REVERB, DUB DELAY và VINYL DRIVE trên iPhone',
    statement='Nightcore ngược với slowed + reverb: bài hát phát nhanh hơn và cao hơn nên nghe sáng và nhiều năng lượng hơn. Tốc độ và cao độ thay đổi cùng nhau, như đĩa than quay nhanh hơn. Trong VibeDeck chỉ cần một chạm vào preset NIGHTCORE, rồi bạn tự chỉnh âm thanh.',
    ft='Biến thành nightcore', features=[['Preset một chạm', 'Chạm NIGHTCORE và bài hát nhanh hơn với cao độ cao hơn.'], ['Tinh chỉnh', 'SPEED / PITCH, reverb, echo, bộ lọc DJ, BASS BOOST và saturation ấm.'],
                                         ['Ghi và chia sẻ', 'Trong Studio nhấn REC, ghi tối đa 2 phút với fade in và fade out rồi chia sẻ.']],
    blocks=[('Cách làm nightcore trên iPhone', 'ol', ['Cài ' + B('VibeDeck Player') + ' từ App Store và nhập bài hát.', 'Phát bài hát và mở ' + B('Effects') + '.', 'Chạm preset ' + B('NIGHTCORE') + '.',
             'Muốn nhanh hay chậm hơn? Kéo ' + B('SPEED / PITCH') + ': tốc độ và cao độ thay đổi cùng nhau.', 'Thêm ' + B('REVERB') + ' hoặc ' + B('BASS BOOST') + ' tùy thích.',
             'Để chia sẻ, mở bài hát trong ' + B('VibeDeck Studio') + ', nhấn ' + B('REC') + ' và ghi tối đa hai phút.', B('ORIGINAL') + ' trở về âm thanh gốc.']),
            ('Các preset một chạm khác', 'ul', [B('SLOWED + REVERB:') + ' chậm hơn, trầm hơn, với đuôi reverb dài.', B('DUB DELAY:') + ' tiếng vọng theo nhịp nhạc.', B('VINYL DRIVE:') + ' âm thanh ấm và dày như đĩa than cũ.'])],
    also='Xem thêm: <a href="{eq}">EQ DJ 3 và 8 băng tần</a>, <a href="{stems}">cách tách giọng hát khỏi bài hát</a>.',
    faq_title='Nightcore: câu hỏi thường gặp',
    faq=[['Làm sao tạo bản nightcore của bài hát trên iPhone?', 'Phát bài hát trong VibeDeck Player, mở Effects và chạm NIGHTCORE. Bài hát nhanh hơn và cao độ tăng. Bạn có thể chỉnh tốc độ và thêm reverb hoặc bass.'],
         ['Nightcore là gì?', 'Là phiên bản bài hát được phát nhanh hơn và cao hơn, nghe sáng và sôi động hơn.'],
         ['Có thể tăng tốc mà không tăng cao độ không?', 'Có. Trong VibeDeck Studio bạn có thể khóa tông và chỉ đổi tempo.'],
         ['Có thể ghi và chia sẻ bản của tôi không?', 'Có. Trong Studio nhấn REC, ghi tối đa hai phút với fade in và fade out rồi chia sẻ.'],
         ['Có hoạt động ngoại tuyến không?', 'Có. Các preset hoạt động với file nhạc trong thư viện VibeDeck, không cần internet.']],
    free_q='Có miễn phí không?', cta='Nhanh hơn, cao hơn, sáng hơn. Chỉ một chạm.', note='Ứng dụng bằng tiếng Anh: mở Effects và chạm «NIGHTCORE».')

BPM['vi'] = dict(
    title='BPM của mọi bài hát và sắp xếp theo tempo | VibeDeck',
    desc='Xem BPM của mọi bài hát trên iPhone: VibeDeck hiện BPM chính xác trên màn hình chính và sắp xếp hàng chờ theo tempo. Ngoại tuyến, không quảng cáo.',
    crumb='BPM của mọi bài hát', eyebrow=['Tính năng', 'BPM'], h1='BPM của mọi bài hát.', h1sub='Và hàng chờ theo tempo',
    lede='VibeDeck Player hiện BPM của bài đang phát ngay trên màn hình chính. Trong hàng chờ bạn có thể sắp xếp theo BPM: bài hát được nhóm theo khoảng tempo, mỗi bài có BPM chính xác. Hoạt động ngoại tuyến trên iPhone và iPad với file MP3, FLAC và WAV của bạn.',
    alt='Màn hình chính VibeDeck Player trên iPhone có BPM', banner_alt='VibeDeck Studio trên iPhone với BPM bài hát, pitch DJ cổ điển và master tempo',
    statement='DJ, người chạy bộ và vũ công đều hỏi cùng một câu: bài này tempo bao nhiêu? Gõ nhịp bằng tay hay mở ứng dụng khác đều mất thời gian. VibeDeck hiện BPM của mọi bài trong thư viện và xếp chúng theo tempo để bài tiếp theo luôn khớp.',
    ft='Tempo trong nháy mắt', features=[['BPM trên màn hình chính', 'Tempo của bài đang phát nằm cạnh dạng sóng.'], ['Sắp xếp theo BPM', 'Hàng chờ nhóm bài theo khoảng tempo, mỗi bài có BPM chính xác.'], ['Đổi tempo', 'Trong Studio, tempo từ -100% đến +100%, key-lock giữ nguyên tông.']],
    blocks=[('Cách xem BPM của bài hát', 'ol', ['Cài ' + B('VibeDeck Player') + ' từ App Store và nhập nhạc.', 'Phát một bài. ' + B('BPM') + ' hiện trên màn hình chính.',
             'Mở ' + B('hàng chờ') + ' và sắp xếp theo ' + B('BPM') + '. Bài hát được nhóm theo khoảng tempo, có BPM chính xác.', 'Cần tempo khác? Mở bài trong ' + B('VibeDeck Studio') + ' và đổi tempo. Key-lock giữ nguyên tông.']),
            ('Dành cho ai', 'ul', [B('DJ:') + ' ghép các bài có tempo gần nhau và lên kế hoạch chuyển bài.', B('Nhà sản xuất:') + ' kiểm tra tempo bài tham khảo trước khi làm.', B('Chạy bộ và tập gym:') + ' hàng chờ theo nhịp của bạn.', B('Vũ công:') + ' bài hát đúng tốc độ để tập.'])],
    also='Xem thêm: <a href="{nc}">nightcore trên điện thoại</a>, <a href="{eq}">EQ DJ 3 và 8 băng tần</a>.',
    faq_title='BPM: câu hỏi thường gặp',
    faq=[['Làm sao xem BPM của bài hát trên iPhone?', 'Nhập bài hát vào VibeDeck Player và phát. BPM hiện trên màn hình chính.'],
         ['Có thể sắp xếp nhạc theo BPM không?', 'Có. Sắp xếp hàng chờ theo BPM: bài hát được nhóm theo khoảng tempo, mỗi bài có BPM chính xác.'],
         ['Có thể đổi BPM của bài hát không?', 'Có. Trong VibeDeck Studio tempo đổi từ -100% đến +100%. Key-lock giữ nguyên tông.'],
         ['Có hoạt động ngoại tuyến không?', 'Có. VibeDeck dùng file nhạc trên thiết bị của bạn, không cần internet.']],
    free_q='Có miễn phí không?', cta='Biết tempo của mọi bài.', note='Ứng dụng bằng tiếng Anh: tempo hiển thị là «BPM».')

NEW['vi'] = dict(
    title='Có gì mới trong VibeDeck Player: Stems, iPad, ảnh bìa',
    desc='Có gì mới trong VibeDeck Player 1.0.21: Stems tách bài hát thành acapella và nhạc nền, ứng dụng vừa mọi iPad và iPhone, ảnh bìa hiện trên màn hình khóa.',
    crumb='Có gì mới', eyebrow=['Cập nhật', '1.0.21'], h1='Có gì mới trong VibeDeck Player.', h1sub='Phiên bản 1.0.21',
    lede='VibeDeck Player 1.0.21 có Stems: tách bất kỳ bài nào thành acapella và nhạc nền, mix trực tiếp hoặc mở trong Studio, thêm hiệu ứng và xuất. VibeDeck giờ vừa với mọi iPad và mọi iPhone, cũ và mới. Ảnh bìa tìm được cũng hiện trên màn hình khóa, và bạn có thể tìm ảnh bìa cho bất kỳ bài nào.',
    alt='Màn hình chính VibeDeck Player trên iPhone', banner_alt='VibeDeck Stems tách bài hát thành acapella và nhạc nền trên iPhone',
    statement='Mỗi bản cập nhật VibeDeck đều từ một ý tưởng: cùng bài hát, cảm giác mới. Phiên bản 1.0.21 thêm công cụ lớn nhất từ trước đến nay, Stems, và làm ứng dụng vừa mọi màn hình, từ iPhone nhỏ nhất đến iPad lớn nhất.',
    ft='Mới trong 1.0.21', features=[['Stems', 'Tách bất kỳ bài nào thành acapella và nhạc nền. Mix trực tiếp hoặc thêm hiệu ứng trong Studio. Xuất.'], ['iPad', 'VibeDeck vừa với mọi iPad và iPhone, cũ và mới.'], ['Ảnh bìa', 'Ảnh bìa tìm được cũng hiện trên màn hình khóa. Tìm ảnh bìa cho bất kỳ bài nào.']],
    blocks=[('Phiên bản 1.0.21', 'ul', [B('Stems:') + ' tách bất kỳ bài nào thành acapella và nhạc nền ngay trên điện thoại, mix trực tiếp hoặc thêm hiệu ứng trong Studio rồi xuất.', B('iPad:') + ' VibeDeck vừa với mọi iPad và iPhone, cũ và mới.',
             B('Ảnh bìa:') + ' ảnh bìa tìm được hiện trên màn hình khóa. Tìm ảnh bìa cho bất kỳ bài nào.', 'Sửa lỗi và cải tiến.']),
            ('Phiên bản 1.0.20', 'ul', [B('Nhiều bài cùng lúc:') + ' chọn một loạt bài của bạn, chia sẻ sang VibeDeck và chúng sẽ có trong hàng chờ.', B('Sắp xếp theo BPM:') + ' hàng chờ nhóm theo tempo, mỗi bài có BPM chính xác.',
             B('Chọn dạng sóng:') + ' Needles hoặc Bars.', B('Stems trong thư viện:') + ' trong Library, mục Tools.', B('Chia sẻ từ hàng chờ:') + ' gửi bài đang phát từ menu của nó.', 'Hub sáng hơn, hàng chờ và núm Studio mượt hơn, sửa lỗi.'])],
    also='Xem thêm: <a href="{stems}">cách tách giọng hát khỏi bài hát</a>, <a href="{nc}">nightcore trên điện thoại</a>, <a href="{bpm}">BPM của mọi bài hát</a>.',
    faq_title='Cập nhật VibeDeck: câu hỏi thường gặp',
    faq=[['VibeDeck Player 1.0.21 có gì mới?', 'Stems tách bài hát thành acapella và nhạc nền, ứng dụng vừa mọi iPad và iPhone, ảnh bìa tìm được hiện trên màn hình khóa.'],
         ['VibeDeck có chạy trên iPad không?', 'Có. VibeDeck vừa với mọi iPad và mọi iPhone, cũ và mới.'],
         ['VibeDeck có xóa giọng hát khỏi bài hát được không?', 'Có. Stems tách bài hát thành acapella và nhạc nền trên điện thoại. Bạn có thể mix trực tiếp, thêm hiệu ứng trong Studio và xuất.'],
         ['Làm sao nhận bản cập nhật?', 'Cập nhật VibeDeck Player trên App Store. Người dùng mới tải miễn phí.']],
    free_q='Có miễn phí không?', cta='Cùng bài hát. Cảm giác mới. Cập nhật ngay.', note='Ứng dụng bằng tiếng Anh: Stems nằm trong Library, mục Tools.')

# ------------------------------------------------------------------ Chinese (Traditional)
NC['zh-Hant'] = dict(
    title='iPhone 上的 Nightcore：一鍵預設 | VibeDeck',
    desc='在 iPhone 和 iPad 上把自己的歌曲做成 nightcore：點一下 VibeDeck 的 NIGHTCORE 預設，歌曲變得更快、更高。離線使用，沒有廣告。',
    crumb='Nightcore', eyebrow=['效果', 'Nightcore'], h1='手機上的 nightcore，一鍵完成。', h1sub='更快、更高、更明亮',
    lede='想做 nightcore，就在 VibeDeck Player 播放歌曲，打開 Effects，點 NIGHTCORE。歌曲會加快，音高也一起升高。調整速度、加入殘響或低音，錄下片段再分享。在 iPhone 和 iPad 上用你的 MP3、FLAC、WAV 離線使用。',
    alt='iPhone 上的 VibeDeck Player 主畫面', banner_alt='iPhone 上的 VibeDeck Effects 面板：NIGHTCORE、SLOWED + REVERB、DUB DELAY、VINYL DRIVE 預設',
    statement='Nightcore 跟 slowed + reverb 相反：歌曲播得更快、更高，聽起來更明亮、更有能量。速度和音高一起改變，就像唱片轉得更快。在 VibeDeck 只要點一下 NIGHTCORE 預設，之後的聲音由你自己調整。',
    ft='做成 nightcore', features=[['一鍵預設', '點 NIGHTCORE，歌曲加快、音高變高。'], ['細部調整', 'SPEED / PITCH、殘響、回音、DJ 濾波、BASS BOOST 和溫暖飽和。'], ['錄音並分享', '在 Studio 按 REC，含淡入淡出最長錄 2 分鐘，然後分享。']],
    blocks=[('如何在 iPhone 上做 nightcore', 'ol', ['從 App Store 安裝 ' + B('VibeDeck Player') + ' 並匯入歌曲。', '播放歌曲並打開 ' + B('Effects') + '。', '點 ' + B('NIGHTCORE') + ' 預設。',
             '想更快或更慢？拖動 ' + B('SPEED / PITCH') + '：速度和音高一起改變。', '依喜好加入 ' + B('REVERB') + ' 或 ' + B('BASS BOOST') + '。',
             '要分享時，在 ' + B('VibeDeck Studio') + ' 打開歌曲，按 ' + B('REC') + '，最長錄兩分鐘。', B('ORIGINAL') + ' 回到原本的聲音。']),
            ('其他一鍵預設', 'ul', [B('SLOWED + REVERB：') + '更慢、更低，帶長長的殘響尾音。', B('DUB DELAY：') + '跟著音樂節拍的回音。', B('VINYL DRIVE：') + '像老唱片般溫暖飽滿的聲音。'])],
    also='延伸閱讀：<a href="{eq}">3 段 DJ EQ 與 8 段等化器</a>、<a href="{stems}">如何分離歌曲人聲</a>',
    faq_title='Nightcore：常見問題',
    faq=[['如何在 iPhone 上把歌曲做成 nightcore？', '在 VibeDeck Player 播放歌曲，打開 Effects，點 NIGHTCORE。歌曲會加快、音高升高。也可以調整速度，加入殘響或低音。'],
         ['什麼是 nightcore？', '把歌曲播得更快、音高更高的版本，聽起來更明亮、更有活力。'],
         ['可以只加快速度、不升高音高嗎？', '可以。在 VibeDeck Studio 可以鎖定調性，只改變速度。'],
         ['可以錄下並分享我的版本嗎？', '可以。在 Studio 按 REC，含淡入淡出最長錄兩分鐘，然後分享片段。'],
         ['可以離線使用嗎？', '可以。預設使用 VibeDeck 資料庫裡的音樂檔，不需要網路。']],
    free_q='免費嗎？', cta='更快、更高、更明亮。一鍵完成。', note='App 介面為英文：打開 Effects，點「NIGHTCORE」。')

BPM['zh-Hant'] = dict(
    title='每首歌的 BPM，依速度排序 | VibeDeck',
    desc='在 iPhone 上看到每首歌的 BPM：VibeDeck 在主畫面顯示精確 BPM，並依速度排序播放佇列。離線使用，沒有廣告。',
    crumb='每首歌的 BPM', eyebrow=['功能', 'BPM'], h1='每首歌的 BPM。', h1sub='播放佇列依速度排序',
    lede='VibeDeck Player 直接在主畫面顯示正在播放歌曲的 BPM。播放佇列可以依 BPM 排序：歌曲按速度範圍分組，每首都標示精確 BPM。在 iPhone 和 iPad 上用你的 MP3、FLAC、WAV 離線使用。',
    alt='iPhone 上顯示 BPM 的 VibeDeck Player 主畫面', banner_alt='iPhone 上的 VibeDeck Studio：歌曲 BPM、經典 DJ 音高與 master tempo',
    statement='DJ、跑者和舞者都想知道同一件事：這首歌的速度是多少？手動打拍子或另開 App 都很花時間。VibeDeck 顯示資料庫裡每首歌的 BPM，並依速度排好，讓下一首剛剛好。',
    ft='速度一目了然', features=[['主畫面上的 BPM', '正在播放歌曲的速度就在波形旁邊。'], ['依 BPM 排序', '播放佇列按速度範圍分組，每首都有精確 BPM。'], ['改變速度', '在 Studio 速度從 -100% 到 +100%，key-lock 保持調性。']],
    blocks=[('如何知道歌曲的 BPM', 'ol', ['從 App Store 安裝 ' + B('VibeDeck Player') + ' 並匯入音樂。', '播放歌曲，' + B('BPM') + ' 會出現在主畫面。',
             '打開' + B('播放佇列') + '，依 ' + B('BPM') + ' 排序。歌曲按速度範圍分組，並標示精確 BPM。', '需要別的速度？在 ' + B('VibeDeck Studio') + ' 打開歌曲並調整。key-lock 保持調性。']),
            ('適合誰', 'ul', [B('DJ：') + '把速度相近的歌放在一起，規劃銜接。', B('製作人：') + '開工前確認參考曲的速度。', B('跑步與健身：') + '配合你節奏的播放佇列。', B('舞者：') + '找到適合練習速度的歌。'])],
    also='延伸閱讀：<a href="{nc}">手機上的 nightcore</a>、<a href="{eq}">3 段 DJ EQ 與 8 段等化器</a>',
    faq_title='BPM：常見問題',
    faq=[['如何在 iPhone 上知道歌曲的 BPM？', '把歌曲匯入 VibeDeck Player 並播放，BPM 會顯示在主畫面。'],
         ['可以依 BPM 排序音樂嗎？', '可以。播放佇列依 BPM 排序後，歌曲按速度範圍分組，每首都有精確 BPM。'],
         ['可以改變歌曲的 BPM 嗎？', '可以。在 VibeDeck Studio 速度可從 -100% 調到 +100%，key-lock 保持調性。'],
         ['可以離線使用嗎？', '可以。VibeDeck 使用裝置上的音樂檔，不需要網路。']],
    free_q='免費嗎？', cta='掌握每首歌的速度。', note='App 介面為英文：速度顯示為「BPM」。')

NEW['zh-Hant'] = dict(
    title='VibeDeck Player 新功能：Stems、iPad、封面',
    desc='VibeDeck Player 1.0.21 新功能：Stems 把任何歌曲分成清唱和伴奏，App 適合每台 iPad 和 iPhone，找到的封面也會顯示在鎖定畫面。',
    crumb='新功能', eyebrow=['更新', '1.0.21'], h1='VibeDeck Player 新功能。', h1sub='版本 1.0.21',
    lede='VibeDeck Player 1.0.21 帶來 Stems：把任何歌曲分成清唱和伴奏，現場混音，或在 Studio 打開加入效果再匯出。VibeDeck 現在適合每台 iPad 和每支 iPhone，新舊都可以。找到的封面也會顯示在鎖定畫面，任何歌曲都能搜尋封面。',
    alt='iPhone 上的 VibeDeck Player 主畫面', banner_alt='VibeDeck Stems 在 iPhone 上把歌曲分成清唱和伴奏',
    statement='VibeDeck 的每次更新都來自同一個想法：同一首歌，新的感受。1.0.21 加入目前最大的工具 Stems，並讓 App 適合每種螢幕，從最小的 iPhone 到最大的 iPad。',
    ft='1.0.21 新功能', features=[['Stems', '任何歌曲分成清唱和伴奏。現場混音或在 Studio 加效果。匯出。'], ['iPad', 'VibeDeck 適合每台 iPad 和 iPhone，新舊都可以。'], ['封面', '找到的封面也會顯示在鎖定畫面。任何歌曲都能搜尋封面。']],
    blocks=[('版本 1.0.21', 'ul', [B('Stems：') + '在手機上把任何歌曲分成清唱和伴奏，現場混音或在 Studio 加效果後匯出。', B('iPad：') + 'VibeDeck 適合每台 iPad 和 iPhone，新舊都可以。',
             B('封面：') + '找到的封面顯示在鎖定畫面。任何歌曲都能搜尋封面。', '錯誤修正與改進。']),
            ('版本 1.0.20', 'ul', [B('一次分享多首：') + '選一批自己的歌曲分享到 VibeDeck，它們就會在播放佇列裡。', B('依 BPM 排序：') + '播放佇列按速度分組，每首都有精確 BPM。',
             B('選擇波形：') + 'Needles 或 Bars。', B('資料庫裡的 Stems：') + '在 Library 的 Tools 裡。', B('從佇列分享：') + '從選單直接傳送正在播放的歌曲。', '更亮的 Hub、更流暢的佇列和 Studio 旋鈕，以及錯誤修正。'])],
    also='延伸閱讀：<a href="{stems}">如何分離歌曲人聲</a>、<a href="{nc}">手機上的 nightcore</a>、<a href="{bpm}">每首歌的 BPM</a>',
    faq_title='VibeDeck 更新：常見問題',
    faq=[['VibeDeck Player 1.0.21 有什麼新功能？', 'Stems 把任何歌曲分成清唱和伴奏，App 適合每台 iPad 和 iPhone，找到的封面也會顯示在鎖定畫面。'],
         ['VibeDeck 可以在 iPad 上用嗎？', '可以。VibeDeck 適合每台 iPad 和每支 iPhone，新舊都可以。'],
         ['VibeDeck 可以去掉歌曲的人聲嗎？', '可以。Stems 在手機上把歌曲分成清唱和伴奏。可以現場混音、在 Studio 加效果並匯出。'],
         ['如何取得更新？', '在 App Store 更新 VibeDeck Player。新使用者可以免費下載。']],
    free_q='免費嗎？', cta='同一首歌，新的感受。立即更新。', note='App 介面為英文：Stems 在 Library 的 Tools 裡。')

# ------------------------------------------------------------------ Chinese (Simplified)
NC['zh-Hans'] = dict(
    title='iPhone 上的 Nightcore：一键预设 | VibeDeck',
    desc='在 iPhone 和 iPad 上把自己的歌曲做成 nightcore：点一下 VibeDeck 的 NIGHTCORE 预设，歌曲变得更快、更高。离线使用，没有广告。',
    crumb='Nightcore', eyebrow=['效果', 'Nightcore'], h1='手机上的 nightcore，一键完成。', h1sub='更快、更高、更明亮',
    lede='想做 nightcore，就在 VibeDeck Player 播放歌曲，打开 Effects，点 NIGHTCORE。歌曲会加快，音高也一起升高。调整速度、加入混响或低音，录下片段再分享。在 iPhone 和 iPad 上用你的 MP3、FLAC、WAV 离线使用。',
    alt='iPhone 上的 VibeDeck Player 主界面', banner_alt='iPhone 上的 VibeDeck Effects 面板：NIGHTCORE、SLOWED + REVERB、DUB DELAY、VINYL DRIVE 预设',
    statement='Nightcore 和 slowed + reverb 相反：歌曲播得更快、更高，听起来更明亮、更有能量。速度和音高一起改变，就像唱片转得更快。在 VibeDeck 只要点一下 NIGHTCORE 预设，之后的声音由你自己调整。',
    ft='做成 nightcore', features=[['一键预设', '点 NIGHTCORE，歌曲加快、音高变高。'], ['细节调整', 'SPEED / PITCH、混响、回声、DJ 滤波、BASS BOOST 和温暖饱和。'], ['录音并分享', '在 Studio 按 REC，含淡入淡出最长录 2 分钟，然后分享。']],
    blocks=[('如何在 iPhone 上做 nightcore', 'ol', ['从 App Store 安装 ' + B('VibeDeck Player') + ' 并导入歌曲。', '播放歌曲并打开 ' + B('Effects') + '。', '点 ' + B('NIGHTCORE') + ' 预设。',
             '想更快或更慢？拖动 ' + B('SPEED / PITCH') + '：速度和音高一起改变。', '按喜好加入 ' + B('REVERB') + ' 或 ' + B('BASS BOOST') + '。',
             '要分享时，在 ' + B('VibeDeck Studio') + ' 打开歌曲，按 ' + B('REC') + '，最长录两分钟。', B('ORIGINAL') + ' 回到原来的声音。']),
            ('其他一键预设', 'ul', [B('SLOWED + REVERB：') + '更慢、更低，带长长的混响尾音。', B('DUB DELAY：') + '跟着音乐节拍的回声。', B('VINYL DRIVE：') + '像老唱片一样温暖饱满的声音。'])],
    also='延伸阅读：<a href="{eq}">3 段 DJ EQ 和 8 段均衡器</a>、<a href="{stems}">如何分离歌曲人声</a>',
    faq_title='Nightcore：常见问题',
    faq=[['如何在 iPhone 上把歌曲做成 nightcore？', '在 VibeDeck Player 播放歌曲，打开 Effects，点 NIGHTCORE。歌曲会加快、音高升高。也可以调整速度，加入混响或低音。'],
         ['什么是 nightcore？', '把歌曲播得更快、音高更高的版本，听起来更明亮、更有活力。'],
         ['可以只加快速度、不升高音高吗？', '可以。在 VibeDeck Studio 可以锁定调性，只改变速度。'],
         ['可以录下并分享我的版本吗？', '可以。在 Studio 按 REC，含淡入淡出最长录两分钟，然后分享片段。'],
         ['可以离线使用吗？', '可以。预设使用 VibeDeck 资料库里的音乐文件，不需要网络。']],
    free_q='免费吗？', cta='更快、更高、更明亮。一键完成。', note='App 界面为英文：打开 Effects，点“NIGHTCORE”。')

BPM['zh-Hans'] = dict(
    title='每首歌的 BPM，按速度排序 | VibeDeck',
    desc='在 iPhone 上看到每首歌的 BPM：VibeDeck 在主界面显示精确 BPM，并按速度排序播放队列。离线使用，没有广告。',
    crumb='每首歌的 BPM', eyebrow=['功能', 'BPM'], h1='每首歌的 BPM。', h1sub='播放队列按速度排序',
    lede='VibeDeck Player 直接在主界面显示正在播放歌曲的 BPM。播放队列可以按 BPM 排序：歌曲按速度范围分组，每首都标注精确 BPM。在 iPhone 和 iPad 上用你的 MP3、FLAC、WAV 离线使用。',
    alt='iPhone 上显示 BPM 的 VibeDeck Player 主界面', banner_alt='iPhone 上的 VibeDeck Studio：歌曲 BPM、经典 DJ 音高和 master tempo',
    statement='DJ、跑者和舞者都想知道同一件事：这首歌的速度是多少？手动打拍子或另开 App 都很花时间。VibeDeck 显示资料库里每首歌的 BPM，并按速度排好，让下一首刚刚好。',
    ft='速度一目了然', features=[['主界面上的 BPM', '正在播放歌曲的速度就在波形旁边。'], ['按 BPM 排序', '播放队列按速度范围分组，每首都有精确 BPM。'], ['改变速度', '在 Studio 速度从 -100% 到 +100%，key-lock 保持调性。']],
    blocks=[('如何知道歌曲的 BPM', 'ol', ['从 App Store 安装 ' + B('VibeDeck Player') + ' 并导入音乐。', '播放歌曲，' + B('BPM') + ' 会出现在主界面。',
             '打开' + B('播放队列') + '，按 ' + B('BPM') + ' 排序。歌曲按速度范围分组，并标注精确 BPM。', '需要别的速度？在 ' + B('VibeDeck Studio') + ' 打开歌曲并调整。key-lock 保持调性。']),
            ('适合谁', 'ul', [B('DJ：') + '把速度相近的歌放在一起，规划衔接。', B('制作人：') + '开工前确认参考曲的速度。', B('跑步和健身：') + '配合你节奏的播放队列。', B('舞者：') + '找到适合练习速度的歌。'])],
    also='延伸阅读：<a href="{nc}">手机上的 nightcore</a>、<a href="{eq}">3 段 DJ EQ 和 8 段均衡器</a>',
    faq_title='BPM：常见问题',
    faq=[['如何在 iPhone 上知道歌曲的 BPM？', '把歌曲导入 VibeDeck Player 并播放，BPM 会显示在主界面。'],
         ['可以按 BPM 排序音乐吗？', '可以。播放队列按 BPM 排序后，歌曲按速度范围分组，每首都有精确 BPM。'],
         ['可以改变歌曲的 BPM 吗？', '可以。在 VibeDeck Studio 速度可从 -100% 调到 +100%，key-lock 保持调性。'],
         ['可以离线使用吗？', '可以。VibeDeck 使用设备上的音乐文件，不需要网络。']],
    free_q='免费吗？', cta='掌握每首歌的速度。', note='App 界面为英文：速度显示为“BPM”。')

NEW['zh-Hans'] = dict(
    title='VibeDeck Player 新功能：Stems、iPad、封面',
    desc='VibeDeck Player 1.0.21 新功能：Stems 把任何歌曲分成清唱和伴奏，App 适配每台 iPad 和 iPhone，找到的封面也会显示在锁屏上。',
    crumb='新功能', eyebrow=['更新', '1.0.21'], h1='VibeDeck Player 新功能。', h1sub='版本 1.0.21',
    lede='VibeDeck Player 1.0.21 带来 Stems：把任何歌曲分成清唱和伴奏，现场混音，或在 Studio 打开加入效果再导出。VibeDeck 现在适配每台 iPad 和每部 iPhone，新旧都可以。找到的封面也会显示在锁屏上，任何歌曲都能搜索封面。',
    alt='iPhone 上的 VibeDeck Player 主界面', banner_alt='VibeDeck Stems 在 iPhone 上把歌曲分成清唱和伴奏',
    statement='VibeDeck 的每次更新都来自同一个想法：同一首歌，新的感受。1.0.21 加入目前最大的工具 Stems，并让 App 适配每种屏幕，从最小的 iPhone 到最大的 iPad。',
    ft='1.0.21 新功能', features=[['Stems', '任何歌曲分成清唱和伴奏。现场混音或在 Studio 加效果。导出。'], ['iPad', 'VibeDeck 适配每台 iPad 和 iPhone，新旧都可以。'], ['封面', '找到的封面也会显示在锁屏上。任何歌曲都能搜索封面。']],
    blocks=[('版本 1.0.21', 'ul', [B('Stems：') + '在手机上把任何歌曲分成清唱和伴奏，现场混音或在 Studio 加效果后导出。', B('iPad：') + 'VibeDeck 适配每台 iPad 和 iPhone，新旧都可以。',
             B('封面：') + '找到的封面显示在锁屏上。任何歌曲都能搜索封面。', '错误修复和改进。']),
            ('版本 1.0.20', 'ul', [B('一次分享多首：') + '选一批自己的歌曲分享到 VibeDeck，它们就会在播放队列里。', B('按 BPM 排序：') + '播放队列按速度分组，每首都有精确 BPM。',
             B('选择波形：') + 'Needles 或 Bars。', B('资料库里的 Stems：') + '在 Library 的 Tools 里。', B('从队列分享：') + '从菜单直接发送正在播放的歌曲。', '更亮的 Hub、更流畅的队列和 Studio 旋钮，以及错误修复。'])],
    also='延伸阅读：<a href="{stems}">如何分离歌曲人声</a>、<a href="{nc}">手机上的 nightcore</a>、<a href="{bpm}">每首歌的 BPM</a>',
    faq_title='VibeDeck 更新：常见问题',
    faq=[['VibeDeck Player 1.0.21 有什么新功能？', 'Stems 把任何歌曲分成清唱和伴奏，App 适配每台 iPad 和 iPhone，找到的封面也会显示在锁屏上。'],
         ['VibeDeck 可以在 iPad 上用吗？', '可以。VibeDeck 适配每台 iPad 和每部 iPhone，新旧都可以。'],
         ['VibeDeck 可以去掉歌曲的人声吗？', '可以。Stems 在手机上把歌曲分成清唱和伴奏。可以现场混音、在 Studio 加效果并导出。'],
         ['如何获取更新？', '在 App Store 更新 VibeDeck Player。新用户可以免费下载。']],
    free_q='免费吗？', cta='同一首歌，新的感受。立即更新。', note='App 界面为英文：Stems 在 Library 的 Tools 里。')

# ------------------------------------------------------------------ Thai
NC['th'] = dict(
    title='Nightcore บน iPhone: พรีเซ็ตแตะครั้งเดียว | VibeDeck',
    desc='ทำเพลงของคุณเป็น nightcore บน iPhone และ iPad: แตะพรีเซ็ต NIGHTCORE ใน VibeDeck เพลงจะเร็วขึ้นและสูงขึ้น ใช้ออฟไลน์ ไม่มีโฆษณา',
    crumb='Nightcore', eyebrow=['เอฟเฟกต์', 'Nightcore'], h1='Nightcore บนมือถือ แตะครั้งเดียว', h1sub='เร็วขึ้น สูงขึ้น สดใสขึ้น',
    lede='อยากทำ nightcore ให้เปิดเพลงใน VibeDeck Player เปิด Effects แล้วแตะ NIGHTCORE เพลงจะเร็วขึ้นและโทนเสียงสูงขึ้นไปด้วย ปรับความเร็ว เพิ่มรีเวิร์บหรือเบส อัดคลิปแล้วแชร์ ใช้งานออฟไลน์บน iPhone และ iPad กับไฟล์ MP3, FLAC และ WAV ของคุณ',
    alt='หน้าจอหลัก VibeDeck Player บน iPhone', banner_alt='แผง Effects ของ VibeDeck บน iPhone พร้อมพรีเซ็ต NIGHTCORE, SLOWED + REVERB, DUB DELAY และ VINYL DRIVE',
    statement='Nightcore ตรงข้ามกับ slowed + reverb เพลงเล่นเร็วขึ้นและสูงขึ้น จึงฟังสดใสและมีพลังกว่า ความเร็วและโทนเสียงเปลี่ยนไปพร้อมกัน เหมือนแผ่นเสียงที่หมุนเร็วขึ้น ใน VibeDeck แค่แตะพรีเซ็ต NIGHTCORE ครั้งเดียว แล้วปรับเสียงต่อได้ตามใจ',
    ft='ทำให้เป็น nightcore', features=[['พรีเซ็ตแตะครั้งเดียว', 'แตะ NIGHTCORE เพลงจะเร็วขึ้นและโทนสูงขึ้น'], ['ปรับละเอียด', 'SPEED / PITCH รีเวิร์บ เอคโค่ ฟิลเตอร์ DJ BASS BOOST และแซทูเรชันอุ่น ๆ'], ['อัดและแชร์', 'ใน Studio กด REC อัดได้สูงสุด 2 นาทีพร้อม fade in และ fade out แล้วแชร์']],
    blocks=[('วิธีทำ nightcore บน iPhone', 'ol', ['ติดตั้ง ' + B('VibeDeck Player') + ' จาก App Store แล้วนำเข้าเพลง', 'เปิดเพลงแล้วเปิด ' + B('Effects'), 'แตะพรีเซ็ต ' + B('NIGHTCORE'),
             'อยากเร็วขึ้นหรือช้าลง เลื่อน ' + B('SPEED / PITCH') + ' ความเร็วและโทนเปลี่ยนพร้อมกัน', 'เพิ่ม ' + B('REVERB') + ' หรือ ' + B('BASS BOOST') + ' ตามชอบ',
             'ถ้าจะแชร์ เปิดเพลงใน ' + B('VibeDeck Studio') + ' กด ' + B('REC') + ' แล้วอัดได้สูงสุดสองนาที', B('ORIGINAL') + ' กลับไปเป็นเสียงปกติ']),
            ('พรีเซ็ตแตะครั้งเดียวอื่น ๆ', 'ul', [B('SLOWED + REVERB:') + ' ช้าลง ต่ำลง พร้อมหางรีเวิร์บยาว', B('DUB DELAY:') + ' เสียงสะท้อนตามจังหวะเพลง', B('VINYL DRIVE:') + ' เสียงอุ่นและแน่นเหมือนแผ่นเสียงเก่า'])],
    also='อ่านเพิ่มเติม: <a href="{eq}">อีควอไลเซอร์ DJ 3 และ 8 แบนด์</a> <a href="{stems}">วิธีแยกเสียงร้องออกจากเพลง</a>',
    faq_title='Nightcore: คำถามที่พบบ่อย',
    faq=[['ทำเพลงเป็น nightcore บน iPhone อย่างไร', 'เปิดเพลงใน VibeDeck Player เปิด Effects แล้วแตะ NIGHTCORE เพลงจะเร็วขึ้นและโทนสูงขึ้น ปรับความเร็วและเพิ่มรีเวิร์บหรือเบสได้'],
         ['nightcore คืออะไร', 'เวอร์ชันของเพลงที่เล่นเร็วขึ้นและโทนสูงขึ้น ฟังสดใสและมีพลังกว่า'],
         ['เร่งความเร็วโดยไม่เพิ่มโทนได้ไหม', 'ได้ ใน VibeDeck Studio ล็อกคีย์แล้วเปลี่ยนแค่เทมโปได้'],
         ['อัดและแชร์เวอร์ชันของฉันได้ไหม', 'ได้ ใน Studio กด REC อัดได้สูงสุดสองนาทีพร้อม fade in และ fade out แล้วแชร์คลิป'],
         ['ใช้ออฟไลน์ได้ไหม', 'ได้ พรีเซ็ตใช้กับไฟล์เพลงในคลัง VibeDeck โดยไม่ต้องใช้อินเทอร์เน็ต']],
    free_q='ใช้ฟรีไหม', cta='เร็วขึ้น สูงขึ้น สดใสขึ้น แตะครั้งเดียว', note='แอปเป็นภาษาอังกฤษ: เปิด Effects แล้วแตะ «NIGHTCORE»')

BPM['th'] = dict(
    title='BPM ของทุกเพลง และเรียงตามเทมโป | VibeDeck',
    desc='ดู BPM ของทุกเพลงบน iPhone: VibeDeck แสดง BPM ที่แม่นยำบนหน้าจอหลัก และเรียงคิวตามเทมโป ใช้ออฟไลน์ ไม่มีโฆษณา',
    crumb='BPM ของทุกเพลง', eyebrow=['ฟีเจอร์', 'BPM'], h1='BPM ของทุกเพลง', h1sub='และคิวเรียงตามเทมโป',
    lede='VibeDeck Player แสดง BPM ของเพลงที่กำลังเล่นบนหน้าจอหลักทันที ในคิวเรียงตาม BPM ได้ เพลงจะถูกจัดกลุ่มตามช่วงเทมโป และแต่ละเพลงมี BPM ที่แม่นยำ ใช้งานออฟไลน์บน iPhone และ iPad กับไฟล์ MP3, FLAC และ WAV ของคุณ',
    alt='หน้าจอหลัก VibeDeck Player บน iPhone ที่แสดง BPM', banner_alt='VibeDeck Studio บน iPhone แสดง BPM ของเพลง พิตช์ DJ แบบคลาสสิก และ master tempo',
    statement='ดีเจ นักวิ่ง และนักเต้นถามเหมือนกัน เพลงนี้เทมโปเท่าไร การเคาะเองหรือเปิดแอปอื่นเสียเวลา VibeDeck แสดง BPM ของทุกเพลงในคลังและเรียงตามเทมโป เพลงถัดไปจึงเข้ากันพอดี',
    ft='เห็นเทมโปทันที', features=[['BPM บนหน้าจอหลัก', 'เทมโปของเพลงที่เล่นอยู่ข้างรูปคลื่น'], ['เรียงตาม BPM', 'คิวจัดกลุ่มตามช่วงเทมโป แต่ละเพลงมี BPM ที่แม่นยำ'], ['เปลี่ยนเทมโป', 'ใน Studio เทมโป -100% ถึง +100% และ key-lock รักษาคีย์']],
    blocks=[('วิธีดู BPM ของเพลง', 'ol', ['ติดตั้ง ' + B('VibeDeck Player') + ' จาก App Store แล้วนำเข้าเพลง', 'เปิดเพลง ' + B('BPM') + ' จะขึ้นบนหน้าจอหลัก',
             'เปิด' + B('คิว') + 'แล้วเรียงตาม ' + B('BPM') + ' เพลงจะจัดกลุ่มตามช่วงเทมโปพร้อม BPM ที่แม่นยำ', 'อยากได้เทมโปอื่น เปิดเพลงใน ' + B('VibeDeck Studio') + ' แล้วปรับ key-lock รักษาคีย์ไว้']),
            ('เหมาะกับใคร', 'ul', [B('ดีเจ:') + ' จัดเพลงเทมโปใกล้กันและวางแผนการต่อเพลง', B('โปรดิวเซอร์:') + ' เช็กเทมโปเพลงอ้างอิงก่อนเริ่มทำ', B('วิ่งและฟิตเนส:') + ' คิวที่เข้ากับจังหวะของคุณ', B('นักเต้น:') + ' หาเพลงความเร็วพอดีสำหรับซ้อม'])],
    also='อ่านเพิ่มเติม: <a href="{nc}">nightcore บนมือถือ</a> <a href="{eq}">อีควอไลเซอร์ DJ 3 และ 8 แบนด์</a>',
    faq_title='BPM: คำถามที่พบบ่อย',
    faq=[['ดู BPM ของเพลงบน iPhone อย่างไร', 'นำเข้าเพลงใน VibeDeck Player แล้วเปิด BPM จะแสดงบนหน้าจอหลัก'],
         ['เรียงเพลงตาม BPM ได้ไหม', 'ได้ เรียงคิวตาม BPM เพลงจะจัดกลุ่มตามช่วงเทมโป แต่ละเพลงมี BPM ที่แม่นยำ'],
         ['เปลี่ยน BPM ของเพลงได้ไหม', 'ได้ ใน VibeDeck Studio เทมโปเปลี่ยนได้ตั้งแต่ -100% ถึง +100% key-lock รักษาคีย์'],
         ['ใช้ออฟไลน์ได้ไหม', 'ได้ VibeDeck ใช้ไฟล์เพลงในเครื่องของคุณโดยไม่ต้องใช้อินเทอร์เน็ต']],
    free_q='ใช้ฟรีไหม', cta='รู้เทมโปของทุกเพลง', note='แอปเป็นภาษาอังกฤษ: เทมโปแสดงเป็น «BPM»')

NEW['th'] = dict(
    title='มีอะไรใหม่ใน VibeDeck Player: Stems, iPad, ปก',
    desc='มีอะไรใหม่ใน VibeDeck Player 1.0.21: Stems แยกเพลงเป็นอะคาเปลลาและดนตรี แอปพอดีกับทุก iPad และ iPhone และปกเพลงแสดงบนหน้าจอล็อก',
    crumb='มีอะไรใหม่', eyebrow=['อัปเดต', '1.0.21'], h1='มีอะไรใหม่ใน VibeDeck Player', h1sub='เวอร์ชัน 1.0.21',
    lede='VibeDeck Player 1.0.21 มาพร้อม Stems: แยกเพลงไหนก็ได้เป็นอะคาเปลลาและดนตรี มิกซ์สด หรือเปิดใน Studio เพิ่มเอฟเฟกต์แล้วส่งออก VibeDeck ตอนนี้พอดีกับทุก iPad และทุก iPhone ทั้งรุ่นเก่าและใหม่ ปกที่หาเจอแสดงบนหน้าจอล็อกด้วย และค้นหาปกให้เพลงไหนก็ได้',
    alt='หน้าจอหลัก VibeDeck Player บน iPhone', banner_alt='VibeDeck Stems แยกเพลงเป็นอะคาเปลลาและดนตรีบน iPhone',
    statement='ทุกอัปเดตของ VibeDeck มาจากไอเดียเดียวกัน เพลงเดิม ความรู้สึกใหม่ เวอร์ชัน 1.0.21 เพิ่มเครื่องมือที่ใหญ่ที่สุดจนถึงตอนนี้ คือ Stems และทำให้แอปพอดีกับทุกหน้าจอ ตั้งแต่ iPhone เล็กที่สุดถึง iPad ใหญ่ที่สุด',
    ft='ใหม่ใน 1.0.21', features=[['Stems', 'แยกเพลงไหนก็ได้เป็นอะคาเปลลาและดนตรี มิกซ์สดหรือเพิ่มเอฟเฟกต์ใน Studio ส่งออก'], ['iPad', 'VibeDeck พอดีกับทุก iPad และ iPhone ทั้งรุ่นเก่าและใหม่'], ['ปกเพลง', 'ปกที่หาเจอแสดงบนหน้าจอล็อกด้วย ค้นหาปกให้เพลงไหนก็ได้']],
    blocks=[('เวอร์ชัน 1.0.21', 'ul', [B('Stems:') + ' แยกเพลงไหนก็ได้เป็นอะคาเปลลาและดนตรีบนมือถือ มิกซ์สดหรือเพิ่มเอฟเฟกต์ใน Studio แล้วส่งออก', B('iPad:') + ' VibeDeck พอดีกับทุก iPad และ iPhone ทั้งรุ่นเก่าและใหม่',
             B('ปกเพลง:') + ' ปกที่หาเจอแสดงบนหน้าจอล็อก ค้นหาปกให้เพลงไหนก็ได้', 'แก้ไขข้อบกพร่องและปรับปรุง']),
            ('เวอร์ชัน 1.0.20', 'ul', [B('หลายเพลงพร้อมกัน:') + ' เลือกเพลงของคุณหลายเพลง แชร์ไปที่ VibeDeck แล้วจะอยู่ในคิว', B('เรียงตาม BPM:') + ' คิวจัดกลุ่มตามเทมโป แต่ละเพลงมี BPM ที่แม่นยำ',
             B('เลือกรูปคลื่น:') + ' Needles หรือ Bars', B('Stems ในคลัง:') + ' ใน Library หมวด Tools', B('แชร์จากคิว:') + ' ส่งเพลงที่เล่นอยู่จากเมนูของมัน', 'Hub สว่างขึ้น คิวและปุ่มหมุนใน Studio ลื่นขึ้น แก้ไขข้อบกพร่อง'])],
    also='อ่านเพิ่มเติม: <a href="{stems}">วิธีแยกเสียงร้องออกจากเพลง</a> <a href="{nc}">nightcore บนมือถือ</a> <a href="{bpm}">BPM ของทุกเพลง</a>',
    faq_title='อัปเดต VibeDeck: คำถามที่พบบ่อย',
    faq=[['VibeDeck Player 1.0.21 มีอะไรใหม่', 'Stems แยกเพลงเป็นอะคาเปลลาและดนตรี แอปพอดีกับทุก iPad และ iPhone และปกที่หาเจอแสดงบนหน้าจอล็อก'],
         ['VibeDeck ใช้บน iPad ได้ไหม', 'ได้ VibeDeck พอดีกับทุก iPad และทุก iPhone ทั้งรุ่นเก่าและใหม่'],
         ['VibeDeck ลบเสียงร้องออกจากเพลงได้ไหม', 'ได้ Stems แยกเพลงเป็นอะคาเปลลาและดนตรีบนมือถือ มิกซ์สด เพิ่มเอฟเฟกต์ใน Studio และส่งออกได้'],
         ['รับอัปเดตอย่างไร', 'อัปเดต VibeDeck Player ใน App Store ผู้ใช้ใหม่ดาวน์โหลดได้ฟรี']],
    free_q='ใช้ฟรีไหม', cta='เพลงเดิม ความรู้สึกใหม่ อัปเดตเลย', note='แอปเป็นภาษาอังกฤษ: Stems อยู่ใน Library หมวด Tools')


if __name__ == '__main__':
    for kind, src, name in (('nightcore', NC, 'nightcore'), ('bpm', BPM, 'bpm'), ('whats-new', NEW, 'whats-new')):
        out = {'_note': f'Localized versions of the English {kind} page. Generated by _build/guides_i18n/updates_src.py.'}
        for code in ORDER:
            out[code] = page(kind, code, src[code])
            c = out[code]
            print(kind, code, len(c['title']), len(c['desc']), c['slug'])
        (HERE / f'{name}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
