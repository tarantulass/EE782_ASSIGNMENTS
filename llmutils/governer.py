from ollama import chat
from ollama import ChatResponse
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils.logsetup import get_logger
from prompts.judgeprompt import judgeprompt

def instructiongenerator(file: str)->str:
    logger = get_logger("governer")
    logger.info(f"Using model: {config.MODEL_NAME}")

    try:
        with open(file, 'r') as f:   
            text = f.read()
        prompt = judgeprompt(text)
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
    
if __name__ == "__main__":
    instructiongenerator()