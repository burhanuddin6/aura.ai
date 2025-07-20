
import streamlit as st
import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from graphrag.graphrag import GraphRAGPipeline

# --- Streamlit App ---

st.set_page_config(page_title="Docskeeping AI", layout="wide")

st.title("📚 Docskeeping AI (Apple Vision Pro)")
st.markdown("""
This is a demonstration of Docskeeping AI, a chatbot that is grounded with relevant documentation and achieves 0 hallucination with the help of Graph based Retrieval-Augmented Generation (RAG).
This is a proof of concept demonstration of how one can build a highly effective search and QnA system. I have used the Apple Vision Pro documentation for this demo, so you will only get relevant answers related to Apple Vision Pro and its frameworks like ARKit, RealityKit, etc.
This demo does not show graph indexing process here, but its discussed in my technical blog post [mentioned here](https://burhanuddin6.github.io/resume/#aura).    
""")

# Initialize the GraphRAGPipeline
@st.cache_resource
def get_pipeline():
    return GraphRAGPipeline()

pipeline = get_pipeline()

# Pre-made prompts
premade_prompts = [
    "How to decode barcodes using ARKit in visionOS",
    "How can I use the RealityKit framework to create a 3D object in the Apple Vision Pro?",
    "How do I add 3D content to my app?",
]

st.subheader("Ask a question")

# Use session state to store the query
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

def set_query(prompt):
    st.session_state.user_query = prompt

# Display premade prompts as buttons
st.write("Or try one of these:")
for prompt in premade_prompts:
    if st.button(prompt):
        set_query(prompt)

# Text input for user query
user_query = st.text_input("Enter your question here:", value=st.session_state.user_query, key="query_input")


if user_query:
    st.markdown("---")
    st.subheader("Response")

    with st.spinner("Thinking..."):
        # Run the async chat function
        response_data = asyncio.run(pipeline.chat(user_query))
        response_data = dict(response_data)

        # Display the retrieved content
        with st.expander("Retrieved Content", expanded=False):
            st.text(response_data.get("context", "No context retrieved."))

        # Display the LLM's thinking
        with st.expander("LLM Thinking", expanded=False):
            st.text(response_data.get("thinking", "No thinking process available."))

        # Display the final answer
        st.markdown("### Final Answer")
        st.markdown(response_data.get("answer", "No answer generated."))
