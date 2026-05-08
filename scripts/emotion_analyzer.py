import re
from textblob import TextBlob

EMOTION_KEYWORDS = {
    "high": ["screamed", "war", "death", "betrayal", "explosion", "angry", "run"],
    "medium": ["walked", "looked", "spoke", "realized", "found"],
    "low": ["peace", "calm", "silence", "soft", "gentle"]
}

def analyze_emotion(text: str):
    text_lower = text.lower()

    score = 0.5  # neutral baseline

    for word in EMOTION_KEYWORDS["high"]:
        if word in text_lower:
            score += 0.3

    for word in EMOTION_KEYWORDS["low"]:
        if word in text_lower:
            score -= 0.2

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    score += polarity * 0.5

    score = max(0.1, min(1.0, score))

    if score > 0.7:
        return "high", score
    elif score > 0.4:
        return "medium", score
    else:
        return "low", score