import os
import shutil
from ollama import chat
from langchain_community.document_loaders import CSVLoader, TextLoader, PDFPlumberLoader
from src.database.vector_db import add_documents

def process_uploaded_files(uploaded_files: list, chunk_size: int, chunk_overlap: int):
	"""
	Processes files uploaded by user and add it to vectorstore
	"""
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
			print("Documents loaded")
			docs = loader.load()
			add_documents(docs, chunk_size, chunk_overlap)

		return True
	finally:
		# Remove the temp folder and its contents
		shutil.rmtree(temp_folder, ignore_errors=True)

def invoke_ollama(user_prompt, model="deepseek-r1:1.5b", system_prompt="You are a helpful assistant."):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    chat_response = chat(
        model=model, 
        messages=messages,
    )

    return chat_response['message']['content']


