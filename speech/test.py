import json
import sys
import pyaudio
from vosk import Model, KaldiRecognizer

# Download a Vosk model from https://alphacephei.com/vosk/models
# For example, vosk-model-small-en-us-0.15 (small English model)
# Extract it to a folder, e.g., 'model' directory in your working directory

if len(sys.argv) != 2:
    print("Usage: python3 demo.py <model_path>")
    print("Example: python3 demo.py ./model")
    sys.exit(1)

model_path = sys.argv[1]
if not os.path.exists(model_path):
    print(f"Please download a model to {model_path}")
    print("You can download small-en-us model from https://alphacephei.com/vosk/models")
    sys.exit(1)

model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Listening... Speak into the microphone. Press Ctrl+C to stop.")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print(f"Recognized: {result.get('text', '')}")
        else:
            partial = json.loads(rec.PartialResult())
            if partial.get('partial', ''):
                print(f"Partial: {partial.get('partial', '')}", end='', flush=True)
                # Clear partial on next iteration (you can add \r for overwrite)
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()