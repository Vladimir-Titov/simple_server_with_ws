import uvicorn
from fastapi import FastAPI, WebSocket, Depends
from starlette.websockets import WebSocketDisconnect
from typing_extensions import Annotated

from app import Message
from app.services.chess_service import ChessService
from app.services.connect_manager import ConnectionManager
from web.dependecies import chess_service
from web.dependecies.common import connection_manager

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    chess_service: Annotated[ChessService, Depends(chess_service)],
    manager: Annotated[ConnectionManager, Depends(connection_manager)],
):
    await manager.connect(websocket)
    try:
        while True:
            data = await manager.get_message(websocket)
            message = Message.parse_obj(data)
            result = await chess_service.process(message)
            await manager.reply(result, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/active_connections")
async def get_active_connections(manager: Annotated[ConnectionManager, Depends(connection_manager)]):
    return {'online': [(client.name, client.ready_to_game) for client in manager.active_connections.values()]}


if __name__ == "__main__":
    uvicorn.run('manage:app', host='0.0.0.0', port=80, loop='asyncio')
