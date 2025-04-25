from __future__ import annotations

import asyncio
import logging

import neo4j
from neo4j_graphrag.experimental.components.entity_relation_extractor import (
    LLMEntityRelationExtractor,
    OnError,
)
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.experimental.components.pdf_loader import PdfLoader
from neo4j_graphrag.experimental.components.schema import (
    SchemaBuilder,
)
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import (
    FixedSizeSplitter,
)
from neo4j_graphrag.experimental.pipeline.pipeline import PipelineResult
from neo4j_graphrag.llm import LLMInterface, OpenAILLM

logging.basicConfig(level=logging.INFO)

from graphrag.shared.env import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)
from graphrag.data_model import (
    ENTITIES,
    RELATIONS,
    POTENTIAL_SCHEMA,
)
from graphrag.azure_llm import CustomLLM

async def define_and_run_pipeline(
    neo4j_driver: neo4j.Driver, llm: LLMInterface
) -> PipelineResult:
    from neo4j_graphrag.experimental.pipeline import Pipeline

    # Set up the pipeline
    pipe = Pipeline()
    pipe.add_component(
        PdfLoader(),
        "pdf_loader",
    )
    pipe.add_component(
        FixedSizeSplitter(chunk_size=4000, chunk_overlap=200), "splitter"
    )
    pipe.add_component(SchemaBuilder(), "schema")
    pipe.add_component(
        LLMEntityRelationExtractor(
            llm=llm,
            on_error=OnError.RAISE,
        ),
        "extractor",
    )
    pipe.add_component(Neo4jWriter(neo4j_driver), "writer")
    pipe.connect("pdf_loader", "splitter", input_config={"text": "pdf_loader.text"})
    pipe.connect("splitter", "extractor", input_config={"chunks": "splitter"})
    pipe.connect(
        "schema",
        "extractor",
        input_config={
            "schema": "schema",
            "document_info": "pdf_loader.document_info",
        },
    )
    pipe.connect(
        "extractor",
        "writer",
        input_config={"graph": "extractor"},
    )

    pipe_inputs = {
        "pdf_loader": {
            "filepath": "graphrag/Apple_Vision_Pro_Privacy_Overview.pdf",
            "metadata": {
                "title": "Apple Vision Pro Privacy Overview",
                "author": "Apple Inc.",
                "language": "en",
                "version": "1.0",
                "description": "An overview of privacy features for Apple Vision Pro.",
            },
        },
        "schema": {
            "entities": ENTITIES,
            "relations": RELATIONS,
            "potential_schema": POTENTIAL_SCHEMA,
        },
    }
    return await pipe.run(pipe_inputs)


async def main() -> PipelineResult:
    llm = CustomLLM("")
    driver = neo4j.GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    res = await define_and_run_pipeline(driver, llm)
    driver.close()
    # await llm.async_client.close()
    return res


if __name__ == "__main__":
    res = asyncio.run(main())
    print(res)
