from typing import Dict, Optional
import logging

from langchain_community.document_loaders import WikipediaLoader
from neo4j_graphrag.experimental.components.types import DocumentInfo, PdfDocument
from neo4j_graphrag.exceptions import PdfLoaderError
from neo4j_graphrag.experimental.components.types import DocumentInfo, PdfDocument
from neo4j_graphrag.experimental.components.pdf_loader import PdfLoader

from graphrag.shared.llm_graph_builder_exception import LLMGraphBuilderException

class WikiLoaderError(PdfLoaderError):
  pass

class WikiLoader(PdfLoader):
  @staticmethod
  def get_documents_from_Wikipedia(wiki_query:str, language:str):
    try:
      pages = WikipediaLoader(query=wiki_query.strip(), lang=language, load_all_available_meta=False,doc_content_chars_max=100000, load_max_docs=1).load()
      metadata = pages[0].metadata
      logging.info(f"Total Pages from Wikipedia = {len(pages)}")
      return metadata, pages
    except Exception as e:
      message="Failed To Process Wikipedia Query"
      error_message = str(e)
      logging.exception(f'Failed To Process Wikipedia Query, Exception Stack trace: {error_message}')
      raise LLMGraphBuilderException(error_message+' '+message)
    
  async def run(
      self,
      query: str,
      language: Optional[str] = "en",
  ) -> PdfDocument:
      try:
        metadata, pages = self.get_documents_from_Wikipedia(query, language)
      except Exception as e:
          raise WikiLoaderError(e)
      
      if not pages:
          raise WikiLoaderError("No pages found for the given query.")
      
      text = pages[0].page_content
      return PdfDocument(
          text=text,
          document_info=DocumentInfo(
              path=metadata['source'],
              metadata=metadata,
          ),
      )