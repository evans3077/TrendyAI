import moviepy as mp
import os

def extract_audio(video_path: str, output_audio_path: str) -> str:
    """
    Extracts audio from the video and saves it to output_audio_path.
    
    Returns the output audio file path.
    """

    # Ensure folder exists
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

    clip = mp.VideoFileClip(video_path)

    if not clip.audio:
        raise ValueError("No audio track found in this video.")

    clip.audio.write_audiofile(output_audio_path)

    clip.close()

    return output_audio_path
