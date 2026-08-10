from pydantic import BaseModel


class YouTubeVideo(BaseModel):
    video_id: str
    title: str
    description: str
    channel_title: str
    published_at: str
    thumbnail: str
    duration: str
    duration_iso: str
    view_count: int
    like_count: int
    comment_count: int


class YouTubeSearchResponse(BaseModel):
    query: str
    count: int
    next_page_token: str | None = None
    results: list[YouTubeVideo]