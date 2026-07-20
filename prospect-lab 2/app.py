"""
Prospect Lab — Streamlit Dashboard
Petrol Bazlı Ürün Takip, Tahmin ve Uyarı Sistemi
BTK Hackathon 2026 — MVP
 
Çalıştırma: streamlit run app.py
Web: https://prospectapp.finance
"""
import streamlit as st  
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf

from src.news_analyzer import analyze_news_sentiment
from src.predictor import predict_oil_price
from src.product_engine import get_correlation, generate_alert


# ─────────────────────────────────────────────────────────────
# SAYFA YAPILANDIRMASI
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prospect Lab — Petrol Bazlı Ürün Zekâsı",
    page_icon="◣",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "watchlist" not in st.session_state:
    st.session_state.watchlist = ["Benzin", "Lojistik"]

# ─────────────────────────────────────────────────────────────
# BAŞLIK
# ─────────────────────────────────────────────────────────────
st.title("◣ Prospect Lab")
st.caption(
    "Petrol bazlı ürün takip, haber-temelli tahmin ve akıllı uyarı motoru. "
    "BTK Hackathon 2026 MVP · prospectapp.finance"
)

# ─────────────────────────────────────────────────────────────
# YAN PANEL — TAKİP LİSTESİ
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Takip Listem")
    st.caption("Petrol fiyatına bağlı olarak izlemek istediğiniz ürün/sektörleri ekleyin.")

    new_product = st.text_input(
        "Yeni ürün ekle",
        placeholder="örn: Benzin, Plastik, Lojistik, Havayolu, Gübre..."
    )

    col_a, col_b = st.columns(2)
    if col_a.button("Ekle", use_container_width=True) and new_product.strip():
        if new_product.strip() not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_product.strip())
            st.success(f"{new_product.strip()} eklendi.")
        else:
            st.info("Bu ürün zaten listede.")

    if col_b.button("Temizle", use_container_width=True):
        st.session_state.watchlist = []
        st.rerun()

    st.divider()

    if st.session_state.watchlist:
        st.subheader("Mevcut liste")
        for p in st.session_state.watchlist:
            st.write(f"• **{p}**")
    else:
        st.info("Liste boş.")

    st.divider()
    st.caption("🌐 [prospectapp.finance](https://prospectapp.finance)")
    st.caption("📦 v0.1 MVP")

# ─────────────────────────────────────────────────────────────
# ÜST PANEL — BRENT VERİSİ + TAHMİN
# ─────────────────────────────────────────────────────────────
col_chart, col_pred = st.columns([2, 1])

with col_chart:
    st.subheader("Brent Petrol — Son 90 Gün")
    try:
        oil = yf.download("BZ=F", period="3mo", progress=False)
        if not oil.empty:
            st.line_chart(oil["Close"], height=300)
            current_price = float(oil["Close"].iloc[-1])
            week_ago = float(oil["Close"].iloc[-7])
            change_pct = ((current_price - week_ago) / week_ago) * 100

            st.metric(
                "Şu anki fiyat (USD/varil)",
                f"${current_price:.2f}",
                delta=f"{change_pct:+.2f}% (haftalık)"
            )
        else:
            raise ValueError("Veri boş döndü")
    except Exception as e:
        current_price = 82.41
        change_pct = 1.2
        st.warning("Canlı veri alınamadı, demo değerlerle devam ediliyor.")
        st.metric("Demo fiyat (USD/varil)", f"${current_price:.2f}",
                  delta=f"{change_pct:+.2f}%")

with col_pred:
    st.subheader("7 Günlük Tahmin")
    predicted = predict_oil_price(current_price, change_pct)
    pred_change = ((predicted - current_price) / current_price) * 100
    direction = "📈 Yükseliş" if predicted > current_price else "📉 Düşüş"

    st.metric(
        "Tahmin (USD/varil)",
        f"${predicted:.2f}",
        delta=f"{pred_change:+.2f}%"
    )
    st.write(f"**Yön:** {direction}")
    st.caption(
        "Tahmin = trend × 0.40 + sentiment × 3.0 + mean_reversion × 0.15"
    )

# ─────────────────────────────────────────────────────────────
# HABER SENTIMENT
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("Haber Sentiment Analizi")

news_score, news_items = analyze_news_sentiment()
if news_score > 0.1:
    sentiment_label = "Pozitif — fiyatlar üzerinde yukarı yönlü baskı"
    sentiment_color = "🟢"
elif news_score < -0.1:
    sentiment_label = "Negatif — fiyatlar üzerinde aşağı yönlü baskı"
    sentiment_color = "🔴"
else:
    sentiment_label = "Nötr — anlamlı yön sinyali yok"
    sentiment_color = "⚪"

col_s1, col_s2 = st.columns([1, 3])
col_s1.metric("Sentiment skoru", f"{news_score:+.2f}")
col_s2.write(f"{sentiment_color} **{sentiment_label}**")

with st.expander("Taranan başlıklar"):
    for item in news_items:
        st.write(f"• {item}")

# ─────────────────────────────────────────────────────────────
# UYARILAR
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("Ürün Uyarıları")

if not st.session_state.watchlist:
    st.info("Sol panelden takip listesine ürün ekleyerek uyarıları görüntüleyin.")
else:
    for product in st.session_state.watchlist:
        corr = get_correlation(product)
        alert = generate_alert(product, corr, predicted, current_price)

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"### {product}")
            col2.metric("Korelasyon", f"{corr:+.2f}")
            st.write(alert)

# ─────────────────────────────────────────────────────────────
# ALT
# ─────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Prospect Lab v0.1 MVP — BTK Hackathon 2026 · "
    "Üretilen uyarılar bilgilendirme amaçlıdır, yatırım tavsiyesi değildir. · "
    "Web: prospectapp.finance"
)
