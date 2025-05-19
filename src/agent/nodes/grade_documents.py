from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate 


LLM = ChatOllama(model="deepseek-coder:1.5b", format="json", temperature=0)

RETRIEVAL_PROMPT = PromptTemplate(
	template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a grader assessing relevance
	of a retrieved document to a user question. If the document contains keywords related to the user question,
	grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
	Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
	Provide the binary score as a JSON with a single key 'score' and no preamble or explanation. 
	<|eot_id|><|start_header_id|>user<|end_header_id|>
	Here is the retrieved document: \n\n{document} \n\n
	Here is the user question: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
	""",
	input_variables=["question", "document"]
)

def retrieval_grader(state: dict):
	"""
	This function determines if any retrieved documents are relevant to the question.
	If not relevant => Set flag to run web search

	Args:
		state: The current graph state
	
	Returns:
		state: Filtered to contain only relevant documents + updated web search state 
	"""
	# Init retrieval grader
	retrieval_grader = RETRIEVAL_PROMPT | LLM | JsonOutputParser()

	print("---CHECK DOCUMENT RELEVANCE TO THE QUESTION---")
	question = state["question"]
	documents = state["documents"]

	filtered_docs = []
	web_search = "No"
	for doc in documents:
		score = retrieval_grader.invoke({"question": question, "document": doc.page_content})
		grade = score["score"]
		# Add relevant documents to filtered_docs
		if grade.lower() == "yes":
			print("---GRADE: DOCUMENT RELEVANT")
			filtered_docs.append(doc)
		else:
			print("GRADE: DOCUMENT NOT RELEVANT")
			web_search = "Yes"
			continue
		
	return {"documents": filtered_docs, "question": question, "web_search": web_search}