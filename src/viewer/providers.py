from repository.repos import TrackRepo, DroneTruthRepo, LocalizedRepo

_track_repo: TrackRepo | None = None
_truth_repo: DroneTruthRepo | None = None
_local_repo: LocalizedRepo | None = None


def set_track_repo(repo: TrackRepo) -> None:
    global _track_repo
    _track_repo = repo


def get_track_repo() -> TrackRepo:
    if _track_repo is None:
        raise RuntimeError("track repo is not set")
    return _track_repo


def set_truth_repo(repo: DroneTruthRepo) -> None:
    global _truth_repo
    _truth_repo = repo


def get_truth_repo() -> DroneTruthRepo:
    if _truth_repo is None:
        raise RuntimeError("truth repo is not set")
    return _truth_repo


def set_local_repo(repo: LocalizedRepo):
    global _local_repo
    _local_repo = repo


def get_local_repo():
    if _local_repo is None:
        raise RuntimeError("local repo is not set")
    return _local_repo
