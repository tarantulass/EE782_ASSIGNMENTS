import cv2
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from deepface import DeepFace
from utils.logsetup import get_logger
import tempfile

logger = get_logger(__name__)  

def facerecognition(image_path: str, db_dir: str) -> bool:

    if not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        logger.warning("File not supported. Only .jpg/.jpeg/.png allowed.")
        return False

    try:
        df = DeepFace.find(
            img_path=image_path,
            db_path=db_dir,
            model_name='VGG-Face',
            detector_backend='opencv',
            distance_metric='cosine',
            enforce_detection=False
        )
        logger.info(df.head())
        return not df.empty  # True if match found, else False
    except Exception as e:
        logger.error(f"Error encountered: {e}")
        return False

def capture_and_recognize(db_dir: str):
    """
    Captures a frame from webcam and performs face recognition.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Cannot access webcam.")
        return False

    logger.info("Press 'q' to capture and process the frame.")
    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to grab frame.")
            break

        cv2.imshow("Webcam - Press 'q' to capture", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                temp_path = tmpfile.name
                cv2.imwrite(temp_path, frame)
            logger.info(f"Captured image saved to {temp_path}")
            result = facerecognition(temp_path, db_dir)
            os.remove(temp_path)
            logger.info(f"Face recognition result: {result}")
            cap.release()
            cv2.destroyAllWindows()
            return result

if __name__ == "__main__":
    result = capture_and_recognize(config.DB_DIR)
    print(f"Face recognized: {result}")
