from pymongo import MongoClient

import transport.mqtt.channels as chan
from transport.mqtt.client import init_client
from transport.mqtt.codec import JsonCodec
from repository.repos import TrackRepo, DroneTruthRepo, LocalizedRepo
from repository.config import MongoConfig

from .ingest import TrackIngestor, DroneTruthIngestor, LocalizedIngestor


def main() -> None:
    cid, mqtt_client = init_client()
    codec = JsonCodec()

    try:
        mongo_config = MongoConfig.from_env()
        mongo_client = MongoClient(mongo_config.uri)
        mongo_db = mongo_client[mongo_config.db]

        # Drone track

        track_repo = TrackRepo(mongo_db)
        track_repo.setup()
        track_ingestor = TrackIngestor(track_repo)

        track_chan = chan.TrackSampleChannel(cid, mqtt_client, codec)
        track_chan.subscribe(track_ingestor.on_track_sample)

        # Drone truth

        truth_repo = DroneTruthRepo(mongo_db)
        truth_repo.setup()
        truth_ingestor = DroneTruthIngestor(truth_repo)

        truth_chan = chan.DroneTruthChannel(cid, mqtt_client, codec)
        truth_chan.subscribe(truth_ingestor.on_drone_truth_sample) 

        # Drone localized

        local_repo = LocalizedRepo(mongo_db)
        local_repo.setup()
        local_ingestor = LocalizedIngestor(local_repo)

        local_chan = chan.LocalizedSampleChannel(cid, mqtt_client, codec)
        local_chan.subscribe(local_ingestor.on_localized_sample)

        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print("Stopping the ingestor service")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
