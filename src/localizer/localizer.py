from transport.protocols import LocalizedSampleChannel
from common.entities import (
    StationReport,
    LocalizedSample,
)

from .epoch import EpochBuffer
from .tdoa import TdoaSolver
from .models import EmitterPing, PositionEstimate


class Localizer:
    def __init__(
        self,
        sample_channel: LocalizedSampleChannel,
    ):
        self._sample_channel = sample_channel
        self._epochs = EpochBuffer(depth=1)
        self._solver = TdoaSolver()

    def on_station_report(self, report: StationReport) -> None:
        print(f"localizer: station report: report = {report.station_id}")
        if self._epochs.advance(report.epoch):
            self.on_epoch_advanced()

        self._epochs.try_put(report)

    def on_epoch_advanced(self):
        epochs = self._epochs.drain_expired()
        if len(epochs) == 0:
            return

        for epoch in epochs:
            for ping in epoch.pings():
                pe = self._solver.solve(ping.hits)
                if pe is None:
                    continue
                self._emit_sample(ping, pe)

    def _emit_sample(self, ping: EmitterPing, pe: PositionEstimate) -> None:
        self._sample_channel.publish(
            LocalizedSample(
                epoch=ping.epoch,
                emitter_id=ping.id,
                telemetry=ping.telemetry,
                position=pe.pos,
                position_std=pe.std,
            )
        )
