from app.services.duration import format_duration


def test_format_hours_minutes_seconds():
    assert format_duration("PT4H23M21S") == "4h 23m"


def test_format_hours_only():
    assert format_duration("PT2H") == "2h"


def test_format_minutes_seconds():
    assert format_duration("PT11M53S") == "12m"


def test_format_minutes():
    assert format_duration("PT7M") == "7m"


def test_format_seconds():
    assert format_duration("PT25S") == "25s"


def test_invalid_duration():
    assert format_duration("invalid") == "Unknown"