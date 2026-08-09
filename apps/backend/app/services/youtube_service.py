from typing import Any

import httpx

from app.core.config import get_settings
from app.services.duration import format_duration


YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


async def search_youtube(
    query: str,
    max_results: int = 10,
) -> list[dict[str, Any]]:
    settings = get_settings()

    if not settings.youtube_api_key:
        raise RuntimeError("YouTube API key is not configured.")

    search_params = {
        "part": "snippet",
        "q": query.strip(),
        "type": "video",
        "maxResults": max_results,
        "key": settings.youtube_api_key,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        search_response = await client.get(
            YOUTUBE_SEARCH_URL,
            params=search_params,
        )

        search_response.raise_for_status()

        search_data = search_response.json()

        results = []

        for item in search_data.get("items", []):
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

        if not results:
            return []

        video_ids = ",".join(
            result["video_id"] for result in results
        )

        video_params = {
            "part": "contentDetails,statistics",
            "id": video_ids,
            "key": settings.youtube_api_key,
        }

        video_response = await client.get(
            YOUTUBE_VIDEOS_URL,
            params=video_params,
        )

        video_response.raise_for_status()

        video_data = video_response.json()

    metadata = {
        item["id"]: item
        for item in video_data.get("items", [])
    }

    for result in results:
        video = metadata.get(result["video_id"], {})
        content_details = video.get("contentDetails", {})
        statistics = video.get("statistics", {})

        raw_duration = content_details.get("duration", "")

        result["duration"] = format_duration(raw_duration)
        result["duration_iso"] = raw_duration
        result["view_count"] = int(statistics.get("viewCount", 0))
        result["like_count"] = int(statistics.get("likeCount", 0))
        result["comment_count"] = int(statistics.get("commentCount", 0))

    return results