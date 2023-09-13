from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Any

from polar_flow_export.models.calender_events import CalendarEvent, CalendarEventTypes
from polar_flow_export.models.exercise import Exercise
from polar_flow_export.models.fitness_data import FitnessData


class CalendarEventFactory:
    _type_map = {
        CalendarEventTypes.EXERCISE: Exercise,
        CalendarEventTypes.FITNESS_DATA: FitnessData
    }

    def make(self, d: Dict[str, Any]) -> CalendarEvent:
        try:
            t = CalendarEventTypes(d["type"])
        except KeyError:
            raise RuntimeError(f"Encountered a calendar event without type {d}")
        except TypeError:
            raise RuntimeError(f"Unknown type for {d}")
        return self._type_map[t].make(d)
