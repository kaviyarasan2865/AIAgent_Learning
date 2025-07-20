# AI Study Assistant for Quiz Question Generation

This Streamlit app lets you upload a study PDF, generates a concise summary, and creates interactive multiple-choice quizzes using Google Gemini LLM.

## Features

- Upload any PDF study material
- Automatic bullet-point summary generation
- 5 high-quality MCQs per document
- Interactive quiz with instant feedback and explanations
- Powered by Gemini 1.5 Flash via LangChain

## Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Study_Assistant_for_Quiz_Question_Generation
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**

   - Create a `.env` file in the project root (already present).
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your-gemini-api-key
     ```
   - Never share your API key publicly.

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

   The app will be available at [http://localhost:8501](http://localhost:8501).

## How it works

- The app loads your API key from `.env` using the `python-dotenv` package.
- The key is accessed in Python with:
  ```python
  import os
  from dotenv import load_dotenv
  load_dotenv()
  api_key = os.getenv("GEMINI_API_KEY")
  ```
- The Gemini LLM is initialized with this key for all AI tasks.

## Security

- **Do not commit your `.env` file or API key to public repositories.**
- The `.gitignore` file already excludes common virtual environments.

##