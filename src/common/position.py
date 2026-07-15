from __future__ import annotations

import random
import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """Cartesian position in meters."""

    x: float
    y: float

    def distance_to(self, other: Position) -> float:
        """Euclidean distance to another position."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def __add__(self, other: Position) -> Position:
        return Position(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: Position) -> Position:
        return Position(
            self.x - other.x,
            self.y - other.y,
        )

    @staticmethod
    def random(scale: float) -> Position:
        return Position(
            x=random.uniform(-scale, scale),
            y=random.uniform(-scale, scale),
        )


@dataclass(frozen=True, slots=True)
class Velocity:
    """Cartesian velocity in meters per second"""
    x: float
    y: float

    def step(self, dt: float) -> Position:
        return Position(self.x*dt, self.y*dt)

    
    def __add__(self, other: Velocity) -> Velocity:
        return Velocity(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: Velocity) -> Velocity:
        return Velocity(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, factor: float) -> Velocity:
          return Velocity(self.x * factor, self.y * factor)


    def __rmul__(self, factor: float) -> Velocity:
          return self * factor

    
    @staticmethod
    def random(scale: float) -> Velocity:
        return Velocity(
            x=random.uniform(-scale, scale),
            y=random.uniform(-scale, scale),
        )
