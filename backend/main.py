# backend/main.py
from fastapi import FastAPI
from backend.api.channel_context.router import router as channel_router
from backend.api.video_analyzer.router import router as video_router
from backend.core.youtube_auth import router as youtube_auth_router
from backend.api.content_analyzer.router import router as content_router



app = FastAPI()

app.include_router(channel_router)
app.include_router(video_router)
app.include_router(youtube_auth_router)
app.include_router(content_router)

@app.get("/")
def root():
    return {"message": "Welcome to Trendy AI Platform!"}


