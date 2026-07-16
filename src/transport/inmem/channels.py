from __future__ import annotations

from collections.abc import Callable

import transport.protocols as p 
import common.entities as e


class StationReportChannel:
    def __init__(self) -> None:
        self._handlers: list[p.StationReportHandler] = []

    def subscribe(self, handler: p.StationReportHandler) -> None:
        self._handlers.append(handler)

    def publish(self, report: e.StationReport) -> None:
        for handler in self._handlers:
            handler(report)



class HeartbeatChannel:
    def __init__(self) -> None:
        self._handlers: list[p.HeartbeatHandler] = []

    def subscribe(self, handler: p.HeartbeatHandler) -> None:
        self._handlers.append(handler)

    def publish(self, hb: e.Heartbeat) -> None:
        for handler in self._handlers:
            handler(hb)


class SignalChannel:
    def __init__(self) -> None:
        self._handlers: list[p.SignalHandler] = []

    def subscribe(self, handler: p.SignalHandler) -> None:
        self._handlers.append(handler)

    def publish(self, signal: e.Signal) -> None:
        for handler in self._handlers:
            handler(signal)


class TickChannel:
    def __init__(self) -> None:
        self._handlers: list[p.TickHandler] = []

    def subscribe(self, handler: p.TickHandler) -> None:
        self._handlers.append(handler)

    def publish(self, tick: e.Tick) -> None:
        for handler in self._handlers:
            handler(tick)


class LocalizedSampleChannel:
    def __init__(self) -> None:
        self._handlers: list[p.LocalizedSampleHandler] = []

    def subscribe(self, handler: p.LocalizedSampleHandler) -> None:
        self._handlers.append(handler)

    def publish(self, sample: e.LocalizedSample) -> None:
        for handler in self._handlers:
            handler(sample)


class TrackChannel:
    def __init__(self) -> None:
        self._handlers: list[p.TrackSampleHandler] = []

    def subscribe(self, handler: p.TrackSampleHandler) -> None:
        self._handlers.append(handler)

    def publish(self, sample: e.TrackSample) -> None:
        for handler in self._handlers:
            handler(sample)


class DroneTruthChannel:
    def __init__(self) -> None:
        self._handlers: list[p.DroneTruthSampleHandler] = []

    def subscribe(self, handler: p.DroneTruthSampleHandler) -> None:
        self._handlers.append(handler)

    def publish(self, sample: e.DroneTruthSample) -> None:
        for handler in self._handlers:
            handler(sample)

