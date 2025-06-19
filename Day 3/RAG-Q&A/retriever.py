# retriever.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

class DocumentRetriever:
    def __init__(self, persist_directory="chroma_db"):
        print(f"Loading Chroma DB from: {persist_directory}")
        # Use the same model that was used for indexing (384 dimensions)
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",  # This model has 384 dimensions
            model_kwargs={'device': 'cpu'}
        )
        
        # Check if DB exists
        if not os.path.exists(persist_directory):
            print("⚠️ Warning: No existing database found. Please run the indexing script first.")
            return
            
        self.vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model
        )
    
    def get_relevant_documents(self, query: str, k: int = 4):
        try:
            if not hasattr(self, 'vectordb'):
                raise Exception("Database not initialized. Please run the indexing script first.")
            docs = self.vectordb.similarity_search(query, k=k)
            return docs
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
