"""This example illustrates how to get started easily with the SimpleKGPipeline
and ingest text into a Neo4j Knowledge Graph.

This example assumes a Neo4j db is up and running. Update the credentials below
if needed.

NB: when building a KG from text, no 'Document' node is created in the Knowledge Graph.
"""

# builtin libs
import asyncio
import logging
import os

# graphrag libs
import neo4j
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.pipeline.pipeline import PipelineResult
from neo4j_graphrag.llm import LLMInterface
from neo4j_graphrag.embeddings import OllamaEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.llm import OllamaLLM

from neo4j_graphrag.experimental.components.pdf_loader import PdfLoader
from graphrag.document_sources.wikipedia import WikiLoader
from typing import Any


# 3rd party libs
from dotenv import load_dotenv

# local libs
from graphrag.data_model import ENTITIES, RELATIONS, POTENTIAL_SCHEMA
from graphrag.azure_llm import CustomLLM

# Load environment variables from .env file
load_dotenv(".env")

logging.basicConfig()
logging.getLogger("neo4j_graphrag").setLevel(logging.DEBUG)
# logging.getLogger("neo4j_graphrag").setLevel(logging.INFO)


# Neo4j db infos
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USERNAME", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
DATABASE = "neo4j"

class CustomKGPipeline(SimpleKGPipeline):
    """
    Custom pipeline class to override the default behavior of the SimpleKGPipeline.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runner = None

    async def run_async(self, user_input: dict[str, Any]) -> PipelineResult:
        """
        Run the pipeline with the given text.
        """
        return await self.runner.run(user_input)
    

# Text to process
TEXT = """The son of Duke Leto Atreides and the Lady Jessica, Paul is the heir of House Atreides,
an aristocratic family that rules the planet Caladan, the rainy planet, since 10191."""

def define_pipeline(
) -> CustomKGPipeline :
    llm : LLMInterface = OllamaLLM(
        model_name=os.getenv("KG_BUILDER_LLM_MODEL_NAME"),
        model_params={
            "max_tokens": 2000,
            "response_format": {"type": "json_object"},
        },
    )
    
    neo4j_driver : neo4j.Driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
    
    # Create an instance of the CustomKGPipeline
    kg_builder = CustomKGPipeline(
        llm=CustomLLM(""),
        driver=neo4j_driver,
        embedder=OllamaEmbeddings(model=os.getenv("KG_BUILDER_EMBEDDING_MODEL_NAME")),
        entities=ENTITIES,
        relations=RELATIONS,
        potential_schema=POTENTIAL_SCHEMA,
        from_pdf=True,
        neo4j_database=DATABASE,
        pdf_loader=WikiLoader(),
    )

    return kg_builder, neo4j_driver


async def run_pipeline(
    kg_builder: CustomKGPipeline,
    user_input: dict[str, Any],
) -> PipelineResult:
    """
    Run the pipeline with the given text."
    """
    # Create an instance of the CustomKGPipeline
    return await kg_builder.run_async(user_input=user_input)


async def main() -> PipelineResult:
    kg_builder, neo4j_driver = define_pipeline()
    res = await run_pipeline(kg_builder, TEXT)
    
    # Close the Neo4j driver
    await kg_builder.runner.close()
    neo4j_driver.close()
    return res


async def build_kg_from_text(
    text: str = TEXT,
) -> None:
    """
    Build a KG from the given text.
    """
    kg_builder, neo4j_driver = define_pipeline()
    res = await run_pipeline(kg_builder, {"text": text})
    
    # Close the Neo4j driver
    await kg_builder.runner.close()
    neo4j_driver.close()
    return res

async def build_kg_from_text(
    
) -> None:
    """
    Build a KG from the given text.
    """
    kg_builder, neo4j_driver = define_pipeline()
    res = await run_pipeline(kg_builder, {"text": text})
    
    # Close the Neo4j driver
    await kg_builder.runner.close()
    neo4j_driver.close()
    return res

if __name__ == "__main__":
    res = asyncio.run(main())
    print(res)









