import common.constants as const
from common.ids import EmitterId
from common.samples import LocalizedSample, TrackSample
from transport.in_memory.channels import TrackChannel
from .state import TrackState, LocationEstimate
from .kalman import (
    KalmanFilter,
    ConstantVelocity2D,
)


class Tracker:
    def __init__(self, track_channel: TrackChannel):
        model = ConstantVelocity2D(
            time_scale=const.epoch_duration_s,
            kick_density=const.velocity_kick_density, 
        )
        self._track_channel = track_channel
        self._filter = KalmanFilter(model)
        self._tracks: dict[EmitterId, TrackState] = {}

    def on_location_update(self, sample: LocalizedSample) -> None:
        loc = LocationEstimate(
            id=sample.emitter_id,
            pos=sample.position,
            err=sample.position_std,
            epoch=sample.epoch,
        )
        track = self.track(loc)

        pos, pos_err = track.position()
        vel, vel_err = track.velocity()

        track_sample = TrackSample(
            epoch=track.epoch,
            emitter_id=track.id,
            position=pos,
            position_std=pos_err,
            velocity=vel,
            velocity_std=vel_err,
            telemetry=sample.telemetry
        )

        self._track_channel.publish(track_sample)

    def track(self, loc: LocationEstimate) -> TrackState:
        track = self._tracks.get(loc.id)
        if track is None:
            track = TrackState.from_location(loc)
        else:
            track = self._filter.predict(track, loc.epoch)
            track = self._filter.update(track, loc)

        self._tracks[track.id] = track
        return track

