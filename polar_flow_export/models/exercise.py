from pathlib import Path
from typing import Callable, Optional, Dict, Any, List

from polar_flow_export.models.calender_events import CalendarEvent
from dataclasses import dataclass


@dataclass
class Exercise(CalendarEvent):
    def _store(self, parent_dir: Path, url_opener: Callable[[str, Optional[Dict[str, Any]]], bytes]) -> List[Path]:
        paths = []
        store_dir = self.get_store_dir(parent_dir)
        for session_data_type in ["tcx", "csv", "gpx"]:
            session_data_type_dir = store_dir.joinpath(session_data_type)
            session_data_type_dir.mkdir(mode=0o755, exist_ok=True)
            out_file = session_data_type_dir.joinpath(f"{self._get_datetime()}.{session_data_type}")
            with open(out_file, 'w') as out_f:
                response = url_opener(f"/api/export/training/{session_data_type}/{self.list_item_id}", None)
                out_f.write(response.decode())
            paths.append(out_file)
        return paths

