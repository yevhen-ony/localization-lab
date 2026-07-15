from transport.mqtt.client import init_client
from transport.mqtt.codec import JsonCodec
import transport.mqtt.channels as chan

from .localizer import Localizer


def main() -> None:
    cid, mqtt_client = init_client()

    try:
        codec = JsonCodec()
        report_chan = chan.StationReportChannel(cid, mqtt_client, codec)
        sample_chan = chan.LocalizedSampleChannel(cid, mqtt_client, codec)

        localizer = Localizer(sample_chan)
        report_chan.subscribe(localizer.on_station_report)

        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print("Stopping the localizer service")
    finally:
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
