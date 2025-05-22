from src.database.vector_db import retrieve_vector_database
from src.logger import get_logger

logger = get_logger(__name__)

def retrieve(state: dict):
	"""
	This function retrieve documents from vectorstore

	Args:
		state: The current graph state
		retriever: retriever tool from vectorDB
			
	Returns:
			state: New key added to state, documents that contains retrieved documents
	"""
	retriever = retrieve_vector_database()
	logger.info("---RETRIEVING VECTORSTORE---")
	question = state["question"]
	documents = retriever.invoke(question)
	return {"documents": documents, "question": question}