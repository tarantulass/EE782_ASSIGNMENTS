import cv2
import os, sys
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from deepface import DeepFace
from utils.logsetup import get_logger

logger = get_logger(__name__)  

def facerecognition(image_path: str, db_dir: str, threshold: float = 0.1) -> bool:
    if not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        logger.warning("File not supported.")
        return False

    for f in os.listdir(db_dir):
        db_image_path = os.path.join(db_dir, f)
        if os.path.isfile(db_image_path):
            try:
                result = DeepFace.verify(
                    img1_path=image_path,
                    img2_path=db_image_path,
                    model_name='VGG-Face',
                    detector_backend='opencv',
                    distance_metric='cosine',
                    enforce_detection=False
                )
                logger.info(f"Comparing with {f}: distance {result['distance']}, verified {result['verified']}")
                if result['distance'] < threshold or result['verified']:
                    return True
            except Exception as e:
                logger.error(f"Error verifying {f}: {e}")
    return False


def capture_and_recognize(db_dir: str, threshold: float = 0.1):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Cannot access webcam.")
        return False

    logger.info("Press 'q' to capture and recognize.")
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
            result = facerecognition(temp_path, db_dir, threshold=threshold)
            os.remove(temp_path)
            logger.info(f"Face recognition result: {result}")

            cap.release()
            cv2.destroyAllWindows()
            return result


if __name__ == "__main__":
    result = capture_and_recognize(config.DB_DIR, threshold=0.4)
    print(f"Face recognized: {result}")
