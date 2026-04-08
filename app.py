import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timedelta
from google import genai
import webbrowser
from textblob import TextBlob
import os
from dotenv import load_dotenv

load_dotenv()

# ================= API KEYS =================
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

articles = []
auto_refresh_on = False

# ================= FUNCTIONS =================

def fetch_news(category=None):
    query = search_entry.get().strip()

    if category:
        query = category

    if not query:
        messagebox.showwarning("Input Error", "Enter topic or choose category.")
        return

    status_label.config(text="Fetching latest news...", fg="yellow")
    root.update_idletasks()

    from_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

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

        news_box.delete("1.0", tk.END)
        articles.clear()

        if response.status_code != 200:
            raise Exception(data.get("message", "API Error"))

        articles.extend(data["articles"])

        if not articles:
            news_box.insert(tk.END, "❌ No news found.\n")
            return

        for i, article in enumerate(articles, 1):
            sentiment = analyze_sentiment(article["title"])

            news_box.insert(tk.END, f"📰 {i}. {article['title']}\n", "headline")
            news_box.insert(tk.END, f"Source: {article['source']['name']} | {sentiment}\n")

            link = article["url"]
            news_box.insert(tk.END, "Read More\n", ("link", link))
            news_box.insert(tk.END, "-" * 60 + "\n")

        status_label.config(text="Latest news loaded.", fg="lightgreen")

    except Exception as e:
        news_box.insert(tk.END, f"Error: {e}")
        status_label.config(text="Error fetching news.", fg="red")


def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "😊 Positive"
    elif polarity < 0:
        return "😡 Negative"
    else:
        return "😐 Neutral"


def summarize_news():
    if not articles:
        messagebox.showwarning("No Content", "Fetch news first.")
        return

    status_label.config(text="Generating AI summary...", fg="cyan")

    try:
        combined_text = ""
        for article in articles[:5]:
            combined_text += article["title"] + "\n"

        limited_content = combined_text[:3000]

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"Summarize this news in 5 bullet points:\n{limited_content}"
        )

        summary = response.text

        news_box.delete("1.0", tk.END)
        news_box.insert(tk.END, "🤖 AI SUMMARY\n\n", "title")
        news_box.insert(tk.END, summary)

        status_label.config(text="Summary generated.", fg="lightgreen")

    except Exception as e:
        news_box.insert(tk.END, f"AI Error: {e}")
        status_label.config(text="AI error.", fg="red")


def toggle_auto_refresh():
    global auto_refresh_on
    auto_refresh_on = not auto_refresh_on

    if auto_refresh_on:
        status_label.config(text="Auto-refresh ON", fg="cyan")
        auto_refresh()
    else:
        status_label.config(text="Auto-refresh OFF", fg="red")


def auto_refresh():
    if auto_refresh_on:
        fetch_news()
        root.after(60000, auto_refresh)


def open_link(event):
    index = news_box.index("@%s,%s" % (event.x, event.y))
    tags = news_box.tag_names(index)

    for tag in tags:
        if tag.startswith("http"):
            webbrowser.open(tag)


# ================= GUI =================

root = tk.Tk()
root.title("🚀 AI News Intelligence Dashboard")
root.geometry("950x680")
root.configure(bg="#121212")

tk.Label(root, text="🧠 AI News Intelligence Dashboard",
         font=("Arial", 22, "bold"),
         bg="#121212", fg="#00ffcc").pack(pady=10)

frame = tk.Frame(root, bg="#121212")
frame.pack()

search_entry = tk.Entry(frame, width=40, font=("Arial", 13))
search_entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame, text="Search",
          command=fetch_news,
          bg="#00c853", fg="white").pack(side=tk.LEFT, padx=5)

tk.Button(frame, text="AI Summary",
          command=summarize_news,
          bg="#2962ff", fg="white").pack(side=tk.LEFT, padx=5)

tk.Button(frame, text="Auto Refresh",
          command=toggle_auto_refresh,
          bg="#ff6d00", fg="white").pack(side=tk.LEFT, padx=5)

# Categories
cat_frame = tk.Frame(root, bg="#121212")
cat_frame.pack(pady=5)

for cat in ["Technology", "Sports", "Business", "Health", "Entertainment"]:
    tk.Button(cat_frame, text=cat,
              command=lambda c=cat: fetch_news(c),
              bg="#333", fg="white").pack(side=tk.LEFT, padx=4)

news_box = tk.Text(root, wrap=tk.WORD, bg="#1e1e1e", fg="white")
news_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scroll = ttk.Scrollbar(news_box)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
news_box.config(yscrollcommand=scroll.set)
scroll.config(command=news_box.yview)

news_box.tag_config("title", font=("Arial", 16, "bold"), foreground="#00e5ff")
news_box.tag_config("headline", font=("Arial", 12, "bold"))
news_box.tag_config("link", foreground="#64b5f6", underline=True)

news_box.tag_bind("link", "<Button-1>", open_link)

status_label = tk.Label(root, text="Ready", bg="#121212", fg="lightgreen")
status_label.pack()

root.mainloop()