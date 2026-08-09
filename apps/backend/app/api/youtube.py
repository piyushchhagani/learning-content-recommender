from fastapi import APIRouter, HTTPException, Query

from app.services.youtube_service import search_youtube


router = APIRouter(
    prefix="/api/youtube",
    tags=["YouTube"],
)


@router.get("/search")
async def youtube_search(
    q: str = Query(..., min_length=1),
    max_results: int = Query(10, ge=1, le=50),
):
    query = q.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    try:
        results = await search_youtube(
            query,
            max_results,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch results from YouTube.",
        ) from exc

    return {
        "query": query,
        "count": len(results),
        "results": results,
    }