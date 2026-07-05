from __future__ import annotations

from common.ids import StationId
from common.heartbeat import Heartbeat
from common.tick import Tick
from common.telemetry import Telemetry
from common.position import Position
from common.signal import Signal

from transport.in_memory.channels import SignalChannel

from .drone import Drone, Emission
from .medium import Medium
from .terrain import Terrain


class World:
    def __init__(
        self,
        medium: Medium,
        terrain: Terrain,
        signal_channel: SignalChannel,
    ) -> None:
        self.drones: list[Drone] = []
        self._terrain = terrain
        self._medium = medium 
        self._signal_channel = signal_channel
        self._stations: dict[StationId, Heartbeat] = {}

    def on_heartbeat(self, heartbeat: Heartbeat) -> None:
        self._stations[heartbeat.station_id] = heartbeat

    def on_tick(self, tick: Tick) -> None:
        for drone in self.drones:
            drone.on_tick(tick)

    def measure(self, position: Position) -> Telemetry:
        return self._terrain.sample(position)
        
    def transmit(self, drone: Drone, emission: Emission) -> int:
        count = 0
        for station in self._stations.values():

            propagation = self._medium.propagate(
                emitter_position=drone.position,
                receiver_position=station.position,
            )
            
            if propagation is None:
                continue
            signal = Signal(
                slot=emission.slot,
                emitter_id=drone.id,
                receiver_id=station.station_id,
                telemetry=emission.telemetry,
                arrival_time=propagation.arrival_time,
            )

            self._signal_channel.publish(signal)
            count += 1

        return count
    
    def add_drone(self, drone: Drone):
        drone.bind_environment(self)
        self.drones.append(drone)
