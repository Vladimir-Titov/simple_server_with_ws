from app.services.connect_manager import ConnectionManager


async def connection_manager() -> ConnectionManager:
    return ConnectionManager()
