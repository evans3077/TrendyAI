def compute_quality_score(text_data, visual_data, audio_data):
    score = 0

    # text richness (keywords + topics)
    score += min(len(text_data.get("keywords", [])), 20)
    score += min(len(text_data.get("topics", [])), 10)

    # sentiment neutrality preferred
    polarity = text_data["sentiment"]["polarity"]
    score += max(0, 10 - abs(polarity * 10))

    # visual completeness
    if visual_data["frame_count"] > 0:
        score += 10

    # audio presence
    if audio_data["duration_seconds"] > 0:
        score += 10

    return round(score, 2)
