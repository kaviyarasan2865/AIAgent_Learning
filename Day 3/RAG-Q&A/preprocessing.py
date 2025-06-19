# preprocessing.py

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
import shutil

def index_documents(docs_dir="./data"):
    # Remove existing DB if it exists
    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")
        print("Removed existing database")
    
    # Initialize the same embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Load PDF documents
    print(f"Loading documents from {docs_dir}")
    loader = DirectoryLoader(docs_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    print(f"Split into {len(splits)} chunks")
    
    # Create vector store (persists automatically)
    print("Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )
    print("✅ Indexing complete!")

if __name__ == "__main__":
    index_documents("E:/Agentic_AI_Workshop/Day 3/RAG-Q&A/data")
