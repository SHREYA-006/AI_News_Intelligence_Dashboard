import os
import streamlit as st
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", os.getenv("NEWS_API_KEY"))


def fetch_news_data(query):
    from_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 8,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return None, data.get("message", "API Error")

        return data.get("articles", []), None

    except requests.exceptions.Timeout:
        return None, "News request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Internet connection issue while fetching news."
    except Exception:
        return None, "Could not fetch news right now."