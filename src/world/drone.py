from __future__ import annotations

import random
from typing import Protocol
from dataclasses import dataclass

from common.position import Position, Velocity
import common.constants as const
from common.entities import (
        EmitterId,
        Telemetry,
        Tick,
)

from .navigation import Navigation


@dataclass(frozen=True, slots=True)
class Emission:
    slot: int
    telemetry: Telemetry


class DroneEnvironment(Protocol):
    def measure(self, position: Position) -> Telemetry: ...
    def transmit(self, drone: Drone, emission: Emission) -> int: ...


class Drone:
    def __init__(
        self,
        drone_id: EmitterId,
        position: Position,
        velocity: Velocity,
        noise: float = 0,
    ):
        self._id = drone_id
        self._navi = Navigation(position, velocity, noise)
        self._env: DroneEnvironment | None = None

    @property
    def env(self) -> DroneEnvironment:
        assert self._env is not None, "Drone is not attached to an environment"
        return self._env

    @property
    def id(self) -> EmitterId:
        return self._id

    @property
    def position(self) -> Position:
        return self._navi.position

    def on_tick(self, tick: Tick) -> None:
        dt = const.epoch_duration_s
        self._navi.advance(dt)

        telemetry = self.env.measure(self.position)
        emission = Emission(
            slot=random.randrange(0, tick.slots),
            telemetry=telemetry,
        )
        self.env.transmit(self, emission)

    def bind_environment(self, env: DroneEnvironment) -> None:
        self._env = env
