import asyncio
from uuid import UUID

from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect

from app.api.dependencies.frames import (
    MQTTAdapterDependency,
    ProcessFrameUseCaseDependency,
)


class APIMQTTRouteHandler:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._register_mqtt_event()

    def register_route(self, app: FastAPI) -> None:
        app.include_router(self.router)

    def _register_mqtt_event(self) -> None:
        @self.router.on_event('startup')
        async def startup_event(
            use_case: ProcessFrameUseCaseDependency,
            mqtt_adapter: MQTTAdapterDependency,
        ):
            asyncio.create_task(mqtt_adapter.mqtt_listener(use_case))
