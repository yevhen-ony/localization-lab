import time
from common.position import Position
from common.ids import EmitterId, ReceiverId
from station.station import Station
from localizer.localizer import Localizer
from clock.clock import Clock
from tracker.tracker import Tracker
from repository.tracks import MongoTrackRepo
from ingestor.ingest import TrackIngestor
from world.terrain import Terrain
from world.medium import Medium
from world.world import World
from world.drone import Drone
from transport.in_memory.channels import (
    TickChannel,
    SignalChannel,
    HeartbeatChannel,
    StationReportChannel,
    LocalizedSampleChannel,
    TrackChannel,
)

from pymongo import MongoClient


def main():
    tick_channel = TickChannel()
    signal_channel = SignalChannel()
    heartbeat_channel = HeartbeatChannel()
    report_channel = StationReportChannel()
    location_channel = LocalizedSampleChannel()
    track_channel = TrackChannel()

    terrain = Terrain()
    medium = Medium()
    world = World(
        medium=medium,
        terrain=terrain,
        signal_channel=signal_channel,
    )

    drones = [
        Drone(EmitterId("drone-1"), Position(-50, -20)),
        Drone(EmitterId("drone-2"), Position(30, 40)),
    ]

    for drone in drones:
        world.add_drone(drone)

    stations = [
        Station(
            station_id=ReceiverId("station-1"),
            position=Position(40, -40),
            heartbeat_channel=heartbeat_channel,
            observation_channel=report_channel,
        ),
        Station(
            station_id=ReceiverId("station-2"),
            position=Position(-20, 50),
            heartbeat_channel=heartbeat_channel,
            observation_channel=report_channel,
        ),
        Station(
            station_id=ReceiverId("station-3"),
            position=Position(-30, -20),
            heartbeat_channel=heartbeat_channel,
            observation_channel=report_channel,
        ),
        Station(
            station_id=ReceiverId("station-4"),
            position=Position(0, 60),
            heartbeat_channel=heartbeat_channel,
            observation_channel=report_channel,
        ),
        Station(
            station_id=ReceiverId("station-5"),
            position=Position(60, 0),
            heartbeat_channel=heartbeat_channel,
            observation_channel=report_channel,
        ),
        Station(
            station_id=ReceiverId("station-6"),
            position=Position(40, 40),
            heartbeat_channel=heartbeat_channel,
            observation_channel=report_channel,
        ),
        Station(
            station_id=ReceiverId("station-7"),
            position=Position(-30, 40),
            heartbeat_channel=heartbeat_channel,
            observation_channel=report_channel,
        ),
    ]
    clock = Clock(tick_channel=tick_channel)
    localizer = Localizer(
        station_count=len(stations),
        sample_channel=location_channel,
    )
    tracker = Tracker(track_channel)


    mongo_client = MongoClient("mongodb://localhost:27017")
    mongo_db = mongo_client["localization-lab"]

    repo = MongoTrackRepo(mongo_db)
    ingestor = TrackIngestor(repo)

    tick_channel.subscribe(world.on_tick)
    heartbeat_channel.subscribe(world.on_heartbeat)

    for station in stations:
        tick_channel.subscribe(station.on_tick)
        signal_channel.subscribe(station.on_signal)

    report_channel.subscribe(localizer.on_station_report)
    location_channel.subscribe(tracker.on_location_update)
    track_channel.subscribe(ingestor.on_track_sample)


    for i in range(100):
        print(f"epoch {i}")
        clock.emit_tick()
        time.sleep(1)


main()
