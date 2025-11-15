# backend/core/youtube_auth.py
import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

router = APIRouter(prefix="/auth", tags=["YouTube OAuth"])

# Google OAuth 2.0 scopes
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly"
]

# Path to your client_secret.json
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")

# 1️⃣ Start OAuth flow
@router.get("/login")
def login_with_google():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/oauth2callback"
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return RedirectResponse(auth_url)

# 2️⃣ Callback handler
@router.get("/oauth2callback")
def oauth2callback(request: Request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/oauth2callback"
    )
    flow.fetch_token(authorization_response=str(request.url))
    creds = flow.credentials

    # Example: fetch channel analytics
    youtube = build("youtube", "v3", credentials=creds)
    analytics = build("youtubeAnalytics", "v2", credentials=creds)

    # Basic channel info
    channel_resp = youtube.channels().list(
        part="snippet,statistics,brandingSettings",
        mine=True
    ).execute()

    # Basic analytics example
    analytics_resp = analytics.reports().query(
        ids="channel==MINE",
        startDate="2024-01-01",
        endDate="2024-12-31",
        metrics="views,watchTime,averageViewDuration",
        dimensions="day"
    ).execute()

    return JSONResponse({
        "channel_info": channel_resp,
        "analytics_sample": analytics_resp
    })
