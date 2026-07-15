from dataclasses import dataclass
from common.position import Position
from common.entities import (
    EmitterId,
    ReceiverId,
    Telemetry,
)


@dataclass(frozen=True, slots=True)
class ReceiverHit:
    id: ReceiverId
    pos: Position
    time_ns: float


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
