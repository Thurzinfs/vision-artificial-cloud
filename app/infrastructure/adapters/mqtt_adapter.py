import asyncio
from uuid import UUID

import aiomqtt

from app.domain.contracts.adapters.mqtt_adapter import IMQTTAdapter
from config import settings


class MQTTAdapter(IMQTTAdapter):
    def __init__(self) -> None:
        self.broker_host = settings.BROKER_HOST
        self.broker_topic = settings.BROKER_TOPIC

    async def mqtt_listener(self, use_case):
        while True:
            try:
                async with aiomqtt.Client(self.broker_host) as client:
                    await client.subscribe(self.broker_topic)

                    async for message in client.messages:
                        payload = bytes(message.payload)

                        try:
                            device = UUID(message.topic.value.split('/')[-1])
                            print('device: ', device)
                        except ValueError:
                            continue

                        try:
                            await use_case.execute(device, payload)
                        except Exception as e:
                            print(f'Erro no use case: {type(e).__name__}: {e}')

            except aiomqtt.MqttError as e:
                await asyncio.sleep(5)

            except Exception as e:
                await asyncio.sleep(5)
