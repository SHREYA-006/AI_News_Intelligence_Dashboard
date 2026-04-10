import streamlit as st


def load_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
    }

    .stApp {
        background: white;
        color: #2b2b2b;
    }

    .main-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        color: #b71c1c;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #7a4a4a;
        margin-bottom: 1.2rem;
    }

    .simple-line {
        border-bottom: 1.5px solid #f3b4b4;
        margin: 14px 0 18px 0;
    }

    .status-box {
        padding: 10px 12px;
        border-left: 4px solid #d84343;
        background: #fff8f8;
        margin: 10px 0 16px 0;
        font-weight: 600;
    }

    .status-info { color: #8a3b3b; }
    .status-success { color: #1f7a3a; }
    .status-warning { color: #9a6700; }
    .status-error { color: #b71c1c; }

    .section-title {
        color: #b71c1c;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .news-card {
        padding: 14px 0 6px 0;
    }
                
    .news-separator {
        border-bottom: 1.5px solid #f3c4c4;
        margin: 14px 0 18px 0;
    }

    .news-title {
        color: #a31515;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .news-meta {
        color: #6d4a4a;
        font-size: 0.95rem;
        margin-bottom: 8px;
    }

    .news-desc {
        color: #333333;
        font-size: 0.97rem;
        line-height: 1.5;
        margin-bottom: 10px;
    }

    .verify-good { color: #1f7a3a; font-weight: 700; }
    .verify-mid { color: #a36a00; font-weight: 700; }
    .verify-bad { color: #b71c1c; font-weight: 700; }

    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #efb5b5;
        background: white;
        color: #b71c1c;
        font-weight: 700;
        min-height: 42px;
    }

    div.stButton > button:hover {
        border: 1px solid #d84343;
        color: #8e1111;
        background: #fff5f5;
    }

    div[data-baseweb="input"] > div {
        background-color: white !important;
        border-radius: 10px !important;
        border: 1.5px solid #efb5b5 !important;
        min-height: 46px !important;
    }

    input {
        color: #2b2b2b !important;
        font-size: 16px !important;
    }

    input::placeholder {
        color: #b57b7b !important;
        opacity: 1 !important;
    }

    /* Strong toggle styling */
    div[data-testid="stToggle"] {
        opacity: 1 !important;
        margin-top: 4px;
    }

    div[data-testid="stToggle"] label,
    div[data-testid="stToggle"] label *,
    div[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"] * {
        color: #5c1414 !important;
        fill: #5c1414 !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)