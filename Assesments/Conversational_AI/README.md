# 👗 Clothing Store Competitor Intelligence (Conversational AI)

A Streamlit app that uses multi-agent AI (AutoGen + Gemini 1.5 Flash) to generate detailed competitor analysis reports for clothing stores in any location.

---

## Features

- **Multi-agent architecture**: Research Analyst, Strategy Consultant, and Report Compiler agents collaborate to analyze competitors.
- **Powered by Google Gemini 1.5 Flash** for advanced reasoning and summarization.
- **Customizable**: Choose location, number of competitors, and detail level.
- **Professional reports**: Output includes tables, bullet points, and actionable recommendations.
- **Downloadable Markdown reports**.

---

## Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Assesments/Conversational_AI
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**

   - You can enter your Gemini API key in the sidebar when running the app.
   - Or, for convenience, create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## Usage

- Enter your Gemini API key (from [Google AI Studio](https://aistudio.google.com/app/apikey)) in the sidebar.
- Set your location, number of competitors, and detail level.
- Click **Generate Report**.
- View and download the generated competitor analysis.

---

## Security

- **Never share your API key publicly.**
- The `.gitignore` file excludes `.env` and virtual environments.

---

## License

MIT License

---

## Credits

- [AutoGen](https://github.com/microsoft/autogen)
- [LangChain](https://langchain.com/)
- [Google Gemini](https://aistudio.google.com/)