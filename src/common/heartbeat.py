from dataclasses import dataclass

from .ids import ReceiverId
from .position import Position


@dataclass(frozen=True, slots=True)
class Heartbeat:
    station_id: ReceiverId
    position: Position
