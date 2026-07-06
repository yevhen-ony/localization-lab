from common.station_report import StationReport


class Ground:
    def __init__(self, station_count: int):
        self._station_count = station_count

    def on_station_report(self, report: StationReport) -> None:
        for observation in report.observations:
            print(
                f"[{report.epoch}] "
                f"{observation.emitter_id} "
                f"@ {report.station_id} "
                f"t={observation.arrival_time.ns} ns"
            )
        print()

