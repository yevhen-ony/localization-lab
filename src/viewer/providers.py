from repository.tracks import TrackRepo

_track_repo: TrackRepo | None = None


def set_track_repo(repo: TrackRepo) -> None:
    global _track_repo
    _track_repo = repo


def get_track_repo() -> TrackRepo:
    if _track_repo is None:
        raise RuntimeError("track repo is not set")
    return _track_repo
