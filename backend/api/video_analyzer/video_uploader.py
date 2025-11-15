import os, uuid

def save_video_file(file):
    video_dir = "data/raw"
    os.makedirs(video_dir, exist_ok=True)

    video_path = os.path.join(video_dir, f"{uuid.uuid4()}_{file.filename}")
    with open(video_path, "wb") as buffer:
        buffer.write(file.file.read())
    return video_path
