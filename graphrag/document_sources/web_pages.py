from langchain_community.document_loaders import WebBaseLoader
from shared.llm_graph_builder_exception import LLMGraphBuilderException
from shared.common_fn import last_url_segment
from typing import Dict, Optional
from neo4j_graphrag.experimental.components.types import DocumentInfo, PdfDocument
from neo4j_graphrag.experimental.components.pdf_loader import PdfLoader
from neo4j_graphrag.exceptions import PdfLoaderError

def get_documents_from_web_page(source_url:str):
  try:
    pages = WebBaseLoader(source_url, verify_ssl=False).load()
    return pages
  except Exception as e:
    raise LLMGraphBuilderException(str(e))

class WebPageLoaderError(PdfLoaderError):
    pass

class WebPageLoader(PdfLoader):
    async def run(
        self,
        source_url: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> PdfDocument:
        try:
            pages = get_documents_from_web_page(source_url)
        except Exception as e:
            raise WebPageLoaderError(str(e))

        if not pages:
            raise WebPageLoaderError("No content retrieved from the web page.")

        # concatenate all page contents
        full_text = "\n\n".join(page.page_content for page in pages)

        return PdfDocument(
            text=full_text,
            document_info=DocumentInfo(
                path=source_url,
                metadata=self.get_document_metadata(full_text, metadata),
            ),
        )
