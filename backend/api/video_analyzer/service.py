import os
import uuid
import json
import time
from datetime import datetime

from moviepy import VideoFileClip
from transformers import pipeline

from .audio_extractor import extract_audio
from backend.api.video_analyzer.speech_to_text import transcribe_audio
from .video_summary import summarize_long_text
from .video_uploader import save_video_file
from .frame_extractor import extract_key_frames

# Folder for global analysis JSONs
ANALYSIS_DIR = "data/processed/analysis"
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


async def analyze_video(file):
    """
    Full video analysis pipeline:
    - Save video
    - Extract audio
    - Extract key frames
    - Full transcript (NO CUTOFF, chunked Whisper)
    - Long-text summary (chunked summarizer)
    - Metadata
    """

    # ------------------------------------------------
    # 1. Create Job Folder
    # ------------------------------------------------
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    job_id = f"job_{timestamp}_{uuid.uuid4().hex[:6]}"

    base_dir = os.path.join("data", "processed", job_id)
    video_dir = os.path.join(base_dir, "video")
    audio_dir = os.path.join(base_dir, "audio")
    frames_dir = os.path.join(base_dir, "frames")
    clips_dir = os.path.join(base_dir, "clips")
    analysis_dir = os.path.join(base_dir, "analysis")

    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)
    os.makedirs(analysis_dir, exist_ok=True)

    # ------------------------------------------------
    # 2. Save Video
    # ------------------------------------------------
    video_path = os.path.join(video_dir, "original.mp4")
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # ------------------------------------------------
    # 3. Extract Audio
    # ------------------------------------------------
    audio_path = os.path.join(audio_dir, "audio.wav")
    extract_audio(video_path, audio_path)

    # ------------------------------------------------
    # 4. Extract Key Frames
    # ------------------------------------------------
    extract_key_frames(video_path, frames_dir)

    # ------------------------------------------------
    # 5. Chunked Transcription (NO CUT-OFF)
    # ------------------------------------------------
    transcript_text = transcribe_audio(audio_path, chunk_minutes=15)

    transcript_path = os.path.join(analysis_dir, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    # ------------------------------------------------
    # 6. Chunked Summary (Long-text safe)
    # ------------------------------------------------
    summary_text = summarize_long_text(transcript_text)

    summary_path = os.path.join(analysis_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    # ------------------------------------------------
    # 7. Metadata
    # ------------------------------------------------
    clip = VideoFileClip(video_path)
    metadata = {
        "duration_seconds": clip.duration,
        "fps": clip.fps,
        "resolution": f"{clip.w}x{clip.h}"
    }
    clip.close()

    # ------------------------------------------------
    # 8. Build JSON Response
    # ------------------------------------------------
    json_response = {
        "job_id": job_id,
        "paths": {
            "video": video_path,
            "audio": audio_path,
            "frames_folder": frames_dir,
            "clips_folder": clips_dir,
            "transcript_path": transcript_path,
            "summary_path": summary_path
        },
        "frames": sorted(os.listdir(frames_dir)),
        "clips": sorted(os.listdir(clips_dir)),
        "video_metadata": metadata,
        "analysis": {
            "scene_summary_path": summary_path,
            "audio_transcript_path": transcript_path,
            "detected_objects": [],  # Will be filled by content analyzer
            "detected_text": [],
            "key_topics": []
        },
        "status": "completed"
    }

    # ------------------------------------------------
    # 9. Save Global JSON
    # ------------------------------------------------
    json_output_path = os.path.join(ANALYSIS_DIR, f"{job_id}.json")
    with open(json_output_path, "w") as f:
        json.dump(json_response, f, indent=4)

    json_response["analysis_json_path"] = json_output_path

    return json_response
