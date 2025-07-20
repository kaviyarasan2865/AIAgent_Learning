# 🌍 Travel Assistant AI

A conversational AI travel assistant built with Streamlit, LangChain, and Google Gemini. Instantly get weather, attractions, and accommodation recommendations for any destination!

---

## Features

- **Conversational Chat UI** for travel planning
- **Live Weather** using WeatherAPI (with OpenWeatherMap fallback)
- **Top Attractions** via DuckDuckGo search + Gemini summarization
- **Personalized Accommodation** suggestions by travel style
- **All powered by Google Gemini LLM**

---

## Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Assesments/Travel_Assistant_AI
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys**

   Create a `.env` file in the project root with:

   ```
   WEATHER_API_KEY=your_weatherapi_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

   - Get a [WeatherAPI key](https://www.weatherapi.com/)
   - Get a [Google Gemini API key](https://aistudio.google.com/app/apikey)

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at [http://localhost:8501](http://localhost:8501).

---

## How it works

- Loads API keys from `.env` using `python-dotenv`
- Uses Gemini LLM for summarization and chat
- Weather and search tools are called dynamically by the agent
- All chat history and results are shown in the Streamlit UI

---

## Security

- **Never commit your `.env` file or API keys to GitHub.**
- `.gitignore` already excludes `.env` and virtual environments.

---

## License

MIT License

---

## Credits

- [Google Gemini](https://aistudio.google.com/)
- [LangChain](https://langchain.com/)
-