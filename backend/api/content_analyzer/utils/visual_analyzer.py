import os
import cv2

def analyze_visuals(frames_dir):
    if not os.path.exists(frames_dir):
        return {"frame_count": 0, "resolution": None, "avg_brightness": None}

    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])

    if not frames:
        return {"frame_count": 0, "resolution": None, "avg_brightness": None}

    first_frame = os.path.join(frames_dir, frames[0])
    img = cv2.imread(first_frame)
    if img is None:
        return {"frame_count": len(frames), "resolution": None, "avg_brightness": None}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = float(gray.mean())
    h, w = img.shape[:2]

    return {
        "frame_count": len(frames),
        "resolution": f"{w}x{h}",
        "avg_brightness": brightness,
        "description": "CPU-safe visual analysis"
    }
