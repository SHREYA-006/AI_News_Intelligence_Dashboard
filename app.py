import streamlit as st
import time
from styles.style import load_css
from utils.helpers import (
    initialize_session_state,
    analyze_sentiment,
    credibility_class,
    set_status,
    local_fake_news_detector,
)
from services.news_service import fetch_news_data
from services.summary_service import generate_summary


st.set_page_config(
    page_title="AI News Intelligence Portal",
    page_icon="📰",
    layout="wide"
)

load_css()
initialize_session_state()

# ================= CORE FUNCTIONS =================
def fetch_news(category=None):
    query = st.session_state.search_query.strip()
    if category:
        query = category

    if not query:
        set_status("Enter a topic or choose a category.", "warning")
        return

    set_status("Fetching latest news...", "info")
    st.session_state.last_query = query
    st.session_state.summary = None
    st.session_state.credibility_results = {}

    articles, error = fetch_news_data(query)

    if error:
        set_status(error, "error")
        return

    st.session_state.articles = articles

    if not st.session_state.articles:
        set_status("No news found for this topic.", "warning")
        return

    set_status("Latest news loaded successfully.", "success")


def summarize_news():
    if not st.session_state.articles:
        set_status("Fetch news first before generating a summary.", "warning")
        return

    set_status("Generating AI summary...", "info")

    summary, error = generate_summary(st.session_state.articles[:5])

    print("Returned Summary:", summary)
    print("Returned Error:", error)

    if error:
        st.session_state.summary = None
        set_status(error, "warning")
        return

    st.session_state.summary = summary
    set_status("Summary generated successfully.", "success")


def analyze_article_credibility(index):
    if index >= len(st.session_state.articles):
        return

    article = st.session_state.articles[index]
    title = article.get("title", "")
    description = article.get("description", "")
    source = article.get("source", {}).get("name", "Unknown Source")

    if not title.strip():
        set_status("Not enough article data for fake news detection.", "warning")
        return

    set_status("Running fake news detection...", "info")

    result = local_fake_news_detector(title, description, source)
    st.session_state.credibility_results[index] = result

    set_status("Fake news detection completed.", "success")


def analyze_all_credibility():
    if not st.session_state.articles:
        set_status("Fetch news first before running fake news detection.", "warning")
        return

    set_status("Checking visible news...", "info")

    for i in range(min(5, len(st.session_state.articles))):
        article = st.session_state.articles[i]
        title = article.get("title", "")
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "Unknown Source")

        if not title.strip():
            continue

        result = local_fake_news_detector(title, description, source)
        st.session_state.credibility_results[i] = result

    set_status("Fake news detection updated.", "success")


def toggle_auto_refresh():
    if st.session_state.auto_refresh_on:
        set_status("Auto-refresh is ON.", "info")
    else:
        set_status("Auto-refresh is OFF.", "warning")


# ================= HEADER =================
st.markdown('<div class="main-title">📰 AI News Intelligence Portal</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Live news, sentiment analysis, AI summary, and fake news detection</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="simple-line"></div>', unsafe_allow_html=True)

# ================= STATUS =================
status_class = f"status-{st.session_state.status_type}"
st.markdown(
    f'<div class="status-box {status_class}">{st.session_state.status_text}</div>',
    unsafe_allow_html=True
)

# ================= SEARCH =================
st.markdown('<div class="section-title">Search News</div>', unsafe_allow_html=True)

st.text_input(
    "Search News",
    key="search_query",
    placeholder="Search your news here...",
    label_visibility="collapsed"
)

btn_col1, btn_col2, btn_col3 = st.columns([1.2, 1.2, 5])

with btn_col1:
    if st.button("Search"):
        fetch_news()

with btn_col2:
    if st.button("AI Summary"):
        summarize_news()

st.markdown('<div class="simple-line"></div>', unsafe_allow_html=True)

# ================= CONTROLS =================
left, right = st.columns([5, 1.8])

with left:
    st.markdown('<div class="section-title">Categories</div>', unsafe_allow_html=True)
    cat_cols = st.columns(5)
    categories = ["Technology", "Sports", "Business", "Health", "Entertainment"]

    for i, cat in enumerate(categories):
        with cat_cols[i]:
            if st.button(cat, key=f"cat_{cat}"):
                fetch_news(cat)

with right:
    st.markdown('<div class="section-title">Controls</div>', unsafe_allow_html=True)

    st.toggle(
        "Auto Refresh",
        key="auto_refresh_on",
        on_change=toggle_auto_refresh
    )

st.markdown('<div class="simple-line"></div>', unsafe_allow_html=True)

# ================= SUMMARY =================
print("Current session summary:", st.session_state.summary)

if st.session_state.summary is not None and str(st.session_state.summary).strip() != "":
    st.markdown('<div class="section-title">🤖 AI Summary</div>', unsafe_allow_html=True)
    st.write(st.session_state.summary)
    st.markdown('<div class="simple-line"></div>', unsafe_allow_html=True)

# ================= NEWS =================
if st.session_state.articles:
    st.markdown('<div class="section-title">Latest News</div>', unsafe_allow_html=True)

    for i, article in enumerate(st.session_state.articles):
        title = article.get("title", "No title available")
        source = article.get("source", {}).get("name", "Unknown Source")
        description = article.get("description") or "No description available."
        link = article.get("url", "#")
        sentiment = analyze_sentiment(title)

        st.markdown(f"""
        <div class="news-card">
            <div class="news-title">📰 {i+1}. {title}</div>
            <div class="news-meta"><b>Source:</b> {source} &nbsp; | &nbsp; <b>Sentiment:</b> {sentiment}</div>
            <div class="news-desc">{description}</div>
            <div><a href="{link}" target="_blank">Read full article</a></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Verify News", key=f"verify_{i}"):
            analyze_article_credibility(i)

        if i in st.session_state.credibility_results:
            result = st.session_state.credibility_results[i]
            css_class = credibility_class(result["label"])

            st.markdown(
                f'<div class="{css_class}">Detection Result: {result["label"]}</div>',
                unsafe_allow_html=True
            )
            st.write(f"**Confidence:** {result['confidence']}")
            st.write(f"**Reason:** {result['reason']}")

        st.markdown('<div class="news-separator"></div>', unsafe_allow_html=True)

else:
    st.write("Search for a topic or choose a category to fetch the latest news.")

# ================= AUTO REFRESH =================
if st.session_state.auto_refresh_on:
    time.sleep(60)
    if st.session_state.last_query:
        fetch_news(st.session_state.last_query)
    st.rerun()