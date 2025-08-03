# ChatMD
Welcome to ChatMD, an AI-powered chatbot that helps you quickly learn and summarize medical information. 

This project implements a full-stack RAG (Retrieval-Augmented Generation) pipeline using industry standard tools, including
- LangChain
- Pinecone
- Google Embeddings
- Groq's LLaMA 3 LLM model
  
To create domain-specific answers to medical queries using real PDF documents.

Feel free to play with the deployed project [here](https://chatmd.streamlit.app/)

# Demo

# System Architecture

![IMG_0942](https://github.com/user-attachments/assets/6d908320-402f-42f0-822a-ac8b6ff4bca4)

# Features
- Uploading and processing PDFs
- Chunking + embedding with **LangChain**
- Semantic search w/ **(Pinecone) Vector DB**
- LLM response generation with **Groq's LLaMA3-70B**
- Backend using **FastAPI (deployment via Render)**
- Frontend using **Streamlit**

# Setup

### Get UV Python package manager
- `curl -LsSf https://astral.sh/uv/install.sh | sh`
- check if successfully installed with `uv -V`

### Setup prerequisites
0. Get API keys for the following and put it in a `/server/.env` file
    - `GOOGLE_API_KEY`
    - `PINECONE_API_KEY`
    - `PINECONE_INDEX_NAME`
    - `GROQ_API_KEY`
1. `source .venv/bin/activate`
2. `cd server`
3. `uv pip install -r requirements.txt`

### Start server     
- make sure you are in the server directory
- `uvicorn test:app --reload`
- `uvicorn main:app --reload`

### Start client
- make sure you are in the client directory
- `uv pip install -r requirements.txt`
- `streamlit run app.py`
