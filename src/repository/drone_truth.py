from typing import Sequence
from dataclasses import asdict

from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ReplaceOne
import common.entities as e

DRONE_TRUTH_COLLECTION = "truth"


class MongoDroneTruthRepo:
    def __init__(self, mongo_db: Database):
        self._collection: Collection = mongo_db[DRONE_TRUTH_COLLECTION]

    def setup(self) -> None:
        self._collection.create_index([("emitter_id", 1), ("epoch", 1)], unique=True)
        self._collection.create_index([("epoch", 1)])

    def put(self, sample: e.DroneTruthSample) -> None:
        self.put_many([sample])

    def put_many(self, samples: Sequence[e.DroneTruthSample]) -> None:
        if not samples:
            return

        ops = [self._to_replace_op(sample) for sample in samples]
        self._collection.bulk_write(ops, ordered=False)
    
    def _to_replace_op(self, sample: e.DroneTruthSample) -> ReplaceOne:
        filter = {
            "emitter_id": str(sample.emitter_id),
            "epoch": int(sample.epoch),
        }
        return ReplaceOne(
            filter=filter,
            replacement=asdict(sample),
            upsert=True,
        )


