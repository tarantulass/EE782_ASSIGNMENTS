from ollama import chat
from ollama import ChatResponse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils.logsetup import get_logger
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def summarygenerator()->str:
    logger = get_logger("telegramchat")
    logger.info(f"Using model: {config.MODEL_NAME}")

    try:
        response: ChatResponse = chat(model=config.MODEL_NAME, messages=[
            {
                'role': 'user',
                'content': 'Summarize the entire conversation in less than 150 words.',
            },
            ])
        logger.info(response['message']['content'])


        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        message = response['message']['content']

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}

        chat = requests.post(url, data=payload)
        logger.info(chat.json())


    except Exception as e:
        logger.error(f"Error in ollama API: {e}")
        sys.exit(1)

    
if __name__ == "__main__":
    summarygenerator()