from fastapi import APIRouter, HTTPException, Query

from app.core.config import get_settings
from app.schemas.youtube import YouTubeSearchResponse
from app.services.youtube_service import search_youtube

router = APIRouter(
    prefix="/api/youtube",
    tags=["YouTube"],
)

@router.get(
    "/search",
    response_model=YouTubeSearchResponse,
)
async def youtube_search(
    q: str = Query(..., min_length=1),
    max_results: int = Query(10, ge=1, le=50),
    page_token: str | None = Query(None),
    min_score: float | None = Query(None, ge=0.0, le=100.0),
):
    settings = get_settings()

    query = q.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    if min_score is None:
        min_score = settings.recommendation_min_score

    try:
        search_result = await search_youtube(
            query,
            max_results,
            page_token,
            min_score,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch results from YouTube.",
        ) from exc

    results = search_result["results"]

    return {
        "query": query,
        "count": len(results),
        "next_page_token": search_result["next_page_token"],
        "results": results,
    }