import os
import cv2
import numpy as np


def analyze_visual_features(frames_folder: str):
    """
    Computes:
        - frame_count
        - avg_brightness
        - avg_sharpness
        - motion_intensity
    """

    if not os.path.exists(frames_folder):
        return {
            "frame_count": 0,
            "avg_brightness": 0,
            "avg_sharpness": 0,
            "motion_intensity": 0
        }

    frames = sorted(os.listdir(frames_folder))
    if len(frames) == 0:
        return {
            "frame_count": 0,
            "avg_brightness": 0,
            "avg_sharpness": 0,
            "motion_intensity": 0
        }

    brightness_vals = []
    sharpness_vals = []
    motion_vals = []

    prev_gray = None

    for frame_name in frames:
        path = os.path.join(frames_folder, frame_name)
        frame = cv2.imread(path)

        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Brightness = mean pixel intensity
        brightness_vals.append(np.mean(gray))

        # Sharpness = variance of Laplacian
        sharpness_vals.append(cv2.Laplacian(gray, cv2.CV_64F).var())

        # Motion = difference vs previous frame
        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            motion_vals.append(np.mean(diff))

        prev_gray = gray

    return {
        "frame_count": len(frames),
        "avg_brightness": float(np.mean(brightness_vals)),
        "avg_sharpness": float(np.mean(sharpness_vals)),
        "motion_intensity": float(np.mean(motion_vals) if len(motion_vals) else 0)
    }
