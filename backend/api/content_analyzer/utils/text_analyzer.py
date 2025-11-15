import re
from textblob import TextBlob
from collections import Counter

def extract_keywords(text: str, limit=20):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    return [w for w, _ in Counter(words).most_common(limit)]

def extract_topics(summary: str, limit=5):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", summary.lower())
    return [w for w, _ in Counter(words).most_common(limit)]

def analyze_sentiment(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.25:
        label = "positive"
    elif polarity < -0.25:
        label = "negative"
    else:
        label = "neutral"
    return {"polarity": float(polarity), "sentiment": label}

def analyze_text(transcript: str, summary: str):
    return {
        "transcript": transcript,
        "summary": summary,
        "keywords": extract_keywords(transcript),
        "topics": extract_topics(summary),
        "sentiment": analyze_sentiment(transcript)
    }
