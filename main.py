import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llmutils.activate import activation
from speech.test import recordAudio
from utils.notify_cam import notify_cam
import config
from utils.logsetup import get_logger
from llmutils.conversation import intruder_dialogue
from llmutils.governer import instructiongenerator
from llmutils.telegramchat import summarygenerator
from facerecognition.facerecognizer import facerecognition

if __name__ == "__main__":
    logger = get_logger("main")

    recordAudio()
    status = activation()
    notify_cam(status)
    knownface = facerecognition(config.DB_DIR)
    with open(config.TEXT_FILE, 'w') as f:
        f.write("")

    while not knownface:
        logger.warning("Intruder detected!")
        intruder_dialogue(level=1)
        level = instructiongenerator(config.TEXT_FILE)
        if level == 3:
            break   

    if config.TEXT_FILE:    
        summarygenerator()
