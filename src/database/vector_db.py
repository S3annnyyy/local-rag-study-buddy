import os
from langchain_community.document_loaders import FireCrawlLoader, DirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d")
VECTOR_DB_PATH = f"vectorstore_{timestamp}"

def retrieve_vector_database():
	"""
	This function initializes a vector database or retrieves from vectorstore if exists
	"""
	embeddings = HuggingFaceEmbeddings()
	if os.path.exists(VECTOR_DB_PATH) and os.listdir(VECTOR_DB_PATH):
		print(f"Existing vectorstore: {VECTOR_DB_PATH} found")			
		vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
	else:
		# Initialize a new vectorstore
		vectorstore = Chroma.from_documents(
			embeddings,
			persist_directory=VECTOR_DB_PATH
		)
	retriever = vectorstore.as_retriever()
	return retriever

def add_documents(documents: list, CHUNK_SIZE: int, CHUNK_OVERLAP: int):
	"""
	This function converts documents uploaded into embeddings and either
		(a) Add to existing vectorstore
		(b) Create vectorestore and add embeddings inside 

	Args:
		documents (list): List of documents to add to the vectorstore
	"""
	embeddings = HuggingFaceEmbeddings()
	
	# Process the new documents
	print("Processing documents...")
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
		print("Added documents to vectorstore")	
	else:
		# Create new vector store if it doesn't exist
		vectorstore = Chroma.from_documents(
			split_documents,
			embeddings,
			persist_directory=VECTOR_DB_PATH
		)
		print("Initialized new vectorstore")	
	print("Processing complete")
	return vectorstore