from dataclasses import dataclass
import math

from common.position import Position
from common.entities import Telemetry


@dataclass
class Terrain:
    def sample(self, position: Position) -> Telemetry:
        return Telemetry(
            temperature=self._temperature(position.x, position.y),
        )

    @staticmethod
    def _temperature(x: float, y: float) -> float:
        return (
            100.0
            + 20.0 * math.sin(x / 30.0)
            + 15.0 * math.cos(y / 20.0)
        )
