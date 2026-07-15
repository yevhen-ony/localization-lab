from common.position import Position
from common.entities import (
    Heartbeat,
    ReceiverId,
    Observation,
    StationReport,
    Signal,
    Tick,
)
from transport.protocols import (
    HeartbeatChannel,
    StationReportChannel,
)


class Station:
    def __init__(
        self,
        station_id: ReceiverId,
        position: Position,
        heartbeat_channel: HeartbeatChannel,
        report_channel: StationReportChannel,
    ) -> None:
        self._station_id = station_id
        self._position = position
        self._epoch = 0
        self._heartbeat_channel = heartbeat_channel
        self._observation_channel = report_channel
        self._slots: list[Signal | None] = []

    def emit_heartbeat(self) -> None:
        self._heartbeat_channel.publish(
            Heartbeat(
                station_id=self._station_id,
                position=self.position,
            )
        )

    @property
    def id(self) -> ReceiverId:
        return self._station_id

    @property
    def position(self) -> Position:
        return self._position

    def emit_epoch(self) -> None:
        observations = [
            Observation.from_signal(signal)
            for signal in self._slots
            if signal is not None
        ]
        if not observations:
            return

        batch = StationReport(
            epoch=self._epoch,
            station_id=self.id,
            station_position=self.position,
            observations=observations,
        )
        self._observation_channel.publish(batch)

    def on_tick(self, tick: Tick) -> None:
        self.emit_heartbeat()
        self.emit_epoch()
        self._slots = [None] * tick.slots
        self._epoch = tick.epoch

    def on_signal(self, signal: Signal) -> None:
        if signal.receiver_id != self.id:
            return

        if not (0 <= signal.slot < len(self._slots)):
            return

        self._slots[signal.slot] = signal
