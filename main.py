import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llmutils.activate import activation
from speech.test import recordAudio
from utils.notify_cam import notify_cam
from facerecognition import facerecognizer
import config
from utils.logsetup import get_logger

if __name__ == "__main__":
    logger = get_logger("main")

    recordAudio()
    status = activation()
    notify_cam(status)

    while unknownface:
        unknownface = facerecognizer(img, config.DB_DIR)
        
    
