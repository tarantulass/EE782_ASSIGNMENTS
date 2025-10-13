## Instructions to run the code
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip: deepface, pyttsx3
4. Set up environment variables for TELEGRAM_BOT_TOKEN and CHAT_ID in a .env file.
5. Download the quantized "granite3.1-moe:3b" model from ollama
6. Generate the gemini api key from ai-studio and add it in .env file. (create a .env as it has api keys)
7. Run the main.py file to start the application.

## Problems and solutions
1. Face recognition using face_recognition was extremely problematic due to cmake and dlib dependecies conflict. Switched to deepface for better accuracy and simpler implmentation - further optimized by reducing the dimensions, using other models and .find function instead.
2. Pinecone integration for vector database was complex and time-consuming initially, can be easily extended for images as the code is modular.
3. LLM model selection was challenging due to the variety of models available. Chose granite3.1-moe:3b based on Openllm leaderboard.
4. `pyttsx3` throws `AttributeError: 'NoneType' object has no attribute 'suppress'` at program exit, and sometimes speech doesn’t play. Actually the engine’s internal driver is cleaned up too late or improperly, and `runAndWait()` may not complete before exit. Solution: Call `tts.stop()` and `del tts` after speaking, or initialize the engine locally to ensure proper cleanup and reliable speech.


## References 

1. Indently.io and sefik llkin serengil for face recognition programs
2. Openllm leaderboard for LLM model selection
3. Telegram bot API documentation for sending messages via bot
4. DeepFace documentation for face recognition - dropped later due to inconsistent results.
5. Pinecone documentation for vector database - dropped later due to time constraints. (Idea was to develop a more robust face recognition system using vector embeddings and similarity search)