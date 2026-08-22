# Prospect Lab — Yol Haritası
 
Bu belge, Prospect Lab'in uzun vadeli geliştirme planını ve her sürümün hedeflerini detaylandırır.
 
## Vizyon 

> Her son tüketicinin, küresel petrol fiyatına bağlı olduğunu bilmediği ürünleri **kendi diliyle, kendi listesi üzerinden** takip edebildiği, **gerçek bir aksiyon vereni** olduğu bir araç.

## Sürüm Planı   

### v0.1 — MVP (Mayıs 2026, BTK Hackathon)

**Hedef:** Konsept ispatı; çekirdek motorları çalışır halde sunmak.

- [x] Brent canlı veri çekimi (Yahoo Finance)
- [x] Tahmin formülü (trend + sentiment + mean-reversion)
- [x] Statik korelasyon tablosu (17 sektör)
- [x] Streamlit dashboard
- [x] Landing sayfası (`index.html`)
- [x] MIT lisans, MIT okuma materyali

---

### v0.2 — Sentiment Genişletme (Q3 2026)

**Hedef:** Haber sentiment motorunu canlı veriye taşımak.

- [ ] NewsAPI entegrasyonu (`/v2/everything?q=oil`)
- [ ] GDELT 2.0 RSS feed bağlantısı
- [ ] Türkçe BERT sentiment modeli
- [ ] Multi-language (TR + EN) başlık tarama
- [ ] Sentiment trend grafiği (24h / 7g / 30g)
- [ ] Streamlit Community Cloud üzerinde yayın

**Başarı kriteri:** Sentiment skorlarının manuel etiketle korelasyonu ≥ 0.75.

---

### v0.3 — Derin Tahmin (Q4 2026)

**Hedef:** Tahmin modelini state-of-art seviyeye çıkarmak.

- [ ] Facebook Prophet entegrasyonu (baseline)
- [ ] PyTorch LSTM + attention katmanı
- [ ] Multivariate features:
  - Brent fiyat zaman serisi
  - Haber sentiment endeksi
  - USD/DXY endeksi
  - S&P 500 / VIX
  - OPEC fundamentals
- [ ] Backtest framework (geçmiş veri üzerinde model performansı)
- [ ] Ensemble blending (Prophet × LSTM × XGBoost)

**Başarı kriteri:** 7-gün MAPE < 4% (Brent tahmininde).

---

### v0.4 — Dinamik Korelasyon (Q1 2027)

**Hedef:** Statik korelasyon tablosundan dinamik öğrenmeye geçiş.

- [ ] TÜİK API entegrasyonu (TÜFE alt kalemleri)
- [ ] TCMB API entegrasyonu (Enerji EYP)
- [ ] Gerçek ürün fiyat verisi toplama pipeline'ı
- [ ] Canlı korelasyon hesaplama (rolling window regression)
- [ ] Korelasyon değişim alarmı (örn: "Plastik-petrol korelasyonu son 30 günde 0.65'ten 0.78'e yükseldi")

**Başarı kriteri:** En az 30 ürün/sektör için dinamik katsayı.

---

### v0.5 — Bildirim Katmanı (Q2 2027)

**Hedef:** Dashboard dışında, kullanıcının olduğu yere uyarı götürmek.

- [ ] E-posta uyarı sistemi (SMTP + SendGrid)
- [ ] Web push notification
- [ ] Telegram bot entegrasyonu
- [ ] Kullanıcı bazlı uyarı eşiği özelleştirme
- [ ] Uyarı sıklığı ayarı (anlık / günlük özet / haftalık)

**Başarı kriteri:** Uyarı tetiklenme → kullanıcıya iletim < 30 saniye.

---

### v1.0 — Üretim (Q3 2027)

**Hedef:** Halka açık, ölçeklenebilir SaaS ürünü.

- [ ] Kullanıcı hesabı sistemi (JWT auth)
- [ ] PostgreSQL veritabanı
- [ ] Redis cache layer
- [ ] FastAPI backend (Streamlit'ten taşınma)
- [ ] React + TypeScript + Tailwind frontend
- [ ] Docker + Kubernetes (GKE / EKS)
- [ ] CI/CD (GitHub Actions)
- [ ] Monitoring (Grafana + Prometheus)
- [ ] Premium tier (gelişmiş tahminler + API erişimi)
- [ ] [prospectapp.finance](https://prospectapp.finance) tam yayın

**Başarı kriteri:** 10.000 eş zamanlı kullanıcı, %99.5 uptime.

---

### v1.1+ — Genişleme (2027 sonrası)

**Hedef:** Petrol ötesine genişleme.

- [ ] Doğalgaz (TTF / Henry Hub)
- [ ] Tarım emtiaları (buğday, mısır, soya)
- [ ] Metaller (altın, gümüş, bakır, alüminyum)
- [ ] Döviz (USD, EUR, GBP)
- [ ] Kripto varlık entegrasyonu (BTC / ETH korelasyonu)
- [ ] B2B API (toptan satıcılar, tedarik zinciri yöneticileri için)
- [ ] Mobil uygulama (iOS + Android)

---

## Açık Sorular ve Araştırma Konuları

Aşağıdaki konular ürün geliştirme sürecinde araştırılacak ve karara bağlanacaktır:

1. **Korelasyon mu, ko-entegrasyon mu?** Statik korelasyon yerine zaman serisi ko-entegrasyon testleriyle daha derin ilişkiler ortaya çıkarılabilir mi?
2. **Causal inference:** Sadece korelasyon değil, nedensellik ilişkilerini Granger nedensellik testleriyle yakalamak.
3. **Uyarı yorgunluğu:** Kullanıcı çok fazla uyarı alırsa görmezden gelmeye başlar. Hangi sıklık optimum?
4. **Bölgesel farklılıklar:** Türkiye için optimize edilmiş model, başka ülkelerde aynı performansı verir mi?
5. **Düzenleyici çerçeve:** Finansal araç olarak kabul edilmemek için ne tür disclaimer ve sınırlamalar gerekli?

---

## Topluluk Katkıları

Açık kaynak olduğu için topluluktan beklenen katkılar:

- Yeni ürün/sektör korelasyon önerileri (issue olarak açılması)
- Haber kaynağı önerileri (özellikle yerel Türkçe kaynaklar)
- Tahmin modeli iyileştirmeleri (PR olarak gönderilmesi)
- Çeviri (İngilizce ve diğer dillerde UI desteği)
- Dokümantasyon ve örnek kullanım senaryoları
