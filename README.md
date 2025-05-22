# StudyBuddy: Local RAG Agent built with Deepseek R1 and Langgraph
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/558e19c7-11a4-4afd-a87f-0a8c75457c32" />

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
1. Create free-tier accounts from   [Tavily AI](https://tavily.com/)
2. Create `.env,local` file under the root folder in this manner:
```
TAVILY_API_KEY=XXX
```
3. Create virtual environment in root folder
```
python -m venv .venv
```
4. Activate environment by running `.\venv\Scripts\Activate.ps1` for Windows Powershell or `source venv/bin/activate` for MacOs/Linux 
5. Install [ollama](https://www.ollama.com/) and download deepseek-R1 model by running the following in command prompt: (You can choose bigger models)
```
ollama pull deepseek-r1:1.5b
ollama run deepseek-r1:1.5b
~Should take about 5 minutes unless your laptop trashy af 
```

### Install dependencies with:
```
pip install requirements.txt
```

Once it's done start up by running this command in the terminal:
```
streamlit run app.py
```
