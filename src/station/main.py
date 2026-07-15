from transport.mqtt.client import init_client
from transport.mqtt.codec import JsonCodec
import transport.mqtt.channels as chan

from .station import Station
from common.position import Position
from common.entities import ReceiverId

def main() -> None:
    cid, mqtt_client = init_client()

    try:
        codec = JsonCodec()

        signal_channel = chan.SignalChannel(cid, mqtt_client, codec)
        tick_channel = chan.TickChannel(cid, mqtt_client, codec)
        report_channel = chan.StationReportChannel(cid, mqtt_client, codec)
        heartbeat_channel = chan.HeartbeatChannel(cid, mqtt_client, codec)
        
        stations = [
            Station(
                station_id=ReceiverId("station-1"),
                position=Position(40, -40),
                heartbeat_channel=heartbeat_channel,
                report_channel=report_channel,
            ),
            Station(
                station_id=ReceiverId("station-2"),
                position=Position(-20, 50),
                heartbeat_channel=heartbeat_channel,
                report_channel=report_channel,
            ),
            Station(
                station_id=ReceiverId("station-3"),
                position=Position(-30, -20),
                heartbeat_channel=heartbeat_channel,
                report_channel=report_channel,
            ),
            Station(
                station_id=ReceiverId("station-4"),
                position=Position(0, 60),
                heartbeat_channel=heartbeat_channel,
                report_channel=report_channel,
            ),
            Station(
                station_id=ReceiverId("station-5"),
                position=Position(60, 0),
                heartbeat_channel=heartbeat_channel,
                report_channel=report_channel,
            ),
            Station(
                station_id=ReceiverId("station-6"),
                position=Position(40, 40),
                heartbeat_channel=heartbeat_channel,
                report_channel=report_channel,
            ),
            Station(
                station_id=ReceiverId("station-7"),
                position=Position(-30, 40),
                heartbeat_channel=heartbeat_channel,
                report_channel=report_channel,
            ),
        ]

        for station in stations:
            tick_channel.subscribe(station.on_tick)
            signal_channel.subscribe(station.on_signal)

        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print("Stopping the station service")
    finally:
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
