from pymongo import MongoClient

import transport.mqtt.channels as chan
from transport.mqtt.client import init_client
from transport.mqtt.codec import JsonCodec
from repository.tracks import MongoTrackRepo
from repository.config import MongoConfig

from .ingest import TrackIngestor


def main() -> None:
    cid, mqtt_client = init_client()
    codec = JsonCodec()

    try:
        mongo_config = MongoConfig.from_env()
        mongo_client = MongoClient(mongo_config.uri)
        mongo_db = mongo_client[mongo_config.db]

        repo = MongoTrackRepo(mongo_db)
        ingestor = TrackIngestor(repo)

        sample_chan = chan.TrackSampleChannel(cid, mqtt_client, codec)
        sample_chan.subscribe(ingestor.on_track_sample)

        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print("Stopping the ingestor service")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
