import uvicorn
from fastapi import FastAPI, Depends, Header
from starlette.middleware.cors import CORSMiddleware
from typing_extensions import Annotated

from app.services.chess_service import ChessService
from app.services.game_manager import GameManager
from web.dependecies import chess_service
from web.dependecies.common import game_manager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/search_games')
async def search_games(
    chess_service: Annotated[ChessService, Depends(chess_service)],
    name: Annotated[str, Header()],
):
    return await chess_service.search_game(name)


@app.get('/found_games')
async def found_games(
    chess_service: Annotated[ChessService, Depends(chess_service)],
    name: Annotated[str, Header()],
):
    return await chess_service.found_games(name)


@app.get("/ready_players")
async def get_active_connections(manager: Annotated[GameManager, Depends(game_manager)]):
    return manager.ready_players


if __name__ == "__main__":
    uvicorn.run('manage:app', host='localhost', port=9000, loop='asyncio')
