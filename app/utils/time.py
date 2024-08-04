from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


def now_datetime() -> datetime:
    """
    현재 datetime (한국 timezone)
    """
    return datetime.now(tz=KST)
