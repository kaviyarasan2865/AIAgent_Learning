# 🎓 Personalized Educational Recommendations

A Streamlit app that generates a complete learning path—including curated learning materials, quizzes, and project ideas—for any topic and skill level. Powered by Google Gemini, CrewAI, and Serper API for real-time web search.

---

## Features

- **Learning Material Curator:**  
  Finds the best videos, articles, and exercises for your chosen topic using live web search.
- **Quiz Master:**  
  Generates multiple-choice quiz questions to test your understanding.
- **Project Mentor:**  
  Suggests hands-on project ideas tailored to your skill level.
- **Multi-Agent Collaboration:**  
  Uses CrewAI to simulate expert agents working together.
- **Interactive Streamlit UI:**  
  Enter your topic and level, then get a structured learning path in seconds.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Personalized_Educational_Recommendations
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Your `requirements.txt` should include:
   ```
   streamlit
   python-dotenv
   google-generativeai
   langchain-google-genai
   crewai
   pydantic
   requests
   ```

3. **Set up your API keys**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     SERPER_API_KEY=your_serper_api_key
     ```
   - Get your Gemini key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Get your Serper key from [serper.dev](https://serper.dev/)

---

## Usage

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **In your browser:**
   - Enter your learning topic (e.g., "Machine Learning").
   - Select your skill level (Beginner, Intermediate, Advanced).
   - Click **Generate Learning Path**.
   - Explore the tabs for curated materials, quizzes, and project ideas.

---

## How It Works

- The app loads your API keys and initializes Gemini and CrewAI agents.
- When you enter a topic and level, the agents:
  1. Search the web for up-to-date learning resources.
  2. Generate quiz questions using Gemini.
  3. Suggest practical projects for your level.
- Results are displayed in a user-friendly, tabbed interface.

---

## Security

- **Never share your `.env` or API keys publicly.**
- `.env` and virtual environments should be excluded in `.gitignore`.

---

## License

MIT License

---

## Credits

- [Google Gemini](https://aistudio.google.com/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Serper API](https://serper.dev/)
- [Streamlit](https://streamlit.io/)