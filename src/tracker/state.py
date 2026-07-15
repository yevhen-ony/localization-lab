from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

from common.position import Position, Velocity
from common.entities import EmitterId
import common.constants as const

Vector = NDArray[np.float64]
Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class LocationEstimate:
    id: EmitterId
    pos: Position
    err: float
    epoch: int

    @property
    def z(self):
        """Measurement vector."""
        return np.array([self.pos.x, self.pos.y])

    @property
    def R(self):
        """Measurement covariance matrix."""
        err = max(self.err, const.min_location_std) 
        return np.eye(2) * err**2


@dataclass(frozen=True, slots=True)
class TrackState:
    """TrackState is a state of the 2D constante velocity model"""

    id: EmitterId
    epoch: int
    x: Vector  # state vector [p_x, p_y, v_x, v_y] (4, 1)
    P: Matrix  # state covariance matrix (4 x 4)

    def update(self, x: Vector, P: Matrix, t: int) -> TrackState:
        return TrackState(self.id, t, x, P)

    @staticmethod
    def from_location(loc: LocationEstimate) -> TrackState:
        s_pp = loc.err**2
        s_vv = 3.0**2

        return TrackState(
            id=loc.id,
            epoch=loc.epoch,
            x=np.array([loc.pos.x, loc.pos.y, 0, 0]),
            P=np.diag([s_pp, s_pp, s_vv, s_vv]),
        )

    def _error_2d(self, P: Matrix) -> float:
        var = np.linalg.eigvalsh(P)[-1]
        return np.sqrt(var)

    def position(self) -> tuple[Position, float]:
        err = self._error_2d(self.P[:2, :2])
        pos = Position(self.x[0], self.x[1])
        return pos, err

    def velocity(self) -> tuple[Velocity, float]:
        err = self._error_2d(self.P[2:, 2:])
        vel = Velocity(self.x[2], self.x[3])
        return vel, err
