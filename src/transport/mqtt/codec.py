from typing import Protocol
import json


class Codec(Protocol):
    def marshal(self, obj: dict) -> bytes: ...
    def unmarshal(self, raw: bytes) -> dict: ...


class JsonCodec:
    def marshal(self, obj: dict) -> bytes:
        return json.dumps(obj).encode("utf-8")

    def unmarshal(self, raw: bytes):
        return json.loads(raw.decode("utf-8"))
