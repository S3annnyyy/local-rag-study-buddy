from src.logger import get_logger

logger = get_logger(__name__)

def decide_to_generate(state: dict):
	"""
	This function determines whether to generate an answer or continue to web search

	Args:
		state: The current graph state

	Returns:
		str: Binary decision fo next node to call 
	"""
	logger.info("---ACCESS GRADED DOCUMENTS---")
	
	if state["web_search"] == "Yes":
		logger.info("---DECISION: ALL DOCUMENTS NOT RELEVANT TO USER INPUT, CONTINUING WEB SEARCH---")
		return "websearch"
	else:
		logger.info("---DECISION: GENERATE ANSWER---")
		return "generate_response"