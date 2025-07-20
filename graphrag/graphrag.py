# Auto-add project root to sys.path for direct script execution
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import os
import asyncio
from typing import Any, List, Optional, Union
from neo4j_graphrag.llm import LLMInterface, LLMResponse
from neo4j_graphrag.message_history import MessageHistory, LLMMessage
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.embeddings import OllamaEmbeddings # Assuming this or similar embedder
from neo4j_graphrag.types import LLMMessage # Ensure this is imported

from graphrag.azure_llm import CustomLLM
from graphrag.vector_cypher_retriever import retriever as Retriever

# --- GraphRAGPipeline Class (Added truncation limits) ---
class GraphRAGPipeline:
    """
    A RAG chat pipeline integrating a custom LLM and a Neo4j VectorCypherRetriever.
    Includes an option to provide additional context text from a file and context truncation.
    """
    def __init__(
        self,
        llm: LLMInterface = CustomLLM(""),
        retriever: VectorCypherRetriever = Retriever,
        system_instruction: Optional[str] = "You are a helpful assistant that answers questions based *only* on the provided information (graph data and/or file text). If the information does not contain the answer, explicitly state that you cannot answer based on the provided information. Do not use prior knowledge. Maintain a conversational tone.",
        retrieval_top_k: int = 1,
        max_graph_context_chars: int = 300000, # Max chars for the entire graph context section
        max_graph_item_text_chars: int = 50000, # Max chars for 'fullText' within one graph item
        max_file_context_chars: int = 300000,   # Max chars for the file context section
        max_overall_context_chars: int = 600000 # Max chars for the combined context before query
    ):
        """
        Initializes the GraphRAGPipeline with truncation limits.

        Args:
            llm: An instance of a class implementing LLMInterface (e.g., CustomLLM).
            retriever: An instance of VectorCypherRetriever.
            system_instruction: An optional initial system instruction for the LLM.
            retrieval_top_k: The number of top relevant nodes to retrieve from the graph.
            max_graph_context_chars: Max characters for the formatted graph context section.
            max_graph_item_text_chars: Max characters for the 'fullText' field within each graph item.
            max_file_context_chars: Max characters for the formatted file context section.
            max_overall_context_chars: Max characters for the combined graph and file context.
        """
        self.llm = llm
        self.retriever = retriever
        self.system_instruction = system_instruction
        self.retrieval_top_k = retrieval_top_k

        # Truncation Limits
        self.max_graph_context_chars = max_graph_context_chars
        self.max_graph_item_text_chars = max_graph_item_text_chars
        self.max_file_context_chars = max_file_context_chars
        self.max_overall_context_chars = max_overall_context_chars

        # print("GraphRAGPipeline initialized.")
        # print(f"LLM: {type(self.llm).__name__}")
        # print(f"Retriever: {type(self.retriever).__name__}")
        # print(f"Retrieval Top K: {self.retrieval_top_k}")
        # print(f"Context Truncation Limits:")
        # print(f"  Graph Item Text: {self.max_graph_item_text_chars}")
        # print(f"  Graph Section: {self.max_graph_context_chars}")
        # print(f"  File Section: {self.max_file_context_chars}")
        # print(f"  Overall Context: {self.max_overall_context_chars}")


    async def chat(self, user_query: str, context_file_text: Optional[str] = None) -> str:
        """
        Performs a RAG chat turn. Retrieves graph context, optionally includes
        additional file text, generates response, and updates history, applying truncation limits.

        Args:
            user_query: The user's input string.
            context_file_text: Optional text content from a file to include as context.

        Returns:
            The generated response from the LLM.
        """
        print(f"\nUser: {user_query}")
        if context_file_text:
            print(f"Including file context (approx {len(context_file_text)} chars before truncation).")


        # 1. Retrieve graph context based ONLY on the user_query
        retrieval_results = []
        try:
            print(f"Retrieving graph context for query: '{user_query}'...")
            # VectorCypherRetriever has an asearch method
            retrieval_results = self.retriever.search(query_text=user_query, top_k=self.retrieval_top_k)
        except Exception as e:
            print(f"Error during graph retrieval: {e}")


        # 2. Format and truncate graph context section
        formatted_graph_context = ""
        if retrieval_results:
            formatted_graph_context = str(retrieval_results)
        else:
            formatted_graph_context = "--- Retrieved Graph Information ---\nNo relevant information found in the knowledge graph.\n---\n\n"


        # 3. Format and truncate file context section
        formatted_file_context = ""
        if context_file_text:
             formatted_file_context += "--- Additional File Information ---\n"
             truncated_file_text = context_file_text.strip()
             if len(truncated_file_text) > self.max_file_context_chars:
                  truncated_file_text = truncated_file_text[:self.max_file_context_chars] + "...\n[File context truncated]"

             formatted_file_context += truncated_file_text
             formatted_file_context += "\n---\n\n"


        # 4. Combine contexts (graph and file)
        combined_context = ""
        # Add graph context if it's more than just the header/no results message
        if len(formatted_graph_context.strip()) > len("--- Retrieved Graph Information ---\nNo relevant information found in the knowledge graph.\n---\n\n".strip()):
             combined_context += formatted_graph_context
        elif formatted_graph_context.strip() == "--- Retrieved Graph Information ---\nNo relevant information found in the knowledge graph.\n---\n\n".strip():
             # Keep the "No relevant information" message if no graph results
             combined_context += formatted_graph_context


        if formatted_file_context.strip(): # Add file context if it's not empty
             combined_context += formatted_file_context

        # Apply overall context truncation as the final step before adding query/instructions
        if len(combined_context) > self.max_overall_context_chars:
             combined_context = combined_context[:self.max_overall_context_chars] + "\n... [Overall context truncated]\n" # Add truncation indicator

        # Print combined context for debugging (potentially truncated)
        # print("Combined Context for LLM (potentially truncated):")
        # print(combined_context)
        # print("-" * 20)


        # 5. Prepare LLM input (combine combined_context and user query)
        # Craft the prompt instructing the LLM to use the provided information
        # The instructions should mention that the context might be truncated
        llm_input = f"""Using the following provided information (which may include graph data and file text, and might be truncated), answer the user's query.
If the provided information does not contain the answer, explicitly state that you cannot answer based on the provided information.
Do not use prior knowledge outside of the provided information. Maintain a conversational tone.

{combined_context}

User Query: {user_query}
"""

        # 6. Generate response
        response_data = {"thinking": "Error generating response.", "answer": "Error generating response."}
        try:
            llm_response: LLMResponse = await self.llm.ainvoke(
                input=llm_input,
                message_history=[],
                # Pass the system instruction only on the first call if history is empty
                system_instruction=self.system_instruction if self.system_instruction else None
            )
            response_data = self.filter_and_extract_thinking(llm_response.content)
        except Exception as e:
             print(f"Error during LLM generation: {e}")
             response_data["answer"] = f"An error occurred while generating the response: {e}"

        # 8. Return structured response
        return {
            "context": combined_context,
            "thinking": response_data.get("thinking", "No thinking process available."),
            "answer": response_data.get("answer", "No answer generated.")
        }


    def add_files(self, file_paths: List[str]):
        """
        Placeholder method for adding files to the graph database (ingestion).
        """
        print(f"--- File Ingestion (Placeholder) ---")
        print(f"Received {len(file_paths)} file(s) for ingestion into the graph.")
        print("NOTE: Implement your actual ingestion pipeline here!")
        print("Files to process:")
        for file_path in file_paths:
            print(f"- {file_path}")
            # --- Your Ingestion Logic Goes Here ---
            # Example: call a function that reads, chunks, embeds, and loads to Neo4j
            # try:
            #     process_file_for_graph_ingestion(file_path, self.retriever.driver, self.retriever.embedder)
            #     print(f"Successfully initiated processing for {file_path}")
            # except Exception as e:
            #     print(f"Error processing {file_path}: {e}")
            # --- End of Ingestion Logic Placeholder ---
        print("--- End File Ingestion Placeholder ---\n")

    def filter_and_extract_thinking(self, content: str) -> dict:
        think_tag_start = "<think>"
        think_tag_end = "</think>"
        start_index = content.find(think_tag_start)
        end_index = content.find(think_tag_end)

        if start_index != -1 and end_index != -1:
            thinking = content[start_index + len(think_tag_start):end_index].strip()
            answer = content[end_index + len(think_tag_end):].strip()
        else:
            thinking = "No thinking process found."
            answer = content

        return {"thinking": thinking, "answer": answer}

# Comment out the hardcoded async main example
# async def main():
#     pipeline = GraphRAGPipeline()
#     user_query = "How can I use the RealityKit framework to create a 3D object in the Apple Vision Pro?"
#     response = await pipeline.chat(user_query)
#     print(f"Final Response: {response}")
#
# if __name__ == "__main__":
#     asyncio.run(main())

# Interactive CLI chat loop
import asyncio  # ensure asyncio is available

def main():
    pipeline = GraphRAGPipeline()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("Chat session started. Type 'exit' or 'quit' to end.")
    while True:
        user_query = input("You: ")
        if user_query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        # run the async chat turn
        response = loop.run_until_complete(pipeline.chat(user_query))
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()

