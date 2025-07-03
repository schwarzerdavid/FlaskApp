from dataclasses import dataclass
from typing import Optional

from App.src.consts.scheduler_consts import NO_ROOM_ASSIGNED


@dataclass
class RoomSlot:
    room_id: int = NO_ROOM_ASSIGNED
    starting_day: Optional[int] = None
    starting_hour: Optional[int] = None
    time_assigned: Optional[int] = None

    def is_sooner_then(self, other):
        if self.room_id == NO_ROOM_ASSIGNED:
            return False
        if other.room_id == NO_ROOM_ASSIGNED:
            return True
        else:
            if self.starting_day != other.starting_day:
                return self.starting_day < other.starting_day
            else:
                return self.starting_hour < other.starting_hour

    def is_empty(self):
        return self.room_id == NO_ROOM_ASSIGNED

