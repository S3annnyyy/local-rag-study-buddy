from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document
from src.config import TAVILY_API_KEY
from src.logger import get_logger

logger = get_logger(__name__)

def tavily_web_search_tool(state: dict):
    """
    This function conducts web search based on question and change in state

    Args:
        state: Current graph state

    Returns:
        state: Appended web results to documents
    """
    logger.info("---STARTING WEB SEARCH---")
    question, documents, search_count = state["question"], state["documents"], state.get("curr_search_count", 0)
    web_search_tool = TavilySearchResults(k=3, tavily_api_key=TAVILY_API_KEY) 

    documents_searched = web_search_tool.invoke({"query": question})
    web_results = "\n".join([document["content"] for document in documents_searched])
    web_results = Document(page_content=web_results)

    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
     
    search_count += 1
    return {"documents": documents, "question": question, "curr_search_count": search_count}