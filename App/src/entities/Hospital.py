from dataclasses import dataclass
from typing import List

from App.src.entities.operation_room import OperationRoom

@dataclass
class Hospital:
    operation_rooms: List[OperationRoom]
