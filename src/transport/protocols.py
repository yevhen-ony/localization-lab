from typing import Protocol, Callable

from common.entities import (
    StationReport,
    Heartbeat,
    Signal,
    Tick,
    LocalizedSample,
    TrackSample,
)

StationReportHandler = Callable[[StationReport], None]

class StationReportChannel(Protocol):
    def subscribe(self, handler: StationReportHandler) -> None: ...
    def publish(self, report: StationReport) -> None: ...


HeartbeatHandler = Callable[[Heartbeat], None]

class HeartbeatChannel(Protocol):
    def subscribe(self, handler: HeartbeatHandler) -> None: ...
    def publish(self, hb: Heartbeat) -> None: ...


SignalHandler = Callable[[Signal], None]


class SignalChannel(Protocol):
    def subscribe(self, handler: SignalHandler) -> None: ...
    def publish(self, signal: Signal) -> None: ...


TickHandler = Callable[[Tick], None]

class TickChannel(Protocol):
    def subscribe(self, handler: TickHandler) -> None: ...
    def publish(self, tick: Tick) -> None: ...


LocalizedSampleHandler = Callable[[LocalizedSample], None]

class LocalizedSampleChannel(Protocol):
    def subscribe(self, handler: LocalizedSampleHandler) -> None: ...
    def publish(self, sample: LocalizedSample) -> None: ...


TrackSampleHandler = Callable[[TrackSample], None]


class TrackChannel(Protocol):
    def subscribe(self, handler: TrackSampleHandler) -> None: ...
    def publish(self, sample: TrackSample) -> None: ...
