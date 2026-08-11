from typing import Any


def calculate_recommendation_score(video: dict[str, Any]) -> float:
    """
    Calculate a deterministic learning-content recommendation score.

    The score combines:
    - view count
    - like count
    - comment count
    - duration
    """

    views = max(int(video.get("view_count", 0)), 0)
    likes = max(int(video.get("like_count", 0)), 0)
    comments = max(int(video.get("comment_count", 0)), 0)

    duration = video.get("duration", "")

    score = 0.0

    if views > 0:
        score += min(views / 1_000_000, 1.0) * 40

    if likes > 0 and views > 0:
        like_ratio = likes / views
        score += min(like_ratio / 0.05, 1.0) * 30

    if comments > 0 and views > 0:
        comment_ratio = comments / views
        score += min(comment_ratio / 0.005, 1.0) * 10

    if duration:
        score += 20

    return round(score, 2)