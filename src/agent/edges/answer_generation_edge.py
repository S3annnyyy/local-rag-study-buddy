def decide_to_generate(state: dict):
	"""
	This function determines whether to generate an answer or add to web search

	Args:
		state: The current graph state

	Returns:
		str: Binary decision fo next node to call 
	"""
	print("---ACCESS GRADED DOCUMENTS---")
	web_search = state["web_search"]
	
	if web_search == "Yes":
		print("---DECISION: ALL DOCUMENTS NOT RELEVANT TO QN, INCLUDE WEB SEARCH---")
		return "websearch"
	else:
		print("---DECISION: GENERATE ANSWER---")
		return "generate_response"