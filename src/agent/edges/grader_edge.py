from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate 
from langchain_ollama import ChatOllama

HALLUCINATION_PROMPT = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
	You are a grader assessing whether an answer is grounded in / supported by a set of facts.
	You must respond with a JSON object ONLY, with a single key 'score' whose value is either 'yes' or 'no'.
	Example: {{"score": "yes"}} or {{"score": "no"}} — no extra text, no explanation.

	Facts:
	{documents}
	-----
	Answer:
	{generation}
	<|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
		input_variables=["generation", "documents"],
)


GRADING_PROMPT = PromptTemplate(
	template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing 
	whether an answer is useful to resolve a question. Give a binary score 'yes' or 'no' to indicate 
	whether the answer is useful to resolve a question. Provide the binary score as a JSON with a 
	single key 'score' and no preamble or explanation. <|eot_id|><|start_header_id|>user<|end_header_id|> 
	Here is the answer: {generation}
	-----
	Here is the question: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
	input_variables=["generation", "question"],
)

LLM = ChatOllama(model="deepseek-r1:1.5b", format="json", temperature=0)

def hallucination_grader(state: dict):
	"""
	"""
	question = state["question"]
	documents = state["documents"]
	generation = state["generation"]
	hallucinationGrader = HALLUCINATION_PROMPT | LLM | JsonOutputParser()
	answerGrader = GRADING_PROMPT | LLM | JsonOutputParser()

	hallucination_score = hallucinationGrader.invoke({"documents": documents, "generation": generation})
	print("hallucination_score:", hallucination_score)
	hallucination_grade = hallucination_score["score"]
	

	if hallucination_grade.lower() == "yes":
		print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS") 
		print("---GRADE GENERATION vs QUESTION---")
		answer_score = answerGrader.invoke({"question": question, "generation": generation})
		answer_grade = answer_score["score"]

		if answer_grade.lower() == "yes":
			print("---DECISION: GENERATION ANSWERS QUESTION, NOT HALLUCINATION")
			return "useful"
		else:
			print("---DECISION: GENERATION IS A HALLUCINATION")
			return "not useful"
	else:
		print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS")
		return "not supported"