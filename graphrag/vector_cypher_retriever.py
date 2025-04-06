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

# 3rd party libs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define database credentials
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USERNAME", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
DATABASE = "neo4j"
INDEX_NAME = "vectorIndex"

# for each Movie node matched by the vector search, retrieve more context:
# the name of all actors starring in that movie
# RETRIEVAL_QUERY = """
# RETURN  node.title as movieTitle,
#         node.plot as moviePlot,
#         collect { MATCH (actor:Actor)-[:ACTED_IN]->(node) RETURN actor.name } AS actors,
#         score as similarityScore
# """

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

# RETRIEVAL_QUERY = """
# RETURN node;
# """

with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
    # Initialize the retriever
    retriever = VectorCypherRetriever(
        driver=driver,
        index_name=INDEX_NAME,
        # note: embedder is optional if you only use query_vector
        embedder=OllamaEmbeddings(model=os.getenv("KG_BUILDER_EMBEDDING_MODEL_NAME")),
        retrieval_query=RETRIEVAL_QUERY,
        # optionally, configure how to format the results
        # (see corresponding example in 'customize' directory)
        # result_formatter=None,
        # optionally, set neo4j database
        neo4j_database=DATABASE,
    )

    # Perform the similarity search for a text query
    # (retrieve the top 5 most similar nodes)
    query_text = "How can I build apps for the VisionPro using iOS?"
    print(retriever.search(query_text=query_text, top_k=5))

    # note: it is also possible to query from a query_vector directly:
    # query_vector: list[float] = [...]
    # retriever.search(query_vector=query_vector, top_k=5)
