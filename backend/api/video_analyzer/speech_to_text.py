import os
import math
import tempfile
import subprocess
import whisper


# Whisper model is loaded ONCE (fast & memory safe)
_whisper_model = whisper.load_model("medium")


def _chunk_audio(input_audio_path: str, chunk_length: int = 30):
    """
    Splits audio into fixed-length chunks using ffmpeg.
    chunk_length is in seconds.
    """
    temp_dir = tempfile.mkdtemp(prefix="audio_chunks_")

    # Get duration of audio
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_audio_path
    ]
    duration_str = subprocess.check_output(cmd).decode().strip()
    duration = float(duration_str)
    total_chunks = math.ceil(duration / chunk_length)

    chunk_paths = []

    for i in range(total_chunks):
        start = i * chunk_length
        chunk_file = os.path.join(temp_dir, f"chunk_{i}.wav")
        cmd = [
            "ffmpeg", "-y",
            "-i", input_audio_path,
            "-ss", str(start),
            "-t", str(chunk_length),
            chunk_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunk_paths.append(chunk_file)

    return chunk_paths, temp_dir


def transcribe_audio(audio_path: str):
    """
    Transcribes LONG AUDIO SAFELY with:
        - FFmpeg chunking
        - Whisper medium
        - Auto-merge
        - No cutoff
    """

    chunks, temp_dir = _chunk_audio(audio_path, chunk_length=30)

    full_transcription = []

    for idx, chunk_file in enumerate(chunks):
        try:
            result = _whisper_model.transcribe(chunk_file)
            text = result.get("text", "").strip()
        except Exception as e:
            text = f"[ERROR processing chunk {idx}: {str(e)}]"

        full_transcription.append(text)

    # Merge all chunk transcripts into one full transcript
    merged_text = "\n".join(full_transcription).strip()

    # Cleanup temporary chunk folder
    try:
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
    except:
        pass

    return merged_text
