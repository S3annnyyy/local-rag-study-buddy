from pprint import pprint
from langgraph.graph import END, StateGraph
from src.agent.nodes.retrieve import retrieve
from src.agent.nodes.web_search import tavily_web_search_tool
from src.agent.nodes.grade_documents import retrieval_grader
from src.agent.nodes.answer_generation import generate_response
from src.agent.edges.answer_generation_edge import decide_to_generate
from src.agent.edges.grader_edge import hallucination_grader
from typing_extensions import TypedDict
from typing import List


# Initialize state
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

workflow = StateGraph(LangGraphState)

# Define nodes
workflow.add_node("retrieve", retrieve) 
workflow.add_node("websearch", tavily_web_search_tool) 
workflow.add_node("grade_documents", retrieval_grader)
workflow.add_node("generate_response", generate_response)

# Build graph
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges("grade_documents", decide_to_generate, {
  "websearch": "websearch",
  "generate_response": "generate_response"
})
workflow.add_edge("websearch", "generate_response")
workflow.add_conditional_edges(
  "generate_response",
  hallucination_grader,
  {
    "not_supported": "generate_response",
    "useful": END,
    "not useful": "websearch",
  }
)

# Compile graph
RAG_AGENT = workflow.compile()

# inputs = {"question": ""}
# for output in RAG_AGENT.stream(inputs):
#   for key, value in output.items():
#     pprint(f"Finished running: {key}")
# pprint(value["generation"])