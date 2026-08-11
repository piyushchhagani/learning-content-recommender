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

def test_short_video_gets_no_duration_score():
    video = {
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "duration": "3m",
    }

    assert calculate_recommendation_score(video) == 0.0


def test_learning_length_video_gets_full_duration_score():
    video = {
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "duration": "45m",
    }

    assert calculate_recommendation_score(video) == 20.0


def test_very_long_video_gets_partial_duration_score():
    video = {
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "duration": "4h",
    }

    assert calculate_recommendation_score(video) == 10.0

def test_title_relevance_gets_higher_score():
    video = {
        "search_query": "python",
        "title": "Python Full Course for Beginners",
        "description": "",
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "duration": "",
    }

    assert calculate_recommendation_score(video) == 20.0


def test_description_relevance_gets_partial_score():
    video = {
        "search_query": "python",
        "title": "Complete Programming Course",
        "description": "Learn Python from scratch.",
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "duration": "",
    }

    assert calculate_recommendation_score(video) == 10.0


def test_unrelated_video_gets_no_relevance_score():
    video = {
        "search_query": "python",
        "title": "Docker Full Course",
        "description": "Learn containers and Kubernetes.",
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "duration": "",
    }

    assert calculate_recommendation_score(video) == 0.0

def test_recommendation_score_is_capped_at_100():
    video = {
        "search_query": "web development",
        "title": "Web Development Full Course",
        "description": "Complete web development course.",
        "view_count": 10_000_000,
        "like_count": 1_000_000,
        "comment_count": 100_000,
        "duration": "2h",
    }

    score = calculate_recommendation_score(video)

    assert score == 100.0