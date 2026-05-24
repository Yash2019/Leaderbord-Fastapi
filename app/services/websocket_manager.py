from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, game_name: str, websocket: WebSocket):
        await websocket.accept()
        self.active[game_name].append(websocket)

    def disconnect(self, game_name: str, websocket: WebSocket):
        connections = self.active.get(game_name)

        if not connections:
            return

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            self.active.pop(game_name, None)

    async def broadcast(self, game_name: str, message: dict):
        connections = self.active.get(game_name, [])

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(game_name, websocket)


manager = ConnectionManager()