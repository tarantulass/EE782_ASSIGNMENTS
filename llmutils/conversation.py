import pyttsx3
from ollama import chat
from ollama import ChatResponse
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from speech.test import recordAudio

from utils.logsetup import get_logger
from prompts.buildintruderprompt import buildintruderprompt
tts = pyttsx3.init()



from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai


def intruder_dialogue(level:int, text:str=None):

    logger = get_logger("intruder_dialogue")


    try:
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
    except Exception as e:
        logger.error(f"Error configuring Gemini API: {e}")
        sys.exit(1)

    recordAudio()
    audio_file = genai.upload_file(path=config.AUDIO_DIR)
    logger.info(f"Successfully uploaded file: {audio_file.display_name}")

    # 2. Create an instance of the Gemini 2.5 Model.
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    # 3. Sending a prompt along with the uploaded audio file to the model.
    logger.info("Sending file to model for transcription...")
    response = model.generate_content([
        "Transcribe this audio file.",  
        audio_file
    ])

    text = response.text

    prompt = buildintruderprompt(level, text)

    try:
        response: ChatResponse = chat(model=config.MODEL_NAME, messages=[
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

    tts.say(output)
    tts.runAndWait()

    return output

if __name__ == "__main__":
    level = 1  
    intruder_name = None
    text = intruder_dialogue(level, intruder_name)
