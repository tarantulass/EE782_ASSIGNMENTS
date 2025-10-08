from transformers import pipeline
import pyttsx3
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

generator = pipeline("text-generation", model=config.MODEL_NAME)

tts = pyttsx3.init()

def intruder_dialogue(level:int, intruder_name:str=None):
    """
    level: escalation level (1, 2, 3)
    intruder_name: optional, if you want to include in prompt
    """
    
    # ----------------------
    # 1️⃣ Build the prompt
    # ----------------------
    # TODO: Customize the prompt based on your escalation logic
    prompt = f"""
    You are an AI guard in a hostel room.
    An unrecognized person has entered.
    Escalation level: {level}
    
    # TODO: Add your desired instructions / response format here
    """
    
    # ----------------------
    # 2️⃣ Generate text response from LLM
    # ----------------------
    output = generator(prompt, max_length=100)
    response_text = output[0]['generated_text']
    
    # ----------------------
    # 3️⃣ Convert text to speech
    # ----------------------
    tts.say(response_text)
    tts.runAndWait()
    
    return response_text  # Optional: return text for logging

# ----------------------
# Example usage
# ----------------------
if __name__ == "__main__":
    level = 1  # Example escalation
    intruder_name = None
    text = intruder_dialogue(level, intruder_name)
    print("Bot said:", text)
