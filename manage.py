import orjson
import uvicorn
from fastapi import FastAPI, WebSocket, Depends
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from typing_extensions import Annotated

from app import Message
from app.services.chess_service import ChessService
from app.services.connect_manager import ConnectionManager
from web.dependecies import chess_service
from web.dependecies.common import connection_manager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
            print('response from server: ', result)
            await manager.reply(result, websocket)
    except WebSocketDisconnect as err:
        manager.disconnect(websocket)
    except ValidationError:
        await websocket.send_text(orjson.dumps({
            'WebSocketError': {
                'message': 'unsupported event',
            }
        }))
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


@app.websocket("/echo")
async def echo_socket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f'echo from server: {data}')


@app.get("/active_connections")
async def get_active_connections(manager: Annotated[ConnectionManager, Depends(connection_manager)]):
    return {'online': [(client.name, client.ready_to_game) for client in manager.active_connections.values()]}


if __name__ == "__main__":
    uvicorn.run('manage:app', host='localhost', port=9000, loop='asyncio')
