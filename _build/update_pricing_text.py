#!/usr/bin/env python3
"""Replace the old "core player is free, Premium unlocks the sound engine" sentence.

New model (app 1.0.15, October 2026): 48 hours with everything unlocked for every new
user, no card and no sign-up; after that the free version only plays music (also in
the background); everything else needs VibeDeck PRO.

    python3 _build/update_pricing_text.py          # rewrite pages
    python3 _build/update_pricing_text.py --check  # exit 1 if an old sentence is left

Plain text replacement, so the visible text and its JSON-LD copy change together.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW = {
    'en': 'Every new user gets 48 hours with everything unlocked, with no card and no sign-up. After that the free version plays your music with no ads, also in the background. VibeDeck PRO unlocks everything else: pitch and tempo, waveform scrubbing, EQ, filter, limiter, VibeMod, TONE, AURA, Studio and the Sampler.',
    'de': 'Jeder neue Nutzer bekommt 48 Stunden mit allen Funktionen, ohne Karte und ohne Anmeldung. Danach spielt die kostenlose Version deine Musik ohne Werbung ab, auch im Hintergrund. VibeDeck PRO schaltet alles andere frei: Tonhöhe und Tempo, Spulen in der Wellenform, Equalizer, Filter, Limiter, VibeMod, TONE, AURA, Studio und den Sampler.',
    'es': 'Cada usuario nuevo tiene 48 horas con todo desbloqueado, sin tarjeta y sin registro. Después, la versión gratuita reproduce tu música sin anuncios, también en segundo plano. VibeDeck PRO desbloquea todo lo demás: tono y tempo, desplazamiento por la forma de onda, ecualizador, filtro, limitador, VibeMod, TONE, AURA, Studio y el Sampler.',
    'fr': 'Chaque nouvel utilisateur a 48 heures avec tout débloqué, sans carte et sans inscription. Ensuite, la version gratuite lit votre musique sans publicité, y compris en arrière-plan. VibeDeck PRO débloque tout le reste : hauteur et tempo, navigation sur la forme d’onde, égaliseur, filtre, limiteur, VibeMod, TONE, AURA, Studio et le Sampler.',
    'it': 'Ogni nuovo utente ha 48 ore con tutto sbloccato, senza carta e senza registrazione. Dopo, la versione gratuita riproduce la tua musica senza pubblicità, anche in background. VibeDeck PRO sblocca tutto il resto: tonalità e tempo, scorrimento sulla forma d’onda, equalizzatore, filtro, limiter, VibeMod, TONE, AURA, Studio e il Sampler.',
    'pt-br': 'Todo usuário novo ganha 48 horas com tudo liberado, sem cartão e sem cadastro. Depois disso, a versão gratuita toca sua música sem anúncios, inclusive em segundo plano. O VibeDeck PRO libera todo o resto: tom e andamento, navegação pela forma de onda, equalizador, filtro, limitador, VibeMod, TONE, AURA, Studio e o Sampler.',
    'ru': 'Каждый новый пользователь получает 48 часов со всеми функциями, без карты и без регистрации. Потом бесплатная версия играет вашу музыку без рекламы, в том числе в фоне. VibeDeck PRO открывает всё остальное: высоту тона и темп, перемотку по волне, эквалайзер, фильтр, лимитер, VibeMod, TONE, AURA, Studio и Сэмплер.',
    'ja': '新しいユーザーは48時間、すべての機能を無料で使えます。カードも登録もいりません。その後、無料版では広告なしで音楽を再生できます（バックグラウンド再生も可能）。ピッチとテンポ、波形でのシーク、EQ、フィルター、リミッター、VibeMod、TONE、AURA、Studio、SamplerはVibeDeck PROで使えます。',
    'ko': '모든 신규 사용자는 카드 등록이나 가입 없이 48시간 동안 모든 기능을 사용할 수 있습니다. 그 후 무료 버전은 광고 없이 음악을 재생하며, 백그라운드 재생도 됩니다. 피치와 템포, 파형 탐색, 이퀄라이저, 필터, 리미터, VibeMod, TONE, AURA, Studio, Sampler는 VibeDeck PRO로 사용할 수 있습니다.',
    'tr': 'Her yeni kullanıcı kart ve kayıt olmadan 48 saat boyunca tüm özellikleri kullanır. Sonrasında ücretsiz sürüm müziğini reklamsız çalar, arka planda da. VibeDeck PRO geri kalan her şeyin kilidini açar: ton ve tempo, dalga formunda ileri geri sarma, ekolayzer, filtre, limiter, VibeMod, TONE, AURA, Studio ve Sampler.',
    'id': 'Setiap pengguna baru mendapat 48 jam dengan semua fitur terbuka, tanpa kartu dan tanpa daftar. Setelah itu versi gratis memutar musikmu tanpa iklan, termasuk di latar belakang. VibeDeck PRO membuka semua yang lain: nada dan tempo, geser di gelombang suara, equalizer, filter, limiter, VibeMod, TONE, AURA, Studio, dan Sampler.',
    'pl': 'Każdy nowy użytkownik dostaje 48 godzin ze wszystkimi funkcjami, bez karty i bez rejestracji. Potem darmowa wersja odtwarza Twoją muzykę bez reklam, także w tle. VibeDeck PRO odblokowuje całą resztę: wysokość dźwięku i tempo, przewijanie po fali, korektor, filtr, limiter, VibeMod, TONE, AURA, Studio i Sampler.',
    'nl': 'Elke nieuwe gebruiker krijgt 48 uur met alles ontgrendeld, zonder kaart en zonder account. Daarna speelt de gratis versie je muziek af zonder advertenties, ook op de achtergrond. VibeDeck PRO ontgrendelt al het andere: toonhoogte en tempo, spoelen op de golfvorm, equalizer, filter, limiter, VibeMod, TONE, AURA, Studio en de Sampler.',
    'vi': 'Mỗi người dùng mới được dùng tất cả tính năng trong 48 giờ, không cần thẻ và không cần đăng ký. Sau đó bản miễn phí phát nhạc của bạn không quảng cáo, kể cả khi chạy nền. VibeDeck PRO mở khóa mọi thứ còn lại: cao độ và tempo, tua trên dạng sóng, equalizer, filter, limiter, VibeMod, TONE, AURA, Studio và Sampler.',
    'zh-hant': '每位新用戶都能免費使用全部功能 48 小時，不需綁卡，也不需註冊。之後免費版可以無廣告播放你的音樂，也能在背景播放。音高與速度、波形拖曳、等化器、濾波器、限幅器、VibeMod、TONE、AURA、Studio 和 Sampler 則由 VibeDeck PRO 解鎖。',
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
    """First sentence of the new text: the 48-hour trial."""
    t = NEW[lang]
    end = t.index('。') + 1 if lang in ('ja', 'zh-hant') else t.index('. ') + 1
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
