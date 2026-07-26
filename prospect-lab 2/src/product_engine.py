 """
Prospect Lab — Ürün-Petrol Korelasyon Motoru

Kullanıcının takip listesindeki her ürün için:
  1. Petrolle bağlantı katsayısını belirler
  2. Tahmin edilen petrol hareketini ürüne yansıtır
  3. Aksiyon-odaklı uyarı metni üretir

MVP yaklaşımı:
  - 17 sektör için statik korelasyon haritası (literatür + sezgisel)
  - Eşik tabanlı uyarı kategorileri

Roadmap: 
  - TÜİK + TCMB verisi ile dinamik regresyon (v0.4)
  - Kullanıcı bazlı eşik özelleştirme (v0.5)
"""

# ─────────────────────────────────────────────────────────────
# KORELASYON HARİTASI
# ─────────────────────────────────────────────────────────────
PRODUCT_CORRELATIONS = {
    # Doğrudan akaryakıt (yüksek pozitif korelasyon)
    "benzin": 0.92,
    "mazot": 0.91,
    "motorin": 0.91,
    "lpg": 0.78,
    "akaryakıt": 0.90,

    # Petrokimya
    "plastik": 0.65,
    "petrokimya": 0.74,
    "polimer": 0.68,
    "polyester": 0.62,

    # Lojistik & ulaşım
    "lojistik": 0.62,
    "kargo": 0.58,
    "denizyolu": 0.51,
    "kara taşımacılığı": 0.66,
    "nakliye": 0.64,

    # Havayolu (negatif — talep esnek)
    "havayolu": -0.55,
    "uçak bileti": -0.50,

    # Tarım girdileri
    "gübre": 0.48,
    "boya": 0.42,
    "ambalaj": 0.45,

    # Yeşil enerji (negatif korelasyon)
    "elektrikli araç": -0.48,
    "güneş paneli": -0.32,
    "rüzgar enerjisi": -0.28,
    "batarya": -0.30,
}

DEFAULT_CORRELATION = 0.30


# ─────────────────────────────────────────────────────────────
# UYARI EŞİKLERİ
# ─────────────────────────────────────────────────────────────
THRESHOLDS = {
    "high_alert": 2.0,      # > +2.0%
    "mild_up": 0.5,         # +0.5% ile +2.0%
    "neutral": 0.5,         # -0.5% ile +0.5%
    "mild_down": -2.0,      # -0.5% ile -2.0%
    # < -2.0% → opportunity
}


def get_correlation(product: str) -> float:
    """
    Verilen ürün için petrol-korelasyon katsayısını döner.
    Eşleşme bulunmazsa varsayılan değer (0.30) döner.

    Parametre:
        product: Ürün/sektör adı (büyük-küçük harf duyarsız)

    Döner:
        -1.0 ile +1.0 arasında korelasyon katsayısı
    """
    p = product.lower().strip()
    for key, corr in PRODUCT_CORRELATIONS.items():
        if key in p or p in key:
            return corr
    return DEFAULT_CORRELATION


def generate_alert(
    product: str,
    correlation: float,
    predicted_oil: float,
    current_oil: float
) -> str:
    """
    Verilen ürün için aksiyon-odaklı uyarı metni üretir.

    Parametreler:
        product: Ürün adı
        correlation: Ürünün petrolle korelasyonu
        predicted_oil: Tahmin edilen petrol fiyatı
        current_oil: Mevcut petrol fiyatı

    Döner:
        Markdown formatında uyarı metni
    """
    oil_change = ((predicted_oil - current_oil) / current_oil) * 100
    expected = oil_change * correlation

    if abs(expected) < THRESHOLDS["neutral"]:
        return (
            f"⚪ **{product}** — Beklenen hareket: `{expected:+.2f}%`. "
            f"Önemli bir hareket beklenmiyor. Mevcut alımlarınızı sürdürebilirsiniz."
        )

    if expected > THRESHOLDS["high_alert"]:
        return (
            f"🔴 **YÜKSEK ALARM — {product}**\n\n"
            f"Petrolün **{oil_change:+.2f}%** beklentisiyle bu ürün/sektör "
            f"yaklaşık **{expected:+.2f}%** yükselebilir.\n\n"
            f"👉 **Aksiyon:** Bu hafta içinde stoklamayı veya erken alımı değerlendirin."
        )
    elif expected > THRESHOLDS["mild_up"]:
        return (
            f"🟡 **{product}** — Hafif yükseliş beklentisi: `{expected:+.2f}%`.\n\n"
            f"👉 **Aksiyon:** Yakın takipte kalın. Gerekirse planlı alımları öne çekin."
        )
    elif expected < THRESHOLDS["mild_down"]:
        return (
            f"🟢 **FIRSAT — {product}**\n\n"
            f"Petrolün **{oil_change:+.2f}%** beklentisiyle bu ürün/sektör "
            f"yaklaşık **{expected:+.2f}%** ucuzlayabilir.\n\n"
            f"👉 **Aksiyon:** Alımı erteleyip beklemek mantıklı olabilir."
        )
    else:
        return (
            f"🟢 **{product}** — Hafif düşüş beklentisi: `{expected:+.2f}%`.\n\n"
            f"👉 **Aksiyon:** Acil alım gerekmiyor; takipte kalın."
        )


def get_all_correlations() -> dict:
    """Tüm korelasyon haritasını döner — dashboard'da liste için."""
    return PRODUCT_CORRELATIONS.copy()


if __name__ == "__main__":
    # Modül testi
    test_products = ["benzin", "havayolu", "plastik", "elektrikli araç", "gübre"]
    for p in test_products:
        c = get_correlation(p)
        a = generate_alert(p, c, predicted_oil=84.18, current_oil=82.41)
        print(f"\n[{p}] korelasyon={c:+.2f}")
        print(a)
