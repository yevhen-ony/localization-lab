from typing import Any, Protocol, Callable, Sequence

from pymongo.collection import Collection
from pymongo import ReplaceOne

from common.entities import EmitterId


class Sample(Protocol):
    @property
    def epoch(self) -> int: ...

    @property
    def emitter_id(self) -> EmitterId: ...

class SampleCodec[T: Sample](Protocol):
    def encode(self, sample: T, /) -> dict[str, Any]: ...
    def decode(self, doc: dict[str, Any], /) -> T: ...
 

class MongoSampleRepo[T: Sample]:
    def __init__(
        self,
        collection: Collection,
        codec: SampleCodec[T],
    ):
        self._collection = collection
        self._codec = codec

    def setup(self) -> None:
        self._collection.create_index([("emitter_id", 1), ("epoch", 1)], unique=True)
        self._collection.create_index([("epoch", 1)])

    def put(self, sample: T) -> None:
        self.put_many([sample])

    def put_many(self, samples: Sequence[T]) -> None:
        if not samples:
            return

        ops = [self._to_operation(sample) for sample in samples]
        self._collection.bulk_write(ops, ordered=False)

    def get_samples(
        self,
        emitter_id: EmitterId,
        since_epoch: int | None = None,
    ) -> tuple[T, ...]:
        query: dict[str, Any] = {"emitter_id": str(emitter_id)}
        if since_epoch is not None:
            query["epoch"] = {"$gt": since_epoch}

        docs = self._collection.find(query).sort("epoch", 1)
        return tuple(self._codec.decode(doc) for doc in docs)

    def get_epoch(self, epoch: int) -> tuple[T, ...]:
        query = {"epoch": epoch}
        docs = self._collection.find(query).sort("emitter_id", 1)
        return tuple(self._codec.decode(doc) for doc in docs)

    def last_epoch(self) -> int | None:
        doc = self._collection.find_one(
            sort=[("epoch", -1)],
            projection={"epoch": 1, "_id": 0},
        )
        if doc is None:
            return None
        return int(doc["epoch"])

    def _to_operation(self, sample: T) -> ReplaceOne:
        filter = {
            "emitter_id": str(sample.emitter_id),
            "epoch": int(sample.epoch),
        }
        return ReplaceOne(
            filter=filter,
            replacement=self._codec.encode(sample),
            upsert=True,
        )
