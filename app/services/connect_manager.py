import random
from dataclasses import dataclass
from typing import Dict

import orjson
from starlette.websockets import WebSocket


names = ['Vova', 'Denis', 'Test', 'Kto-to tam', 'Chess']

@dataclass
class Player:
    name: str
    websocket: WebSocket
    ready_to_game: bool = False


class ConnectionManager:
    _instance = None
    active_connections: Dict[str, Player] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        name = websocket.headers.get('name', random.choice())
        self.active_connections[name] = Player(name, websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket.headers['name'])

    @staticmethod
    async def get_message(websocket: WebSocket) -> str:
        data = await websocket.receive_text()
        message = orjson.loads(data)
        message['from_'] = websocket.headers['name']
        return message

    @staticmethod
    async def reply(message: dict, websocket: WebSocket):
        await websocket.send_text(orjson.dumps(message))

    async def send_to_client(self, name: str, message: dict):
        await self.active_connections[name].websocket.send_text(orjson.dumps(message))
