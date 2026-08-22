"""
Prospect Lab — Brent Petrol Tahmin Modülü

7-günlük yön tahmini üretir. Tahmin formülü üç bileşenden oluşur:

  1. Trend etkisi      (haftalık değişimi yumuşatılmış sürdür)
  2. Sentiment etkisi  (haber sentiment'inden gelen yön baskısı)
  3. Mean-reversion    (ortalamaya dönüş eğilimi)
 
Tasarım felsefesi:
  - Açıklanabilirlik > karmaşıklık
  - Yön > kesin sayı
  - Sentiment olmadan teknik analiz eksiktir
 
Roadmap: 
  - Facebook Prophet (v0.2)
  - PyTorch LSTM + attention (v0.3)
  - Ensemble blending (v0.4)
"""
from src.news_analyzer import analyze_news_sentiment


# Tahmin formülü katsayıları
TREND_WEIGHT = 0.40
SENTIMENT_AMPLITUDE = 3.0      # max ±3% sentiment etkisi
MEAN_REVERSION_WEIGHT = 0.15


def predict_oil_price(current: float, weekly_change_pct: float) -> float:
    """
    7-günlük Brent fiyat tahmini.

    Parametreler:
        current: Mevcut Brent spot fiyatı (USD/varil)
        weekly_change_pct: Son haftalık % değişim

    Döner:
        Tahmin edilen fiyat (USD/varil)
    """
    sentiment, _ = analyze_news_sentiment()

    # Bileşen 1: Trend etkisi
    # Mevcut momentum'u yumuşatılmış şekilde projekte et
    trend_effect = weekly_change_pct * TREND_WEIGHT

    # Bileşen 2: Sentiment etkisi
    # Haber sentiment'ini % etkisine çevir
    sentiment_effect = sentiment * SENTIMENT_AMPLITUDE

    # Bileşen 3: Mean-reversion
    # Aşırı hareketleri törpüle (ortalamaya dönüş)
    mean_reversion = -weekly_change_pct * MEAN_REVERSION_WEIGHT

    total_change_pct = trend_effect + sentiment_effect + mean_reversion
    predicted = current * (1 + total_change_pct / 100)

    return predicted


def explain_prediction(current: float, weekly_change_pct: float) -> dict:
    """
    Tahmin bileşenlerini açıklanabilir şekilde döner.
    Dashboard ve sunum için kullanılır.
    """
    sentiment, _ = analyze_news_sentiment()
    trend_effect = weekly_change_pct * TREND_WEIGHT
    sentiment_effect = sentiment * SENTIMENT_AMPLITUDE
    mean_reversion = -weekly_change_pct * MEAN_REVERSION_WEIGHT
    total = trend_effect + sentiment_effect + mean_reversion
    predicted = current * (1 + total / 100)

    return {
        "current": current,
        "predicted": predicted,
        "total_change_pct": total,
        "components": {
            "trend": trend_effect,
            "sentiment": sentiment_effect,
            "mean_reversion": mean_reversion,
        },
        "sentiment_score": sentiment,
    }


if __name__ == "__main__":
    # Modül testi
    result = explain_prediction(current=82.41, weekly_change_pct=2.5)
    print(f"Mevcut: ${result['current']:.2f}")
    print(f"Tahmin: ${result['predicted']:.2f} ({result['total_change_pct']:+.2f}%)")
    print(f"Bileşenler:")
    for k, v in result['components'].items():
        print(f"  • {k:<15} {v:+.3f}%")
