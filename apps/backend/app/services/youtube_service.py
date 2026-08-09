from typing import Any

import httpx

from app.core.config import get_settings


YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


async def search_youtube(
    query: str,
    max_results: int = 10,
) -> list[dict[str, Any]]:
    settings = get_settings()

    if not settings.youtube_api_key:
        raise RuntimeError("YouTube API key is not configured.")

    params = {
        "part": "snippet",
        "q": query.strip(),
        "type": "video",
        "maxResults": max_results,
        "key": settings.youtube_api_key,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            YOUTUBE_SEARCH_URL,
            params=params,
        )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})

        if not video_id:
            continue

        thumbnails = snippet.get("thumbnails", {})

        thumbnail = (
            thumbnails.get("high", {}).get("url")
            or thumbnails.get("medium", {}).get("url")
            or thumbnails.get("default", {}).get("url")
            or ""
        )

        results.append(
            {
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt", ""),
                "thumbnail": thumbnail,
            }
        )

    return results