# backend/api/channel_context/router.py
from fastapi import APIRouter
from .service import get_channel_data

router = APIRouter(prefix="/channel", tags=["Channel Context"])



@router.get("/{channel_id}")
def fetch_channel_context(channel_id: str):
    return get_channel_data(channel_id)



