"""This example uses an example Movie database where movies' plots are embedded
using OpenAI embeddings. OPENAI_API_KEY needs to be set in the environment for
this example to run.

Also requires minimal Cypher knowledge to write the retrieval query.

It shows how to use a vector-cypher retriever to find context
similar to a query **text** using vector similarity + graph traversal.
"""

import os

import neo4j
from neo4j_graphrag.retrievers import VectorCypherRetriever
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
MATCH (startNode {id: "1f83eb2c-addb-41ef-8a08-dd8e9bbb59fc"})  // your starting node

// Step 1: Traverse the chunk chain and collect text
MATCH (startNode)-[:NEXT_CHUNK*0..]-(chunk:Chunk)
WITH DISTINCT chunk
ORDER BY chunk.index

// Step 2: Concatenate text from all chunks
WITH reduce(fullText = '', c IN collect(chunk.text) | fullText + c) AS fullText, collect(chunk) AS chunks

// Step 3: Get non-Chunk neighbors for all chunks
UNWIND chunks AS chunk
OPTIONAL MATCH (chunk)--(neighbor)
WHERE NOT 'Chunk' IN labels(neighbor)

// Step 4: Collect non-Chunk neighbors
WITH fullText, collect(DISTINCT neighbor) AS nonChunkNeighbors
RETURN fullText, nonChunkNeighbors


"""

RETRIEVAL_QUERY = """
MATCH (n)
WHERE n.text IS NOT NULL
RETURN n.text;
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
        query_text = "What is Metal?"
        # print(retriever.search(query_text=query_text, top_k=1))
        print(str(retriever.search(query_text=query_text, top_k=1)))
