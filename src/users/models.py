from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class Segment(StrEnum):
    NEW = "new"
    REGULAR = "regular"
    VIP = "vip"


@dataclass(frozen=True, slots=True)
class User:
    user_id: int
    name: str
    city: str
    segment: Segment
    registered_at: datetime
