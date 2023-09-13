from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Callable, Optional, List
from datetime import datetime


@dataclass
class CalendarEvent(object):
    type: str
    list_item_id: int
    datetime: datetime

    @classmethod
    def make(cls, d: Dict[str, Any]) -> CalendarEvent:
        return cls(
            type=d['type'],
            list_item_id=d['listItemId'],
            datetime=cls.parse_datetime(d['datetime'])
        )

    @classmethod
    def parse_datetime(cls, datetime_str: str) -> datetime:
        """datetime looks like '2023-09-03T21:37:09.000Z'"""
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    def _get_datetime(self) -> str:
        return datetime.strftime(self.datetime, '%Y%m%d_%H%M%S')

    def get_store_dir(self, parent_dir: Path) -> Path:
        class_name = self.__class__.__name__
        store_dir = parent_dir.joinpath(class_name)
        store_dir.mkdir(parents=True, exist_ok=True, mode=0o755)
        return store_dir

    @abstractmethod
    def _store(self, parent_dir: Path, url_opener: Callable[[str, Optional[Dict[str, Any]]], bytes]) -> List[Path]:
        """
        Retrieve the data of this calendar event and store it in a parent dir.

        Return a list of resulting paths.
        """

    def store(self, parent_dir: Path, url_opener: Callable[[str, Optional[Dict[str, Any]]], bytes]) -> List[str]:
        return [str(f) for f in self._store(parent_dir=parent_dir, url_opener=url_opener)]


class CalendarEventTypes(Enum):
    EXERCISE = "EXERCISE"
    FITNESS_DATA = "FITNESSDATA"
