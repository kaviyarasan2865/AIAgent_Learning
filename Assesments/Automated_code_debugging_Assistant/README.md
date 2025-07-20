# 🔍 Automated Code Debugging Assistant (No ONNX)

A Streamlit app that reviews and fixes Python code using static analysis (AST) and Google Gemini LLM—**no ONNX, no code execution, and no external runtime dependencies**. Powered by CrewAI multi-agent orchestration.

---

## Features

- **Static Code Analysis:**  
  Uses Python's AST to find common issues (e.g., print statements, bare excepts, syntax errors) without running the code.
- **LLM-Powered Correction:**  
  Google Gemini 2.5 Flash suggests fixes and explanations for detected issues.
- **Multi-Agent Workflow:**  
  - **Analyzer Agent:** Finds static issues.
  - **Corrector Agent:** Fixes code and explains changes.
  - **Manager Agent:** Coordinates the review process.
- **Streamlit UI:**  
  Paste your Python code, click "Analyze & Fix", and get a corrected version with explanations.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Automated_code_debugging_Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Your `requirements.txt` should include:
   ```
   streamlit
   python-dotenv
   crewai
   langchain-google-genai
   google-generativeai
   ```

3. **Set up your Gemini API key**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     ```
   - Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## Usage

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **In your browser:**
   - Paste your Python code into the text area.
   - Click **Analyze & Fix**.
   - View the fixed code and explanations.

---

## How It Works

- The app uses AST parsing for static analysis (no code execution).
- CrewAI agents (Analyzer, Corrector, Manager) collaborate using Gemini LLM to review and fix code.
- All results are shown in the Streamlit interface.

---

## Security

- **Never share your `.env` or API key publicly.**
- `.env` and virtual environments should be excluded in `.gitignore`.

---

## License

MIT License

---

## Credits

- [Google Gemini](https://aistudio.google.com/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Streamlit](https://streamlit.io/)