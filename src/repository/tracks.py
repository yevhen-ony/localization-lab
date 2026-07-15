from collections.abc import Sequence
from dataclasses import asdict
from typing import Any, Protocol

from pymongo import ReplaceOne
from pymongo.collection import Collection
from pymongo.database import Database

from common.position import Velocity, Position
from common.entities import (
    TrackSample,
    EmitterId,
    Telemetry,
)


TRACK_COLLECTION = "tracks"


class TrackRepo(Protocol):
    def put(self, sample: TrackSample) -> None: ...
    def put_many(self, samples: Sequence[TrackSample]) -> None: ...
    def last_epoch(self) -> int | None: ...
    def get_epoch(self, epoch: int) -> tuple[TrackSample, ...]: ...
    def get_track(
        self,
        emitter_id: EmitterId,
        since_epoch: int | None = None,
    ) -> tuple[TrackSample, ...]: ...


class MongoTrackRepo:
    def __init__(self, mongo_db: Database):
        self._collection: Collection = mongo_db[TRACK_COLLECTION]

    def setup(self) -> None:
        self._collection.create_index([("emitter_id", 1), ("epoch", 1)], unique=True)
        self._collection.create_index([("epoch", 1)])

    def put(self, sample: TrackSample) -> None:
        self.put_many([sample])

    def put_many(self, samples: Sequence[TrackSample]) -> None:
        if not samples:
            return

        ops = [self._to_replace_op(sample) for sample in samples]
        self._collection.bulk_write(ops, ordered=False)

    def get_track(
        self, emitter_id: EmitterId, since_epoch: int | None = None
    ) -> tuple[TrackSample, ...]:
        query: dict[str, Any] = {"emitter_id": str(emitter_id)}
        if since_epoch is not None:
            query["epoch"] = {"$gt": since_epoch}

        docs = self._collection.find(query).sort("epoch", 1)
        return tuple(self._from_doc(doc) for doc in docs)

    def get_epoch(self, epoch: int) -> tuple[TrackSample, ...]:
        query = {"epoch": epoch}
        docs = self._collection.find(query).sort("emitter_id", 1)
        return tuple(self._from_doc(doc) for doc in docs)

    def last_epoch(self) -> int | None:
        doc = self._collection.find_one(
            sort=[("epoch", -1)],
            projection={"epoch": 1, "_id": 0},
        )
        if doc is None:
            return None
        return int(doc["epoch"])

    def _to_replace_op(self, sample: TrackSample) -> ReplaceOne:
        filter = {
            "emitter_id": str(sample.emitter_id),
            "epoch": int(sample.epoch),
        }
        return ReplaceOne(
            filter=filter,
            replacement=self._to_doc(sample),
            upsert=True,
        )

    def _to_doc(self, sample: TrackSample) -> dict:
        return asdict(sample)

    def _from_doc(self, doc: dict) -> TrackSample:
        pos = doc["position"]
        vel = doc["velocity"]
        tele = doc["telemetry"]

        return TrackSample(
            epoch=int(doc["epoch"]),
            emitter_id=EmitterId(doc["emitter_id"]),
            position=Position(**pos),
            position_std=float(doc["position_std"]),
            velocity=Velocity(**vel),
            velocity_std=float(doc["velocity_std"]),
            telemetry=Telemetry(**tele),
        )
