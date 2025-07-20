# 🤖 Agentic Math & Knowledge Assistant

A Python agent that combines Google Gemini LLM with custom mathematical tools for interactive Q&A. The agent can answer general knowledge questions and perform math calculations using addition, subtraction, multiplication, and division tools.

---

## Features

- **Conversational agent** powered by Gemini 1.5 Flash (via LangChain)
- **Custom math tools**: addition, subtraction, multiplication, division (with zero-division handling)
- **Agent chooses when to use tools** for math, or answers directly for general knowledge
- **Interactive command-line chat interface**
- **Agent state and workflow managed by LangGraph**

---

## Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Assesments/Create_an_Agent_Using_LLM_and_Custom_Mathematical_Functions
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**

   - Create a `.env` file in the project root:
     ```
     GOOGLE_API_KEY=your_gemini_api_key
     ```
   - Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)

4. **Run the agent**

   ```bash
   python app.py
   ```

---

## Usage

- Type your question or math problem at the prompt.
- The agent will respond, using tools for math when needed.
- Type `exit` or `quit` to end the session.

**Examples:**
```
You: What is the capital of France?
Agent: The capital of France is Paris.

You: What is 12.5 * 8.2?
Agent: The result of multiplying 12.5 by 8.2 is 102.5.
```

---

## Security

- **Never share your `.env` file or API key publicly.**
- The `.gitignore` file excludes `.env` and virtual environments.

---

## License

MIT License

---

## Credits

- [LangChain](https://langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Gemini](https://aistudio.google.com/)