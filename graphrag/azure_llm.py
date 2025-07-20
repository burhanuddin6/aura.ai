import os
from typing import Any, List, Optional, Union

from neo4j_graphrag.llm import LLMInterface, LLMResponse
from neo4j_graphrag.message_history import MessageHistory
from neo4j_graphrag.types import LLMMessage

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.aio import ChatCompletionsClient as AsyncChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from graphrag.shared.env import AZURE_INFERENCE_ENDPOINT, AZURE_INFERENCE_CREDENTIAL, AZURE_MODEL_NAME

class CustomLLM(LLMInterface):
    def __init__(
        self, model_name: str, system_instruction: Optional[str] = None, **kwargs: Any
    ):
        super().__init__(model_name, **kwargs)
        self.endpoint = AZURE_INFERENCE_ENDPOINT
        self.key = AZURE_INFERENCE_CREDENTIAL
        self.model_name = AZURE_MODEL_NAME
        if not self.endpoint or not self.key or not self.model_name:
            print("Missing environment variable 'AZURE_INFERENCE_ENDPOINT' or 'AZURE_INFERENCE_CREDENTIAL'")
            print("Set them before running this sample.")
            exit()

    def invoke(
        self,
        input: str,
        message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:

        messages = message_history.messages if message_history else []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        messages.append(UserMessage(content=input))

        client = ChatCompletionsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))

        response = client.complete(
            messages=messages,
            max_tokens=10240,
            model=self.model_name,
            timeout=20,
        )

        return LLMResponse(content=self.filter_content(response.choices[0].message.content))

    async def ainvoke(
        self,
        input: str,
        message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:

        messages = message_history.messages if message_history else []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        messages.append(UserMessage(content=input))
        async with AsyncChatCompletionsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key)) as client:

            response = await client.complete(
                messages=messages,
                max_tokens=10240,
                model=self.model_name,
                timeout=10,
            )

            print(response.choices[0].message.content)
            print(f"Token usage: {response.usage}")
        
        # remove filter content for inference but keep it for indexing since the think tag will be problematic 
        # when trying to build the graph
        return LLMResponse(content=self.filter_content(response.choices[0].message.content))

    def filter_content(self, content: str) -> str:
        # find the think tag </think> and remove text above it
        think_tag = "</think>"
        think_index = content.find(think_tag)
        if think_index != -1:
            content = content[think_index + len(think_tag):]
        else:
            # if think tag not found, just return the content
            content = content
        return content
    
import asyncio

async def main():
    llm = CustomLLM("")
    res: LLMResponse = await llm.ainvoke("Hello world")
    print(res.content)    

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())