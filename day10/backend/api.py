from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from agents.workflow import run_bug_fixer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BugFixRequest(BaseModel):
    input_data: Dict[str, Any]

class BugFixResponse(BaseModel):
    result: Any

@app.post("/api/bug-fix", response_model=BugFixResponse)
def bug_fix(request: BugFixRequest):
    try:
        result = run_bug_fixer(request.input_data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health():
    return {"status": "ok"}
