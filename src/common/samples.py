from dataclasses import dataclass

from .ids import EmitterId
from .position import Position, Velocity
from .telemetry import Telemetry


@dataclass(frozen=True, slots=True)
class LocalizedSample:
    epoch: int
    emitter_id: EmitterId
    position: Position
    position_std: float
    telemetry: Telemetry


@dataclass(frozen=True, slots=True)
class TrackSample:
    epoch: int
    emitter_id: EmitterId
    position: Position
    position_std: float
    velocity: Velocity 
    velocity_std: float
    telemetry: Telemetry

