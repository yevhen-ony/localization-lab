import numpy as np
import numpy.typing as npt

import common.constants as const
from common.position import Position

from .models import ReceiverHits, PositionEstimate


Matrix = npt.NDArray[np.float64]
Vector = npt.NDArray[np.float64]


class TdoaSolver:
    def solve(self, hits: ReceiverHits) -> PositionEstimate | None:
        if len(hits) < 4:
            return None

        M, d = self._equation(hits)
        u0, _, rank, _ = np.linalg.lstsq(M, d, rcond=None)
        if rank < 3:
            return None

        pos = Position(u0[0], u0[1])
        err = self._estimate_error(hits, pos)

        return PositionEstimate(
            pos=pos,
            std=err,
        )

    def _equation(self, hits: ReceiverHits) -> tuple[Matrix, Vector]:
        # M * u = d

        M_rows = []
        d_vals = []

        ref = hits[0]
        x0, y0, t0 = ref.pos.x, ref.pos.y, ref.time_ns

        for hit in hits[1:]:
            x, y, t = hit.pos.x, hit.pos.y, hit.time_ns

            dr = const.propagation_speed * (t - t0)
            M_rows.append([2 * (x - x0), 2 * (y - y0), 2 * dr])
            d_vals.append(x**2 + y**2 - x0**2 - y0**2 - dr**2)

        return np.array(M_rows), np.array(d_vals)

    def _jacobian(self, hits: ReceiverHits, pos: Position) -> Matrix:
        ref = hits[0]
        r1 = ref.pos.distance_to(pos)

        rows = []

        for hit in hits[1:]:
            r = hit.pos.distance_to(pos)

            rows.append(
                [
                    (pos.x - hit.pos.x) / r - (pos.x - ref.pos.x) / r1,
                    (pos.y - hit.pos.y) / r - (pos.y - ref.pos.y) / r1,
                ]
            )
        return np.array(rows, dtype=float)

    def _covariance(self, size: int) -> Matrix:
        return np.eye(size) + np.ones((size, size))

    def _estimate_error(self, hits: ReceiverHits, pos: Position) -> float:
        J = self._jacobian(hits, pos)
        R = self._covariance(len(hits) - 1)
        P = np.linalg.inv(J.T @ np.linalg.solve(R, J))

        var = np.linalg.eigvalsh(P)[-1]
        distance_std = const.propagation_speed * const.arrival_time_std
        return distance_std * np.sqrt(var)
