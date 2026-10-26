import json
from uuid import UUID

from app.domain.contracts.adapters.websocket_adapter import (
    IWebsocketManagerAdapter,
)


class SendResultUseCase:
    def __init__(self, ws_adapter: IWebsocketManagerAdapter) -> None:
        self.ws_adapter = ws_adapter

    async def execute(self, payload: str):
        try:
            device = UUID(json.loads(payload)['device'])

        except (ValueError, KeyError, TypeError):
            return
        await self.ws_adapter.send_results_to_apps(device, payload)
