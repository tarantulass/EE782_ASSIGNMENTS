## Global configuration
import os

SAMPLING_RATE = 16000
PIC_RATE = 2 # frames per second
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "speech", "input.wav")  
ACTIVATION_PHRASE = "guard my room"
WEBCAM_DIR = os.path.join(os.path.dirname(__file__), "facerecognition", "frames")   
DB_DIR = os.path.join(os.path.dirname(__file__), "facerecognition", "DBface", "registered")

MODEL_NAME = "granite3.1-moe:3b"
