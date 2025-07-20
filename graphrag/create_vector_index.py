import os
# Auto-add project root to sys.path for direct script execution
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import neo4j
from neo4j_graphrag.indexes import create_vector_index

from graphrag.shared.env import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    NEO4J_VECTOR_INDEX_NAME,
    VECTOR_DIMENSION,
)

driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
print(f"Connecting to Neo4j at {NEO4J_URI} with user {NEO4J_USERNAME} and password {NEO4J_PASSWORD}.")
create_vector_index(
    driver,
    NEO4J_VECTOR_INDEX_NAME,
    label="Chunk",
    embedding_property="embedding",
    dimensions=VECTOR_DIMENSION,
    similarity_fn="cosine",
)