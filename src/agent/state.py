from typing_extensions import TypedDict
from typing import List

class LangGraphState(TypedDict):
    """
    Represents the state of RAG LLM model architecture

    Attributes:
        question => question input
        generation => response generated from LLM
        web_search => result from web search 
        documents => corpus of documents for embedding
    """
    question: str
    generation: str
    web_search: str
    documents: List[str]