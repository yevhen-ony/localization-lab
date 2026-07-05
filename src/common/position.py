from __future__ import annotations

import random
import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """Cartesian position."""

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
