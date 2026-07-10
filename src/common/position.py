from __future__ import annotations

import random
import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """Cartesian position in meters."""

    x: float
    y: float
    z: float = 0.0

    def distance_to(self, other: Position) -> float:
        """Euclidean distance to another position."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def __add__(self, other: Position) -> Position:
        return Position(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: Position) -> Position:
        return Position(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    @staticmethod
    def random(scale: float) -> "Position":
        return Position(
            x=random.uniform(-scale, scale),
            y=random.uniform(-scale, scale),
        )


@dataclass(frozen=True, slots=True)
class Velocity:
    """Cartesian velocity in meters per second"""
    x: float
    y: float
    z: float = 0

    def step(self, dt: float) -> Position:
        return Position(self.x*dt, self.y*dt, self.z*dt)

    
    def __add__(self, other: Velocity) -> Velocity:
        return Velocity(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: Velocity) -> Velocity:
        return Velocity(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )
