from dataclasses import dataclass

from .ids import EmitterId, StationId
from .telemetry import Telemetry
from .arrival_time import ArrivalTime


@dataclass(frozen=True, slots=True)
class Signal:
    slot: int
    emitter_id: EmitterId
    receiver_id: StationId
    arrival_time: ArrivalTime
    telemetry: Telemetry
