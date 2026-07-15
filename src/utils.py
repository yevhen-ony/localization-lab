import json
from dataclasses import asdict
from common.entities import (
    TrackSample,
    LocalizedSample,
    EmitterId,
)


class TrackSamplePrinter:
    def __init__(self, emitter_ids: list[EmitterId]):
        self._ids = emitter_ids

    def print_sample(self, sample: TrackSample) -> None:
        if sample.emitter_id in self._ids:
            print(json.dumps(asdict(sample), indent=2))


class LocalizedSamplePrinter:
    def __init__(self, emitter_ids: list[EmitterId]):
        self._ids = emitter_ids

    def print(self, sample: LocalizedSample) -> None:
        if sample.emitter_id in self._ids:
            print(json.dumps(asdict(sample), indent=2))
