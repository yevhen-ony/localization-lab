from dataclasses import dataclass, field
from collections import defaultdict

from common.entities import (
    EmitterId,
    ReceiverId,
    StationReport,
    Telemetry,
)

from .models import EmitterPing, ReceiverHit


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
        tele: dict[EmitterId, Telemetry] = {}

        for report in self.reports.values():
            for obs in report.observations:
                hit = ReceiverHit(
                    id=report.station_id,
                    pos=report.station_position,
                    time_ns=obs.arrival_time.ns,
                )
                hits[obs.emitter_id].append(hit)
                tele.setdefault(obs.emitter_id, obs.telemetry)

        return tuple(
            EmitterPing(
                epoch=self.epoch,
                id=emitter_id,
                hits=tuple(emitter_hits),
                telemetry=tele[emitter_id],
            )
            for emitter_id, emitter_hits in hits.items()
        )


@dataclass(slots=True)
class EpochBuffer:
    depth: int
    latest_epoch: int = -1
    buckets: dict[int, EpochBucket] = field(default_factory=dict)

    def advance(self, epoch: int) -> bool:
        if self.latest_epoch >= epoch:
            return False

        self.latest_epoch = epoch
        self.buckets[epoch] = EpochBucket(epoch=epoch)
        return True

    def try_put(self, report: StationReport) -> bool:
        if report.epoch not in self.buckets:
            return False

        self.buckets[report.epoch].put(report)
        return True

    def drain_expired(self) -> tuple[EpochBucket, ...]:
        expired = tuple(
            bucket for bucket in self.buckets.values() if self._is_expired(bucket.epoch)
        )

        for bucket in expired:
            del self.buckets[bucket.epoch]

        return expired

    def _is_expired(self, epoch: int) -> bool:
        oldest_kept_epoch = self.latest_epoch - self.depth + 1
        return epoch < oldest_kept_epoch
