from __future__ import annotations

import os
from dataclasses import dataclass, field

import uvicorn
from pymongo import MongoClient

from repository.repos import TrackRepo
from repository.config import MongoConfig

from .providers import set_track_repo
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

    repo = TrackRepo(mongo_db)
    repo.setup()

    set_track_repo(repo)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=cfg.listen_port,
    )

if __name__ == "__main__":
    main()
