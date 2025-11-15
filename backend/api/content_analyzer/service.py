import os
import json
from .utils.text_analyzer import analyze_text
from .utils.audio_analyzer import analyze_audio
from backend.api.content_analyzer.utils.visual_analyzer import analyze_visuals
from .utils.fusion_engine import fuse_content
from .utils.quality_scorer import compute_quality_score


def analyze_job(job_path: str):
    """
    Full multi-module CPU-safe analysis for next pipeline module.
    """

    # === Locate files ===
    transcript_path = os.path.join(job_path, "transcript.txt")
    summary_path = os.path.join(job_path, "summary.txt")

    base_folder = os.path.dirname(os.path.dirname(job_path))
    frames_folder = os.path.join(base_folder, "frames")
    audio_path = os.path.join(base_folder, "audio", "audio.wav")
    video_path = os.path.join(base_folder, "video", "original.mp4")

    # === Load text ===
    transcript = open(transcript_path, "r", encoding="utf-8").read()
    summary = open(summary_path, "r", encoding="utf-8").read()

    # === Run analysis modules ===
    text_data = analyze_text(transcript, summary)
    audio_data = analyze_audio(audio_path)
    visual_data = analyze_visuals(frames_folder)
    fusion_data = fuse_content(text_data, visual_data, audio_data)
    quality_score = compute_quality_score(text_data, visual_data, audio_data)

    # === Assemble final output ===
    result = {
        "status": "completed",
        "mode": "cpu_modular_full_pipeline",
        "paths": {
            "transcript": transcript_path,
            "summary": summary_path,
            "video": video_path,
            "audio": audio_path,
            "frames_folder": frames_folder,
        },
        "text": text_data,
        "visual": visual_data,
        "audio": audio_data,
        "fusion": fusion_data,
        "quality_score": quality_score
    }

    # === Save JSON ===
    output_json = os.path.join(
        base_folder, "..", "analysis", f"{os.path.basename(base_folder)}.json"
    )
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return result
