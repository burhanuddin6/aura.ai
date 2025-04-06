import os

import neo4j
from neo4j_graphrag.indexes import create_vector_index

# 3rd party libs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j db infos
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USERNAME", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
INDEX_NAME = "vectorIndex"
DIMENSION = 768

driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)

create_vector_index(
    driver,
    INDEX_NAME,
    label="Chunk",
    embedding_property="embedding",
    dimensions=DIMENSION,
    similarity_fn="euclidean",
)