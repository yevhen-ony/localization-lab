from common.entities import TrackSample, DroneTruthSample
from repository.repos import TrackRepo, DroneTruthRepo


class TrackIngestor:
    def __init__(self, repo: TrackRepo):
        self._repo = repo

    def ingest(self, sample: TrackSample) -> None:
        self._repo.put(sample)

    def on_track_sample(self, sample: TrackSample) -> None:
        print(
            f"ingestor: track sample: epoch = {sample.epoch} id = {sample.emitter_id}"
        )
        self.ingest(sample)


class DroneTruthIngestor:
    def __init__(self, repo: DroneTruthRepo):
        self._repo = repo

    def ingest(self, sample: DroneTruthSample):
        self._repo.put(sample)

    def on_drone_truth_sample(self, sample: DroneTruthSample) -> None:
        print(
            f"ingestor: drone truth sampe: epoch {sample.epoch} id = {sample.emitter_id}"
        )
        self.ingest(sample)
