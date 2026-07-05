from common.observation import ObservationBatch

class Ground:
    def on_observation(self, batch: ObservationBatch) -> None:
        for observation in batch.observations:
            print(
                f"[{batch.epoch}] "
                f"{observation.emitter_id} "
                f"@ {batch.station_id} "
                f"t={observation.arrival_time.ns} ns"
            )
        print()

