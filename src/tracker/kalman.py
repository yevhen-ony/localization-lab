from dataclasses import dataclass, field
import numpy as np
import common.constants as const

from .state import (
    TrackState,
    LocationEstimate,
    Matrix,
)


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
        """Converts the descret timestamp in the time interval"""
        return t * const.epoch_duration_s


class KalmanFilter:
    def __init__(self, model: ConstantVelocity2D):
        self.model = model
        self.I = np.eye(4)

    def predict(self, track: TrackState, t: int) -> TrackState:
        """Predict the next track state using the motion model."""

        tt = t - track.epoch

        if tt < 0:
            raise ValueError("cannot predict to a past timestamp")

        if tt == 0:
            return track

        dt = self.model.time(tt)

        F = self.model.F(dt)
        Q = self.model.Q(dt)

        x = F @ track.x
        P = F @ track.P @ F.T + Q
        return track.update(x, P, t)

    def update(self, track: TrackState, loc: LocationEstimate) -> TrackState:
        """Update the track with a location measurement at the same timestamp."""

        if track.epoch != loc.epoch:
            raise ValueError("cannot update with out-of-sync sample")

        H = self.model.H
        R = loc.R

        i = loc.z - H @ track.x

        S = H @ track.P @ H.T + R
        A = track.P @ H.T
        K = np.linalg.solve(S.T, A.T).T

        x = track.x + K @ i
        P = (self.I - K @ H) @ track.P
        return track.update(x, P, track.epoch)
