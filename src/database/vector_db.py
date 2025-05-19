import os
from langchain_community.document_loaders import FireCrawlLoader, DirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


VECTOR_DB_PATH = "existing_vectorstore"

def create_vector_database(CHUNK_SIZE: int, CHUNK_OVERLAP: int):
	"""
	This function creates vector database or retrieves from vectorstore if exists
	Args:
		CHUNK_SIZE (int):
		CHUNK_OVERLAP (int): 
	"""
	embeddings = HuggingFaceEmbeddings()
	if os.path.exists(VECTOR_DB_PATH) and os.listdir(VECTOR_DB_PATH):			
		vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
	else:
		# Load documents and create a new vectorstore
		loader = DirectoryLoader("./files")
		docs = loader.load()
		
		# Process the new documents
		semantic_text_splitter = SemanticChunker(embeddings)
		documents = semantic_text_splitter.split_documents(docs)
		text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
			chunk_size=CHUNK_SIZE,
			chunk_overlap=CHUNK_OVERLAP
		)
		split_documents = text_splitter.split_documents(documents)
		vectorstore = Chroma.from_documents(
			split_documents,
			embeddings,
			persist_directory=VECTOR_DB_PATH
		)
		retriever = vectorstore.as_retriever()
	return retriever

def add_documents(documents: list, CHUNK_SIZE: int, CHUNK_OVERLAP: int):
	"""
	Add new documents to the existing vectorstore.

	Args:
		documents (list): List of documents to add to the vectorstore
	"""
	embeddings = HuggingFaceEmbeddings()
	
	# Process the new documents
	semantic_text_splitter = SemanticChunker(embeddings)
	documents = semantic_text_splitter.split_documents(documents)
	text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
		chunk_size=CHUNK_SIZE,
		chunk_overlap=CHUNK_OVERLAP
	)
	split_documents = text_splitter.split_documents(documents)

	# Add to existing vectorstore
	if os.path.exists(VECTOR_DB_PATH) and os.listdir(VECTOR_DB_PATH):			
		vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
		vectorstore.add_documents(split_documents)
	else:
		# Create new vector store if it doesn't exist
		vectorstore = Chroma.from_documents(
			split_documents,
			embeddings,
			persist_directory=VECTOR_DB_PATH
		)

	return vectorstore