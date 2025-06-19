# Conversion Obstacle Analyzer 🔍

An AI-powered system that autonomously identifies and resolves hidden friction points in website user journeys to improve conversion outcomes.

## 🎯 Problem Statement

Many websites, despite being visually appealing, suffer from high bounce rates due to hidden friction points in the user journey. This tool helps identify and resolve these issues using multiple AI agents.

## 🤖 Key Features

### Multi-Agent System
- **User Flow Simulation Agent**: Emulates different user personas navigating the site
- **Friction Detection Agent**: Identifies high-drop-off elements and confusion points
- **Benchmarking Agent**: Uses RAG to compare against industry best practices
- **UX Optimization Agent**: Provides actionable UI/UX improvements

### Technologies Used
- LangChain for agent orchestration
- Google Gemini for AI processing
- FAISS for vector storage
- FastAPI for backend API
- Streamlit for user interface

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kaviyarasanIhub/Agentic_AI_Workshop.git
direct to appropriate folder(day9)
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Google API key:
```bash
set GOOGLE_API_KEY=your_api_key_here
```

### Running the Application

1. Start the FastAPI server:
```bash
uvicorn api:app --reload
```

2. Launch the Streamlit UI:
```bash
streamlit run ui.py
```

3. Open your browser and navigate to:
- API: http://127.0.0.1:8000
- UI: http://localhost:8501

## 📊 Usage

1. Enter your website's HTML code
2. Define user personas (or use defaults)
3. Click "Analyze Website"
4. Review the comprehensive analysis:
   - User journey simulations
   - Friction point detection
   - Benchmark comparisons
   - UX recommendations

## 🔧 API Endpoints

### POST /analyze
Analyzes a website for friction points and improvements.

**Request Body:**
```json
{
    "html_content": "string",
    "personas": ["string"]
}
```

**Response:**
```json
{
    "user_journeys": [],
    "friction_points": {},
    "benchmark_analysis": {},
    "ux_recommendations": {}
}
```

