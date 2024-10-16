from fastapi import FastAPI, Response, WebSocket, HTTPException, status, Query, APIRouter
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from http import HTTPStatus
import uuid
import random


app = FastAPI()

# WebSocket Chat
chat_rooms = {}


from dataclasses import dataclass, field
from uuid import uuid4

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect

@dataclass(slots=True)
class Broadcaster:
    subscribers: list[WebSocket] = field(init=False, default_factory=list)

    async def subscribe(self, ws: WebSocket) -> None:
        await ws.accept()
        self.subscribers.append(ws)

    async def unsubscribe(self, ws: WebSocket) -> None:
        self.subscribers.remove(ws)

    async def publish(self, message: str) -> None:
        for ws in self.subscribers:
            await ws.send_text(message)


broadcaster = Broadcaster()


@app.post("/publish")
async def post_publish(request: Request):
    message = (await request.body()).decode()
    await broadcaster.publish(message)


@app.websocket("/subscribe")
async def ws_subscribe(ws: WebSocket):
    client_id = uuid4()
    await broadcaster.subscribe(ws)
    await broadcaster.publish(f"client {client_id} subscribed")

    try:
        while True:
            text = await ws.receive_text()
            await broadcaster.publish(text)
    except WebSocketDisconnect:
        await broadcaster.unsubscribe(ws)
        await broadcaster.publish(f"client {client_id} unsubscribed")

@app.websocket("/chat/{chat_name}")
async def websocket_endpoint(websocket: WebSocket, chat_name: str):
    await websocket.accept()
    if chat_name not in chat_rooms:
        chat_rooms[chat_name] = []

    username = f"User_{random.randint(1000, 9999)}"
    chat_rooms[chat_name].append((websocket, username))

    try:
        while True:
            data = await websocket.receive_text()
            for client, _ in chat_rooms[chat_name]:
                if client != websocket:
                    await client.send_text(f"{username} :: {data}")
    except WebSocketDisconnect:
        try:
            chat_rooms[chat_name].remove((websocket, username))
        except:
            pass
    finally:
        try:
            chat_rooms[chat_name].remove((websocket, username))
        except:
            pass
if __name__ == "__main__":
    # If you running test by debug and want to see output in rooms.
    #exit()
    import uvicorn
    import contextlib
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    from fastapi.testclient import TestClient
    from websocket import create_connection
    client = TestClient(app)
    print('================ lol ================')

    import pytest
    from fastapi.testclient import TestClient
    import multiprocessing
    import websockets
    import websocket
    import json
    import contextlib
    import time
    import threading
    import uvicorn
    import pytest
    from uvicorn import Config, Server


    class Server(uvicorn.Server):
        def install_signal_handlers(self):
            pass

        @contextlib.contextmanager
        def run_in_thread(self):
            thread = threading.Thread(target=self.run)
            thread.start()
            try:
                while not self.started:
                    time.sleep(1e-3)
                yield
            finally:
                self.should_exit = True
                thread.join()
    config = Config("ws_rooms:app", host="0.0.0.0", port=8000, log_level="info")
    server = Server(config=config)

    def test_websocket_chat():
        with server.run_in_thread():
            ws = websocket.create_connection("ws://localhost:8000/subscribe")
            print(ws.recv())
            r1 = "room1"
            r2 = "room2" 
            ws1 = websocket.create_connection(f"ws://localhost:8000/chat/{r1}")
            ws2 = websocket.create_connection(f"ws://localhost:8000/chat/{r1}")
            ws3 = websocket.create_connection(f"ws://localhost:8000/chat/{r2}")
            ws4 = websocket.create_connection(f"ws://localhost:8000/chat/{r2}")
            print(f"Sending from every user.")
            msg1 = "Hello from user 1"
            msg2 = "Hello from user 2"
            msg3 = "Hello from user 3"
            msg4 = "Hello from user 4"
            ws1.send_text(msg1)
            ws2.send_text(msg2)
            ws3.send_text(msg3)
            ws4.send_text(msg4)
            print(f"Sended.")
            print(f"Heared:")
            ans1 = ws1.recv()
            ans2 = ws2.recv()
            ans3 = ws3.recv()
            ans4 = ws4.recv()
            print(f"ws1 in {r1}", ans1)
            print(f"ws2 in {r1}", ans2)
            print(f"ws3 in {r2}", ans3)
            print(f"ws4 in {r2}", ans4)
            assert msg2 in ans1
            assert msg1 in ans2
            assert msg4 in ans3
            assert msg3 in ans4
    test_websocket_chat()
#    pass
#    exit()
#    import uvicorn
#    #uvicorn.run(app, host="0.0.0.0", port=8000)
#    from fastapi.testclient import TestClient
#    client = TestClient(app)
#    response = client.post("/cart")
#    print("DSKGL IDSJGKJSDHJG HSDKJHG KSDHG KDSFHG")
#    print(response)
#    
    
