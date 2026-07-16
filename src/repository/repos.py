from dataclasses import asdict
from typing import Any


from pymongo.database import Database

from common.entities import TrackSample, DroneTruthSample

from .sample import MongoSampleRepo


TRACK_COLLECTION = "tracks"
DRONE_TRUTH_COLLECTION = "truths"

# Track Repo

class TrackSampleCodec:
    def encode(self, sample: TrackSample) -> dict[str, Any]:
        return asdict(sample)

    def decode(self, doc: dict[str, Any]) -> TrackSample:
        return TrackSample.from_dict(doc)


class TrackRepo(MongoSampleRepo[TrackSample]):
    def __init__(self, db: Database):
        collection = db[TRACK_COLLECTION]
        super().__init__(collection, TrackSampleCodec())

# DroneTruth Repo

class DroneTruthSampleCodec:
    def encode(self, sample: DroneTruthSample) -> dict[str, Any]:
        return asdict(sample)

    def decode(self, doc: dict[str, Any]) -> DroneTruthSample:
        return DroneTruthSample.from_dict(doc)


class DroneTruthRepo(MongoSampleRepo[DroneTruthSample]):
    def __init__(self, db: Database):
        collection = db[DRONE_TRUTH_COLLECTION]
        super().__init__(collection, DroneTruthSampleCodec())

