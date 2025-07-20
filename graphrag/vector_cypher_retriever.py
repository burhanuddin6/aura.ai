"""This example uses an example Movie database where movies' plots are embedded
using OpenAI embeddings. OPENAI_API_KEY needs to be set in the environment for
this example to run.

Also requires minimal Cypher knowledge to write the retrieval query.

It shows how to use a vector-cypher retriever to find context
similar to a query **text** using vector similarity + graph traversal.
"""
# Auto-add project root to sys.path for direct script execution
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import os

import neo4j
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.types import RetrieverResult
from neo4j_graphrag.embeddings import OllamaEmbeddings

from graphrag.shared.env import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    NEO4J_VECTOR_INDEX_NAME,
    VECTOR_DIMENSION,
    DATABASE,
    KG_BUILDER_EMBEDDING_MODEL_NAME,
)

RETRIEVAL_QUERY = """
MATCH(n) RETURN n.text;
"""

with neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
    # Initialize the retriever
    retriever = VectorCypherRetriever(
        driver=driver,
        index_name=NEO4J_VECTOR_INDEX_NAME,
        embedder=OllamaEmbeddings(model=KG_BUILDER_EMBEDDING_MODEL_NAME),
        retrieval_query=RETRIEVAL_QUERY,
        neo4j_database=DATABASE,
    )

    if __name__ == "__main__":
        # Perform the similarity search for a text query
        # (retrieve the top 5 most similar nodes)
        query_text = "How can I use barcode detection in ARKit to decode barcodes"
        # print(retriever.search(query_text=query_text, top_k=1))
        result : RetrieverResult = retriever.search(query_text=query_text, top_k=1)
        for a in result:
            print(a)