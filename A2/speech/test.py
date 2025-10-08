import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config
from pynput import keyboard
from utils.logsetup import get_logger

def recordAudio():
    logger = get_logger("recordAudio")
    logger.info("Recording... Press Ctrl+C to stop.")
    frames = []

    try:
        while True:
            data = sd.rec(int(0.5 * config.SAMPLING_RATE), samplerate=config.SAMPLING_RATE, channels=1)
            sd.wait()
            frames.append(data)
    except KeyboardInterrupt:
        logger.info("Stopped recording.")

    audio = np.concatenate(frames, axis=0)
    write(config.AUDIO_DIR, config.SAMPLING_RATE, audio)
    logger.info("Saved as input.wav")

if __name__ == "__main__":
    recordAudio()