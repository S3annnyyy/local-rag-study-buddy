import os
import re
import shutil
from ollama import chat
from tavily import TavilyClient
from pydantic import BaseModel
from langchain_community.document_loaders import CSVLoader, TextLoader, PDFPlumberLoader
from src.database.vector_db import create_vector_database, add_documents

def process_uploaded_files(uploaded_files: list, chunk_size: int, chunk_overlap: int):
	temp_folder = "temp_files"
	os.makedirs(temp_folder, exist_ok=True)

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
			docs = loader.load()
			add_documents(docs, chunk_size, chunk_overlap)

		return True
	finally:
		# Remove the temp folder and its contents
		shutil.rmtree(temp_folder, ignore_errors=True)