import os
import wave
import contextlib

def get_audio_duration(path):
    if not os.path.exists(path):
        return 0.0
    try:
        with contextlib.closing(wave.open(path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / float(rate)
    except:
        return 0.0

def analyze_audio(audio_path: str):
    duration = get_audio_duration(audio_path)
    return {
        "duration_seconds": duration,
        "speech_ratio": min(duration / 60.0, 1.0),  # placeholder
        "notes": "CPU-safe audio analysis (no ML)"
    }
