import json
from dataclasses import asdict
from common.localized_sample import LocalizedSample
from common.ids import EmitterId

class Tracker:
    def __init__(self, emitter_ids: list[EmitterId]):
        self._ids = emitter_ids

    def print_sample(self, sample: LocalizedSample) -> None:
        if sample.emitter_id in self._ids: 
            print(json.dumps(asdict(sample), indent=2))
