import streamlit as st
from textblob import TextBlob


def initialize_session_state():
    defaults = {
        "articles": [],
        "summary": None,
        "status_text": "Ready",
        "status_type": "info",
        "search_query": "",
        "last_query": "",
        "auto_refresh_on": False,
        "credibility_results": {}
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_status(message, status_type="info"):
    st.session_state.status_text = message
    st.session_state.status_type = status_type


def analyze_sentiment(text):
    analysis = TextBlob(text or "")
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "😊 Positive"
    elif polarity < 0:
        return "😐 Negative"
    else:
        return "🔵 Neutral"


def local_fake_news_detector(title, description, source):
    text = f"{title} {description}".lower()

    suspicious_words = [
        "shocking", "you won't believe", "miracle", "secret", "exposed",
        "viral", "breaking", "must read", "unbelievable", "click here",
        "exclusive", "rumor", "rumour", "fake", "scam", "hoax"
    ]

    trusted_sources = [
        "bbc", "reuters", "associated press", "ap", "the hindu", "ndtv",
        "times of india", "hindustan times", "indian express", "cnn",
        "al jazeera", "forbes", "bloomberg", "cnbc", "the guardian"
    ]

    score = 50
    reasons = []

    source_lower = (source or "").lower()

    if any(ts in source_lower for ts in trusted_sources):
        score += 25
        reasons.append("trusted source")
    elif source_lower.strip() == "" or source_lower == "unknown source":
        score -= 10
        reasons.append("unknown source")
    else:
        reasons.append("unverified source")

    suspicious_count = 0
    for word in suspicious_words:
        if word in text:
            suspicious_count += 1

    if suspicious_count > 0:
        score -= suspicious_count * 10
        reasons.append("sensational wording")

    uppercase_count = sum(1 for ch in title if ch.isupper())
    if len(title) > 0 and uppercase_count > len(title) * 0.4:
        score -= 15
        reasons.append("excessive uppercase title")

    if not description or len(description.strip()) < 25:
        score -= 10
        reasons.append("very limited context")

    if title.count("!") >= 2 or description.count("!") >= 2:
        score -= 10
        reasons.append("exaggerated punctuation")

    score = max(0, min(100, score))

    if score >= 75:
        label = "Likely Reliable"
    elif score >= 45:
        label = "Needs Verification"
    else:
        label = "Suspicious"

    reason = ", ".join(reasons) if reasons else "basic content analysis"

    return {
        "label": label,
        "confidence": f"{score}/100",
        "reason": reason.capitalize()
    }


def credibility_class(label):
    label_low = label.lower()
    if "reliable" in label_low or "credible" in label_low:
        return "verify-good"
    elif "suspicious" in label_low or "fake" in label_low:
        return "verify-bad"
    return "verify-mid"