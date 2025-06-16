# preprocessing.py

import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

CHROMA_DIR = "chroma_db"

def load_and_chunk_documents(pdf_dir="data/"):
    """
    Load PDF files from the given directory and split them into text chunks.
    """
    all_docs = []

    for file_name in os.listdir(pdf_dir):
        if file_name.endswith(".pdf"):
            print(f"Loading: {file_name}")
            loader = PyPDFLoader(os.path.join(pdf_dir, file_name))
            documents = loader.load()
            all_docs.extend(documents)

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)

    return chunks

def create_chroma_vectorstore(chunks, persist_directory=CHROMA_DIR):
    """
    Generate embeddings from chunks and store them in Chroma DB.
    """
    print("Generating embeddings and creating Chroma DB...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    vectordb.persist()
    print(f"Chroma DB saved to: {persist_directory}")

def run_preprocessing(pdf_dir="data/"):
    """
    Full preprocessing pipeline: Load -> Chunk -> Vectorize -> Save
    """
    chunks = load_and_chunk_documents(pdf_dir)
    create_chroma_vectorstore(chunks)

if __name__ == "__main__":
    run_preprocessing()
