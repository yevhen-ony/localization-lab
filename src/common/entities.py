from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

from .position import Position, Velocity

EmitterId = NewType("EmitterId", str)
ReceiverId = NewType("ReceiverId", str)


@dataclass(frozen=True, slots=True)
class ArrivalTime:
    ns: float


@dataclass(frozen=True, slots=True)
class Telemetry:
    temperature: float


@dataclass(frozen=True, slots=True)
class Tick:
    epoch: int
    slots: int


@dataclass(frozen=True, slots=True)
class Signal:
    slot: int
    emitter_id: EmitterId
    receiver_id: ReceiverId
    arrival_time: ArrivalTime
    telemetry: Telemetry

    @staticmethod
    def from_dict(d: dict) -> Signal:
        return Signal(
            slot=d["slot"],
            emitter_id=EmitterId(d["emitter_id"]),
            receiver_id=ReceiverId(d["receiver_id"]),
            arrival_time=ArrivalTime(**d["arrival_time"]),
            telemetry=Telemetry(**d["telemetry"]),
        )


@dataclass(frozen=True, slots=True)
class Heartbeat:
    station_id: ReceiverId
    position: Position

    @staticmethod
    def from_dict(d: dict) -> Heartbeat:
        return Heartbeat(
            station_id=ReceiverId(d["station_id"]),
            position=Position(**d["position"]),
        )


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

    @staticmethod
    def from_dict(d: dict) -> Observation:
        return Observation(
            emitter_id=EmitterId(d["emitter_id"]),
            arrival_time=ArrivalTime(**d["arrival_time"]),
            telemetry=Telemetry(**d["telemetry"]),
        )


@dataclass(frozen=True, slots=True)
class StationReport:
    epoch: int
    station_id: ReceiverId
    station_position: Position
    observations: list[Observation]

    @staticmethod
    def from_dict(d: dict) -> "StationReport":
        return StationReport(
            epoch=d["epoch"],
            station_id=ReceiverId(d["station_id"]),
            station_position=Position(**d["station_position"]),
            observations=[Observation.from_dict(obs) for obs in d["observations"]],
        )


@dataclass(frozen=True, slots=True)
class LocalizedSample:
    epoch: int
    emitter_id: EmitterId
    position: Position
    position_std: float
    telemetry: Telemetry

    @staticmethod
    def from_dict(d: dict) -> "LocalizedSample":
        return LocalizedSample(
            epoch=d["epoch"],
            emitter_id=EmitterId(d["emitter_id"]),
            position=Position(**d["position"]),
            position_std=d["position_std"],
            telemetry=Telemetry(**d["telemetry"]),
        )


@dataclass(frozen=True, slots=True)
class TrackSample:
    epoch: int
    emitter_id: EmitterId
    position: Position
    position_std: float
    velocity: Velocity
    velocity_std: float
    telemetry: Telemetry

    @staticmethod
    def from_dict(d: dict) -> TrackSample:
        return TrackSample(
            epoch=d["epoch"],
            emitter_id=EmitterId(d["emitter_id"]),
            position=Position(**d["position"]),
            position_std=d["position_std"],
            velocity=Velocity(**d["velocity"]),
            velocity_std=d["velocity_std"],
            telemetry=Telemetry(**d["telemetry"]),
        )


@dataclass(frozen=True, slots=True)
class DroneTruthSample:
    epoch: int
    emitter_id: EmitterId
    position: Position
    velocity: Velocity

    @staticmethod
    def from_dict(d: dict) -> DroneTruthSample:
        return DroneTruthSample(
            epoch=d["epoch"],
            emitter_id=EmitterId(d["emitter_id"]),
            position=Position(**d["position"]),
            velocity=Velocity(**d["velocity"]),
        )
