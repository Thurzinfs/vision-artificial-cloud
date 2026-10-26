from typing import Annotated

from fastapi import Depends

from app.api.dependencies.frames import get_websocket_manager_adapter
from app.application.use_cases.results import SendResultUseCase
from app.domain.contracts.adapters.websocket_adapter import (
    IWebsocketManagerAdapter,
)


def get_send_result_use_case(
    adapter: IWebsocketManagerAdapter = Depends(get_websocket_manager_adapter),
) -> SendResultUseCase:
    return SendResultUseCase(ws_adapter=adapter)


SendResultUseCaseDependency = Annotated[
    SendResultUseCase, Depends(get_send_result_use_case)
]
