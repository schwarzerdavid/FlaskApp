from dataclasses import dataclass
from typing import Optional

from App.src.entities.room_slot import RoomSlot


@dataclass
class AssignResponse:
    is_assigned: bool
    room_slot: Optional[RoomSlot] = None
    place_on_queue: Optional[int] = None
