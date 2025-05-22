import os
import shutil
from ollama import chat
from langchain_community.document_loaders import CSVLoader, TextLoader, PDFPlumberLoader
from src.database.vector_db import add_documents
from src.logger import get_logger


logger = get_logger(__name__)

def process_uploaded_files(uploaded_files: list, chunk_size: int, chunk_overlap: int):
	"""
	Processes files uploaded by user and add it to vectorstore
	"""
	temp_folder = "temp_files"
	os.makedirs(temp_folder, exist_ok=True)
	logger.info("Creating temp folders")

	try:
		for uploaded_file in uploaded_files:
			file_extension = uploaded_file.name.split(".")[-1].lower()
			temp_file_path = os.path.join(temp_folder, uploaded_file.name)

			# Save file temporarily
			with open(temp_file_path, "wb") as f:
				f.write(uploaded_file.getvalue())

			# Choose the appropriate loader
			if file_extension == "csv":
				loader = CSVLoader(temp_file_path)
			elif file_extension in ["txt", "md"]:
				loader = TextLoader(temp_file_path)
			elif file_extension == "pdf":
				loader = PDFPlumberLoader(temp_file_path)
			else:
				continue

			# Load and append documents
			logger.info("Documents loaded")
			docs = loader.load()
			add_documents(docs, chunk_size, chunk_overlap)

		return True
	finally:
		shutil.rmtree(temp_folder, ignore_errors=True)
		logger.info("Temp folders dumped")

def invoke_ollama(user_prompt, model="deepseek-r1:1.5b", history=None):
	messages = [{"role": "system", "content": "You are a helpful study assistant that answers clearly and concisely."}]
	if history:
		messages.extend(history)
	messages.append({"role": "user", "content": user_prompt})

	chat_response = chat(
		model=model, 
		messages=messages,
	)

	return chat_response['message']['content']
