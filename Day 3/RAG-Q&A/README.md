# Create README.md file
content = """# RAG (Retrieval Augmented Generation) Implementation

This is a straightforward implementation of RAG using LangChain, Chroma DB, and Google's Gemini model.

## Components

1. **Retriever** (`retriever.py`)
   - Uses HuggingFace embeddings (all-MiniLM-L6-v2)
   - Stores and retrieves documents using ChromaDB

2. **Generator** (`main.py`)
   - Uses Gemini Pro for text generation
   - Combines retrieved context with user questions

3. **Preprocessor** (`preprocessing.py`)
   - Splits documents into chunks
   - Creates vector embeddings
   - Stores them in ChromaDB

## Quick Start

1. Set up environment:
   ```bash
   pip install langchain-huggingface langchain-chroma google-generativeai python-dotenv sentence-transformers chromadb
   ```

2. Create `.env` file with your Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. Add your PDF documents to the `data/` folder

4. Index your documents:
   ```bash
   python preprocessing.py
   ```

5. Run the RAG system:
   ```bash
   python main.py
   ```

## How it Works

1. **Indexing (preprocessing.py)**
   - Loads PDF documents
   - Splits them into manageable chunks
   - Creates vector embeddings
   - Stores in ChromaDB

2. **Querying (main.py)**
   - Takes user question
   - Finds relevant document chunks
   - Combines with prompt
   - Generates answer using Gemini

## Notes

- Uses 384-dimensional embeddings
- Chunks are 1000 characters with 200 character overlap
- Retrieves top 4 most relevant chunks per query
"""