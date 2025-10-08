import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logsetup import get_logger
import requests
from dotenv import load_dotenv
load_dotenv()
import cv2
import config

def notify_cam(activation: bool, LOG_NAME: str = "notify_cam"):
    logger = get_logger(LOG_NAME)

    if activation:
        logger.info("Activation phrase detected! Notifying camera...")

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        message = "Hello the guard bot is activated!"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}

        response = requests.post(url, data=payload)
        logger.info(response.json())

        logger.info("Camera notified to start recording.")
        logger.info("Starting webcam...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Cannot open webcam")
            return

        ret, frame = cap.read()
        frame_path = os.path.join(config.WEBCAM_DIR, "first_frame.jpg")  
        if ret:
            logger.info("Webcam activated successfully. Captured one frame for now.")
            cv2.imwrite(frame_path, frame)

    else:
        logger.info("No activation phrase detected. Camera remains idle.")