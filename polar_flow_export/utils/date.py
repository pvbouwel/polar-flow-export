from datetime import datetime, date
from typing import Union


def date_trunc(d: datetime) -> date:
    return date(year=d.year, month=d.month, day=d.day)


def date_str(d: Union[datetime, date]) -> str:
    return f"{d.year}-{d.month}-{d.day}"
