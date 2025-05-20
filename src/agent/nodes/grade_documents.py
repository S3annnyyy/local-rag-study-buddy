from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate 


LLM = ChatOllama(model="deepseek-r1:1.5b", format="json", temperature=0)

RETRIEVAL_PROMPT = PromptTemplate(
	template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
	You are a grader assessing the relevance of a retrieved document to a user question.
	If the document contains keywords or content related to the user question, grade it as relevant.
	It does not need to be a stringent test — the goal is to filter out obviously unrelated results.

	You must respond in **strict JSON format** as follows:
	{{"score": "yes"}} or {{"score": "no"}}.

	- Do not use numeric values like 1 or 0.
	- Do not include any preamble, explanation, or extra text.
	- Only respond with the JSON object.

	<|eot_id|><|start_header_id|>user<|end_header_id|>
	Here is the retrieved document:

	{document}

	Here is the user question:

	{question}

	Now, is the document relevant to the question? Respond strictly as instructed.

	<|eot_id|><|start_header_id|>assistant<|end_header_id|>
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
		print(f"GRADE given: {grade}")
		# Add relevant documents to filtered_docs
		if grade == "yes" or grade == "1":
			print("---GRADE: DOCUMENT RELEVANT")
			filtered_docs.append(doc)
		else:
			print("GRADE: DOCUMENT NOT RELEVANT")
			web_search = "Yes"
			continue
		
	return {"documents": filtered_docs, "question": question, "web_search": web_search}