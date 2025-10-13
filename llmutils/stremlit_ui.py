import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings
import numpy as np
import av
import requests
from ollama import chat, ChatResponse
import config
from utils.logsetup import get_logger
from utils.structuredoutputs import InstructionOutput  

logger = get_logger("StreamlitUI")

# --- Gemini Speech-to-Text Helper ---
def transcribe_audio(file_path: str) -> str:
    """
    Sends audio file to Gemini API and returns transcription.
    """
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        response = requests.post(
            "https://api.gemini.com/speech-to-text",
            headers={"Authorization": f"Bearer {config.GEMINI_API_KEY}"},
            files={"file": audio_bytes},
        )
        response.raise_for_status()
        return response.json().get("transcription", "")
    except Exception as e:
        logger.error(f"STT Error: {e}")
        return ""

# --- Audio Processor for Streamlit WebRTC ---
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_buffer = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Collect raw audio samples
        array = frame.to_ndarray()
        self.audio_buffer.append(array)
        return frame

# --- Streamlit App ---
st.set_page_config(page_title="Granite Chatbot", layout="wide")
st.title("Granite/Gemma Conversation Bot with Recording")

# Conversation history stored in session
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.header("🎤 Record Your Voice")
webrtc_ctx = webrtc_streamer(key="speech", audio_processor_factory=AudioProcessor)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Stop & Transcribe"):
        if webrtc_ctx.audio_processor:
            processor = webrtc_ctx.audio_processor
            # Combine audio chunks
            audio_data = np.concatenate(processor.audio_buffer, axis=1)
            tmp_file = "speech/input.wav"
            # Save as WAV for Gemini API
            import soundfile as sf
            sf.write(tmp_file, audio_data.T, 44100)
            st.success("Audio recorded!")
            transcription = transcribe_audio(tmp_file)
            st.text_area("You said:", value=transcription, height=100)
            st.session_state.conversation.append({"role": "user", "content": transcription})
            # Clear buffer
            processor.audio_buffer.clear()

with col2:
    if st.button("Clear Conversation"):
        st.session_state.conversation = []
        st.success("Conversation cleared!")

st.header("🤖 Bot Response")
if st.session_state.conversation:
    try:
        system_prompt = {
            "role": "system",
            "content": (
                "You are a conversation assistant. "
                "Summarize the conversation and generate the next escalation prompt. "
                "Return JSON like {\"summary\": ..., \"next_prompt\": ...}"
            )
        }
        response: ChatResponse = chat(
            model=config.MODEL_NAME,
            messages=[system_prompt] + st.session_state.conversation
        )

        import json
        bot_output_json = json.loads(response.message.content)
        structured_output = InstructionOutput(**bot_output_json)
        st.subheader("Summary")
        st.write(structured_output.summary)
        st.subheader("Next Prompt")
        st.write(structured_output.next_prompt)

        # Add bot reply to conversation
        st.session_state.conversation.append(
            {"role": "assistant", "content": structured_output.next_prompt}
        )

    except Exception as e:
        logger.error(f"Bot Error: {e}")
        st.error(f"Error generating bot response: {e}")
