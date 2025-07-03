from dataclasses import dataclass, field
from typing import List

from App.src.entities.or_scheduler import ORScheduler
from App.src.enums.equipment_enum import EquipmentEnum


@dataclass
class OperationRoom:
    id: int
    equipment: List[EquipmentEnum]
    scheduler: ORScheduler = field(default_factory=ORScheduler)
