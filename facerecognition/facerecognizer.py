from deepface import DeepFace
import cv2
from utils.logsetup import get_logger


def facerecognition(image: str, db_dir: str) -> bool:
    logger = get_logger(__name__)

    for file in db_dir:
        logger.info(f"Comparing with {file}")
        result = DeepFace.verify(image, file, model_name="Facenet", detector_backend="opencv", enforce_detection=False)
        logger.info(f"Face recognition result for {image}: {result}")
        if result["verified"]:
            return True
    return False

if __name__ == "__main__":
    facerecognition("img1.jpg", "./facerecognition/DBface")  