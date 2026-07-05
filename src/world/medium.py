from dataclasses import dataclass

from common.position import Position
from common.arrival_time import ArrivalTime


@dataclass(frozen=True, slots=True)
class Propagation:
    arrival_time: ArrivalTime


@dataclass(frozen=True)
class Medium:
    action_range: float = 100.0
    noise_level: float = 0.3
    propagation_speed: float = 0.3 # m/ns 

    def propagate(
        self,
        emitter_position: Position,
        receiver_position: Position,
    ) -> Propagation | None:
        dist = receiver_position.distance_to(emitter_position)
        if dist > self.action_range:
            return None

        arrival_time_ns = dist / self.propagation_speed

        return Propagation(  
            arrival_time=ArrivalTime(ns=round(arrival_time_ns)),
        )
