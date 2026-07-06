from dataclasses import dataclass
from common.ids import ReceiverId 
from common.position import Position
from common.observation import Observation

@dataclass(frozen=True, slots=True)
class StationReport:
    epoch: int
    station_id: ReceiverId
    station_position: Position
    observations: list[Observation]
