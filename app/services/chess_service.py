import asyncio
from uuid import uuid4

from app.models.common import EventType
from app.models.message import Message
from app.services.connect_manager import ConnectionManager
from board import BOARD


class ChessService:

    def __init__(self):
        self.connection_manager = ConnectionManager()

    async def start_game(self, message: Message):
        ready_player = self.connection_manager.active_connections[message.from_]
        ready_player.ready_to_game = True

        while True:
            await asyncio.sleep(0.01)

            for player in self.connection_manager.active_connections.values():
                if player.ready_to_game and ready_player.name != player.name:
                    return {
                        'event_type': EventType.START_GAME,
                        'payload': {
                            'you': message.from_,
                            'opponent': player.name,
                            'game_id': uuid4(),
                        }
                    }

    def get_online_players(self):
        return {
            'event_type': EventType.ONLINE_PLAYERS,
            'payload': {
                'online_players': [
                    {name: str(player.websocket.client)} for name, player in
                    self.connection_manager.active_connections.items()
                ],
                'count_online_players': len(self.connection_manager.active_connections),
            }
        }

    @staticmethod
    def start_board_event():
        return {
            'event_type': EventType.START_BOARD,
            'payload': {
                'board': BOARD,
            },
        }

    async def process(self, message: Message):
        if message.event_type == EventType.ONLINE_PLAYERS:
            return self.get_online_players()
        elif message.event_type == EventType.START_GAME:
            return await self.start_game(message)
        elif message.event_type == EventType.MOVE:
            return {}
        elif message.event_type == EventType.START_BOARD:
            return self.start_board_event()
        return {'event_type': None, 'payload': 'unsupported type'}
