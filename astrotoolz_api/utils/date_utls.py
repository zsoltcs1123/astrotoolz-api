from datetime import datetime


def parse_utc_date(date_str: str) -> datetime:
    try:
        if "T" not in date_str:
            date_str += "T00:00:00Z"
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")