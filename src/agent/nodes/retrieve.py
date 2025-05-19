from src.database.vector_db import create_vector_database

def retrieve(state: dict):
	"""
	This function retrieve documents from vectorstore

	Args:
		state: The current graph state
		retriever: retriever tool from vectorDB
			
	Returns:
			state: New key added to state, documents that contains retrieved documents
	"""
	retriever = create_vector_database(1000, 200)
	print("---RETRIEVE---")
	question = state["question"]
	documents = retriever.invoke(question)
	return {"documents": documents, "question": question}