from typing import Any


def _duration_score(duration: str) -> float:
    if not duration:
        return 0.0

    total_minutes = 0

    parts = duration.split()

    for part in parts:
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


def calculate_recommendation_score(video: dict[str, Any]) -> float:
    views = max(int(video.get("view_count", 0)), 0)
    likes = max(int(video.get("like_count", 0)), 0)
    comments = max(int(video.get("comment_count", 0)), 0)

    score = 0.0

    if views > 0:
        score += min(views / 1_000_000, 1.0) * 40

    if likes > 0 and views > 0:
        like_ratio = likes / views
        score += min(like_ratio / 0.05, 1.0) * 30

    if comments > 0 and views > 0:
        comment_ratio = comments / views
        score += min(comment_ratio / 0.005, 1.0) * 10

    score += _duration_score(video.get("duration", ""))

    return round(score, 2)