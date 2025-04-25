import os

import neo4j
from neo4j_graphrag.indexes import create_vector_index

# 3rd party libs
from dotenv import load_dotenv

from graphrag.shared.env import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    NEO4J_VECTOR_INDEX_NAME,
    VECTOR_DIMENSION,
)

driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

create_vector_index(
    driver,
    NEO4J_VECTOR_INDEX_NAME,
    label="Chunk",
    embedding_property="embedding",
    dimensions=VECTOR_DIMENSION,
    similarity_fn="cosine",
)