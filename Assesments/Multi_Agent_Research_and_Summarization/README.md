# 🧠 Multi-Agent Research and Summarization Assistant

This project is a fully agentic research assistant built with Streamlit, LangChain, LangGraph, and Google Gemini. It can answer questions by searching the web, retrieving from your own documents, or using the Gemini LLM—then summarizes the results for you.

---

## Features

- **Multi-Agent Pipeline:**  
  Routes your query to the best agent: Web Search, Retrieval-Augmented Generation (RAG), or LLM.
- **Document Support:**  
  Upload PDFs, DOCX, or TXT files to the `rag` folder for custom knowledge retrieval.
- **Web Search Integration:**  
  Uses DuckDuckGo for real-time web answers.
- **Gemini LLM:**  
  Uses Google Gemini 1.5 Flash for reasoning and summarization.
- **Automatic Summarization:**  
  All answers are summarized for clarity.
- **Streamlit UI:**  
  Simple web interface for asking questions and viewing answers.

---

## How the Code Works

1. **Configuration & LLM Setup**
   - Loads your Google Gemini API key from `.env`.
   - Initializes Gemini LLM and embedding model.

2. **File Parsing**
   - Reads all `.pdf`, `.docx`, and `.txt` files in the `rag` folder.
   - Splits documents into chunks and creates a FAISS vector store for retrieval.

3. **Agents**
   - **Router Agent:** Decides if the query should go to Web Search, RAG, or LLM.
   - **Web Agent:** Uses DuckDuckGo to answer.
   - **RAG Agent:** Retrieves from your documents and answers using Gemini.
   - **LLM Agent:** Answers directly using Gemini.
   - **Summarizer Agent:** Summarizes the answer.

4. **LangGraph Workflow**
   - Orchestrates the flow: Router → (Web/RAG/LLM) → Summarizer.

5. **Streamlit App**
   - Loads documents (if any).
   - Accepts user questions.
   - Runs the agentic workflow and displays the summarized answer.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Multi_Agent_Research_and_Summarization
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *If you see errors about missing packages, also run:*
   ```bash
   pip install streamlit langchain langgraph pdfplumber python-docx faiss-cpu google-generativeai duckduckgo-search python-dotenv
   ```

3. **Set up your Google Gemini API key**
   - Create a `.env` file in the project root:
     ```
     GOOGLE_API_KEY=your_gemini_api_key
     ```
   - Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)

4. **(Optional) Add your documents**
   - Place `.pdf`, `.docx`, or `.txt` files in a folder named `rag` in the project directory.

---

## Running the App

```bash
streamlit run app.py
```

- Open the provided local URL in your browser.
- Enter your question and click **Submit**.
- The app will display a summarized answer, using web search, your documents, or Gemini as appropriate.

---

## Notes

- If no documents are found, the app uses a small fallback knowledge base.
- Make sure your `.env` file is **not** committed to GitHub for security.
- The app is modular and easy to extend with more agents or tools.

---

## License

MIT License

---

## Credits

- [LangChain](https://langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Gemini](https://aistudio.google.com/)
-