# 💼 Financial Portfolio Manager

A Streamlit app that uses multi-agent AI (AutoGen + Gemini 2.5 Flash) to analyze your financial portfolio and generate a personalized investment report. The system simulates a team of financial experts—Portfolio Analyst, Growth/Value Strategist, and Financial Advisor—collaborating to provide actionable recommendations.

---

## Features

- **Conversational Multi-Agent System:**  
  - **Portfolio Analyst:** Analyzes your current investments and financial profile.
  - **Growth/Value Strategist:** Suggests tailored investment options based on your strategy.
  - **Financial Advisor:** Compiles a comprehensive, markdown-formatted report with recommendations and risk assessment.
- **Gemini LLM Powered:**  
  Uses Google Gemini 2.5 Flash for all reasoning and content generation.
- **Interactive Streamlit UI:**  
  Enter your salary, age, expenses, goals, risk tolerance, and portfolio details to get a custom report.
- **Secure:**  
  API key is loaded from your `.env` file and never stored in code.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Financial_Portfolio_Manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Your `requirements.txt` should include:
   ```
   streamlit
   autogen
   google-genai
   vertexai
   python-dotenv
   ```

3. **Set up your Gemini API key**
   - Create a `.env` file in the project root:
     ```
     GOOGLE_API_KEY=your_gemini_api_key
     ```
   - Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## Usage

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **In your browser:**
   - Fill in your financial details and portfolio.
   - Click **Generate Report**.
   - View your personalized investment report, including strategy, recommendations, and risk assessment.

---

## How It Works

- The app collects your financial profile and portfolio.
- Agents collaborate (using AutoGen) to:
  1. Analyze your portfolio and determine a strategy (Growth or Value).
  2. Suggest specific investments based on your strategy.
  3. Compile a comprehensive report with actionable steps and risk analysis.
- All outputs are displayed in the Streamlit interface.

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
- [Microsoft AutoGen](https://github.com/microsoft/autogen)
