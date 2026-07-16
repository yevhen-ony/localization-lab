from typing import Protocol, Callable, TypeAlias

import common.entities as e


class Channel[T](Protocol):
    def subscribe(self, handler: Callable[[T], None], /) -> None: ...
    def publish(self, value: T, /) -> None: ...


StationReportHandler: TypeAlias = Callable[[e.StationReport], None]
StationReportChannel: TypeAlias = Channel[e.StationReport]


HeartbeatHandler: TypeAlias = Callable[[e.Heartbeat], None]
HeartbeatChannel: TypeAlias = Channel[e.Heartbeat]


SignalHandler: TypeAlias = Callable[[e.Signal], None]
SignalChannel: TypeAlias = Channel[e.Signal]


TickHandler: TypeAlias = Callable[[e.Tick], None]
TickChannel: TypeAlias = Channel[e.Tick]

LocalizedSampleHandler: TypeAlias = Callable[[e.LocalizedSample], None]
LocalizedSampleChannel: TypeAlias = Channel[e.LocalizedSample]


TrackSampleHandler: TypeAlias = Callable[[e.TrackSample], None]
TrackChannel: TypeAlias = Channel[e.TrackSample]


DroneTruthSampleHandler: TypeAlias = Callable[[e.DroneTruthSample], None]
DroneTruthChannel: TypeAlias = Channel[e.DroneTruthSample]
