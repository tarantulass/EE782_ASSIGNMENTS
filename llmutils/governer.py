from ollama import chat
from ollama import ChatResponse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils.logsetup import get_logger

def instructiongenerator()->str:
    logger = get_logger("governer")
    logger.info(f"Using model: {config.MODEL_NAME}")

    try:
        response: ChatResponse = chat(model=config.MODEL_NAME, messages=[
            {
                'role': 'user',
                'content': 'Why is the sky blue?',
            },
            ],
            max_tokens=100
            )
        logger.info(response['message']['content'])

    except Exception as e:
        logger.error(f"Error in ollama API: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    instructiongenerator()