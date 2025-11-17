import whisper

def transcribe_audio_file(audio_path: str):
    """
    Full transcription – no cutoff.
    Whisper handles long audio by chunking internally.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False)
    return result["text"]
