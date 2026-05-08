from scripts.emotion_analyzer import analyze_emotion


def assign_music_cues(timeline):
    """
    Adds music metadata to each scene in the timeline.
    """

    enriched = []

    for item in timeline:

        if item["type"] != "scene":
            enriched.append(item)
            continue

        emotion, score = analyze_emotion(item["text"])

        music_style = decide_music_style(emotion, score)
        intensity = decide_intensity(score)
        volume = decide_volume(score)

        item["music"] = {
            "style": music_style,
            "intensity": intensity,
            "volume": volume,
            "fade_in": 1.5 if score > 0.6 else 1.0,
            "fade_out": 1.5
        }

        enriched.append(item)

    return enriched


def decide_music_style(emotion, score):

    if emotion == "high":
        return "cinematic orchestral tension, hybrid trailer style"

    if emotion == "medium":
        return "emotional cinematic ambient score"

    return "soft atmospheric pads, minimal piano tones"


def decide_intensity(score):

    if score > 0.75:
        return "high"
    if score > 0.45:
        return "medium"
    return "low"


def decide_volume(score):

    if score > 0.75:
        return 0.35  # keep under dialogue
    if score > 0.45:
        return 0.25
    return 0.15