from common.samples import TrackSample

from repository.tracks import TrackRepo

class TrackIngestor:
    def __init__(self, repo: TrackRepo):
        self._repo = repo

    def ingest(self, sample: TrackSample) -> None:
        self._repo.put(sample)

    def on_track_sample(self, sample: TrackSample) -> None:
        self.ingest(sample)


