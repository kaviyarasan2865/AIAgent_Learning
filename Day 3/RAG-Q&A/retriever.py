# retriever.py

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

CHROMA_DIR = "chroma_db"

def load_chroma_retriever(persist_directory=CHROMA_DIR):
    """
    Loads the Chroma vector store and returns a retriever object.
    """
    print(f"Loading Chroma DB from: {persist_directory}")

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 4})  # k = top 4 chunks
    return retriever
