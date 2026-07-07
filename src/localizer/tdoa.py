import numpy as np
import numpy.typing as npt

from .models import EmitterPing, EmitterFix
from common.position import Position


Matrix = npt.NDArray[np.float64]
Vector = npt.NDArray[np.float64]


class TdoaSolver:
    propagation_speed: float = 0.3  # m/ns

    def solve(self, ping: EmitterPing) -> EmitterFix | None:
        if len(ping.hits) < 4:
            return None

        M, d = self._build_matrix(ping)
        u0, _, rank, _ = np.linalg.lstsq(M, d, rcond=None)
        if rank < 3:
            return None
        
        pos = Position(u0[0], u0[1])
        err = self._estimate_error(ping, pos)

        return EmitterFix(
            epoch=ping.epoch,
            emitter_id=ping.id,
            position=pos,
            error=err,
        )


    def _build_matrix(self, ping: EmitterPing) -> tuple[Matrix, Vector]:
        # M * u = d
        # u = [x0, y0, r1]
        # x0, y0 - emitter's coords
        # r1 - distance to the referenced receiver

        hits = ping.hits

        M_rows = []
        d_vals = []

        h1 = hits[0]
        x1 = h1.pos.x
        y1 = h1.pos.y
        t1 = h1.time_ns

        for h in hits[1:]:
            x = h.pos.x
            y = h.pos.y
            t = h.time_ns
            dr = self.propagation_speed * (t - t1)

            M_rows.append(
                [
                    2 * (x - x1),
                    2 * (y - y1),
                    2 * dr,
                ]
            )
            d_vals.append(x**2 + y**2 - x1**2 - y1**2 - dr**2)
        return np.array(M_rows), np.array(d_vals)

    
    def _estimate_error(self, ping: EmitterPing, pos: Position) -> float:
        ref = ping.hits[0] 
        r1 = ref.pos.distance_to(pos)

        errors = []

        for hit in ping.hits[1:]:
            predicted = hit.pos.distance_to(pos) - r1
            measured = self.propagation_speed * (hit.time_ns - ref.time_ns)
            errors.append(predicted - measured)

        return np.linalg.norm(errors) / np.sqrt(len(errors)) 

