import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from logger import logger

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY") # For Vector embeddings
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY") # Vector db store
PINECONE_ENV="us-east-1"
PINECONE_INDEX_NAME="chat-md-index"

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

UPLOAD_DIR="./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# PINECONE init
pinecone=Pinecone(api_key=PINECONE_API_KEY)
spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
curr_indexes = [i["name"] for i in pinecone.list_indexes()]

if PINECONE_INDEX_NAME not in curr_indexes:
    pinecone.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="dotproduct", # can also use cosine
        spec=spec
    )

    logger.info("RAG process started")

    while not pinecone.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        logger.info(f"Pinecone index {PINECONE_INDEX_NAME} not created yet, sleeping for 1 second")
        time.sleep(1)

index = pinecone.Index(PINECONE_INDEX_NAME)

# Load, Split, Embed, and Upsert PDF DOCS Content
def upload_vectorstore(uploaded_files):
    embed_model=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths=[] # successfully uploaded files paths

    # UPLOAD
    for file in uploaded_files:
        save_path=Path(UPLOAD_DIR)/file.filename # create location for file to be stored
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # SPLIT
    for file_path in file_paths:
        loader=PyPDFLoader(file_path)
        documents=loader.load()

        splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks=splitter.split_documents(documents)

        # return context used
        texts = [chunk.page_content for chunk in chunks]
        metadata = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"Embedding chunks {len(chunks)}")
        embedding=embed_model.embed_documents(texts)

        for i in range(len(ids)):
            metadata[i]["chunk"] = i
        
        print("Upserting embeddings...")
        with tqdm(total=len(embedding), desc="Upsert embeddings") as progress:
            index.upsert(vectors=zip(ids, embedding, metadata))
            progress.update(len(embedding))

        print(f"Upload complete for {file_path}")


