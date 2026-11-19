#!/usr/bin/env python3
"""Replace the old "core player is free, Premium unlocks the sound engine" sentence.

New model (app 1.0.23): VibeDeck PRO offers a 3-day free trial on the yearly plan, plus
monthly and Lifetime options; the free version plays music with no ads (also in the
background); everything else needs VibeDeck PRO.

    python3 _build/update_pricing_text.py          # rewrite pages
    python3 _build/update_pricing_text.py --check  # exit 1 if an old sentence is left

Plain text replacement, so the visible text and its JSON-LD copy change together.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW = {
    'en': 'VibeDeck PRO offers a 3-day free trial on the yearly plan, plus monthly and Lifetime options. The free version plays your music with no ads, also in the background. VibeDeck PRO unlocks everything else: pitch and tempo, waveform scrubbing, EQ, filter, limiter, VibeMod, TONE, AURA, Studio and the Sampler.',
    'de': 'VibeDeck PRO bietet eine kostenlose 3-tägige Testphase für den Jahrestarif, dazu Monats- und Lifetime-Optionen. Die kostenlose Version spielt deine Musik ohne Werbung ab, auch im Hintergrund. VibeDeck PRO schaltet alles andere frei: Tonhöhe und Tempo, Spulen in der Wellenform, Equalizer, Filter, Limiter, VibeMod, TONE, AURA, Studio und den Sampler.',
    'es': 'VibeDeck PRO ofrece una prueba gratuita de 3 días en el plan anual, además de opciones mensuales y Lifetime. La versión gratuita reproduce tu música sin anuncios, también en segundo plano. VibeDeck PRO desbloquea todo lo demás: tono y tempo, desplazamiento por la forma de onda, ecualizador, filtro, limitador, VibeMod, TONE, AURA, Studio y el Sampler.',
    'fr': 'VibeDeck PRO propose un essai gratuit de 3 jours sur l’abonnement annuel, ainsi que des formules mensuelle et Lifetime. La version gratuite lit votre musique sans publicité, y compris en arrière-plan. VibeDeck PRO débloque tout le reste : hauteur et tempo, navigation sur la forme d’onde, égaliseur, filtre, limiteur, VibeMod, TONE, AURA, Studio et le Sampler.',
    'it': 'VibeDeck PRO offre una prova gratuita di 3 giorni sul piano annuale, oltre a opzioni mensili e Lifetime. La versione gratuita riproduce la tua musica senza pubblicità, anche in background. VibeDeck PRO sblocca tutto il resto: tonalità e tempo, scorrimento sulla forma d’onda, equalizzatore, filtro, limiter, VibeMod, TONE, AURA, Studio e il Sampler.',
    'pt-br': 'O VibeDeck PRO oferece um teste gratuito de 3 dias no plano anual, além de opções mensais e Lifetime. A versão gratuita toca sua música sem anúncios, inclusive em segundo plano. O VibeDeck PRO libera todo o resto: tom e andamento, navegação pela forma de onda, equalizador, filtro, limitador, VibeMod, TONE, AURA, Studio e o Sampler.',
    'ru': 'VibeDeck PRO предлагает бесплатный пробный период 3 дня на годовом тарифе, а также месячный тариф и Lifetime. Бесплатная версия играет вашу музыку без рекламы, в том числе в фоне. VibeDeck PRO открывает всё остальное: высоту тона и темп, перемотку по форме волны, EQ, фильтр, лимитер, VibeMod, TONE, AURA, Studio и Sampler.',
    'ja': 'VibeDeck PROでは年間プランで3日間の無料トライアルが使え、月額プランとLifetimeも選べます。無料版では広告なしで音楽を再生できます（バックグラウンド再生も可能）。ピッチとテンポ、波形でのシーク、EQ、フィルター、リミッター、VibeMod、TONE、AURA、Studio、SamplerはVibeDeck PROで使えます。',
    'ko': 'VibeDeck PRO는 연간 요금제에서 3일 무료 체험을 제공하며, 월간 요금제와 Lifetime도 있습니다. 무료 버전은 광고 없이 음악을 재생하며, 백그라운드 재생도 됩니다. 피치와 템포, 파형 탐색, 이퀄라이저, 필터, 리미터, VibeMod, TONE, AURA, Studio, Sampler는 VibeDeck PRO로 사용할 수 있습니다.',
    'tr': 'VibeDeck PRO, yıllık planda 3 günlük ücretsiz deneme sunar; aylık ve Lifetime seçenekleri de var. Ücretsiz sürüm müziğini reklamsız çalar, arka planda da. VibeDeck PRO geri kalan her şeyin kilidini açar: ton ve tempo, dalga formunda ileri geri sarma, ekolayzer, filtre, limiter, VibeMod, TONE, AURA, Studio ve Sampler.',
    'id': 'VibeDeck PRO menawarkan uji coba gratis 3 hari untuk paket tahunan, plus opsi bulanan dan Lifetime. Versi gratis memutar musikmu tanpa iklan, termasuk di latar belakang. VibeDeck PRO membuka semua yang lain: nada dan tempo, geser di gelombang suara, equalizer, filter, limiter, VibeMod, TONE, AURA, Studio, dan Sampler.',
    'pl': 'VibeDeck PRO oferuje 3-dniowy darmowy okres próbny w planie rocznym, a do tego opcje miesięczne i Lifetime. Darmowa wersja odtwarza Twoją muzykę bez reklam, także w tle. VibeDeck PRO odblokowuje całą resztę: wysokość dźwięku i tempo, przewijanie po fali, korektor, filtr, limiter, VibeMod, TONE, AURA, Studio i Sampler.',
    'nl': 'VibeDeck PRO biedt een gratis proefperiode van 3 dagen op het jaarabonnement, plus maand- en Lifetime-opties. De gratis versie speelt je muziek af zonder advertenties, ook op de achtergrond. VibeDeck PRO ontgrendelt al het andere: toonhoogte en tempo, spoelen op de golfvorm, equalizer, filter, limiter, VibeMod, TONE, AURA, Studio en de Sampler.',
    'vi': 'VibeDeck PRO có bản dùng thử miễn phí 3 ngày cho gói năm, cùng các lựa chọn gói tháng và Lifetime. Bản miễn phí phát nhạc của bạn không quảng cáo, kể cả khi chạy nền. VibeDeck PRO mở khóa mọi thứ còn lại: cao độ và tempo, tua trên dạng sóng, equalizer, filter, limiter, VibeMod, TONE, AURA, Studio và Sampler.',
    'zh-hant': 'VibeDeck PRO 在年繳方案中提供 3 天免費試用，另有月繳和 Lifetime 可選。免費版可以無廣告播放你的音樂，也能在背景播放。音高與速度、波形拖曳、等化器、濾波器、限幅器、VibeMod、TONE、AURA、Studio 和 Sampler 則由 VibeDeck PRO 解鎖。',
    'uk': 'VibeDeck PRO пропонує безкоштовний пробний період 3 дні на річному тарифі, а також місячний тариф і Lifetime. Безкоштовна версія грає вашу музику без реклами, зокрема у фоні. VibeDeck PRO відкриває решту: висоту тону й темп, перемотування за формою хвилі, EQ, фільтр, лімітер, VibeMod, TONE, AURA, Studio та Sampler.',
    'th': 'VibeDeck PRO ให้ทดลองใช้ฟรี 3 วันสำหรับแพ็กเกจรายปี และยังมีแพ็กเกจรายเดือนกับ Lifetime ด้วย เวอร์ชันฟรีเล่นเพลงของคุณได้โดยไม่มีโฆษณา รวมถึงเล่นในเบื้องหลัง ส่วนระดับเสียงและเทมโป การเลื่อนบนรูปคลื่นเสียง อีควอไลเซอร์ ฟิลเตอร์ ลิมิตเตอร์ VibeMod, TONE, AURA, Studio และ Sampler ต้องใช้ VibeDeck PRO',
    'zh-hans': 'VibeDeck PRO 在年付方案中提供 3 天免费试用，另有月付和 Lifetime 可选。免费版可以无广告播放你的音乐，也能在后台播放。音高与速度、波形拖动、均衡器、滤波器、限幅器、VibeMod、TONE、AURA、Studio 和 Sampler 则由 VibeDeck PRO 解锁。',
}

# Old sentence -> language of the replacement
OLD = {
    'The core player is free with no ads. VibeDeck Premium unlocks the full sound engine: pitch and filter, EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.': 'en',
    'The core offline player is free with no ads. Premium unlocks the full sound engine including pitch and filter, EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.': 'en',
    'The core player is free and has no ads. VibeDeck Premium is optional and unlocks the full sound engine: pitch and filter, EQ with gain, limiter, VibeMod, TONE, AURA and Smart Metadata.': 'en',
    'The core player is free with no ads. VibeDeck Premium unlocks the full sound engine.': 'en',
    'Der Basis-Player ist kostenlos und werbefrei. Premium schaltet die komplette Sound-Engine frei: Tonhöhe und Filter, Equalizer mit Gain, Limiter, VibeMod, TONE, AURA und Smart Metadata.': 'de',
    'El reproductor básico es gratis y sin anuncios. Premium desbloquea todo el motor de sonido: tono y filtro, ecualizador con ganancia, limitador, VibeMod, TONE, AURA y Smart Metadata.': 'es',
    'Le lecteur de base est gratuit et sans publicité. Premium débloque tout le moteur sonore : hauteur et filtre, égaliseur avec gain, limiteur, VibeMod, TONE, AURA et Smart Metadata.': 'fr',
    'Il lettore di base è gratuito e senza pubblicità. Premium sblocca il motore audio completo: pitch e filtro, equalizzatore con gain, limiter, VibeMod, TONE, AURA e Smart Metadata.': 'it',
    'O player básico é grátis e sem anúncios. O Premium libera todo o motor de som: tom e filtro, equalizador com ganho, limitador, VibeMod, TONE, AURA e Smart Metadata.': 'pt-br',
    'Базовый плеер бесплатный и без рекламы. Premium открывает весь звуковой движок: высоту тона и фильтр, эквалайзер с усилением, лимитер, VibeMod, TONE, AURA и Smart Metadata.': 'ru',
    '基本のプレーヤーは無料で、広告もありません。Premiumでは、ピッチとフィルター、ゲイン付きEQ、リミッター、VibeMod、TONE、AURA、スマートメタデータなど、すべてのサウンド機能が使えます。': 'ja',
    '기본 플레이어는 무료이고 광고가 없습니다. Premium을 사용하면 피치와 필터, 게인 이퀄라이저, 리미터, VibeMod, TONE, AURA, Smart Metadata까지 사운드 엔진 전체를 쓸 수 있습니다.': 'ko',
    'Temel çalar ücretsiz ve reklamsız. Premium tüm ses motorunun kilidini açar: ton ve filtre, kazançlı ekolayzer, limiter, VibeMod, TONE, AURA ve Smart Metadata.': 'tr',
    'Pemutar dasarnya gratis dan tanpa iklan. Premium membuka seluruh mesin suara: nada dan filter, equalizer dengan gain, limiter, VibeMod, TONE, AURA, dan Smart Metadata.': 'id',
    'Podstawowy odtwarzacz jest darmowy i bez reklam. Premium odblokowuje cały silnik dźwięku: wysokość dźwięku i filtr, korektor ze wzmocnieniem, limiter, VibeMod, TONE, AURA i Smart Metadata.': 'pl',
    'De basisspeler is gratis en zonder advertenties. Premium ontgrendelt de hele geluidsengine: toonhoogte en filter, equalizer met gain, limiter, VibeMod, TONE, AURA en Smart Metadata.': 'nl',
    'Trình phát cơ bản miễn phí và không quảng cáo. Premium mở khóa toàn bộ bộ máy âm thanh: cao độ và filter, equalizer có gain, limiter, VibeMod, TONE, AURA và Smart Metadata.': 'vi',
    '基本播放器免費且無廣告。Premium 解鎖完整音效引擎：音高與濾波器、帶增益的等化器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata。': 'zh-hant',
}

# "How much does it cost?" answers on the language home pages: add the trial after the first sentence
FAQ_FIRST = {
    'de': 'Der Download ist kostenlos und werbefrei.', 'es': 'La descarga es gratis y sin anuncios.',
    'fr': 'Le téléchargement est gratuit et sans publicité.', 'id': 'Unduhannya gratis dan tanpa iklan.',
    'it': 'Il download è gratuito e senza pubblicità.', 'ko': '다운로드는 무료이고 광고가 없습니다.',
    'nl': 'Downloaden is gratis en zonder advertenties.', 'pl': 'Pobranie jest darmowe i bez reklam.',
    'pt-br': 'O download é grátis e sem anúncios.', 'ru': 'Скачать можно бесплатно, рекламы нет.',
    'tr': 'İndirmesi ücretsiz ve reklamsız.', 'vi': 'Tải về miễn phí và không quảng cáo.', 'zh-hant': '下載免費且無廣告。',
}


def trial(lang):
    """First sentence of the new text: the 3-day trial."""
    t = NEW[lang]
    if lang in ('ja', 'zh-hant', 'zh-hans'):
        end = t.index('。') + 1
    elif lang == 'th':
        # Thai has no sentence-ending punctuation: the trial sentence ends
        # right before the second sentence, which starts with "เวอร์ชันฟรี".
        end = t.index(' เวอร์ชันฟรี')
    else:
        end = t.index('. ') + 1
    if lang == 'ja': end = t.index('。', end) + 1  # two short sentences
    return t[:end]


def pages():
    for p in sorted(ROOT.rglob('*.html')):
        if p.relative_to(ROOT).parts[0] not in ('_build', '.github'):
            yield p


def main():
    check = '--check' in sys.argv
    left, changed = [], 0
    for p in pages():
        s = p.read_text(encoding='utf-8'); orig = s
        for old, lang in OLD.items():
            s = s.replace(old, NEW[lang])
        rel = p.relative_to(ROOT).as_posix()
        lang = rel.split('/')[0] if '/' in rel else 'en'
        if rel == f'{lang}/index.html' and lang in FAQ_FIRST:
            first, add = FAQ_FIRST[lang], ' ' + trial(lang)
            if first + add not in s:  # idempotent: add the trial once after each copy of the first sentence
                s = s.replace(first + ' ', first + add + ' ').replace(first + '<', first + add + '<').replace(first + '"', first + add + '"')
        if check:
            if any(old in s for old in OLD): left.append(rel)
        elif s != orig:
            p.write_text(s, encoding='utf-8'); changed += 1
    if check:
        print('\n'.join(left)); sys.exit(1 if left else 0)
    print('updated', changed, 'pages')


if __name__ == '__main__':
    main()
