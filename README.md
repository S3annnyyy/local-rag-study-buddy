# StudyBuddy: Local RAG Agent built with Deepseek R1 and Langgraph
I built a corrective AI RAG agent using LangGraph and DeepSeek R1 model running on Ollama. This agent acts like a study buddy, designed to help students summarize their notes and answer their queries.
![rag_demo_2 (1)](https://github.com/user-attachments/assets/481c0589-5938-44bd-add1-dc0bba187bca)

# RAG Architecture
![image](https://github.com/user-attachments/assets/9fa3b5b3-ac08-4e2c-9ab1-ece947ef0b41)

# How to run
Ensure you have Python `3.10.9` or higher, pip `24.0` or higher installed.

### Clone repository
```
git clone https://github.com/S3annnyyy/local-rag-study-buddy.git
cd local-rag-study-buddy 
```

### Configuring environment.
1. Obtain Tavily API Key by creating free-tier account from [Tavily AI](https://tavily.com/)
2. Create `.env,local` file under the root folder in this manner:
```
TAVILY_API_KEY=XXX
```
3. Create virtual environment in root folder
```
python -m venv .venv
```
4. Activate environment by running `.venv/Scripts/Activate.ps1` for Windows Powershell or `source .venv/bin/activate` for MacOs/Linux 
5. Install [ollama](https://www.ollama.com/) and download deepseek-R1 model by running the following in command prompt: (You can choose bigger models)
```
ollama pull deepseek-r1:1.5b
ollama run deepseek-r1:1.5b
~Should take about 5 minutes unless your laptop trashy af 
```

### Install dependencies with:
```
pip install -r requirements.txt
```

Once it's done start up by running this command in the terminal:
```
streamlit run app.py
```

# Visualizing workflow with LangGraph Studio
![rag_workflow](https://github.com/user-attachments/assets/de997d3d-86b5-4d9d-b0d6-e1af3c035e1a)
1. Sign up for an account [here](https://smith.langchain.com/) and create an API key
2. Add API key to `.env.local`
```
LANGSMITH_API_KEY=lsv2_***
```
3. Run the following commands
```
pip install -U "langgraph-cli[inmem]"
langgraph dev
```
4. An interface will popup and you can test the worklow through inputs
