import os
import asyncio
import io
import mimetypes
from typing import Optional, Annotated

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import PlainTextResponse
# Import your GraphRAGPipeline, CustomLLM, and Retriever setup
from graphrag.pipeline import GraphRAGPipeline
from graphrag.azure_llm import CustomLLM
# Import the global retriever instance and the driver closing function
from graphrag.vector_cypher_retriever import retriever as global_retriever_instance, close_neo4j_driver

# Import libraries for file processing
# Consider installing: pip install pymupdf python-docx python-multipart
try:
    import fitz # PyMuPDF
except ImportError:
    fitz = None
    print("Warning: PyMuPDF not installed. PDF file processing will not be available.")

try:
    import docx # python-docx
except ImportError:
    docx = None
    print("Warning: python-docx not installed. DOCX file processing will not be available.")

# --- Helper functions for text extraction ---

async def _extract_text_from_pdf(file_content: bytes) -> str:
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) is not installed. Cannot process PDF files.")
    text = ""
    try:
        # Open PDF from memory bytes
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise RuntimeError(f"Failed to extract text from PDF: {e}")

async def _extract_text_from_docx(file_content: bytes) -> str:
    if docx is None:
         raise RuntimeError("python-docx not installed. Cannot process DOCX files.")
    text = ""
    try:
        # Open DOCX from memory bytes using BytesIO
        doc = docx.Document(io.BytesIO(file_content))
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        raise RuntimeError(f"Failed to extract text from DOCX: {e}")


async def _extract_text_from_txt(file_content: bytes) -> str:
    try:
        # Attempt to decode as UTF-8, fallback if necessary
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
         try:
              return file_content.decode('latin-1') # Basic fallback
         except Exception as e:
              print(f"Error decoding text file: {e}")
              raise RuntimeError(f"Failed to decode text file: {e}")
    except Exception as e:
        print(f"Error reading text file: {e}")
        raise RuntimeError(f"Failed to read text file: {e}")


async def extract_text_from_file(file: UploadFile) -> str:
    """Extracts text from supported file types."""
    file_content = await file.read()
    filename = file.filename.lower()

    # Determine file type based on extension or mimetype
    if filename.endswith(".pdf") or (file.content_type and "application/pdf" in file.content_type):
        return await _extract_text_from_pdf(file_content)
    elif filename.endswith(".docx") or (file.content_type and "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in file.content_type):
        return await _extract_text_from_docx(file_content)
    elif filename.endswith(".txt") or (file.content_type and "text/plain" in file.content_type):
        return await _extract_text_from_txt(file_content)
    else:
        # Try guessing mimetype if not obvious
        mime, _ = mimetypes.guess_type(filename)
        if mime:
             if "application/pdf" in mime:
                  return await _extract_text_from_pdf(file_content)
             elif "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in mime:
                   return await _extract_text_from_docx(file_content)
             elif "text/plain" in mime:
                   return await _extract_text_from_txt(file_content)


        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type or 'unknown'}. Supported types: PDF, DOCX, TXT."
        )

# --- FastAPI App Initialization ---
app = FastAPI(
    title="GraphRAG Chat API",
    description="Backend API for GraphRAG chat with file context.",
    version="1.0.0",
)

# Placeholder for the RAG pipeline instance
pipeline: Optional[GraphRAGPipeline] = None

# --- Startup and Shutdown Events ---

@app.on_event("startup")
async def startup_event():
    # Initialize the pipeline with the created instances
    global pipeline
    pipeline = GraphRAGPipeline()

# @app.on_event("shutdown")
# async def shutdown_event():
#     """Close resources like the Neo4j driver on app shutdown."""
#     print("FastAPI shutdown event triggered.")
#     # Call the closing function from the retriever module
#     close_neo4j_driver()
#     print("Shutdown complete.")


# --- API Routes ---

@app.get("/", response_class=PlainTextResponse, summary="Health Check")
async def read_root():
    """Basic health check endpoint."""
    return "GraphRAG FastAPI backend is running."

@app.post("/chat", summary="Chat with GraphRAG Pipeline")
async def chat_endpoint(
    query: Annotated[str, Form(description="The user's query string.")],
    file: Annotated[Optional[UploadFile], File(description="Optional document file (PDF, DOCX, TXT) for additional context.")] = None
):
    """
    Receives a user query and an optional file, processes them using the
    GraphRAG pipeline, and returns the assistant's response.
    """
    global pipeline
    if pipeline is None:
        # If pipeline initialization failed at startup
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG pipeline is not initialized. Check server logs for startup errors."
        )

    context_file_text: Optional[str] = None
    if file:
        try:
            print(f"Received file: {file.filename}, content_type: {file.content_type}")
            context_file_text = await extract_text_from_file(file)
            print(f"Extracted text length: {len(context_file_text or '')}")
        except RuntimeError as e:
            # File extraction failed
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
             # Catch any other unexpected file processing errors
             print(f"Unexpected error processing file: {e}")
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred during file processing.")


    try:
        # Call the GraphRAGPipeline's async chat method
        assistant_response = await pipeline.chat(user_query=query, context_file_text=context_file_text)
        return {"response": assistant_response}
    except Exception as e:
        # Catch any errors from the pipeline.chat method
        print(f"Error during RAG pipeline chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the chat request: {e}"
        )