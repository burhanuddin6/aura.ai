#  Copyright (c) "Neo4j"
#  Neo4j Sweden AB [https://neo4j.com]
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      https://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

## *********************************************
# WARNING: this example is linked from the doc
# page do not delete until the docs are updated
## **********************************************

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
    SchemaEntity,
    SchemaRelation,
)
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import (
    FixedSizeSplitter,
)
from neo4j_graphrag.experimental.pipeline.pipeline import PipelineResult
from neo4j_graphrag.llm import LLMInterface, OpenAILLM
from graphrag.shared.env import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)

logging.basicConfig(level=logging.INFO)


async def define_and_run_pipeline(
    neo4j_driver: neo4j.Driver, llm: LLMInterface
) -> PipelineResult:
    from neo4j_graphrag.experimental.pipeline import Pipeline

    # Instantiate Entity and Relation objects
    entities = [
        SchemaEntity(label="PERSON", description="An individual human being."),
        SchemaEntity(
            label="ORGANIZATION",
            description="A structured group of people with a common purpose.",
        ),
        SchemaEntity(label="LOCATION", description="A location or place."),
        SchemaEntity(
            label="HORCRUX",
            description="A magical item in the Harry Potter universe.",
        ),
    ]
    relations = [
        SchemaRelation(
            label="SITUATED_AT", description="Indicates the location of a person."
        ),
        SchemaRelation(
            label="LED_BY",
            description="Indicates the leader of an organization.",
        ),
        SchemaRelation(
            label="OWNS",
            description="Indicates the ownership of an item such as a Horcrux.",
        ),
        SchemaRelation(
            label="INTERACTS", description="The interaction between two people."
        ),
    ]
    potential_schema = [
        ("PERSON", "SITUATED_AT", "LOCATION"),
        ("PERSON", "INTERACTS", "PERSON"),
        ("PERSON", "OWNS", "HORCRUX"),
        ("ORGANIZATION", "LED_BY", "PERSON"),
    ]

    # Set up the pipeline
    pipe = Pipeline()
    # pipe.add_component(PdfLoader(), "pdf_loader")
    from document_sources.wikipedia import WikiLoader
    pipe.add_component(
        WikiLoader(),
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
            "query": "Harry Potter",
            "metadata": {
                "title": "Harry Potter and the Death Hallows",
                "author": "J.K. Rowling",
                "language": "en",
            },
        },
        "schema": {
            "entities": entities,
            "relations": relations,
            "potential_schema": potential_schema,
        },
    }
    return await pipe.run(pipe_inputs)


async def main() -> PipelineResult:
    from azure_llm import CustomLLM
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
