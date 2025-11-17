import os
import easyocr

_ocr = easyocr.Reader(["en"], gpu=False)


def detect_text_easyocr(frames_folder: str):
    """
    Extract readable text from video frames using EasyOCR (CPU mode).
    """
    if not os.path.exists(frames_folder):
        return []

    results = []

    for frame in sorted(os.listdir(frames_folder)):
        fpath = os.path.join(frames_folder, frame)

        try:
            detections = _ocr.readtext(fpath)

            frame_texts = [d[1] for d in detections]  # (bbox, text, confidence)
            results.append({
                "frame": frame,
                "text": frame_texts
            })

        except Exception:
            continue

    return results
