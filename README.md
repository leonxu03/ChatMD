# ChatMD
RAG chatbot that uses uploaded PDF vector embeddings as context to answer medical related queries

# Setup

### Get UV Python package manager
- `curl -LsSf https://astral.sh/uv/install.sh | sh`
- check if successfully installed with `uv -V`

### Setup prerequisites
1. `source .venv/bin/activate`
2. `cd server`
3. `uv pip install -r requirements.txt`

### Start server     
- make sure you are in the server directory
- `uvicorn test:app --reload`