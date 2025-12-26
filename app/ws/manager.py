from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def send(self, ws: WebSocket, msg: dict):
        await ws.send_text(json.dumps(msg))

    async def broadcast(self, msg: dict):
        for ws in self.active:
            try:
                await ws.send_text(json.dumps(msg))
            except:
                pass

ws_manager = ConnectionManager()