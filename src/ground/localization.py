from common.ids import EmitterId, ReceiverId
from common.position import Position
from common.arrival_time import ArrivalTime
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReceiverHit:
    receiver_id: ReceiverId
    position: Position
    arrival_time: ArrivalTime


@dataclass(frozen=True, slots=True)
class EmitterPing:
    epoch: int
    emitter_id: EmitterId
    hits: tuple[ReceiverHit, ...]


