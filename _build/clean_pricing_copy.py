#!/usr/bin/env python3
"""Idempotent site-wide copy & JSON-LD cleanup across all 18 languages (209 content pages).

Replaces price-related 'Free', 3-day trial, monthly/yearly subscription wording, and USD price tiers
with neutral copy stating availability on iOS and Android with subscription or one-time Lifetime access
inside the app. Preserves technical terms (ad-free, DRM-free, hands-free, distraction-free, free space/storage),
URLs, canonical/hreflang links, GoatCounter, id='premium', layout, and valid JSON-LD.

Usage:
    python3 _build/clean_pricing_copy.py            # apply updates + update sitemap.xml dates
    python3 _build/clean_pricing_copy.py --dry-run  # preview counts without writing
"""
import datetime
import glob
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://vibedeckplayer.app"
TODAY = datetime.date.today().isoformat()

SKIP_FILES = {
    "404.html",
    "privacy.html",
    "support.html",
    "terms.html",
    "vibedeck-vs-music-speed-changer/index.html",
}

HOME_LANGS = {
    "index.html": "en",
    "de/index.html": "de",
    "es/index.html": "es",
    "fr/index.html": "fr",
    "id/index.html": "id",
    "it/index.html": "it",
    "ja/index.html": "ja",
    "ko/index.html": "ko",
    "nl/index.html": "nl",
    "pl/index.html": "pl",
    "pt-br/index.html": "pt-br",
    "ru/index.html": "ru",
    "th/index.html": "th",
    "tr/index.html": "tr",
    "uk/index.html": "uk",
    "vi/index.html": "vi",
    "zh-hans/index.html": "zh-hans",
    "zh-hant/index.html": "zh-hant",
}

# ------------------------------------------------------------------ 1. #premium neutral block (18 languages)
PREMIUM_BLOCK = {
    "en": (
        "VibeDeck Player is available on iOS and Android. VibeDeck PRO unlocks the full sound toolkit: pitch and tempo, waveform scrubbing, 3-band DJ EQ and 8-band equalizer, filter, limiter, VibeMod, TONE, AURA, Studio, Stems and Sampler.",
        "Available via subscription or one-time Lifetime access inside the app on the App Store and Google Play. No ads, no account, no tracking.",
    ),
    "de": (
        "VibeDeck Player ist für iOS und Android verfügbar. VibeDeck PRO schaltet alle Sound-Werkzeuge frei: Tonhöhe und Tempo, Spulen in der Wellenform, 3-Band-DJ-EQ und 8-Band-Equalizer, Filter, Limiter, VibeMod, TONE, AURA, Studio, Stems und Sampler.",
        "Zugang per Abo oder einmaligem Lifetime-Kauf direkt in der App über den App Store und Google Play. Keine Werbung, kein Konto, kein Tracking.",
    ),
    "es": (
        "VibeDeck Player está disponible en iOS y Android. VibeDeck PRO desbloquea todas las herramientas de sonido: tono y tempo, desplazamiento por la forma de onda, EQ DJ de 3 bandas y ecualizador de 8 bandas, filtro, limitador, VibeMod, TONE, AURA, Studio, Stems y Sampler.",
        "Disponible mediante suscripción o acceso Lifetime de pago único dentro de la app en App Store y Google Play. Sin anuncios, sin cuenta y sin rastreo.",
    ),
    "fr": (
        "VibeDeck Player est disponible sur iOS et Android. VibeDeck PRO débloque tous les outils sonores : hauteur et tempo, navigation sur la forme d’onde, EQ DJ 3 bandes et égaliseur 8 bandes, filtre, limiteur, VibeMod, TONE, AURA, Studio, Stems et Sampler.",
        "Accessible par abonnement ou via un accès Lifetime en paiement unique dans l’application sur l’App Store et Google Play. Sans publicité, sans compte et sans suivi.",
    ),
    "id": (
        "VibeDeck Player tersedia di iOS dan Android. VibeDeck PRO membuka seluruh alat suara: nada dan tempo, geser pada gelombang suara, EQ DJ 3 band dan equalizer 8 band, filter, limiter, VibeMod, TONE, AURA, Studio, Stems, dan Sampler.",
        "Tersedia melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi lewat App Store dan Google Play. Tanpa iklan, tanpa akun, tanpa pelacakan.",
    ),
    "it": (
        "VibeDeck Player è disponibile su iOS e Android. VibeDeck PRO sblocca tutti gli strumenti audio: tonalità e tempo, scorrimento sulla forma d’onda, EQ DJ a 3 bande ed equalizzatore a 8 bande, filtro, limiter, VibeMod, TONE, AURA, Studio, Stems e Sampler.",
        "Disponibile tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app su App Store e Google Play. Senza pubblicità, senza account e senza tracciamento.",
    ),
    "ja": (
        "VibeDeck PlayerはiOSとAndroidで利用できます。VibeDeck PROでは、ピッチとテンポ、波形でのシーク、3バンドDJ EQと8バンドイコライザー、フィルター、リミッター、VibeMod、TONE、AURA、Studio、Stems、Samplerなどすべてのサウンド機能が使えます。",
        "アプリ内のサブスクリプションまたは買い切りのLifetimeアクセスでご利用いただけます（App Store・Google Play対応）。広告なし、アカウント不要、トラッキングなし。",
    ),
    "ko": (
        "VibeDeck Player는 iOS와 Android에서 이용할 수 있습니다. VibeDeck PRO로 피치와 템포, 파형 탐색, 3밴드 DJ EQ 및 8밴드 이퀄라이저, 필터, 리미터, VibeMod, TONE, AURA, Studio, Stems, Sampler 등 모든 사운드 도구를 사용할 수 있습니다.",
        "App Store와 Google Play의 앱 내에서 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다. 광고, 계정, 추적이 없습니다.",
    ),
    "nl": (
        "VibeDeck Player is beschikbaar op iOS en Android. VibeDeck PRO ontgrendelt alle geluidstools: toonhoogte en tempo, spoelen op de golfvorm, 3-bands DJ-EQ en 8-bands equalizer, filter, limiter, VibeMod, TONE, AURA, Studio, Stems en Sampler.",
        "Beschikbaar via een abonnement of eenmalige Lifetime-toegang in de app via de App Store en Google Play. Geen advertenties, geen account en geen tracking.",
    ),
    "pl": (
        "VibeDeck Player jest dostępny na iOS i Androida. VibeDeck PRO odblokowuje wszystkie narzędzia dźwięku: wysokość dźwięku i tempo, przewijanie po fali, 3-pasmowy korektor DJ i 8-pasmowy equalizer, filtr, limiter, VibeMod, TONE, AURA, Studio, Stems i Sampler.",
        "Dostępny w ramach subskrypcji lub jednorazowego dostępu Lifetime wewnątrz aplikacji w App Store i Google Play. Bez reklam, bez konta i bez śledzenia.",
    ),
    "pt-br": (
        "O VibeDeck Player está disponível para iOS e Android. O VibeDeck PRO libera todas as ferramentas de som: tom e andamento, navegação pela forma de onda, EQ DJ de 3 bandas e equalizador de 8 bandas, filtro, limitador, VibeMod, TONE, AURA, Studio, Stems e Sampler.",
        "Disponível por assinatura ou acesso Lifetime em pagamento único dentro do aplicativo na App Store e no Google Play. Sem anúncios, sem conta e sem rastreamento.",
    ),
    "ru": (
        "VibeDeck Player доступен на iOS и Android. VibeDeck PRO открывает все инструменты звука: высоту тона и темп, перемотку по форме волны, 3-полосный DJ эквалайзер и 8-полосный эквалайзер, фильтр, лимитер, VibeMod, TONE, AURA, Studio, Stems и Sampler.",
        "Доступен по подписке или с разовым Lifetime-доступом внутри приложения в App Store и Google Play. Без рекламы, без аккаунта и без трекинга.",
    ),
    "th": (
        "VibeDeck Player พร้อมใช้งานบน iOS และ Android โดย VibeDeck PRO ปลดล็อกเครื่องมือเสียงครบชุด ทั้งระดับเสียงและเทมโป การเลื่อนบนรูปคลื่นเสียง DJ EQ 3 แบนด์และอีควอไลเซอร์ 8 แบนด์ ฟิลเตอร์ ลิมิตเตอร์ VibeMod, TONE, AURA, Studio, Stems และ Sampler",
        "เลือกใช้งานได้ทั้งแบบสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอปบน App Store และ Google Play ไม่มีโฆษณา ไม่ต้องมีบัญชี ไม่มีการติดตาม",
    ),
    "tr": (
        "VibeDeck Player, iOS ve Android için kullanılabilir. VibeDeck PRO tüm ses araçlarının kilidini açar: perde ve tempo, dalga formunda gezinme, 3 bantlı DJ EQ ve 8 bantlı ekolayzer, filtre, limiter, VibeMod, TONE, AURA, Studio, Stems ve Sampler.",
        "App Store ve Google Play üzerinden uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir. Reklam yok, hesap yok, takip yok.",
    ),
    "uk": (
        "VibeDeck Player доступний на iOS та Android. VibeDeck PRO відкриває всі інструменти звуку: висоту тону й темп, перемотування за формою хвилі, 3-смуговий DJ еквалайзер і 8-смуговий еквалайзер, фільтр, лімітер, VibeMod, TONE, AURA, Studio, Stems та Sampler.",
        "Доступний за підпискою або з разовим Lifetime-доступом усередині застосунку в App Store та Google Play. Без реклами, без акаунта і без трекінгу.",
    ),
    "vi": (
        "VibeDeck Player có mặt trên iOS và Android. VibeDeck PRO mở khóa toàn bộ công cụ âm thanh: cao độ và tempo, tua trên dạng sóng, EQ DJ 3 dải và equalizer 8 dải, filter, limiter, VibeMod, TONE, AURA, Studio, Stems và Sampler.",
        "Có gói đăng ký hoặc quyền truy cập Lifetime trả một lần ngay trong ứng dụng trên App Store và Google Play. Không quảng cáo, không tài khoản, không theo dõi.",
    ),
    "zh-hans": (
        "VibeDeck Player 支持 iOS 和 Android。VibeDeck PRO 解锁完整音效工具：音高与速度、波形拖动、3 段 DJ EQ 与 8 段均衡器、滤波器、限幅器、VibeMod、TONE、AURA、Studio、Stems 和 Sampler。",
        "可在 App Store 和 Google Play 的应用内选择订阅或一次性购买 Lifetime 权限。无广告、免账号、不追踪。",
    ),
    "zh-hant": (
        "VibeDeck Player 支援 iOS 與 Android。VibeDeck PRO 解鎖完整音效工具：音高與速度、波形拖曳、3 段 DJ EQ 與 8 段等化器、濾波器、限幅器、VibeMod、TONE、AURA、Studio、Stems 與 Sampler。",
        "可在 App Store 與 Google Play 的 App 內選擇訂閱或一次性購買 Lifetime 權限。無廣告、免帳號、不追蹤。",
    ),
}

# ------------------------------------------------------------------ 2. Glance table Access row (18 languages)
GLANCE_ROW = {
    "en": (
        "Access",
        'Available on iOS and Android; subscription or one-time Lifetime access inside the app (<a href="https://apps.apple.com/app/vibedeck-player/id6784724920?pt=129091862&amp;ct=home&amp;mt=8">App Store</a> · <a href="https://play.google.com/store/apps/details?id=com.vibedeck.player&amp;referrer=utm_source%3Dvibedeckplayer.app%26utm_medium%3Dwebsite%26utm_campaign%3Dhome">Google Play</a>)',
    ),
    "de": ("Zugang", "Verfügbar für iOS und Android; Abo oder einmaliger Lifetime-Zugang in der App"),
    "es": ("Acceso", "Disponible en iOS y Android; suscripción o acceso Lifetime de pago único dentro de la app"),
    "fr": ("Accès", "Disponible sur iOS et Android ; abonnement ou accès Lifetime en paiement unique dans l’application"),
    "id": ("Akses", "Tersedia di iOS dan Android; langganan atau akses Lifetime sekali bayar di dalam aplikasi"),
    "it": ("Accesso", "Disponibile su iOS e Android; abbonamento o accesso Lifetime con pagamento unico nell’app"),
    "ja": ("利用方法", "iOS・Android対応。アプリ内でサブスクリプションまたは買い切りLifetimeアクセスを利用可能"),
    "ko": ("이용 방식", "iOS 및 Android 지원, 앱 내에서 구독 또는 일회성 Lifetime 이용권 선택 가능"),
    "nl": ("Toegang", "Beschikbaar op iOS en Android; abonnement of eenmalige Lifetime-toegang in de app"),
    "pl": ("Dostęp", "Dostępny na iOS i Androida; subskrypcja lub jednorazowy dostęp Lifetime w aplikacji"),
    "pt-br": ("Acesso", "Disponível para iOS e Android; assinatura ou acesso Lifetime em pagamento único no app"),
    "ru": ("Доступ", "Доступен на iOS и Android; подписка или разовый Lifetime-доступ внутри приложения"),
    "th": ("การเข้าถึง", "ใช้งานได้บน iOS และ Android พร้อมตัวเลือกสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวในแอป"),
    "tr": ("Erişim", "iOS ve Android için mevcut; uygulama içi abonelik veya tek seferlik Lifetime erişimi"),
    "uk": ("Доступ", "Доступний на iOS та Android; підписка або разовий Lifetime-доступ усередині застосунку"),
    "vi": ("Quyền truy cập", "Có trên iOS và Android; gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng"),
    "zh-hans": ("获取方式", "支持 iOS 和 Android，应用内提供订阅或一次性 Lifetime 权限"),
    "zh-hant": ("取得方式", "支援 iOS 與 Android，App 內提供訂閱或一次性 Lifetime 權限"),
}

OLD_GLANCE_LABELS = [
    "Price", "Preis", "Precio", "Prix", "Harga", "Prezzo", "料金", "가격",
    "Prijs", "Cena", "Preço", "Цена", "ราคา", "Fiyat", "Ціна", "Giá", "价格", "價格",
    "Access", "Zugang", "Acceso", "Accès", "Akses", "Accesso", "利用方法", "이용 방식",
    "Toegang", "Dostęp", "Acesso", "Доступ", "การเข้าถึง", "Erişim", "Quyền truy cập", "获取方式", "取得方式",
]

# ------------------------------------------------------------------ 3. Share messages (18 languages)
SHARE_MSG = {
    "en": "VibeDeck Player: an offline music player that changes pitch and tempo and records sound from YouTube, TikTok and more. Available on iOS and Android.",
    "ja": "VibeDeck Player：キーとテンポを変えられて、YouTubeやTikTokなどの音を録音できるオフラインプレーヤー。iOS・Android対応。",
    "es": "VibeDeck Player: reproductor sin conexión que cambia el tono y el tempo y graba el sonido de YouTube, TikTok y más. Disponible en iOS y Android.",
    "pt-br": "VibeDeck Player: player offline que muda o tom e o andamento e grava o som do YouTube, do TikTok e mais. Disponível para iOS e Android.",
    "de": "VibeDeck Player: Offline-Musikplayer, der Tonart und Tempo ändert und den Ton von YouTube, TikTok und mehr aufnimmt. Für iOS und Android.",
    "fr": "VibeDeck Player : un lecteur hors ligne qui change la tonalité et le tempo et enregistre le son de YouTube, TikTok et plus. Disponible sur iOS et Android.",
    "it": "VibeDeck Player: lettore offline che cambia tonalità e tempo e registra l'audio di YouTube, TikTok e altro. Disponibile su iOS e Android.",
    "ru": "VibeDeck Player: офлайн-плеер, который меняет тональность и темп и записывает звук из YouTube, TikTok и не только. Доступен на iOS и Android.",
    "uk": "VibeDeck Player: офлайн-плеєр, який змінює тональність і темп та записує звук із YouTube, TikTok та не лише. Доступний на iOS та Android.",
    "ko": "VibeDeck Player: 키와 템포를 바꾸고 YouTube, TikTok 등의 소리를 녹음하는 오프라인 플레이어. iOS 및 Android 지원.",
    "tr": "VibeDeck Player: tonu ve tempoyu değiştiren, YouTube, TikTok ve daha fazlasının sesini kaydeden çevrimdışı çalar. iOS ve Android için.",
    "id": "VibeDeck Player: pemutar offline yang bisa mengubah nada dan tempo serta merekam suara dari YouTube, TikTok, dan lainnya. Tersedia di iOS dan Android.",
    "pl": "VibeDeck Player: odtwarzacz offline, który zmienia tonację i tempo i nagrywa dźwięk z YouTube, TikToka i nie tylko. Dostępny na iOS i Androida.",
    "nl": "VibeDeck Player: offline speler die toonhoogte en tempo verandert en geluid van YouTube, TikTok en meer opneemt. Beschikbaar voor iOS en Android.",
    "vi": "VibeDeck Player: trình phát offline đổi tone và tempo, ghi lại âm thanh từ YouTube, TikTok và hơn thế nữa. Có mặt trên iOS và Android.",
    "zh-hant": "VibeDeck Player：能升降調、改速度，還能錄下 YouTube、TikTok 等 App 聲音的離線播放器。支援 iOS 與 Android。",
    "zh-hans": "VibeDeck Player：能升降调、改速度，还能录下 YouTube、TikTok 等 App 声音的离线播放器。支持 iOS 和 Android。",
    "th": "VibeDeck Player: เครื่องเล่นเพลงออฟไลน์ที่ปรับคีย์และเทมโปได้ และอัดเสียงจาก YouTube, TikTok และอื่น ๆ ได้ พร้อมใช้งานบน iOS และ Android",
}

# ------------------------------------------------------------------ 4. 14 localized MP3 pages Title & H1
MP3_TITLE_H1 = {
    "de/mp3-player-ohne-werbung/index.html": (
        "MP3-Player ohne Werbung und offline | VibeDeck",
        '<span class="h1-plain">MP3-Player ohne Werbung</span> <span class="h1-sub">Offline, ohne Konto, ohne Tracking</span>',
    ),
    "es/reproductor-mp3-sin-anuncios/index.html": (
        None,  # title already clean
        '<span class="h1-plain">Reproductor MP3 sin anuncios</span> <span class="h1-sub">Sin conexión, sin cuenta y sin rastreo</span>',
    ),
    "fr/lecteur-mp3-sans-pub/index.html": (
        "Lecteur MP3 sans pub et hors ligne | VibeDeck",
        '<span class="h1-plain">Lecteur MP3 sans pub</span> <span class="h1-sub">Hors ligne, sans compte, sans pistage</span>',
    ),
    "id/pemutar-mp3-tanpa-iklan/index.html": (
        "Pemutar MP3 offline tanpa iklan | VibeDeck",
        '<span class="h1-plain">Pemutar MP3 tanpa iklan</span> <span class="h1-sub">Offline, tanpa akun, tanpa pelacakan</span>',
    ),
    "it/lettore-mp3-senza-pub/index.html": (
        "Lettore MP3 offline e senza pubblicità | VibeDeck",
        '<span class="h1-plain">Lettore MP3 senza pubblicità</span> <span class="h1-sub">Offline, senza account, senza tracciamento</span>',
    ),
    "ko/mp3-player/index.html": (
        "광고 없는 오프라인 MP3 플레이어 | VibeDeck",
        '<span class="h1-plain">광고 없는 MP3 플레이어</span> <span class="h1-sub">오프라인, 계정 불필요, 추적 없음</span>',
    ),
    "nl/mp3-speler-zonder-advertenties/index.html": (
        "Offline MP3-speler zonder advertenties | VibeDeck",
        '<span class="h1-plain">MP3-speler zonder advertenties</span> <span class="h1-sub">Offline, zonder account, zonder tracking</span>',
    ),
    "pl/odtwarzacz-mp3-bez-reklam/index.html": (
        "Odtwarzacz MP3 offline bez reklam | VibeDeck",
        '<span class="h1-plain">Odtwarzacz MP3 bez reklam</span> <span class="h1-sub">Offline, bez konta, bez śledzenia</span>',
    ),
    "ru/mp3-pleer-bez-reklamy/index.html": (
        "MP3-плеер без рекламы и интернета | VibeDeck",
        '<span class="h1-plain">MP3-плеер без рекламы</span> <span class="h1-sub">Без интернета, без аккаунта, без слежки</span>',
    ),
    "th/mp3-player-mai-mi-khotsana/index.html": (
        "เครื่องเล่น MP3 ไม่มีโฆษณา ใช้ออฟไลน์ | VibeDeck",
        '<span class="h1-plain">เครื่องเล่น MP3 ไม่มีโฆษณา</span> <span class="h1-sub">ออฟไลน์ ไม่ต้องมีบัญชี ไม่มีการติดตาม</span>',
    ),
    "tr/reklamsiz-mp3-calar/index.html": (
        "Çevrimdışı ve reklamsız MP3 çalar | VibeDeck",
        '<span class="h1-plain">Reklamsız MP3 çalar</span> <span class="h1-sub">Çevrimdışı, hesapsız, takipsiz</span>',
    ),
    "vi/trinh-phat-mp3-khong-quang-cao/index.html": (
        "Trình phát MP3 offline, không quảng cáo | VibeDeck",
        '<span class="h1-plain">Trình phát MP3 không quảng cáo</span> <span class="h1-sub">Offline, không tài khoản, không theo dõi</span>',
    ),
    "zh-hans/mp3-player/index.html": (
        "离线无广告 MP3 播放器 | VibeDeck",
        '<span class="h1-plain">无广告 MP3 播放器</span> <span class="h1-sub">离线、免账号、不追踪</span>',
    ),
    "zh-hant/mp3-player/index.html": (
        "離線無廣告 MP3 播放器 | VibeDeck",
        '<span class="h1-plain">無廣告 MP3 播放器</span> <span class="h1-sub">離線、免帳號、不追蹤</span>',
    ),
}

# ------------------------------------------------------------------ 5. Meta descriptions (exact string map)
META_DESC_MAP = {
    # English
    "Free offline music player and speed changer for iPhone and Android. Plays MP3, AAC, M4A, WAV, AIFF and FLAC. Pitch, filter, EQ, limiter, AURA and TONE require PRO. No ads, no account.":
        "Offline music player and speed changer for iOS and Android. Plays MP3, AAC, M4A, WAV, AIFF and FLAC with EQ, pitch and tempo. No ads, no account.",
    "An MP3 player with no ads, no account and no tracking. Play your MP3 files offline on iPhone and Android with EQ, pitch and tempo. Download VibeDeck free.":
        "An MP3 player with no ads, no account and no tracking. Play your MP3 files offline on iOS and Android with EQ, pitch and tempo control.",
    "Play MP3, FLAC and WAV on Android with no internet, no ads and no account. EQ, pitch and tempo control. Free download on Google Play.":
        "Play MP3, FLAC and WAV on Android with no internet, no ads and no account. EQ, pitch and tempo control. Available on Google Play.",
    "Play lossless FLAC files offline on iPhone and iPad with an EQ, pitch and tempo control. No ads, no account, no tracking. Download VibeDeck free.":
        "Play lossless FLAC files offline on iPhone and iPad with EQ, pitch and tempo control. No ads, no account, no tracking. Available on the App Store.",
    "Play lossless FLAC on Android offline with an EQ, pitch and tempo control. Also WAV and MP3. No ads, no account. Free on Google Play.":
        "Play lossless FLAC on Android offline with EQ, pitch and tempo control. Also WAV and MP3. No ads, no account. Available on Google Play.",
    "Shift a song’s key by ±8 st and change its tempo independently, offline on iPhone and Android. For singers, musicians, dancers and DJs. Free.":
        "Shift a song’s key by ±8 st and change its tempo independently, offline on iOS and Android. Built for singers, musicians, dancers and DJs.",
    "Your whole music library offline on iPhone and iPad: MP3, FLAC and WAV. No WiFi, no streaming subscription, no ads. EQ, pitch and tempo. Download free.":
        "Your whole music library offline on iPhone and iPad: MP3, FLAC and WAV. No WiFi, no streaming, no ads. EQ, pitch and tempo control.",
    # German
    "Spiele MP3, AAC, M4A, WAV, AIFF und FLAC ohne Internet auf iPhone und Android. Keine Werbung, kein Konto. Tonart (±8 st), Tempo und EQ anpassen. Kostenlos.":
        "Spiele MP3, AAC, M4A, WAV, AIFF und FLAC ohne Internet auf iOS und Android. Keine Werbung, kein Konto. Tonart (±8 st), Tempo und EQ.",
    "Kostenloser MP3-Player ohne Werbung, ohne Konto und ohne Tracking für iPhone und Android. Deine Dateien ohne Internet, mit Equalizer, Tonart und Tempo.":
        "Offline-MP3-Player ohne Werbung, ohne Konto und ohne Tracking für iOS und Android. Deine Dateien ohne Internet, mit Equalizer, Tonart und Tempo.",
    # Spanish
    "Reproduce MP3, AAC, M4A, WAV, AIFF y FLAC sin internet en iPhone y Android. Sin anuncios ni cuenta. Cambia el tono (±8 st), el tempo y el ecualizador. Gratis.":
        "Reproduce MP3, AAC, M4A, WAV, AIFF y FLAC sin internet en iOS y Android. Sin anuncios ni cuenta. Cambia el tono (±8 st), el tempo y el ecualizador.",
    "Reproductor MP3 gratis, sin anuncios, sin cuenta y sin rastreo para iPhone y Android. Tus archivos sin internet, con ecualizador, tono y tempo.":
        "Reproductor MP3 sin conexión, sin anuncios, sin cuenta y sin rastreo para iOS y Android. Tus archivos sin internet, con ecualizador, tono y tempo.",
    # French
    "Écoutez MP3, AAC, M4A, WAV, AIFF et FLAC sans internet sur iPhone et Android. Sans pub ni compte. Tonalité (±8 st), tempo et égaliseur. Gratuit.":
        "Écoutez MP3, AAC, M4A, WAV, AIFF et FLAC sans internet sur iOS et Android. Sans pub ni compte. Tonalité (±8 st), tempo et égaliseur.",
    "Lecteur MP3 gratuit sans pub, sans compte et sans pistage pour iPhone et Android. Vos fichiers sans internet, avec égaliseur, tonalité et tempo.":
        "Lecteur MP3 hors ligne sans pub, sans compte et sans pistage pour iOS et Android. Vos fichiers sans internet, avec égaliseur, tonalité et tempo.",
    # Indonesian
    "Putar MP3, AAC, M4A, WAV, AIFF dan FLAC tanpa internet di iPhone dan Android. Tanpa iklan dan akun. Nada (±8 semitone), tempo, dan equalizer. Gratis.":
        "Putar MP3, AAC, M4A, WAV, AIFF, dan FLAC tanpa internet di iOS dan Android. Tanpa iklan dan akun. Nada (±8 semitone), tempo, dan equalizer.",
    "Pemutar MP3 gratis tanpa iklan, akun, dan pelacakan untuk iPhone dan Android. File kamu tanpa internet, dengan equalizer, nada, dan tempo.":
        "Pemutar MP3 offline tanpa iklan, akun, dan pelacakan untuk iOS dan Android. File kamu tanpa internet, dengan equalizer, nada, dan tempo.",
    # Italian
    "Ascolta MP3, AAC, M4A, WAV, AIFF e FLAC offline su iPhone e Android, senza pubblicità o account. Pitch, tempo ed EQ con PRO. Download gratuito.":
        "Ascolta MP3, AAC, M4A, WAV, AIFF e FLAC offline su iOS e Android, senza pubblicità o account. Pitch, tempo ed EQ con VibeDeck PRO.",
    "Lettore MP3 gratuito senza pubblicità, account o tracciamento per iPhone e Android. Riproduzione offline; equalizzatore, pitch e tempo con PRO.":
        "Lettore MP3 offline senza pubblicità, account o tracciamento per iOS e Android. Riproduzione locale; equalizzatore, pitch e tempo con PRO.",
    "Trasponi i brani fino a ±8 st senza cambiare il tempo. Per cantare ed esercitarti su iPhone e Android. Pitch con PRO; download gratuito.":
        "Trasponi i brani fino a ±8 st senza cambiare il tempo. Per cantare ed esercitarti su iOS e Android. Controllo pitch incluso in VibeDeck PRO.",
    # Japanese
    "iPhone・Androidで手持ちの音楽ファイルをオフライン再生。MP3・AAC・M4A・WAV・AIFF・FLAC対応、広告なし・アカウント不要。キー変更（±8 st）、テンポ、EQ、リミッターも。無料ダウンロード。":
        "iOS・Androidで手持ちの音楽ファイルをオフライン再生。MP3・AAC・M4A・WAV・AIFF・FLAC対応、広告なし・アカウント不要。キー変更（±8 st）、テンポ、EQ、リミッター搭載。",
    # Korean
    "iPhone과 Android에서 MP3, AAC, M4A, WAV, AIFF, FLAC를 인터넷 없이 재생하세요. 광고와 계정 없이 키(±8 반음), 템포, 이퀄라이저를 조절할 수 있습니다. 무료.":
        "iOS와 Android에서 MP3, AAC, M4A, WAV, AIFF, FLAC를 인터넷 없이 재생하세요. 광고와 계정 없이 키(±8 반음), 템포, 이퀄라이저를 조절할 수 있습니다.",
    "iPhone과 Android용 무료 MP3 플레이어. 광고, 계정, 추적 없이 내 파일을 인터넷 없이 재생하고 이퀄라이저, 키, 템포를 조절하세요.":
        "iOS와 Android용 오프라인 MP3 플레이어. 광고, 계정, 추적 없이 내 파일을 인터넷 없이 재생하고 이퀄라이저, 키, 템포를 조절하세요.",
    # Dutch
    "Speel MP3, AAC, M4A, WAV, AIFF en FLAC af zonder internet op iPhone en Android. Geen advertenties, geen account. Toonhoogte (±8 halve tonen), tempo en equalizer. Gratis.":
        "Speel MP3, AAC, M4A, WAV, AIFF en FLAC af zonder internet op iOS en Android. Geen advertenties, geen account. Toonhoogte (±8 halve tonen), tempo en equalizer.",
    "Gratis MP3-speler zonder advertenties, account of tracking voor iPhone en Android. Je bestanden zonder internet, met equalizer, toonhoogte en tempo.":
        "Offline MP3-speler zonder advertenties, account of tracking voor iOS en Android. Je bestanden zonder internet, met equalizer, toonhoogte en tempo.",
    # Polish
    "Słuchaj MP3, AAC, M4A, WAV, AIFF i FLAC bez internetu na iPhonie i Androidzie. Bez reklam i konta. Tonacja (±8 półtonów), tempo i korektor. Za darmo.":
        "Słuchaj MP3, AAC, M4A, WAV, AIFF i FLAC bez internetu na iOS i Androidzie. Bez reklam i konta. Tonacja (±8 półtonów), tempo i korektor.",
    "Darmowy odtwarzacz MP3 bez reklam, konta i śledzenia na iPhone’a i Androida. Twoje pliki bez internetu, z korektorem, tonacją i tempem.":
        "Odtwarzacz MP3 offline bez reklam, konta i śledzenia na iOS i Androida. Twoje pliki bez internetu, z korektorem, tonacją i tempem.",
    # Portuguese (BR)
    "Ouça MP3, AAC, M4A, WAV, AIFF e FLAC sem internet no Android e no iPhone. Sem anúncios e sem conta. Mude o tom (±8 st), a velocidade e o equalizador. Grátis.":
        "Ouça MP3, AAC, M4A, WAV, AIFF e FLAC sem internet no iOS e no Android. Sem anúncios e sem conta. Mude o tom (±8 st), a velocidade e o equalizador.",
    "Ouça MP3, AAC, M4A, WAV, AIFF e FLAC sem internet no Android. Sem anúncios, sem conta e sem rastreamento. Equalizador, tom e andamento. Download grátis no Google Play.":
        "Ouça MP3, AAC, M4A, WAV, AIFF e FLAC sem internet no Android. Sem anúncios, sem conta e sem rastreamento. Equalizador, tom e andamento no Google Play.",
    # Russian
    "Слушайте MP3, AAC, M4A, WAV, AIFF и FLAC без интернета на iPhone и Android. Без рекламы и аккаунта. Тональность (±8 полутонов), темп и эквалайзер. Бесплатно.":
        "Слушайте MP3, AAC, M4A, WAV, AIFF и FLAC без интернета на iOS и Android. Без рекламы и аккаунта. Тональность (±8 полутонов), темп и эквалайзер.",
    "Бесплатный MP3-плеер без рекламы, аккаунта и слежки для iPhone и Android. Ваши файлы без интернета, с эквалайзером, тональностью и темпом.":
        "Офлайн MP3-плеер без рекламы, аккаунта и слежки для iOS и Android. Ваши файлы без интернета, с эквалайзером, тональностью и темпом.",
    # Thai
    "ฟัง MP3, AAC, M4A, WAV, AIFF และ FLAC โดยไม่ต้องใช้เน็ตบน iPhone และ Android ไม่มีโฆษณา ไม่ต้องมีบัญชี ปรับคีย์ (±8 เซมิโทน) เทมโป และอีควอไลเซอร์ได้ ดาวน์โหลดฟรี":
        "ฟัง MP3, AAC, M4A, WAV, AIFF และ FLAC โดยไม่ต้องใช้เน็ตบน iOS และ Android ไม่มีโฆษณา ไม่ต้องมีบัญชี ปรับคีย์ (±8 เซมิโทน) เทมโป และอีควอไลเซอร์ได้",
    "เครื่องเล่น MP3 ฟรี ไม่มีโฆษณา ไม่ต้องมีบัญชี ไม่มีการติดตาม สำหรับ iPhone และ Android ฟังไฟล์ของคุณโดยไม่ต้องใช้เน็ต พร้อมอีควอไลเซอร์ คีย์ และเทมโป":
        "เครื่องเล่น MP3 ออฟไลน์ ไม่มีโฆษณา ไม่ต้องมีบัญชี ไม่มีการติดตาม สำหรับ iOS และ Android ฟังไฟล์ของคุณโดยไม่ต้องใช้เน็ต พร้อมอีควอไลเซอร์ คีย์ และเทมโป",
    # Turkish
    "iPhone ve Android’de MP3, AAC, M4A, WAV, AIFF ve FLAC’ı internetsiz dinle. Reklam ve hesap yok. Ton (±8 yarım ton), tempo ve ekolayzer. Ücretsiz.":
        "iOS ve Android’de MP3, AAC, M4A, WAV, AIFF ve FLAC’ı internetsiz dinle. Reklam ve hesap yok. Ton (±8 yarım ton), tempo ve ekolayzer.",
    "iPhone ve Android için reklamsız, hesapsız ve takipsiz ücretsiz MP3 çalar. Dosyaların internetsiz; ekolayzer, ton ve tempo ayarıyla.":
        "iOS ve Android için reklamsız, hesapsız ve takipsiz çevrimdışı MP3 çalar. Dosyaların internetsiz; ekolayzer, ton ve tempo ayarıyla.",
    # Ukrainian
    "Слухайте MP3, AAC, M4A, WAV, AIFF і FLAC без інтернету на iPhone та Android. Без реклами й акаунта. Тональність (±8 півтонів), темп і еквалайзер. Безкоштовно.":
        "Слухайте MP3, AAC, M4A, WAV, AIFF і FLAC без інтернету на iOS та Android. Без реклами й акаунта. Тональність (±8 півтонів), темп і еквалайзер.",
    # Vietnamese
    "Nghe MP3, AAC, M4A, WAV, AIFF và FLAC không cần internet trên iPhone và Android. Không quảng cáo, không tài khoản. Tone (±8 nửa cung), tempo và equalizer. Miễn phí.":
        "Nghe MP3, AAC, M4A, WAV, AIFF và FLAC không cần internet trên iOS và Android. Không quảng cáo, không tài khoản. Tone (±8 nửa cung), tempo và equalizer.",
    "Trình phát MP3 miễn phí không quảng cáo, không tài khoản, không theo dõi cho iPhone và Android. File của bạn không cần internet, có equalizer, tone và tempo.":
        "Trình phát MP3 offline không quảng cáo, không tài khoản, không theo dõi cho iOS và Android. File của bạn không cần internet, có equalizer, tone và tempo.",
    # Simplified Chinese
    "在 iPhone 和 Android 上不用网络播放 MP3、AAC、M4A、WAV、AIFF 和 FLAC。无广告、免账号。音调（±8 个半音）、速度和均衡器。免费。":
        "在 iOS 和 Android 上不用网络播放 MP3、AAC、M4A、WAV、AIFF 和 FLAC。无广告、免账号。支持音调（±8 个半音）、速度和均衡器。",
    "适用于 iPhone 和 Android 的免费 MP3 播放器，无广告、免账号、不追踪。不用网络播放你的文件，还能调整均衡器、音调和速度。":
        "适用于 iOS 和 Android 的离线 MP3 播放器，无广告、免账号、不追踪。不用网络播放你的文件，还能调整均衡器、音调和速度。",
    # Traditional Chinese
    "在 iPhone 和 Android 上不用網路播放 MP3、AAC、M4A、WAV、AIFF 和 FLAC。無廣告、免帳號。音調（±8 個半音）、速度和等化器。免費。":
        "在 iOS 與 Android 上不用網路播放 MP3、AAC、M4A、WAV、AIFF 和 FLAC。無廣告、免帳號。支援音調（±8 個半音）、速度和等化器。",
    "適用於 iPhone 和 Android 的免費 MP3 播放器，無廣告、免帳號、不追蹤。不用網路播放你的檔案，還能調整等化器、音調和速度。":
        "適用於 iOS 與 Android 的離線 MP3 播放器，無廣告、免帳號、不追蹤。不用網路播放你的檔案，還能調整等化器、音調和速度。",
}

# ------------------------------------------------------------------ 6. Neutral FAQ templates per language
# (access_q_general, access_q_pro, access_a_full, access_a_tools, ads_a_clean, update_a_clean)
LANG_FAQ = {
    "en": {
        "q_app": "How does access to VibeDeck Player work?",
        "q_pro": "How do I unlock VibeDeck PRO?",
        "a_full": "VibeDeck Player is available on iOS and Android with no ads and no account required. VibeDeck PRO unlocks the full sound toolkit (pitch, tempo, waveform scrubbing, 3-band DJ EQ and 8-band equalizer, filter, limiter, VibeMod, TONE, AURA, Studio, Stems and Sampler) via a subscription or one-time Lifetime access inside the app.",
        "a_tools": "VibeDeck Player is available on iOS and Android with no ads. Equalizer, limiter, pitch, tempo, Studio, Stems, Sampler and other sound tools are part of VibeDeck PRO, available via a subscription or one-time Lifetime access inside the app.",
        "a_ads": "No. VibeDeck Player shows no banner ads, no video ads and no popups, and you do not need an account.",
        "a_pro_inc": "The full sound engine: pitch and filter, 3-band DJ EQ or 8-band equalizer, limiter, VibeMod, TONE, AURA and Smart Metadata. Available on iOS and Android via a subscription or one-time Lifetime access inside the app.",
        "a_upd": "Update VibeDeck Player on the App Store or Google Play. Available on iOS and Android.",
    },
    "de": {
        "q_app": "Wie funktioniert der Zugang zu VibeDeck Player?",
        "q_pro": "Wie bekomme ich Zugang zu VibeDeck PRO?",
        "a_full": "VibeDeck Player ist für iOS und Android ohne Werbung und ohne Konto verfügbar. VibeDeck PRO schaltet alle Sound-Werkzeuge frei (Tonhöhe, Tempo, Wellenform-Spulen, 3-Band-DJ-EQ und 8-Band-Equalizer, Filter, Limiter, VibeMod, TONE, AURA, Studio, Stems und Sampler) per Abo oder einmaligem Lifetime-Zugang direkt in der App.",
        "a_tools": "VibeDeck Player ist für iOS und Android ohne Werbung verfügbar. Equalizer, Limiter, Tonhöhe, Tempo, Studio, Stems, Sampler und weitere Sound-Werkzeuge gehören zu VibeDeck PRO und sind per Abo oder einmaligem Lifetime-Zugang in der App erhältlich.",
        "a_ads": "Nein. VibeDeck Player zeigt keine Banner, keine Videos und keine Pop-ups, und du brauchst kein Konto.",
        "a_pro_inc": "Die komplette Sound-Engine: Tonhöhe und Filter, 3-Band-DJ-EQ oder 8-Band-Equalizer, Limiter, VibeMod, TONE, AURA und Smart Metadata. Verfügbar für iOS und Android per Abo oder einmaligem Lifetime-Zugang in der App.",
        "a_upd": "Aktualisiere VibeDeck Player im App Store oder bei Google Play. Verfügbar für iOS und Android.",
    },
    "es": {
        "q_app": "¿Cómo funciona el acceso a VibeDeck Player?",
        "q_pro": "¿Cómo se accede a VibeDeck PRO?",
        "a_full": "VibeDeck Player está disponible en iOS y Android, sin anuncios y sin cuenta. VibeDeck PRO desbloquea todas las herramientas de sonido (tono, tempo, desplazamiento por la forma de onda, EQ DJ de 3 bandas y ecualizador de 8 bandas, filtro, limitador, VibeMod, TONE, AURA, Studio, Stems y Sampler) mediante suscripción o acceso Lifetime de pago único dentro de la app.",
        "a_tools": "VibeDeck Player está disponible en iOS y Android sin anuncios. El ecualizador, el limitador, el tono, el tempo, Studio, Stems, Sampler y las demás herramientas de sonido forman parte de VibeDeck PRO, disponible mediante suscripción o acceso Lifetime de pago único dentro de la app.",
        "a_ads": "No. VibeDeck Player no muestra banners, videos ni ventanas emergentes, y no necesitas crear una cuenta.",
        "a_pro_inc": "Todo el motor de sonido: tono y filtro, EQ DJ de 3 bandas o ecualizador de 8 bandas, limitador, VibeMod, TONE, AURA y Smart Metadata. Disponible en iOS y Android mediante suscripción o acceso Lifetime de pago único dentro de la app.",
        "a_upd": "Actualiza VibeDeck Player en el App Store o Google Play. Disponible en iOS y Android.",
    },
    "fr": {
        "q_app": "Comment fonctionne l’accès à VibeDeck Player ?",
        "q_pro": "Comment accéder à VibeDeck PRO ?",
        "a_full": "VibeDeck Player est disponible sur iOS et Android, sans publicité et sans compte. VibeDeck PRO débloque tous les outils sonores (hauteur, tempo, navigation sur la forme d’onde, EQ DJ 3 bandes et égaliseur 8 bandes, filtre, limiteur, VibeMod, TONE, AURA, Studio, Stems et Sampler) par abonnement ou accès Lifetime en paiement unique dans l’application.",
        "a_tools": "VibeDeck Player est disponible sur iOS et Android sans publicité. L’égaliseur, le limiteur, la hauteur, le tempo, Studio, Stems, Sampler et les autres outils sonores font partie de VibeDeck PRO, accessible par abonnement ou accès Lifetime en paiement unique dans l’application.",
        "a_ads": "Non. VibeDeck Player n’affiche ni bannières, ni vidéos, ni pop-ups, et aucun compte n’est nécessaire.",
        "a_pro_inc": "Tout le moteur sonore : hauteur et filtre, EQ DJ 3 bandes ou égaliseur 8 bandes, limiteur, VibeMod, TONE, AURA et Smart Metadata. Disponible sur iOS et Android par abonnement ou accès Lifetime en paiement unique dans l’application.",
        "a_upd": "Mettez à jour VibeDeck Player dans l’App Store ou Google Play. Disponible sur iOS et Android.",
    },
    "id": {
        "q_app": "Bagaimana cara kerja akses VibeDeck Player?",
        "q_pro": "Bagaimana cara mengakses VibeDeck PRO?",
        "a_full": "VibeDeck Player tersedia di iOS dan Android tanpa iklan dan tanpa akun. VibeDeck PRO membuka seluruh alat suara (nada, tempo, geser pada gelombang suara, EQ DJ 3 band dan equalizer 8 band, filter, limiter, VibeMod, TONE, AURA, Studio, Stems, dan Sampler) melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
        "a_tools": "VibeDeck Player tersedia di iOS dan Android tanpa iklan. Equalizer, limiter, nada, tempo, Studio, Stems, Sampler, dan alat suara lainnya merupakan bagian dari VibeDeck PRO yang tersedia melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
        "a_ads": "Tidak. VibeDeck Player tidak menampilkan banner, video, atau pop-up, dan kamu tidak perlu akun.",
        "a_pro_inc": "Seluruh mesin suara: nada dan filter, EQ DJ 3 band atau equalizer 8 band, limiter, VibeMod, TONE, AURA, dan Smart Metadata. Tersedia di iOS dan Android melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
        "a_upd": "Perbarui VibeDeck Player di App Store atau Google Play. Tersedia di iOS dan Android.",
    },
    "it": {
        "q_app": "Come funziona l’accesso a VibeDeck Player?",
        "q_pro": "Come si accede a VibeDeck PRO?",
        "a_full": "VibeDeck Player è disponibile su iOS e Android senza pubblicità e senza account. VibeDeck PRO sblocca tutti gli strumenti audio (tonalità, tempo, scorrimento sulla forma d’onda, EQ DJ a 3 bande ed equalizzatore a 8 bande, filtro, limiter, VibeMod, TONE, AURA, Studio, Stems e Sampler) tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",
        "a_tools": "VibeDeck Player è disponibile su iOS e Android senza pubblicità. Equalizzatore, limiter, tonalità, tempo, Studio, Stems, Sampler e gli altri strumenti audio fanno parte di VibeDeck PRO, disponibile tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",
        "a_ads": "No. VibeDeck Player non mostra banner, video o pop-up pubblicitari, e non serve un account.",
        "a_pro_inc": "Il motore audio completo: pitch e filtro, EQ DJ a 3 bande o equalizzatore a 8 bande, limiter, VibeMod, TONE, AURA e Smart Metadata. Disponibile su iOS e Android tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",
        "a_upd": "Aggiorna VibeDeck Player su App Store o Google Play. Disponibile su iOS e Android.",
    },
    "ja": {
        "q_app": "VibeDeck Playerの利用方法は？",
        "q_pro": "VibeDeck PROの利用方法は？",
        "a_full": "VibeDeck PlayerはiOSとAndroidに対応しており、広告なし・アカウント不要で使えます。ピッチとテンポ、波形でのシーク、3バンドDJ EQと8バンドイコライザー、フィルター、リミッター、VibeMod、TONE、AURA、Studio、Stems、Samplerなどのサウンド機能はVibeDeck PROに含まれ、アプリ内のサブスクリプションまたは買い切りのLifetimeアクセスで利用できます。",
        "a_tools": "VibeDeck PlayerはiOSとAndroidで広告なしで使えます。イコライザー、リミッター、ピッチ、テンポ、Studio、Stems、Samplerなどのサウンド機能はVibeDeck PROに含まれ、アプリ内のサブスクリプションまたは買い切りのLifetimeアクセスで利用できます。",
        "a_ads": "ありません。VibeDeck Playerに広告はなく、アカウント登録も不要です。",
        "a_pro_inc": "ピッチとフィルター、3バンドDJ EQまたは8バンドイコライザー、リミッター、VibeMod、TONE、AURA、スマートメタデータなどすべてのサウンド機能です。iOSとAndroidのアプリ内でサブスクリプションまたは買い切りのLifetimeアクセスを選べます。",
        "a_upd": "App StoreまたはGoogle PlayでVibeDeck Playerをアップデートしてください。iOSとAndroidに対応しています。",
    },
    "ko": {
        "q_app": "VibeDeck Player는 어떻게 이용하나요?",
        "q_pro": "VibeDeck PRO는 어떻게 이용하나요?",
        "a_full": "VibeDeck Player는 iOS와 Android에서 광고와 계정 없이 이용할 수 있습니다. 피치와 템포, 파형 탐색, 3밴드 DJ EQ 및 8밴드 이퀄라이저, 필터, 리미터, VibeMod, TONE, AURA, Studio, Stems, Sampler 등 모든 사운드 도구는 앱 내 구독 또는 일회성 Lifetime 이용권으로 VibeDeck PRO를 활성화해 사용할 수 있습니다.",
        "a_tools": "VibeDeck Player는 iOS와 Android에서 광고 없이 이용할 수 있습니다. 이퀄라이저, 리미터, 피치, 템포, Studio, Stems, Sampler 등의 사운드 도구는 VibeDeck PRO 기능이며, 앱 내에서 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",
        "a_ads": "아니요. VibeDeck Player에는 배너, 동영상, 팝업 광고가 없으며 계정도 필요 없습니다.",
        "a_pro_inc": "사운드 엔진 전체입니다. 피치와 필터, 3밴드 DJ EQ 또는 8밴드 이퀄라이저, 리미터, VibeMod, TONE, AURA, Smart Metadata가 포함되며, iOS와 Android 앱 내에서 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",
        "a_upd": "App Store 또는 Google Play에서 VibeDeck Player를 업데이트하세요. iOS와 Android에서 이용할 수 있습니다.",
    },
    "nl": {
        "q_app": "Hoe werkt toegang tot VibeDeck Player?",
        "q_pro": "Hoe krijg ik toegang tot VibeDeck PRO?",
        "a_full": "VibeDeck Player is beschikbaar op iOS en Android, zonder advertenties en zonder account. VibeDeck PRO ontgrendelt alle geluidstools (toonhoogte, tempo, spoelen op de golfvorm, 3-bands DJ-EQ en 8-bands equalizer, filter, limiter, VibeMod, TONE, AURA, Studio, Stems en Sampler) via een abonnement of eenmalige Lifetime-toegang in de app.",
        "a_tools": "VibeDeck Player is beschikbaar op iOS en Android zonder advertenties. Equalizer, limiter, toonhoogte, tempo, Studio, Stems, Sampler en andere geluidstools horen bij VibeDeck PRO en zijn beschikbaar via een abonnement of eenmalige Lifetime-toegang in de app.",
        "a_ads": "Nee. VibeDeck Player toont geen banners, video’s of pop-ups, en je hebt geen account nodig.",
        "a_pro_inc": "De hele geluidsengine: toonhoogte en filter, 3-bands DJ-EQ of 8-bands equalizer, limiter, VibeMod, TONE, AURA en Smart Metadata. Beschikbaar op iOS en Android via een abonnement of eenmalige Lifetime-toegang in de app.",
        "a_upd": "Werk VibeDeck Player bij in de App Store of Google Play. Beschikbaar voor iOS en Android.",
    },
    "pl": {
        "q_app": "Jak działa dostęp do VibeDeck Player?",
        "q_pro": "Jak uzyskać dostęp do VibeDeck PRO?",
        "a_full": "VibeDeck Player jest dostępny na iOS i Androida, bez reklam i bez konta. VibeDeck PRO odblokowuje wszystkie narzędzia dźwięku (wysokość dźwięku, tempo, przewijanie po fali, 3-pasmowy korektor DJ i 8-pasmowy equalizer, filtr, limiter, VibeMod, TONE, AURA, Studio, Stems i Sampler) w ramach subskrypcji lub jednorazowego dostępu Lifetime wewnątrz aplikacji.",
        "a_tools": "VibeDeck Player jest dostępny na iOS i Androida bez reklam. Equalizer, limiter, wysokość dźwięku, tempo, Studio, Stems, Sampler i inne narzędzia dźwięku wchodzą w skład VibeDeck PRO, dostępnego w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",
        "a_ads": "Nie. VibeDeck Player nie wyświetla banerów, filmów ani wyskakujących okienek, i nie potrzebujesz konta.",
        "a_pro_inc": "Cały silnik dźwięku: wysokość dźwięku i filtr, 3-pasmowy korektor DJ lub 8-pasmowy, limiter, VibeMod, TONE, AURA i Smart Metadata. Dostępny na iOS i Androida w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",
        "a_upd": "Zaktualizuj VibeDeck Player w App Store lub Google Play. Aplikacja jest dostępna na iOS i Androida.",
    },
    "pt-br": {
        "q_app": "Como funciona o acesso ao VibeDeck Player?",
        "q_pro": "Como acessar o VibeDeck PRO?",
        "a_full": "O VibeDeck Player está disponível para iOS e Android, sem anúncios e sem conta. O VibeDeck PRO libera todas as ferramentas de som (tom, andamento, navegação pela forma de onda, EQ DJ de 3 bandas e equalizador de 8 bandas, filtro, limitador, VibeMod, TONE, AURA, Studio, Stems e Sampler) por assinatura ou acesso Lifetime em pagamento único dentro do aplicativo.",
        "a_tools": "O VibeDeck Player está disponível para iOS e Android sem anúncios. Equalizador, limitador, tom, andamento, Studio, Stems, Sampler e outras ferramentas de som fazem parte do VibeDeck PRO, disponível por assinatura ou acesso Lifetime em pagamento único dentro do aplicativo.",
        "a_ads": "Não. O VibeDeck Player não exibe banners, vídeos nem pop-ups, e você não precisa criar conta.",
        "a_pro_inc": "Todo o motor de som: tom e filtro, EQ DJ de 3 bandas ou equalizador de 8 bandas, limitador, VibeMod, TONE, AURA e Smart Metadata. Disponível para iOS e Android por assinatura ou acesso Lifetime em pagamento único dentro do aplicativo.",
        "a_upd": "Atualize o VibeDeck Player na App Store ou no Google Play. Disponível para iOS e Android.",
    },
    "ru": {
        "q_app": "Как устроен доступ к VibeDeck Player?",
        "q_pro": "Как получить доступ к VibeDeck PRO?",
        "a_full": "VibeDeck Player доступен на iOS и Android, без рекламы и без аккаунта. VibeDeck PRO открывает все инструменты звука (высоту тона, темп, перемотку по форме волны, 3-полосный DJ эквалайзер и 8-полосный эквалайзер, фильтр, лимитер, VibeMod, TONE, AURA, Studio, Stems и Sampler) по подписке или с разовым Lifetime-доступом внутри приложения.",
        "a_tools": "VibeDeck Player доступен на iOS и Android без рекламы. Эквалайзер, лимитер, тональность, темп, Studio, Stems, Sampler и другие инструменты звука входят в VibeDeck PRO, который доступен по подписке или с разовым Lifetime-доступом внутри приложения.",
        "a_ads": "Нет. VibeDeck Player не показывает баннеры, видео и всплывающие окна, и аккаунт не нужен.",
        "a_pro_inc": "Все звуковые функции: высота тона и фильтр, 3-полосный DJ эквалайзер или 8-полосный, лимитер, VibeMod, TONE, AURA и Smart Metadata. Доступ открывается на iOS и Android по подписке или с разовым Lifetime-доступом внутри приложения.",
        "a_upd": "Обновите VibeDeck Player в App Store или Google Play. Приложение доступно на iOS и Android.",
    },
    "th": {
        "q_app": "การเข้าถึง VibeDeck Player ทำงานอย่างไร",
        "q_pro": "จะปลดล็อก VibeDeck PRO ได้อย่างไร",
        "a_full": "VibeDeck Player พร้อมใช้งานบน iOS และ Android โดยไม่มีโฆษณาและไม่ต้องมีบัญชี VibeDeck PRO ปลดล็อกเครื่องมือเสียงครบชุด ทั้งระดับเสียง เทมโป การเลื่อนบนรูปคลื่นเสียง DJ EQ 3 แบนด์และอีควอไลเซอร์ 8 แบนด์ ฟิลเตอร์ ลิมิตเตอร์ VibeMod, TONE, AURA, Studio, Stems และ Sampler ผ่านการสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",
        "a_tools": "VibeDeck Player พร้อมใช้งานบน iOS และ Android โดยไม่มีโฆษณา อีควอไลเซอร์ ลิมิตเตอร์ ระดับเสียง เทมโป Studio, Stems, Sampler และเครื่องมือเสียงอื่น ๆ อยู่ใน VibeDeck PRO ซึ่งเลือกใช้งานได้ทั้งแบบสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",
        "a_ads": "ไม่มี VibeDeck Player ไม่แสดงแบนเนอร์ วิดีโอ หรือป๊อปอัป และไม่ต้องมีบัญชี",
        "a_pro_inc": "เอนจินเสียงครบชุด: ระดับเสียงและฟิลเตอร์ DJ EQ 3 แบนด์หรืออีควอไลเซอร์ 8 แบนด์ ลิมิตเตอร์ VibeMod, TONE, AURA และ Smart Metadata ใช้งานได้บน iOS และ Android ผ่านการสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",
        "a_upd": "อัปเดต VibeDeck Player ได้ใน App Store หรือ Google Play พร้อมใช้งานบน iOS และ Android",
    },
    "tr": {
        "q_app": "VibeDeck Player’a erişim nasıl çalışır?",
        "q_pro": "VibeDeck PRO’ya nasıl erişebilirim?",
        "a_full": "VibeDeck Player, iOS ve Android için reklamsız ve hesapsız olarak kullanılabilir. VibeDeck PRO tüm ses araçlarını (perde, tempo, dalga formunda gezinme, 3 bantlı DJ EQ ve 8 bantlı ekolayzer, filtre, limiter, VibeMod, TONE, AURA, Studio, Stems ve Sampler) uygulama içi abonelik veya tek seferlik Lifetime erişimiyle açar.",
        "a_tools": "VibeDeck Player, iOS ve Android için reklamsız olarak kullanılabilir. Ekolayzer, limiter, perde, tempo, Studio, Stems, Sampler ve diğer ses araçları VibeDeck PRO’ya dahildir; uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",
        "a_ads": "Hayır. VibeDeck Player banner, video ya da açılır pencere göstermez ve hesap gerektirmez.",
        "a_pro_inc": "Tüm ses motoru: ton ve filtre, 3 bantlı DJ EQ veya 8 bantlı ekolayzer, limiter, VibeMod, TONE, AURA ve Smart Metadata. iOS ve Android’de uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",
        "a_upd": "VibeDeck Player’ı App Store veya Google Play’den güncelleyin. iOS ve Android için kullanılabilir.",
    },
    "uk": {
        "q_app": "Як влаштований доступ до VibeDeck Player?",
        "q_pro": "Як отримати доступ до VibeDeck PRO?",
        "a_full": "VibeDeck Player доступний на iOS та Android, без реклами й без акаунта. VibeDeck PRO відкриває всі інструменти звуку (висоту тону, темп, перемотування за формою хвилі, 3-смуговий DJ еквалайзер і 8-смуговий еквалайзер, фільтр, лімітер, VibeMod, TONE, AURA, Studio, Stems та Sampler) за підпискою або з разовим Lifetime-доступом усередині застосунку.",
        "a_tools": "VibeDeck Player доступний на iOS та Android без реклами. Еквалайзер, лімітер, тональність, темп, Studio, Stems, Sampler та інші інструменти звуку входять до VibeDeck PRO, який доступний за підпискою або з разовим Lifetime-доступом усередині застосунку.",
        "a_ads": "Ні. VibeDeck Player не показує банери, відео чи спливні вікна, і акаунт не потрібен.",
        "a_pro_inc": "Усі звукові функції: висота тону й фільтр, 3-смуговий DJ еквалайзер або 8-смуговий, лімітер, VibeMod, TONE, AURA і Smart Metadata. Доступ відкривається на iOS та Android за підпискою або з разовим Lifetime-доступом усередині застосунку.",
        "a_upd": "Оновіть VibeDeck Player в App Store або Google Play. Застосунок доступний на iOS та Android.",
    },
    "vi": {
        "q_app": "Quyền truy cập VibeDeck Player hoạt động thế nào?",
        "q_pro": "Làm sao để mở khóa VibeDeck PRO?",
        "a_full": "VibeDeck Player có mặt trên iOS và Android, không quảng cáo và không cần tài khoản. VibeDeck PRO mở khóa toàn bộ công cụ âm thanh (cao độ, tempo, tua trên dạng sóng, EQ DJ 3 dải và equalizer 8 dải, filter, limiter, VibeMod, TONE, AURA, Studio, Stems và Sampler) thông qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần ngay trong ứng dụng.",
        "a_tools": "VibeDeck Player có mặt trên iOS và Android và không có quảng cáo. Equalizer, limiter, cao độ, tempo, Studio, Stems, Sampler và các công cụ âm thanh khác thuộc VibeDeck PRO, có sẵn qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",
        "a_ads": "Không. VibeDeck Player không hiển thị banner, video hay pop-up, và bạn không cần tài khoản.",
        "a_pro_inc": "Toàn bộ bộ máy âm thanh: cao độ và filter, EQ DJ 3 dải hoặc equalizer 8 dải, limiter, VibeMod, TONE, AURA và Smart Metadata. Có sẵn trên iOS và Android qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",
        "a_upd": "Cập nhật VibeDeck Player trên App Store hoặc Google Play. Có mặt trên iOS và Android.",
    },
    "zh-hans": {
        "q_app": "VibeDeck Player 的使用方式是什么？",
        "q_pro": "如何解锁 VibeDeck PRO？",
        "a_full": "VibeDeck Player 支持 iOS 和 Android，无广告、免账号。VibeDeck PRO 解锁完整音效工具（音高、速度、波形拖动、3 段 DJ EQ 与 8 段均衡器、滤波器、限幅器、VibeMod、TONE、AURA、Studio、Stems 和 Sampler），可在应用内选择订阅或一次性购买 Lifetime 权限。",
        "a_tools": "VibeDeck Player 支持 iOS 和 Android 且无广告。均衡器、限幅器、音高、速度、Studio、Stems、Sampler 等声音工具属于 VibeDeck PRO，可在应用内通过订阅或一次性购买 Lifetime 权限解锁。",
        "a_ads": "没有。VibeDeck Player 不显示横幅、视频或弹窗广告，也不需要账号。",
        "a_pro_inc": "完整音效引擎：音高与滤波器、3 段 DJ EQ 或 8 段均衡器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata。可在 iOS 和 Android 应用内通过订阅或一次性购买 Lifetime 权限解锁。",
        "a_upd": "在 App Store 或 Google Play 更新 VibeDeck Player。支持 iOS 和 Android。",
    },
    "zh-hant": {
        "q_app": "VibeDeck Player 的使用方式是什麼？",
        "q_pro": "如何解鎖 VibeDeck PRO？",
        "a_full": "VibeDeck Player 支援 iOS 與 Android，無廣告、免帳號。VibeDeck PRO 解鎖完整音效工具（音高、速度、波形拖曳、3 段 DJ EQ 與 8 段等化器、濾波器、限幅器、VibeMod、TONE、AURA、Studio、Stems 與 Sampler），可在 App 內選擇訂閱或一次性購買 Lifetime 權限。",
        "a_tools": "VibeDeck Player 支援 iOS 與 Android 且無廣告。等化器、限幅器、音高、速度、Studio、Stems、Sampler 等聲音工具屬於 VibeDeck PRO，可在 App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",
        "a_ads": "沒有。VibeDeck Player 不顯示橫幅、影片或彈出廣告，也不需要帳號。",
        "a_pro_inc": "完整音效引擎：音高與濾波器、3 段 DJ EQ 或 8 段等化器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata。可在 iOS 與 Android App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",
        "a_upd": "在 App Store 或 Google Play 更新 VibeDeck Player。支援 iOS 與 Android。",
    },
}

# Exact FAQ (question -> new question, answer -> new answer) overrides for special / page-specific FAQs
# Plus general rules matched by (lang, old_q_norm) or old_a pattern.
SPECIAL_FAQ_Q_EXACT = {
    # English special questions
    ("en", "Is VibeDeck Player free?"): ("q_app", "a_full"),
    ("en", "Is it free?"): ("q_pro", "a_tools"),
    ("en", "Is pitch control free?"): ("q_pro", "a_tools"),
    ("en", "Is key change free?"): ("q_pro", "a_tools"),
    ("en", "How much does it cost on Android?"): ("q_app", "a_full"),
    ("en", "Is VibeDeck Player free on Android?"): ("q_app", "a_full"),
    ("en", "Is there a free offline music player with no ads?"): (
        "Is there an offline music player with no ads?",
        "Yes. VibeDeck Player works fully offline on iOS and Android with no ads and no account. VibeDeck PRO unlocks the full sound engine with pitch, EQ, limiter and visuals via a subscription or one-time Lifetime access inside the app.",
    ),
    # German
    ("de", "Ist es kostenlos?"): ("q_pro", "a_tools"),
    ("de", "Ist das kostenlos?"): ("q_pro", "a_tools"),
    ("de", "Ist die App kostenlos?"): ("q_app", "a_full"),
    ("de", "Was kostet die App?"): ("q_app", "a_full"),
    # Spanish
    ("es", "¿Es gratis?"): ("q_pro", "a_tools"),
    ("es", "¿Cuánto cuesta?"): ("q_app", "a_full"),
    # French
    ("fr", "Est-ce gratuit ?"): ("q_pro", "a_tools"),
    ("fr", "C’est gratuit ?"): ("q_pro", "a_tools"),
    ("fr", "C'est gratuit ?"): ("q_pro", "a_tools"),
    ("fr", "Combien ça coûte ?"): ("q_app", "a_full"),
    # Indonesian
    ("id", "Apakah gratis?"): ("q_pro", "a_tools"),
    ("id", "Berapa harganya?"): ("q_app", "a_full"),
    # Italian
    ("it", "È gratis?"): ("q_pro", "a_tools"),
    ("it", "È gratuito?"): ("q_pro", "a_tools"),
    ("it", "Quanto costa?"): ("q_app", "a_full"),
    # Japanese
    ("ja", "無料ですか？"): ("q_pro", "a_tools"),
    ("ja", "無料ですか?"): ("q_pro", "a_tools"),
    ("ja", "無料で使えますか？"): ("q_pro", "a_tools"),
    # Korean
    ("ko", "무료인가요?"): ("q_pro", "a_tools"),
    ("ko", "가격은 얼마인가요?"): ("q_app", "a_full"),
    # Dutch
    ("nl", "Is het gratis?"): ("q_pro", "a_tools"),
    ("nl", "Wat kost het?"): ("q_app", "a_full"),
    # Polish
    ("pl", "Czy to jest darmowe?"): ("q_pro", "a_tools"),
    ("pl", "Czy to za darmo?"): ("q_pro", "a_tools"),
    ("pl", "Ile to kosztuje?"): ("q_app", "a_full"),
    # Portuguese (BR)
    ("pt-br", "É grátis?"): ("q_pro", "a_tools"),
    ("pt-br", "Quanto custa?"): ("q_app", "a_full"),
    ("pt-br", "Quanto custa no Android?"): ("q_app", "a_full"),
    ("pt-br", "É grátis no Android?"): ("q_app", "a_full"),
    # Russian
    ("ru", "Это бесплатно?"): ("q_pro", "a_tools"),
    ("ru", "Сколько это стоит?"): ("q_app", "a_full"),
    # Thai
    ("th", "ฟรีไหม"): ("q_pro", "a_tools"),
    ("th", "ใช้ฟรีไหม"): ("q_pro", "a_tools"),
    ("th", "ราคาเท่าไร"): ("q_app", "a_full"),
    # Turkish
    ("tr", "Ücretsiz mi?"): ("q_pro", "a_tools"),
    ("tr", "Ne kadar?"): ("q_app", "a_full"),
    # Ukrainian
    ("uk", "Чи безкоштовно це?"): ("q_pro", "a_tools"),
    ("uk", "Скільки це коштує?"): ("q_app", "a_full"),
    # Vietnamese
    ("vi", "Có miễn phí không?"): ("q_pro", "a_tools"),
    ("vi", "Giá bao nhiêu?"): ("q_app", "a_full"),
    # Simplified Chinese
    ("zh-hans", "免费吗？"): ("q_pro", "a_tools"),
    ("zh-hans", "是免费的吗？"): ("q_pro", "a_tools"),
    ("zh-hans", "要多少钱？"): ("q_app", "a_full"),
    # Traditional Chinese
    ("zh-hant", "免費嗎？"): ("q_pro", "a_tools"),
    ("zh-hant", "是免費的嗎？"): ("q_pro", "a_tools"),
    ("zh-hant", "要多少錢？"): ("q_app", "a_full"),
}

# Questions whose Q stays the same (or clean), only A changes
FAQ_ANSWER_BY_Q_NORM = {
    # Ads questions
    ("en", "Does it have ads?"): "a_ads",
    ("en", "Is there really no ads in VibeDeck Player?"): "a_ads",
    ("en", "Is there a FLAC player for Android without ads?"):
        "Yes. VibeDeck Player has no ads and needs no account. Available on iOS and Android.",
    ("en", "What is the best ad-free offline music player?"):
        "It depends on what you need. If you want an offline music player with no ads that also changes pitch and tempo, runs on both iOS and Android, and offers a subscription or one-time Lifetime access inside the app, VibeDeck Player is built for exactly that.",
    ("en", "Where is looping in VibeDeck Player?"):
        "Loops are part of VibeDeck Studio, the creative toolkit inside VibeDeck Player. Available on iOS and Android with no ads, via a subscription or one-time Lifetime access inside the app.",
    ("en", "Does VibeDeck Player play AAC, M4A or AIFF files?"):
        "Yes. VibeDeck Player plays AAC, M4A and AIFF files, as well as MP3, WAV and FLAC. ALAC is not named in the App Store listing, so test one ALAC file in the app before you convert your library.",
    ("en", "How do I get the update?"): "a_upd",
    # Localized ads questions
    ("de", "Gibt es Werbung?"): "a_ads",
    ("de", "Gibt es wirklich keine Werbung?"): "a_ads",
    ("es", "¿Tiene anuncios?"): "a_ads",
    ("es", "¿De verdad no tiene anuncios?"): "a_ads",
    ("fr", "Y a-t-il des publicités ?"): "a_ads",
    ("fr", "Il n’y a vraiment aucune pub ?"): "a_ads",
    ("id", "Apakah ada iklan?"): "a_ads",
    ("id", "Benar-benar tidak ada iklan?"): "a_ads",
    ("it", "Ci sono pubblicità?"): "a_ads",
    ("it", "Non ci sono davvero pubblicità?"): "a_ads",
    ("ja", "広告はありますか？"): "a_ads",
    ("ko", "광고가 있나요?"): "a_ads",
    ("ko", "정말 광고가 하나도 없나요?"): "a_ads",
    ("nl", "Zijn er advertenties?"): "a_ads",
    ("nl", "Echt helemaal geen advertenties?"): "a_ads",
    ("pl", "Czy są reklamy?"): "a_ads",
    ("pl", "Naprawdę nie ma żadnych reklam?"): "a_ads",
    ("pt-br", "Tem anúncios?"): "a_ads",
    ("pt-br", "Existe player FLAC para Android sem anúncios?"):
        "Sim. O VibeDeck Player não exibe anúncios e não pede conta. Disponível para iOS e Android.",
    ("ru", "Есть реклама?"): "a_ads",
    ("ru", "Рекламы правда совсем нет?"): "a_ads",
    ("th", "มีโฆษณาไหม"): "a_ads",
    ("th", "ไม่มีโฆษณาจริง ๆ เหรอ"): "a_ads",
    ("tr", "Reklam var mı?"): "a_ads",
    ("tr", "Gerçekten hiç reklam yok mu?"): "a_ads",
    ("uk", "Є реклама?"): "a_ads",
    ("vi", "Có quảng cáo không?"): "a_ads",
    ("vi", "Thật sự không có quảng cáo nào?"): "a_ads",
    ("zh-hans", "有广告吗？"): "a_ads",
    ("zh-hans", "真的完全没有广告吗？"): "a_ads",
    ("zh-hant", "有廣告嗎？"): "a_ads",
    ("zh-hant", "真的完全沒有廣告嗎？"): "a_ads",
    # What is included in PRO questions
    ("de", "Was enthält VibeDeck PRO?"): "a_pro_inc",
    ("es", "¿Qué incluye VibeDeck PRO?"): "a_pro_inc",
    ("fr", "Que comprend VibeDeck PRO ?"): "a_pro_inc",
    ("id", "Apa saja isi VibeDeck PRO?"): "a_pro_inc",
    ("it", "Cosa include VibeDeck PRO?"): "a_pro_inc",
    ("ja", "VibeDeck PROでは何が使えますか？"): "a_pro_inc",
    ("ko", "VibeDeck PRO에는 무엇이 포함되나요?"): "a_pro_inc",
    ("nl", "Wat zit er in VibeDeck PRO?"): "a_pro_inc",
    ("pl", "Co zawiera VibeDeck PRO?"): "a_pro_inc",
    ("pt-br", "O que vem no VibeDeck PRO?"): "a_pro_inc",
    ("ru", "Что входит в VibeDeck PRO?"): "a_pro_inc",
    ("th", "VibeDeck PRO มีอะไรบ้าง"): "a_pro_inc",
    ("tr", "VibeDeck PRO’da neler var?"): "a_pro_inc",
    ("uk", "Що входить до VibeDeck PRO?"): "a_pro_inc",
    ("vi", "VibeDeck PRO có gì?"): "a_pro_inc",
    ("zh-hans", "VibeDeck PRO 包含什么？"): "a_pro_inc",
    ("zh-hant", "VibeDeck PRO 包含什麼？"): "a_pro_inc",
    # Update questions (whats-new pages)
    ("de", "Wie bekomme ich das Update?"): "a_upd",
    ("es", "¿Cómo consigo la actualización?"): "a_upd",
    ("fr", "Comment obtenir la mise à jour ?"): "a_upd",
    ("id", "Bagaimana mendapatkan pembaruan?"): "a_upd",
    ("it", "Come ottengo l’aggiornamento?"): "a_upd",
    ("ja", "アップデートの方法は？"): "a_upd",
    ("ko", "업데이트는 어떻게 받나요?"): "a_upd",
    ("nl", "Hoe krijg ik de update?"): "a_upd",
    ("pl", "Jak dostać aktualizację?"): "a_upd",
    ("pt-br", "Como pego a atualização?"): "a_upd",
    ("ru", "Как получить обновление?"): "a_upd",
    ("th", "รับอัปเดตอย่างไร"): "a_upd",
    ("tr", "Güncellemeyi nasıl alırım?"): "a_upd",
    ("vi", "Làm sao nhận bản cập nhật?"): "a_upd",
    ("zh-hans", "如何获取更新？"): "a_upd",
    ("zh-hant", "如何取得更新？"): "a_upd",
}

# ------------------------------------------------------------------ 7. Body text exact replacements (all 18 languages)
# Ordered from longest to shortest at runtime. Every string is exact HTML text (inside <p>, <h2>, etc.).
BODY_REPLACEMENTS = {
    # --- Hero lede trial sentences on 18 homepages ---
    " Try VibeDeck PRO free for 3 days on the yearly plan.":
        " Available via subscription or one-time Lifetime access inside the app.",
    " Teste VibeDeck PRO 3 Tage kostenlos im Jahrestarif.":
        " Zugang per Abo oder einmaligem Lifetime-Kauf direkt in der App.",
    " Prueba VibeDeck PRO gratis 3 días en el plan anual.":
        " Disponible mediante suscripción o acceso Lifetime de pago único dentro de la app.",
    " Essayez VibeDeck PRO gratuitement pendant 3 jours avec l’abonnement annuel.":
        " Accessible par abonnement ou accès Lifetime en paiement unique dans l’application.",
    " Coba VibeDeck PRO gratis 3 hari dengan paket tahunan.":
        " Tersedia melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
    " Prova VibeDeck PRO gratis per 3 giorni con il piano annuale.":
        " Disponibile tramite abbonamento o accesso Lifetime con pagamento unico nell’app.",
    "VibeDeck PROを年間プランで3日間無料でお試しいただけます。":
        "アプリ内のサブスクリプションまたは買い切りのLifetimeアクセスで利用できます。",
    " 연간 요금제로 VibeDeck PRO를 3일 무료로 써 보세요.":
        " 앱 내에서 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",
    " Probeer VibeDeck PRO 3 dagen gratis met het jaarabonnement.":
        " Beschikbaar via een abonnement of eenmalige Lifetime-toegang in de app.",
    " Wypróbuj VibeDeck PRO za darmo przez 3 dni w planie rocznym.":
        " Dostępny w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",
    " Teste o VibeDeck PRO grátis por 3 dias no plano anual.":
        " Disponível por assinatura ou acesso Lifetime em pagamento único dentro do app.",
    " Попробуйте VibeDeck PRO бесплатно 3 дня на годовом тарифе.":
        " Доступен по подписке или с разовым Lifetime-доступом внутри приложения.",
    " ลองใช้ VibeDeck PRO ฟรี 3 วันสำหรับแพ็กเกจรายปี":
        " ใช้งานได้ผ่านการสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",
    " VibeDeck PRO’yu yıllık planda 3 gün ücretsiz dene.":
        " Uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",
    " Спробуйте VibeDeck PRO безкоштовно 3 дні на річному тарифі.":
        " Доступний за підпискою або з разовим Lifetime-доступом усередині застосунку.",
    " Dùng thử VibeDeck PRO miễn phí 3 ngày với gói năm.":
        " Có sẵn qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",
    "在年付方案中免费试用 VibeDeck PRO 3 天。":
        "可在应用内通过订阅或一次性购买 Lifetime 权限解锁。",
    "在年繳方案中免費試用 VibeDeck PRO 3 天。":
        "可在 App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",

    # --- Repeated 6-guide PRO paragraphs (all 18 languages) ---
    "VibeDeck PRO offers a 3-day free trial on the yearly plan, plus monthly and Lifetime options. After the trial, the free version plays your music (also in the background). EQ, limiter and other sound tools need VibeDeck PRO.":
        LANG_FAQ["en"]["a_tools"],
    "VibeDeck PRO offers a 3-day free trial on the yearly plan, plus monthly and Lifetime options. The free version plays your music with no ads, also in the background. VibeDeck PRO unlocks everything else: pitch and tempo, waveform scrubbing, EQ, filter, limiter, VibeMod, TONE, AURA, Studio and the Sampler.":
        LANG_FAQ["en"]["a_full"],
    "VibeDeck PRO bietet eine kostenlose 3-tägige Testphase für den Jahrestarif, dazu Monats- und Lifetime-Optionen. Nach der Testphase spielt die kostenlose Version deine Musik (auch im Hintergrund). Equalizer, Limiter und die anderen Sound-Werkzeuge brauchen VibeDeck PRO.":
        LANG_FAQ["de"]["a_tools"],
    "VibeDeck PRO ofrece una prueba gratuita de 3 días en el plan anual, además de opciones mensuales y Lifetime. Después de la prueba, la versión gratuita reproduce tu música (también en segundo plano). El ecualizador, el limitador y las demás herramientas de sonido necesitan VibeDeck PRO.":
        LANG_FAQ["es"]["a_tools"],
    "VibeDeck PRO propose un essai gratuit de 3 jours sur l’abonnement annuel, ainsi que des formules mensuelle et Lifetime. Après l’essai, la version gratuite lit votre musique (aussi en arrière-plan). L’égaliseur, le limiteur et les autres outils de son nécessitent VibeDeck PRO.":
        LANG_FAQ["fr"]["a_tools"],
    "VibeDeck PRO menawarkan uji coba gratis 3 hari untuk paket tahunan, plus opsi bulanan dan Lifetime. Setelah uji coba, versi gratis memutar musikmu (juga di latar belakang). Equalizer, limiter, dan alat suara lainnya butuh VibeDeck PRO.":
        LANG_FAQ["id"]["a_tools"],
    "VibeDeck PRO offre una prova gratuita di 3 giorni sul piano annuale, oltre a opzioni mensili e Lifetime. Dopo la prova, la versione gratuita riproduce la tua musica (anche in background). L’equalizzatore, il limiter e gli altri strumenti audio richiedono VibeDeck PRO.":
        LANG_FAQ["it"]["a_tools"],
    "VibeDeck PROでは年間プランで3日間の無料トライアルが使え、月額プランとLifetimeも選べます。トライアルの後、無料版では音楽の再生ができます（バックグラウンド再生も可能）。イコライザー、リミッターなどのサウンドツールにはVibeDeck PROが必要です。":
        LANG_FAQ["ja"]["a_tools"],
    "VibeDeck PRO는 연간 요금제에서 3일 무료 체험을 제공하며, 월간 요금제와 Lifetime도 있습니다. 체험이 끝나면 무료 버전은 음악을 재생합니다(백그라운드 재생 포함). 이퀄라이저, 리미터 등 사운드 도구는 VibeDeck PRO가 필요합니다.":
        LANG_FAQ["ko"]["a_tools"],
    "VibeDeck PRO biedt een gratis proefperiode van 3 dagen op het jaarabonnement, plus maand- en Lifetime-opties. Na de proefperiode speelt de gratis versie je muziek (ook op de achtergrond). De equalizer, de limiter en de andere geluidstools hebben VibeDeck PRO nodig.":
        LANG_FAQ["nl"]["a_tools"],
    "VibeDeck PRO oferuje 3-dniowy darmowy okres próbny w planie rocznym, a do tego opcje miesięczne i Lifetime. Po okresie próbnym darmowa wersja odtwarza Twoją muzykę (także w tle). Equalizer, limiter i inne narzędzia dźwięku wymagają VibeDeck PRO.":
        LANG_FAQ["pl"]["a_tools"],
    "O VibeDeck PRO oferece um teste gratuito de 3 dias no plano anual, além de opções mensais e Lifetime. Depois do teste, a versão gratuita toca sua música (inclusive em segundo plano). O equalizador, o limitador e as outras ferramentas de som precisam do VibeDeck PRO.":
        LANG_FAQ["pt-br"]["a_tools"],
    "VibeDeck PRO предлагает бесплатный пробный период 3 дня на годовом тарифе, а также месячный тариф и Lifetime. После пробного периода бесплатная версия играет вашу музыку (в том числе в фоне). EQ, лимитер и другие инструменты звука требуют VibeDeck PRO.":
        LANG_FAQ["ru"]["a_tools"],
    "VibeDeck PRO ให้ทดลองใช้ฟรี 3 วันสำหรับแพ็กเกจรายปี และยังมีแพ็กเกจรายเดือนกับ Lifetime ด้วย หลังจากทดลองใช้แล้ว เวอร์ชันฟรีเล่นเพลงได้ รวมถึงเล่นเบื้องหลัง อีควอไลเซอร์ ลิมิตเตอร์ และเครื่องมือเสียงอื่น ๆ ต้องใช้ VibeDeck PRO":
        LANG_FAQ["th"]["a_tools"],
    "VibeDeck PRO, yıllık planda 3 günlük ücretsiz deneme sunar; aylık ve Lifetime seçenekleri de var. Deneme bitince ücretsiz sürüm müzik çalar, arka planda da. Ekolayzer, limiter ve diğer ses araçları VibeDeck PRO gerektirir.":
        LANG_FAQ["tr"]["a_tools"],
    "VibeDeck PRO пропонує безкоштовний пробний період 3 дні на річному тарифі, а також місячний тариф і Lifetime. Після пробного періоду безкоштовна версія грає вашу музику (зокрема у фоні). Еквалайзер, лімітер та інші інструменти звуку потребують VibeDeck PRO.":
        LANG_FAQ["uk"]["a_tools"],
    "VibeDeck PRO có bản dùng thử miễn phí 3 ngày cho gói năm, cùng các lựa chọn gói tháng và Lifetime. Sau khi dùng thử, bản miễn phí phát nhạc (kể cả chạy nền). Equalizer, limiter và các công cụ âm thanh khác cần VibeDeck PRO.":
        LANG_FAQ["vi"]["a_tools"],
    "VibeDeck PRO 在年付方案中提供 3 天免费试用，另有月付和 Lifetime 可选。试用结束后，免费版可以播放音乐，也能后台播放。均衡器、限幅器和其他声音工具需要 VibeDeck PRO。":
        LANG_FAQ["zh-hans"]["a_tools"],
    "VibeDeck PRO 在年繳方案中提供 3 天免費試用，另有月繳和 Lifetime 可選。試用結束後，免費版可以播放音樂，也能背景播放。等化器、限幅器和其他聲音工具需要 VibeDeck PRO。":
        LANG_FAQ["zh-hant"]["a_tools"],

    # --- FLAC page headings ("Free and PRO" -> "VibeDeck PRO") ---
    "<h2>Kostenlos und PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Gratis y PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Gratuit et PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Gratis dan PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Gratis e PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>無料版とPRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>무료와 PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Gratis en PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Darmowa wersja i PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Бесплатно и PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>ฟรีและ PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Ücretsiz ve PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>Miễn phí và PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>免费版与 PRO</h2>": "<h2>VibeDeck PRO</h2>",
    "<h2>免費版與 PRO</h2>": "<h2>VibeDeck PRO</h2>",

    # --- English subpage body sentences ---
    "The core player is free with no ads. The 3-band or 8-band EQ and the limiter are part of VibeDeck PRO.":
        "VibeDeck Player works on iOS and Android with no ads. The 3-band DJ EQ, 8-band equalizer and limiter are part of VibeDeck PRO, available via subscription or one-time Lifetime access inside the app.",
    "The offline player built around the checklist. Free, no ads.":
        "The offline music player built around the checklist. Available on iOS and Android, with no ads and no account.",
    "Pitch control is part of VibeDeck PRO; the player itself is free with no ads.":
        "Pitch control is part of VibeDeck PRO, available on iOS and Android via subscription or one-time Lifetime access inside the app, with no ads.",
    "Studio is the creative toolkit in VibeDeck Player; the core player is free with no ads and no account.":
        "Studio is the creative toolkit in VibeDeck Player, available on iOS and Android with no ads and no account via subscription or one-time Lifetime access inside the app.",
    "The filter is part of VibeDeck Studio, the creative toolkit in VibeDeck Player. The core player is free with no ads.":
        "The filter is part of VibeDeck Studio, the creative toolkit in VibeDeck Player, available on iOS and Android with no ads via subscription or one-time Lifetime access inside the app.",
    "Loops are part of VibeDeck Studio, the creative toolkit in VibeDeck Player. The core player is free with no ads.":
        "Loops are part of VibeDeck Studio, the creative toolkit in VibeDeck Player, available on iOS and Android with no ads via subscription or one-time Lifetime access inside the app.",
    "Changing the key (Pitch) is part of VibeDeck PRO. The download is free and has no ads.":
        "Changing the key (Pitch) is part of VibeDeck PRO, available on iOS and Android with no ads via subscription or one-time Lifetime access inside the app.",
    "The limiter is part of VibeDeck PRO; the player itself is free with no ads.":
        "The limiter is part of VibeDeck PRO, available on iOS and Android with no ads via subscription or one-time Lifetime access inside the app.",
    "Free music apps usually mean one thing: ads between your songs, or a paywall to remove them. VibeDeck Player is free and still shows nothing. No banners, no videos, no popups. The business model is an optional PRO upgrade for the sound engine, not your attention.":
        "Many music apps interrupt your listening with banners, video ads or tracking. VibeDeck Player shows nothing of the kind: no banners, no videos, no popups. Available on iOS and Android with a subscription or one-time Lifetime access inside the app.",
    "Play lossless FLAC offline on iPhone and iPad, with a real EQ, pitch and tempo. Download free.":
        "Play lossless FLAC offline on iPhone and iPad, with a real EQ, pitch and tempo. Available on the App Store.",
    "Tempo and pitch are part of VibeDeck PRO; the player itself is free with no ads.":
        "Tempo and pitch are part of VibeDeck PRO, available on iOS and Android with no ads via subscription or one-time Lifetime access inside the app.",
    "VibeDeck Player is made by Yuliy Metelskiy. It is free to download, and some sound tools are part of VibeDeck PRO.":
        "VibeDeck Player is made by Yuliy Metelskiy. Available on iOS and Android, with a subscription or one-time Lifetime access inside the app for VibeDeck PRO.",

    # --- German subpage body sentences ---
    "Der Player ist kostenlos und werbefrei. VibeDeck PRO schaltet die komplette Sound-Engine frei: Tonhöhe und Filter, 3-Band-DJ-EQ oder 8-Band-Equalizer, Limiter, VibeMod, TONE, AURA und Smart Metadata. Den Preis zeigt der Store in deinem Land.":
        "VibeDeck Player ist für iOS und Android ohne Werbung verfügbar. VibeDeck PRO schaltet die komplette Sound-Engine frei: Tonhöhe und Filter, 3-Band-DJ-EQ oder 8-Band-Equalizer, Limiter, VibeMod, TONE, AURA und Smart Metadata. Zugang per Abo oder einmaligem Lifetime-Kauf direkt in der App.",
    "Die Basis-App ist kostenlos. VibeDeck PRO ist ein optionaler Kauf, der die komplette Sound-Engine freischaltet: Tonhöhe und Filter, 3-Band-DJ-EQ oder 8-Band-Equalizer, Limiter, VibeMod, TONE, AURA und Smart Metadata. Auch ohne PRO bleibt die App werbefrei.":
        "VibeDeck Player ist für iOS und Android ohne Werbung verfügbar. VibeDeck PRO schaltet die komplette Sound-Engine frei: Tonhöhe und Filter, 3-Band-DJ-EQ oder 8-Band-Equalizer, Limiter, VibeMod, TONE, AURA und Smart Metadata. Zugang per Abo oder einmaligem Lifetime-Kauf direkt in der App.",
    "Keine Banner, keine Videos, keine gesponserten Pop-ups. Weder in der kostenlosen Version noch in PRO.":
        "Keine Banner, keine Videos, keine gesponserten Pop-ups. Nichts unterbricht deine Musik.",
    "Kostenlose Musik-Apps kosten meist auf andere Art: Werbung zwischen den Songs oder eine Gebühr, um sie loszuwerden. VibeDeck Player ist kostenlos und zeigt trotzdem nichts an. Finanziert wird er durch ein optionales PRO-Upgrade für den Sound, nicht durch deine Aufmerksamkeit.":
        "Viele Musik-Apps unterbrechen deine Songs mit Werbung oder Tracking. VibeDeck Player zeigt keine Werbung und braucht kein Konto. Verfügbar für iOS und Android per Abo oder einmaligem Lifetime-Zugang in der App.",
    "Tempo und Tonhöhe gehören zu VibeDeck PRO; der Player selbst ist kostenlos und ohne Werbung.":
        "Tempo und Tonhöhe gehören zu VibeDeck PRO, verfügbar für iOS und Android ohne Werbung per Abo oder einmaligem Lifetime-Zugang in der App.",
    "Die Tonartänderung (Pitch) ist eine Funktion von VibeDeck PRO. Der Download ist kostenlos und werbefrei.":
        "Die Tonartänderung (Pitch) ist eine Funktion von VibeDeck PRO, verfügbar für iOS und Android ohne Werbung per Abo oder einmaligem Lifetime-Zugang in der App.",

    # --- Spanish subpage body sentences ---
    "El tempo y el tono forman parte de VibeDeck PRO; el reproductor es gratis y sin anuncios.":
        "El tempo y el tono forman parte de VibeDeck PRO, disponible en iOS y Android sin anuncios mediante suscripción o acceso Lifetime de pago único dentro de la app.",
    "El reproductor es gratis y no tiene anuncios. VibeDeck PRO desbloquea el motor de sonido completo: tono y filtro, EQ DJ de 3 bandas o ecualizador de 8 bandas, limitador, VibeMod, TONE, AURA y Smart Metadata. El precio aparece en la tienda de tu país.":
        "VibeDeck Player está disponible en iOS y Android sin anuncios. VibeDeck PRO desbloquea el motor de sonido completo: tono y filtro, EQ DJ de 3 bandas o ecualizador de 8 bandas, limitador, VibeMod, TONE, AURA y Smart Metadata, mediante suscripción o acceso Lifetime de pago único dentro de la app.",
    "La app básica es gratis. VibeDeck PRO es una compra opcional que desbloquea el motor de sonido completo: tono y filtro, EQ DJ de 3 bandas o ecualizador de 8 bandas, limitador, VibeMod, TONE, AURA y Smart Metadata. Sin PRO, la app sigue sin anuncios.":
        "VibeDeck Player está disponible en iOS y Android sin anuncios. VibeDeck PRO desbloquea el motor de sonido completo: tono y filtro, EQ DJ de 3 bandas o ecualizador de 8 bandas, limitador, VibeMod, TONE, AURA y Smart Metadata, mediante suscripción o acceso Lifetime de pago único dentro de la app.",
    "Las apps de música gratis suelen cobrar de otra forma: anuncios entre canciones o un pago para quitarlos. VibeDeck Player es gratis y no muestra nada. Se financia con una mejora PRO opcional para el sonido, no con tu atención.":
        "Muchas apps de música interrumpen tus canciones con anuncios o rastreo. VibeDeck Player no muestra anuncios ni pide cuenta. Disponible en iOS y Android mediante suscripción o acceso Lifetime de pago único dentro de la app.",
    "Sin banners, sin videos y sin ventanas emergentes patrocinadas. Ni en la versión gratuita ni en PRO.":
        "Sin banners, sin videos y sin ventanas emergentes patrocinadas. Nada interrumpe tu música.",

    # --- French subpage body sentences ---
    "Le changement de tonalité (Pitch) est une fonction de VibeDeck PRO. Le téléchargement est gratuit et sans publicité.":
        "Le changement de tonalité (Pitch) fait partie de VibeDeck PRO, disponible sur iOS et Android sans publicité par abonnement ou accès Lifetime en paiement unique dans l’application.",
    "Le lecteur est gratuit et sans publicité. VibeDeck PRO débloque tout le moteur sonore\xa0: hauteur et filtre, EQ DJ 3 bandes ou égaliseur 8 bandes, limiteur, VibeMod, TONE, AURA et Smart Metadata. Le prix s’affiche sur le store de votre pays.":
        "VibeDeck Player est disponible sur iOS et Android sans publicité. VibeDeck PRO débloque tout le moteur sonore\xa0: hauteur et filtre, EQ DJ 3 bandes ou égaliseur 8 bandes, limiteur, VibeMod, TONE, AURA et Smart Metadata, par abonnement ou accès Lifetime en paiement unique dans l’application.",
    "Les applis de musique gratuites se paient autrement\xa0: des pubs entre les morceaux, ou un abonnement pour les supprimer. VibeDeck Player est gratuit et n’affiche rien. Il se finance par une option PRO pour le son, pas par votre attention.":
        "Beaucoup d’applis de musique coupent vos morceaux avec des publicités ou du suivi. VibeDeck Player n’affiche aucune publicité et ne demande aucun compte. Disponible sur iOS et Android par abonnement ou accès Lifetime en paiement unique dans l’application.",
    "L’application de base est gratuite. VibeDeck PRO est un achat facultatif qui débloque tout le moteur sonore\xa0: hauteur et filtre, EQ DJ 3 bandes ou égaliseur 8 bandes, limiteur, VibeMod, TONE, AURA et Smart Metadata. Sans PRO, l’appli reste sans pub.":
        "VibeDeck Player est disponible sur iOS et Android sans publicité. VibeDeck PRO débloque tout le moteur sonore\xa0: hauteur et filtre, EQ DJ 3 bandes ou égaliseur 8 bandes, limiteur, VibeMod, TONE, AURA et Smart Metadata, par abonnement ou accès Lifetime en paiement unique dans l’application.",
    "Ni bannières, ni vidéos, ni pop-ups sponsorisés. Ni dans la version gratuite, ni dans PRO.":
        "Ni bannières, ni vidéos, ni pop-ups sponsorisés. Rien ne coupe votre musique.",
    "Le tempo et la hauteur font partie de VibeDeck PRO ; le lecteur lui-même est gratuit et sans pub.":
        "Le tempo et la hauteur font partie de VibeDeck PRO, disponible sur iOS et Android sans publicité par abonnement ou accès Lifetime en paiement unique dans l’application.",

    # --- Indonesian subpage body sentences ---
    "Tempo dan nada termasuk dalam VibeDeck PRO; pemutarnya sendiri gratis dan tanpa iklan.":
        "Tempo dan nada termasuk dalam VibeDeck PRO, tersedia di iOS dan Android tanpa iklan melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
    "Pemutarnya gratis dan tanpa iklan. VibeDeck PRO membuka seluruh mesin suara: nada dan filter, EQ DJ 3 band atau equalizer 8 band, limiter, VibeMod, TONE, AURA, dan Smart Metadata. Harga tampil di toko aplikasi negaramu.":
        "VibeDeck Player tersedia di iOS dan Android tanpa iklan. VibeDeck PRO membuka seluruh mesin suara: nada dan filter, EQ DJ 3 band atau equalizer 8 band, limiter, VibeMod, TONE, AURA, dan Smart Metadata, melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
    "Aplikasi dasarnya gratis. VibeDeck PRO adalah pembelian opsional yang membuka seluruh mesin suara: nada dan filter, EQ DJ 3 band atau equalizer 8 band, limiter, VibeMod, TONE, AURA, dan Smart Metadata. Tanpa PRO pun aplikasinya tetap tanpa iklan.":
        "VibeDeck Player tersedia di iOS dan Android tanpa iklan. VibeDeck PRO membuka seluruh mesin suara: nada dan filter, EQ DJ 3 band atau equalizer 8 band, limiter, VibeMod, TONE, AURA, dan Smart Metadata, melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
    "Aplikasi musik gratis biasanya dibayar dengan cara lain: iklan di antara lagu, atau langganan untuk menghilangkannya. VibeDeck Player gratis dan tidak menampilkan apa pun. Aplikasi ini dibiayai oleh PRO untuk suara, bukan oleh perhatianmu.":
        "Banyak aplikasi musik memotong lagumu dengan iklan atau pelacakan. VibeDeck Player tidak menampilkan iklan dan tidak meminta akun. Tersedia di iOS dan Android melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",
    "Tanpa banner, tanpa video, tanpa pop-up bersponsor. Di versi gratis maupun PRO.":
        "Tanpa banner, tanpa video, tanpa pop-up bersponsor. Tidak ada yang mengganggu musikmu.",
    "Pengubah nada (Pitch) adalah fitur VibeDeck PRO. Unduhannya gratis dan tanpa iklan.":
        "Pengubah nada (Pitch) adalah fitur VibeDeck PRO, tersedia di iOS dan Android tanpa iklan melalui langganan atau akses Lifetime sekali bayar di dalam aplikasi.",

    # --- Italian subpage body sentences ---
    "Il cambio di tonalità, chiamato Pitch, fa parte di VibeDeck PRO. Il download è gratuito e senza pubblicità.":
        "Il cambio di tonalità (Pitch) fa parte di VibeDeck PRO, disponibile su iOS e Android senza pubblicità tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",
    "Il lettore è gratuito e senza pubblicità. VibeDeck PRO sblocca il motore audio completo: pitch e filtro, EQ DJ a 3 bande o equalizzatore a 8 bande, limiter, VibeMod, TONE, AURA e Smart Metadata. I prezzi di PRO dipendono dal paese e sono indicati su App Store e Google Play.":
        "VibeDeck Player è disponibile su iOS e Android senza pubblicità. VibeDeck PRO sblocca il motore audio completo: pitch e filtro, EQ DJ a 3 bande o equalizzatore a 8 bande, limiter, VibeMod, TONE, AURA e Smart Metadata, tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",
    "L’app di base è gratuita. VibeDeck PRO è un acquisto facoltativo che sblocca il motore audio completo: pitch e filtro, EQ DJ a 3 bande o equalizzatore a 8 bande, limiter, VibeMod, TONE, AURA e Smart Metadata. Anche senza PRO, l’app resta senza pubblicità.":
        "VibeDeck Player è disponibile su iOS e Android senza pubblicità. VibeDeck PRO sblocca il motore audio completo: pitch e filtro, EQ DJ a 3 bande o equalizzatore a 8 bande, limiter, VibeMod, TONE, AURA e Smart Metadata, tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",
    "Molte app gratuite mostrano pubblicità o richiedono un abbonamento per rimuoverla. VibeDeck Player non mostra pubblicità: si sostiene con un’opzione PRO per le funzioni audio, non con la tua attenzione.":
        "Molte app musicali interrompono l’ascolto con pubblicità o tracciamento. VibeDeck Player non mostra pubblicità e non richiede account. Disponibile su iOS e Android tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",
    "Niente banner, video o pop-up pubblicitari, né nella versione gratuita né in PRO.":
        "Niente banner, video o pop-up pubblicitari. Nulla interrompe la tua musica.",
    "Tempo e intonazione fanno parte di VibeDeck PRO; il lettore è gratuito e senza pubblicità.":
        "Tempo e intonazione fanno parte di VibeDeck PRO, disponibile su iOS e Android senza pubblicità tramite abbonamento o accesso Lifetime con pagamento unico all’interno dell’app.",

    # --- Japanese subpage body sentences ---
    "プレーヤー本体は無料で、広告はありません。VibeDeck PROでは、ピッチとフィルター、3バンドDJ EQまたは8バンドイコライザー、リミッター、VibeMod、TONE、AURA、Smart Metadataを含むサウンドエンジン全体が使えるようになります。":
        "VibeDeck PlayerはiOSとAndroidで広告なしで使えます。VibeDeck PROでは、ピッチとフィルター、3バンドDJ EQまたは8バンドイコライザー、リミッター、VibeMod、TONE、AURA、Smart Metadataを含むサウンドエンジン全体が使えます。アプリ内のサブスクリプションまたは買い切りのLifetimeアクセスで利用できます。",
    "キー変更（ピッチ）はVibeDeck PROの機能です。アプリのダウンロードは無料で、広告はありません。":
        "キー変更（ピッチ）はVibeDeck PROの機能です。iOSとAndroidで広告なしで使え、アプリ内のサブスクリプションまたは買い切りのLifetimeアクセスで利用できます。",
    "テンポとピッチの調整はVibeDeck PROの機能です。アプリのダウンロードは無料で、広告はありません。":
        "テンポとピッチの調整はVibeDeck PROの機能です。iOSとAndroidで広告なしで使え、アプリ内のサブスクリプションまたは買い切りのLifetimeアクセスで利用できます。",

    # --- Korean subpage body sentences ---
    "플레이어는 무료이고 광고가 없습니다. VibeDeck PRO를 사용하면 피치와 필터, 3밴드 DJ EQ 또는 8밴드 이퀄라이저, 리미터, VibeMod, TONE, AURA, Smart Metadata까지 사운드 엔진 전체를 쓸 수 있습니다. 가격은 내 나라의 스토어에 표시됩니다.":
        "VibeDeck Player는 iOS와 Android에서 광고 없이 이용할 수 있습니다. VibeDeck PRO를 사용하면 피치와 필터, 3밴드 DJ EQ 또는 8밴드 이퀄라이저, 리미터, VibeMod, TONE, AURA, Smart Metadata까지 사운드 엔진 전체를 쓸 수 있으며, 앱 내 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",
    "키 변경(Pitch)은 VibeDeck PRO 기능입니다. 다운로드는 무료이고 광고가 없습니다.":
        "키 변경(Pitch)은 VibeDeck PRO 기능입니다. iOS와 Android에서 광고 없이 앱 내 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",
    "기본 앱은 무료입니다. VibeDeck PRO는 선택 구매이며 피치와 필터, 3밴드 DJ EQ 또는 8밴드 이퀄라이저, 리미터, VibeMod, TONE, AURA, Smart Metadata까지 사운드 엔진 전체를 열어 줍니다. PRO 없이도 광고는 없습니다.":
        "VibeDeck Player는 iOS와 Android에서 광고 없이 이용할 수 있습니다. VibeDeck PRO는 피치와 필터, 3밴드 DJ EQ 또는 8밴드 이퀄라이저, 리미터, VibeMod, TONE, AURA, Smart Metadata까지 사운드 엔진 전체를 열어 주며, 앱 내 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",
    "무료 음악 앱은 다른 방식으로 대가를 받습니다. 곡 사이에 광고를 넣거나, 광고를 없애려면 구독하게 만들죠. VibeDeck Player는 무료이고 아무것도 띄우지 않습니다. 수익은 여러분의 관심이 아니라 사운드용 PRO에서 나옵니다.":
        "많은 음악 앱이 곡 사이에 광고를 넣거나 사용자를 추적합니다. VibeDeck Player는 광고가 없고 계정도 필요 없습니다. iOS와 Android 앱 내에서 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",
    "배너도, 동영상도, 스폰서 팝업도 없습니다. 무료 버전에도, PRO에도.":
        "배너도, 동영상도, 스폰서 팝업도 없습니다. 음악 감상을 방해하는 요소가 없습니다.",
    "템포와 피치는 VibeDeck PRO 기능이며, 플레이어 자체는 무료이고 광고가 없습니다.":
        "템포와 피치는 VibeDeck PRO 기능이며, iOS와 Android에서 광고 없이 앱 내 구독 또는 일회성 Lifetime 이용권으로 이용할 수 있습니다.",

    # --- Dutch subpage body sentences ---
    "De speler is gratis en zonder advertenties. VibeDeck PRO ontgrendelt de hele geluidsengine: toonhoogte en filter, 3-bands DJ-EQ of 8-bands equalizer, limiter, VibeMod, TONE, AURA en Smart Metadata. De prijs zie je in de store van jouw land.":
        "VibeDeck Player is beschikbaar op iOS en Android zonder advertenties. VibeDeck PRO ontgrendelt de hele geluidsengine: toonhoogte en filter, 3-bands DJ-EQ of 8-bands equalizer, limiter, VibeMod, TONE, AURA en Smart Metadata, via een abonnement of eenmalige Lifetime-toegang in de app.",
    "De basisapp is gratis. VibeDeck PRO is een optionele aankoop die de hele geluidsengine ontgrendelt: toonhoogte en filter, 3-bands DJ-EQ of 8-bands equalizer, limiter, VibeMod, TONE, AURA en Smart Metadata. Ook zonder PRO blijft de app vrij van advertenties.":
        "VibeDeck Player is beschikbaar op iOS en Android zonder advertenties. VibeDeck PRO ontgrendelt de hele geluidsengine: toonhoogte en filter, 3-bands DJ-EQ of 8-bands equalizer, limiter, VibeMod, TONE, AURA en Smart Metadata, via een abonnement of eenmalige Lifetime-toegang in de app.",
    "Geen banners, geen video’s, geen gesponsorde pop-ups. Niet in de gratis versie en niet in PRO.":
        "Geen banners, geen video’s, geen gesponsorde pop-ups. Niets onderbreekt je muziek.",
    "Gratis muziekapps laten je op een andere manier betalen: advertenties tussen nummers, of een abonnement om ze weg te halen. VibeDeck Player is gratis en toont niets. De app verdient aan PRO voor het geluid, niet aan jouw aandacht.":
        "Veel muziekapps onderbreken je nummers met advertenties of tracking. VibeDeck Player toont geen advertenties en vraagt geen account. Beschikbaar op iOS en Android via een abonnement of eenmalige Lifetime-toegang in de app.",
    "Tempo en toonhoogte horen bij VibeDeck PRO; de speler zelf is gratis en zonder advertenties.":
        "Tempo en toonhoogte horen bij VibeDeck PRO, beschikbaar op iOS en Android zonder advertenties via een abonnement of eenmalige Lifetime-toegang in de app.",
    "Toonsoort veranderen (Pitch) is een functie van VibeDeck PRO. Downloaden is gratis en zonder advertenties.":
        "Toonsoort veranderen (Pitch) is een functie van VibeDeck PRO, beschikbaar op iOS en Android zonder advertenties via een abonnement of eenmalige Lifetime-toegang in de app.",

    # --- Polish subpage body sentences ---
    "Odtwarzacz jest darmowy i bez reklam. VibeDeck PRO odblokowuje cały silnik dźwięku: wysokość dźwięku i filtr, 3-pasmowy korektor DJ lub 8-pasmowy, limiter, VibeMod, TONE, AURA i Smart Metadata. Cena jest widoczna w sklepie w Twoim kraju.":
        "VibeDeck Player jest dostępny na iOS i Androida bez reklam. VibeDeck PRO odblokowuje cały silnik dźwięku: wysokość dźwięku i filtr, 3-pasmowy korektor DJ lub 8-pasmowy, limiter, VibeMod, TONE, AURA i Smart Metadata, w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",
    "Podstawowa aplikacja jest darmowa. VibeDeck PRO to opcjonalny zakup, który odblokowuje cały silnik dźwięku: wysokość dźwięku i filtr, 3-pasmowy korektor DJ lub 8-pasmowy, limiter, VibeMod, TONE, AURA i Smart Metadata. Bez PRO aplikacja też nie ma reklam.":
        "VibeDeck Player jest dostępny na iOS i Androida bez reklam. VibeDeck PRO odblokowuje cały silnik dźwięku: wysokość dźwięku i filtr, 3-pasmowy korektor DJ lub 8-pasmowy, limiter, VibeMod, TONE, AURA i Smart Metadata, w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",
    "Za darmowe aplikacje muzyczne płaci się inaczej: reklamami między utworami albo abonamentem, żeby je wyłączyć. VibeDeck Player jest darmowy i niczego nie wyświetla. Utrzymuje się z PRO dla dźwięku, a nie z Twojej uwagi.":
        "Wiele aplikacji muzycznych przerywa muzykę reklamami albo śledzi użytkowników. VibeDeck Player nie wyświetla żadnych reklam i nie wymaga konta. Dostępny na iOS i Androida w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",
    "Żadnych banerów, filmów ani sponsorowanych okienek. Ani w wersji darmowej, ani w PRO.":
        "Żadnych banerów, filmów ani sponsorowanych okienek. Nic nie przerywa Twojej muzyki.",
    "Zmiana tonacji (Pitch) jest funkcją VibeDeck PRO. Pobranie jest darmowe i bez reklam.":
        "Zmiana tonacji (Pitch) jest funkcją VibeDeck PRO, dostępnego na iOS i Androida bez reklam w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",
    "Tempo i wysokość dźwięku są częścią VibeDeck PRO; sam odtwarzacz jest darmowy i bez reklam.":
        "Tempo i wysokość dźwięku są częścią VibeDeck PRO, dostępnego na iOS i Androida bez reklam w ramach subskrypcji lub jednorazowego dostępu Lifetime w aplikacji.",

    # --- Portuguese (BR) subpage body sentences ---
    "Tempo e tom fazem parte do VibeDeck PRO; o player é gratuito e sem anúncios.":
        "Tempo e tom fazem parte do VibeDeck PRO, disponível para iOS e Android sem anúncios por assinatura ou acesso Lifetime em pagamento único dentro do aplicativo.",
    "O player básico é grátis; o VibeDeck PRO libera o motor de som completo, com tom e filtro, EQ DJ de 3 bandas ou equalizador de 8 bandas e limitador. No iPhone e no iPad o app também toca FLAC.":
        "O VibeDeck Player está disponível para iOS e Android sem anúncios. O VibeDeck PRO libera o motor de som completo, com tom e filtro, EQ DJ de 3 bandas ou equalizador de 8 bandas e limitador, por assinatura ou acesso Lifetime em pagamento único dentro do aplicativo.",
    "O player básico é grátis e sem anúncios. O VibeDeck PRO libera o motor de som completo: tom e filtro, EQ DJ de 3 bandas ou equalizador de 8 bandas, limitador, VibeMod, TONE, AURA e Smart Metadata.":
        "O VibeDeck Player está disponível para iOS e Android sem anúncios. O VibeDeck PRO libera o motor de som completo: tom e filtro, EQ DJ de 3 bandas ou equalizador de 8 bandas, limitador, VibeMod, TONE, AURA e Smart Metadata, por assinatura ou acesso Lifetime em pagamento único dentro do aplicativo.",

    # --- Russian subpage body sentences ---
    "Плеер бесплатный и без рекламы. VibeDeck PRO открывает все звуковые функции: высоту тона и фильтр, 3-полосный DJ эквалайзер или 8-полосный, лимитер, VibeMod, TONE, AURA и Smart Metadata. Цена указана в магазине приложений вашей страны.":
        "VibeDeck Player доступен на iOS и Android без рекламы. VibeDeck PRO открывает все звуковые функции: высоту тона и фильтр, 3-полосный DJ эквалайзер или 8-полосный, лимитер, VibeMod, TONE, AURA и Smart Metadata, по подписке или с разовым Lifetime-доступом внутри приложения.",
    "Базовое приложение бесплатное. VibeDeck PRO покупается по желанию и открывает все звуковые функции: высоту тона и фильтр, 3-полосный DJ эквалайзер или 8-полосный, лимитер, VibeMod, TONE, AURA и Smart Metadata. Без PRO рекламы тоже нет.":
        "VibeDeck Player доступен на iOS и Android без рекламы. VibeDeck PRO открывает все звуковые функции: высоту тона и фильтр, 3-полосный DJ эквалайзер или 8-полосный, лимитер, VibeMod, TONE, AURA и Smart Metadata, по подписке или с разовым Lifetime-доступом внутри приложения.",
    "Бесплатные музыкальные приложения берут плату по-другому: реклама между треками или подписка, чтобы её убрать. VibeDeck Player бесплатный и ничего лишнего не показывает. Он зарабатывает на PRO для звука, а не на вашем внимании.":
        "Многие музыкальные приложения прерывают треки рекламой или собирают данные пользователей. VibeDeck Player не показывает рекламу и не требует аккаунта. Приложение доступно на iOS и Android по подписке или с разовым Lifetime-доступом внутри приложения.",
    "Ни баннеров, ни видео, ни рекламных всплывающих окон. Ни в бесплатной версии, ни в PRO.":
        "Ни баннеров, ни видео, ни рекламных всплывающих окон. Ничто не прерывает вашу музыку.",
    "Смена тональности (Pitch) входит в VibeDeck PRO. Скачать приложение можно бесплатно, рекламы нет.":
        "Смена тональности (Pitch) входит в VibeDeck PRO, доступный на iOS и Android без рекламы по подписке или с разовым Lifetime-доступом внутри приложения.",
    "Темп и высота тона входят в VibeDeck PRO, а сам плеер бесплатный и без рекламы.":
        "Темп и высота тона входят в VibeDeck PRO, доступный на iOS и Android без рекламы по подписке или с разовым Lifetime-доступом внутри приложения.",

    # --- Thai subpage body sentences ---
    "เครื่องเล่นใช้ฟรีและไม่มีโฆษณา VibeDeck PRO ปลดล็อกเอนจินเสียงครบชุด: ระดับเสียงและฟิลเตอร์ DJ EQ 3 แบนด์หรืออีควอไลเซอร์ 8 แบนด์ ลิมิตเตอร์ VibeMod, TONE, AURA และ Smart Metadata ราคาแสดงตามสโตร์ของประเทศคุณ":
        "VibeDeck Player พร้อมใช้งานบน iOS และ Android โดยไม่มีโฆษณา VibeDeck PRO ปลดล็อกเอนจินเสียงครบชุด: ระดับเสียงและฟิลเตอร์ DJ EQ 3 แบนด์หรืออีควอไลเซอร์ 8 แบนด์ ลิมิตเตอร์ VibeMod, TONE, AURA และ Smart Metadata ผ่านการสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",
    "แอปพื้นฐานใช้ฟรี VibeDeck PRO เป็นการซื้อที่ไม่บังคับ ปลดล็อกเอนจินเสียงครบชุด: ระดับเสียงและฟิลเตอร์ DJ EQ 3 แบนด์หรืออีควอไลเซอร์ 8 แบนด์ ลิมิตเตอร์ VibeMod, TONE, AURA และ Smart Metadata แม้ไม่ซื้อ PRO แอปก็ไม่มีโฆษณา":
        "VibeDeck Player พร้อมใช้งานบน iOS และ Android โดยไม่มีโฆษณา VibeDeck PRO ปลดล็อกเอนจินเสียงครบชุด: ระดับเสียงและฟิลเตอร์ DJ EQ 3 แบนด์หรืออีควอไลเซอร์ 8 แบนด์ ลิมิตเตอร์ VibeMod, TONE, AURA และ Smart Metadata ผ่านการสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",
    "แอปเพลงฟรีมักเก็บเงินคุณด้วยวิธีอื่น เช่น โฆษณาระหว่างเพลง หรือให้สมัครสมาชิกเพื่อปิดโฆษณา VibeDeck Player ใช้ฟรีและไม่แสดงอะไรเลย แอปอยู่ได้ด้วยตัวเลือก PRO สำหรับเสียง ไม่ใช่ด้วยความสนใจของคุณ":
        "แอปเพลงจำนวนมากมักมีโฆษณาคั่นระหว่างเพลงหรือมีการติดตามผู้ใช้ VibeDeck Player ไม่มีโฆษณาและไม่ต้องมีบัญชี พร้อมใช้งานบน iOS และ Android ผ่านการสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",
    "ไม่มีแบนเนอร์ วิดีโอ หรือป๊อปอัปโฆษณา ทั้งในเวอร์ชันฟรีและใน PRO":
        "ไม่มีแบนเนอร์ วิดีโอ หรือป๊อปอัปโฆษณา ไม่มีสิ่งใดมาขัดจังหวะเพลงของคุณ",
    "การเปลี่ยนคีย์ (Pitch) เป็นฟีเจอร์ของ VibeDeck PRO ดาวน์โหลดฟรีและไม่มีโฆษณา":
        "การเปลี่ยนคีย์ (Pitch) เป็นฟีเจอร์ของ VibeDeck PRO พร้อมใช้งานบน iOS และ Android โดยไม่มีโฆษณา ผ่านการสมัครสมาชิกหรือสิทธิ์ Lifetime แบบซื้อครั้งเดียวภายในแอป",

    # --- Turkish subpage body sentences ---
    "Çalar ücretsiz ve reklamsız. VibeDeck PRO tüm ses motorunun kilidini açar: ton ve filtre, 3 bantlı DJ EQ veya 8 bantlı ekolayzer, limiter, VibeMod, TONE, AURA ve Smart Metadata. Fiyat, ülkendeki mağazada görünür.":
        "VibeDeck Player, iOS ve Android için reklamsız olarak kullanılabilir. VibeDeck PRO tüm ses motorunun kilidini açar: ton ve filtre, 3 bantlı DJ EQ veya 8 bantlı ekolayzer, limiter, VibeMod, TONE, AURA ve Smart Metadata; uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",
    "Banner yok, video yok, sponsorlu açılır pencere yok. Ne ücretsiz sürümde ne PRO’da.":
        "Banner yok, video yok, sponsorlu açılır pencere yok. Müziğini hiçbir şey bölmez.",
    "Temel uygulama ücretsiz. VibeDeck PRO isteğe bağlı bir satın almadır ve tüm ses motorunun kilidini açar: ton ve filtre, 3 bantlı DJ EQ veya 8 bantlı ekolayzer, limiter, VibeMod, TONE, AURA ve Smart Metadata. PRO olmadan da uygulama reklamsızdır.":
        "VibeDeck Player, iOS ve Android için reklamsız olarak kullanılabilir. VibeDeck PRO tüm ses motorunun kilidini açar: ton ve filtre, 3 bantlı DJ EQ veya 8 bantlı ekolayzer, limiter, VibeMod, TONE, AURA ve Smart Metadata; uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",
    "Ücretsiz müzik uygulamalarının bedeli başka türlü ödenir: şarkı aralarında reklamlar ya da onları kaldırmak için abonelik. VibeDeck Player ücretsiz ve hiçbir şey göstermez. Gelirini senin dikkatinden değil, ses için sunulan PRO’dan elde eder.":
        "Pek çok müzik uygulaması şarkıların arasına reklam koyar ya da seni takip eder. VibeDeck Player hiç reklam göstermez ve hesap gerektirmez. iOS ve Android’de uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",
    "Ton değiştirme (Pitch) VibeDeck PRO’nun bir özelliğidir. İndirmesi ücretsiz ve reklamsız.":
        "Ton değiştirme (Pitch) VibeDeck PRO’nun bir özelliğidir; iOS ve Android’de reklamsız olarak uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",
    "Tempo ve ton VibeDeck PRO’ya dahildir; çaların kendisi ücretsiz ve reklamsızdır.":
        "Tempo ve ton VibeDeck PRO’ya dahildir; iOS ve Android’de reklamsız olarak uygulama içi abonelik veya tek seferlik Lifetime erişimiyle kullanılabilir.",

    # --- Ukrainian subpage body sentences ---
    "Темп і висота тону входять до VibeDeck PRO, а сам плеєр безкоштовний і без реклами.":
        "Темп і висота тону входять до VibeDeck PRO, доступного на iOS та Android без реклами за підпискою або з разовим Lifetime-доступом усередині застосунку.",
    "Зміна тональності (Pitch) входить до VibeDeck PRO. Завантажити застосунок можна безкоштовно, реклами немає.":
        "Зміна тональності (Pitch) входить до VibeDeck PRO, доступного на iOS та Android без реклами за підпискою або з разовим Lifetime-доступом усередині застосунку.",

    # --- Vietnamese subpage body sentences ---
    "Đổi tone (Pitch) là tính năng của VibeDeck PRO. Tải về miễn phí và không quảng cáo.":
        "Đổi tone (Pitch) là tính năng của VibeDeck PRO, có mặt trên iOS và Android không quảng cáo qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",
    "Tempo và cao độ thuộc VibeDeck PRO; trình phát thì miễn phí và không quảng cáo.":
        "Tempo và cao độ thuộc VibeDeck PRO, có mặt trên iOS và Android không quảng cáo qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",
    "Trình phát miễn phí và không quảng cáo. VibeDeck PRO mở khóa toàn bộ bộ máy âm thanh: cao độ và filter, EQ DJ 3 dải hoặc equalizer 8 dải, limiter, VibeMod, TONE, AURA và Smart Metadata. Giá hiển thị trên cửa hàng tại quốc gia của bạn.":
        "VibeDeck Player có mặt trên iOS và Android không quảng cáo. VibeDeck PRO mở khóa toàn bộ bộ máy âm thanh: cao độ và filter, EQ DJ 3 dải hoặc equalizer 8 dải, limiter, VibeMod, TONE, AURA và Smart Metadata, qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",
    "Không banner, không video, không pop-up tài trợ. Cả bản miễn phí lẫn PRO.":
        "Không banner, không video, không pop-up tài trợ. Không gì làm gián đoạn âm nhạc của bạn.",
    "Ứng dụng cơ bản miễn phí. VibeDeck PRO là gói mua tùy chọn, mở khóa toàn bộ bộ máy âm thanh: cao độ và filter, EQ DJ 3 dải hoặc equalizer 8 dải, limiter, VibeMod, TONE, AURA và Smart Metadata. Không có PRO thì ứng dụng vẫn không có quảng cáo.":
        "VibeDeck Player có mặt trên iOS và Android không quảng cáo. VibeDeck PRO mở khóa toàn bộ bộ máy âm thanh: cao độ và filter, EQ DJ 3 dải hoặc equalizer 8 dải, limiter, VibeMod, TONE, AURA và Smart Metadata, qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",
    "Ứng dụng nghe nhạc miễn phí thường bắt bạn trả theo cách khác: quảng cáo giữa các bài, hoặc trả phí để tắt chúng. VibeDeck Player miễn phí và không hiển thị gì cả. Ứng dụng sống nhờ gói PRO cho âm thanh, không phải nhờ sự chú ý của bạn.":
        "Nhiều ứng dụng nghe nhạc chèn quảng cáo giữa các bài hát hoặc theo dõi người dùng. VibeDeck Player không hiển thị quảng cáo và không yêu cầu tài khoản. Có mặt trên iOS và Android qua gói đăng ký hoặc quyền truy cập Lifetime trả một lần trong ứng dụng.",

    # --- Simplified Chinese subpage body sentences ---
    "速度与音高属于 VibeDeck PRO 功能；播放器本身免费且无广告。":
        "速度与音高属于 VibeDeck PRO 功能，支持 iOS 和 Android 且无广告，可在应用内通过订阅或一次性购买 Lifetime 权限解锁。",
    "播放器免费且无广告。VibeDeck PRO 解锁完整音效引擎：音高与滤波器、3 段 DJ EQ 或 8 段均衡器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata。价格以你所在国家或地区的应用商店为准。":
        "VibeDeck Player 支持 iOS 和 Android 且无广告。VibeDeck PRO 解锁完整音效引擎：音高与滤波器、3 段 DJ EQ 或 8 段均衡器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata，可在应用内通过订阅或一次性购买 Lifetime 权限解锁。",
    "免费音乐 App 往往用别的方式收费：歌曲之间插广告，或者要你订阅才能去掉广告。VibeDeck Player 免费，而且不显示任何广告。它靠可选的 PRO 音效功能维持，而不是靠你的注意力。":
        "许多音乐 App 会在歌曲之间插播广告或追踪用户。VibeDeck Player 没有任何广告，也不需要账号，支持 iOS 和 Android，可在应用内通过订阅或一次性购买 Lifetime 权限解锁。",
    "基础 App 免费。VibeDeck PRO 是可选购买，解锁完整音效引擎：音高与滤波器、3 段 DJ EQ 或 8 段均衡器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata。不买 PRO，App 也没有广告。":
        "VibeDeck Player 支持 iOS 和 Android 且无广告。VibeDeck PRO 解锁完整音效引擎：音高与滤波器、3 段 DJ EQ 或 8 段均衡器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata，可在应用内通过订阅或一次性购买 Lifetime 权限解锁。",
    "没有横幅、视频或赞助弹窗。免费版没有，PRO 也没有。":
        "没有横幅、视频或赞助弹窗，没有任何内容打断你的音乐。",
    "变调（Pitch）属于 VibeDeck PRO 功能。下载免费且无广告。":
        "变调（Pitch）属于 VibeDeck PRO 功能，支持 iOS 和 Android 且无广告，可在应用内通过订阅或一次性购买 Lifetime 权限解锁。",

    # --- Traditional Chinese subpage body sentences ---
    "速度與音高屬於 VibeDeck PRO 功能；播放器本身免費且無廣告。":
        "速度與音高屬於 VibeDeck PRO 功能，支援 iOS 與 Android 且無廣告，可在 App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",
    "播放器免費且無廣告。VibeDeck PRO 解鎖完整音效引擎：音高與濾波器、3 段 DJ EQ 或 8 段等化器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata。價格以你所在國家的商店為準。":
        "VibeDeck Player 支援 iOS 與 Android 且無廣告。VibeDeck PRO 解鎖完整音效引擎：音高與濾波器、3 段 DJ EQ 或 8 段等化器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata，可在 App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",
    "免費音樂 App 通常用別的方式讓你付出代價：歌曲之間的廣告，或付費訂閱才能去除廣告。VibeDeck Player 免費，而且什麼都不顯示。它靠音效的 PRO 營運，而不是靠你的注意力。":
        "許多音樂 App 會在歌曲之間插播廣告或追蹤使用者。VibeDeck Player 不顯示任何廣告，也不需要帳號，支援 iOS 與 Android，可在 App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",
    "基本 App 免費。VibeDeck PRO 是可選購買，能解鎖完整音效引擎：音高與濾波器、3 段 DJ EQ 或 8 段等化器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata。就算沒有 PRO，App 也沒有廣告。":
        "VibeDeck Player 支援 iOS 與 Android 且無廣告。VibeDeck PRO 解鎖完整音效引擎：音高與濾波器、3 段 DJ EQ 或 8 段等化器、限幅器、VibeMod、TONE、AURA 和 Smart Metadata，可在 App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",
    "沒有橫幅、沒有影片、沒有贊助彈窗。免費版和 PRO 都一樣。":
        "沒有橫幅、沒有影片、沒有贊助彈窗，沒有任何干擾打斷你的音樂。",
    "升降調（Pitch）是 VibeDeck PRO 功能。下載免費且無廣告。":
        "升降調（Pitch）是 VibeDeck PRO 功能，支援 iOS 與 Android 且無廣告，可在 App 內透過訂閱或一次性購買 Lifetime 權限解鎖。",
}

# Validate no em dashes in any generated copy
for _blob in (PREMIUM_BLOCK, GLANCE_ROW, SHARE_MSG, MP3_TITLE_H1, META_DESC_MAP, LANG_FAQ, SPECIAL_FAQ_Q_EXACT, FAQ_ANSWER_BY_Q_NORM, BODY_REPLACEMENTS):
    assert "—" not in repr(_blob), "Em dash found in replacement tables!"


def norm_space(s: str) -> str:
    return re.sub(r"[\s\u00a0\u202f]+", " ", s).strip()


def resolve_faq_update(lang: str, old_q: str, old_a: str):
    """Return (new_q, new_a) if FAQ item should be rewritten, else (old_q, old_a)."""
    qn = norm_space(old_q)
    # 1. Question needs rewriting (e.g. "Is it free?", "Сколько это стоит?")
    key = (lang, qn)
    if key in SPECIAL_FAQ_Q_EXACT:
        q_val, a_val = SPECIAL_FAQ_Q_EXACT[key]
        new_q = LANG_FAQ[lang][q_val] if q_val in LANG_FAQ[lang] else q_val
        new_a = LANG_FAQ[lang][a_val] if a_val in LANG_FAQ[lang] else a_val
        return new_q, new_a
    # 2. Only answer needs rewriting (ads, PRO included, update, ALAC, etc.)
    if key in FAQ_ANSWER_BY_Q_NORM:
        a_val = FAQ_ANSWER_BY_Q_NORM[key]
        new_a = LANG_FAQ[lang][a_val] if a_val in LANG_FAQ[lang] else a_val
        return old_q, new_a
    return old_q, old_a


def build_premium_section(lang: str) -> str:
    p1, p2 = PREMIUM_BLOCK[lang]
    e = html.escape
    return (
        '<section class="section" id="premium" aria-labelledby="premium-title">\n'
        '  <div class="wrap">\n'
        '    <div class="glass box" data-reveal style="max-width:760px;margin-inline:auto;text-align:center">\n'
        '      <h2 class="h2" id="premium-title">VibeDeck PRO</h2>\n'
        f'      <p class="lede" style="margin:20px auto 0">{e(p1, quote=False)}</p>\n'
        f'      <p style="margin:16px auto 0;max-width:56ch;color:var(--muted);font-size:15px;line-height:1.65">{e(p2, quote=False)}</p>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def update_share_section(s: str, lang: str) -> str:
    """Update share text in #share (both data-text and URL-encoded hrefs)."""
    m = re.search(r'<section class="section" id="share".*?</section>', s, re.S)
    if not m:
        return s
    sec = m.group(0)
    new_msg = SHARE_MSG[lang]
    # Find current page URL from data-share-copy or data-url
    u_m = re.search(r'data-share-copy="([^"?]+)', sec)
    if not u_m:
        return s
    page_url = u_m.group(1)

    # 1. Update data-text on native share button
    sec2 = re.sub(
        r'(data-text=")[^"]*(")',
        lambda x: x.group(1) + html.escape(new_msg, quote=True) + x.group(2),
        sec,
    )

    # 2. Update WhatsApp, Telegram, X, Threads, Email hrefs cleanly
    def q(v):
        return urllib.parse.quote(v, safe="")

    wa_url = f"{page_url}?utm_source=whatsapp&utm_medium=share&utm_campaign=share"
    tg_url = f"{page_url}?utm_source=telegram&utm_medium=share&utm_campaign=share"
    x_url = f"{page_url}?utm_source=x&utm_medium=share&utm_campaign=share"
    th_url = f"{page_url}?utm_source=threads&utm_medium=share&utm_campaign=share"
    mail_url = f"{page_url}?utm_source=email&utm_medium=share&utm_campaign=share"

    repl_hrefs = {
        "whatsapp": f"https://wa.me/?text={q(new_msg)}%20{q(wa_url)}",
        "telegram": f"https://t.me/share/url?url={q(tg_url)}&text={q(new_msg)}",
        "x": f"https://x.com/intent/post?text={q(new_msg)}&url={q(x_url)}",
        "threads": f"https://www.threads.com/intent/post?text={q(new_msg)}%20{q(th_url)}",
        "email": f"mailto:?subject={q('VibeDeck Player')}&body={q(new_msg + ' ' + mail_url)}",
    }

    for net, new_href in repl_hrefs.items():
        esc_href = html.escape(new_href, quote=True)
        sec2 = re.sub(
            rf'(<a class="share-pill" href=")[^"]*("[^>]*data-share="{net}")',
            lambda x, h=esc_href: x.group(1) + h + x.group(2),
            sec2,
        )

    return s[:m.start()] + sec2 + s[m.end():]


def update_title_and_meta(s: str, rel: str):
    """Update <title>, <h1> (for 14 MP3 pages), meta description/og/twitter tags."""
    new_title = None
    new_desc = None

    # 1. Title & H1 on the 14 MP3 pages
    if rel in MP3_TITLE_H1:
        t_val, h1_inner = MP3_TITLE_H1[rel]
        if t_val:
            new_title = t_val
            s = re.sub(
                r"(<title>)(.*?)(</title>)",
                lambda m: m.group(1) + html.escape(t_val, quote=False) + m.group(3),
                s,
                count=1,
                flags=re.S,
            )
            for prop in ("og:title", "twitter:title"):
                s = re.sub(
                    rf'(<meta\s+(?:property|name)="{prop}"\s+content=")[^"]*(")',
                    lambda m: m.group(1) + html.escape(t_val, quote=True) + m.group(2),
                    s,
                )
        s = re.sub(
            r'(<h1[^>]*>)(.*?)(</h1>)',
            lambda m: m.group(1) + h1_inner + m.group(3),
            s,
            count=1,
            flags=re.S,
        )

    # 2. Meta descriptions (description, og:description, twitter:description)
    def repl_meta(m):
        nonlocal new_desc
        old = html.unescape(m.group(2))
        if old in META_DESC_MAP:
            repl = META_DESC_MAP[old]
            new_desc = repl
            return m.group(1) + html.escape(repl, quote=True) + m.group(3)
        return m.group(0)

    s = re.sub(
        r'(<meta\s+(?:name="description"|property="og:description"|name="twitter:description")\s+content=")([^"]*)(")',
        repl_meta,
        s,
    )
    return s, new_title, new_desc


def update_home_sections(s: str, rel: str, lang: str) -> str:
    """Update #premium block and Glance table Price row on the 18 homepages."""
    if rel not in HOME_LANGS:
        return s

    # 1. Replace #premium section
    s = re.sub(
        r'<section class="section" id="premium"[^>]*>.*?</section>',
        lambda _: build_premium_section(lang),
        s,
        count=1,
        flags=re.S,
    )

    # 2. Replace Price/Access row in glance table
    th_label, td_html = GLANCE_ROW[lang]
    labels_pat = "|".join(re.escape(x) for x in OLD_GLANCE_LABELS)
    s = re.sub(
        rf'<tr><th scope="row">(?:{labels_pat})</th><td>.*?</td></tr>',
        lambda _: f'<tr><th scope="row">{html.escape(th_label, quote=False)}</th><td>{td_html}</td></tr>',
        s,
        count=1,
        flags=re.S,
    )

    # 3. Remove trailing "Prices may vary by region." dim note under glance table on EN home
    s = s.replace('<p class="dim">Prices may vary by region.</p>', "")
    return s


def update_body_copy(s: str) -> str:
    """Apply exact body text replacements outside <script> and <style>."""
    # Split out script blocks so we never accidentally corrupt JSON-LD formatting with plain text replace
    parts = re.split(r"(<script\b.*?</script>)", s, flags=re.S)
    ordered = sorted(BODY_REPLACEMENTS.items(), key=lambda kv: -len(kv[0]))
    for i in range(0, len(parts), 2):
        chunk = parts[i]
        for old, new in ordered:
            if old in chunk:
                chunk = chunk.replace(old, new)
        parts[i] = chunk
    return "".join(parts)


def update_visible_faq(s: str, lang: str):
    """Update visible FAQ <details> and return updated HTML."""
    def repl_det(m):
        pre_q, q_html, mid, a_html, post_a = m.groups()
        old_q = html.unescape(re.sub(r"<[^>]+>", "", q_html))
        old_a = html.unescape(re.sub(r"<[^>]+>", "", a_html))
        new_q, new_a = resolve_faq_update(lang, old_q, old_a)
        if new_q == old_q and new_a == old_a:
            return m.group(0)
        return (
            pre_q
            + html.escape(new_q, quote=False)
            + mid
            + html.escape(new_a, quote=False)
            + post_a
        )

    return re.sub(
        r'(<details><summary><h3[^>]*>)(.*?)(</h3></summary><div class="a"><p>)(.*?)(</p></div></details>)',
        repl_det,
        s,
        flags=re.S,
    )


def update_jsonld(s: str, lang: str, new_title, new_desc, page_changed_before_ld: bool) -> str:
    """Update all JSON-LD blocks cleanly and validate with json.loads()."""
    # Read final visible title/desc/FAQ from HTML so JSON-LD is 100% synced
    t_m = re.search(r"<title>(.*?)</title>", s, re.S)
    cur_title = html.unescape(t_m.group(1)).strip() if t_m else None
    d_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s)
    cur_desc = html.unescape(d_m.group(1)).strip() if d_m else None

    def repl_script(m):
        raw_json = m.group(2)
        data = json.loads(raw_json)
        changed = False
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        for node in nodes:
            if not isinstance(node, dict):
                continue
            tp = node.get("@type")

            # 1. MobileApplication / SoftwareApplication -> Variant A clean freemium minimum
            if tp in ("MobileApplication", "SoftwareApplication"):
                clean_offer = {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
                if node.get("offers") != clean_offer:
                    node["offers"] = clean_offer
                    changed = True

            # 2. WebPage / Article -> sync name & description
            if tp == "WebPage":
                if cur_title and node.get("name") != cur_title and new_title:
                    node["name"] = cur_title
                    changed = True
                if cur_desc and node.get("description") != cur_desc and (new_desc or node.get("description") in META_DESC_MAP):
                    node["description"] = cur_desc
                    changed = True
            if tp == "Article":
                if cur_desc and node.get("description") != cur_desc and (new_desc or node.get("description") in META_DESC_MAP):
                    node["description"] = cur_desc
                    changed = True

            # 3. FAQPage -> apply exact same resolver as visible FAQ
            if tp == "FAQPage":
                for q_obj in node.get("mainEntity", []):
                    old_q = q_obj.get("name", "")
                    ans = q_obj.get("acceptedAnswer", {})
                    old_a = ans.get("text", "")
                    nq, na = resolve_faq_update(lang, old_q, old_a)
                    if nq != old_q or na != old_a:
                        q_obj["name"] = nq
                        ans["text"] = na
                        changed = True

        # 4. Update dateModified if page changed at all
        if changed or page_changed_before_ld:
            for node in nodes:
                if isinstance(node, dict) and "dateModified" in node:
                    if node["dateModified"] != TODAY:
                        node["dateModified"] = TODAY
                        changed = True

        if not changed:
            return m.group(0)

        dumped = "\n" + json.dumps(data, ensure_ascii=False, indent=1) + "\n"
        json.loads(dumped)  # verify round-trip validity
        return m.group(1) + dumped + m.group(3)

    return re.sub(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        repl_script,
        s,
        flags=re.S,
    )


def update_sitemap(changed_rels, dry_run: bool) -> int:
    sm_path = ROOT / "sitemap.xml"
    sm = sm_path.read_text(encoding="utf-8")
    changed_urls = set()
    for rel in changed_rels:
        if rel == "index.html":
            changed_urls.add(SITE + "/")
        elif rel.endswith("/index.html"):
            changed_urls.add(SITE + "/" + rel[:-len("index.html")])
        else:
            changed_urls.add(SITE + "/" + rel)

    count = 0

    def repl_url(m):
        nonlocal count
        url, mid, old_date = m.group(1), m.group(2), m.group(3)
        if url in changed_urls and old_date != TODAY:
            count += 1
            return f"<loc>{url}{mid}{TODAY}"
        return m.group(0)

    sm2 = re.sub(
        r"<loc>([^<]+)(</loc>(?:(?!</url>).)*?<lastmod>)([^<]+)",
        repl_url,
        sm,
        flags=re.S,
    )
    if sm2 != sm and not dry_run:
        sm_path.write_text(sm2, encoding="utf-8")
    return count


def main():
    dry_run = "--dry-run" in sys.argv
    all_html = sorted(
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*.html")
        if not p.relative_to(ROOT).as_posix().startswith("_build/")
    )
    content_files = [r for r in all_html if r not in SKIP_FILES]
    changed_files = []

    for rel in content_files:
        p = ROOT / rel
        orig = p.read_text(encoding="utf-8")
        m_lang = re.search(r'<html[^>]*\blang="([^"]+)"', orig)
        lang = m_lang.group(1).lower() if m_lang else "en"

        s = orig
        s, new_title, new_desc = update_title_and_meta(s, rel)
        s = update_home_sections(s, rel, lang)
        s = update_share_section(s, lang)
        s = update_body_copy(s)
        s = update_visible_faq(s, lang)
        changed_before_ld = (s != orig)
        s = update_jsonld(s, lang, new_title, new_desc, changed_before_ld)

        if s != orig:
            changed_files.append(rel)
            if not dry_run:
                p.write_text(s, encoding="utf-8")

    sm_count = update_sitemap(changed_files, dry_run)
    mode = "DRY RUN" if dry_run else "UPDATED"
    print(f"[{mode}] content={len(content_files)} changed={len(changed_files)} skipped={len(all_html) - len(content_files)} sitemap_lastmod_updated={sm_count}")


if __name__ == "__main__":
    main()
