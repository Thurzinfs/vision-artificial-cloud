import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.dependencies.frames import (
    get_mqtt_adapter,
    get_websocket_manager_adapter,
)
from app.api.handlers.api_mqtt_handler import APIMQTTRouteHandler
from app.api.handlers.api_websocket_handler import APIWebsocketRouteHandler
from app.application.use_cases.frames import ProcessFrameUseCase


@asynccontextmanager
async def lifespan(app: FastAPI):
    use_case = ProcessFrameUseCase(get_websocket_manager_adapter())
    task = asyncio.create_task(get_mqtt_adapter().mqtt_listener(use_case))
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan, root_path='/api/v1')


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_headers=['*'],
    allow_methods=['*'],
)

websocket_handler = APIWebsocketRouteHandler()

websocket_handler.register_route(app)
