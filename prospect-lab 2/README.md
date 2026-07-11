<div align="center">

# ◣ PROSPECT LAB 

**Petrol bazlı ürün zekâsı: takip, tahmin ve aksiyon-odaklı uyarı motoru**

*BTK Hackathon 2026 — Resmi başvuru deposu*

[![Status](https://img.shields.io/badge/status-MVP-c8ff3e?style=flat-square)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)]()
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b?style=flat-square)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)]() 
[![Hackathon](https://img.shields.io/badge/BTK-Hackathon%202026-orange?style=flat-square)]()

🌐 **Web:** [prospectapp.finance](https://prospectapp.finance)  ·  📊 **Demo:** Streamlit Dashboard  ·  📺 **Video:** Project Walkthrough

</div> 

---

## ❖ İçindekiler

1. [Tek Cümlede](#-tek-cümlede)
2. [Problem](#-problem)
3. [Çözüm: Prospect Lab](#-çözüm-prospect-lab)
4. [Mimari Genel Bakış](#-mimari-genel-bakış)
5. [Modüller](#-modüller)
6. [Veri Kaynakları](#-veri-kaynakları)
7. [Tahmin Yaklaşımı](#-tahmin-yaklaşımı)
8. [Uyarı Mantığı](#-uyarı-mantığı)
9. [Hedef Kitle ve Kullanım Senaryoları](#-hedef-kitle-ve-kullanım-senaryoları)
10. [Kurulum](#-kurulum)
11. [Hızlı Başlangıç](#-hızlı-başlangıç)
12. [Proje Yapısı](#-proje-yapısı)
13. [Yol Haritası](#-yol-haritası)
14. [Teknoloji Yığını](#-teknoloji-yığını)
15. [Sınırlamalar ve Dürüst Notlar](#-sınırlamalar-ve-dürüst-notlar)
16. [SSS](#-sss)
17. [Lisans ve İletişim](#-lisans-ve-iletişim)

---

## ❖ Tek Cümlede

> **Prospect Lab**, Brent petrol fiyatını canlı izler, global haber akışını sentiment skoruna çevirir, sektörel korelasyonları çözer ve son tüketici için **"al / bekle / stokla"** şeklinde aksiyon-odaklı uyarılar üretir.

Yatırımcı için değil, **hayatın içindeki tüketici ve küçük işletme için** tasarlanmıştır.

---

## ❖ Problem

Dünya ekonomisinin neredeyse tamamı, doğrudan ya da dolaylı olarak petrol fiyatına bağlıdır. Plastikten ambalaja, lojistikten havacılığa, gübreden boyaya — fiyat zincirinin başında çoğunlukla Brent durur. Buna rağmen son tüketicinin ve küçük işletmenin elinde, bu bağı **kendi takip listesi üzerinden**, **kendi diliyle**, **aksiyona dönük şekilde** anlamasını sağlayan bir araç yoktur.

**Mevcut araçların eksiği:**

| Mevcut araç tipi | Kim için? | Eksik |
|---|---|---|
| Bloomberg / TradingView / Investing | Profesyonel yatırımcı | Karmaşık, ücretli, son tüketiciye yabancı dilde |
| Haber siteleri | Genel okuyucu | Aksiyon vermez, sadece anlatır |
| Devlet enerji raporları | Akademik / sektör | Geç yayınlanır, geriye dönüktür |
| Sosyal medya | Herkes | Gürültülü, doğrulanamaz |

**Prospect Lab'in cevabı:** Bu boşluğu *kullanıcının kendi ürün listesi* üzerinden, *bir AI motoru* aracılığıyla doldurmak.

### Türkiye özelinde önemi

- İmalat sanayisinin **maliyet zincirinin yaklaşık %68'i** doğrudan/dolaylı enerji-petrol bağlıdır.
- Brent'teki yön değişikliği, raftaki tüketici fiyatına **3-5 hafta** içinde yansır.
- Bu pencere, **bilinçli tüketici davranışı için sömürülebilir bir zaman aralığıdır**.

---

## ❖ Çözüm: Prospect Lab

Prospect Lab üç bilgi kaynağını tek bir motorda birleştirir:

```
┌─────────────────────────┐
│  1. Brent fiyat verisi  │ ── canlı, intraday + 90-gün histori
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│  2. Haber sentiment     │ ── OPEC, jeopolitik, stok, talep haberleri
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│  3. Ürün korelasyonu    │ ── 17 sektör için bağlantı katsayıları
└──────────┬──────────────┘
           │
           ▼
   ╔═══════════════════╗
   ║   AKSİYON UYARISI ║ ── kullanıcının takip listesindeki ürünler için
   ╚═══════════════════╝
```

**Çıktı örneği:**

> 🔴 **YÜKSEK ALARM — Benzin**: Petrolün +2.15% beklentisiyle bu ürün yaklaşık +1.98% yükselebilir. **Bu hafta içinde stoklamayı veya erken alımı değerlendirin.**

> 🟢 **FIRSAT — Plastik tabanlı mobilya**: Beklenen düşüş -1.42%. **Bekleyebilirsiniz.**

---

## ❖ Mimari Genel Bakış

```
                    ┌────────────────────┐
                    │   index.html       │   ← Landing + canlı mock-up
                    │   (prospectapp.finance)│
                    └────────────────────┘
                              │
                              │ kullanıcı tıklar → dashboard
                              ▼
        ┌─────────────────────────────────────────────┐
        │              app.py (Streamlit)             │
        │  ─────────────────────────────────────────  │
        │  · Watchlist yönetimi                       │
        │  · Brent grafiği (canlı)                    │
        │  · Tahmin paneli                            │
        │  · Sentiment paneli                         │
        │  · Uyarı kartları                           │
        └────────────────────┬────────────────────────┘
                             │
        ┌────────────────────┼─────────────────────────┐
        │                    │                         │
        ▼                    ▼                         ▼
┌────────────────┐  ┌────────────────┐      ┌────────────────────┐
│  predictor.py  │  │ news_analyzer  │      │  product_engine.py │
│                │  │     .py        │      │                    │
│  · trend       │  │ · headline tar │      │ · korelasyon haritası│
│  · sentiment   │  │ · skor üretimi │      │ · uyarı şablonları │
│  · mean-rev.   │  │ · feature exp. │      │ · aksiyon çevirici │
└───────┬────────┘  └───────┬────────┘      └─────────┬──────────┘
        │                   │                         │
        └───────────────────┼─────────────────────────┘
                            ▼
                   ┌────────────────────┐
                   │ Veri kaynakları    │
                   │ · Yahoo Finance    │
                   │ · (Roadmap: NewsAPI│
                   │    + GDELT + EIA)  │
                   └────────────────────┘
```

Modüler tasarım sayesinde her motor bağımsız geliştirilebilir, değiştirilebilir, test edilebilir.

---

## ❖ Modüller

### ⓘ Modül 1 — Brent İzleme & Tahmin

**Dosya:** `src/predictor.py` + `app.py` içindeki grafik bölümü

**Sorumluluğu:**
- Yahoo Finance `BZ=F` (Brent Crude Futures) üzerinden 90-gün histori çekmek
- Mevcut spot fiyatı ve haftalık değişimi hesaplamak
- 7-günlük yön tahmini üretmek

**Tahmin formülü (mevcut MVP):**

```
trend_effect      = weekly_change_pct × 0.40
sentiment_effect  = news_sentiment    × 3.00     (max ±3%)
mean_reversion    = -weekly_change_pct × 0.15
toplam_değişim    = trend + sentiment + mean_rev
tahmin            = current × (1 + toplam_değişim / 100)
```

Bu formül, **aşırı volatil günlerde momentum'u yumuşatır**, **haber sentiment'inin yön belirleyici etkisini ön plana çıkarır**, ve **istatistiksel olarak fiyatın ortalamaya dönme eğilimini** baz alır.

---

### ⓘ Modül 2 — Haber Sentiment Motoru

**Dosya:** `src/news_analyzer.py`

**Sorumluluğu:**
- Petrol piyasasını etkileyen başlıkları taramak
- Her başlığı sentiment skoruna çevirmek (-1.0 → +1.0)
- Ortalama skoru tahmin modeline `feature` olarak beslemek

**Mevcut MVP yaklaşımı:**
- Statik başlık havuzu + ağırlıklı sentiment etiketleri
- Yedek olarak anahtar-kelime tabanlı sentiment çözücü

**Pozitif sinyaller (fiyat yukarı):** OPEC kesinti, jeopolitik gerilim, stok düşüşü, talep artışı, kıtlık

**Negatif sinyaller (fiyat aşağı):** Arz fazlası, stok artışı, resesyon, yenilenebilir geçiş

**Roadmap:** NewsAPI / GDELT canlı entegrasyonu + Türkçe BERT (`dbmdz/bert-base-turkish-cased`) sentiment modeli.

---

### ⓘ Modül 3 — Ürün-Petrol Korelasyon Motoru

**Dosya:** `src/product_engine.py`

**Sorumluluğu:**
- Kullanıcının takip listesindeki her ürün için petrolle bağlantı katsayısı belirlemek
- Tahmin edilen petrol hareketini ürüne yansıtmak
- Aksiyon-odaklı uyarı metni üretmek

**Korelasyon haritası (17 sektör, kısaltılmış):**

| Kategori | Ürün/Sektör | Korelasyon |
|---|---|---|
| Doğrudan akaryakıt | Benzin / Mazot / Motorin | +0.91 ila +0.92 |
| Petrokimya | Plastik / Petrokimya | +0.65 / +0.74 |
| Lojistik | Kara / Kargo / Denizyolu | +0.51 ila +0.66 |
| Hava taşıması | Havayolu | −0.55 (talep esnek) |
| Tarım girdileri | Gübre / Boya / Ambalaj | +0.42 ila +0.48 |
| Yeşil enerji | Elektrikli araç / Güneş / Rüzgar | −0.28 ila −0.48 |

Katsayılar literatür + sezgisel kalibrasyona dayanır. **Roadmap:** Gerçek ürün fiyat zaman serileriyle dinamik regresyon ve katsayıların **canlı güncellenmesi**.

---

## ❖ Veri Kaynakları

| Kaynak | Tür | Kullanım | Durum |
|---|---|---|---|
| Yahoo Finance (`yfinance`) | Finansal zaman serisi | Brent spot + 90-gün histori | ✅ Entegre |
| Statik başlık havuzu | Manuel | Sentiment MVP'si | ✅ Entegre |
| NewsAPI | REST API | Canlı haber çekimi | ⏳ Roadmap |
| GDELT Project | Açık veri | Geniş haber + sentiment | ⏳ Roadmap |
| EIA Open Data | Devlet API | Stok / arz / talep verisi | ⏳ Roadmap |
| OPEC Monthly | PDF/scrape | Resmi tahminler | ⏳ Roadmap |
| TCMB / TÜİK | Açık veri | TR tüketici fiyat indeksi | ⏳ Roadmap |

---

## ❖ Tahmin Yaklaşımı

### Felsefe

> *"Mükemmel ama geç gelen tahmin, yanlıştan kötüdür."*

Prospect Lab'in tahmin felsefesi şunlara dayanır:

1. **Açıklanabilirlik > karmaşıklık.** Kullanıcı neden bu uyarıyı aldığını anlamalı. Bu yüzden ilk sürümde kara kutu yerine **şeffaf, ağırlıklı formül** seçildi.
2. **Yön > kesin sayı.** Brent'i ±0.10 dolar hassasiyetle tahmin etmek son tüketici için anlamsızdır. Önemli olan **yön ve büyüklük sınıfı** (büyük yukarı / hafif yukarı / nötr / hafif aşağı / büyük aşağı).
3. **Sentiment olmadan teknik analiz eksiktir.** Brent piyasasının asıl hareket ettiricisi haberlerdir; bunu modele entegre etmek tahmin kalitesini katlar.

### Roadmap modeli

- **v0.2** — Prophet (Facebook) + multivariate feature seti
- **v0.3** — LSTM (PyTorch) + attention katmanı + sentiment embedding
- **v0.4** — Ensemble: Prophet × LSTM × XGBoost ağırlıklı blending

---

## ❖ Uyarı Mantığı

Beklenen ürün fiyat hareketi (`expected_product_change`) hesaplanır:

```
expected_product_change = oil_change_pct × product_correlation
```

Sonra eşik sınırlarına göre uyarı kategorisi atanır:

| Beklenen hareket | Kategori | Aksiyon önerisi |
|---|---|---|
| > +2.0% | 🔴 YÜKSEK ALARM | Stokla / şimdi al |
| +0.5% ile +2.0% | 🟡 HAFİF YÜKSELİŞ | Takipte kal |
| −0.5% ile +0.5% | ⚪ NÖTR | Önemli hareket yok |
| −0.5% ile −2.0% | 🟢 HAFİF DÜŞÜŞ | Bekle, acele etme |
| < −2.0% | 🟢 FIRSAT | Alımı ertele |

Eşikler kullanıcı tarafından özelleştirilebilir hâle getirilecektir (roadmap).

---

## ❖ Hedef Kitle ve Kullanım Senaryoları

### Senaryo A: Küçük işletme sahibi (lojistik firması)

Mehmet Bey, bir nakliye firması işletiyor. Filosu için aylık yakıt alımı yapıyor. Prospect Lab'e "Mazot" ekliyor. Sistem şu uyarıyı gönderiyor:

> 🔴 **YÜKSEK ALARM — Mazot**: Petrolün +3.2% beklentisiyle bu ürün ~+2.9% yükselebilir. **Bu hafta tank doldurmayı planlayın.**

Mehmet Bey, normalde **gelecek hafta** alacağı yakıtı **bu hafta** alıyor, **%2.9 maliyet farkı** kazanıyor. 50 ton mazot üzerinden ortalama ~30.000 TL.

### Senaryo B: Tüketici (mobilya / beyaz eşya)

Ayşe Hanım, ev yenilemesi planlıyor. Listeye "Plastik mobilya" ve "Beyaz eşya boyası" ekliyor. Sistem:

> 🟢 **FIRSAT — Plastik tabanlı ürünler**: Brent'te beklenen düşüş ile bu kategoride **1-2 hafta beklemek mantıklı**.

### Senaryo C: KOBİ üreticisi (tekstil)

Tekstil üreticisi Ahmet Bey, polyester (petrol türevi) ham madde alıyor. Sistem ona OPEC kararı sonrası "stoklamayı düşün" uyarısı veriyor. Üretim takvimini buna göre ayarlıyor.

---

## ❖ Kurulum

### Gereksinimler

- Python 3.10 veya üzeri
- pip
- (İsteğe bağlı) virtualenv veya conda

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/KULLANICI_ADI/prospect-lab.git
cd prospect-lab

# 2. Sanal ortam (önerilir)
python -m venv venv
source venv/bin/activate    # macOS / Linux
# venv\Scripts\activate     # Windows

# 3. Bağımlılıklar
pip install -r requirements.txt
```

---

## ❖ Hızlı Başlangıç

### 1. Landing site

`index.html` dosyasını çift tıklayın — varsayılan tarayıcınız açar. Canlı animasyonlu Brent mock-up, modül kartları, uyarı örnekleri.

Web ortamı: **[prospectapp.finance](https://prospectapp.finance)** *(yayın aşamasında)*

### 2. Streamlit dashboard

```bash
streamlit run app.py
```

Tarayıcı otomatik açılır (varsayılan: `http://localhost:8501`).

Yapabilecekleriniz:
- Sol panelden takip listenize ürün ekleyin
- Brent 90-gün grafiğini canlı görün
- 7-günlük tahmini ve haber sentiment skorunu okuyun
- Her ürün için aksiyon uyarısını alın

### 3. Modülleri ayrı ayrı test etme

```python
from src.predictor import predict_oil_price
from src.news_analyzer import analyze_news_sentiment
from src.product_engine import get_correlation, generate_alert

score, items = analyze_news_sentiment()
prediction = predict_oil_price(current=82.41, weekly_change_pct=1.2)
corr = get_correlation("benzin")
alert = generate_alert("benzin", corr, prediction, 82.41)

print(alert)
```

---

## ❖ Proje Yapısı

```
prospect-lab/
├── README.md                  ← Bu dosya
├── LICENSE                    ← MIT
├── requirements.txt           ← Python bağımlılıkları
├── app.py                     ← Streamlit dashboard giriş noktası
├── index.html                 ← Landing + mock-up sayfası
│
├── src/                       ← Çekirdek motor modülleri
│   ├── __init__.py
│   ├── predictor.py           ← Brent tahmin modülü
│   ├── news_analyzer.py       ← Haber sentiment motoru
│   └── product_engine.py      ← Ürün korelasyon + uyarı motoru
│
└── docs/                      ← Belgeler
    ├── ARCHITECTURE.md        ← Detaylı mimari
    └── ROADMAP.md             ← Uzun vadeli yol haritası
```

---

## ❖ Yol Haritası

### v0.1 — MVP (Mevcut sürüm, BTK Hackathon 2026)

- [x] Brent canlı veri (Yahoo Finance)
- [x] Trend + sentiment + mean-reversion ağırlıklı tahmin
- [x] 17 sektör için statik korelasyon tablosu
- [x] Streamlit dashboard (watchlist + uyarı paneli)
- [x] Landing site (`index.html`)
- [x] Modüler kod tabanı

### v0.2 — Sentiment Genişletme (Q3 2026)

- [ ] NewsAPI canlı entegrasyonu
- [ ] GDELT 2.0 RSS feed bağlantısı
- [ ] Türkçe BERT sentiment modeli (`dbmdz/bert-base-turkish-cased`)
- [ ] Çoklu dilde başlık tarama (TR + EN)
- [ ] Sentiment trend grafiği

### v0.3 — Derin Tahmin (Q4 2026)

- [ ] Facebook Prophet entegrasyonu
- [ ] PyTorch LSTM + attention katmanı
- [ ] Multivariate features (haber + USD endeksi + S&P500)
- [ ] Backtest framework

### v0.4 — Dinamik Korelasyon (Q1 2027)

- [ ] Türkiye İstatistik Kurumu (TÜİK) ürün fiyat verisi
- [ ] TCMB enerji endeksleri
- [ ] Gerçek ürün fiyatlarıyla canlı regresyon
- [ ] Statik tablodan dinamik öğrenmeye geçiş

### v0.5 — Bildirim Katmanı (Q2 2027)

- [ ] E-posta uyarıları (eşik aşıldığında)
- [ ] Web push notification
- [ ] Telegram bot entegrasyonu
- [ ] Kullanıcı bazlı eşik özelleştirme

### v1.0 — Üretim (Q3 2027)

- [ ] Kullanıcı hesabı + JWT
- [ ] PostgreSQL veritabanı
- [ ] FastAPI backend (Streamlit yerine)
- [ ] React + TypeScript frontend
- [ ] Docker + Kubernetes deployment
- [ ] [prospectapp.finance](https://prospectapp.finance) yayın

---

## ❖ Teknoloji Yığını

### Mevcut

| Katman | Teknoloji |
|---|---|
| Backend | Python 3.10+ |
| Veri çekimi | yfinance |
| Veri işleme | pandas, numpy |
| Dashboard | Streamlit |
| Landing | HTML + CSS + vanilla JS |

### Hedef (Roadmap)

| Katman | Teknoloji |
|---|---|
| Backend | FastAPI |
| ML / Tahmin | PyTorch (LSTM), Prophet, scikit-learn |
| NLP | HuggingFace Transformers, BERT-tr |
| Frontend | React + TypeScript + Tailwind |
| Veritabanı | PostgreSQL + Redis |
| Deployment | Docker + Kubernetes + GitHub Actions |
| Monitoring | Grafana + Prometheus |

---

## ❖ Sınırlamalar ve Dürüst Notlar

Bu sürüm **bir MVP'dir**. Aşağıdaki noktalar bilinçli olarak basitleştirilmiştir:

1. **Haber sentiment motoru** şu anda statik bir başlık havuzu üzerinden çalışmaktadır. Canlı NewsAPI ve BERT entegrasyonu roadmap'tedir.
2. **Tahmin modeli** üretim seviyesi bir LSTM/Prophet değil, açıklanabilir bir ağırlıklı kombinasyondur. Demo amaçlıdır.
3. **Korelasyon katsayıları** literatür + sezgisel kalibrasyondur. Gerçek ürün fiyatlarıyla doğrulanmamıştır.
4. **Uyarı sistemi** uygulama içidir. E-posta / push roadmap'tedir.
5. **Veri kaynağı çeşitliliği** sınırlıdır (sadece Yahoo Finance). EIA, OPEC, TÜİK, TCMB entegrasyonları planlanmaktadır.

Bu sınırlamalar **biliniyor, kabul ediliyor ve yol haritasında yeri belirleniyor**. İlk 10'a kalınması durumunda yapılacak sunumda her birinin teknik detayı ve zaman çizelgesi paylaşılacaktır.

---

## ❖ SSS

**S: Bu sadece petrol için mi çalışıyor?**
C: Şu an evet, çünkü petrol global maliyet zincirinin en geniş ayağı. Roadmap'te doğalgaz, altın, bakır, buğday gibi başka emtialar eklenecek.

**S: Yatırım tavsiyesi mi veriyor?**
C: Hayır. Prospect Lab **bilgilendirme** ve **tüketici / işletme aksiyon önerisi** verir. Finansal araçlara yatırım kararı için profesyonel danışmanlık almalısınız.

**S: Korelasyon katsayıları nereden geliyor?**
C: İlk sürümde literatür + sektör raporlarına dayalı sezgisel kalibrasyon. v0.4'te gerçek fiyat verisi üzerinden öğrenilen değerlere geçilecek.

**S: Türkçe haber kaynakları desteklenecek mi?**
C: Evet. v0.2 sürümünde Hürriyet, Habertürk, Anadolu Ajansı gibi yerli kaynaklar + Türkçe BERT sentiment dahil edilecek.

**S: Açık kaynak mı?**
C: Evet, MIT lisanslı. Topluluk katkıları memnuniyetle karşılanır.

**S: prospectapp.finance ne zaman aktif olacak?**
C: Hackathon değerlendirme sürecinden sonra, v0.2 ile birlikte.

---

## ❖ Lisans ve İletişim

**Lisans:** MIT (bkz. `LICENSE` dosyası)

**Web:** [prospectapp.finance](https://prospectapp.finance)

**Geliştirme deposu:** Bu GitHub reposu

**Sorumluluk Reddi:** Prospect Lab tarafından üretilen uyarılar **bilgilendirme amaçlıdır**. Yatırım tavsiyesi değildir. Verilen kararlardan kullanıcı sorumludur.

---

<div align="center">

**◣ PROSPECT LAB**

*Her şey petrole bağlı. Artık tahmin değil, uyarı.*

BTK Hackathon 2026 · Made for BTK Akademi × Google × GİRVAK

</div>
