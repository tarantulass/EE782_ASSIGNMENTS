from deepface import DeepFace
# from deepface.basemodels import VGGFace
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logsetup import get_logger


def facerecognition(image: str, db_dir: str) -> bool:
    logger = get_logger(__name__)

    ## for speed up
    # files = [os.path.join(db_dir, f) for f in os.listdir(db_dir) if os.path.isfile(os.path.join(db_dir, f))]
    # for file in files:
    #     logger.info(f"Comparing with {file}")
    #     result = DeepFace.verify(image, file, model_name="Facenet", detector_backend="opencv", enforce_detection=False)
    #     logger.info(f"Face recognition result for {image}: {result}")
    #     if result["verified"]:
    #         return True
    # return False
    try:
      df = DeepFace.find(img_path = image, db_path = db_dir, model_name = 'VGG-Face', detector_backend='opencv',distance_metric = 'cosine',enforce_detection=False)
      logger.info(df.head())
    except Exception as e:
      logger.error(f"Error encountered: {e}")

if __name__ == "__main__":
    facerecognition("test1.webp", "./facerecognition/DBface/registered")  
    facerecognition("test2.jpeg", "./facerecognition/DBface/registered")  