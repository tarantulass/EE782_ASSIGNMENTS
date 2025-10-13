from deepface import DeepFace
# from deepface.basemodels import VGGFace
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logsetup import get_logger


def facerecognition(image: str, db_dir: str) -> bool:
    logger = get_logger(__name__)

    try:
      df = DeepFace.find(img_path = image, db_path = db_dir, model_name = 'VGG-Face', detector_backend='opencv',distance_metric = 'cosine',enforce_detection=False)
      logger.info(df.head())
    except Exception as e:
      logger.error(f"Error encountered: {e}")


if __name__ == "__main__":
    facerecognition("test1.webp", "./facerecognition/DBface/registered")  
