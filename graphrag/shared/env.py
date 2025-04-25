import os
from dotenv import load_dotenv
load_dotenv(".env.azure")

AZURE_INFERENCE_ENDPOINT = os.environ["AZURE_INFERENCE_ENDPOINT"]
AZURE_INFERENCE_CREDENTIAL = os.environ["AZURE_INFERENCE_CREDENTIAL"]
AZURE_MODEL_NAME = os.environ["AZURE_MODEL_NAME"]

# Load environment variables from .env file
load_dotenv(".env")

# Neo4j db infos
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")
NEO4J_VECTOR_INDEX_NAME = "vectorIndex"
VECTOR_DIMENSION = 768