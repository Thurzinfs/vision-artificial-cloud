from collections import defaultdict
from typing import Dict
from uuid import UUID

from fastapi import WebSocket

from app.domain.contracts.adapters.websocket_adapter import (
    IWebsocketManagerAdapter,
)


class WebsocketManagerAdapter(IWebsocketManagerAdapter):
    def __init__(self) -> None:
        self.active_connections: Dict[UUID, WebSocket] = {}
        self.apps: dict[UUID, set[WebSocket]] = defaultdict(set)

    async def connect(self, client: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[client] = websocket

    async def send_pessoal_message(self, client: UUID, message: bytes) -> None:
        if client in self.active_connections:
            websocket = self.active_connections[client]
            await websocket.send_bytes(message)

    async def broadcast_to_local_servers(self, message: bytes) -> None:
        for connection in self.active_connections.values():
            await connection.send_bytes(message)

    def disconnect(self, client: UUID) -> None:
        if client in self.active_connections:
            del self.active_connections[client]

    async def connect_app(self, device: UUID, websocket: WebSocket):
        await websocket.accept()
        self.apps[device].add(websocket)

    async def send_results_to_apps(self, device: UUID, payload: str):
        for ws in list(self.apps.get(device, ())):
            try:
                await ws.send_text(payload)

            except Exception:
                self.apps[device].discard(ws)

    def disconnect_app(self, device: UUID, websocket: WebSocket) -> None:
        self.apps[device].discard(websocket)
