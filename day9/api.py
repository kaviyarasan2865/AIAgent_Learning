from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agents import analyze_and_optimize_site

app = FastAPI(
    title="Conversion Obstacle Analyzer",
    description="AI-powered system for detecting and resolving website friction points",
    version="1.0.0"
)

class WebsiteAnalysisRequest(BaseModel):
    html_content: str
    personas: List[str]

class WebsiteAnalysisResponse(BaseModel):
    user_journeys: List[dict]
    friction_points: Optional[dict]
    benchmark_analysis: Optional[dict]
    ux_recommendations: Optional[dict]

@app.post("/analyze", response_model=WebsiteAnalysisResponse)
async def analyze_website(request: WebsiteAnalysisRequest):
    try:
        results = analyze_and_optimize_site(request.html_content, request.personas)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Conversion Obstacle Analyzer API"}