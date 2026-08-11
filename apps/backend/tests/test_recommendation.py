from app.services.recommendation import calculate_recommendation_score


def test_high_quality_video_gets_high_score():
    video = {
        "view_count": 5_000_000,
        "like_count": 250_000,
        "comment_count": 25_000,
        "duration": "2h 30m",
    }

    score = calculate_recommendation_score(video)

    assert score == 100.0


def test_video_without_metadata_gets_zero_score():
    video = {
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "duration": "",
    }

    score = calculate_recommendation_score(video)

    assert score == 0.0


def test_negative_metadata_does_not_reduce_score():
    video = {
        "view_count": -100,
        "like_count": -10,
        "comment_count": -5,
        "duration": "",
    }

    score = calculate_recommendation_score(video)

    assert score == 0.0