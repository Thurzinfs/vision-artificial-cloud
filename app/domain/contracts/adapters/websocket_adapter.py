from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import WebSocket


class IWebsocketManagerAdapter(ABC):
    @abstractmethod
    async def connect(self, client: UUID, websocket: WebSocket) -> None:
        ...

    @abstractmethod
    async def send_pessoal_message(self, client: UUID, message: bytes) -> None:
        ...

    @abstractmethod
    async def broadcast_to_local_servers(self, message: bytes | str) -> None:
        ...

    @abstractmethod
    def disconnect(self, client: UUID) -> None:
        ...

    @abstractmethod
    async def connect_app(self, device: UUID, websocket: WebSocket) -> None:
        ...

    @abstractmethod
    async def send_results_to_apps(self, device: UUID, payload: str) -> None:
        ...

    @abstractmethod
    def disconnect_app(self, device: UUID, websocket: WebSocket) -> None:
        ...
