from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

LLM = ChatOllama(model="deepseek-r1:1.5b", temperature=0)

ANSGEN_PROMPT = PromptTemplate(
	template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for question-answering tasks.
	Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
	Use three sentences maximum and keep the answer concise <|eot_id|><|start_header_id|>user<|end_header_id|>
	Question: {question}
	Context: {context}
	Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
	input_variables=["question", "document"],
)

def generate_response(state: dict):
	"""
	This function generates an answer using RAG on retrieved documents 

	Args:
		state: Current state of graph

	Returns:
		state: New key added to state, generation that contains LLM response
	"""
	print("---GENERATE RESPONSE---")
	question = state["question"]
	documents = state["documents"]

	rag_chain = ANSGEN_PROMPT | LLM | StrOutputParser()
	
	generation = rag_chain.invoke({"context": documents, "question": question})
	return {"documents": documents, "question": question, "generation": generation} 
