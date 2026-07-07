import json
from dataclasses import asdict

from common.station_report import StationReport

from .epoch import EpochBuffer
from .tdoa import TdoaSolver


class Localizer:
    def __init__(self, station_count: int):
        self._station_count = station_count
        self.epochs = EpochBuffer(depth=1)
        self.solver = TdoaSolver()

    def on_station_report(self, report: StationReport) -> None:
        if self.epochs.advance(report.epoch):
            self.on_epoch_advanced()

        self.epochs.try_put(report)

    def on_epoch_advanced(self):
        epochs = self.epochs.drain_expired()
        if len(epochs) == 0:
            return

        for epoch in epochs:
            print(f"======== Epoch {epoch.epoch} ========")
            for ping in epoch.pings(): 
                fix = self.solver.solve(ping)
                if fix is None:
                    continue
                print(json.dumps(asdict(fix), indent=2))
