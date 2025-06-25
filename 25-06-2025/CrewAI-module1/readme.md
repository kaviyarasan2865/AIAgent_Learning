# CrewAI Logistics Optimization Workflow

This project demonstrates a multi-agent workflow for logistics optimization using [CrewAI](https://github.com/joaomdmoura/crewAI) and Google Gemini LLM.

## Features
- **Multi-agent CrewAI workflow**: Logistics Analyst and Optimization Strategist agents collaborate to analyze and optimize logistics operations.
- **Gemini LLM integration**: Uses Google Gemini for advanced reasoning and report generation.
- **Sample logistics data**: Includes delivery routes and inventory turnover for realistic analysis.

## Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd CrewAI-module1
```

### 2. Install Dependencies
CrewAI and Google Generative AI SDK are required. Install with pip:
```bash
pip install crewai google-generativeai
```

### 3. Set Up Gemini API Key
Obtain your [Google Gemini API key](https://aistudio.google.com/app/apikey) and set it as an environment variable:

**On Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-gemini-api-key"
```
**On Linux/macOS:**
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

## Usage

Run the main workflow script:
```bash
python main.py
```

You should see agent outputs and the final optimization plan in the terminal.

## Customization
- **Logistics Data**: Edit the `logistics_data` dictionary in `main.py` to use your own routes and inventory.
- **Agent Goals/Backstories**: Adjust the `goal` and `backstory` fields for each agent to fit your use case.
- **LLM Settings**: Change the `model` or `temperature` in the `LLM` setup for different behaviors.

## Troubleshooting
- **API Key Errors**: Ensure your `GOOGLE_API_KEY` is set and valid.
- **Dependency Issues**: Run `pip install -r requirements.txt` if you add a requirements file.
- **CrewAI Docs**: See [CrewAI documentation](https://docs.crewai.com/) for advanced usage.

## License
MIT License
