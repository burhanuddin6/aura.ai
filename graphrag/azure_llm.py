from langchain_core.messages import HumanMessage, SystemMessage

import random
import string
from typing import Any, List, Optional, Union

from neo4j_graphrag.llm import LLMInterface, LLMResponse
from neo4j_graphrag.message_history import MessageHistory
from neo4j_graphrag.types import LLMMessage

import time

class CustomLLM(LLMInterface):
    def __init__(
        self, model_name: str, system_instruction: Optional[str] = None, **kwargs: Any
    ):
        super().__init__(model_name, **kwargs)
        from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
        import os
        from dotenv import load_dotenv
        load_dotenv(".env.azure")

        self.model = AzureAIChatCompletionsModel(
            endpoint=os.getenv("AZURE_INFERENCE_ENDPOINT"),
            credential=os.getenv("AZURE_INFERENCE_CREDENTIAL"),
            model_name=os.getenv("AZURE_MODEL_NAME")
        )
        print("Model initialized")
        print(os.getenv("AZURE_INFERENCE_ENDPOINT"))
        print(os.getenv("AZURE_INFERENCE_CREDENTIAL"))
        print(os.getenv("AZURE_MODEL_NAME"))

    def invoke(
        self,
        input: str,
        message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        content: str = (
            self.model_name + ": " + "".join(random.choices(string.ascii_letters, k=30))
        )
        # properly call the langchain model
        messages = message_history.messages if message_history else []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        messages.append(HumanMessage(content=input))

        response = self.model.invoke(messages)
        return LLMResponse(content=response.content)

    async def ainvoke(
        self,
        input: str,
        message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        
        import os
        from azure.ai.inference.aio import ChatCompletionsClient
        from azure.ai.inference.models import SystemMessage, UserMessage
        from azure.core.credentials import AzureKeyCredential

        try:
            endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
            key = os.environ["AZURE_INFERENCE_CREDENTIAL"]
        except KeyError:
            print("Missing environment variable 'AZURE_INFERENCE_ENDPOINT' or 'AZURE_INFERENCE_CREDENTIAL'")
            print("Set them before running this sample.")
            exit()

        messages = message_history.messages if message_history else []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        messages.append(UserMessage(content=input))
        async with ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key)) as client:

            response = await client.complete(
                messages=messages,
                max_tokens=10240,
                model=os.getenv("AZURE_MODEL_NAME"),
                timeout=10,
            )

            print(response.choices[0].message.content)
            print(f"\nToken usage: {response.usage}")
        
        content = response.choices[0].message.content

        # find the think tag </think> and remove text above it
        think_tag = "</think>"
        think_index = content.find(think_tag)
        if think_index != -1:
            content = content[think_index + len(think_tag):]
        else:
            # if think tag not found, just return the content
            content = content
            
        return LLMResponse(content=content)
    

import asyncio

async def main():
    llm = CustomLLM("")
    res: LLMResponse = await llm.ainvoke("Hello world")
    print(res.content)
    

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())