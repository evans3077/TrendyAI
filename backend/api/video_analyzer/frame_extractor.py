import moviepy as mp
import os

def extract_key_frames(video_path, output_dir, frame_interval=2):
    # force conversion to float or int
    frame_interval = float(frame_interval)

    clip = mp.VideoFileClip(video_path)
    duration = clip.duration

    t = 0
    idx = 0

    while t < duration:
        frame = clip.get_frame(t)
        frame_path = os.path.join(output_dir, f"frame_{idx}.jpg")
        mp.ImageClip(frame).save_frame(frame_path)
        t += frame_interval
        idx += 1

    clip.close()
