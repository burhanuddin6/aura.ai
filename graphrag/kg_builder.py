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

# local libs
from graphrag.data_model import ENTITIES, RELATIONS, POTENTIAL_SCHEMA
from graphrag.azure_llm import CustomLLM
from graphrag.shared.env import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)

logging.basicConfig()
logging.getLogger("neo4j_graphrag").setLevel(logging.DEBUG)
# logging.getLogger("neo4j_graphrag").setLevel(logging.INFO)


# Neo4j db infos
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)
DATABASE = "neo4j"

# Text to process
TEXT = """The son of Duke Leto Atreides and the Lady Jessica, Paul is the heir of House Atreides,
an aristocratic family that rules the planet Caladan, the rainy planet, since 10191."""

def define_pipeline(from_pdf: bool = False) -> SimpleKGPipeline:
    llm : LLMInterface = OllamaLLM(
        model_name=os.getenv("KG_BUILDER_LLM_MODEL_NAME"),
        model_params={
            "max_tokens": 2000,
            "response_format": {"type": "json_object"},
        },
    )
    
    neo4j_driver : neo4j.Driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    
    # Create an instance of the SimpleKGPipeline
    kg_builder = SimpleKGPipeline(
        llm=CustomLLM(""),
        driver=neo4j_driver,
        embedder=OllamaEmbeddings(model=os.getenv("KG_BUILDER_EMBEDDING_MODEL_NAME")),
        entities=ENTITIES,
        relations=RELATIONS,
        potential_schema=POTENTIAL_SCHEMA,
        from_pdf=from_pdf,
        neo4j_database=DATABASE,
        pdf_loader=PdfLoader() if from_pdf else None,
    )

    return kg_builder, neo4j_driver


async def run_pipeline(
    kg_builder: SimpleKGPipeline,
    text: str = TEXT,
    file_path: str = None,
) -> PipelineResult:
    """
    Run the pipeline with the given text."
    """
    # Create an instance of the SimpleKGPipeline
    if file_path:
        return await kg_builder.run_async(file_path=file_path)
    return await kg_builder.run_async(text=text)



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
    res = await run_pipeline(kg_builder, text=text)
    
    # Close the Neo4j driver
    await kg_builder.runner.close()
    neo4j_driver.close()
    return res

async def build_kg_from_pdf(
    file_path: str = "graphrag/Apple_Vision_Pro_Privacy_Overview.pdf",
) -> None:
    """
    Build a KG from the given text.
    """
    kg_builder, neo4j_driver = define_pipeline(from_pdf=True)
    res = await run_pipeline(kg_builder, file_path=file_path)
    
    # Close the Neo4j driver
    await kg_builder.runner.close()
    neo4j_driver.close()
    return res


if __name__ == "__main__":
    res = asyncio.run(main())
    print(res)








