import pathlib

from fastapi import Depends, FastAPI, WebSocket, Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from common.entities import EmitterId
from repository.repos import TrackRepo

from .handlers import stream_track
from .providers import get_track_repo

STATIC_DIR = pathlib.Path(__file__).parent / "static"

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.websocket("/ws/tracks/{emitter_id}")
async def track_ws(
    ws: WebSocket,
    emitter_id: str = Path(min_length=1),
    repo: TrackRepo = Depends(get_track_repo)
) -> None:
    await stream_track(ws, repo, EmitterId(emitter_id))
