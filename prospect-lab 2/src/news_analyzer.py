"""
Prospect Lab — Haber Sentiment Motoru

Petrol piyasasını etkileyen haber başlıklarını tarar ve her birini sentiment
skoruna (-1.0 ile +1.0 arasında) çevirir. Skor, predictor.py modülü tarafından
tahmin formülüne feature olarak beslenir.

MVP yaklaşımı:
- Statik başlık havuzu + ağırlıklı sentiment etiketleri
- Yedek olarak anahtar-kelime tabanlı sentiment

Roadmap:
- NewsAPI canlı entegrasyonu
- GDELT 2.0 RSS feed bağlantısı
- Türkçe BERT (dbmdz/bert-base-turkish-cased) sentiment modeli
"""
import random
from typing import List, Tuple


# Sentiment etiketli temsili başlık havuzu
# Gerçek implementasyonda NewsAPI veya GDELT'ten canlı çekilecek
SAMPLE_HEADLINES: List[Tuple[str, float]] = [
    # Pozitif (fiyat yukarı)
    ("OPEC+ üretim kesintisini sürdürme kararı aldı", 0.6),
    ("Orta Doğu'da gerilim petrol piyasalarını etkiledi", 0.7),
    ("Çin'in talep tahminleri yukarı revize edildi", 0.4),
    ("Suudi Arabistan, gönüllü üretim kesintisini uzattı", 0.55),
    ("Kasırga sezonu Meksika Körfezi rafinerilerini tehdit ediyor", 0.5),
    ("ABD stratejik petrol rezervleri tarihsel düşük seviyede", 0.45),

    # Negatif (fiyat aşağı)
    ("ABD ham petrol stokları beklenenden fazla arttı", -0.5),
    ("Doların güçlenmesi emtia fiyatlarını baskıladı", -0.3),
    ("Yeni keşfedilen rezervler arzı artıracak", -0.4),
    ("Küresel resesyon endişeleri talebi düşürebilir", -0.6),
    ("Yenilenebilir enerjiye geçiş hızlandı", -0.2),
    ("Çin imalat PMI'sı düşük geldi, talep zayıf", -0.5),
    ("IEA, küresel petrol talebinin yavaşladığını açıkladı", -0.45),
]

POSITIVE_KEYWORDS = [
    "kesinti", "gerilim", "talep artışı", "stok düşüşü", "kıtlık",
    "ambargo", "yaptırım", "kasırga", "savaş", "askeri operasyon"
]
NEGATIVE_KEYWORDS = [
    "arz fazlası", "stok artışı", "resesyon", "yenilenebilir",
    "düşüş", "anlaşma", "ateşkes", "yavaşlama", "zayıflama"
]


def analyze_news_sentiment(n: int = 5) -> Tuple[float, List[str]]:
    """
    Son n başlığı tarar ve ortalama sentiment skoru üretir.

    Parametreler:
        n: Taranacak başlık sayısı (varsayılan 5)

    Döner:
        (ortalama_skor, başlık_listesi)
        - ortalama_skor: -1.0 ile +1.0 arasında float
        - başlık_listesi: skorlarıyla birlikte başlık metinleri
    """
    selected = random.sample(SAMPLE_HEADLINES, min(n, len(SAMPLE_HEADLINES)))
    scores = [s for _, s in selected]
    avg = sum(scores) / len(scores) if scores else 0.0
    items = [f"{h}  (skor: {s:+.2f})" for h, s in selected]
    return avg, items


def keyword_based_sentiment(text: str) -> float:
    """
    Anahtar kelime tabanlı yedek sentiment çözücü.
    Yeni başlıklar için kullanılır (havuzda olmayan).

    Parametre:
        text: Analiz edilecek başlık metni

    Döner:
        -1.0 ile +1.0 arasında sentiment skoru
    """
    text_lower = text.lower()
    score = 0.0
    for kw in POSITIVE_KEYWORDS:
        if kw in text_lower:
            score += 0.3
    for kw in NEGATIVE_KEYWORDS:
        if kw in text_lower:
            score -= 0.3
    return max(-1.0, min(1.0, score))


if __name__ == "__main__":
    # Modül testi
    score, items = analyze_news_sentiment()
    print(f"Ortalama sentiment: {score:+.2f}")
    print("Başlıklar:")
    for item in items:
        print(f"  • {item}")
