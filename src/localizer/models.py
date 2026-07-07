from common.ids import EmitterId, ReceiverId
from common.position import Position
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReceiverHit:
    id: ReceiverId
    pos: Position
    time_ns: int 


@dataclass(frozen=True, slots=True)
class EmitterPing:
    epoch: int
    id: EmitterId
    hits: tuple[ReceiverHit, ...]


@dataclass(frozen=True, slots=True)
class EmitterFix:
    epoch: int
    emitter_id: EmitterId
    position: Position
    error: float 

