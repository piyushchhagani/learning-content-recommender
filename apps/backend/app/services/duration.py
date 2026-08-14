import re


_DURATION_PATTERN = re.compile(
    r"^PT"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+)S)?$"
)


def format_duration(duration: str) -> str:
    match = _DURATION_PATTERN.match(duration)

    if not match:
        return "Unknown"

    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)

    total_minutes = hours * 60 + minutes

    if seconds >= 30:
        total_minutes += 1

    if total_minutes == 0:
        return f"{seconds}s"

    if total_minutes < 60:
        return f"{total_minutes}m"

    formatted_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60

    if remaining_minutes == 0:
        return f"{formatted_hours}h"

    return f"{formatted_hours}h {remaining_minutes}m"