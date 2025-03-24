import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load environment variables from a .env file
load_dotenv()

# Get the model name from the environment variable, with a default fallback
model_name = os.getenv("LLM_MODEL_NAME")

llm = ChatOllama(
    model=model_name,
)