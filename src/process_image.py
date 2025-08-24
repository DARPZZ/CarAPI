import easyocr
import numpy as np
import src.numberplate_checks as numberplate_checks
import cv2
from ultralytics import YOLO

model_path = "src/models/AI/best.pt"
yolo_model = YOLO(model_path)
reader_da = easyocr.Reader(['da', 'en'], gpu=False)
confidence_threshold = 0.2

def get_numberplate_info(cropped_plate_img):
    plate_array = []
    """
    Takes a cropped plate image as a numpy array (BGR or RGB),
    runs OCR, filters by confidence, and validates Danish number plates.
    Returns the detected plate as a string or None.
    """
    img_rgb = cv2.cvtColor(cropped_plate_img, cv2.COLOR_BGR2GRAY)

    results_with_details = reader_da.readtext(img_rgb, detail=1, paragraph=False)
    
    confident_results = []
    for (bbox, text, confidence) in results_with_details:
        if confidence >= confidence_threshold:
            confident_results.append(text)
    
    for element in confident_results:
        plate_array.append(element)
    for numberplate in plate_array:
        numberplate_lenght = len(numberplate)
        if(numberplate_lenght > 6 and numberplate_lenght < 10):
            return numberplate_checks.numberplate_check(numberplate)

def load_image(nummerplade):
    """
    Loads an image from either:
    - A file path (string)
    - A file-like object (e.g. FastAPI UploadFile)
    Returns an RGB numpy array.
    """
    if isinstance(nummerplade, str):  
        img = cv2.imread(nummerplade)
        if img is None:
            raise ValueError(f"[ERROR] Could not load image from path: {nummerplade}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    elif hasattr(nummerplade, "read"):  
        file_bytes = np.frombuffer(nummerplade.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("[ERROR] Could not decode uploaded image")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    else:
        raise TypeError("[ERROR] Unsupported input type for load_image()")


def test(nummerplade):
    try:
        print(f"[INFO] Successfully loaded model from: {model_path}")
    except Exception as e:
        print(e)

    img_rgb = load_image(nummerplade)
    results = yolo_model.predict(img_rgb, conf=0.3, iou=0.4, verbose=True)

    if not results or len(results[0].boxes) == 0:
        print("[WARNING] No detections found.")
        return None

    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    detected_plates = []
    for i, result in enumerate(results):
        boxes = result.boxes
        for j in range(len(boxes)):
            coords = boxes.xyxy[j].tolist()
            x1, y1, x2, y2 = map(int, coords)
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(img_bgr.shape[1], x2), min(img_bgr.shape[0], y2)

            cropped_plate = img_bgr[y1:y2, x1:x2]
            if cropped_plate.size == 0:
                continue

            plate_text = get_numberplate_info(cropped_plate)
            if plate_text:
                detected_plates.append(plate_text)

    if detected_plates:
        print("[INFO] Detected number plates:", detected_plates)
        return detected_plates
    else:
        print("[WARNING] No valid number plates found.")
        return None