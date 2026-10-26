from uuid import UUID

from app.domain.contracts.adapters.websocket_adapter import (
    IWebsocketManagerAdapter,
)


class ProcessFrameUseCase:
    def __init__(self, websocket_adapter: IWebsocketManagerAdapter) -> None:
        self.websocket_adapter = websocket_adapter

    async def execute(self, device: UUID, image: bytes):
        if not image:
            return

        await self.websocket_adapter.send_pessoal_message(
            device, device.bytes + image
        )
