from __future__ import annotations

import os
from dataclasses import dataclass

@dataclass
class MongoConfig:
    uri: str = "mongodb://localhost:27017"
    db: str = "localization-lab"

    @staticmethod
    def from_env() -> MongoConfig:
        cfg = MongoConfig()
        cfg.uri = os.getenv("MONGO_URI", cfg.uri)
        cfg.db = os.getenv("MONGO_DB", cfg.db)
        return cfg

