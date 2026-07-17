from transport.mqtt.client import init_client
from transport.mqtt.codec import JsonCodec
import transport.mqtt.channels as chan
from common.entities import EmitterId
from common.position import Position, Velocity


from .world import World
from .terrain import Terrain
from .medium import Medium
from .drone import Drone


def main() -> None:
    cid, mqtt_client = init_client()

    try:
        codec = JsonCodec()

        signal_chan = chan.SignalChannel(cid, mqtt_client, codec)
        tick_chan = chan.TickChannel(cid, mqtt_client, codec)
        heartbeat_chan = chan.HeartbeatChannel(cid, mqtt_client, codec)
        drone_truth_chan = chan.DroneTruthChannel(cid, mqtt_client, codec)

        terrain = Terrain()
        medium = Medium()
        world = World(
            medium=medium,
            terrain=terrain,
            signal_channel=signal_chan,
        )

        drones = [
            Drone(EmitterId("drone-1"), Position(-20, -20), Velocity(1, 1), 0.5),
        ]

        for drone in drones:
            world.add_drone(drone)
            drone.set_truth_channel(drone_truth_chan)

        tick_chan.subscribe(world.on_tick)
        heartbeat_chan.subscribe(world.on_heartbeat)

        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print("Stopping the world service")
    finally:
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
