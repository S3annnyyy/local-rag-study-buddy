from langgraph.graph import START, END, StateGraph
from agent.state import LangGraphState
from src.agent.nodes.retrieve import retrieve
from src.agent.nodes.web_search import tavily_web_search_tool
from src.agent.nodes.grade_documents import retrieval_grader
from src.agent.nodes.answer_generation import generate_response

# Initialize state
workflow = StateGraph(LangGraphState)

# Define nodes
workflow.add_node("retrieve", retrieve) 
workflow.add_node("websearch", tavily_web_search_tool) 
workflow.add_node("grade_documents", retrieval_grader)
workflow.add_node("generate_response", generate_response)