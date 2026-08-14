from typing import Any


def _duration_score(duration: str) -> float:
    if not duration:
        return 0.0

    total_minutes = 0

    for part in duration.split():
        if part.endswith("h"):
            total_minutes += int(part[:-1]) * 60
        elif part.endswith("m"):
            total_minutes += int(part[:-1])
        elif part.endswith("s"):
            total_minutes += 1 if int(part[:-1]) >= 30 else 0

    if total_minutes < 5:
        return 0.0

    if total_minutes < 15:
        return 10.0

    if total_minutes <= 180:
        return 20.0

    return 10.0


def _relevance_score(video: dict[str, Any]) -> float:
    query = str(video.get("search_query", "")).strip().lower()

    if not query:
        return 0.0

    title = str(video.get("title", "")).lower()
    description = str(video.get("description", "")).lower()

    if query in title:
        return 20.0

    if query in description:
        return 10.0

    return 0.0


def calculate_recommendation_breakdown(
    video: dict[str, Any],
) -> dict[str, float]:
    views = max(int(video.get("view_count", 0)), 0)
    likes = max(int(video.get("like_count", 0)), 0)
    comments = max(int(video.get("comment_count", 0)), 0)

    relevance_score = _relevance_score(video)

    views_score = 0.0
    if views > 0:
        views_score = min(views / 1_000_000, 1.0) * 40

    like_score = 0.0
    if likes > 0 and views > 0:
        like_ratio = likes / views
        like_score = min(like_ratio / 0.05, 1.0) * 30

    comment_score = 0.0
    if comments > 0 and views > 0:
        comment_ratio = comments / views
        comment_score = min(comment_ratio / 0.005, 1.0) * 10

    duration_score = _duration_score(
        video.get("duration", "")
    )

    total_score = min(
        round(
            relevance_score
            + views_score
            + like_score
            + comment_score
            + duration_score,
            2,
        ),
        100.0,
    )

    return {
        "relevance_score": round(relevance_score, 2),
        "views_score": round(views_score, 2),
        "like_score": round(like_score, 2),
        "comment_score": round(comment_score, 2),
        "duration_score": round(duration_score, 2),
        "total_score": total_score,
    }


def calculate_recommendation_score(video: dict[str, Any]) -> float:
    return calculate_recommendation_breakdown(video)["total_score"]

def filter_recommendations(
    videos: list[dict[str, Any]],
    min_score: float = 30.0,
) -> list[dict[str, Any]]:
    return [
        video
        for video in videos
        if video.get("recommendation_score", 0.0) >= min_score
    ]
