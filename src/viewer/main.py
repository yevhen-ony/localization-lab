from __future__ import annotations

import os
from dataclasses import dataclass, field

import uvicorn
from pymongo import MongoClient

from repository.repos import TrackRepo, DroneTruthRepo, LocalizedRepo
from repository.config import MongoConfig

from .providers import set_track_repo, set_truth_repo, set_local_repo
from .app import app


@dataclass(slots=True)
class Config:
    mongo: MongoConfig = field(default_factory=MongoConfig)
    listen_port: int = 8080

    @staticmethod
    def from_env() -> Config:
        cfg = Config()

        cfg.mongo = MongoConfig.from_env()
        cfg.listen_port = int(os.getenv("LISTEN_PORT", str(cfg.listen_port)))

        return cfg


def main():
    cfg = Config.from_env()

    mongo_client = MongoClient(cfg.mongo.uri)
    mongo_db = mongo_client[cfg.mongo.db]

    track_repo = TrackRepo(mongo_db)
    track_repo.setup()
    set_track_repo(track_repo)

    truth_repo = DroneTruthRepo(mongo_db)
    truth_repo.setup()
    set_truth_repo(truth_repo)

    local_repo = LocalizedRepo(mongo_db)
    local_repo.setup()
    set_local_repo(local_repo)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=cfg.listen_port,
    )


if __name__ == "__main__":
    main()
