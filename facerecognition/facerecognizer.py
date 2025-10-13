import facerecognition
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logsetup import get_logger
import config

# def facerecognition(image: str, db_dir: str) -> bool:
#     logger = get_logger(__name__)

#     try:
#       df = DeepFace.find(img_path = image, db_path = db_dir, model_name = 'VGG-Face', detector_backend='opencv',distance_metric = 'cosine',enforce_detection=False)
#       logger.info(df.head())
#     except Exception as e:
#       logger.error(f"Error encountered: {e}")

def encode_faces():
    logger = get_logger("faceencoder")

    for image in os.listdir(config.DB_DIR):
        try:
            img_path = os.path.join(config.DB_DIR, image)
            face_image = facerecognition.load_image_file(img_path)
            embedding = facerecognition.get_face_embedding(face_image)
            logger.info(f"Encoded {image}: {embedding}")
        except Exception as e:
            logger.error(f"Error encoding {image}: {e}")

def facerecognition(image: str, db_dir: str) -> bool:
    logger = get_logger("facerecognizer")
    
    try:

    except Exception as e:

if __name__ == "__main__":
    facerecognition("test1.webp", "./facerecognition/DBface/registered")  
    facerecognition("test2.jpeg", "./facerecognition/DBface/registered")  