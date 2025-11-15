# backend/api/channel_context/service.py
import requests
from backend.core.config import settings

def get_channel_data(channel_id: str):
    # 1️⃣ Channel info
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={channel_id}&key={settings.YOUTUBE_API_KEY}"
    res = requests.get(url)
    data = res.json()

    if "error" in data:
        return {"error": data["error"]["message"]}
    if "items" not in data or len(data["items"]) == 0:
        return {"error": "Channel not found"}

    channel = data["items"][0]
    snippet = channel.get("snippet", {})
    stats = channel.get("statistics", {})
    content = channel.get("contentDetails", {})

    uploads_playlist = content.get("relatedPlaylists", {}).get("uploads")
    if not uploads_playlist:
        return {"error": "Uploads playlist not found for this channel"}

    # 2️⃣ Fetch all videos safely
    videos = []
    next_page_token = None
    max_pages = 5  # limit to avoid infinite loops
    page = 0

    while page < max_pages:
        playlist_url = (
            f"https://www.googleapis.com/youtube/v3/playlistItems"
            f"?part=snippet&maxResults=50&playlistId={uploads_playlist}&key={settings.YOUTUBE_API_KEY}"
        )
        if next_page_token:
            playlist_url += f"&pageToken={next_page_token}"

        response = requests.get(playlist_url)
        res_json = response.json()

        if "error" in res_json:
            break

        for item in res_json.get("items", []):
            snippet_data = item.get("snippet", {})
            resource = snippet_data.get("resourceId", {})
            video_id = resource.get("videoId")
            if not video_id:
                continue
            videos.append({
                "video_id": video_id,
                "title": snippet_data.get("title"),
                "published_at": snippet_data.get("publishedAt"),
                "thumbnails": snippet_data.get("thumbnails", {}),
            })

        next_page_token = res_json.get("nextPageToken")
        if not next_page_token:
            break
        page += 1  # increment page counter

    return {
        "channel_id": channel_id,
        "name": snippet.get("title"),
        "description": snippet.get("description"),
        "published_at": snippet.get("publishedAt"),
        "country": snippet.get("country"),
        "subscribers": stats.get("subscriberCount"),
        "views": stats.get("viewCount"),
        "video_count": stats.get("videoCount"),
        "uploads_playlist_id": uploads_playlist,
        "videos_fetched": len(videos),
        "videos": videos
    }
