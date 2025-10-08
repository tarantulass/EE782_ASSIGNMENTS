from openai import OpenAI
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config
from dotenv import load_dotenv
load_dotenv()

def activation():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    audio_file = open(config.AUDIO_DIR, "rb")

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-transcribe", 
        file=audio_file, 
        response_format="text"
    )

    logger.debug(transcription.text)

    