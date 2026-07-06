from dataclasses import dataclass, field
from collections import defaultdict
from common.ids import EmitterId, ReceiverId
from common.station_report import StationReport

from .localization import EmitterPing, ReceiverHit


@dataclass(slots=True)
class EpochBucket:
    epoch: int
    reports: dict[ReceiverId, StationReport] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.reports)

    def put(self, report: StationReport) -> None:
        assert report.epoch == self.epoch, "Report belongs to a different epoch"
        self.reports[report.station_id] = report

    def pings(self) -> tuple[EmitterPing, ...]:

        hits: defaultdict[EmitterId, list[ReceiverHit]] = defaultdict(list)

        for report in self.reports.values():
            for observation in report.observations:
                hit = ReceiverHit(
                    receiver_id=report.station_id,
                    position=report.station_position,
                    arrival_time=observation.arrival_time,
                )
                hits[observation.emitter_id].append(hit)

        return tuple(
            EmitterPing(
                epoch=self.epoch,
                emitter_id=emitter_id,
                hits=tuple(hits),
            )
            for emitter_id, hits in hits.items()
        )


@dataclass(slots=True)
class EpochBuffer:
    depth: int
    latest_epoch: int = -1
    buckets: dict[int, EpochBucket] = field(default_factory=dict)

    def try_put(self, report: StationReport) -> bool:
        self.latest_epoch = max(self.latest_epoch, report.epoch)

        if self._is_expired(report.epoch):
            return False

        if report.epoch not in self.buckets:
            self.buckets[report.epoch] = EpochBucket(epoch=report.epoch)

        self.buckets[report.epoch].put(report)
        return True

    def drain_expired(self) -> tuple[EpochBucket, ...]:
        expired = tuple(
            bucket for bucket in self.buckets.values()
            if self._is_expired(bucket.epoch)
        )

        for bucket in expired:
            del self.buckets[bucket.epoch]

        return expired

    def _is_expired(self, epoch: int) -> bool:
        oldest_kept_epoch = self.latest_epoch - self.depth + 1
        return epoch < oldest_kept_epoch
