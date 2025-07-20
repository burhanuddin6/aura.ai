import os
from dotenv import load_dotenv
# if file exists

# print("Loading environment variables from .env file...")
if os.path.exists(".env.azure"):
    load_dotenv(".env.azure")
#     print("Loaded .env.azure")
# else:
#     print("No .env.azure file found, using system environment variables.")

AZURE_INFERENCE_ENDPOINT = os.environ["AZURE_INFERENCE_ENDPOINT"]
AZURE_INFERENCE_CREDENTIAL = os.environ["AZURE_INFERENCE_CREDENTIAL"]
AZURE_MODEL_NAME = os.environ["AZURE_MODEL_NAME"]

# Load environment variables from .env file
if os.path.exists(".env"):
    load_dotenv(".env")

# Neo4j db infos
NEO4J_URI = "neo4j+s://74e32ff9.databases.neo4j.io"
NEO4J_USERNAME = os.environ['NEO4J_USERNAME']
NEO4J_PASSWORD = os.environ['NEO4J_PASSWORD'] 
# NEO4J_URI = 'bolt://localhost:7687'
# NEO4J_USERNAME = 'neo4j'
# NEO4J_PASSWORD = '12345678'


NEO4J_VECTOR_INDEX_NAME = "vectorIndex"
VECTOR_DIMENSION = 768
DATABASE = "neo4j"

KG_BUILDER_LLM_MODEL_NAME = os.getenv("KG_BUILDER_LLM_MODEL_NAME", "llama3.1:8b")
KG_BUILDER_EMBEDDING_MODEL_NAME = os.getenv("KG_BUILDER_EMBEDDING_MODEL_NAME", "nomic-embed-text")