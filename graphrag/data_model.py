from neo4j_graphrag.experimental.pipeline.types import (
    EntityInputType,
    RelationInputType,
)

# Instantiate Entity and Relation objects. This defines the
# entities and relations the LLM will be looking for in the text.
ENTITIES: list[EntityInputType] = [
    {"label": "Company", "description": "A company that produces products", "properties": [{"name": "name", "type": "STRING"}]},
    {"label": "Product", "properties": [{"name": "name", "type": "STRING"}, {"name": "category", "type": "STRING"}]},
    # ... or with a dict if more details are needed,
    # such as a description:
]
# same thing for relationships:
RELATIONS: list[RelationInputType] = [
    {
        "label": "BELONGS_TO",
        "description": "Used to describe which a belongs to relationship between two nodes. For example a documentation can belong to a product",
    },
]
POTENTIAL_SCHEMA = [
    ("Product", "BELONGS_TO", "Company"),
]

