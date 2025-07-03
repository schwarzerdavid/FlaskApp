from dataclasses import dataclass
from typing import Optional

from App.src.enums.doctor_types import DoctorTypes


@dataclass
class ORRequest:
    doctor_type: DoctorTypes
    request_id: Optional[int] = None
