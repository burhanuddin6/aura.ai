import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

# Load environment variables from a .env file
load_dotenv()

# Get the model name from the environment variable, with a default fallback
model_name = os.getenv("LLM_MODEL_NAME")
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")

llm = ChatOllama(
    model=model_name,
)

emb_model = OllamaEmbeddings(
    model="deepseek-r1:7b",
)
r1 = emb_model.embed_documents(
    [
        "Alpha is the first letter of Greek alphabet",
        "Beta is the second letter of Greek alphabet",
    ]
)
r2 = emb_model.embed_query(
    "What is the second letter of Greek alphabet"
)

