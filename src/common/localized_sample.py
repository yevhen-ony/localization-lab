from dataclasses import dataclass

from .ids import EmitterId
from .position import Position
from .telemetry import Telemetry


@dataclass(frozen=True, slots=True)
class LocalizedSample:
    epoch: int
    emitter_id: EmitterId
    position: Position
    position_error: float
    telemetry: Telemetry
