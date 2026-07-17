import pathlib

from fastapi import Depends, FastAPI, WebSocket, Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from common.entities import EmitterId
from repository.repos import TrackRepo, DroneTruthRepo, LocalizedRepo

from .handlers import stream_track, stream_truth, stream_local
from .providers import get_track_repo, get_truth_repo, get_local_repo

STATIC_DIR = pathlib.Path(__file__).parent / "static"

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/track")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "track.html")


@app.get("/map")
def map() -> FileResponse:
    return FileResponse(STATIC_DIR / "map.html")


@app.get("/local")
def local() -> FileResponse:
    return FileResponse(STATIC_DIR / "local.html")


@app.websocket("/ws/tracks/{emitter_id}")
async def track_ws(
    ws: WebSocket,
    emitter_id: str = Path(min_length=1),
    repo: TrackRepo = Depends(get_track_repo),
) -> None:
    await stream_track(ws, repo, EmitterId(emitter_id))


@app.websocket("/ws/truth/{emitter_id}")
async def truth_ws(
    ws: WebSocket,
    emitter_id: str = Path(min_length=1),
    repo: DroneTruthRepo = Depends(get_truth_repo),
) -> None:
    await stream_truth(ws, repo, EmitterId(emitter_id))


@app.websocket("/ws/local/{emitter_id}")
async def local_ws(
    ws: WebSocket,
    emitter_id: str = Path(min_length=1),
    repo: LocalizedRepo = Depends(get_local_repo),
) -> None:
    await stream_local(ws, repo, EmitterId(emitter_id))
