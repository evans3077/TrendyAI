from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .service import analyze_video
import traceback

router = APIRouter(prefix="/video", tags=["Video Analyzer"])

@router.post("/analyze")
async def analyze_uploaded_video(file: UploadFile = File(...)):
    """
    Upload a video, extract transcript + summary.
    """
    try:
        result = await analyze_video(file)
        return JSONResponse(content=result)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")


