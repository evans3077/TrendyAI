import os
import json

from .utils.file_utils import read_text_file, ensure_dir
from .utils.text_utils import clean_text

from .speech_to_text import transcribe_audio_file
from .summarizer import generate_summary
from .keyword_extractor import extract_keywords_keybert
from .topic_extractor import extract_topics_minilm
from .sentiment_analyzer import analyze_sentiment

from .object_detector import detect_objects_yolo_cpu
from .text_detector import detect_text_easyocr
from .visual_analyzer import analyze_visual_features


def analyze_job(job_path: str):
    """
    Full intelligent CPU-friendly analysis.

    Produces:
        - Full transcript
        - High-quality summary
        - KeyBERT keywords
        - Semantic topics (MiniLM)
        - Sentiment
        - YOLO object detection
        - OCR on-screen text detection
        - Visual metrics
    """

    # ---------------------------------------------
    # PATHS
    # ---------------------------------------------
    transcript_path = os.path.join(job_path, "transcript.txt")
    summary_path = os.path.join(job_path, "summary.txt")

    base_folder = os.path.dirname(os.path.dirname(job_path))
    frames_folder = os.path.join(base_folder, "frames")
    audio_path = os.path.join(base_folder, "audio", "audio.wav")
    video_path = os.path.join(base_folder, "video", "original.mp4")

    # ---------------------------------------------
    # 1. TRANSCRIPT
    # ---------------------------------------------
    if os.path.exists(transcript_path):
        transcript = read_text_file(transcript_path)
    else:
        transcript = transcribe_audio_file(audio_path)
        ensure_dir(os.path.dirname(transcript_path))
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)

    transcript_clean = clean_text(transcript)

    # ---------------------------------------------
    # 2. SUMMARY
    # ---------------------------------------------
    if os.path.exists(summary_path):
        summary = read_text_file(summary_path)
    else:
        summary = generate_summary(transcript_clean)
        ensure_dir(os.path.dirname(summary_path))
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

    # ---------------------------------------------
    # 3. KEYWORDS (KeyBERT-MiniLM)
    # ---------------------------------------------
    keywords = extract_keywords_keybert(transcript_clean)

    # ---------------------------------------------
    # 4. TOPICS (SentenceTransformer MiniLM)
    # ---------------------------------------------
    topics = extract_topics_minilm(transcript_clean)

    # ---------------------------------------------
    # 5. SENTIMENT
    # ---------------------------------------------
    sentiment = analyze_sentiment(transcript_clean)

    # ---------------------------------------------
    # 6. OBJECT DETECTION (YOLO)
    # ---------------------------------------------
    detected_objects = detect_objects_yolo_cpu(frames_folder)

    # ---------------------------------------------
    # 7. OCR ON-SCREEN TEXT
    # ---------------------------------------------
    detected_text = detect_text_easyocr(frames_folder)

    # ---------------------------------------------
    # 8. VISUAL FEATURE ANALYSIS
    # ---------------------------------------------
    visual_stats = analyze_visual_features(frames_folder)

    # ---------------------------------------------
    # 9. BUILD RESULT
    # ---------------------------------------------
    result = {
        "status": "completed",

        "paths": {
            "transcript": transcript_path,
            "summary": summary_path,
            "video": video_path,
            "audio": audio_path,
            "frames_folder": frames_folder,
        },

        "text": {
            "transcript": transcript,
            "summary": summary,
            "keywords": keywords,
            "topics": topics,
            "sentiment": sentiment,
        },

        "visual": {
            "stats": visual_stats,
            "detected_objects": detected_objects,
            "detected_text": detected_text,
        },

        "audio": {
            "path": audio_path
        }
    }

    # ---------------------------------------------
    # 10. SAVE OUTPUT JSON
    # ---------------------------------------------
    output_path = os.path.join(base_folder, "analysis", "content_analysis.json")
    ensure_dir(os.path.dirname(output_path))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return result
