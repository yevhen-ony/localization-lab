from common.ids import EmitterId, ReceiverId
from common.position import Position
from common.telemetry import Telemetry
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReceiverHit:
    id: ReceiverId
    pos: Position
    time_ns: int


ReceiverHits = tuple[ReceiverHit, ...]


@dataclass(frozen=True, slots=True)
class EmitterPing:
    epoch: int
    id: EmitterId
    hits: ReceiverHits
    telemetry: Telemetry


@dataclass(frozen=True, slots=True)
class PositionEstimate:
    pos: Position
    std: float
