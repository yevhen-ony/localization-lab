from __future__ import annotations

import os
from dataclasses import dataclass

import uvicorn
from pymongo import MongoClient

from repository.tracks import MongoTrackRepo

from .providers import set_track_repo
from .app import app


@dataclass(slots=True)
class Config:
    mongo_db: str = "localization-lab"
    mongo_uri: str = "mongodb://localhost:27017"
    listen_port: int = 8080

    @staticmethod
    def from_env() -> Config:
        cfg = Config()

        cfg.mongo_db = os.getenv("MONGO_DB", cfg.mongo_db)
        cfg.mongo_uri = os.getenv("MONGO_URI", cfg.mongo_uri)
        cfg.listen_port = int(os.getenv("LISTEN_PORT", str(cfg.listen_port)))

        return cfg


def main():
    cfg = Config.from_env()

    mongo_client = MongoClient(cfg.mongo_uri)
    mongo_db = mongo_client[cfg.mongo_db]

    repo = MongoTrackRepo(mongo_db)
    repo.setup()

    set_track_repo(repo)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=cfg.listen_port,
    )

if __name__ == "__main__":
    main()
