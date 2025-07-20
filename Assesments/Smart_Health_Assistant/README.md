# 🤖 Smart Health Assistant

A multi-agent Streamlit app that generates a personalized health plan—including BMI calculation, health recommendations, meal plans, and workout schedules—using Google Gemini 1.5 Flash and Microsoft AutoGen.

---

## Features

- **Conversational Multi-Agent System:**  
  - **BMI Agent:** Calculates BMI, categorizes it, and provides health advice.
  - **Diet Planner Agent:** Creates meal plans tailored to your BMI and dietary preference.
  - **Workout Scheduler Agent:** Designs a weekly workout plan based on your age, gender, and meal plan.
  - **User Proxy Agent:** Shares your health data with other agents and coordinates the workflow.
- **Gemini LLM Powered:**  
  Uses Google Gemini 1.5 Flash for all reasoning and content generation.
- **Interactive Streamlit UI:**  
  Enter your details, generate your plan, and download the results.
- **Secure:**  
  API key is entered via the sidebar and never stored.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assesments/Smart_Health_Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Your `requirements.txt` should include:
   ```
   streamlit
   google-generativeai
   autogen
   python-dotenv
   ```

3. **Get your Gemini API key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your key.

---

## Usage

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **In your browser:**
   - Enter your Gemini API key in the sidebar.
   - Fill in your weight, height, age, gender, and dietary preference.
   - Click **Generate Health Plan**.
   - View the agent conversation and download your personalized plan.

---

## How It Works

- The app collects your health data and preferences.
- Agents collaborate (using AutoGen) to:
  1. Calculate and analyze your BMI.
  2. Generate a meal plan.
  3. Create a workout schedule.
- All steps and results are shown in the UI, with the final plan available for download.

---

## Security

- **Never share your API key publicly.**
- `.env` and virtual environments should be excluded in `.gitignore`.

---

## License

MIT License

---

## Credits

- [Google Gemini](https://aistudio.google.com/)
- [Microsoft AutoGen](https://github.com/microsoft/autogen)