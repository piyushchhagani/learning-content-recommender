from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Learning Content Recommender"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "development"
    assert data["status"] == "running"


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_youtube_search_accepts_min_score():
    response = client.get(
        "/api/youtube/search?q=python&min_score=80"
    )

    assert response.status_code in (200, 502)


def test_youtube_search_rejects_invalid_min_score():
    response = client.get(
        "/api/youtube/search?q=python&min_score=101"
    )

    assert response.status_code == 422


def test_youtube_search_rejects_negative_min_score():
    response = client.get(
        "/api/youtube/search?q=python&min_score=-1"
    )

    assert response.status_code == 422

def test_youtube_search_passes_min_score(monkeypatch):
    captured = {}

    async def fake_search_youtube(
        query,
        max_results,
        page_token,
        min_score,
    ):
        captured["min_score"] = min_score
        return {
            "results": [],
            "next_page_token": None,
        }

    monkeypatch.setattr(
        "app.api.youtube.search_youtube",
        fake_search_youtube,
    )

    response = client.get(
        "/api/youtube/search?q=python&min_score=75"
    )

    assert response.status_code == 200
    assert captured["min_score"] == 75.0