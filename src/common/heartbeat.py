from dataclasses import dataclass

from .ids import StationId
from .position import Position


@dataclass(frozen=True, slots=True)
class Heartbeat:
    station_id: StationId
    position: Position
