from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate 
from langchain_ollama import ChatOllama
from src.logger import get_logger

logger = get_logger(__name__)

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
	whether an answer is useful to resolve a question.
	You must respond with a JSON object ONLY, with a single key 'score' whose value is either 'yes' or 'no'.
	Example: {{"score": "yes"}} or {{"score": "no"}} — no extra text, no explanation.

	Question:
	{question}
	-----
	Answer:
	{generation}
	<|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
	input_variables=["generation", "question"],
)

LLM = ChatOllama(model="deepseek-r1:1.5b", format="json", temperature=0)

def hallucination_grader(state: dict):
	"""
	"""
	question, documents, generation = state["question"], state["documents"], state["generation"]
	hallucinationGrader = HALLUCINATION_PROMPT | LLM | JsonOutputParser()
	answerGrader = GRADING_PROMPT | LLM | JsonOutputParser()

	hallucination_score = hallucinationGrader.invoke({"documents": documents, "generation": generation})
	logger.info(f"Hallucination_score: {hallucination_score}")

	hallucination_grade = hallucination_score.get("score", "no")
	
	if hallucination_grade.lower() == "yes":
		logger.info("---DECISION: LLM GENERATION IS GROUNDED IN DOCUMENTS---") 
		logger.info("---GRADE LLM GENERATION AGAINST USER QUESTION---")
		answer_score = answerGrader.invoke({"question": question, "generation": generation})
		answer_grade = answer_score.get("score", "no")
		logger.info(f"Answer Grade: {answer_grade}")

		if answer_grade.lower() == "yes":
			logger.info("---DECISION: GENERATION ANSWERS QUESTION, NOT HALLUCINATION---")
			return "useful"
		else:
			logger.info("---DECISION: GENERATION IS A HALLUCINATION---")
	else:
		logger.info("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS---")
	
	curr_search_count, search_limit = state.get("curr_search_count", 0), state.get("max_search_queries")
	logger.info(f"Current search count: {curr_search_count}, limit: {search_limit}")
	if curr_search_count >= search_limit:		
		logger.info("---DECISION: SEARCH LIMIT EXCEEDED, OUTPUTTING BEST GUESS---")
		return "useful"
	
	logger.info("---DECISION: SEARCH LIMIT NOT EXCEEDED, CONTINUING WEB SEARCH---")
	return "not useful"