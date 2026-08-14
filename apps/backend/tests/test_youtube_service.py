import pytest

from app.services.youtube_service import search_youtube


@pytest.mark.anyio
async def test_search_youtube_sends_page_token(monkeypatch):
    captured = {}
    call_count = 0

    class FakeResponse:
        def __init__(self, data):
            self.data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self.data

    search_response = FakeResponse(
        {
            "items": [
                {
                    "id": {
                        "videoId": "video-123",
                    },
                    "snippet": {
                        "title": "Python Tutorial",
                        "description": "Learn Python",
                        "channelTitle": "Test Channel",
                        "publishedAt": "2026-01-01T00:00:00Z",
                        "thumbnails": {
                            "default": {
                                "url": "https://example.com/thumb.jpg",
                            }
                        },
                    },
                }
            ],
            "nextPageToken": "next-page",
        }
    )

    video_response = FakeResponse(
        {
            "items": [
                {
                    "id": "video-123",
                    "contentDetails": {
                        "duration": "PT10M",
                    },
                    "statistics": {
                        "viewCount": "1000",
                        "likeCount": "100",
                        "commentCount": "10",
                    },
                }
            ]
        }
    )

    async def fake_get(self, url, **kwargs):
        nonlocal call_count

        call_count += 1

        if call_count == 1:
            captured["url"] = url
            captured["params"] = kwargs["params"]
            return search_response

        return video_response

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        get = fake_get

    monkeypatch.setattr(
        "app.services.youtube_service.httpx.AsyncClient",
        lambda timeout: FakeClient(),
    )

    monkeypatch.setattr(
        "app.services.youtube_service.get_settings",
        lambda: type(
            "Settings",
            (),
            {"youtube_api_key": "test-key"},
        )(),
    )

    result = await search_youtube(
        "python",
        max_results=10,
        page_token="page-2",
        min_score=30.0,
    )

    assert captured["params"]["pageToken"] == "page-2"
    assert result["next_page_token"] == "next-page"