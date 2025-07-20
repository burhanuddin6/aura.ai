from neo4j_graphrag.experimental.pipeline.types import (
    EntityInputType,
    RelationInputType,
)

# Define the entities (nodes) that the LLM will extract from the text.
ENTITIES: list[EntityInputType] = [
    {
        "label": "Document",
        "description": "A single piece of documentation, typically a web page or a section from a PDF.",
        "properties": [
            {"name": "title", "type": "STRING", "description": "The main title of the document."},
            {"name": "content_summary", "type": "STRING", "description": "A brief summary of the document's content."},
            {"name": "full_content_hash", "type": "STRING", "description": "A hash of the full content for integrity/deduplication."},
        ],
    },
    {
        "label": "Concept",
        "description": "Key technical terms, functionalities, or ideas discussed in the documentation (e.g., RealityKit, Immersive Spaces, Plane Detection).",
        "properties": [
            {"name": "name", "type": "STRING", "description": "The name of the concept or feature."},
            {"name": "description", "type": "STRING", "description": "A brief explanation of the concept/feature."},
            {"name": "type", "type": "STRING", "description": "Categorization (e.g., 'Spatial Computing', 'Graphics', 'Interaction')."},
        ],
    },
    {
        "label": "App",
        "description": "Specific applications or sample projects mentioned (e.g., BOT-anist, Hello World).",
        "properties": [
            {"name": "name", "type": "STRING", "description": "The name of the app or sample."},
            {"name": "description", "type": "STRING", "description": "What the app/sample demonstrates or its purpose."},
            {"name": "type", "type": "STRING", "description": "E.g., 'Sample App', 'Featured App'."},
        ],
    },
    {
        "label": "API",
        "description": "Programming interfaces, frameworks, or development tools (e.g., ARKitSession, Reality Composer Pro, SwiftUI).",
        "properties": [
            {"name": "name", "type": "STRING", "description": "The name of the API, framework, or tool."},
            {"name": "type", "type": "STRING", "description": "E.g., 'API', 'Framework', 'Development Tool'."},
            {"name": "description", "type": "STRING", "description": "A brief overview of its function."},
        ],
    },
    {
        "label": "Platform",
        "description": "Operating systems or hardware platforms (e.g., visionOS, iOS, Apple Vision Pro).",
        "properties": [
            {"name": "name", "type": "STRING", "description": "The name of the platform."},
            {"name": "type", "type": "STRING", "description": "E.g., 'Operating System', 'Device'."},
        ],
    },
    {
        "label": "Interaction",
        "description": "User interaction methods (e.g., Tap to Select, Pinch to Rotate, Eye Tracking).",
        "properties": [
            {"name": "name", "type": "STRING", "description": "The name of the interaction."},
            {"name": "description", "type": "STRING", "description": "How the interaction works or its effect."},
        ],
    },
    {
        "label": "VideoSegment",
        "description": "Segments of video transcripts found in the documentation.",
        "properties": [
            {"name": "video_title", "type": "STRING", "description": "The title of the video."},
            {"name": "start_time", "type": "STRING", "description": "Timestamp of the segment start (e.g., '00:01:23')."},
            {"name": "end_time", "type": "STRING", "description": "Timestamp of the segment end."},
            {"name": "text", "type": "STRING", "description": "The transcribed text of the segment."},
            {"name": "speaker", "type": "STRING", "description": "The speaker, if identifiable (optional)."},
        ],
    },
]

# Define the relationships (edges) that connect the entities.
RELATIONS: list[RelationInputType] = [
    {
        "label": "DOCUMENT_DESCRIBES",
        "description": "A document provides information about a concept, API, or interaction. Properties: context_sentence (the sentence in which the relationship was identified), relevance_score (how strongly the document describes the entity).",
    },
    {
        "label": "DOCUMENT_REFERENCES",
        "description": "A document mentions or refers to an app, platform, or a video. Properties: context_sentence.",
    },
    {
        "label": "DEMONSTRATES",
        "description": "An app or sample project illustrates or uses a specific concept, API, or interaction. Properties: context_sentence.",
    },
    {
        "label": "USES",
        "description": "An app or sample is built using a specific API, framework, or tool. Properties: context_sentence.",
    },
    {
        "label": "IS_PART_OF",
        "description": "A concept, feature, API, or tool belongs to or is a component of a larger platform or another API/Framework.",
    },
    {
        "label": "SUPPORTS",
        "description": "A platform provides support for a particular API, feature, or interaction.",
    },
    {
        "label": "RELATED_TO",
        "description": "Indicates a semantic relationship or connection between two concepts/features that are often discussed together or are interdependent. Properties: reason (why they are related, e.g., 'often used together', 'alternative approach').",
    },
    {
        "label": "DISCUSSES",
        "description": "A segment of a video discusses a particular concept, app, platform, or interaction.",
    },
]

# Define the potential schema, listing valid (SourceNode, RelationshipType, TargetNode) combinations.
POTENTIAL_SCHEMA = [
    ("Document", "DOCUMENT_DESCRIBES", "Concept"),
    ("Document", "DOCUMENT_DESCRIBES", "API"),
    ("Document", "DOCUMENT_DESCRIBES", "Interaction"),
    ("Document", "DOCUMENT_REFERENCES", "App"),
    ("Document", "DOCUMENT_REFERENCES", "Platform"),
    ("Document", "DOCUMENT_REFERENCES", "VideoSegment"),
    ("App", "DEMONSTRATES", "Concept"),
    ("App", "DEMONSTRATES", "API"),
    ("App", "DEMONSTRATES", "Interaction"),
    ("App", "USES", "API"),
    ("Concept", "IS_PART_OF", "Platform"),
    ("API", "IS_PART_OF", "Platform"),
    ("API", "IS_PART_OF", "API"),  # e.g., a sub-framework is part of a larger framework
    ("Platform", "SUPPORTS", "API"),
    ("Platform", "SUPPORTS", "Concept"),
    ("Platform", "SUPPORTS", "Interaction"),
    ("Concept", "RELATED_TO", "Concept"),
    ("VideoSegment", "DISCUSSES", "Concept"),
    ("VideoSegment", "DISCUSSES", "App"),
    ("VideoSegment", "DISCUSSES", "Platform"),
    ("VideoSegment", "DISCUSSES", "Interaction"),
]