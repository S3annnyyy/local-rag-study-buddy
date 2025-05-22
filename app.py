import torch
import pyperclip
import streamlit as st
from src.utils import process_uploaded_files, generate_response 
from src.logger import get_logger
from src.theme.custom import set_custom_theme

torch.classes.__path__ = [] # Little hack to remove torch.classes.__path__ runtime error [REF: Issue #1] 
logger = get_logger(__name__)

def clear_chat():
	logger.info("Clearing chat session state.")
	st.session_state.messages = []
	st.session_state.processing_complete = False
	st.session_state.uploader_key = 0

def main():
	st.set_page_config(page_title="StudyDaddy", layout="wide") 

	# Initialize session states
	if "processing_complete" not in st.session_state:
		st.session_state.processing_complete = False
	if "uploader_key" not in st.session_state:
		st.session_state.uploader_key = 0
	if "messages" not in st.session_state:
		st.session_state.messages = []
	if "max_search_queries" not in st.session_state:
		st.session_state.max_search_queries = 5  # Default value of 5
	if "chunk_size" not in st.session_state:
		st.session_state.chunk_size = 1000
	if "chunk_overlap" not in st.session_state:
		st.session_state.chunk_overlap = 200
	if "files_ready" not in st.session_state:
		st.session_state.files_ready = False  # Tracks if files are uploaded but not processed
	if "enable_rag" not in st.session_state:
		st.session_state.enable_rag = False

	# Title row with clear button
	col1, col2 = st.columns([6, 1])
	with col2:
		if st.button("Clear Chat", use_container_width=True):
			clear_chat()
			st.rerun()

	# Sidebar configuration
	st.sidebar.title("StudyDaddy")

	# Theme toggle
	with st.sidebar:  
		is_dark_mode = st.sidebar.toggle("Dark Mode", value=False)
	set_custom_theme(is_dark_mode, st)

	# Maximum search queries input
	st.session_state.max_search_queries = st.sidebar.number_input(
		label="Number of search queries",
		min_value=1,
		max_value=10,
		value=st.session_state.max_search_queries,
		help="The maximum number of search queries LLM can make. (1-10)"
	)
	
	enable_web_search = st.sidebar.checkbox("Enable Web Search", value=False)
	st.session_state.enable_rag = st.sidebar.checkbox("Enable RAG", value=st.session_state.enable_rag)
	
	# Chunk overlap
	st.session_state.chunk_overlap = st.sidebar.slider(
		label="Chunk overlap",
		min_value=0,
		max_value=400,
		value=st.session_state.chunk_overlap,
		help="Makes sure important information at the edges is repeated in the next piece so nothing gets lost (Recommended 200-400)"
	)

	# Chunk size
	st.session_state.chunk_size = st.sidebar.slider(
		label="Chunk size",
		min_value=0,
		max_value=2000,
		value=st.session_state.chunk_size,
		help="How big each piece of text is when splitting a document (Recommended 1000-2000)"
	)

	# Upload file logic
	uploaded_files = st.sidebar.file_uploader(
		label="Upload Study Materials",
		type=["pdf", "txt", "csv", "md"],
		accept_multiple_files=True,
		key=f"uploader_{st.session_state.uploader_key}",
		help="Gives LLM context to reference"
	)

	# Check if files are uploaded but not yet processed
	if uploaded_files:
		logger.info(f"{len(uploaded_files)} files uploaded.")
		st.session_state.enable_rag = True
		st.session_state.files_ready = True  # Mark that files are available
		st.session_state.processing_complete = False  # Reset processing status

	# Display the "Upload files" button when user upload files 
	if st.session_state.files_ready and not st.session_state.processing_complete:
		process_button_placeholder = st.sidebar.empty()  

		with process_button_placeholder.container():
			process_clicked = st.button("Upload files", use_container_width=True)

		if process_clicked:
			with process_button_placeholder:
				with st.status("Processing files...", expanded=False) as status:
					logger.info("Starting file processing.")
					if process_uploaded_files(uploaded_files, st.session_state.chunk_size, st.session_state.chunk_overlap):
						st.session_state.processing_complete = True
						st.session_state.files_ready = False  # Reset files ready flag
						st.session_state.uploader_key += 1  # Reset uploader to allow new uploads
						logger.info("Files processed successfully.")

					status.update(label="Files uploaded successfully!", state="complete", expanded=False)
	
	
	# Display chat messages
	for index, message in enumerate(st.session_state.messages):
		with st.chat_message(message["role"]):
			st.write(message["content"])  # Show the message normally

			# Show copy button only for AI messages at the bottom
			if message["role"] == "assistant":
				if st.button("📋", key=f"copy_{index}"):
					pyperclip.copy(message["content"])

	
	# Chat input and response handling
	if user_input := st.chat_input("Ask anything"):
		# Add user message
		st.session_state.messages.append({"role": "user", "content": user_input})
		with st.chat_message("user"):
			st.write(user_input)

		# Generate and display assistant response
		assistant_response = generate_response(
			user_input, 
			st
		)

		# Store assistant message
		st.session_state.messages.append({"role": "assistant", "content": assistant_response["final_answer"]})

		with st.chat_message("assistant"):
			st.write(assistant_response["final_answer"])  # Deepseek response

			# Copy button below the AI message
			if st.button("📋", key=f"copy_{len(st.session_state.messages)}"):
				pyperclip.copy(assistant_response["final_answer"])

if __name__ == "__main__":
    main()