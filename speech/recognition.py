from pinecone import Pinecone, ServerlessSpec

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from utils.logsetup import get_logger
import config

def recognize_speech(file_path: str) -> bool:
    try:
        pc = Pinecone(api_key=config.PINECONE_API_KEY)

    except Exception as e:
        logger = get_logger("speech_recognition")
        logger.error(f"Error initializing Pinecone: {e}")
        sys.exit(1)