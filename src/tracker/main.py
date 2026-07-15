from transport.mqtt.client import init_client
from transport.mqtt.codec import JsonCodec
import transport.mqtt.channels as chan

from .tracker import Tracker


def main() -> None:
    cid, mqtt_client = init_client()
    codec = JsonCodec()

    try:
        locsample_chan = chan.LocalizedSampleChannel(cid, mqtt_client, codec)
        tracksample_chan = chan.TrackSampleChannel(cid, mqtt_client, codec)

        tracker = Tracker(tracksample_chan)
        locsample_chan.subscribe(tracker.on_location_update)

        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print("Stopping the tracker service")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
