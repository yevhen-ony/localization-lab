import time
from common.position import Position
from common.ids import EmitterId, StationId
from station.station import Station
from ground.ground import Ground
from clock.clock import Clock
from world.terrain import Terrain
from world.medium import Medium
from world.world import World
from world.drone import Drone
from transport.in_memory.channels import (
    TickChannel,
    SignalChannel,
    HeartbeatChannel,
    ObservationChannel,
)


def main():
    tick_channel = TickChannel()
    signal_channel = SignalChannel()
    heartbeat_channel = HeartbeatChannel()
    observation_channel = ObservationChannel()

    terrain = Terrain()
    medium = Medium()
    world = World(
        medium=medium,
        terrain=terrain,
        signal_channel=signal_channel,
    )

    drones = [
        Drone(EmitterId("drone-1"), Position(-5, -1)),
        Drone(EmitterId("drone-2"), Position(12, 12)),
    ]

    for drone in drones:
        world.add_drone(drone)

    stations = [
        Station(
            station_id=StationId("station-1"),
            position=Position(3, 4),
            heartbeat_channel=heartbeat_channel,
            observation_channel=observation_channel,
        ),
        Station(
            station_id=StationId("station-2"),
            position=Position(-4, 2),
            heartbeat_channel=heartbeat_channel,
            observation_channel=observation_channel,
        ),
    ]
    clock = Clock(tick_channel=tick_channel)
    ground = Ground()

    tick_channel.subscribe(world.on_tick)
    heartbeat_channel.subscribe(world.on_heartbeat)

    for station in stations:
        tick_channel.subscribe(station.on_tick)
        signal_channel.subscribe(station.on_signal)

    observation_channel.subscribe(ground.on_observation)

    for i in range(100):
        print(f"epoch {i}")
        clock.emit_tick()
        time.sleep(1)


main()
