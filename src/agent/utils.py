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

def invoke_ollama(model: str, system_prompt: str, user_prompt: str, output_format=None):
	messages = [
		{"role": "system", "content": system_prompt},
		{"role": "user", "content": user_prompt}
	]

	chat_response = chat(
		model=model, 
		messages=messages,
		format=output_format.model_json_schema() if output_format else None
	)

	if output_format:
		return output_format.model_validate_json(chat_response.message.content)
	else:
		return chat_response.message.content

def tavily_web_search_tool(query: str, include_raw_content=True, max_results=3):
	"""
	This function conducts web search using Tavily API

	Args:
		query (str): The search query to execute
		include_raw_content (bool): Whether to include the raw_content from Tavily in the formatted string
		max_results (int): Maximum number of results to return

	Returns:
		dictionary of format:
		{
			"results": [
				{
					"title": "Title of the page",
					"url": "https://link.to/the/page",
					"content": "Summary or snippet of the page content",
					"raw_content": "Full raw HTML/text content of the page"  # Only if include_raw_content=True
				},
			]
		}
	"""
	tavily_client = TavilyClient()
	response = tavily_client.search(
		query,
		max_results=max_results,
		include_raw_content=include_raw_content
	)

	return response
