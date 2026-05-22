# Prospect Lab — Mimari Detayları

Bu belge, Prospect Lab'in v0.1 MVP mimarisinin teknik detaylarını ve roadmap üzerindeki gelişim planını açıklar.

## 1. Sistem Genel Bakış

Prospect Lab modüler bir Python uygulamasıdır. Her motor (predictor, news_analyzer, product_engine) bağımsız olarak çalışır, test edilir ve geliştirilir. UI katmanı Streamlit ile sağlanır; landing sayfası statik HTML olarak [prospectapp.finance](https://prospectapp.finance) adresinde yayınlanır.

## 2. Veri Akışı

```
[Yahoo Finance API]
        │
        ▼
[ Brent zaman serisi (90 gün) ]
        │
        ├─→ Spot fiyat
        ├─→ Haftalık % değişim
        │
        ▼
[ predictor.predict_oil_price() ]
   ▲
   │  feature
   │
[ news_analyzer.analyze_news_sentiment() ]
   │
   ▼
[ 7-gün tahmin ]
        │
        ▼
[ product_engine.generate_alert() ]
        │     (her takip edilen ürün için)
        ▼
[ Streamlit UI / index.html mock-up ]
```

## 3. Modül Detayları

### 3.1 predictor.py

**Sorumluluk:** 7 günlük Brent yön tahmini.

**Formül:**

```
trend_effect      = weekly_change_pct × 0.40
sentiment_effect  = news_sentiment    × 3.00
mean_reversion    = -weekly_change_pct × 0.15
predicted = current × (1 + (trend + sentiment + mean_rev) / 100)
```

**Tasarım kararları:**

- Trend katsayısı 0.40 olarak alındı: momentum'u tamamen sürdürmemek, yumuşatmak.
- Sentiment amplitüdü 3.0%: literatürde haber etkisinin günlük volatiliteye katkısı ~1-3% civarında.
- Mean-reversion 0.15: aşırı hareketlerin ortalamaya dönme eğilimini hafifçe modellemek.

**Roadmap:**
- v0.2: Prophet entegrasyonu (multivariate ile)
- v0.3: PyTorch LSTM + attention katmanı
- v0.4: Ensemble (Prophet × LSTM × XGBoost)

### 3.2 news_analyzer.py

**Sorumluluk:** Haber başlıklarını tarayıp sentiment skoru üretmek.

**Mevcut MVP yaklaşımı:**
- 13 başlıktan oluşan statik havuz (literatür ve OPEC raporlarından kalibre)
- Her başlığa manuel sentiment etiketi (-1.0 ile +1.0)
- Çağrıldığında rastgele 5 başlık seçilip ortalama skor hesaplanır
- Yedek: anahtar kelime tabanlı çözücü (havuzda olmayan başlıklar için)

**Roadmap:**
- v0.2: NewsAPI canlı entegrasyon (REST endpoint: `/v2/everything?q=oil`)
- v0.2: GDELT 2.0 RSS feed bağlantısı
- v0.2: Türkçe BERT (`dbmdz/bert-base-turkish-cased`) ile sentiment classification
- v0.3: Çoklu dil (TR + EN) başlık tarama
- v0.3: Sentiment trend grafiği

### 3.3 product_engine.py

**Sorumluluk:** Ürün-petrol korelasyonu + aksiyon uyarısı.

**Korelasyon haritası (17 sektör):**

Statik bir sözlük (`PRODUCT_CORRELATIONS`). Anahtar: ürün adı (küçük harf), değer: -1.0 ile +1.0 arası katsayı. Eşleşme bulunmazsa varsayılan 0.30 döner.

**Uyarı eşikleri:**

| Beklenen hareket | Kategori |
|---|---|
| > +2.0% | YÜKSEK ALARM (kırmızı) |
| +0.5% ile +2.0% | HAFİF YÜKSELİŞ (sarı) |
| ±0.5% | NÖTR (beyaz) |
| -0.5% ile -2.0% | HAFİF DÜŞÜŞ (yeşil) |
| < -2.0% | FIRSAT (yeşil) |

**Roadmap:**
- v0.4: TÜİK + TCMB ürün fiyat verileriyle dinamik regresyon
- v0.4: Kullanıcı bazlı eşik özelleştirme

## 4. UI Katmanı

### 4.1 Streamlit Dashboard (`app.py`)

- Sol panel: Takip listesi yönetimi
- Üst panel: Brent grafiği + 7-gün tahmin metrikleri
- Orta: Haber sentiment paneli + taranan başlıklar
- Alt: Her ürün için uyarı kartı

**Tasarım kararları:**
- Streamlit seçimi: hızlı MVP için Python tabanlı en pratik framework
- Native bileşenler (`st.metric`, `st.line_chart`, `st.container`)
- v1.0'da React + FastAPI migrasyonu planlı

### 4.2 Landing Sayfası (`index.html`)

- Tek dosya statik HTML
- Custom CSS (CSS değişkenleri, grid, animasyonlar)
- Fraunces (serif) + JetBrains Mono (mono) typography
- Koyu tema + asit yeşili accent
- Canlı spot fiyat simülasyonu (vanilla JS)
- [prospectapp.finance](https://prospectapp.finance) adresinde yayınlanacak

## 5. Test Stratejisi

**Mevcut:** Her modül dosyasının altında `if __name__ == "__main__"` bloğunda manuel test.

**Roadmap:**
- pytest framework entegrasyonu (v0.2)
- Unit testler (her motor için)
- Integration testler (end-to-end uyarı pipeline)
- Backtest framework (predictor için, v0.3)

## 6. Deployment

**Mevcut:** Lokal Streamlit (`streamlit run app.py`).

**Roadmap:**
- v0.2: Streamlit Community Cloud (ücretsiz hosting)
- v0.5: Docker + AWS/GCP
- v1.0: Kubernetes cluster + CI/CD (GitHub Actions)

## 7. Performans & Ölçeklenebilirlik Hedefleri

| Metrik | MVP | v1.0 hedef |
|---|---|---|
| Eş zamanlı kullanıcı | 1 (lokal) | 10.000 |
| Uyarı üretim gecikmesi | < 2 sn | < 200 ms |
| Tahmin güncelleme sıklığı | Talep üzerine | Saatlik |
| Veri tazeliği | Anlık | Anlık + cache |

## 8. Güvenlik ve Gizlilik (Roadmap)

- v1.0: JWT tabanlı auth
- v1.0: TLS, rate limiting, CORS politikaları
- v1.0: KVKK uyumlu kullanıcı verisi yönetimi
- v1.0: API key yönetimi (kullanıcı kendi NewsAPI anahtarını ekleyebilir)
