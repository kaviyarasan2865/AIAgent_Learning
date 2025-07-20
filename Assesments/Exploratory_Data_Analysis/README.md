# 🔍 Agentic Exploratory Data Analysis (EDA) with Gemini + AutoGen

This project is a Streamlit app that performs Exploratory Data Analysis (EDA) on CSV datasets using a multi-agent system powered by Google Gemini and Microsoft AutoGen. Each agent specializes in a step of the EDA process, from data cleaning to report generation and critique.

---

## Features

- **Multi-Agent Architecture:**  
  - **DataPrepAgent:** Cleans and preprocesses the data.
  - **EDAAgent:** Extracts insights and suggests visualizations.
  - **ReportGeneratorAgent:** Compiles a professional EDA report.
  - **CriticAgent:** Reviews and critiques the report.
  - **ExecutorAgent:** Validates the generated preprocessing code.
- **LLM-Powered Reasoning:**  
  Uses Google Gemini 1.5 Flash for all agent reasoning and code generation.
- **Interactive Streamlit UI:**  
  Upload your CSV, run the analysis, and view each agent's output in expandable sections.
- **No Docker Required:**  
  Code execution is disabled for security and simplicity.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Exploratory_Data_Analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If you encounter issues, ensure you have:
   ```
   streamlit
   pandas
   python-dotenv
   google-generativeai
   autogen
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
   - Upload a CSV file.
   - Click **"Run Agentic EDA"**.
   - Explore the outputs from each agent in the expandable sections.

---

## How It Works

- The app loads your CSV and stores it in the session state.
- Each agent (subclass of `AssistantAgent`) receives the data and a role-specific prompt.
- Agents use Gemini to generate code, insights, reports, and critiques.
- All outputs are displayed in the Streamlit interface for easy review.

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