import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llmutils.activate import activation
from speech.test import recordAudio
from utils.notify_cam import notify_cam

if __name__ == "__main__":
    recordAudio()
    status = activation()
    notify_cam(status)
    unknownface = True
    while unknownface:
    
    