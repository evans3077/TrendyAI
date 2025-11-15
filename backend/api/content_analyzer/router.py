from fastapi import APIRouter, HTTPException, Query
from backend.api.content_analyzer.service import analyze_job

router = APIRouter(prefix="/content", tags=["Content Analyzer"])

@router.get("/analyze")
def run_analysis(job_path: str = Query(..., description="Path to the job analysis folder")):
    try:
        result = analyze_job(job_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
