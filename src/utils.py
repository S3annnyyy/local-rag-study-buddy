import re
import os
import shutil
import types
from ollama import chat
from langchain_community.document_loaders import CSVLoader, TextLoader, PDFPlumberLoader
from src.database.vector_db import add_documents
from src.logger import get_logger
from src.agent.workflow import RAG_AGENT


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

def extract_response_components(generation: str):
	"""
	Extracts the <think></think> reasoning block and final answer from generation text.
	"""
	think_block, final_answer = "", generation

	# Find <think> block
	think_match = re.search(r"<think>(.*?)</think>", generation, re.DOTALL)
	if think_match:
		think_block = think_match.group(1).strip()
		# Remove think block from final answer
		final_answer = re.sub(r"<think>.*?</think>", "", generation, flags=re.DOTALL).strip()

	logger.debug("Extracted think_block and final_answer from generation.")
	return think_block, final_answer

def generate_response(user_input: str, st: types.ModuleType):
	"""
	Generate a response based on the user input using the agent, with optional web search capability.
	Args:
		user_input (str): User prompt
		st (Module): Streamlit session state 
	Returns:
		dict: The generated response and reasoning.
	"""
	langgraph_status = st.status("**Agent running...**", state="running")  # Sets status to running
	logger.info(f"Received user input: {user_input}")
	inputs = {"question": user_input}
	final_generation, think_block = None, None

	if st.session_state.enable_rag:
		logger.info("Routing user input to RAG workflow.")
		try:
			for output in RAG_AGENT.stream(inputs):
				for key, value in output.items():
					if "generation" in value:
						final_generation = value["generation"]

			if final_generation is None:
				final_generation = "Agent couldn't find an answer."

			think_block, final_answer = extract_response_components(final_generation)
			
			langgraph_status.update(state="complete", label="**Using LangGraph** (Tasks completed)")
			logger.info("RAG workflow completed successfully.")

		except Exception as e:
			final_answer = f"An error occurred: {str(e)}"
			think_block = ""
			langgraph_status.update(state="error", label="Something went wrong.")
			logger.error(f"Exception in RAG workflow: {e}")
	else:
		logger.info("Routing user input to direct LLM generation.")
		final_generation = invoke_ollama(user_input, history=st.session_state.messages)
		think_block, final_answer = extract_response_components(final_generation)
		logger.info("Direct LLM generation completed.")
	
	logger.debug("Generated response and parsing to frontend.")
	langgraph_status.update(state="complete", label="**Using Deepseek R1 model**")
	print("Output retrieved, parsing to frontend")
	return {"final_answer": final_answer, "reasoning": think_block}