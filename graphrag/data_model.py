from neo4j_graphrag.experimental.pipeline.types import (
    EntityInputType,
    RelationInputType,
)

# Instantiate Entity and Relation objects. This defines the
# entities and relations the LLM will be looking for in the text.
ENTITIES: list[EntityInputType] = [
    "Chunk",
    {"label": "Doc", "description": "A chunk of text that is part of a document. This label is added to nodes with Chunk label that are from some document"},
    {"label": "Company", "description": "A company that produces products", "properties": [{"name": "name", "type": "STRING"}]},
    {"label": "Product", "properties": [{"name": "name", "type": "STRING"}, {"name": "category", "type": "STRING"}]},
    # ... or with a dict if more details are needed,
    # such as a description:
    {"label": "Url", "description": "Stores any links that are mentioned", "properties": [{"name": "url", "type": "STRING"}]},
]
# same thing for relationships:
RELATIONS: list[RelationInputType] = [
    {
        "label": "BELONGS_TO",
        "description": "Used to describe which a belongs to relationship between two nodes. For example a documentation can belong to a product",
    },
    {
        "label": "URL_FOR",
        "description": "Used to indicate which chunk source the URL is for",
    }
]
POTENTIAL_SCHEMA = [
    ("Product", "BELONGS_TO", "Company"),
]

