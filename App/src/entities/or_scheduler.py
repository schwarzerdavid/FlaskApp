from dataclasses import dataclass, field
from typing import List

from App.src.consts.scheduler_consts import OR_WORKING_HOURS_A_DAY, EMPTY_SLOT_REQUEST_ID, SCHEDULER_PERIOD_IN_DAYS


@dataclass
class ORScheduler:
    time_table: List[List[int]] = field(default_factory=lambda: [[EMPTY_SLOT_REQUEST_ID] * OR_WORKING_HOURS_A_DAY for _ in range(SCHEDULER_PERIOD_IN_DAYS)])
