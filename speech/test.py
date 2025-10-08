import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

def recordAudio():

    print("Recording... Press Ctrl+C to stop.")
    frames = []

    try:
        while True:
            data = sd.rec(int(0.5 * config.SAMPLING_RATE), samplerate=config.SAMPLING_RATE, channels=1)
            sd.wait()
            frames.append(data)
    except KeyboardInterrupt:
        print("Stopped recording.")

    audio = np.concatenate(frames, axis=0)
    write(config.AUDIO_DIR, config.SAMPLING_RATE, audio)
    print("Saved as input.wav")

if __name__ == "__main__":
    recordAudio()