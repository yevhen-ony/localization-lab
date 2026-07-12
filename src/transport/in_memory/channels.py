from __future__ import annotations

from collections.abc import Callable

from common.station_report import StationReport
from common.heartbeat import Heartbeat
from common.signal import Signal
from common.tick import Tick
from common.samples import LocalizedSample, TrackSample


StationReportHandler = Callable[[StationReport], None]


class StationReportChannel:
    def __init__(self) -> None:
        self._handlers: list[StationReportHandler] = []

    def subscribe(self, handler: StationReportHandler) -> None:
        self._handlers.append(handler)

    def publish(self, batch: StationReport) -> None:
        for handler in self._handlers:
            handler(batch)


HeartbeatHandler = Callable[[Heartbeat], None]


class HeartbeatChannel:
    def __init__(self) -> None:
        self._handlers: list[HeartbeatHandler] = []

    def subscribe(self, handler: HeartbeatHandler) -> None:
        self._handlers.append(handler)

    def publish(self, report: Heartbeat) -> None:
        for handler in self._handlers:
            handler(report)


SignalHandler = Callable[[Signal], None]


class SignalChannel:
    def __init__(self) -> None:
        self._handlers: list[SignalHandler] = []

    def subscribe(self, handler: SignalHandler) -> None:
        self._handlers.append(handler)

    def publish(self, signal: Signal) -> None:
        for handler in self._handlers:
            handler(signal)


TickHandler = Callable[[Tick], None]


class TickChannel:
    def __init__(self) -> None:
        self._handlers: list[TickHandler] = []

    def subscribe(self, handler: TickHandler) -> None:
        self._handlers.append(handler)

    def publish(self, report: Tick) -> None:
        for handler in self._handlers:
            handler(report)


LocalizedSampleHandler = Callable[[LocalizedSample], None]


class LocalizedSampleChannel:
    def __init__(self) -> None:
        self._handlers: list[LocalizedSampleHandler] = []

    def subscribe(self, handler: LocalizedSampleHandler) -> None:
        self._handlers.append(handler)

    def publish(self, sample: LocalizedSample) -> None:
        for handler in self._handlers:
            handler(sample)


TrackSampleHandler = Callable[[TrackSample], None]


class TrackChannel:
    def __init__(self) -> None:
        self._handlers: list[TrackSampleHandler] = []

    def subscribe(self, handler: TrackSampleHandler) -> None:
        self._handlers.append(handler)

    def publish(self, sample: TrackSample) -> None:
        for handler in self._handlers:
            handler(sample)
