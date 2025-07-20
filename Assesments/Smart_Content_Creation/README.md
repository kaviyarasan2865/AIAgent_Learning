# 📝 Smart Content Creation: Agentic AI Content Refinement

This Streamlit app simulates a conversation between two AI agents—a Content Creator and a Content Critic—powered by Google Gemini and AutoGen. The Creator drafts and revises technical content, while the Critic provides structured feedback, resulting in high-quality, markdown-formatted educational material.

---

## Features

- **Agentic Collaboration:**  
  - Content Creator Agent: Drafts and revises technical content on a chosen topic.
  - Content Critic Agent: Evaluates content for technical accuracy, clarity, and depth, and suggests improvements.
- **LLM-Powered:**  
  Uses Google Gemini 1.5 Flash for all content generation and critique.
- **Interactive UI:**  
  Choose your topic and number of conversation turns, then watch the agents refine the content in real time.
- **Markdown Output:**  
  All content is structured in markdown for easy reuse.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Smart_Content_Creation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Make sure your `requirements.txt` includes:
   ```
   streamlit
   google-generativeai
   autogen
   langchain-google-genai
   python-dotenv
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
   - Enter a discussion topic (e.g., "Agentic AI").
   - Select the number of conversation turns.
   - Click **Start Simulation** to watch the agents collaborate and refine the content.

3. **Review the results:**
   - The final, refined content is shown at the end.
   - Expandable sections show the full conversation trace between the Creator and Critic agents.

---

## How It Works

- The app uses two agent classes (Creator and Critic), each with a system prompt and access to Gemini via LangChain.
- On each turn, the Creator generates or revises content, and the Critic provides feedback.
- The process repeats for the selected number of turns, simulating iterative content refinement.
- All interactions and outputs are displayed in the Streamlit interface.

---

## Security

- **Never share your `.env` or API key publicly.**
- The `.gitignore` file should exclude `.env` and virtual environments.

---

## License

MIT License

---

## Credits

- [Google Gemini](https://aistudio.google.com/)
- [Microsoft AutoGen](https://github.com/microsoft/autogen)
- [LangChain](https://langchain.com/)
- [Streamlit](https://streamlit.io/)