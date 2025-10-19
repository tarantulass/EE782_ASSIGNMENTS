import pyttsx3
from ollama import chat
from ollama import ChatResponse
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from speech.test import recordAudio

from utils.logsetup import get_logger
from prompts.buildintruderprompt import buildintruderprompt


from dotenv import load_dotenv
load_dotenv()
from google import genai


def intruder_dialogue(level:int, text:str=None):

    logger = get_logger("intruder_dialogue")


    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
    except Exception as e:
        logger.error(f"Error configuring Gemini API: {e}")
        sys.exit(1)

    recordAudio()
    audio_file = client.files.upload(path=config.AUDIO_DIR)
    logger.info(f"Successfully uploaded file: {audio_file.display_name}")


    # 3. Sending a prompt along with the uploaded audio file to the model.
    logger.info("Sending file to model for transcription...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = ["Transcribe this audio file.",  
        audio_file
    ])

    text = response.text
    logger.debug(f"Transcription result: {text}")
    
    prompt = buildintruderprompt(level, text)

    try:
        response: ChatResponse = chat(model=config.MODEL_NAME, messages=[
            {
                'role': 'system',
                'content': 'You are an AI guard in a hostel room.',
            },
            {
                'role': 'user',
                'content': prompt,
            },
            ])
        logger.info(response['message']['content'])

    except Exception as e:
        logger.error(f"Error in ollama API: {e}")
        sys.exit(1)


    output = response.message.content
    logger.info(f"Reply: {output}")

    with open(config.TEXT_FILE, 'a') as f:
        f.write(f"User: {text}\nAI: {output}\n")

    tts = pyttsx3.init()
    try:
        tts.say(output)
        tts.runAndWait()
    finally:
        tts.stop()
        del tts

    return output

if __name__ == "__main__":
    level = 1  
    intruder_name = None
    text = intruder_dialogue(level, intruder_name)
