from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Dict, Any, List

from polar_flow_export.models.calender_events import CalendarEvent


@dataclass
class FitnessData(CalendarEvent):
    index: int

    @classmethod
    def make(cls, d: Dict[str, Any]) -> CalendarEvent:
        return cls(
            type=d['type'],
            list_item_id=d['listItemId'],
            datetime=cls.parse_datetime(d['datetime']),
            index=d['index']
        )

    def _store(self, parent_dir: Path, url_opener: Callable[[str, Optional[Dict[str, Any]]], bytes]) -> List[Path]:
        store_dir = self.get_store_dir(parent_dir)
        out_file = store_dir.joinpath(f"{self._get_datetime()}.txt")
        with open(out_file, 'w') as out_f:
            out_f.write(str(self.index))
        return [out_file]
