# 🧾 AI Bill Management Agent

A Streamlit app that uses Google Gemini Vision and AutoGen agents to extract, categorize, and summarize expenses from uploaded bill images. Upload a photo of your bill and let the AI handle expense categorization and trend analysis!

---

## Features

- **Bill Image Analysis:**  
  Upload a bill (JPG/PNG), and Gemini Vision extracts all expenses.
- **Automatic Categorization:**  
  Expenses are grouped into categories: Groceries, Dining, Utilities, Shopping, Entertainment, Others.
- **Expense Summarization:**  
  The AI summarizes total spending, category-wise totals, and highlights unusual spending patterns.
- **Multi-Agent Workflow:**  
  Uses AutoGen agents for bill processing and expense summarization, simulating a collaborative workflow.
- **Interactive UI:**  
  View categorized expenses, a natural language summary, and a chat log of agent interactions.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Bill_Management_Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Your `requirements.txt` should include:
   ```
   streamlit
   pillow
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
   - Upload a bill image (JPG or PNG).
   - Wait for the AI to extract and categorize expenses.
   - View the categorized expenses, summary, and agent chat log.

---

## How It Works

- The app loads your Gemini API key and initializes the Gemini Vision model.
- When you upload a bill image, the model extracts expenses and groups them by category.
- AutoGen agents simulate a workflow: bill processing, categorization, and summarization.
- The results and agent interactions are displayed in the Streamlit UI.

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
- [Streamlit](https://streamlit.io/)