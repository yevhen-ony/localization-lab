import asyncio
from dataclasses import asdict
from fastapi import WebSocket, WebSocketDisconnect
from repository.repos import TrackRepo
from collections.abc import Awaitable, Callable
from functools import wraps
from common.entities import EmitterId


WebSocketHandler = Callable[..., Awaitable[None]]


def websocket_endpoint(handler: WebSocketHandler) -> WebSocketHandler:
    @wraps(handler)
    async def wrapper(ws: WebSocket, *args, **kwargs) -> None:
        await ws.accept()

        try:
            await handler(ws, *args, **kwargs)
        except WebSocketDisconnect:
            return
        except Exception:
            await ws.close(code=1011)
            raise

    return wrapper


@websocket_endpoint
async def stream_track(ws: WebSocket, repo: TrackRepo, emitter_id: EmitterId) -> None:
    last_epoch = repo.last_epoch()

    while True:
        await asyncio.sleep(0.5)


        print(f"stream {emitter_id=} {last_epoch=}")
        samples = repo.get_samples(emitter_id, last_epoch)
        print(f"samples={len(samples)}")

        if not samples: 
            continue

        last_epoch = samples[-1].epoch
        await ws.send_json([asdict(s) for s in samples])

