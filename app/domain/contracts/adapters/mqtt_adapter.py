from abc import ABC, abstractmethod


class IMQTTAdapter(ABC):
    @abstractmethod
    async def mqtt_listener(self, callback):
        ...
