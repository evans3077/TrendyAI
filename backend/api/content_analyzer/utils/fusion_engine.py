def fuse_content(text_data, visual_data, audio_data):
    """
    Fusion layer: creates high-level reasoning across modalities.
    """
    transcript = text_data.get("transcript", "").lower()
    topics = text_data.get("topics", [])

    fusion = {
        "dominant_topics": topics[:3],
        "visual_support": "low" if visual_data["frame_count"] < 5 else "good",
        "audio_quality": "acceptable" if audio_data["duration_seconds"] > 0 else "missing",
        "narrative_strength": len(transcript.split()) // 30,  # words per 30 tokens
    }

    return fusion
