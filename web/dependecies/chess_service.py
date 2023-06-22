from app.services.chess_service import ChessService


async def chess_service() -> ChessService:
    return ChessService()
