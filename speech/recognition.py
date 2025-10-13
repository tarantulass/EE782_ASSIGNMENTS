import whisper

def recognize_speech(file_path: str) -> bool:

    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    print(result["text"])
    return True
