from uuid import UUID

from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect

from app.api.dependencies.frames import WebSocketAdapterDependency
from app.api.dependencies.results import SendResultUseCaseDependency


class APIWebsocketRouteHandler:
    def __init__(self) -> None:
        self.websocket_route = APIRouter()
        self._register_websocket_router()
        self._register_websocket_app_router()

    def register_route(self, app: FastAPI) -> None:
        app.include_router(self.websocket_route)

    def _register_websocket_router(self) -> None:
        @self.websocket_route.websocket('/ws/local/{client}')
        async def websocket_endpoint(
            websocket: WebSocket,
            client: UUID,
            adapter: WebSocketAdapterDependency,
            use_case: SendResultUseCaseDependency,
        ):
            await adapter.connect(client, websocket)

            try:
                while True:
                    data = await websocket.receive_text()
                    print(data)
                    await use_case.execute(data)

            except WebSocketDisconnect:
                adapter.disconnect(client)

    def _register_websocket_app_router(self) -> None:
        @self.websocket_route.websocket('/ws/app/{device}')
        async def websocket_app(
            device: UUID,
            websocket: WebSocket,
            adapter: WebSocketAdapterDependency,
        ):
            await adapter.connect_app(device, websocket)
            try:
                while True:
                    await websocket.receive_text()

            except WebSocketDisconnect:
                adapter.disconnect_app(device, websocket)
