from dataclasses import dataclass, field
from common.position import Position
import numpy as np
from numpy.typing import NDArray


Vector = NDArray[np.float64]
Matrix = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class LocationSample:
    pos: Position
    std: float
    time: int

    @property
    def z(self):
        """Measurement vector."""
        return np.array([self.pos.x, self.pos.y])

    @property
    def R(self):
        """Measurement covariance matrix."""
        return np.eye(2) * self.std**2


@dataclass(frozen=True, slots=True)
class TrackState:
    """TrackState is a state of the 2D constante velocity model"""

    x: Vector  # state vector [p_x, p_y, v_x, v_y] (4, 1)
    P: Matrix  # state covariance matrix (4 x 4)
    t: int


@dataclass
class ConstantVelocity2D:
    """
    Constant-velocity model with random velocity impulses.

    Velocity kicks Δv ~ N(0, sigma_v^2) arrive as a Poisson process N(t) ~ Poisson(lambda*t),
    producing the process noise covariance Q(dt).

    kick_density = lambda * sigma_v**2
    """

    time_scale: float
    kick_density: float
    H: Matrix = field(init=False)

    def __post_init__(self):
        self.H = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            dtype=float,
        )

    def F(self, dt: float) -> Matrix:
        """Propagation matrix."""
        return np.array(
            [
                [1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            dtype=float,
        )

    def Q(self, dt: float) -> Matrix:
        """Process noise covariance from random velocity impulses."""
        s_pp = dt**3 / 3
        s_pv = dt**2 / 2
        s_vv = dt

        return self.kick_density * np.array(
            [
                [s_pp, 0, s_pv, 0],
                [0, s_pp, 0, s_pv],
                [s_pv, 0, s_vv, 0],
                [0, s_pv, 0, s_vv],
            ],
            dtype=float,
        )

    def time(self, t: int) -> float:
        """ Converts the descret timestamp in the time interval"""
        return t * self.time_scale


class KalmanFilter:
    def __init__(self, model: ConstantVelocity2D):
        self.model = model
        self.I = np.eye(4)

    def predict(self, track: TrackState, t: int) -> TrackState:
        """Predict the next track state using the motion model."""

        tt = t - track.t

        if tt < 0:
            raise ValueError("cannot predict to a past timestamp")

        if tt == 0:
            return track

        dt = self.model.time(tt)

        F = self.model.F(dt)
        Q = self.model.Q(dt)

        x = F @ track.x
        P = F @ track.P @ F.T + Q
        return TrackState(x, P, t)

    def update(self, track: TrackState, sample: LocationSample) -> TrackState:
        """Update the track with a location measurement at the same timestamp."""

        if track.t != sample.time:
            raise ValueError("cannot update with out-of-sync sample")

        H = self.model.H
        R = sample.R

        i = sample.z - H @ track.x
        S = H @ track.P @ H.T + R
        K = track.P @ H.T @ np.linalg.inv(S)

        x = track.x + K @ i
        P = (self.I - K @ H) @ track.P
        return TrackState(x, P, track.t)
