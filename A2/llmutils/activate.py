import os
import sys
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logsetup import get_logger
import config
from dotenv import load_dotenv

import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

try:
    genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    sys.exit(1)


def activation(LOG_NAME: str = "activate")->bool:
   
    logger = get_logger(LOG_NAME)
    
    try:
        logger.info(f"Uploading audio file: {config.AUDIO_DIR}")
        
        # 1. Upload the audio file to the Gemini API.
        # This returns a File object that we can reference.
        audio_file = genai.upload_file(path=config.AUDIO_DIR)
        logger.info(f"Successfully uploaded file: {audio_file.display_name}")

        # 2. Create an instance of the Gemini 2.5 Model.
        # 'gemini-2.5-flash' is faster and more cost-effective for tasks like this.
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")

        # 3. Sending a prompt along with the uploaded audio file to the model.
        logger.info("Sending file to model for transcription...")
        response = model.generate_content([
            "Transcribe this audio file.",  
            audio_file
        ])

        text = response.text
        logger.debug(f"Transcription result: {text}")
        if config.ACTIVATION_PHRASE.lower() in text.lower():
            logger.info("Activation phrase detected!")
            return True
        else:
            logger.info("Activation phrase not detected.")
            return False

    except FileNotFoundError:
        logger.error(f"Audio file not found at path: {config.AUDIO_DIR}")
    except Exception as e:
        logger.error(f"An error occurred during transcription: {e}")


if __name__ == "__main__":
    activation()