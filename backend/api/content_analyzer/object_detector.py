import os
import super_gradients as super_gradients
from super_gradients.training import models
from super_gradients.common.object_names import Models


# Load YOLO-NAS small for CPU inference
_yolo = models.get(Models.YOLO_NAS_S, pretrained_weights="coco")


def detect_objects_yolo_cpu(frames_folder: str):
    """
    Detect common objects in frames using YOLO-NAS (CPU safe).
    Returns a list of dicts: [{frame: "frame_0.jpg", objects: [...]}, ...]
    """

    if not os.path.exists(frames_folder):
        return []

    results = []

    for frame in sorted(os.listdir(frames_folder)):
        fpath = os.path.join(frames_folder, frame)

        try:
            preds = _yolo.predict(fpath).prediction

            objects = []
            for label, conf, box in zip(
                preds.class_names,
                preds.confidence,
                preds.bboxes_xyxy
            ):
                objects.append({
                    "label": label,
                    "confidence": float(conf)
                })

            results.append({
                "frame": frame,
                "objects": objects
            })

        except Exception:
            # skip corrupt frames
            continue

    return results




