from __future__ import annotations

import random
from typing import Protocol
from dataclasses import dataclass

from transport.protocols import DroneTruthChannel

from common.position import Position, Velocity
import common.constants as const
import common.entities as e

from .navigation import Navigation


@dataclass(frozen=True, slots=True)
class Emission:
    slot: int
    telemetry: e.Telemetry


class DroneEnvironment(Protocol):
    def measure(self, position: Position) -> e.Telemetry: ...
    def transmit(self, drone: Drone, emission: Emission) -> int: ...


class Drone:
    def __init__(
        self,
        drone_id: e.EmitterId,
        position: Position,
        velocity: Velocity,
        noise: float = 0,
    ):
        self._id = drone_id
        self._navi = Navigation(position, velocity, noise)
        self._env: DroneEnvironment | None = None
        self._chan: DroneTruthChannel | None = None

    @property
    def env(self) -> DroneEnvironment:
        assert self._env is not None, "Drone is not attached to an environment"
        return self._env

    @property
    def id(self) -> e.EmitterId:
        return self._id

    @property
    def position(self) -> Position:
        return self._navi.position

    @property
    def velocity(self) -> Velocity:
        return self._navi.velocity

    def on_tick(self, tick: e.Tick) -> None:
        dt = const.epoch_duration_s
        self._navi.advance(dt)

        if self._chan:
            self._chan.publish(self._truth(tick.epoch))

        telemetry = self.env.measure(self.position)
        emission = Emission(
            slot=random.randrange(0, tick.slots),
            telemetry=telemetry,
        )
        self.env.transmit(self, emission)

    def bind_environment(self, env: DroneEnvironment) -> None:
        self._env = env

    def set_truth_channel(self, channel: DroneTruthChannel) -> None:
        self._chan = channel

    def _truth(self, epoch: int) -> e.DroneTruthSample:
        return e.DroneTruthSample(
            epoch=epoch,
            emitter_id=self.id,
            position=self.position,
            velocity=self._navi.velocity,
        )


