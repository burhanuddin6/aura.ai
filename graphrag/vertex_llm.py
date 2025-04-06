from neo4j_graphrag.llm import LLMResponse, VertexAILLM
from vertexai.generative_models import GenerationConfig

generation_config = GenerationConfig(temperature=0.0)
vertex_llm = VertexAILLM(
    model_name="gemini-1.5-flash-001",
    generation_config=generation_config,
    # add here any argument that will be passed to the
    # vertexai.generative_models.GenerativeModel client
)

if __name__ == "__main__":
    res: LLMResponse = vertex_llm.invoke("say something")
    print(res.content)