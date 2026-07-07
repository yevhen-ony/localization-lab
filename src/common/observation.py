from __future__ import annotations

from dataclasses import dataclass

from .arrival_time import ArrivalTime
from .ids import EmitterId
from .telemetry import Telemetry
from .signal import Signal


@dataclass(frozen=True, slots=True)
class Observation:
    emitter_id: EmitterId
    arrival_time: ArrivalTime
    telemetry: Telemetry

    @staticmethod
    def from_signal(signal: Signal) -> Observation:
        return Observation(
            emitter_id=signal.emitter_id,
            arrival_time=signal.arrival_time,
            telemetry=signal.telemetry,
        )
