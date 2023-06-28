from app.services.connect_manager import ConnectionManager
from app.services.game_manager import GameManager


async def connection_manager() -> ConnectionManager:
    return ConnectionManager()


async def game_manager() -> GameManager:
    return GameManager()
