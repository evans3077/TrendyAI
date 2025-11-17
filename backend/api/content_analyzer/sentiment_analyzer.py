from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    blob = TextBlob(text)
    vader_scores = vader.polarity_scores(text)

    polarity = (blob.sentiment.polarity + vader_scores["compound"]) / 2

    if polarity > 0.2:
        label = "positive"
    elif polarity < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {
        "polarity": polarity,
        "sentiment": label
    }
