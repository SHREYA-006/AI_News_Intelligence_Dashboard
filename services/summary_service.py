import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


def safe_summary_generate(prompt, retries=3, delay=2):
    models_to_try = [
        "gemini-3-flash-preview",
        "gemini-2.0-flash"
    ]

    last_error = ""

    for model_name in models_to_try:
        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                text = getattr(response, "text", None)

                if text and text.strip():
                    print("SUMMARY SUCCESS:", text[:200])
                    return text.strip(), None

                last_error = "Empty response returned by AI service."

            except Exception as e:
                last_error = str(e)
                print("SUMMARY ERROR:", last_error)

                temporary = any(word in last_error.lower() for word in [
                    "503", "unavailable", "overloaded", "high demand",
                    "timeout", "deadline", "rate limit", "quota", "500"
                ])

                if temporary and attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))
                    continue
                else:
                    break

    low = last_error.lower()

    if "api key" in low or "permission_denied" in low or "403" in low:
        return None, "AI service is not configured correctly."
    elif "quota" in low or "rate limit" in low or "429" in low:
        return None, "AI usage limit reached. Please try again later."
    elif "503" in low or "unavailable" in low or "overloaded" in low or "high demand" in low:
        return None, "AI service is temporarily busy. Please try again."
    elif "404" in low or "not found" in low:
        return None, "Selected AI model is not available for this API key."
    elif "empty response" in low:
        return None, "AI could not generate a summary right now."
    else:
        return None, "Summary is unavailable at the moment."


def generate_summary(articles):
    combined_text = ""
    for article in articles:
        title = article.get("title", "")
        desc = article.get("description", "")
        combined_text += f"Title: {title}\nDescription: {desc}\n\n"

    prompt = f"""
Summarize the following news into exactly 5 short bullet points.
Keep it simple, clear, and useful for a student presentation.

News:
{combined_text[:2500]}
"""

    return safe_summary_generate(prompt)