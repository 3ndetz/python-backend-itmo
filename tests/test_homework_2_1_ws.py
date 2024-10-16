from http import HTTPStatus
from http.client import UNPROCESSABLE_ENTITY
from typing import Any
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
import asyncio
from httpx import AsyncClient
import websockets
import websocket
import json
import contextlib
import time
import threading
import uvicorn
import pytest
from faker import Faker
from fastapi.testclient import TestClient

from lecture_2.hw.ws_rooms import app
print('================ 0lol ================')
#client = TestClient(app)
print('================ lol ================')

import pytest
from fastapi.testclient import TestClient
import multiprocessing
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


def test_websocket_chat():
    config = Config("lecture_2.hw.ws_rooms:app", host="0.0.0.0", port=8000, log_level="info")
    server = Server(config=config)
    with server.run_in_thread():
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
