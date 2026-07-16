from common.entities import TrackSample, DroneTruthSample
from repository.tracks import MongoTrackRepo
from repository.drone_truth import MongoDroneTruthRepo


class TrackIngestor:
    def __init__(self, repo: MongoTrackRepo):
        self._repo = repo

    def ingest(self, sample: TrackSample) -> None:
        self._repo.put(sample)

    def on_track_sample(self, sample: TrackSample) -> None:
        print(
            f"ingestor: track sample: epoch = {sample.epoch} id = {sample.emitter_id}"
        )
        self.ingest(sample)


class DroneTruthIngestor:
    def __init__(self, repo: MongoDroneTruthRepo):
        self._repo = repo

    def ingest(self, sample: DroneTruthSample):
        self._repo.put(sample)

    def on_drone_truth_sample(self, sample: DroneTruthSample) -> None:
        print(
            f"ingestor: drone truth sampe: epoch {sample.epoch} id = {sample.emitter_id}"
        )
        self.ingest(sample)
