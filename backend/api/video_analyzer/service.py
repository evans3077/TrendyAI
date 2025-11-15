import os, uuid, json, time
from datetime import datetime
from moviepy import VideoFileClip
from transformers import pipeline
from .audio_extractor import extract_audio
from .speech_to_text import transcribe_audio
from .video_summary import summarize_video
from .video_uploader import save_video_file
from .frame_extractor import extract_key_frames

# Folder to store analysis JSONs
ANALYSIS_DIR = "data/processed/analysis"
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Hugging Face summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

async def analyze_video(file):
    # 1. Create job folder
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    job_id = f"job_{timestamp}_{uuid.uuid4().hex[:6]}"
    base_dir = os.path.join("data", "processed", job_id)

    video_dir = os.path.join(base_dir, "video")
    audio_dir = os.path.join(base_dir, "audio")
    frames_dir = os.path.join(base_dir, "frames")
    clips_dir = os.path.join(base_dir, "clips")

    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)

    # 2. Save video
    video_path = os.path.join(video_dir, "original.mp4")
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # 3. Audio extraction
    audio_path = os.path.join(audio_dir, "audio.wav")
    extract_audio(video_path, audio_path)

    # 4. Frame extraction
    extract_key_frames(video_path, frames_dir)

    # 4a. Transcribe audio
    transcript_text = transcribe_audio(audio_path)

    # 4b. Summarize video based on transcript
    summary_text = summarize_video(transcript_text)

    # 5. Metadata using moviepy
    clip = VideoFileClip(video_path)
    metadata = {
        "duration_seconds": clip.duration,
        "fps": clip.fps,
        "resolution": f"{clip.w}x{clip.h}"
    }
    clip.close()

    # 6. Prepare JSON dictionary with transcript and summary
    json_response = {
        "job_id": job_id,
        "paths": {
            "video": video_path,
            "audio": audio_path,
            "frames_folder": frames_dir,
            "clips_folder": clips_dir
        },
        "frames": sorted(os.listdir(frames_dir)),
        "clips": sorted(os.listdir(clips_dir)),
        "video_metadata": metadata,
        "analysis": {
            "scene_summary": summary_text,       # full summary
            "audio_summary": transcript_text,    # full transcript
            "detected_objects": [],
            "detected_text": [],
            "key_topics": []
        },
        "status": "completed"
    }

    # 7. Save JSON to analysis folder
    json_output_path = os.path.join(ANALYSIS_DIR, f"{job_id}.json")
    with open(json_output_path, "w") as f:
        json.dump(json_response, f, indent=4)

    # Optional: include the JSON path in the response
    json_response["analysis_json_path"] = json_output_path

    return json_response
