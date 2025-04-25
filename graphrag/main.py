# load json from merged.json
import json
import os
import asyncio

# merged json stored at ./Data/merged.json
json_file_path = os.path.join("Data/VisionPro", "merged.json")
with open(json_file_path, "r") as f:
    data = json.load(f)


import graphrag.kg_builder as kg_builder

vision_docs = data["visionos_docs_PDFs"]

async def process_vision_docs():
    for key, value in list(vision_docs.items())[:10]:
        data = f'{key}: {value}'
        await kg_builder.build_kg_from_text(data)
    # await kg_builder.build_kg_from_pdf()

# Run the async function
asyncio.run(process_vision_docs())


