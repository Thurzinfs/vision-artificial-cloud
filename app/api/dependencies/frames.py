from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.application.use_cases.frames import ProcessFrameUseCase
from app.domain.contracts.adapters.websocket_adapter import (
    IWebsocketManagerAdapter,
)
from app.infrastructure.adapters.mqtt_adapter import MQTTAdapter
from app.infrastructure.adapters.websocket_adapter import (
    WebsocketManagerAdapter,
)


@lru_cache
def get_mqtt_adapter() -> MQTTAdapter:
    return MQTTAdapter()


@lru_cache
def get_websocket_manager_adapter() -> WebsocketManagerAdapter:
    return WebsocketManagerAdapter()


def get_process_frame_use_case(
    websocket_adapter: IWebsocketManagerAdapter = Depends(
        get_websocket_manager_adapter
    ),
) -> ProcessFrameUseCase:
    return ProcessFrameUseCase(websocket_adapter=websocket_adapter)


WebSocketAdapterDependency = Annotated[
    WebsocketManagerAdapter, Depends(get_websocket_manager_adapter)
]
MQTTAdapterDependency = Annotated[MQTTAdapter, Depends(get_mqtt_adapter)]
ProcessFrameUseCaseDependency = Annotated[
    ProcessFrameUseCase, Depends(get_process_frame_use_case)
]
