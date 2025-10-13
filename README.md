## Instructions to run the code
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip:
4. Set up environment variables for TELEGRAM_BOT_TOKEN and CHAT_ID in a .env file.
5. Run the main.py file to start the application.

## Problems and solutions
1. Face recognition using DeepFace was inconsistent and unreliable. Switched to face_recognition library for better accuracy.
2. Pinecone integration for vector database was complex and time-consuming. Dropped due to time constraints.
3. LLM model selection was challenging due to the variety of models available. Chose granite3.1-moe:3b based on Openllm leaderboard.
4. 

## References 

1. Indently.io for face recognition programs
2. Openllm leaderboard for LLM model selection
3. Telegram bot API documentation for sending messages via bot
4. DeepFace documentation for face recognition - dropped later due to inconsistent results.
5. Pinecone documentation for vector database - dropped later due to time constraints. (Idea was to develop a more robust face recognition system using vector embeddings and similarity search)